import numpy as np
import cv2
import glob

def stitcherFunc(image_source, scale_percent):
    images = []
    imageStitcher = cv2.Stitcher_create()
    for image in image_source:
        img = cv2.imread(image)
        images.append(img)
        print(image+" appended.")
        cv2.waitKey(0)
    print("Stitching started.")
    error, stitched_img = imageStitcher.stitch(images)
    if not error:
        width = int(stitched_img.shape[1] * scale_percent / 100)
        height = int(stitched_img.shape[0] * scale_percent / 100)
        dim = (width,height)
        resized = cv2.resize(stitched_img, dim, interpolation=cv2.INTER_AREA)
        print("Stitching completed.")
    else:
        print("error",error)
    return resized