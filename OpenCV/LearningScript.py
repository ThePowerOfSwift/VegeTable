#######################################################################
#TODO: 
#	1) Explore other methods to sort contours (currently largest area)
#	2) Find way to extract average color value from within contour
#	3) Add to preProcessing stub to add filtering functionality
#	4) Add support for terminal arguments
#		a) folder path
#		b) fruit/veggie id number for folder
########################################################################
import sys
import time
import cv2
import numpy as np
import cmath
import os
from matplotlib import pyplot as plt

def perimeter(points):
	length = 0
	for element in points:
		for e in element:
			a = e[0]
			b = e[1]
			c = (a**2)+(b**2)
			c = c**0.5
			length = length + c
	return(length)

def edgeDetection(image,blur=15,lower=1,upper=2):
	while ( True ):
		img = image.copy()
		img = cv2.GaussianBlur(img,(blur,blur),0)
		img = cv2.Canny(img,40,80)
		cv2.imshow('select edges to search for contours',img)
		cv2.moveWindow('select edges to search for contours',0,0)
		key_pressed = cv2.waitKey(0)
		if (key_pressed == 10):
			cv2.destroyAllWindows()
			return (img)
		if (key_pressed == 65363):
			lower = lower * 2
			upper = upper * 2
			cv2.destroyAllWindows()
		if (key_pressed == 65361):
			if (lower > 1):
				lower = int(lower/2)
				upper = int(upper/2)
			else:
				print ('minumum threshold value reached')
		if (key_pressed == 65362):
			blur = blur +2
		if (key_pressed == 65364):
			if (blur > 1):
				blur = blur - 2
			else:
				print ('minumum blur value reached')
		if (key_pressed == 27):
			cv2.destroyAllWindows()
			exit()
		cv2.destroyAllWindows()
	return(img)

def getContours(edges,img):
	thickness=3
	contours, hierarchy = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
	areas = []
	for i in range(len(contours)):
		area = cv2.contourArea(contours[i])
		areas.append([area,i])
	areas.sort(key=lambda x: x[0],reverse=True)
	i = 0
	while (i< len(contours)):
		temp = img.copy()
		area_key = areas[i]
		c = contours[area_key[1]]
		cv2.drawContours(temp, c, -1, (0,255,0), thickness)
		cv2.imshow('select contour to process',temp)
		cv2.moveWindow('select contour to process',0,0)
		key_pressed = cv2.waitKey(0)
		if (key_pressed == 10):
			cv2.destroyAllWindows()
			return(c,thickness)
		if (key_pressed == 65361):
			if (i>0):
				i = i - 1
			else:
				print ('first contour reached')
			cv2.destroyAllWindows()
		if (key_pressed == 65363):
			i = i+1
			cv2.destroyAllWindows()
		if (key_pressed == 65362):
			thickness = thickness + 1
			cv2.destroyAllWindows()
		if (key_pressed == 65364):
			if (thickness > 1):
				thickness = thickness - 1
			else:
				print ('minumim thickness reached')
			cv2.destroyAllWindows()
		if (key_pressed == 27):
			cv2.destroyAllWindows()
			exit()

def processImage(image,output_file = 'all_data.csv',object_id = 39):
	img = None
	if (str(type(image))=='<type \'str\'>'):
		img = cv2.imread(image)
	if (str(type(image))=='<type \'numpy.ndarray\'>'):
		img = image.copy()
	img = preProcess(img)
	edges = edgeDetection(img)
	contour,thickness = getContours(edges,img)
	area_perim = (cv2.contourArea(contour))/(cv2.arcLength(contour,True))
	convex_hull = cv2.convexHull(contour,returnPoints=True)
	total_convex = (perimeter(contour))/ (perimeter(convex_hull))
	print ('area_perim -  '+str(area_perim))
	print ('convex_total - '+str(total_convex))
	print('Enter - write data to file and return to image selection\nC - cancel return to image selection without writing data to file')
	print ('R - reprocess image\nESC - quit')
	cv2.drawContours(img, contour, -1, (0,255,0), thickness)
	cv2.imshow('review image before writing data to file',img)
	cv2.moveWindow('review image before writing data to file',0,0)
	key_pressed = cv2.waitKey(0)
	if (key_pressed == 10):
		f = open(output_file,'a')
		out = str(object_id) + ',' + str(area_perim) + ',' + str(total_convex) + '\n'
		f.write(out)
		print ('Data written to file')
		return
	if (key_pressed == 114):
		cv2.destroyAllWindows()
		processImage(img)
	if (key_pressed == 99):
		cv2.destroyAllWindows()
		return
	if (key_pressed == 27):
		cv2.destroyAllWindows()
		exit()

def preProcess(image):
	return (image)

def help():
	print ('Instructions to go here')	

def main(fp):
	while (True):
		files = os.listdir(fp)
		i = 0
		while (i < len(files)):
			image = fp + files[i]
			img = cv2.imread(image)
			cv2.imshow('select image to process',img)
			cv2.moveWindow('select image to process',0,0)
			key_pressed = cv2.waitKey(0)
			if ( key_pressed == 10):
				processImage(img)
			if ( key_pressed == 65363):
				i = i + 1
				cv2.destroyAllWindows()
			if ( key_pressed == 65361):
				if (i>0):
					i = i - 1
				else:
					print ('beginning of image file list reached')
				cv2.destroyAllWindows()
			if ( key_pressed == 27):
				cv2.destroyAllWindows()
				return
		
if (len(sys.argv)>1):
	path = sys.argv[1]
	main(path)
else:
	fp = os.path.dirname(__file__) + 'images/bananas/'
	main(fp)
exit()
