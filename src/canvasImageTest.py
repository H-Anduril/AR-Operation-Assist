from tkinter import *
from PIL import Image, ImageTk
import os

root = Tk()
root.geometry("1200x900")

frame = Frame(root)
frame.pack()

print("global reached")
c = Canvas(frame, width = 1700, height = 1700, bg = "white")
c.pack()



class MainFrame:
    def __init__(self, image0, image1 ):
        print("class reached")
        self.__image0 = image0
        self.__image1 = image1
        self.__x, self.__y = 250,250
        self.__picture0 = c.create_image( self.__x, self.__y,
                                          image =  self.__image0, tag="im0")
        self.__picture1 = c.create_image( self.__x, self.__y,
                                          image =  self.__image1, tag="im1")
        self.__move = False
        c.bind( "<Button-1>", self.startMovement)
        c.bind( "<ButtonRelease-1>", self.stopMovement)
        c.bind( "<Motion>", self.movement)

    def startMovement( self, event ):
        self.__move = True
        self.initi_x = c.canvasx(event.x) #Translate mouse x screen coordinate to canvas coordinate
        self.initi_y = c.canvasy(event.y) #Translate mouse y screen coordinate to canvas coordinate
        print('startMovement init', self.initi_x, self.initi_y)
        self.movingimage = c.find_closest(self.initi_x, self.initi_y, halo=5) # get canvas object ID of where mouse pointer is 
        print(self.movingimage)
        print(c.find_all()) # get all canvas objects ID 

    def stopMovement( self, event ):
        self.__move = False

    def movement( self, event ):
        if self.__move:
            end_x = c.canvasx(event.x) #Translate mouse x screen coordinate to canvas coordinate
            end_y = c.canvasy(event.y) #Translate mouse y screen coordinate to canvas coordinate
            print('movement end', end_x, end_y)
            deltax = end_x - self.initi_x #Find the difference
            deltay = end_y - self.initi_y
            print('movement delta', deltax, deltay)
            self.initi_x = end_x #Update previous current with new location
            self.initi_y = end_y
            print('movement init', self.initi_x, self.initi_y)
            # print(c.itemcget(self.movingimage, "filepath"))
            c.move(self.movingimage, deltax, deltay) # move object
            

if __name__ == "__main__":
    print("main reached")
    im0 = PhotoImage( file = r"C:\Users\hw1048\Documents\AR-Operation-Assist\data\Augmented Reality\images\1.png")     
    im1 = PhotoImage( file = r"C:\Users\hw1048\Documents\AR-Operation-Assist\data\Augmented Reality\images\screw.png")
    # im2 = PhotoImage( file = "giphy.gif" )
    m = MainFrame( im0, im1 )
    root.mainloop()