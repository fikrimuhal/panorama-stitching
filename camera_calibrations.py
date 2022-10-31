import numpy as np
import cv2 as cv
import glob
# termination criteria
CHECKBOARD = (9, 7)
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.01) #0.001
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((CHECKBOARD[0]*CHECKBOARD[1],3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKBOARD[1], 0:CHECKBOARD[0]].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('calibration_photos/*.jpeg')
for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #cv.imshow('img', gray)
    #cv.waitKey(0)
    #print(gray.shape[::-1])
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (CHECKBOARD[1],CHECKBOARD[0]), None)
    # If found, add object points, image points (after refining them)
    #print("slm")
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (CHECKBOARD[1],CHECKBOARD[0]), corners2, ret)
        cv.imshow('img', img)
        #cv.imwrite("slm.png", img)
        ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        print("ret", ret)
        print("dist", dist)
        print("mtx", mtx)
        largeimg = cv.imread('test_imgs\IMG_20221025-124338.png')
        graylargeimg = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        #img = cv.imread('left12.jpg')
        #h,  w = img.shape[:2]
        #h, w = gray.shape[:2]
        h, w = graylargeimg.shape[:2]
        newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w, h), 1, (w, h))
        # undistort
    
        dst = cv.undistort(largeimg, mtx, dist, None, newcameramtx)

        cv.imwrite('uncroppedresult.png', dst)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y+h, x:x+w]
        cv.imwrite('calibresult2.png', dst)
        
        cv.waitKey(0)
cv.destroyAllWindows()