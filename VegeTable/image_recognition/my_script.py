#########################################################################
#																	    #
#   Imaging processing script run via 'main' function at end of file.   #
#																		#
#	Written By: David Ferullo											#
#																	    #
#########################################################################

#IMPORTS:
#OpenCV library for image processing and numpy for large binary arrays
import cv2
import numpy as np

#Resize image for 
def resizeImage(img):
	height, width, channels = img.shape
	size = float(height * width)
	new_size = float(200 * 200)
	ratio = (new_size / size) ** 0.5
	if (ratio < 1):
		new_height = int(height * ratio)
		new_width = int(width * ratio)
		small = cv2.resize(img, (new_width,new_height)) 
		return (small)
	else:
		return(img)

#mask image to extract object based on hue
def hueMask(img):
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	height, width, channels = img.shape
	lower = np.array([0,50,50])
	upper = np.array([255,255,255])
	mask = cv2.inRange(hsv, lower, upper)
	obj = cv2.bitwise_and(img,img, mask=mask)
	return (obj,mask)

#get list of percentages for hue ranges that comprise masked object
def applyFilters(obj,mask):
	pcts = []
	totals = []
	h_low = 0
	h_high = 5
	hsv = cv2.cvtColor(obj, cv2.COLOR_BGR2HSV)
	total = 0
	for row in mask:
		for pixel in row:
			total += pixel
	totals.append(total)
	while ( h_high <= 255):
		lower = np.array([h_low,50,50])
		upper = np.array([h_high,255,255])
		f_mask = cv2.inRange(hsv, lower, upper)
		f_total = 0
		for row in f_mask:
			for pixel in row:
				f_total += pixel
		totals.append(f_total)
		pct = int((float(f_total)/total) * 100)
		pcts.append(pct)
		h_low += 5
		h_high += 5
	return (pcts)

#get shape data using area and perimeter of masked object
def shapeData(mask,img):
	height = len(mask)
	width = len(mask[0])
	perimeter = 0
	area = 0
	i = 1
	coords = []
	x_min = width
	x_max = 0
	y_min = height
	y_max = 0
	while (i < (len(mask) - 1) ):
		j = 1
		while (j < (len(mask[i]) -1 ) ):
			matrix = [[mask[i-1][j-1],mask[i-1][j],mask[i-1][j+1]],[mask[i][j-1],mask[i][j],mask[i][j+1]],[mask[i+1][j-1],mask[i+1][j],mask[i+1][j+1]]]
			m_total = 0
			for m in matrix:
				m_total += sum(m)
			if ( m_total > 0 ):
				if ( m_total == 2295):
					area += 1
				else:
					perimeter += 1
					if ( j < y_min ):
						y_min = j
					if ( j > y_max ):
						y_max = j
					if ( i < x_min ):
						x_min = i
					if ( i > x_max ):
						x_max = i
			j += 1
		i += 1
	ratio = float(area)/perimeter
	return (ratio)

#main image processing function, calls other image processing functions and returns data to main function
def processImage(filepath):
	img = cv2.imread(filepath)
	img = resizeImage(img)
	height, width, channels = img.shape
	obj,mask = hueMask(img)
	shape = shapeData(mask,img)
	filters = applyFilters(obj,mask)
	return (shape,filters)

#function identifies object based on image data including hue ranges and object shape
def identify(stat):
	shape = stat[0]
	filters = stat[1]
	highs = []
	i = 0
	while (i < len(filters)):
		if (filters[i] > 10):
			highs.append(i)
		i += 1
	print (highs)
	if ( (0 in highs) and ( (34 in highs) or (35 in highs) ) ):
		return('apple')
	elif ( (4 in highs) and (shape < 10) ):
		return('banana')
	elif ( ( (2 in highs) or (3 in highs) ) and (shape > 10 ) ):
		return ('orange')
	elif ( ( (2 in highs) or (3 in highs) ) and (shape < 7 ) ):
		return ('carrot')
	elif ( 10 in highs ):
		return ('cucumber')
	else:
		return ('unknown')

#main function to be called by server program
def main(filepath):
	try:
		shape,filters = processImage(filepath)
		data = [shape,filters]
		return(identify(data))
	except:
		return ('unknown')
