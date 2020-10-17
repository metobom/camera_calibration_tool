import cv2
import numpy as np

K0 = np.load('CMAT_DIST/logitech_c310_cam_mat.npy')
dist0 = np.load('CMAT_DIST/logitech_c310_dist_coeffs.npy')
K1 = np.load('CMAT_DIST/logitech_c310_cam_mat.npy')
dist1 = np.load('CMAT_DIST/logitech_c310_dist_coeffs.npy')

R = np.load('STEREO_CALIB/stereo_rmat.npy')
t = np.load('STEREO_CALIB/stereo_tvec.npy')

R1, R2, P1, P2, Q, roi_left, roi_right = cv2.stereoRectify(K0, dist0, K1, dist1, (1280, 720), R, t)



x = np.dot(R1, P1)
print(x)
y = np.dot(R2, P2)
print(y)
np.save('STEREO_RECTIFY/P1', x)
np.save('STEREO_RECTIFY/P2', y)


