import cv2 as cv #s
import numpy as np
import xml.etree.ElementTree as ET
import xml.etree.ElementTree as ET
from xml.dom import minidom
from imutils import paths
import sys
import os
import urllib.request
from tqdm import tqdm

confThreshold = 0.25  #Confidence threshold
nmsThreshold = 0.45   #Non-maximum suppression threshold
#inpWidth = 416       #Width of network's input image
#inpHeight = 416      #Height of network's input image


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]





# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if confidence > confThreshold:
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    newBoxes=[]
    indices = cv.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for i in indices:
        i = i[0]
        #box = boxes[i]
        #left = box[0]
        #top = box[1]
        #width = box[2]
        #height = box[3]
        newBoxes.append(boxes[i])
        # drawPred(classIds[i], confidences[i], left, top, left + width, top + height)
    return newBoxes


#Load names of classes
dirPath =os.path.dirname(os.path.realpath(__file__))
classesFile = dirPath + "/fichs/vocEstomas.names";

classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')



class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


# Give the configuration and weight files for the model and
# load the network using them.
modelConfiguration = dirPath + "/fichs/yolov3Estomas.cfg";
modelWeights = dirPath + "/fichs/yolov3Stomata.weights";
url = "https://www.dropbox.com/s/fce0bsyl12enh4e/yolov3Stomata.weights?dl=1"
if  not os.path.exists(modelWeights):
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=modelWeights, reporthook=t.update_to)




def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def generateXML(filename,outputPath,w,h,d,boxes):
    top = ET.Element('annotation')
    childFolder = ET.SubElement(top, 'folder')
    childFolder.text = 'images'
    childFilename = ET.SubElement(top, 'filename')
    childFilename.text = filename[0:filename.rfind(".")]
    childPath = ET.SubElement(top, 'path')
    childPath.text = outputPath + "/" + filename
    childSource = ET.SubElement(top, 'source')
    childDatabase = ET.SubElement(childSource, 'database')
    childDatabase.text = 'Unknown'
    childSize = ET.SubElement(top, 'size')
    childWidth = ET.SubElement(childSize, 'width')
    childWidth.text = str(w)
    childHeight = ET.SubElement(childSize, 'height')
    childHeight.text = str(h)
    childDepth = ET.SubElement(childSize, 'depth')
    childDepth.text = str(d)
    childSegmented = ET.SubElement(top, 'segmented')
    childSegmented.text = str(0)
    for box in boxes:
        category = 'stoma'
        (x,y,wb,hb) = box
        childObject = ET.SubElement(top, 'object')
        childName = ET.SubElement(childObject, 'name')
        childName.text = category
        childPose = ET.SubElement(childObject, 'pose')
        childPose.text = 'Unspecified'
        childTruncated = ET.SubElement(childObject, 'truncated')
        childTruncated.text = '0'
        childDifficult = ET.SubElement(childObject, 'difficult')
        childDifficult.text = '0'
        childBndBox = ET.SubElement(childObject, 'bndbox')
        childXmin = ET.SubElement(childBndBox, 'xmin')
        childXmin.text = str(x)
        childYmin = ET.SubElement(childBndBox, 'ymin')
        childYmin.text = str(y)
        childXmax = ET.SubElement(childBndBox, 'xmax')
        childXmax.text = str(x+wb)
        childYmax = ET.SubElement(childBndBox, 'ymax')
        childYmax.text = str(y+hb)
    return prettify(top)


def generateXMLFromImage(imagePath):
    net = cv.dnn.readNetFromDarknet(modelConfiguration, modelWeights)
    net.setPreferableBackend(cv.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv.dnn.DNN_TARGET_CPU)
    im = cv.VideoCapture(imagePath)
    hasFrame, frame = im.read()
    wI, hI, d = frame.shape
    tam = min(wI,hI)
    if tam>=0 and tam<=624:
        inpWidth = 416
        inpHeight = 416
    elif tam>624 and tam<=1040:
        inpWidth = 832
        inpHeight = 832
    else:
        inpWidth = 1248
        inpHeight = 1248
    blob = cv.dnn.blobFromImage(frame, 1 / 255, (inpWidth, inpHeight), [0, 0, 0], 1, crop=False)

    # Sets the input to the network
    net.setInput(blob)

    # Runs the forward pass to get output of the output layers
    outs = net.forward(getOutputsNames(net))

    # Remove the bounding boxes with low confidence
    boxes = postprocess(frame, outs)

    #wI, hI, d = frame.shape
    file = open(imagePath[0:imagePath.rfind(".")] + ".xml", "w")
    file.write(generateXML(imagePath[0:imagePath.rfind(".")], "", wI, hI, d, boxes))
    file.close()



def mainImage(imagePath):
    # Leemos el parametro pasado por linea de comandos
    #arg1 = sys.argv[1]
    #arg2 = sys.argv[2]
    #arg3 = sys.argv[3]
    # Invocamos a la funcion con dichos parametros y mostramos el resultado por pantalla
    #print(prueba.genera_vector_aleatorio(arg1,arg2,arg3))
    generateXMLFromImage(imagePath)

def mainDataset(imagesPath):
    # Leemos el parametro pasado por linea de comandos
    #arg1 = sys.argv[1]
    # Invocamos a la funcion con dichos parametros y mostramos el resultado por pantalla
    images = list(paths.list_files(imagesPath, validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")))
    for image in images:
        generateXMLFromImage(image)
