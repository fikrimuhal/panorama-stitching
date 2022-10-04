from turtle import st
from imageStitching import stitcherFunc
import glob
import cv2
import numpy as np
import pandas as pd
import time

DEGREE_CONST = 360

def mEvent(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        locations.append([mouseX, mouseY])
        print("appended.")
        print(mouseX, mouseY)

def createVerticalLine(image, position):
    sp = (position, 40)
    ep = (position, image.shape[0])
    c = (255, 255, 255)
    t = 1
    print("v line printed at : ", position)
    return cv2.line(image, sp, ep, c, t)

def createHorizontalLine(image, position):
    sp = (0, position)
    ep = (image.shape[1], position)
    c = (255, 255, 255)
    t = 1
    print("h line printed at : ", position)
    return cv2.line(image, sp, ep, c, t)

def getDegreeForPixel(img, px):
    return (px * DEGREE_CONST) / img.shape[1]

def getPixelForVerticalDegree(img, deg):
    return (deg * img.shape[1]) / DEGREE_CONST

def getPixelForHorizontalDegree(img, deg):
    return (deg * img.shape[0]) / DEGREE_CONST

def createVerticalLineForPixel(img, deg):
    #a = getDegreeForPixel(img, px)
    px = getPixelForVerticalDegree(img, deg)
    return createVerticalLine(img, int(px))

def createHorizontalLineForPixel(img, deg):
    #a = getDegreeForPixel(img, px)
    px = getPixelForHorizontalDegree(img, deg)
    return createHorizontalLine(img, int(px))

def createText(img, text, poz):
    font = cv2.FONT_HERSHEY_SIMPLEX
    gap = len(str(text)) * 10
    org = (poz-gap, 30)
    fontScale = 1
    color = (255, 255, 255)
    thickness = 1
    return cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

#img = np.zeros((512, 512, 3), np.uint8)
#cv2.namedWindow('image')
#locations = []
#cv2.setMouseCallback('image', mEvent)
#while(1):
#    cv2.imshow("image", img)
#    print("ilk 10 konumu belirle.")
#    print(len(locations))
#    if(len(locations) == 10):
#        print("completed.")
#        break
#    cv2.waitKey(0)
    
#for i in range(10):
    #print(i+1, ". konum : ", mouseX, mouseY)
    #locations.append([mouseX, mouseY])

#cv2.waitKey(0)

#while(1):
#    print("ilk 10 konumu belirle.")
#    cv2.imshow('image', img)
#    k = cv2.waitKey(20) & 0xFF
#    if k == 27:
#        break
#    elif k == ord('a'):
#        print(mouseX, mouseY)

image_paths = glob.glob('iCloud Photos/ilk konum/*.JPEG')
scale_percent = 20
new_file_name = "first_location_stitched_10"
timestr = str("IMG_" + time.strftime("%Y%m%d-%H%M%S"))
stitched = stitcherFunc(image_paths, scale_percent, timestr)
cv2.namedWindow('image')
locations = []
cv2.setMouseCallback('image', mEvent)
while(1):
    #createLine(stitched,200)
    #createLineForPixel(stitched, 10) # line for 10 degree.
    for i in np.arange(0,360,15):
        createVerticalLineForPixel(stitched, i)
        j = getPixelForVerticalDegree(stitched, i)
        createText(stitched, str(i), int(j))
    for i in np.arange(0,360,30):
        createHorizontalLineForPixel(stitched, i)
    cv2.imshow("image", stitched)
    #cv2.imshow("image", img)
    print("ilk 10 konumu belirle.")
    print(len(locations))
    if(len(locations) == 10):
        print("completed.")
        break
    elif(cv2.waitKey(0)):
        break
#locData = pd.read_csv('iCloudPhotos/firstlocation.csv')
newX = getDegreeForPixel(mouseX, stitched)