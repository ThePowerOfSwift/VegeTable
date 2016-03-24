import cv2
import numpy as np
from matplotlib import pyplot as plt

filename = 'fruit.jpg'

img = cv2.imread(filename) #import image object with name 'img'
cv2.imshow('image',img)
cv2.waitKey(0)

img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #convert to hsv image
cv2.imshow('hsv image',img)
cv2.waitKey(0)

hue,sat,val = cv2.split(img) #split hsv image into channels

cv2.imshow('hue channel',hue) #display hue channel
cv2.waitKey(0)
hue = cv2.Canny(hue,100,200) #run edge detection on hue channel and display
cv2.imshow('hue channel edge detection',hue) 
cv2.waitKey(0)

cv2.imshow('saturation channel',sat)
cv2.waitKey(0)
sat = cv2.Canny(sat,100,200) #run edge detection on saturation channel and display
cv2.imshow('saturation channel edge detection',sat) 
cv2.waitKey(0)

cv2.imshow('value channel',val)
cv2.waitKey(0)
val = cv2.Canny(val,100,200) #run edge detection on value channel and display
cv2.imshow('value channel edge detection',val) 
cv2.waitKey(0)

cv2.destroyAllWindows()
