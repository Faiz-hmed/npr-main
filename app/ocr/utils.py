import cv2

def make_final_str(l_str):
    lpn = ""
    escapes = ''.join([chr(char) for char in range(1, 32)])
    translator = str.maketrans('', '', escapes)
    l_str = l_str.translate(translator)
    for i in l_str:
        if i.isdigit() or i.isalpha() or i.isspace():
            lpn += i
    return lpn.strip()

def denoise(img,lb=90,up=200):
    dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
    bw_img = cv2.threshold(dst,lb,up,cv2.THRESH_BINARY)[1]
    return bw_img

def get_spaced_num(str):
    return ' '.join(str)