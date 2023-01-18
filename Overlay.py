# Standard Library
import sys
import os
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import keyboard
from screeninfo import get_monitors

class myOverlay:
    """
    Creates an overlay window using tkinter
    Uses the "-topmost" property to always stay on top of other Windows
    """

    def __init__(self,
                update_frequency_ms: int = 5_000, xpos: int = 0, ypos: int = 0,  LST: list = ((0, 0, 0, 0)), path: str = "crossHair.png", ROOT = 0):
        self.update_frequency_ms = update_frequency_ms
        self.root = Toplevel(ROOT)
        path = os.getcwd() + "\\images\\" +  path
        print(os.getcwd())
        self.defaultImage = Image.open(path)
        self.updating_Image = ImageTk.PhotoImage(self.defaultImage)
        self.updating_Image_level = tk.Label(
            self.root,
            image=self.updating_Image
        )
        self.updating_Image_level.place(x = -2, y = -2)

        # Define Window Geometery
        self.root.overrideredirect(True)
        self.relativeXpos = int(xpos - self.defaultImage.width/2)
        self.relativeYpos = int(ypos - self.defaultImage.height/2 -3)
        self.newPos = str(self.defaultImage.width) + "x" + str(self.defaultImage.height) + "+" + str(self.relativeXpos) + "+" + str(self.relativeYpos)
        print(self.newPos)
        self.root.geometry(self.newPos)
        self.root.lift()
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.wm_attributes("-topmost", True)



    def display(self, myList):
        screenShot = ImageGrab.grab(myList) #x, y, w, h
        return screenShot


    def update_Image(self) -> None:
        if keyboard.is_pressed('='):
            self.updating_Image = ImageTk.PhotoImage(self.defaultImage)
            self.updating_Image_level.configure(image = self.updating_Image)
            self.updating_Image_level.image = self.updating_Image
        elif keyboard.is_pressed('|'):
            sys.exit()

    def update_label(self) -> None:
        self.update_Image()        
        self.root.after(self.update_frequency_ms, self.update_label)


    def run(self) -> None:
        self.root.after(0, self.update_label)
        self.root.mainloop()

def example_callback():
    return 1
    # return str(datetime.now())


def get_monInfo():
    for m in get_monitors():
        print(m)
        if ((str(m)[str(m).index('name')+ 13:str(m).index('name')+ 21]) == 'DISPLAY4'):
            return True
    return False

def setup(Crosshair_Path: str, root):
    lst = list
    xpos = 0
    ypos = 0
    # sets the x,y,width, and height of the screencapture box 
    if get_monInfo() == True:
        print("POG")
        lst = list((457, 255, 610, 665))
        xpos = 1280
        ypos = 720
    else:
        print("NOT POG ")
        lst = list((350, 200, 450, 500))
        xpos = 960
        ypos = 540
        # lst = list((850, 200, 1200, 500))
    overlay = myOverlay(16, xpos, ypos, lst, Crosshair_Path, root)
    overlay.run()

# if __name__ == '__main__':
#     setup("portal.png")
