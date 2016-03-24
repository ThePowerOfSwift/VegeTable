import cv2
import numpy as np
import cmath
from matplotlib import pyplot as plt

image_filename = 'banana3.jpg'
data_out_filename = 'data_out.txt'
data_in_filename = 'data_in.txt'

img = cv2.imread(image_filename)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #convert to grayscale
img = cv2.GaussianBlur(img, (5,5),0) #blur image to reduce insignificant edges
img = cv2.Canny(img,10,20) #run canny edge detector
#contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

cv2.imshow('img',img)
cv2.waitKey(0)


cv2.destroyAllWindows()
