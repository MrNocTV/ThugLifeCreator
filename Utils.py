import os 
import cv2

ALPHA = 3

# this function works with even sub folders
def remove_files_with_extension_in_folder(folder, extension):
    for item in os.listdir(folder):
        if os.path.isdir(os.path.join(folder, item)):
            remove_files_with_extension_in_folder(item, extension)
        elif os.path.isfile(os.path.join(folder, item)):
            # print out file's path
            print(os.path.join(folder, item)) 
            # check extension
            if item.strip().split(".")[-1] == extension:
                os.system("rm -f " + os.path.join(folder, item))

# detect face, eyes and mouth and save to 'to' 
def detect_face_eyes_mouth(img_path, to='./nottingham_detected/'):
    # detect face, eyes and mouth in img 
    # then save to folder 
    # first create two classifier 
    # for face, eye, and mouth 
    face_cascade = cv2.CascadeClassifier('./cascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./cascades/haarcascade_mcs_eyepair_big.xml')
    mouth_cascade = cv2.CascadeClassifier('./cascades/haarcascade_mcs_mouth_1.xml')
    # read image (contains the face)
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    # blur to cancel noise, also convert to grayscale
    blur = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    # glasses to be blended over the  eyes 
    glass = cv2.imread('./images/specs.png', -1)
    # ciga to be blended over the mouth 
    ciga = cv2.imread('./images/ciga.png', -1)

    # detect faces (actually support only one face)
    faces = face_cascade.detectMultiScale(blur, 1.3, 5)
    
    has_eyes = False
    has_mouth = False
    for (x, y, w, h) in faces:
        # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # since we only want to detect the eyes on the face 
        # so we only focus on region of interest (roi)
        # in this case is the face 
        # roi_gray for processing
        roi_gray = blur[y:y+h, x:x+w]
        # roi_color for drawing
        roi_color = img[y:y+h, x:x+w]
        # detect eyes 
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex, ey, ew, eh) in eyes:
            has_eyes = True
            # cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (255, 0, 0), 2)
            break
        
        # detect mouth 
        # detect mouth is a little bit trickier than eyes
        # since it generates a lot of result 
        # and only one of them is correct 
        # so we need to find the right one
        # the next two for loops used to find the correct mouth  
        mouths = mouth_cascade.detectMultiScale(roi_gray, 1.7, 11)
        max_y = -99999999
        max_x = None
        for (mx, my, mw, mh) in mouths:
            my = int(my - 0.15*mh)
            if my > max_y:
                max_y = my
                max_x = mx
        
        for (mx, my, mw, mh) in mouths:
            my = int(my - 0.15*mh)
            if my == max_y:
                has_mouth = True
                # cv2.rectangle(roi_color, (mx, my), (mx+mw, my+mh), (255, 0, 0), 2)
                break
    
    # only draw the glasses over the eyes if we can find the eyes
    # since roi_color is a BGR image (RGB)
    # but glasses is a BGRA (RGB with alpha channel)
    # so we only need the first 3 values [:3] of glass 
    if has_eyes:
        # resize the glass base on the size of the eyes 
        glass = cv2.resize(glass, (int(ew*1.1), int(eh*2.7)))
        width, height, channels = glass.shape
        for i in range(0, width):
            for j in range(0, height):
                # we only need to draw the glasses, not the background 
                # with alpha == 0
                if glass[i, j][3] != 0:
                    roi_color[ey+i-40, ex+j-10] = glass[i, j][:3]
    
    # same thing goes for the mouth 
    if has_mouth:
        # resize the ciga with static size 
        # you can change these values to get better result 
        ciga = cv2.resize(ciga, (130, 50))
        # get the center of the mouth 
        x = mx+mw//2
        y = my+mh//2
        # mark the center of the mouth with a red dot 
        cv2.rectangle(roi_color, (x, y), (x, y) , (0, 0, 255), 4)
        width, height, channels = ciga.shape
        try:
            for i in range(0, width):
                for j in range(0, height):
                    if ciga[i, j][3] != 0:
                        roi_color[y+i, x+j] = ciga[i, j][:3]
        except Exception:
            pass

    # saving stuff 
    new_file = os.path.basename(img_path).split(".")[0]
    new_file += '_detected' + '.png'
    cv2.imwrite(os.path.join(to, new_file), img)

