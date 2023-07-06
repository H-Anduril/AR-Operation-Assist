import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
from PIL import Image, ImageTk

root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.geometry('1920x1080')

window = Frame(root)
window.pack()

file_paths = {}

def select_file():
    tag = inputtext.get(1.0, "end")
    file_path = fd.askopenfilename()
    file_paths[tag] = file_path
    result = ""
    for t in file_paths:
        result = result + "tag: " + t + " location: " + file_paths[t]
    showinfo(message=result)
    showinfo(message="success")
    inputtext.delete(1.0, "end")

inputtext = Text(window, height=5, width=100)
inputtext.pack()

open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack()

root.mainloop()