import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd, colorchooser, ttk
from tkinter.messagebox import showinfo
from tkinter.simpledialog import askstring
from PIL import Image, ImageTk
import pandas as pd
import io
import os
import math
import cv2
import numpy as np
import dbConnect

def open_eps(ps, dpi=300.0):
    img = Image.open(io.BytesIO(ps.encode('utf-8')))
    original = [float(d) for d in img.size]
    scale = dpi/72.0            
    if dpi != 0:
        img.load(scale = math.ceil(scale))
    if scale != 1:
        img.thumbnail([round(scale * d) for d in original], Image.LANCZOS)
    return img

# TODO: make creating shape a new page (essentially a new Class)
class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Test Application")
        self.geometry("1900x1000")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=1920, width=1080)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}

        self.idToImage = {}
        self.idToPhotoImage = {}
        self.idToTag = {}
        self.notMovableID = set()
        
        self.tagToPhotoImage = {}
        self.tagToImage = {}
        self.tagToID = {}
        self.tagToFileDir = {}
        
        self.dbPacket = None
        
        self.maxWidth = 1440
        self.maxHeight = 810
        
        # Scale images if needed
        self.scaleFactor = 1.0
        
        self.canvasSize = (0, 0)
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (DrawPage, CanvasConfigPage, NewShapePage, DBConfigPage, CRUDPage):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(DBConfigPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        if (cont is DrawPage):
            frame.reconfig_size()
        # raises the current frame to the top
        frame.tkraise()
        
class DBConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Database Config Page")
        label.pack(padx=10, pady=10)
        
        serverFrame = tk.Frame(self)
        serverFrame.pack()
        serverLabel = tk.Label(self, text="Server:   ")
        self.serverName = tk.Entry(self, bd=1)
        serverLabel.pack(in_=serverFrame, side=tk.LEFT)
        self.serverName.pack(in_=serverFrame, side=tk.LEFT, padx=1)
        
        dbFrame = tk.Frame(self)
        dbFrame.pack()
        dbLabel = tk.Label(self, text="Database: ")
        self.dbName = tk.Entry(self, bd=1)
        dbLabel.pack(in_=dbFrame, side=tk.LEFT)
        self.dbName.pack(in_=dbFrame, side=tk.LEFT, padx=1)
        
        usernameFrame = tk.Frame(self)
        usernameFrame.pack()
        usernameLabel = tk.Label(self, text="Username: ")
        self.usernameName = tk.Entry(self, bd=1)
        usernameLabel.pack(in_=usernameFrame, side=tk.LEFT)
        self.usernameName.pack(in_=usernameFrame, side=tk.LEFT, padx=1)
        
        passwordFrame = tk.Frame(self)
        passwordFrame.pack()
        passwordLabel = tk.Label(self, text="Password: ")
        self.passwordName = tk.Entry(self, bd=1)
        passwordLabel.pack(in_=passwordFrame, side=tk.LEFT)
        self.passwordName.pack(in_=passwordFrame, side=tk.LEFT, padx=1)
        
        confirm_button = tk.Button(
            self,
            text="Login",
            command=self.connectDB
        )
        confirm_button.pack()
        
        dev_button = tk.Button(
            self,
            text="Dev Login",
            command=self.connectDB_dev
        )
        dev_button.pack()
        
    def connectDB(self):
        server = self.serverName.get()
        db = self.dbName.get()
        username = self.usernameName.get()
        password = self.passwordName.get()
        dbConfig = dbConnect.dbConfig(server, db, username, password)
        self.controller.dbPacket = dbConnect.connect(dbConfig)
        if self.controller.dbPacket.isValid is False:
            showinfo(message="Connection Failed")
            return
        showinfo(message="Success")
        self.controller.show_frame(CRUDPage)
        
    def connectDB_dev(self):
        dbConfig = dbConnect.dbConfig(
            'S011DDB0003',
            'AR_GOA_POC',
            'AR_User',
            'T@@sM22n'
        )
        self.controller.dbPacket = dbConnect.connect(dbConfig)
        if self.controller.dbPacket.isValid is False:
            showinfo(message="Connection Failed")
            return
        showinfo(message="Success")
        self.controller.show_frame(CRUDPage)
        
class CRUDPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Database Operations Page")
        label.pack(padx=10, pady=10)
        
        # CRUD: Read Operations
        displayFrame = tk.Frame(self, pady=10)
        displayFrame.pack()
        
        display_product_button = tk.Button(
            self,
            text="display all products",
            command=self.display_products
        )
        
        display_operation_button = tk.Button(
            self,
            text="display all operations of a product",
            command=self.display_operations
        )
        
        display_steps_button = tk.Button(
            self,
            text="display all steps of an operation",
            command=self.display_steps
        )
        
        display_components_button = tk.Button(
            self,
            text="display all components",
            command=self.display_components
        )
        display_product_button.pack(in_=displayFrame, side=tk.LEFT)
        display_operation_button.pack(in_=displayFrame, side=tk.LEFT, padx=2)
        display_steps_button.pack(in_=displayFrame, side=tk.LEFT, padx=2)
        display_components_button.pack(in_=displayFrame, side=tk.LEFT, padx=2)
        
        # CRUD: Create Operations
        createFrame = tk.Frame(self)
        createFrame.pack(pady=10)
        
        create_product_button = tk.Button(
            self,
            text="add a new product",
            command=self.create_product
        )
        
        create_operation_button = tk.Button(
            self,
            text="add a new operation for a product",
            command=self.create_operation
        )
        
        create_steps_button = tk.Button(
            self,
            text="add a new step for an operation",
            command=self.create_step
        )
        
        create_components_button = tk.Button(
            self,
            text="add a new component",
            command=self.create_component
        )
        create_product_button.pack(in_=createFrame, side=tk.LEFT)
        create_operation_button.pack(in_=createFrame, side=tk.LEFT, padx=2)
        create_steps_button.pack(in_=createFrame, side=tk.LEFT, padx=2)
        create_components_button.pack(in_=createFrame, side=tk.LEFT, padx=2)
        
        # CRUD: Update Operations
        updateFrame = tk.Frame(self)
        updateFrame.pack(pady=10)
        
        update_product_button = tk.Button(
            self,
            text="update a product",
            command=self.update_product
        )
        
        update_operation_button = tk.Button(
            self,
            text="update an operation of a product",
            command=self.update_operation
        )
        
        update_steps_button = tk.Button(
            self,
            text="update a step of an operation",
            command=self.update_step
        )
        
        update_components_button = tk.Button(
            self,
            text="update a component",
            command=self.update_component
        )
        update_product_button.pack(in_=updateFrame, side=tk.LEFT)
        update_operation_button.pack(in_=updateFrame, side=tk.LEFT, padx=2)
        update_steps_button.pack(in_=updateFrame, side=tk.LEFT, padx=2)
        update_components_button.pack(in_=updateFrame, side=tk.LEFT, padx=2)
        
        # CRUD: Delete Operations
        deleteFrame = tk.Frame(self)
        deleteFrame.pack(pady=10)
        
        delete_product_button = tk.Button(
            self,
            text="delete a product",
            command=self.delete_product
        )
        
        delete_operation_button = tk.Button(
            self,
            text="delete an operation of a product",
            command=self.delete_operation
        )
        
        delete_steps_button = tk.Button(
            self,
            text="delete a step of an operation",
            command=self.delete_step
        )
        
        delete_components_button = tk.Button(
            self,
            text="delete a component",
            command=self.delete_component
        )
        delete_product_button.pack(in_=deleteFrame, side=tk.LEFT)
        delete_operation_button.pack(in_=deleteFrame, side=tk.LEFT, padx=2)
        delete_steps_button.pack(in_=deleteFrame, side=tk.LEFT, padx=2)
        delete_components_button.pack(in_=deleteFrame, side=tk.LEFT, padx=2)
        
        displayTableFrame = tk.Frame(self, width=800, height=400)
        displayTableFrame.pack(pady=20)
        horizontalScroll = Scrollbar(displayTableFrame, orient='horizontal')
        horizontalScroll.pack(side=tk.BOTTOM, fill=X)
        verticalScroll = Scrollbar(displayTableFrame, orient='vertical')
        verticalScroll.pack(side=tk.RIGHT, fill=Y)
        
        self.table = ttk.Treeview(displayTableFrame, yscrollcommand=verticalScroll.set, xscrollcommand=horizontalScroll.set)
        self.table.pack()
        verticalScroll.config(command=self.table.yview)
        horizontalScroll.config(command=self.table.xview)
    
    #CRUD: Read APIs
    def display_to_table(self, tableName: str, result: list):
        # remove existing records
        for i in self.table.get_children():
            self.table.delete(i)
            
        self.table['columns'] = tuple([col.column_name for col in self.controller.dbPacket.cursor.columns(table=tableName)])
        self.table.column("#0", width=0, stretch=NO)
        for col in self.table['columns']:
            self.table.column(col, anchor=CENTER, width=300, stretch=NO)
        self.table.heading("#0",text="",anchor=CENTER)
        for col in self.table['columns']:
            self.table.heading(col,text=col,anchor=CENTER)
        tableID = 0
        for row in result:
            self.table.insert(parent='',index='end',iid=tableID,text='', values=tuple(row))
            tableID += 1
            
    def display_products(self):
        result = self.controller.dbPacket.run_query_wResult(sql="select * from dbo.product")
        self.display_to_table('product', result)
    def display_operations(self):
        result = self.controller.dbPacket.run_query_wResult(sql="select * from dbo.operation")
        self.display_to_table('operation', result)
    def display_steps(self):
        result = self.controller.dbPacket.run_query_wResult(sql="select * from dbo.step")
        self.display_to_table('step', result)
    def display_components(self):
        result = self.controller.dbPacket.run_query_wResult(sql="select * from dbo.component")
        self.display_to_table('component', result)
    
    #CRUD: Create APIs
    def create_product(self):
        popup = Toplevel(self)
        popup.geometry("750x250")
        popup.title("Create a new product")
        
        productID_Frame = tk.Frame(popup)
        productID_Frame.pack(pady=10)
        pidLabel = tk.Label(popup, text="New Product ID:   ")
        popup.productID = tk.Entry(popup, bd=1)
        pidLabel.pack(in_=productID_Frame, side=tk.LEFT)
        popup.productID.pack(in_=productID_Frame, side=tk.LEFT, padx=1)
        
        pName_Frame = tk.Frame(popup)
        pName_Frame.pack(pady=10)
        pNameLabel = tk.Label(popup, text="New Product Name:   ")
        popup.pName = tk.Entry(popup, bd=1)
        pNameLabel.pack(in_=pName_Frame, side=tk.LEFT)
        popup.pName.pack(in_=pName_Frame, side=tk.LEFT, padx=1)
        
        create_product_button = tk.Button(
            popup,
            text="Add Product",
            command=lambda: self.confirm_product_add(popup)
        )
        create_product_button.pack(pady=10)
    
    def confirm_product_add(self, parent):
        res = self.controller.dbPacket.run_procedure("add_product", [parent.productID.get(), parent.pName.get()])
        if res == "Success":
            output = self.controller.dbPacket.write_query_result()
            showinfo(message=output[0][0])
        else:
            showinfo(message="Invalid Input.")
        self.controller.dbPacket.connection.commit()
        parent.destroy()
        
    def create_operation(self):
        popup = Toplevel(self)
        popup.geometry("750x250")
        popup.title("Create a new operation")
        
        productID_Frame = tk.Frame(popup)
        productID_Frame.pack(pady=10)
        pidLabel = tk.Label(popup, text="Product ID:   ")
        popup.productID = tk.Entry(popup, bd=1)
        pidLabel.pack(in_=productID_Frame, side=tk.LEFT)
        popup.productID.pack(in_=productID_Frame, side=tk.LEFT, padx=1)
        
        oidFrame = tk.Frame(popup)
        oidFrame.pack(pady=10)
        oidLabel = tk.Label(popup, text="New Operation ID:   ")
        popup.oid = tk.Entry(popup, bd=1)
        oidLabel.pack(in_=oidFrame, side=tk.LEFT)
        popup.oid.pack(in_=oidFrame, side=tk.LEFT, padx=1)
        
        oNameFrame = tk.Frame(popup)
        oNameFrame.pack(pady=10)
        oNameLabel = tk.Label(popup, text="New Operation ID:   ")
        popup.oName = tk.Entry(popup, bd=1)
        oNameLabel.pack(in_=oNameFrame, side=tk.LEFT)
        popup.oName.pack(in_=oNameFrame, side=tk.LEFT, padx=1)
        
        create_operation_button = tk.Button(
            popup,
            text="Add Product",
            command=lambda: self.confirm_operation_add(popup)
        )
        create_operation_button.pack(pady=10)
        
    def confirm_operation_add(self, parent):
        res = self.controller.dbPacket.run_procedure("add_operation", [parent.oid.get(), parent.productID.get(), parent.oName.get()])
        if res == "Success":
            output = self.controller.dbPacket.write_query_result()
            showinfo(message=output[0][0])
        else:
            showinfo(message="Invalid Input.")
        self.controller.dbPacket.connection.commit()
        parent.destroy()
    def create_step(self):
        self.controller.show_frame(CanvasConfigPage)
    def create_component(self):
        self.controller.show_frame(NewShapePage)
        
    #CRUD: Update APIs
    def update_product(self):
        pass
    def update_operation(self):
        pass
    def update_step(self):
        pass
    def update_component(self):
        pass
    
    #CRUD: Delete APIs
    def delete_product(self):
        pass
    def delete_operation(self):
        pass
    def delete_step(self):
        pass
    def delete_component(self):
        pass
    
class DrawPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Draw Page")
        label.pack(padx=10, pady=10)
        self.controller = controller
        self.scene = Canvas(self, width=self.controller.canvasSize[0], height=self.controller.canvasSize[1], bg="white", highlightthickness=1, highlightbackground="black")
        self.scene.pack()
        
        self.currImgConfigInfo = tk.Label(self, text="")
        self.currImgConfigInfo.pack()
        
        self.scene.bind("<Button-1>", self.startMovement)
        self.scene.bind("<Button-3>", self.deleteImage)
        self.scene.bind("<ButtonRelease-1>", self.stopMovement)
        self.scene.bind("<Motion>", self.movement)
        self.scene.bind("<MouseWheel>", self.resize)
        
        self.cursorX = 0
        self.cursorY = 0
        
        self.move = False
        
        inputFrame = Frame(self)
        inputFrame.pack()
        self.inputtext = Entry(self, width=30)
        inputLabel = Label(self, text="Image Tag")
        inputLabel.pack(in_=inputFrame, side=tk.LEFT)
        self.inputtext.pack(in_=inputFrame, side=tk.LEFT, padx=1)
        
        buttonsFrame = tk.Frame(self)
        buttonsFrame.pack(pady=5)
        
        load_file_button = tk.Button(
            self,
            text="Load File",
            command=self.load_file,
        )
        
        prev_button = tk.Button(
            self,
            text="Reconfig canvas size",
            command=self.back_to_CanvasConfig,
        )
        
        save_scene_button = tk.Button(
            self,
            text="Save Current Canvas scene",
            command=self.save_canvas,
        )
        
        draw_shape_button = tk.Button(
            self,
            text="Create New Shape",
            command=self.switch_NewShapePage,
        )
        
        back_to_CRUD_button = tk.Button(
            self,
            text="Back to Main Page",
            command=lambda: self.controller.show_frame(CRUDPage)
        )

        
        load_file_button.pack(in_=buttonsFrame, side=tk.LEFT)
        draw_shape_button.pack(in_=buttonsFrame, side=tk.LEFT, padx=1)
        prev_button.pack(in_=buttonsFrame, side=tk.LEFT, padx=1)
        save_scene_button.pack(in_=buttonsFrame, side=tk.LEFT, padx=1)
        back_to_CRUD_button.pack(in_=buttonsFrame, side=tk.LEFT, padx=1)
    

    def update_currInfo(self, event, reset=False):
        if reset:
            self.currImgConfigInfo.config(text="")
            return
        target = self.scene.find_closest(self.scene.canvasx(event.x), self.scene.canvasx(event.y), halo=5)
        print(target)
        if target == ():
            return
        self.currImgConfigInfo.config(text=
                              "Current Image/Shape Tag: {} | Current Image/Shape Center Coordinates (x, y): {} | Current Image Size: {}"
                              .format(self.controller.idToTag[target[0]],
                                        self.scene.coords(target[0]),
                                        [(self.scene.bbox(target[0])[2] - self.scene.bbox(target[0])[0]), 
                                        (self.scene.bbox(target[0])[3] - self.scene.bbox(target[0])[1])]))
        
    def load_file(self):
        tag = self.inputtext.get()
        file_path = fd.askopenfilename()
        if (len(tag) == 1):
            showinfo(message="missing tag")
            return
        if file_path == '':
            showinfo(message="file not selected")
            return
        tag = tag[:-1]
        if tag in self.controller.tagToFileDir or tag in self.controller.tagToID:
            showinfo(message="Tag already exists")
            return
        self.controller.tagToFileDir[tag] = file_path
        showinfo(message="success")
        self.inputtext.delete()
        self.presentImage(tag)
        
    def reconfig_size(self):
        self.scene.config(width=self.controller.canvasSize[0], height=self.controller.canvasSize[1])
        
    def presentImage(self, tag):
        print(self.controller.tagToFileDir[tag])
        newImage = Image.open(self.controller.tagToFileDir[tag])
        newPhotoImage = ImageTk.PhotoImage(newImage)
        # newPhotoImage = ImageTk.PhotoImage(file=self.controller.tagToFileDir[tag])
        # newImage = newImage.zoom(0.5, 0.5)
        self.controller.tagToPhotoImage[tag] = newPhotoImage
        self.controller.tagToImage[tag] = newImage
        id = self.scene.create_image(250, 250, anchor=CENTER, image=newPhotoImage)
        self.controller.idToPhotoImage[id] = newPhotoImage
        self.controller.idToImage[id] = newImage
        self.controller.idToTag[id] = tag
        self.controller.tagToID[tag] = id
        # self.scene.itemconfig(id, image=newImage)
        print(id)
        
    def startMovement(self, event):
        self.initi_x = self.scene.canvasx(event.x) #Translate mouse x screen coordinate to canvas coordinate
        self.initi_y = self.scene.canvasy(event.y) #Translate mouse y screen coordinate to canvas coordinate
        print('startMovement init', self.initi_x, self.initi_y)
        self.movingimage = self.scene.find_closest(self.initi_x, self.initi_y, halo=5) # get canvas object ID of where mouse pointer is 
        if self.movingimage != () and self.movingimage[0] not in self.controller.notMovableID:
            self.move = True
        print(self.movingimage)
        print(self.scene.find_all()) # get all canvas objects ID
        self.update_currInfo(event) 

    def stopMovement(self, event):
        self.move = False

    def movement(self, event):
        self.cursorX = self.scene.canvasx(event.x)
        self.cursorY = self.scene.canvasy(event.y)
        if self.move:
            # end_x = self.scene.canvasx(event.x) #Translate mouse x screen coordinate to canvas coordinate
            # end_y = self.scene.canvasy(event.y) #Translate mouse y screen coordinate to canvas coordinate
            print('movement end', self.cursorX, self.cursorY)
            deltax = self.cursorX - self.initi_x #Find the difference
            deltay = self.cursorY - self.initi_y
            print('movement delta', deltax, deltay)
            self.initi_x = self.cursorX #Update previous current with new location
            self.initi_y = self.cursorY
            print('movement init', self.initi_x, self.initi_y)
            # print(c.itemcget(self.movingimage, "filepath"))
            self.scene.move(self.movingimage, deltax, deltay) # move object
            self.scene.tag_raise(self.movingimage)
            self.update_currInfo(event)
        
    def resize(self, event):
        #if not self.objOutOfBound():
        if True:
            movingimg = self.scene.find_closest(self.cursorX, self.cursorY, halo=5)
            x = self.scene.canvasx(event.x)
            y = self.scene.canvasy(event.y)
            print(movingimg)
            id = movingimg[0]
            img_w, img_h = self.controller.idToImage[id].size
            if (event.delta == -120):
                newImage = self.controller.idToImage[id].resize((img_w * 9 // 10 - 5, img_h * 9 // 10 - 5))
                # self.scene.scale(movingimg, x, y, 0.9, 0.9)
            elif (event.delta == 120):
                newImage = self.controller.idToImage[id].resize((img_w * 11 // 10 + 5, img_h * 11 // 10 + 5))
                # self.scene.scale(movingimg, x, y, 1.1, 1.1)
            newPhotoImage = ImageTk.PhotoImage(newImage)
            self.scene.itemconfig(id, image=newPhotoImage)
            self.controller.idToImage[id] = newImage
            self.controller.idToPhotoImage[id] = newPhotoImage
            self.update_currInfo(event)

    def deleteImage(self, event):
        movingimg = self.scene.find_closest(self.cursorX, self.cursorY, halo=5)
        id = movingimg[0]
        self.scene.delete(id)
        del self.controller.idToImage[id]
        del self.controller.idToPhotoImage[id]
        tag = self.controller.idToTag[id]
        del self.controller.idToTag[id]

        del self.controller.tagToPhotoImage[tag]
        del self.controller.tagToImage[tag]
        del self.controller.tagToID[tag]
        del self.controller.tagToFileDir[tag]
        self.update_currInfo(event, reset=True)
    
    def objOutOfBound(self):
        if (self.scene.bbox(self.movingimage)[0] < 0
            or self.scene.bbox(self.movingimage)[1] < 0
            or self.scene.bbox(self.movingimage)[2] > self.controller.canvasSize[0]
            or self.scene.bbox(self.movingimage)[3] > self.controller.canvasSize[1]):
            return True
        return False
        
    def back_to_CanvasConfig(self):
        self.controller.idToImage = {}
        self.controller.idToPhotoImage = {}
        self.controller.idToTag = {}
        self.controller.tagToPhotoImage = {}
        self.controller.tagToImage = {}
        self.controller.tagToID = {}
        self.controller.tagToFileDir = {}
        self.controller.canvasSize = (0, 0)
        self.scene.delete("all")
        self.controller.show_frame(CanvasConfigPage)
    
    def switch_NewShapePage(self):
        self.controller.show_frame(NewShapePage)
    
    def save_canvas(self):
        if len(self.scene.find_all()) == 0:
            showinfo(message="Empty scene")
            return
        name = askstring('csvName', 'Name of output csv file')
        if name == "":
            showinfo(message="Invalid output file name")
            return
        result = {'Scene Width': self.controller.canvasSize[0],
                  'Scene Height': self.controller.canvasSize[1],
                  'Tag': [],
                  'x coord': [],
                  'y coord': [],
                  'width': [],
                  'height': [],
                  'File Location': []}
        for id in self.scene.find_all():
            tag = self.controller.idToTag[id]
            result['Tag'].append(tag)
            result['x coord'].append(self.scene.coords(id)[0])
            result['y coord'].append(self.scene.coords(id)[1])
            result['width'].append(self.scene.bbox(id)[2] - self.scene.bbox(id)[0])
            result['height'].append(self.scene.bbox(id)[3] - self.scene.bbox(id)[1])
            result['File Location'].append(self.controller.tagToFileDir[tag])
        df = pd.DataFrame(data=result)
        df.to_csv('../output/sheets/{}.csv'.format(name), index=False)
        showinfo(message="Successfully saved")

    def __str__(self):
        return "DrawPage"
        
class CanvasConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Canvas Size Config Page")
        label.pack(padx=10, pady=10)
        
        widthFrame = Frame(self)
        widthFrame.pack(pady=10)
        
        labelWidth = Label(self, text="Type Canvas Width (in mm)")
        self.inputWidth = Entry(self, width=10)
        
        labelWidth.pack(in_=widthFrame, side=tk.LEFT)
        self.inputWidth.pack(in_=widthFrame, side=tk.LEFT, padx=1)
        
        heightFrame = Frame(self)
        heightFrame.pack(pady=10)
        
        labelHeight = Label(self, text="Type Canvas Height (in mm)")
        self.inputHeight = Entry(self, width=10)
        labelHeight.pack(in_=heightFrame, side=tk.LEFT)
        self.inputHeight.pack(in_=heightFrame, side=tk.LEFT, padx=1)
        
        confirm_button = tk.Button(
            self,
            text="Confirm Canvas Config",
            command=self.saveCanvasConfig
        )
        confirm_button.pack()
        
        switch_button = tk.Button(
            self,
            text="Start Drawing",
            command=self.switchToDrawPage
        )
        switch_button.pack()
        
        back_to_CRUD_button = tk.Button(
            self,
            text="Back to Main Page",
            command=lambda: self.controller.show_frame(CRUDPage)
        )
        back_to_CRUD_button.pack()
        
    def switchToDrawPage(self):
        if (type(self.controller.canvasSize[0]) != int
                or type(self.controller.canvasSize[1]) != int 
                or self.controller.canvasSize[0] == 0 
                or self.controller.canvasSize[1] == 0):
            showinfo(message="Invalid Canvas Size")
            return
        self.controller.show_frame(DrawPage)
        
    def saveCanvasConfig(self):
        canvasWidth = self.inputWidth.get()
        canvasHeight = self.inputHeight.get()
        if (not canvasHeight.replace(".", "").isnumeric() or not canvasWidth.replace(".", "").isnumeric()):
            showinfo(message="Invalid Input")
            return
        canvasWidth = float(canvasWidth)
        canvasHeight = float(canvasHeight)
        if (canvasHeight == 0.0 or canvasWidth == 0.0):
            showinfo(message="Invalid Canvas Size")
            return
        # Determine scale factor if physical workstation size exceeds maximum size of canvas
        if canvasWidth <= self.controller.maxWidth and canvasHeight <= self.controller.maxHeight:
            self.controller.canvasSize = (int(canvasWidth), int(canvasHeight))
        elif ((canvasWidth <= self.controller.maxWidth and canvasHeight > self.controller.maxHeight) 
              or (canvasWidth - self.controller.maxWidth < canvasHeight - self.controller.maxHeight)):
            self.controller.scaleFactor = self.controller.maxHeight / canvasHeight
            self.controller.canvasSize = (int(canvasWidth * self.controller.scaleFactor), self.controller.maxHeight)
        elif ((canvasWidth > self.controller.maxWidth and canvasHeight <= self.controller.maxHeight) 
            or (canvasWidth - self.controller.maxWidth >= canvasHeight - self.controller.maxHeight)):
            
            self.controller.scaleFactor = self.controller.maxWidth / canvasWidth
            self.controller.canvasSize = (self.controller.maxWidth, int(canvasHeight * self.controller.scaleFactor))
        
        showinfo(message="canvas width: {} | canvas height: {} | Scale Factor: {}".format(
            self.controller.canvasSize[0],
            self.controller.canvasSize[1],
            self.controller.scaleFactor))
            
    
    def __str__(self):
        return "CanvasConfigPage"

class NewShapePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Create New Item Page")
        label.pack(padx=10, pady=10)
        self.controller = controller
        self.scene = Canvas(self, width=self.controller.canvasSize[0], height=self.controller.canvasSize[1], bg="white", highlightthickness=1, highlightbackground="black")
        self.scene.pack()
        
        self.itemWidth = 0.0
        self.itemHeight = 0.0
        
        scene_config_button = tk.Button(
            self,
            text="Config Item Size",
            command=self.config_item_size,
        )
        
        create_item_button = tk.Button(
            self,
            text="Create New Item",
            command=self.create_new_shape,
        )
        
        save_item_button = tk.Button(
            self,
            text="Save Shape",
            command=self.save_shape,
        )
        scene_config_button.pack()
        create_item_button.pack()
        save_item_button.pack()
        back_to_CRUD_button = tk.Button(
            self,
            text="Back to Main Page",
            command=lambda: self.controller.show_frame(CRUDPage)
        )
        back_to_CRUD_button.pack()
    
    def config_item_size(self):
        popup = Toplevel(self)
        popup.geometry("750x250")
        popup.title("Shape Config")
        popup.inputWidth = Text(popup, height=1, width=5)
        popup.inputWidth.pack()
        
        labelWidth = Label(popup, text="Type Item Width above")
        labelWidth.pack()
        
        popup.inputHeight = Text(popup, height=1, width=5)
        popup.inputHeight.pack()
        
        labelHeight = Label(popup, text="Type Item Height above")
        labelHeight.pack()
        
        confirm_button = tk.Button(
            popup,
            text="Confirm Item Size",
            command=lambda: self.set_item_size(popup)
        )
        confirm_button.pack()
        
    def set_item_size(self, configWindow):
        itemWidth = configWindow.inputWidth.get(1.0, "end")[:-1]
        itemHeight = configWindow.inputHeight.get(1.0, "end")[:-1]
        try:
            itemWidth = float(itemWidth)
            itemHeight = float(itemHeight)
        except ValueError:
            showinfo(message="Invalid Input")
            return

        if (itemHeight == 0.0 or itemWidth == 0.0):
            showinfo(message="Invalid Canvas Size")
            return
        self.itemWidth = itemWidth
        self.itemHeight = itemHeight
        self.scene.config(height=int(self.itemHeight), width=int(self.itemWidth))
        showinfo(message="Success")
        configWindow.destroy()
        
    def create_new_shape(self):
        popup = Toplevel(self)
        popup.geometry("750x250")
        popup.title("Shape Config")
        
        popup.color = ((0, 0, 0), '#000000') # initialized to be black
        
        colorFrame = tk.Frame(popup)
        colorFrame.pack()
        
        color_label = tk.Label(popup, bg=popup.color[-1],height=1, width=2)
        popup.color_label = color_label
        
        color_picker = tk.Button(
            popup,
            text="Pick color",
            command=lambda: self.choose_color(popup)
        )
        
        curr_color = tk.Label(popup, text="Current Color:")
 
        color_picker.pack(in_=colorFrame, side=tk.LEFT, pady=20)
        curr_color.pack(in_=colorFrame, side=tk.LEFT, padx=5)
        color_label.pack(in_=colorFrame, side=tk.LEFT, padx=1)

        shapeLabel = tk.Label(popup, text="Input Coordinates of Points to create new shape\nForm: x1, y1, x2, y2, ...")
        #shapes = Entry(popup, width=50)
        shapes = Text(popup, height=3, width=50)
        shapeLabel.pack()
        shapes.focus_set()
        popup.shapes = shapes
        shapes.pack()
        
        tagFrame = tk.Frame(popup)
        tagFrame.pack()
        
        tagLabel = tk.Label(popup, text="Tag of the new shape")
        tagEntry = Entry(popup)
        tagLabel.pack(in_=tagFrame, side=tk.LEFT)
        tagEntry.pack(in_=tagFrame, side=tk.LEFT, padx=1)
        
        popup.tagEntry = tagEntry
        
        popup.isSmooth = tk.IntVar()
        smooth = tk.Checkbutton(popup, text="Draw Curve", variable=popup.isSmooth, onvalue=1, offvalue=0)
        smooth.pack()
        
        confirm_button = tk.Button(
            popup,
            text="Generate Shape",
            command=lambda: self.generate_shape(popup)
        )
        confirm_button.pack()
    
    def generate_shape(self, configWindow):
        points = configWindow.shapes.get(1.0, "end")
        try:
            points = points[:-1].split(",")
            points = list(map(float, points))
        except ValueError:
            showinfo(message="Invalid Input")
            configWindow.shapes.delete(1.0, "end")
            return
            
        if len(points) < 4 or len(points) % 2 == 1:
            showinfo(message="Not Enough Input")
            configWindow.shapes.delete(1.0, "end")
            return
        
        print(points)
        print(configWindow.isSmooth.get())
        id = self.scene.create_line(points, fill=configWindow.color[-1], smooth=configWindow.isSmooth.get())
        tag = configWindow.tagEntry.get()
        print(tag)
        configWindow.destroy()
        
    def save_shape(self):
        if len(self.scene.find_all()) == 0:
            showinfo(message="Empty scene")
            return
        name = askstring('csvName', 'Name of output csv file')
        if name == "":
            showinfo(message="Invalid output file name")
            return
        ps = self.scene.postscript(colormode="color", pagewidth=self.itemWidth-1, pageheight=self.itemHeight-1)
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        # im = open_eps(ps, dpi=119.5)
        image_fileName = "/output/images/{}.png".format(name)
        # im.save(".." + image_fileName, dpi=(119.5, 119.5))
        img.save(".." + image_fileName)
        showinfo(message="Success")
    
    def choose_color(self, parent):
        parent.color = colorchooser.askcolor(parent=parent, title="Choose color")
        parent.color_label.config(bg=parent.color[-1])
            
        
if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()