import sys
import cv2
import numpy as np
import cmath
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

def main():
	try:
		image_filename = raw_input('Enter image filename: ')
		data_out_filename = 'data_out.txt'
		data_in_filename = 'data_in.txt'
		out_file = open(data_out_filename,'a')

		img = cv2.imread(image_filename)
		cv2.imshow('image',img)
		cv2.waitKey(0)

		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		img = cv2.GaussianBlur(img, (5,5),0)
		img = cv2.Canny(img,40,80)
		cv2.imshow('image',img)
		cv2.waitKey(0)

		contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

		for i in range(min(10,len(contours))):
			try:
				orig = cv2.imread(image_filename)
				contour = contours[i]
				cv2.drawContours(orig, contour, -1, (0,255,0), 3)
				cv2.imshow('contours-' + str(i),orig)
				cv2.waitKey(0)

				orig = cv2.imread(image_filename)
				convex_hull = cv2.convexHull(contours[i],returnPoints=True)
				cv2.drawContours(orig, convex_hull, -1, (0,255,0), 3)
				cv2.imshow('convex hull-' + str(i),orig)

				cv_contour_perimeter = cv2.arcLength(contours[i],True)
				cv_contour_area = cv2.contourArea(contours[i])
				cv_ratio = cv_contour_area / cv_contour_perimeter
				convex_perimeter = perimeter(convex_hull)
				contour_perimeter = perimeter(contours[i])
				ratio = contour_perimeter / convex_perimeter

				print ('cv ratio - ' + str(cv_ratio))
				print ('ratio - ' + str(ratio))
				query = raw_input('Contour shown(Y/N)? ')
				if ( (query=='Y') or (query=='y') ):
					query = raw_input('Enter ID #: ')
					data = str(query) + ' ' + str(cv_ratio) + ' ' + str(ratio) + '\n'
					try:
						out_file.write(data)
						print ('data written to ' + data_out_filename)
					except:
						print ('error writing to file')
					query = raw_input('Enter new image filename(Y/N)? ')
					if ( (query == 'Y') or (query == 'y') ):
						cv2.destroyAllWindows()
						main()
					cv2.destroyAllWindows()
				break
				cv2.waitKey(0)
				cv2.destroyAllWindows()
			except:
				print ('error')
		cv2.destroyAllWindows()
	except:
		print ('Error with image file. Check filename/format')
		cv2.destroyAllWindows()
main()
exit()
