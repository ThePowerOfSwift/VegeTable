'''
This script is intended to be executed twice.

The first instance will establish which files are to be excluded from the training set.
This is an interactive execution requiring the user to go through the pictures with the left and right arrows.
If an image is to be excluded the space bar needs to be hit.

The second instance reads the exclusions file and processes all the images and stores them in the training
images folder.

'''
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os.path
import sys
import xml.etree.ElementTree as ET
import cv2
import csv

resizeX = 100
resizeY = 100

class BoundingBox(object):
  pass

def GetItem(name, root, index=0):
  count = 0
  for item in root.iter(name):
    if count == index:
      return item.text
    count += 1
  # Failed to find "index" occurrence of item.
  return -1


def GetInt(name, root, index=0):
  return int(GetItem(name, root, index))


def FindNumberBoundingBoxes(root):
  index = 0
  while True:
    if GetInt('xmin', root, index) == -1:
      break
    index += 1
  return index

def GetListOfBoundingFiles(directory):
    xmlFiles = glob.glob(directory + '/*/*.xml')

    return xmlFiles

def ProcessXMLAnnotation(xml_file):
  """Process a single XML file containing a bounding box."""
  # pylint: disable=broad-except
  try:
    tree = ET.parse(xml_file)
  except Exception:
    print('Failed to parse: ' + xml_file, file=sys.stderr)
    return None
  # pylint: enable=broad-except
  root = tree.getroot()

  num_boxes = FindNumberBoundingBoxes(root)
  boxes = []

  for index in xrange(num_boxes):
    box = BoundingBox()
    # Grab the 'index' annotation.
    box.xmin = GetInt('xmin', root, index)
    box.ymin = GetInt('ymin', root, index)
    box.xmax = GetInt('xmax', root, index)
    box.ymax = GetInt('ymax', root, index)

    box.width = GetInt('width', root)
    box.height = GetInt('height', root)
    box.filename = str(GetItem('filename', root)) + '.JPEG'
    box.label = GetItem('name', root)

    xmin = float(box.xmin) / float(box.width)
    xmax = float(box.xmax) / float(box.width)
    ymin = float(box.ymin) / float(box.height)
    ymax = float(box.ymax) / float(box.height)

    # Some images contain bounding box annotations that
    # extend outside of the supplied image. See, e.g.
    # n03127925/n03127925_147.xml
    # Additionally, for some bounding boxes, the min > max
    # or the box is entirely outside of the image.
    min_x = min(xmin, xmax)
    max_x = max(xmin, xmax)
    box.xmin_scaled = min(max(min_x, 0.0), 1.0)
    box.xmax_scaled = min(max(max_x, 0.0), 1.0)

    min_y = min(ymin, ymax)
    max_y = max(ymin, ymax)
    box.ymin_scaled = min(max(min_y, 0.0), 1.0)
    box.ymax_scaled = min(max(max_y, 0.0), 1.0)

    boxes.append(box)

  return boxes



dataDir = "/Users/jkonz/Documents/EC500/VegeTable/VegeTable/data/imagenet/source_images/Grape"
xmlFiles = GetListOfBoundingFiles(dataDir)

print("Found "+str(len(xmlFiles))+" XML files for processing.")

cv2.startWindowThread()

# Check to see if an excluded images file already exists
# This file stores all of the files that have been manually selected to be skipped due to image quality
excludeFiles = []
excludeFile = os.path.join(dataDir, "excludes.csv")
if os.path.isfile(excludeFile):
    useExistingExcludeFile = True
    # Load all the rows in the exclude file, which is all the file names to be excluded from this image processing
    with open(excludeFile, 'rb') as csvFile:
        fileData = csv.reader(csvFile)
        for row in fileData:
            excludeFiles.append(row[0])
else:
    useExistingExcludeFile = False

# Go through all of the XML files
i = 0
while (i >= 0) and (i < len(xmlFiles)):
    xmlFile = xmlFiles[i]

    # Get the base name, it is some random number beginning with an 'n'
    nxxxx, xml = os.path.splitext(os.path.basename(xmlFile))

    bboxes = ProcessXMLAnnotation(xmlFile)
    assert bboxes is not None, 'No bounding boxes found in ' + xmlFile

    # Display the image with the bounding box
    imFile = os.path.join(dataDir, nxxxx+".JPEG")
    if os.path.isfile(imFile):
        img = cv2.imread(imFile)
        for k,bbox in enumerate(bboxes):
            # Guard against improperly specified boxes.
            if (bbox.xmin_scaled >= bbox.xmax_scaled) or (bbox.ymin_scaled >= bbox.ymax_scaled):
                continue

            # show the bounding box
            # pt1 = (int(bbox.xmin), int(bbox.ymin))
            # pt2 = (int(bbox.xmax), int(bbox.ymax))
            # cv2.rectangle(img,pt1,pt2,(255,255,0),thickness=1,lineType=cv2.LINE_AA)
            # cv2.imshow("image",img)

            # crop the image to the size of the bounding box
            crop = img[bbox.ymin:bbox.ymax,bbox.xmin:bbox.xmax,:]
            # cv2.imshow("cropped", crop)
            # cv2.waitKey(1000)

            # perform a gaussian blur to remove sharp features
            blur = crop.copy()
            blur = cv2.GaussianBlur(blur, (9,9),0)
            # cv2.imshow("blurred",blur)
            # cv2.waitKey(1000)

            # perform a canny edge detection
            # canny = blur.copy()
            # canny = cv2.Canny(canny,40,80)
            # cv2.imshow("edge",canny)
            # cv2.waitKey(1000)

            # resize the image to be a standard size
            resize = cv2.resize(blur,(resizeX,resizeY))
            # cv2.imshow("edge",resize)
            # cv2.waitKey(1000)

            # Move up two directory levels and set the training directory
            base, fruitFolder = os.path.split(dataDir)
            base, srcFolder = os.path.split(base)
            trainFolder = os.path.join(base, "training_images",fruitFolder)

            if not os.path.exists(trainFolder):
                os.makedirs(trainFolder)

            trainFile = os.path.splitext(os.path.basename(bbox.filename))[0]+"_"+str(k)+".JPEG"
            trainPath = os.path.join(trainFolder,trainFile)

            exFile = os.path.split(imFile)

            if useExistingExcludeFile:
                if exFile[1] not in excludeFiles:
                    cv2.imwrite(trainPath,resize)

                i += 1
            else:
                cv2.imshow("Image "+str(i+1)+" of "+str(len(xmlFiles)), resize)
                cv2.moveWindow("Image "+str(i+1)+" of "+str(len(xmlFiles)),0,0)
                key = cv2.waitKey(0)

                if key == 32:
                    # SPACEBAR
                    # Skip this image, add it to the exclude files
                    i += 1
                    with open(excludeFile, 'a') as csvFile:
                        csvWriter = csv.writer(csvFile)
                        csvWriter.writerow([exFile[1]])
                        print("Skip file: "+exFile[1])

                if key == 63235:
                    # RIGHT ARROW
                    # Move to the next image, the user wants to keep this one
                    i += 1

                if key == 63234:
                    # LEFT ARROW
                    # Move back one image
                    i -= 1

                if key == 27:
                    # ESCAPE KEY
                    i = len(xmlFiles)

                cv2.destroyAllWindows()



    else:
        print("File does not exist: "+imFile)
        i += 1


