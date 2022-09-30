from imageStitching import stitcherFunc
import glob
import cv2
import numpy as np
import pandas as pd

DEGREE_CONST = 360

def mEvent(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:
        #cv2.circle(img, (x, y), 100, (255, 0, 0), -1)
        mouseX, mouseY = x, y
        locations.append([mouseX, mouseY])
        print("appended.")
        print(mouseX, mouseY)

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
stitched = stitcherFunc(image_paths, scale_percent, new_file_name)
#cv2.imshow("Stitched Image", stitched)

#img = np.zeros((512, 512, 3), np.uint8)
cv2.namedWindow('image')
locations = []
cv2.setMouseCallback('image', mEvent)
while(1):
    cv2.imshow("image", stitched)
    #cv2.imshow("image", img)
    print("ilk 10 konumu belirle.")
    print(len(locations))
    if(len(locations) == 10):
        print("completed.")
        break
    cv2.waitKey(0)
locData = pd.read_csv('iCloudPhotos/firstlocation.csv')

newX = (mouseX * DEGREE_CONST) / stitched.shape[0]