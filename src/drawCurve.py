from tkinter import *
master = Tk()
w = Canvas(master, width=200, height=100)
w.pack()
a = [50, 10, 50, 50, 100, 50]
# w.create_line([150, 0, 100, 50], smooth=1)
# w.create_line([150, 0, 100, 50, 50, 0], smooth=1)
w.create_line(a, smooth=1)

mainloop()

# # Import the required libraries
# from tkinter import *
# from tkinter import ttk

# # Create an instance of tkinter frame or window
# win=Tk()

# # Set the size of the window
# win.geometry("700x350")

# # Define a function to draw the line between two points
# def draw_line(event):
#    global click_num
#    global x1,y1
#    if click_num==0:
#       x1=event.x
#       y1=event.y
#       click_num=1
#    else:
#       x2=event.x
#       y2=event.y
#    # Draw the line in the given co-ordinates
#    canvas.create_line(x1,y1,x2,y2, fill="green", width=10)

# # Create a canvas widget
# canvas=Canvas(win, width=700, height=350, background="white")
# canvas.grid(row=0, column=0)
# canvas.bind('<Button-1>', draw_line)
# click_num=0

# win.mainloop()