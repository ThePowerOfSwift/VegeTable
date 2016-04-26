# Based on example located here:
# https://pythonprogramming.net/feature-matching-homography-python-opencv-tutorial/

# Results: this algorithm has poor matching results for two bananas

import numpy as np
import cv2
import matplotlib.pyplot as plt

imgPath = "../../data/images/"

imgTemplate = cv2.imread(imgPath+'banana/banana2.jpeg',0)
imgSearch = cv2.imread(imgPath+'banana/banana3.jpeg',0)

# this line is necessary for use with OpenCV 3.0, some bug results in an error otherwise
cv2.ocl.setUseOpenCL(False)

#plt.figure()
#plt.imshow(imgTemplate)
#plt.show()


orb = cv2.ORB_create()

kp1, des1 = orb.detectAndCompute(imgTemplate,None)
kp2, des2 = orb.detectAndCompute(imgSearch,None)

bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

matches = bf.match(des1,des2)
matches = sorted(matches, key = lambda x:x.distance)

imgMatch = cv2.drawMatches(imgTemplate,kp1,imgSearch,kp2,matches[:10],None, flags=2)
plt.imshow(imgMatch)
plt.show()