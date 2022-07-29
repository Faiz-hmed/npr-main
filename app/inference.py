import os
from io import BytesIO

import cv2
import numpy as np
from django.core.files.uploadedfile import TemporaryUploadedFile
from PIL import Image

from . import od_pipeline as od
from .ocr import esyocr as eocr
from .ocr import pyt

SERVER_URL = os.getenv('OD_SERVICE_URL')


def load_image(img):
    # img = open(img_buf,'rb').read()
    if type(img) == TemporaryUploadedFile:
        t_img_path = img.temporary_file_path()
        img_b = open(t_img_path,'rb').read()
        img = BytesIO(img_b)

    img = Image.open(img.file)
    im_width, im_height = img.size
    img = np.array(img.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
    
    return (img,(im_width, im_height))

def transform(img_l):
    if type(img_l) != list:
        img_l = [img_l]
    for i in range(len(img_l)):
        img_l[i] = img_l[i].tolist()
    return img_l


def recognize_lpns(imgs: list, return_boxes:bool =False ,ocr_engine=1):
    lpns =[]
    lp_bx = []
    print("ocr engine inferred:",ocr_engine)

    for img in imgs:
        image_np,(imW,imH) = load_image(img)
        print(imW, imH)
        boxes = od.get_bboxes(transform(image_np),imW,imH,SERVER_URL,0.75)
        crops = od.get_crops(image_np,boxes)
        sub_img_lpns = [] 

        for i in range(len(crops)):
            print("\n",i+1,"of",len(crops),"crops")

            if ocr_engine == 0:            
                lpn = pyt.recognize(crops[i])

            if ocr_engine == 1:
                lpn = eocr.recognize(crops[i])
            
            sub_img_lpns.append(lpn.upper())

        lp_bx.append(boxes)
        lpns.append(sub_img_lpns)
    print("-------------------------------------------------------")
    if return_boxes:
        return lp_bx,lpns

    return lpns