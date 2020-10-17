import cv2
import numpy as np
import time

vid0 = cv2.VideoCapture(2)
vid1 = cv2.VideoCapture(4)

count = 0
freq = 90
while True:
    check0, frame0 = vid0.read()
    check1, frame1 = vid1.read()
    f0 = frame0
    f1 = frame1
    frame0 = cv2.resize(frame0, (1280, 720))
    frame1 = cv2.resize(frame1, (1280, 720))
    count += 1 
    if check0 and check1:
        # takes photo and saves it each second for 30 fps camera
        if count % freq == 0:
            cv2.imwrite('imagesL/frame{}.jpg'.format(count/freq), frame0)
            cv2.imwrite('imagesR/frame{}.jpg'.format(count/freq), frame1)
            frame0 = cv2.putText(frame0, 'IMAGE TAKEN', (400,360), cv2.FONT_HERSHEY_COMPLEX, 10, (0,255,0), 4)
            frame1 = cv2.putText(frame1, 'IMAGE TAKEN', (400, 360), cv2.FONT_HERSHEY_COMPLEX, 10, (0,255,0), 4)
            time.sleep(1)
        

        cv2.imshow('frame0', f0)
        cv2.imshow('frame1', f1)
        cv2.waitKey(1)
    else:
        print('No frames.')
