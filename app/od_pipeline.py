import requests
import json
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np


def request_bbox(img, server_url) -> tuple:
    print("Requesting OD...")
    req_data = json.dumps({"instances":img})

    res = requests.post(server_url,data=req_data)
    res.raise_for_status()
    total_time = res.elapsed.total_seconds()
    prediction = res.json()['predictions'][0]
    
    return (prediction,total_time)

def get_bboxes(img_np,imW,imH,server_url,filter_acc=0.75):
    output_dict, total_time = request_bbox(img_np, server_url)
    print("Time taken to get bbox for {},{} image:".format(imW,imH), total_time)
    
    scores = output_dict['detection_scores']
    boxes = output_dict['detection_boxes']
    classes = output_dict['detection_classes']

    bb_boxes = []
    print("Highest conf box:",scores[0])

    for i in range(len(scores)):
      acc = scores[i]
      if acc > filter_acc:
        ymin, xmin, ymax, xmax = tuple(boxes[i])

        ymin = int(max(1,(ymin * imH)))
        xmin = int(max(1,(xmin * imW)))
        ymax = int(min(imH,(ymax * imH)))
        xmax = int(min(imW,(xmax * imW)))
        
        bb_boxes.append([ymin, xmin, ymax, xmax])
    return bb_boxes

def get_crops(img_np,bb_boxes):
    crop_imgs = []
    
    for [ymin, xmin, ymax, xmax] in bb_boxes:
        cropped_img = img_np[ymin:ymax,xmin:xmax]
        crop_imgs.append(cropped_img)
        
    return crop_imgs
