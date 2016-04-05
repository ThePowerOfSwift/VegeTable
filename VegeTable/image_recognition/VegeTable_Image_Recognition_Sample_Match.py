from pybrain.tools.xml.networkreader import NetworkReader
from PIL import Image
import PIL
import numpy
from numpy import ravel
from timeit import default_timer as timer

supportedFruits = ['apple', 'grape', 'orange', 'banana']
width = 200
height = 200

print "Loading neural network..."
start = timer()
fnn = NetworkReader.readFrom('neuralNetwork.xml')
end = timer()
print "Time taken to load neural network: " + str(end-start)

print "Load image to match..."
img = Image.open("../../data/images/testImages/bananaTest.jpeg")
img = img.resize([width, height],PIL.Image.ANTIALIAS)
# img = img.convert("L")
imgArray = numpy.asarray(img.getdata())

result = fnn.activate(ravel(imgArray))

print "Matched to: " + supportedFruits[result.argmax()]