from pybrain.tools.xml.networkreader import NetworkReader
from PIL import Image
import PIL
import numpy
from numpy import ravel
from timeit import default_timer as timer
from os import listdir
from os.path import isfile, join

# Initialize some variables
dataDir = "../../data/imagenet/training_images/"
#supportedFruits = ['Apple', 'Orange', 'Banana']
supportedFruits = ['Apple', 'Unknown']
width = 100
height = 100
allFiles = []
allTargets = []

# Go through all of the supported fruits (expecting folder name to reflect the name of the fruit)
# and load all the file names and expected target
for fruit in supportedFruits:
    dirlist = listdir(dataDir+fruit)
    nPic = 0
    for f in dirlist:
        if isfile(join(dataDir+fruit, f)) and (f[0] is not '.'):
            filename = [dataDir + fruit + "/" + f]
            allFiles.extend(filename)
            allTargets.extend([fruit] * len(filename))
            nPic += 1

print str(len(allFiles)) + " files found for training..."

print "Loading neural network..."
start = timer()
fnn = NetworkReader.readFrom('VegeTable_PyBrain_Neural_Network.xml')
end = timer()
print "Time taken to load neural network: " + str(end-start)

print "Load image to match..."
#img = Image.open(allFiles[4])
img = Image.open("../../data/testImages/apple1.jpeg")
img = img.resize([width, height],PIL.Image.ANTIALIAS)
# img = img.convert("L")
imgArray = numpy.asarray(img.getdata())

result = fnn.activate(ravel(imgArray))

print result

print "Matched to: " + supportedFruits[result.argmax()]