# This python script starts a server that receives a local file path to an image
# The image is then loaded and ran through the neural network and the manual algorithm to match images.
# Upon startup this script will take roughly 10-15 minutes to load the neural networks before
# the server begins listening for a path

import SocketServer
from pybrain.tools.xml.networkreader import NetworkReader
from PIL import Image
import numpy
import cv2
import numpy as np
from numpy import ravel
from timeit import default_timer as timer
import os
import thread
from my_script import main

# ********************** Variable initialization
# The resulting height and width of the image before neural network matching
width = 100
height = 100
# The hue values used for masking
appleHue = [np.array([0, 75, 75]), np.array([25, 255, 255])]
bananaHue = [np.array([20, 75, 75]), np.array([40, 255, 255])]
cucumberHue = [np.array([40, 25, 25]), np.array([90, 255, 255])]
appleXML = 'VegeTable_PyBrain_Neural_Network_Apple.xml'
bananaXML = 'VegeTable_PyBrain_Neural_Network_Banana.xml'
cucumberXML = 'VegeTable_PyBrain_Neural_Network_Cucumber.xml'


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # Get the request text, in this case it is the path to the image file to be matched
        imPath = str(self.request.recv(1024).strip())
        print("Matching File: {}".format(imPath))

        global apple
        global banana
        global cucumber

        # Perform the image matching, start by loading the image file
        if os.path.exists(imPath):
            # Load the image from the file
            img = cv2.imread(imPath)

            # Perform a gaussian blur on the image. This is used to reduce the amount of single pixels
            # that happen to fall within the hue range, overall this is a noise reduction
            blur = cv2.GaussianBlur(img, (15, 15), 0)

            # Convert the blurred image into Hue Saturation Value (HSV) format
            applehsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            bananahsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
            cucumberhsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

            # Mask the image for different hues (apple, banana, cucumber)
            appleMask = cv2.inRange(applehsv, appleHue[0], appleHue[1])
            bananaMask = cv2.inRange(bananahsv, bananaHue[0], bananaHue[1])
            cucumberMask = cv2.inRange(cucumberhsv, cucumberHue[0], cucumberHue[1])

            appleRes = cv2.bitwise_and(img, img, mask=appleMask)
            bananaRes = cv2.bitwise_and(img, img, mask=bananaMask)
            cucumberRes = cv2.bitwise_and(img, img, mask=cucumberMask)

            appleRes = cv2.resize(appleRes, (width, height))
            bananaRes = cv2.resize(bananaRes, (width, height))
            cucumberRes = cv2.resize(cucumberRes, (width, height))

            # Write the masked and resized image to temporary files.
            # This step could be omitted if we were able to convert cv2 images to PIL format
            cv2.imwrite("tempApple.jpeg", appleRes)
            cv2.imwrite("tempBanana.jpeg", bananaRes)
            cv2.imwrite("tempCuke.jpeg", cucumberRes)

            # Read the temp image files into the PIL format
            applePIL = Image.open("tempApple.jpeg")
            bananaPIL = Image.open("tempBanana.jpeg")
            cucumberPIL = Image.open("tempCuke.jpeg")

            # Convert the PIL image into a numpy array
            appleArray = numpy.asarray(applePIL.getdata())
            bananaArray = numpy.asarray(bananaPIL.getdata())
            cucumberArray = numpy.asarray(cucumberPIL.getdata())

            # ********************** APPLE matching
            appleStart = timer()
            appleResult = apple.activate(ravel(appleArray))
            appleEnd = timer()

            if appleResult[0] > 0.3:
                appleMatchRes = "Apple"
            else:
                appleMatchRes = "Unknown"

            print "Apple Network - Matched to: "+appleMatchRes+" in "+str(appleEnd-appleStart)+"sec with prediction scores: ", appleResult

            # ********************** BANANA matching
            bananaStart = timer()
            bananaResult = banana.activate(ravel(bananaArray))
            bananaEnd = timer()

            if bananaResult[0] > 0.3:
                bananaMatchRes = "Banana"
            else:
                bananaMatchRes = "Unknown"

            print "Banana Network - Matched to: "+bananaMatchRes+" in "+str(bananaEnd-bananaStart)+"sec with prediction scores: ", bananaResult

            # ********************** CUCUMBER matching
            cucumberStart = timer()
            cucumberResult = cucumber.activate(ravel(cucumberArray))
            cucumberEnd = timer()

            if cucumberResult[0] > 0.3:
                cucumberMatchRes = "Cucumber"
            else:
                cucumberMatchRes = "Unknown"

            print "Cucumber Network - Matched to: "+cucumberMatchRes+" in "+str(cucumberEnd-cucumberStart)+"sec with prediction scores: ", cucumberResult

            # ********************** Picking which result logic
            # Put the neural network results into a list
            results = [appleResult[0], bananaResult[0], cucumberResult[0]]
            resLabels = ['Apple', 'Banana', 'Cucumber']
            maxIndex = results.index(max(results))

            # Only call this the result if the greatest match percentage is above 30%, otherwise unknown
            if results[maxIndex] > 0.3:
                matchRes = resLabels[maxIndex]
            else:
                matchRes = 'Unknown'

            # Run other algorithm
            # matchRes = str(main(imPath))
            print "Other Algorithm: " + matchRes
        else:
            matchRes = "File Read Error"

        # Reply to the server with the match result
        self.request.sendall(matchRes)

def LoadAppleNeuralNetwork(networkXML):
    print "Loading Apple neural network: "+str(networkXML)
    start = timer()
    global apple
    apple = NetworkReader.readFrom(networkXML)
    end = timer()
    print "Time taken to load Apple neural network: " + str(end-start)

def LoadCucumberNeuralNetwork(networkXML):
    print "Loading Cucumber neural network: "+str(networkXML)
    start = timer()
    global cucumber
    cucumber = NetworkReader.readFrom(networkXML)
    end = timer()
    print "Time taken to load Cucumber neural network: " + str(end-start)

def LoadBananaNeuralNetwork(networkXML):
    print "Loading Banana neural network: "+str(networkXML)
    start = timer()
    global banana
    banana = NetworkReader.readFrom(networkXML)
    end = timer()
    print "Time taken to load Banana neural network: " + str(end-start)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Load the neural networks
    # thread.start_new_thread(LoadAppleNeuralNetwork,('VegeTable_PyBrain_Neural_Network_Apple.xml',))
    # thread.start_new_thread(LoadCucumberNeuralNetwork,('VegeTable_PyBrain_Neural_Network_Cucumber.xml',))
    # thread.start_new_thread(LoadBananaNeuralNetwork,('VegeTable_PyBrain_Neural_Network_Banana.xml',))

    print "Loading Banana neural network: "+str(bananaXML)
    start = timer()
    global banana
    banana = NetworkReader.readFrom(bananaXML)
    end = timer()
    print "Time taken to load Banana neural network: " + str(end-start)

    print "Loading Apple neural network: "+str(appleXML)
    start = timer()
    global apple
    apple = NetworkReader.readFrom(appleXML)
    end = timer()
    print "Time taken to load Apple neural network: " + str(end-start)

    print "Loading Cucumber neural network: "+str(cucumberXML)
    start = timer()
    global cucumber
    cucumber = NetworkReader.readFrom(cucumberXML)
    end = timer()
    print "Time taken to load Cucumber neural network: " + str(end-start)

    # Activate the server; this will keep running until interrupted with Ctrl-C
    print "Server waiting..."
    server.serve_forever()