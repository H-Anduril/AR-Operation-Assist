import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # Adding a title to the window
        self.wm_title("Test Application")
        self.geometry("1200x900")

        # creating a frame and assigning it to container
        container = tk.Frame(self, height=1920, width=1080)
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        self.tagToFileDir = {}
        self.tagToPhotoImage = {}
        self.canvasSize = (0, 0)
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (DrawPage, CanvasConfigPage, CompletionScreen):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Using a method to switch frames
        self.show_frame(CanvasConfigPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        if (cont is DrawPage):
            frame.reconfig_size()
        # raises the current frame to the top
        frame.tkraise()
        
class DrawPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Draw Page")
        label.pack(padx=10, pady=10)
        self.controller = controller
        self.scene = Canvas(self, width=self.controller.canvasSize[0], height=self.controller.canvasSize[1], bg="white", highlightthickness=1, highlightbackground="black")
        self.scene.pack()
        
        self.scene.bind( "<Button-1>", self.startMovement)
        self.scene.bind( "<ButtonRelease-1>", self.stopMovement)
        self.scene.bind( "<Motion>", self.movement)
        self.move = False
        
        self.inputtext = Text(self, height=5, width=100)
        self.inputtext.pack()
        inputLabel = Label(self, text="input image tag here")
        inputLabel.pack()
        
        load_file_button = tk.Button(
            self,
            text="Load File",
            command=self.load_file,
        )

        switch_window_button = tk.Button(
            self,
            text="Next Window",
            command=lambda: controller.show_frame(CompletionScreen),
        )
        
        switch_window_button.pack(side="bottom", fill=tk.X)
        load_file_button.pack()
        
    def load_file(self):
        tag = self.inputtext.get(1.0, "end")
        file_path = fd.askopenfilename()
        if (len(tag) == 1):
            showinfo(message="missing tag")
            return
        self.controller.tagToFileDir[tag] = file_path
        showinfo(message="success")
        self.inputtext.delete(1.0, "end")
        self.presentImage(tag)
        
    def reconfig_size(self):
        self.scene.config(width=self.controller.canvasSize[0], height=self.controller.canvasSize[1])
        
    def presentImage(self, tag):
        print(self.controller.tagToFileDir[tag])
        newImage = ImageTk.PhotoImage(file=self.controller.tagToFileDir[tag])
        # newImage = newImage.zoom(0.5, 0.5)
        self.controller.tagToPhotoImage[tag] = newImage
        id = self.scene.create_image(250, 250, anchor=NW, image=newImage)
        # self.scene.itemconfig(id, image=newImage)
        print(id)
        
    def startMovement(self, event):
        self.move = True
        self.initi_x = self.scene.canvasx(event.x) #Translate mouse x screen coordinate to canvas coordinate
        self.initi_y = self.scene.canvasy(event.y) #Translate mouse y screen coordinate to canvas coordinate
        print('startMovement init', self.initi_x, self.initi_y)
        self.movingimage = self.scene.find_closest(self.initi_x, self.initi_y, halo=5) # get canvas object ID of where mouse pointer is 
        print(self.movingimage)
        print(self.scene.find_all()) # get all canvas objects ID 

    def stopMovement(self, event):
        self.move = False

    def movement( self, event ):
        if self.move:
            end_x = self.scene.canvasx(event.x) #Translate mouse x screen coordinate to canvas coordinate
            end_y = self.scene.canvasy(event.y) #Translate mouse y screen coordinate to canvas coordinate
            print('movement end', end_x, end_y)
            deltax = end_x - self.initi_x #Find the difference
            deltay = end_y - self.initi_y
            print('movement delta', deltax, deltay)
            self.initi_x = end_x #Update previous current with new location
            self.initi_y = end_y
            print('movement init', self.initi_x, self.initi_y)
            # print(c.itemcget(self.movingimage, "filepath"))
            self.scene.move(self.movingimage, deltax, deltay) # move object
        
    def __str__(self):
        return "DrawPage"
        
class CanvasConfigPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the Canvas Size Config Page")
        label.pack(padx=10, pady=10)
        
        self.inputWidth = Text(self, height=1, width=5)
        self.inputWidth.pack()
        
        labelWidth = Label(self, text="Type Canvas Width above")
        labelWidth.pack()
        
        self.inputHeight = Text(self, height=1, width=5)
        self.inputHeight.pack()
        
        labelHeight = Label(self, text="Type Canvas Height above")
        labelHeight.pack()
        
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
        
        # switch_window_button = tk.Button(
        #     self,
        #     text="Go to the Draw Screen",
        #     command=lambda: controller.show_frame(DrawPage),
        # )
        # switch_window_button.pack(side="bottom", fill=tk.X)
        
    def switchToDrawPage(self):
        if (type(self.controller.canvasSize[0]) != int
                or type(self.controller.canvasSize[1]) != int 
                or self.controller.canvasSize[0] == 0 
                or self.controller.canvasSize[1] == 0):
            showinfo(message="Invalid Canvas Size")
            return
        self.controller.show_frame(DrawPage)
        
    def saveCanvasConfig(self):
        canvasWidth = self.inputWidth.get(1.0, "end")[:-1]
        canvasHeight = self.inputHeight.get(1.0, "end")[:-1]
        if (not canvasHeight.isdigit() or not canvasWidth.isdigit()):
            showinfo(message="Invalid Input")
            return
        canvasWidth = int(canvasWidth)
        canvasHeight = int(canvasHeight)
        if (canvasHeight == 0 or canvasWidth == 0):
            showinfo(message="Invalid Canvas Size")
            return
        self.controller.canvasSize = (canvasWidth, canvasHeight)
        showinfo(message="canvas width: {} | canvas height: {}".format(self.controller.canvasSize[0], self.controller.canvasSize[1]))
    
    def __str__(self):
        return "CanvasConfigPage"


class CompletionScreen(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Completion Screen, we did it!")
        label.pack(padx=10, pady=10)
        switch_window_button = ttk.Button(
            self, text="Return to menu", command=lambda: controller.show_frame(CanvasConfigPage)
        )
        switch_window_button.pack(side="bottom", fill=tk.X)
        
    def __str__(self):
        return "CompletionScreen"
    
        
if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()