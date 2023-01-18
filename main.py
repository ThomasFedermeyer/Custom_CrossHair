import tkinter as tk
import shutil
import os
import cv2
import numpy as np
from Overlay import *
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

from PIL import Image 
import PIL 


src = ""
# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry()

currentDirectory = os.getcwd()



    
def select_files():
    filetypes = (
        ('png', '*.png'),
        ('All files', '*.*')
    )

    file = fd.askopenfilenames(
        title='Open files',
        initialdir='Pictures',
        filetypes=filetypes
        )

    global src
    src = file[0]
    print("The src is : ", src)
    combine()

    
def add_transparent_image(background, foreground, x_offset=None, y_offset=None):
    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # center by default
    if x_offset is None: x_offset = (bg_w - fg_w) // 2
    if y_offset is None: y_offset = (bg_h - fg_h) // 2

    w = min(fg_w, bg_w, fg_w + x_offset, bg_w - x_offset)
    h = min(fg_h, bg_h, fg_h + y_offset, bg_h - y_offset)

    if w < 1 or h < 1: return

    # clip foreground and background images to the overlapping regions
    bg_x = max(0, x_offset)
    bg_y = max(0, y_offset)
    fg_x = max(0, x_offset * -1)
    fg_y = max(0, y_offset * -1)
    foreground = foreground[fg_y:fg_y + h, fg_x:fg_x + w]
    background_subsection = background[bg_y:bg_y + h, bg_x:bg_x + w]

    # separate alpha and color channels from the foreground image
    foreground_colors = foreground[:, :, :3]
    alpha_channel = foreground[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # combine the background with the overlay image weighted by alpha
    composite = background_subsection * (1 - alpha_mask) + foreground_colors * alpha_mask

    # overwrite the section of the background image that has been updated
    background[bg_y:bg_y + h, bg_x:bg_x + w] = composite

def combine():
    image1 = Image.open(currentDirectory + "\\images\\DontFuckWith\\NoCrosshair.png") # can just use the base now sice it was already converted
    image2 = Image.open(src)
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    datas = image2.getdata()
 
    newData = []
 
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
 
    image2.putdata(newData)

    image1 = image1.save(currentDirectory + "\\images\\DontFuckWith\\NoCrosshair.png")
    image2 = image2.save(currentDirectory+ "\\images\\DontFuckWith\\Layer.png")

    background = cv2.imread(currentDirectory + "\\images\\DontFuckWith\\NoCrosshair.png")
    overlay = cv2.imread(currentDirectory+ "\\images\\DontFuckWith\\Layer.png", cv2.IMREAD_UNCHANGED)

    add_transparent_image(background, overlay)

    cv2.imwrite(currentDirectory+ "\\images\\DontFuckWith\\example.png", background)

    openimage = Image.open(currentDirectory+ "\\images\\DontFuckWith\\example.png")
    temp = ImageTk.PhotoImage(openimage)
    label1.configure(image = temp)
    label1.image = temp


def Done():
    root.withdraw()
    dst = currentDirectory + "\\images\\Crosshair.png"
    print("selected File : ", src)
    print("dest : ", dst)
    shutil.copyfile(src, dst)
    print("Tsert")
    setup("crossHair.png", root)

# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_files
)

Done_button = ttk.Button(
    root,
    text='Done',
    command=Done
)

open_button.pack(expand=True)
Done_button.pack(expand=True)

image1 = Image.open(currentDirectory + "\\images\\DontFuckWith\\NoCrosshair.png")
test = ImageTk.PhotoImage(image1)

label1 = ttk.Label(
    root,
    image=test)
label1.image = test
label1.pack(expand=True)


# run the application
root.mainloop()
