import PIL.Image as Image 
import sys 
import os 

def gif_to_png(gif_img):
    try:
        img = Image.open(gif_img)
    except IOError:
        print("Failed to read", gif_img)
        sys.exit(1)
    
    try:
        # start converting 
        # actually, this must be placed inside a while loop
        # since gif file usually contains more than one images 
        # but in this case, it just one image but saved as gif file (weird)
        palette = img.getpalette()
        img.putpalette(palette)
        new_img = Image.new("RGBA", img.size)
        new_img.paste(img)
        # done converting, save it for later use 
        cur_dirrectory = os.path.dirname(gif_img)
        file_name = os.path.basename(gif_img).split(".")[0] + '.png'
        new_img.save(os.path.join(cur_dirrectory, file_name))
        
    except EOFError:
        pass