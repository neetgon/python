
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw, ImageFilter
import time, threading, eel, os, random

filename = "web/interface/default.jpg"
global_image = Image.open(filename)
global_image = global_image.convert("RGBA")
data = global_image.load()

size = 0
pixels = []
threads_list = []

def check_pixels(image, x, y):
    global pixels
    
    for yy in range(y):
        pixels.append(image.getpixel((x, yy)))


def potencial_color(image, size):
    global pixels
    
    threads = []
    
    for x in range(10):
        thread = threading.Thread(target = check_pixels, args=(image, x, 10,))
        thread.start()
        threads.append(thread)
    
    count = 0
    color = 0
    
    for i in range(len(pixels)):
        if count < pixels.count(pixels[i]):
            color = pixels[i]
    
    r = color[0]
    g = color[1]
    b = color[2]
    
    for thread in threads:
        thread.join()
    
    return r, g, b

@eel.expose
def convert_list(tolerancia):
    global threads_list
    
    thread = threading.Thread(target = convert, args=(tolerancia, ))
    thread.start()
    
    for thread in threads_list:
        thread.join()
        thread._stop()
    
    threads_list.clear()
    
    threads_list.append(thread)

@eel.expose
def convert(tolerancia):
    try:
        global global_image, size, filename, data
        
        global_image = Image.open(filename)
        global_image = global_image.convert("RGBA")
        size = global_image.size
        
        data = global_image.load()
        
        color = potencial_color(global_image, size)
        
        draw = ImageDraw.Draw(global_image)
        
        threads = []
        
        for i in range(size[0]):
            thread = threading.Thread(target = chroma, args=(color, i, filename, int(tolerancia), draw, ))
            thread.start()       
        
        img_dir = os.listdir("web/img")
        file_name = "display_" + str(len(img_dir))
        
        for i in range(0, len(img_dir)):
            os.remove("web/img/{}".format(img_dir[i]))
        
        rand = random.randint(0, 9999999999999)
        global_image.save("web/img/{}_{}.png".format(file_name, rand))
            
        eel.update_image("img/{}_{}.png".format(file_name, rand))
        
        for thread in threads:
            thread.join()
        
    except:
        pass

@eel.expose
def salvar():
    global global_image, filename
    
    tk = Tk()
    tk.withdraw()
    tk.attributes("-topmost", True)
    
    temp_name = filename[::-1]
    final_name = ""
    
    for i in temp_name:
        if i != "/":
            final_name += i
        else:
            break
    
    final_name = final_name[::-1]
    final_name = final_name.replace(".jpg", "")
    
    try:
        path = filedialog.asksaveasfilename(initialdir = "/{}".format(filename), initialfile = "{}.png".format(final_name), title="Salvar Imagem", defaultextension=".png", filetypes = (("PNG","*.png"),))
        
        global_image.save("{}.png".format(path))
    except:
        pass

def chroma(color, xx, filename, tolerancia, draw):
    global global_image, size
    
    color_r = color[0]; color_g = color[1]; color_b = color[2]
    
    is_solid_color = True
    solid_color_steps = 500
    
    # White background
    if color_r >= 235 - tolerancia and color_g >= 235 - tolerancia and color_b >= 235 - tolerancia:
        for y in range(size[1]):
            r, g, b, a = data[xx, y]
            
            if not (b >= 235 - tolerancia) and not (g >= 235 - tolerancia) and not (b >= 235 - tolerancia):
                is_solid_color = False
                break
            
            if (y + solid_color_steps) < size[1]:
                y += solid_color_steps
        
        if is_solid_color:
            draw.line((xx, 0, xx, size[1]), fill=(0, 0, 0, 0), width=1)
        else:
            for y in range(size[1]):
                r, g, b, a = data[xx, y]
                
                if r >= 235 + tolerancia and g >= 235 + tolerancia and b >= 235 + tolerancia:
                    data[xx, y] = (0, 0, 0, 0)
    
    # Black background
    elif color_r <= (100 - tolerancia) and color_g <= (100 - tolerancia) and color_b <= (100 - tolerancia):
        for y in range(size[1]):
            r, g, b, a = data[xx, y]
            
            if not (b <= 100 - tolerancia) and not (g <= 100 - tolerancia) and not (b <= 100 - tolerancia):
                is_solid_color = False
                break
            
            if (y + solid_color_steps) < size[1]:
                y += solid_color_steps
        
        if is_solid_color:
            draw.line((xx, 0, xx, size[1]), fill=(0, 0, 0, 0), width=1)
        else:
            for y in range(size[1]):
                r, g, b, a = data[xx, y]
                if r <= 100 - tolerancia and g <= 100 - tolerancia and b <= 100 - tolerancia:
                    data[xx, y] = (0, 0, 0, 0)
    else:
        # Red background
        if color_r > color_b and color_r > color_g:
            for y in range(size[1]):
                r, g, b, a = data[xx, y]
                if not (r > b and r > g):
                    is_solid_color = False
                    break
                
                if (y + solid_color_steps) < size[1]:
                    y += solid_color_steps
            
            if is_solid_color:
                draw.line((xx, 0, xx, size[1]), fill=(0, 0, 0, 0), width=1)
            else:
                if color_r > color_b and color_r > color_g:
                    for y in range(size[1]):
                        r, g, b, a = data[xx, y]
                        if (r > b and r > g) and (r - b) > tolerancia and (r - g) > tolerancia:
                            data[xx, y] = (0, 0, 0, 0)
        
        # Green background
        if color_g > color_r and color_g > color_b:
            for y in range(size[1]):
                r, g, b, a = data[xx, y]
                if not (g > r and g > b):
                    is_solid_color = False
                    break
                
                if (y + solid_color_steps) < size[1]:
                    y += solid_color_steps
            
            if is_solid_color:
                draw.line((xx, 0, xx, size[1]), fill=(0, 0, 0, 0), width=1)
            else:
                if color_g > color_r and color_g > color_b:
                    for y in range(size[1]):
                        r, g, b, a = data[xx, y]
                        if (g > r and g > b) and (g - r) > tolerancia and (g - b) > tolerancia:
                            data[xx, y] = (0, 0, 0, 0)
        
        # Blue background
        if color_b > color_r and color_b > color_g:
            for y in range(size[1]):
                r, g, b, a = data[xx, y]
                if not (b > r and b > g):
                    is_solid_color = False
                    break
                
                if (y + solid_color_steps) < size[1]:
                    y += solid_color_steps
            
            if is_solid_color:
                draw.line((xx, 0, xx, size[1]), fill=(0, 0, 0, 0), width=1)
            else:
                if color_b > color_r and color_b > color_g:
                    for y in range(size[1]):
                        r, g, b, a = data[xx, y]
                        if (b > r and b > g) and (b - r) > tolerancia and (b - g) > tolerancia:
                            data[xx, y] = (0, 0, 0, 0)