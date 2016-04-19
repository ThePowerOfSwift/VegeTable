import SocketServer
from pybrain.tools.xml.networkreader import NetworkReader
from PIL import Image
import numpy
import cv2
import numpy as np
from numpy import ravel
from timeit import default_timer as timer
import os
import time

# Initialize some variables
supportedFruits = ['Apple', 'Unknown']
width = 100
height = 100

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        imPath = str(self.request.recv(1024).strip())
        print("Matching File: {}".format(imPath))

        # time.sleep(5)

        # Perform the image matching, start by loading the image file
        if os.path.exists(imPath):
            img = cv2.imread(imPath)

            blur = cv2.GaussianBlur(img, (15, 15), 0)

            hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

            lower_hue = np.array([0, 75, 75])
            upper_hue = np.array([25, 255, 255])

            mask = cv2.inRange(hsv, lower_hue, upper_hue)

            res = cv2.bitwise_and(img, img, mask= mask)

            res = cv2.resize(res, (width, height))

            cv2.imwrite("temp.jpeg", res)

            imgPIL = Image.open("temp.jpeg")
            imgArray = numpy.asarray(imgPIL.getdata())

            start = timer()
            result = fnn.activate(ravel(imgArray))
            end = timer()

            if result[0] > 0.3:
                matchRes = "Apple"
            else:
                matchRes = "Unknown"
        else:
            matchRes = "File Read Error"

        # print imFile + " Matched to: "+matchRes+" in "+str(end-start)+"sec with prediction scores: ", result
        print matchRes

        # just send back the same data, but upper-cased
        self.request.sendall(matchRes)

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Load the neural network
    print "Loading neural network..."
    start = timer()
    fnn = NetworkReader.readFrom('VegeTable_PyBrain_Neural_Network.xml')
    end = timer()
    print "Time taken to load neural network: " + str(end-start)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    print "Server waiting..."
    server.serve_forever()