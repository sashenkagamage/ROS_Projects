#!/usr/bin/env python
import numpy as np #numpy is the data structure that will handle the images; numpy is a multi dimensional array

#import opencv
import cv2

#video_capture = cv2.VideoCapture(0)
video_capture = cv2.VideoCapture('video/ros.mp4')

while(True):

    ret, frame = video_capture.read()

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()