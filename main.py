from turtle import st
from imageStitching import stitcherFunc
import glob
import cv2
import numpy as np
import pandas as pd
import time

DEGREE_CONST = 360
DEGREE_GAP = 54
a = True #imwrite flag
scale_percent = 17 #scale const
locations = [] #empty list for locations
locData = pd.read_csv('iCloud Photos/first_location.csv')
image_wide_const = 30 #degree 

def mEvent(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX, mouseY = x, y
        locations.append([mouseX, mouseY])
        print("x line = " + str(getDegreeForPixelV(stitched4, mouseX)))
        print("y line = " + str(getDegreeForPixelH(stitched4, mouseY)))
        print(mouseX, mouseY)

def createVerticalLine(image, position):
    sp = (position, 100)
    ep = (position, image.shape[0])
    c = (255, 255, 255)
    t = 4
    print("v line printed at : ", position)
    return cv2.line(image, sp, ep, c, t)

def createHorizontalLine(image, position):
    sp = (0, position)
    ep = (image.shape[1], position)
    c = (255, 255, 255)
    t = 4
    print("h line printed at : ", position)
    return cv2.line(image, sp, ep, c, t)

def getDegreeForPixelH(img, px):
    degree = (DEGREE_CONST / 2) * (px / img.shape[0])
    return abs(degree - (DEGREE_CONST / 4))
    #if(degree<0):
    #    return degree + 360
    #else:
    #    return degree % 360

def getDegreeForPixelV(img, px):
    degree = (DEGREE_CONST + image_wide_const) * (px / img.shape[1]) - DEGREE_GAP
    if(degree<0):
        return degree + 360
    else:
        return degree % 360

def getPixelForVerticalDegree(img, deg):
    return (deg * img.shape[1] ) / (DEGREE_CONST + image_wide_const)

def getPixelForHorizontalDegree(img, deg):
    return (deg * img.shape[0] ) / (DEGREE_CONST + image_wide_const)

def createVerticalLineForPixel(img, deg):
    linePerDegree = 20
    imageWidth = img.shape[1] # 360 + 30 = 390 degree image.
    pixelPerDegree = imageWidth / (DEGREE_CONST + image_wide_const)
    startingPoint = DEGREE_GAP * pixelPerDegree
    negativePoint = DEGREE_GAP * pixelPerDegree
    while(startingPoint < imageWidth):
        createVerticalLine(img, int(startingPoint))
        createVerticalLine(img, int(negativePoint))
        negativePoint = negativePoint - (pixelPerDegree * linePerDegree)
        startingPoint = startingPoint + (pixelPerDegree * linePerDegree)

def createHorizontalLineForPixel(img, deg):
    linePerDegree = 20
    imageHeight = img.shape[0] # 180 degree image.
    pixelPerDegree = imageHeight / (DEGREE_CONST / 2) # 360 / 2 = 180
    startingPoint = 0
    while(startingPoint < imageHeight):
        createHorizontalLine(img, int(startingPoint))
        startingPoint = startingPoint + (pixelPerDegree * linePerDegree)
    #px = getPixelForHorizontalDegree(img, deg)
    #return createHorizontalLine(img, int(px))

def createText(img, text, poz):
    linePerDegree = 20
    imageWidth = img.shape[1] # 360 + 30 = 390 degree image.
    pixelPerDegree = imageWidth / (DEGREE_CONST + image_wide_const)
    startingPoint = DEGREE_GAP * pixelPerDegree
    negativePoint = DEGREE_GAP * pixelPerDegree
    negativeDegree = 0
    startingDegree = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 2
    color = (255, 255, 255)
    thickness = 6
    while(startingPoint < imageWidth):
        gap = len(str(startingDegree % 360)) * 10 * fontScale
        org = (int(startingPoint - gap), 100)        
        cv2.putText(img, str(int(startingDegree % 360)), org, font, fontScale, color, thickness, cv2.LINE_AA)
        startingDegree = startingDegree + linePerDegree
        startingPoint = startingPoint + (pixelPerDegree * linePerDegree)
    while(negativePoint > 0):
        neggap = len(str(negativeDegree % 360)) * 10 * fontScale
        negorg = (int(negativePoint - neggap), 100) 
        print("sslm", negorg[0], negorg[1], str(int(negativeDegree % 360)))
        cv2.putText(img, str(int(negativeDegree % 360)), negorg, font, fontScale, color, thickness, cv2.LINE_AA)
        negativeDegree = negativeDegree - linePerDegree
        if(negativeDegree < 0):
            negativeDegree = negativeDegree + 360
        negativePoint = negativePoint - (pixelPerDegree * linePerDegree)
    #return cv2.putText(img, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

def cropImg(img, percent):
    w = img.shape[0]
    h = int(img.shape[1] * (percent / 360))
    return img[0:w, 0:h]

def resizer(img, percent):
    w = int(img.shape[1] * percent / 100)
    h = int(img.shape[0] * percent / 100)
    d = (w, h)
    return cv2.resize(img, d, interpolation = cv2.INTER_AREA)

image_paths = glob.glob('iCloud Photos/ilk konum/*.JPEG')
new_file_name = "first_location_stitched_10"
timestr = str("IMG_" + time.strftime("%Y%m%d-%H%M%S"))
#stitched = stitcherFunc(image_paths, scale_percent)
stitched = cv2.imread("test_imgs/IMG_20221017-234731.png")
stitched2 = cropImg(stitched, image_wide_const)
stitched3 = cv2.hconcat([stitched, stitched2])
cv2.namedWindow('image')
cv2.setMouseCallback('image', mEvent)
while(1):
    #for i in np.arange(0, 360, 20): #vertical operations
    createVerticalLineForPixel(stitched3, 20) #create vertical line per 20 degree
    #j = getPixelForVerticalDegree(stitched3, 20)
    createText(stitched3, "20", 20)
    #for i in np.arange(0, 360, 20): #horizontal operations
    createHorizontalLineForPixel(stitched3, 20) #create horizontal line per 20 degree
    #cv2.imshow("image", stitched4)
    if(a):
        a = False
        cv2.imwrite("test_imgs/" + timestr + ".png", stitched)
        stitched4 = resizer(stitched3, scale_percent)
    cv2.imshow("image", stitched4)    
    print("ilk 10 konumu belirle.")
    print(len(locations))
    if(len(locations) == 10):
        print("completed.")
        break
    elif(cv2.waitKey(0)):
        break
#locData = pd.read_csv('iCloudPhotos/firstlocation.csv')
#newX = getDegreeForPixel(mouseX, stitched)