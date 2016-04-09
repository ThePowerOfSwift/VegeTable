from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.xml.networkwriter import NetworkWriter
from pybrain.tools.xml.networkreader import NetworkReader
from numpy import ravel
import os
from os import listdir
from os.path import isfile, join
from PIL import Image
import PIL
import numpy
from timeit import default_timer as timer

# Initialize some variables
numEpochs = 35
dataDir = "../../data/imagenet/training_images/"
supportedFruits = ['Apple', 'Grape', 'Orange', 'Banana']
width = 50
height = 50
allFiles = []
allTargets = []

# Go through all of the supported fruits (expecting folder name to reflect the name of the fruit)
# and load all the file names and expected target
for fruit in supportedFruits:
    dirlist = listdir(dataDir+fruit)
    nPic = 0
    for f in dirlist:
        if isfile(join(dataDir+fruit, f)) and (f[0] is not '.') and (nPic < 20):
            filename = [dataDir + fruit + "/" + f]
            allFiles.extend(filename)
            allTargets.extend([fruit] * len(filename))
            nPic += 1

print str(len(allFiles)) + " files found for training..."

# Now initialize the neural network, use width*height for the size of the data because all of the images need to
# be resized, greyscaled, and then flattened
print "Loading image files..."
ds = ClassificationDataSet(width*height, 1 , nb_classes=len(supportedFruits))
for k in xrange(len(allFiles)):
    img = Image.open(allFiles[k])
    img = img.resize([width, height],PIL.Image.ANTIALIAS)
    img = img.convert("L")
    imgArray = numpy.asarray(img.getdata())
    ds.addSample(ravel(imgArray)[0], supportedFruits.index(allTargets[k]))

# Split the data set into 75/25, the 75% being the data that is used to train, the 25% will be used to test
# the quality of the neural network training
tstdata, trndata = ds.splitWithProportion( 0.25 )

trndata._convertToOneOfMany( )
tstdata._convertToOneOfMany( )

# Build a new neural network
print "Building the neural network, in-dimension: " + str(trndata.indim) + ", out-dimension: " + str(trndata.outdim)
fnn = buildNetwork( trndata.indim, int(0.5*trndata.indim), trndata.outdim, outclass=SoftmaxLayer )

# Create a new backpropagation trainer
print "Creating backpropagation trainer..."
#trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, learningrate=0.01 , verbose=True, weightdecay=0.01)
trainer = BackpropTrainer(fnn, dataset=trndata, verbose=True)

# Perform epoch training
print "Beginning "+str(numEpochs)+" training epochs..."
start = timer()
trainer.trainEpochs(numEpochs)
end = timer()
print "Time taken for epochs: " + str(end-start)

print 'Percent Error on Test dataset: ' , percentError( trainer.testOnClassData (
           dataset=tstdata )
           , tstdata['class'] )

print "Writing neural network to file..."
NetworkWriter.writeToFile(fnn, 'VegeTable_PyBrain_Neural_Network.xml')