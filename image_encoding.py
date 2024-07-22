#!/usr/bin/env python
import numpy as np #numpy is the data structure that will handle the images; numpy is a multi dimensional array

#import opencv
import cv2

image_name = "tree"

print("reading the image")

color_image = cv2.imread("images/tree.jpg", cv2.IMREAD_COLOR) #method of reading 
cv2.imshow("OG image", color_image)
cv2.moveWindow("original", 0,0)

height, width, channels = color_image.shape

B, G, R = cv2.split(color_image) #split func of the OpenCV library to have channels for the different colours 


cv2.imshow("Blue image", B)     #blue channel
cv2.moveWindow("Blue image", 0,0) 
cv2.imshow("Green image", G)           #green channel
cv2.moveWindow("Green image", 0,0) 
cv2.imshow("Red image", R)        #red channel
cv2.moveWindow("Red image", 0,0) 


#creating in HSV domain

hsv = cv2.cvtColor(color_image, cv2.COLOR_BGR2HSV)
h, s, v = cv2.split(hsv)

'''the images are in numpy arrays, so we can split into h,s,
 and v and join them to a new window'''

hsv_image = np.concatenate((h, s, v), axis =1)
cv2.imshow("Hue, Saturation, Value Image", hsv_image)

#in gray colour domain


gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Image", gray_image)

cv2.waitKey(10000)
cv2.destroyAllWindows()
