import cv2
import numpy as np
from matplotlib import pyplot as plt

orig = cv2.imread('banana.jpg')

img = cv2.imread('banana.jpg') #import image object with name 'img'
cv2.imshow('image',img)
cv2.waitKey(0)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grayscale
cv2.imshow('image',img)
cv2.waitKey(0)

img = cv2.GaussianBlur(img, (3,3),0) #blur image to reduce insignificant edges
cv2.imshow('image',img)
cv2.waitKey(0)

img = cv2.Canny(img,40,150) #run canny edge detector
cv2.imshow('image',img)
cv2.waitKey(0)

img2, c, h = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) #get contours and sort
c = sorted(c, key = cv2.contourArea, reverse = True)[:10]
cnt = c[4]
cv2.drawContours(img,[cnt],0, (0,255,0), 3)
cv2.imshow('image',img)
cv2.waitKey(0)
print cnt
print len(cnt)

for i in range (len(c)):
	cv2.drawContours(img,c,i, (0,255,0), 3)
	cv2.imshow('image',img)
	cv2.waitKey(0)


cv2.destroyAllWindows()
