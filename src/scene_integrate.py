import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('1920x1080')

imageObj1 = None
image = None

def select_image(): 
    global imageObj1
    global image
    # ask the user for the filename
    file_path = fd.askopenfilename()

    # only show the image if they chose something
    if file_path:
        # open the file
        image = Image.open(file_path)

        # create the image object, and save it so that it
        # won't get deleted by the garbage collector
        imageObj1 = ImageTk.PhotoImage(image)

        # configure the canvas item to use this image
        canvas.itemconfigure(image_id, image=imageObj1)
        
my_label = Label(root, text="")
def move(e):
    global imageObj1, image
    imageObj1 = ImageTk.PhotoImage(image)
    image_id = canvas.create_image(e.x, e.y, image=imageObj1)
    my_label.config(text="Coor: x|" + str(e.x) + " y|" + str(e.y))

w = 1000
h = 1000
canvas = Canvas(root, width = w, height = h, bg="white")
canvas.place(x=50, y=50)
canvas.bind('<B1-Motion>', move)
image_id = canvas.create_image(0,0, anchor="nw")


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_image
)
open_button.place(x=65, y=600)



root.mainloop()


# cv.postscript(file="circles.eps")
#     from PIL import Image
#     img = Image.open("circles.eps")
#     img.save("circles.png", "png")