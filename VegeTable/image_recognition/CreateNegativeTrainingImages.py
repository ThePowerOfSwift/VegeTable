import urllib
import cv2
import numpy as np

for i in range(1,100,1):
    imFile = "../../data/imagenet/training_images/Unknown/negImage"+str(i)+".JPEG"
    urllib.urlretrieve("http://lorempixel.com/200/200/", imFile)
    img = cv2.imread(imFile)
    blur = cv2.GaussianBlur(img, (15,15),0)
    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    lower_hue = np.array([40,25,25])
    upper_hue = np.array([90,255,255])

    # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_hue, upper_hue)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)

    cv2.imwrite(imFile,res)
