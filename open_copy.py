#!/usr/bin/env python
import numpy as np #numpy is the data structure that will handle the images; numpy is a multi dimensional array

#import opencv
import cv2

#image_name = "src/ros_test/src/opencv_proj/images/tree.jpg"
image_name = "tree"

print('read an image from the file')
img = cv2.imread("images/"+image_name+".jpg")

print("create a window holder for the image")
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)

print("display the image")
cv2.imshow("Image", img)

print("Press a key inside the image to make a copy")
cv2.waitKey(5000)  #wait for 5 milli seconds

print("image copied to folder images/copy/")
if cv2.imwrite("images/copy/"+image_name+"-copy.jpg", img):
    print("Image saved successfully.")
else:
    print("Failed to save the image.")