#######################################################################
#TODO: 
#	1) Explore other methods to sort contours (currently largest area)
#	2) Find way to extract average color value from within contour
#	3) Add to preProcessing stub to add filtering functionality
#	4) Add support for terminal arguments
#		a) folder path
#		b) fruit/veggie id number for folder
#Issues:
#	1) OpenCV function cv2.contourArea returns incorrect results if 
#	   contour intersects itself
#		a) Use area of minBoundingRectangle instead?
#	2) If image is not color (grayscale, h/s/v layer) contour is not
#	   in color and is difficult to see
#	******image segmentation matlab******
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

def edgeDetection(image,blur=1,lower=1,upper=2):
	print ('\nUp/Down: Increase/Decrease blur\nRight/Left: Increase/Decrease edge detection threshold\nESC: Exit\n')
	while ( True ):
		img = image.copy()
		img = cv2.GaussianBlur(img,(blur,blur),0)
		img = cv2.Canny(img,lower,upper)
		cv2.imshow('select edges to search for contours',img)
		cv2.moveWindow('select edges to search for contours',0,0)
		key_pressed = cv2.waitKey(0)
		cv2.destroyAllWindows()
		if (key_pressed == 10):
			return (img)
		if (key_pressed == 65363):
			lower = lower + 1
			upper = upper + 10
		if (key_pressed == 65361):
			if (lower > 1):
				lower = lower - 1
				upper = upper - 10
			else:
				print ('minumum threshold value reached')
		if (key_pressed == 65362):
			blur = blur + 2
		if (key_pressed == 65364):
			if (blur > 1):
				blur = blur - 2
			else:
				print ('minumum blur value reached')
		if (key_pressed == 27):
			exit()
		cv2.destroyAllWindows()
	return(img)

def getContours(edges,img):
	print ('\nUp/Down: Increase/Decrease contour line thickness\nRight/Left: Change contour\nESC: Exit\n')
	thickness=3
	contours, hierarchy = cv2.findContours(edges,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
	areas = []
	#for i in range(len(contours)):
	#	area = cv2.contourArea(contours[i])
	#	areas.append([area,i])
	#areas.sort(key=lambda x: x[0],reverse=True)
	for i in range(len(contours)):
		perim = perimeter(contours[i])
		areas.append([perim,i])
	areas.sort(key=lambda x: x[0],reverse=True)
	i = 0
	while (i< len(contours)):
		temp = img.copy()
		area_key = areas[i]
		c = contours[area_key[1]]
		cv2.drawContours(temp, c, -1, (0,0,255), thickness)
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

def preProcess(image):
	print ('\nLeft/Right: Change image filtering\nEnter: Select filtered image to process\nESC: Exit\n')
	img = image.copy()
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	h,s,v = cv2.split(image)
	i = 0
	while (True):
		if (i == 0):
			cv2.imshow('full color',image)
			cv2.moveWindow('full color',0,0)
			img = image.copy()
		if (i == 1):
			cv2.imshow('grayscale',gray)
			cv2.moveWindow('grayscale',0,0)
			img = gray.copy()
		if (i == 2):
			cv2.imshow('hue layer',h)
			cv2.moveWindow('hue layer',0,0)
			img = h.copy()
		if (i == 3):
			cv2.imshow('saturation layer',s)
			cv2.moveWindow('saturation layer',0,0)
			img = s.copy()
		if (i == 4):
			cv2.imshow('value layer',v)
			cv2.moveWindow('value layer',0,0)
			img = v.copy()
		key_pressed = cv2.waitKey(0)
		cv2.destroyAllWindows()
		if (key_pressed == 65361):
			if (i > 0):
				i = i - 1
			else:
				i = 3
		if (key_pressed == 65363):
			if (i < 4):
				i = i + 1
			else:
				i = 0
		if (key_pressed == 10):
			cv2.destroyAllWindows()
			return (img)
		if (key_pressed == 27):
			cv2.destroyAllWindows()
			exit()

def maskImage(image,contour):
	out = open('output.csv','w+')
	c_list = []
	for c in contour:
		c_list.append([c[0][0],c[0][1]])
	c_list.sort(key=lambda x: x[0])
	row_list = []
	i = 0
	r = 0
	last = 0
	while (i<len(c_list)):
		x = c_list[i][0]
		y = c_list[i][1]
		if (i==0):
			row_list.append([x,[y]])
			last = x
		else:
			if(x == row_list[len(row_list)-1][0]):
				row_list[len(row_list)-1][1].append(y)
			else:
				row_list.append([x,[y]])
		i = i + 1
	height, width, channels = image.shape
	mask = np.zeros( (height,width) )
	for row in row_list:
		y = row[0]
		row[1].sort()
		i = 0
		while (i<len(row[1])):
			x = row[1][i]
			mask[x][y] = 1
			if (i>0):
				x_0 = row[1][i-1]
				while (x_0 < x):
					mask[x_0][y] = 1
					x_0 = x_0 + 1
			i = i + 1
	cv2.imshow('mask',mask)
	cv2.moveWindow('mask',0,0)
	cv2.waitKey(0)
	return (mask)

def getColor(mask,image):
	cv2.imshow('mask',mask)
	cv2.moveWindow('mask',0,0)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	cv2.imshow('image',image)
	cv2.moveWindow('image',0,0)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	pixels = 0
	b = 0
	g = 0
	r = 0
	for i in range(len(mask)):
		mask_row = mask[i]
		row = image[i]
		for j in range(len(mask_row)):
			mask_column = mask_row[j]
			column = row[j]
			if (mask_column == 1):
				pixels += 1
				b = b + column[0]
				g = g + column[1]
				r = r + column[2]
	b_avg = b / pixels
	g_avg = g / pixels
	r_avg = r / pixels
	return (b_avg, g_avg, r_avg)

def getArea(mask):
	cv2.imshow('mask',mask)
	cv2.waitKey(0)
	total = 0
	for row in mask:
		for pixel in row:
			total += pixel
	return (total)

def processImage(image,output_file = 'data.csv',object_id = 39):
	img = None
	if (str(type(image))=='<type \'str\'>'):
		img = cv2.imread(image)
	if (str(type(image))=='<type \'numpy.ndarray\'>'):
		img = image.copy()
	orig = img.copy()
	img = preProcess(img)
	edges = edgeDetection(img)
	contour,thickness = getContours(edges,img)
	mask = maskImage(image,contour)
	b,g,r = getColor(mask,image)
	perim_area = (perimeter(contour))/(getArea(mask))
	convex_hull = cv2.convexHull(contour,returnPoints=True)
	total_convex = (perimeter(contour))/ (perimeter(convex_hull))
	print ('perim/area -  '+str(perim_area))
	print ('convex length/total length - '+str(total_convex))
	print ('b/g/r values - ' + str(b) + '/' + str(g) + '/' + str(r))
	print('\nEnter - write data to file and return to image selection\nC - cancel return to image selection without writing data to file')
	print ('R - reprocess image\nESC - quit\n')
	cv2.drawContours(img, contour, -1, (0,255,0), thickness)
	cv2.imshow('review image before writing data to file',img)
	cv2.moveWindow('review image before writing data to file',0,0)
	key_pressed = cv2.waitKey(0)
	if (key_pressed == 10):
		#f = open(output_file,'a')
		#out = str(object_id) + ',' + str(area_perim) + ',' + str(total_convex) + '\n'
		#f.write(out)
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

def main(fp):
	print ('\nLeft/Right: Change image to process\n')
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
				cv2.destroyAllWindows()
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
	fp = os.path.dirname(__file__) + 'images/simple/learning/39/'
	main(fp)
exit()
