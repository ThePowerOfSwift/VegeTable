import sys
import time
import cv2
import numpy as np
import cmath
import os
from matplotlib import pyplot as plt

def sortArea(contours):
	areas = []
	for i in range(len(contours)):
		area = cv2.contourArea(contours[i])
		areas.append([area,i])
	areas.sort(key=lambda x: x[0],reverse=True)
	return (areas)

def maskContour(image,contour):
	img = image.copy()
	return (img)

filename = filename = os.path.dirname(__file__) + 'images/test/banana.jpg'
img = cv2.imread(filename)
orig = img.copy()
cv2.imshow('image',img)
cv2.moveWindow('image',0,0)
cv2.waitKey(0)
cv2.destroyAllWindows()
edges = cv2.Canny(img,20,40)
cv2.imshow('edges',edges)
cv2.moveWindow('edges',0,0)
cv2.waitKey(0)
cv2.destroyAllWindows()
contours, hierarchy = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
sizes = sortArea(contours)
size_key = sizes[0]
contour = contours[size_key[1]]
cv2.drawContours(img,contour,-1, (0,255,0), 3)
cv2.imshow('contour',img)
cv2.moveWindow('image',0,0)
cv2.waitKey(0)
cv2.destroyAllWindows()
mask = np.array
exit()	
