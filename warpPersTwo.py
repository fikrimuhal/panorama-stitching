# Importing Libraries
import cv2
import numpy as np


frame = cv2.imread('unstitched/boat01.jpg')
# Plotting four circles on the video of the object you want to        
# see the transformation of.
width, height = 3888,2592

cv2.circle(frame,(1550,1200),5,(0,0,255),-1)
cv2.circle(frame, (2338,1200), 5, (0, 0, 255), -1)
cv2.circle(frame, (0,height), 5, (0, 0, 255), -1)
cv2.circle(frame, (width,height), 5, (0, 0, 255), -1)    # selecting all the above four points in an array
#imgPts = np.float32([[114,151],[605, 89],[72, 420],[637, 420]])
imgPts = np.float32([[1550,1200],[2338,1200],[0,height],[width,height]])

# selecting four points in an array for the destination video( the one you want to see as your output)
#objPoints = np.float32([[0,0],[420,0],[0,637],[420,637]])    #Apply perspective transformation function of openCV2. This function will return the matrix which you can feed into warpPerspective function to get the warped image.
objPoints = np.float32([[0,0],[width,0],[0,height],[width,height]])

matrix = cv2.getPerspectiveTransform(imgPts,objPoints)
result = cv2.warpPerspective(frame,matrix,(16500,3000))    #Now Plotting both the videos(original, warped video)using matplotlib
#cv2.imshow('frame',frame)
#cv2.imshow('Perspective Transformation', result)
cv2.imwrite('twozeroone.png',result)
cv2.waitKey(0)

cv2.destroyAllWindows()

