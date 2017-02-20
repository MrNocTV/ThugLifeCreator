import PIL.Image as Image
import sys
import cv2
from Converter import gif_to_png
from Utils import remove_files_with_extension_in_folder, detect_face_eyes_mouth
import os

# prepare data
# since opencv.imread does not support gif 
# have to convert it to png or jpg
def prepare_data(nottingham):
    # convert all gif in nottinngham to png 
    for file in os.listdir(nottingham):
        # check extension 
        if file.split('.')[-1] == "gif":
            gif_to_png(os.path.join(nottingham, file))
    # remove all gif
    remove_files_with_extension_in_folder('./nottingham/', 'gif')

# create thuglife image from images in fother nottingham 
def detect_images_in(nottingham):
    for file in os.listdir(nottingham):
        # if file == 'f045.png' or file == 'f046.png' or file == 'm050.png':
        file_path = os.path.join(nottingham, file)
        detect_face_eyes_mouth(file_path)
        
prepare_data('./nottingham/')
detect_images_in('./nottingham')

