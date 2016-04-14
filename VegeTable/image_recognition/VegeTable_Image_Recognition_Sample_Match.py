from pybrain.tools.xml.networkreader import NetworkReader
from PIL import Image
import PIL
import numpy
import cv2
import numpy as np
from numpy import ravel
from timeit import default_timer as timer
from os import listdir
from os.path import isfile, join

# Initialize some variables
dataDir = "../../data/testImages"
#supportedFruits = ['Apple', 'Orange', 'Banana']
supportedFruits = ['Apple', 'Unknown']
width = 100
height = 100
allFiles = []
allTargets = []

# Load all of the files in the testImages folder
dirlist = listdir(dataDir)
for f in dirlist:
    if isfile(join(dataDir, f)) and (f[0] is not '.'):
        filename = [dataDir + "/" + f]
        allFiles.extend(filename)
print str(len(allFiles)) + " files found for testing..."

print "Loading neural network..."
start = timer()
fnn = NetworkReader.readFrom('VegeTable_PyBrain_Neural_Network.xml')
end = timer()
print "Time taken to load neural network: " + str(end-start)

def autocrop(image, threshold=0):
    """Crops any edges below or equal to threshold

    Crops blank image to 1x1.

    Returns cropped image.

    """
    if len(image.shape) == 3:
        flatImage = np.max(image, 2)
    else:
        flatImage = image
    assert len(flatImage.shape) == 2

    rows = np.where(np.max(flatImage, 0) > threshold)[0]
    if rows.size:
        cols = np.where(np.max(flatImage, 1) > threshold)[0]
        image = image[cols[0]: cols[-1] + 1, rows[0]: rows[-1] + 1]
    else:
        image = image[:1, :1]

    return image

print "Matching images..."
for imFile in allFiles:
    img = cv2.imread(imFile)

    blur = cv2.GaussianBlur(img, (15,15),0)

    hsv = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

    lower_hue = np.array([0,75,75])
    upper_hue = np.array([25,255,255])

    mask = cv2.inRange(hsv, lower_hue, upper_hue)

    res = cv2.bitwise_and(img,img, mask= mask)

    res = cv2.resize(res,(width,height))

    cv2.imwrite("temp.jpeg",res)

    imgPIL = Image.open("temp.jpeg")
    imgArray = numpy.asarray(imgPIL.getdata())

    start = timer()
    result = fnn.activate(ravel(imgArray))
    end = timer()

    if result[0] > 0.3:
        matchRes = "Apple"
    else:
        matchRes = "Unknown"

    print imFile + " Matched to: "+matchRes+" in "+str(end-start)+"sec with prediction scores: ", result


    res = cv2.putText(res, matchRes, (0,len(res[0,:,0])-10), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, [255,255,255])

    cv2.imshow("processed",res)
    cv2.imshow("original",img)
    cv2.moveWindow("processed",110,0)
    cv2.moveWindow("original",210,0)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


