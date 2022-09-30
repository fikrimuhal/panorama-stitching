import cv2
import numpy as np
import matplotlib.pyplot as plt

#IMAGE_H ,IMAGE_W = 223, 1280
IMAGE_W, IMAGE_H= 3888,1175#2592
#src = np.float32([[0, IMAGE_H], [1207, IMAGE_H], [0, 0], [IMAGE_W, 0]])
#dst = np.float32([[569, IMAGE_H], [711, IMAGE_H], [0, 0], [IMAGE_W, 0]])
src = np.float32([[0, IMAGE_H], [3613, IMAGE_H], [0, 0], [IMAGE_W, 0]])
dst = np.float32([[1457, IMAGE_H], [2417, IMAGE_H], [0, 0], [IMAGE_W, 0]])
M = cv2.getPerspectiveTransform(src, dst) # The transformation matrix
Minv = cv2.getPerspectiveTransform(dst, src) # Inverse transformation

img = cv2.imread('unstitched/boat04.jpg') # Read the test img
img = img[1450:(1450+IMAGE_H), 0:(0+IMAGE_W)] # Apply np slicing for ROI crop
warped_img = cv2.warpPerspective(img, M, (IMAGE_W, IMAGE_H)) # Image warping
cv2.imwrite('waro04.png', warped_img)
#plt.imshow(cv2.cvtColor(warped_img, cv2.COLOR_BGR2RGB)) # Show results
plt.show()