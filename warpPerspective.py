import cv2
import numpy as np

#img = cv2.imread('stitchedOutput.png')
img = cv2.imread('unstitched/boat04.jpg')

width, height = 3888,2592
pts1 = np.float32([[1550,1200],[2338,1200],[0,height],[width,height]])
pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
matrix = cv2.getPerspectiveTransform(pts1,pts2)
imgOutput = cv2.warpPerspective(img,matrix,(width,height))

#for x in range (0,4):
#    cv2.circle(img,(int(pts1[x][0]),int(pts1[x][1])),5,(0,0,255),cv2.FILLED)

#cv2.imshow("Orginal Image", img)
#cv2.imshow("Output Image", imgOutput)
cv2.imwrite("boat04wrappedold.png", imgOutput)
cv2.waitKey(0)