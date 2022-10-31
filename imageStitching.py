import numpy as np
import cv2
import glob

def stitcherFunc(image_source):
    images = []
    imageStitcher = cv2.Stitcher_create()
    for image in image_source:
        img = cv2.imread(image)
        images.append(img)
        print(image + " appended.")
        cv2.waitKey(0)
    print("Stitching started.")
    error, stitched_img = imageStitcher.stitch(images)
    if not error:
        print("Stitching completed.")
    else:
        print("error", error)
    return stitched_img