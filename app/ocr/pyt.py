from .utils import *
import pytesseract
from PIL import Image, ImageEnhance

def recognize(img):
    lpn = pytesseract.image_to_string(img)
        
    lpn = make_final_str(lpn)

    i=0
    while(len(lpn)<9):
        if i==0:
            enhancer = ImageEnhance.Sharpness(Image.fromarray(img))
            en_img = enhancer.enhance(3)
            lpn = make_final_str(pytesseract.image_to_string(en_img))

        if i==1:
            print("1.Sharpening at 80!")
            bw_img = denoise(img,80,170)
            lpn = make_final_str(pytesseract.image_to_string(bw_img))

        if i==2:
            print("2.Thresholding at 90.. Sharpening @ 4!")
            bw_img = denoise(img,90,230)
            enhancer = ImageEnhance.Sharpness(Image.fromarray(bw_img))
            en_img = enhancer.enhance(4)
            lpn = make_final_str(pytesseract.image_to_string(en_img))

        if i==3:
            print("3.Thresholding at 100.. Sharpening @ 5!")
            bw_img = denoise(img,100,255)
            enhancer = ImageEnhance.Sharpness(Image.fromarray(bw_img))
            en_img = enhancer.enhance(5)
            lpn = make_final_str(pytesseract.image_to_string(en_img))

        if i==4:
            print("4.Thresholding at 100.. Sharpening @ 6, Last level!")
            bw_img = denoise(img,100,255)
            enhancer = ImageEnhance.Sharpness(Image.fromarray(bw_img))
            en_img = enhancer.enhance(6)
            lpn = make_final_str(pytesseract.image_to_string(en_img))
        i+=1

        if len(lpn) >=9 and len(lpn)<=13 or i==5:
            break
        
        print("\n\n",lpn)
    return lpn