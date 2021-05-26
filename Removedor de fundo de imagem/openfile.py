from tkinter import *
from tkinter import filedialog
from PIL import Image
import eel, chroma, os, random

@eel.expose
def open_file():
    try:
        tk = Tk()
        tk.withdraw()
        tk.attributes("-topmost", True)
        path = filedialog.askopenfilename()
        chroma.filename = path
        
        img = Image.open(path)
        
        name = "display_" + str(random.randint(0, 9999999999999))
        
        img_dir = os.listdir("web/img")
        
        for i in range(0, len(img_dir)):
            os.remove("web/img/{}".format(img_dir[i]))
        
        img.save("web/img/{}.png".format(name))
        
        eel.update_image("img/{}.png".format(name))
    except:
        pass