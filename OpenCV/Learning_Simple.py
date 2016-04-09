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

def getContours(image,mask):
	orig = image.copy()
	mask = np.array(mask * 255, dtype = np.uint8)
	contours, hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
	sizes = []
	for i in range(len(contours)):
		perim = perimeter(contours[i])
		sizes.append([perim,i])
	sizes.sort(key=lambda x: x[0],reverse=True)
	contour = contours[sizes[0][1]]
	cv2.drawContours(image, contour, -1, (0,0,255), 3)
	return (image,contour)

def maskImage(image):
	thresh = 125
	height, width, channels = image.shape
	mask = np.zeros( (height,width) )
	i = 0
	for i in range(len(image)):
		row = image[i]
		j = 0
		for j in range(len(row)):
			pixel = row[j]
			total = abs(255 - int(pixel[0])) + abs(255-int(pixel[1])) + abs(255-int(pixel[2]))
			if ( total > thresh):
				mask[i][j] = 1
			j += 1
		i += 1
	cv2.destroyAllWindows()
	return (mask)

def getColor(mask,image):
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

def processImage(image,output_file,object_id):
	img = image.copy()
	height, width, channels = img.shape
	orig = img.copy()
	mask = maskImage(img)
	img, contour = getContours(img,mask)
	b, g, r = getColor(mask,img)
	convex_hull = cv2.convexHull(contour,returnPoints=True)
	total_convex = (perimeter(contour))/ (perimeter(convex_hull))
	output = str(object_id) + ',' + str(total_convex) + ',' + str(b) + ',' + str(g) + ',' + str(r) + '\n'
	f = open(output_file,'a')
	f.write(output)

def main(obj_id,fp):
	img_files = os.listdir(fp)
	for img_file in img_files:
		img_file_path = fp + img_file
		img = cv2.imread(img_file_path)
		processImage(img,'data.csv',obj_id)

fp = os.path.dirname(__file__) + 'images/simple/'
folders = os.listdir(fp)
for folder in folders:
	dir_path = fp + folder + '/'
	obj_id = int(folder)
	main(obj_id,dir_path)
exit()
