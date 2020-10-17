import cv2
import numpy as np
import os
import glob

CHECKERBOARD = (6,9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


objpoints = []
imgpoints = [] 

baseline = 2 * 16
objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
prev_img_shape = None

images = glob.glob('./images/*.jpg')
for fname in images:
    img = cv2.imread(fname)
    img = cv2.resize(img, (1280, 720))
    #img = img[:,:1280-baseline] # LEFT
    
    img = img[:,baseline:]  # RIGHT
    print(img.shape)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)   
        imgpoints.append(corners2)
        img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2, ret)
        cv2.imshow('img',img)
        cv2.waitKey(1)
        h,w = img.shape[:2]
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
        np.save('CMAT_DIST/logitech_c310_cam_mat.npy', mtx)
        np.save('CMAT_DIST/logitech_c310_dist_coeffs.npy', dist)
        print("Camera matrix : \n")
        print(mtx)
        print("dist : \n")
        print(dist)
        '''print("rvecs : \n")
        print(rvecs)
        print("tvecs : \n")
        print(tvecs)'''
