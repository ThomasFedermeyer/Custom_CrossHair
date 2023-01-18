# chained imports because it looks clean Fuck you
from Overlay import *

currentDirectory = os.getcwd()
savedFilesPath =  os.path.expanduser("~")  + "\AppData\Roaming\Custom CrossHair"
src = ""

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry()

logo = Image.open(currentDirectory + "\\images\\DontFuckWith\\jimin.png")
photo = ImageTk.PhotoImage(logo)
root.iconphoto(False, photo)

root.title("Custom Crosshair")





    
def select_files():
    filetypes = (
        ('Image', '*.png *.jpg'),
    )

    file = fd.askopenfilenames(
        title='Open files',
        initialdir='Pictures',
        filetypes=filetypes
        )

    if file:
        global src
        src = file[0]
        # print("The src is : ", src)
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
    image2 = image2.convert("RGBA")

    datas = image2.getdata()
 
    newData = []
 
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
 
    image2.putdata(newData)

    image2 = image2.save(savedFilesPath+ "\\images\\DontFuckWith\\Layer.png")

    background = cv2.imread(currentDirectory + "\\images\\DontFuckWith\\NoCrosshair.png")
    overlay = cv2.imread(savedFilesPath+ "\\images\\DontFuckWith\\Layer.png", cv2.IMREAD_UNCHANGED)

    add_transparent_image(background, overlay)

    cv2.imwrite(savedFilesPath+ "\\images\\DontFuckWith\\example.png", background)

    openimage = Image.open(savedFilesPath+ "\\images\\DontFuckWith\\example.png")
    temp = ImageTk.PhotoImage(openimage)
    label1.configure(image = temp)
    label1.image = temp


def Done():
    global src
    if src == "":
        return
    root.withdraw()
    # C:\Users\tommy\AppData\Roaming
    

    dst = savedFilesPath + "\\images\\DontFuckWith\\Layer.png"
    src = src.replace("/", "\\")

    if dst != src:
        shutil.copyfile(src, dst)
    setup("Layer.png", root)


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




def main():
    path = savedFilesPath + "\images\DontFuckWith"
    print("roaming: ", path)
    try:
        os.makedirs(path)
    except OSError as error:
        print("Path: ", path, " already exists")


if __name__ == "__main__":
    main()

# run the application
root.mainloop()

