#!/usr/bin/env python
import numpy as np #numpy is the data structure that will handle the images; numpy is a multi dimensional array

#import opencv
import cv2

image_name = "blackwhite"

print("reading the image")
img = cv2.imread("images/" +image_name+ ".jpg")

print("display the content of the image")
print(img)
print(type(img))
print(img.size)
print(img.shape)
print(img[10])

#there are 3 channels for Red, Blue, Green
