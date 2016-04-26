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

def maskImage(image,height,width):
	thresh = 170
	mask = np.zeros( (height,width) )
	i = 0
	for i in range(len(image)):
		row = image[i]
		j = 0
		for j in range(len(row)):
			if ( row[j] < thresh):
				mask[i][j] = 1
			j += 1
		i += 1
	return (mask)

def getHueRange(mask,image):
	pixels = 0
	hues = []
	hue_total = 0
	n = 0
	for i in range(len(mask)):
		mask_row = mask[i]
		row = image[i]
		for j in range(len(mask_row)):
			if (mask_row[j] == 1):
				hues.append(row[j])
				hue_total += row[j]
				n += 1
	hue_avg = hue_total / n
	S = 0
	for hue in hues:
		S += (hue - hue_avg) ** 2
	S = S / n
	delta = 1.645 * S/(n**0.5)
	hue_lower = hue_avg - delta
	hue_upper = hue_avg + delta
	return (hue_lower,hue_upper)

def getArea(mask):
	total = 0
	for row in mask:
		for pixel in row:
			total += pixel
	return (total)

def getHue(img):
	h,s,v = cv2.split(img)
	return (h)

def processImage(image,output_file,object_id):
	img = image.copy()
	orig = img.copy()
	height, width, channels = img.shape
	img = getHue(img)
	mask = maskImage(img,height,width)
	img, contour = getContours(img,mask)
	lower, upper = getHueRange(mask,img)
	convex_hull = cv2.convexHull(contour,returnPoints=True)
	perim = perimeter(contour)
	total_convex = (perim)/ (perimeter(convex_hull))
	perim_area = (perim/getArea(mask))
	output = str(object_id) + ',' + str(total_convex) + ',' + str(perim_area) + ',' + str(lower) + ',' + str(upper) + '\n'
	f = open(output_file,'a')
	f.write(output)

def main(obj_id,fp):
	img_files = os.listdir(fp)
	for img_file in img_files:
		img_file_path = fp + img_file
		img = cv2.imread(img_file_path)
		processImage(img,'data.txt',obj_id)

clear_file = open('data.txt','w')
clear_file.close()
fp = os.path.dirname(__file__) + 'images/simple/learning/'
folders = os.listdir(fp)
for folder in folders:
	dir_path = fp + folder + '/'
	obj_id = int(folder)
	main(obj_id,dir_path)
