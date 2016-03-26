# Standard imports
import cv2
import numpy as np;
 
# Read image
im = cv2.imread("fruit.jpg")
cv2.imshow('image',im)
cv2.waitKey(0)

im = cv2.GaussianBlur(im, (9,9),0) #blur image to reduce insignificant edges
cv2.imshow('image',im)
cv2.waitKey(0)
 
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector()
 
# Detect blobs.
keypoints = detector.detect(im)
 
# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
