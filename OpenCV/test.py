#script to get opecv key id #s returned by cv2.waitKey function
import cv2
import os
fp = os.path.dirname(__file__) + 'images/bananas/'
fl = os.listdir(fp)
fn = fp + fl[0]
print (fn)
img = cv2.imread(fn)
cv2.imshow('image',img)
cv2.waitKey(0)
exit()