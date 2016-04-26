# VegeTable
Ever been in the grocery store unsure whether or not to buy one vegetable or another? Welcome to VegeTable, the fruit and vegetable identification tool. We promise to keep you informed and educated about what you and your family eat. 


# Overview
This application is divided into several major pieces:
1. iOS application - The iOS app is located in the gitHub at location: mrmarss/VegeTable/VegeTable.
When opening the xcode project be sure to open the file 'VegeTable.xcworkspace', NOT 'VegeTable.xcodeproj'
The user should be able to build this application if running OSX and xcode version 7.3.

2. nodeJS server - The nodeJS server manages communication to and from the iOS app, database, and python script server. For testing purposes this server has been executing locally on the development computer, but could be exported to a server easily. The nodeJS is located here: mrmarss/VegeTable/server/app.js

3. DynamoDB database - The database is hosted by amazon. Communication to the database is controlled by credentials, currently users must be given credentials in order to access nutritional information.

4. Python image recognition - The image recognition algorithms use OpenCV and Pybrain modules in python. Because of the time required to load the neural networks in Pybrain, a simple server was created. When the python server is started the neural networks are loaded. The server then waits for communication from the nodeJS server that will trigger image matching.


# Build Instructions / Dependencies
1. iOS application - The user should be able to open the workspace in xcode and all dependencies will be satisfied. In order to run the application on an iPhone a free developer account is required. The integrated OSX simulator application will not work with the required camera. 

2. nodeJS server - nodeJS version 4.2.6 was used for development. Node can be installed following instructions here:
https://nodejs.org/en/download/package-manager/
Once node is installed the server can be started by running: 'node app.js' from within the folder /VegeTable/server/

3. DynamoDB - This is hosted by amazon and does not need to be built.

4. Python image recognition - There are many dependencies that need to be installed. An output was generated using the 'pip freeze' command. See documentation here: https://pip.pypa.io/en/stable/reference/pip_freeze/
Python 2.7.11 was used for development. The required dependencies are stored in the file /VegeTable/requirements.txt.
It is recommended to install all of the requirements using 'pip install -r requirements.txt'.
There will likely be many system level dependencies that are not encompassed by this requirements file, such as gcc, libjpeg, libblas, and many more. It is not quick or easy to set up this python environment. The best method is to run the 'pip install -r requirements.txt' and when the build fails, install the required dependency and restart the build. 


