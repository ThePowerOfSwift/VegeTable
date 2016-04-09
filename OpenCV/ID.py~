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

def processImage(image):
	img = None
	if (str(type(image))=='<type \'str\'>'):
		img = cv2.imread(image)
	if (str(type(image))=='<type \'numpy.ndarray\'>'):
		img = image.copy()
	height, width, channels = img.shape
	orig = img.copy()
	mask = maskImage(img)
	img, contour = getContours(img,mask)
	b, g, r = getColor(mask,img)
	convex_hull = cv2.convexHull(contour,returnPoints=True)
	total_convex = (perimeter(contour))/ (perimeter(convex_hull))
	return ([total_convex,b,g,r])

def parseLine(line):
	s = ''
	field = 0
	d = 0
	data = []
	for c in line:
		if (c != ','):
			s = s + c
		else:
			if (field == 1):
				d = float(s)
			else:
				d = int(s)
			field += 1
			s = ''
			data.append(d)
	d = int(s)
	data.append(d)
	return (data)

def getData(data_source):
	all_data = []
	with open(data_source,'r') as f:
		for line in f:
			data = parseLine(line)
			all_data.append(data)
	return (all_data)

def identifyObject (image_data,data_source):
	data = getData(data_source)
	ratio = image_data[0]
	b = float(image_data[1])
	g = float(image_data[2])
	r = float(image_data[3])
	matches = []
	for d in data:
		id_num = d[0]
		ratio_src = d[1]
		b_src = float(d[2])
		g_src = float(d[3])
		r_src = float(d[4])
		ratio_pct = abs((ratio - ratio_src)/ratio_src)
		b_pct = abs((b - b_src)/b_src)
		g_pct = abs((g - g_src)/g_src)
		r_pct = abs((r - r_src)/r_src)
		pct_dif_avg = (ratio_pct + b_pct + g_pct + r_pct ) / 4
		match = [id_num,pct_dif_avg]
		matches.append(match)
	best_id = 0
	best_pct = 100
	for m in matches:
		if (m[1] < best_pct):
			best_id = m[0]
			best_pct = m[1]
	return (best_id,best_pct)

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
				data = processImage(img)
				identity, pct_dif = identifyObject(data,'data.csv')
				print (identity)
			if ( key_pressed == 65363):
				i = i + 1
				cv2.destroyAllWindows()
			if ( key_pressed == 65361):
				if (i>0):
					i = i - 1
				else:
					i = len(files)-1
				cv2.destroyAllWindows()
			if ( key_pressed == 27):
				cv2.destroyAllWindows()
				return
		
if (len(sys.argv)>1):
	path = sys.argv[1]
	main(path)
else:
	fp = os.path.dirname(__file__) + 'images/test/'
	main(fp)
exit()
