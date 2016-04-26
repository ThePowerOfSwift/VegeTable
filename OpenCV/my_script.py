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

#Returns the length of the perimeter of the masked object
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

#Returns the area of the masked object
def getArea(mask):
	total = 0
	for row in mask:
		for pixel in row:
			total += pixel
	return (total)

#Returns array of coordinates for largest object identified in image
#Uses the OpenCV function findContours build an array of arrays of coordinates of all objects, sorts
#the array to find the largest object based on perimeter length
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
	return (contour)

#Returns a binary mask of the image to extract the object to be identified. Works only for objects on
#white backgrounds, pixels with total value exceeding threshhold value are part of the object
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
	return (mask)

#Returns the average b/g/r value pixels in the object to be identified
#identifies pixels in input image to be processed using binary mask image
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

#Returns identity of unknown object in input image.
#Compares data from input image against data from known images, returns the identity that is closest to data in the 'data' array
def identifyObject (image_data):
	data = [['apple',11.4304752439,5.17976497623,24,33,156],['apple',15.1892916389,5.4177214839,34,38,159],['apple',24.8131607564,3.6934206395,79,109,197],['apple',20.7979382019,4.16433549348,45,46,153],['apple',13.4574134502,4.14487340468,62,70,192],['apple',12.457566353,4.16890138324,60,63,180],['apple',18.2567607447,5.28119492839,43,34,180],['apple',61.1959949646,6.1736788417,47,57,144],['apple',61.5105953982,6.86478934692,44,47,120],['apple',9.79161690198,4.3579499503,24,24,140],['apple',65.0483164055,9.29891482295,61,64,179],['apple',10.6546805992,3.69996036901,57,58,155],['banana',24.7087641675,7.64722118118,57,164,221],['banana',15.9364461055,9.02075951297,49,155,208],['banana',39.6756945773,8.81072465173,28,177,238],['banana',15.8632241123,10.6817034001,72,157,214],['banana',24.7087641675,7.64722118118,57,164,221],['banana',13.6339431897,8.02431405847,23,168,248],['banana',23.8338564903,9.09455254415,69,169,224],['banana',145.798185434,12.4585891819,44,152,194],['banana',15.4538559789,7.20019567691,31,137,201],['banana',27.3878651215,9.41263226353,43,178,239],['banana',29.6024303484,10.9565502792,37,160,209],['banana',17.2823681082,10.5486136111,49,155,208],['orange',15.9317761359,3.75955037072,24,151,238],['orange',14.1881121057,4.01889495514,33,135,228],['orange',11.8891770418,4.25631026379,20,121,246],['orange',85.1486153623,6.8098274861,59,144,238],['orange',21.0674211959,4.30495231618,69,132,244],['orange',11.2500808932,3.7212413642,24,134,227],['orange',19.4129857654,3.78531774471,8,143,244],['orange',64.270361611,4.66509156572,74,149,217],['orange',10.8649825993,4.16360640603,15,121,247],['orange',15.9701525311,4.50961282451,23,92,206],['orange',42.741849609,6.54480078258,66,135,240],['orange',10.6574935027,4.04721758896,45,123,238],['broccoli',20.3529508925,6.10280166225,81,111,101],['broccoli',19.5582777092,7.02762867849,53,117,108],['broccoli',21.4122129747,5.2163861566,76,134,114],['broccoli',43.7757912981,6.81190456767,79,147,137],['broccoli',73.6592728841,11.1200931186,78,143,127],['broccoli',87.0131446539,9.64887367156,81,151,123],['broccoli',104.236164565,4.43686756438,63,110,70],['broccoli',22.4934935051,4.38732639578,76,136,116],['broccoli',28.5696732091,5.20955060769,53,107,96],['broccoli',58.2340136065,7.08000326046,62,112,106],['broccoli',33.255285698,6.02640117007,85,129,123],['broccoli',21.4122129747,5.2163861566,76,134,114],['cucumber',23.4277263797,7.5171453596,41,118,82],['cucumber',23.6984676305,7.28827572691,67,89,77],['cucumber',19.5941345885,5.897870359,39,115,85],['cucumber',22.0713117393,7.41747282746,61,120,84],['cucumber',27.3598687657,7.51165208981,39,159,120],['cucumber',25.6413002288,6.61976630296,58,89,77],['cucumber',16.2324904736,8.28165931407,43,111,88],['cucumber',24.863456379,7.92374895288,88,105,94],['cucumber',15.5746489473,5.69075814878,66,89,76],['cucumber',19.5941345885,5.897870359,39,115,85],['cucumber',16.3470960814,5.18674415512,69,108,104],['cucumber',16.8196280419,8.1951764063,24,68,84],['carrot',9.56865850392,5.40941271503,81,124,248],['carrot',62.3154905054,13.8075678507,47,133,218],['carrot',105.87350875,18.5170523683,47,137,233],['carrot',477.395870492,27.7180542654,44,101,119],['carrot',20.1762018713,7.8868595277,85,136,242],['carrot',47.6945852698,15.6597097324,50,117,233],['carrot',58.5753996129,18.0089755729,63,140,234],['carrot',55.2687613331,14.766727291,33,117,247],['carrot',41.6510936915,10.0955404786,36,116,230],['carrot',14.4419646558,6.74064323549,43,89,216],['carrot',47.9835169894,11.0712243238,33,113,240],['carrot',12.7100335018,13.13877368,61,117,236]]
	convex_ratio = image_data[0]
	area_ratio = image_data[1]
	b = float(image_data[2])
	g = float(image_data[3])
	r = float(image_data[4])
	matches = []
	for d in data:
		ident = d[0]
		convex_ratio_src = d[1]
		area_ratio_src = d[2]
		b_src = float(d[3])
		g_src = float(d[4])
		r_src = float(d[5])
		convex_ratio_pct = abs((convex_ratio - convex_ratio_src)/convex_ratio_src)
		area_ratio_pct = abs((area_ratio - area_ratio_src)/area_ratio_src)
		b_pct = abs((b - b_src)/b_src)
		g_pct = abs((g - g_src)/g_src)
		r_pct = abs((r - r_src)/r_src)
		pct_dif_avg = (convex_ratio_pct + area_ratio_pct + b_pct + g_pct + r_pct ) / 5
		match = [ident,pct_dif_avg]
		matches.append(match)
	best_id = 0
	best_pct = 100
	for m in matches:
		if (m[1] < best_pct):
			best_id = m[0]
			best_pct = m[1]
	return (best_id,best_pct)

#Image processing function, responsible for calling various functions to extract image characteristics
#Returned values are:
#	1) Ratio of perimeter of object over the length of convex curves in the perimeter
#	2) Ratio of area of the object over the total perimeter length
#	3) Average blue value of pixels in the object
#	4) Average green value of pixels in the object
#	5) Average red value of pixels in the object
def processImage(image):
	img = None
	if (str(type(image))=='<type \'str\'>'):
		img = cv2.imread(image)
	if (str(type(image))=='<type \'numpy.ndarray\'>'):
		img = image.copy()
	height, width, channels = img.shape
	orig = img.copy()
	mask = maskImage(img)
	contour = getContours(img,mask)
	b, g, r = getColor(mask,img)
	convex_hull = cv2.convexHull(contour,returnPoints=True)
	perim = perimeter(contour)
	total_convex = (perim)/ (perimeter(convex_hull))
	perim_area = (perim/getArea(mask))
	return ([total_convex,perim_area,b,g,r])

#Main function, takes relative path to image file as argument
def main(path):
	try:
		img = cv2.imread(path)  	#read input image
		data = processImage(img)	#get parameters of input image
		identity, pct_dif = identifyObject(data) #get identity of input image by comparing against learned data
		return (identity,pct_dif)
	except:
		return ('error',1)
