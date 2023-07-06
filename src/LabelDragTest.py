from tkinter import *
import tkinter
from PIL import Image, ImageTk

window = Tk()

window.wm_attributes('-transparentcolor', 'black')

def drag_start(event):
    event.widget.startX = event.x
    event.widget.startY = event.y

def drag_motion(event):
    x = event.widget.winfo_x() - event.widget.startX + event.x
    y = event.widget.winfo_y() - event.widget.startY + event.y
    event.widget.place(x=x, y=y)

image1 = Image.open(r"C:\Users\hw1048\Documents\AR-Operation-Assist\data\Augmented Reality\images\screw.png")
imageObj = ImageTk.PhotoImage(image1)

image2 = image1 = Image.open(r"C:\Users\hw1048\Documents\AR-Operation-Assist\data\Augmented Reality\images\2.png")
imageObj2 = ImageTk.PhotoImage(image2)

label2 = tkinter.Label(window, image=imageObj2)
label1 = tkinter.Label(window, image=imageObj)


label1.bind("<Button-1>", drag_start)
label1.bind("<B1-Motion>", drag_motion)

label2.bind("<Button-1>", drag_start)
label2.bind("<B1-Motion>", drag_motion)

label1.place(x=100, y=50)
label2.place(x=200, y=100)

window.mainloop()