from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import glob
import os.path
import sys
import xml.etree.ElementTree as ET
import cv2

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



dataDir = "/Users/jkonz/Documents/EC500/VegeTable/VegeTable/data/imagenet/Grape"
xmlFiles = GetListOfBoundingFiles(dataDir)

print("Found "+str(len(xmlFiles))+" XML files for processing.")

cv2.startWindowThread()

# Go through all of the XML files
for xmlFile in xmlFiles:
    # Get the base name, it is some random number beginning with an 'n'
    nxxxx, xml = os.path.splitext(os.path.basename(xmlFile))

    bboxes = ProcessXMLAnnotation(xmlFile)
    assert bboxes is not None, 'No bounding boxes found in ' + xmlFile

    # Display the image with the bounding box
    imFile = os.path.join(dataDir, nxxxx+".JPEG")
    if (os.path.isfile(imFile)):
        img = cv2.imread(imFile)
        for i,bbox in enumerate(bboxes):
            # Guard against improperly specified boxes.
            if (bbox.xmin_scaled >= bbox.xmax_scaled or bbox.ymin_scaled >= bbox.ymax_scaled):
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
            resize = cv2.resize(blur,(100,100))
            # cv2.imshow("edge",resize)
            # cv2.waitKey(1000)


            if not os.path.exists(dataDir+"/training/"):
                os.makedirs(dataDir+"/training/")

            cv2.imwrite(dataDir+"/training/"+os.path.splitext(os.path.basename(bbox.filename))[0]+"_"+str(i)+".JPEG",resize)


    else:
        print("File does not exist: "+imFile)


cv2.destroyAllWindows()