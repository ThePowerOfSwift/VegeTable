#http://docs.opencv.org/3.1.0/d9/d8b/tutorial_py_contours_hierarchy.html#gsc.tab=0
import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = 'banana.jpg'

img = cv2.imread(filename) #import image object with name 'img'
#cv2.imshow('image',img)
#cv2.waitKey(0)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grayscale
#cv2.imshow('image',img)
#cv2.waitKey(0)

img = cv2.GaussianBlur(img, (3,3),0) #blur image to reduce insignificant edges
#cv2.imshow('image',img)
#cv2.waitKey(0)

img = cv2.Canny(img,40,150) #run canny edge detector
#cv2.imshow('image',img)
#cv2.waitKey(0)

contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
convex_hull = cv2.convexHull(contours[0])
orig = cv2.imread(filename)
cv2.imshow('all contours',orig)
cv2.waitKey(0)
cv2.destroyAllWindows()

#For loop iterates through each contour level in countours array of arrays
#Information from each contour level is displayed several times overlayed on the original image:
#1st - contour level displayed
#2nd - points from convex hull
#Then information is printed to console (TO DO: integrate rectangles and convex defects into image):
#1st - bounding rectangle - "the up-right bounding rectangle of a rotated rectangle of the minimum area enclosing the input 2D point setpoint set"
#2nd - minimum area rectangle - "rotated rectangle of the minimum area enclosing the input 2D point set"
#3rd - contour area - the area enclosed by the contour
#4th - contour perimeter - "The function computes a curve length or a closed contour perimeter" (contour closed set to True to get perimeter)
#5th - number of elements in convexity defects
for i in range(len(contours)):
	orig = cv2.imread(filename)
	contour = contours[i]
	cv2.drawContours(orig, contour, -1, (0,255,0), 3)
	cv2.imshow('contours-' + str(i),orig)
	cv2.waitKey(0)

	orig = cv2.imread(filename)
	convex_hull = cv2.convexHull(contours[i])
	cv2.drawContours(orig, convex_hull, -1, (0,255,0), 3)
	cv2.imshow('convex hull-' + str(i),orig)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	print ('bounding rectangle - ' + str(cv2.boundingRect(contours[i])))
	print ('min area rect - ' + str(cv2.minAreaRect(contours[i])))
	print ('contour area - ' + str(cv2.contourArea(contours[i])))
	print ('contour perimeter - ' + str(cv2.arcLength(contours[i],True)))
	#print ('numnber of elements in convexity defects - ' + str(len(cv2.convexityDefects(contours[i],cv2.convexHull(contours[i],returnPoints = False)))))


cv2.destroyAllWindows()
