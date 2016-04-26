from numpy import ravel
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
import PIL
import numpy
from timeit import default_timer as timer
from sklearn.svm import SVC

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
#        if isfile(join(dataDir+fruit, f)) and (f[0] is not '.') and (nPic < 20):
        if isfile(join(dataDir+fruit, f)) and (f[0] is not '.'):
            filename = [dataDir + fruit + "/" + f]
            allFiles.extend(filename)
            allTargets.extend([fruit] * len(filename))
            nPic += 1

print str(len(allFiles)) + " files found for training..."

# Now initialize the neural network, use width*height for the size of the data because all of the images need to
# be resized, greyscaled, and then flattened
print "Loading image files..."
x = []
y = []
for k in xrange(len(allFiles)):
    img = Image.open(allFiles[k])
    img = img.resize([width, height],PIL.Image.ANTIALIAS)
#    img = img.convert("L")
    imgArray = numpy.asarray(img.getdata())
    x.append(ravel(imgArray))
    y.append(supportedFruits.index(allTargets[k]))



print "Beginning fit algorithm..."
start = timer()
clf = SVC()
clf.fit(x,y)
end = timer()
print "Time taken for fit: " + str(end-start)


img = Image.open("../../data/testImages/apple1.jpeg")
img = img.resize([width, height],PIL.Image.ANTIALIAS)
# img = img.convert("L")
imgArray = numpy.asarray(img.getdata())
xtest = ravel(imgArray)

result = clf.predict([xtest])

print result

print "Matched to: " + supportedFruits[result]