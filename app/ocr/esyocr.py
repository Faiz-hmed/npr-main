import cv2
import easyocr
from .utils import get_spaced_num

def recognize(cropped_img):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image=cropped_img,detail=0)

    return get_spaced_num(result)
