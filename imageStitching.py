import numpy as np
import cv2
import glob

def stitcherFunc(image_source, scale_percent):
    images = []
    imageStitcher = cv2.Stitcher_create()
    for image in image_source:
        img = cv2.imread(image)
        images.append(img)
        print(image + " appended.")
        cv2.waitKey(0)
    print("Stitching started.")
    error, stitched_img = imageStitcher.stitch(images)
    #cropped = cropImg(stitched_img, 30)
    #large = cv2.hconcat([stitched_img, cropped])
    #cv2.imwrite("slm.jpg", large)
    if not error:
        #resized = resizer(large, scale_percent)
        print("Stitching completed.")
    else:
        print("error", error)
    #return resized
    return stitched_img