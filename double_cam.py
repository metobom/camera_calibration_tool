import cv2


cam0 = cv2.VideoCapture(2)
cam1 = cv2.VideoCapture(4)

while True:
    check0, frame0 = cam0.read()
    check1, frame1 = cam1.read()
    frame0 = cv2.resize(frame0, (1280, 720))
    frame1 = cv2.resize(frame1, (1280, 720))
    if check0 and check1:
        cv2.imshow('frame0', frame0)
        cv2.imshow('frame1', frame1)
        cv2.waitKey(1)