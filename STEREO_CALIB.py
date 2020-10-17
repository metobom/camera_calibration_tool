import cv2
import numpy as np
import os
import glob

# CAM1 = RIGHT
# CAM0 = LEFT

class STEREO_CALIB():
    def __init__(self):
        self.cam0 = cv2.VideoCapture(2)
        self.cam1 = cv2.VideoCapture(4)
        self.orb = cv2.ORB_create()
        self.matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
        self.K0 = np.load('CMAT_DIST/logitech_c310_cam_mat.npy')
        self.dist0 = np.load('CMAT_DIST/logitech_c310_dist_coeffs.npy')
        self.K1 = np.load('CMAT_DIST/logitech_c310_cam_mat.npy')
        self.dist1 = np.load('CMAT_DIST/logitech_c310_dist_coeffs.npy')
        self.baseline = 2 * 16
        self.W = 1280
        self.H = 720
        
    def calib(self):
        CHECKERBOARD = (6,9)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        objpoints = []
        imgpoints0 = []
        imgpoints1 = [] 
        
        objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
        objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
        count = 0

        imagesL = glob.glob('./imagesL/*.jpg')
        imagesR = glob.glob('./imagesR/*.jpg')
        for fname0, fname1 in zip(imagesL, imagesR):
            f0 = cv2.imread(fname0)
            f1 = cv2.imread(fname1)
            if c:
                gray0 = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY)
                ret0, corners0 = cv2.findChessboardCorners(gray0, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
                gray1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
                ret1, corners1 = cv2.findChessboardCorners(gray1, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_FAST_CHECK + cv2.CALIB_CB_NORMALIZE_IMAGE)
                if ret0 and ret1:
                    count += 1
                    print(count)
                    objpoints.append(objp)
                    corners0_0 = cv2.cornerSubPix(gray0, corners0, (11,11),(-1,-1), criteria)
                    corners1_1 = cv2.cornerSubPix(gray1, corners1, (11,11),(-1,-1), criteria)   
                    imgpoints0.append(corners0_0)
                    imgpoints1.append(corners1_1)
                    out0 = cv2.drawChessboardCorners(f0, CHECKERBOARD, corners0_0, ret0)
                    out1 = cv2.drawChessboardCorners(f1, CHECKERBOARD, corners1_1, ret1)
                    cv2.imshow('f0', f0)
                    cv2.imshow('f1', f1)
                    self.K0 = np.array(self.K0)
                    self.K1 = np.array(self.K1)
                    self.dist0 = np.array(self.dist0)
                    self.dist1 = np.array(self.dist1)
                    retval, camMat1, distCoeffs1, camMat2, distCoeffs2, R, T, E, F = cv2.stereoCalibrate(objpoints, imgpoints0, imgpoints1, self.K0, self.dist0, self.K1, self.dist1, (self.W, self.H), None, None, None, None)
                    #if count == 20:
                    np.save('STEREO_CALIB/logitech_c310_rmat.npy', R)
                    np.save('STEREO_CALIB/logitech_c310_tvec.npy', T)
                    np.save('STEREO_CALIB/stereo_rmat.npy', R)
                    np.save('STEREO_CALIB/stereo_tvec.npy', T)
                    #np.save('STEREO_CALIB/logitech_c310_essential_mat.npy', E)
                    #np.save('STEREO_CALIB/logitech_c310fund_mat.npy', F)
                    print(camMat1)
                    print('______________')
                    print(camMat2)
                    
                    print(T)
        
                cv2.waitKey(1)

    def Main(self):
        self.calib()


if __name__ == "__main__":
    c = STEREO_CALIB()
    c.Main()
        

