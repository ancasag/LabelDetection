import json
import shutil
import os
from lxml import etree
import numpy as np
import glob
from imutils import paths
from sklearn.model_selection import train_test_split
import csv
import urllib.request
from tqdm import tqdm

class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)
def notebookRetinaNet (path, tecnhiques, conf, option):
    #primero realizamos una copia del fichero en la carpeta de las imagenes
    #shutil.copy('notebooks/RetinaNetExampleDD.ipynb', path+'/RetinaNet.ipynb')
    url = "https://www.dropbox.com/s/o3utmrkt93vx2m6/RetinaNetExampleDD.ipynb?dl=1"
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename='RetinaNetExampleDD.ipynb', reporthook=t.update_to)

    os.rename('RetinaNetExampleDD.ipynb', path + '/RetinaNet.ipynb', )
    notebook = path+'/RetinaNet.ipynb'
    with open(notebook) as json_file:
        data = json.load(json_file)
        data['metadata']['colab']['name']='RetinaNet.ipynb'
        clases = []
        lstFiles = []
        for root, dirs, files in os.walk(path):
            for fichero in files:
                (nombreFichero, extension) = os.path.splitext(fichero)
                if (extension == ".xml"):
                    lstFiles.append(nombreFichero + extension)

        lstFiles.sort()
        for fichero in lstFiles:
            # variables que vamos a necesitar
            doc = etree.parse(path + '/' + fichero)
            filename = doc.getroot()  # buscamos la raiz de nuestro xml
            # Listamos todos los objetos que encontremos en nuestro xml
            objetos = filename.findall("object")
            for objeto in objetos:
                name = objeto.find("name").text
                clases.append(name)

        clasesSinRep = np.unique(clases)

        numImg = '!python keras-retinanet/keras_retinanet/bin/train.py --batch-size 2 --steps '+ str(len(glob.glob(path + '/*.jpg'))//2) + ' --epochs 20 --weights snapshots/resnet50_csv_20.h5 --snapshot-path snapshotsDD csv dataset/retinanet_train.csv dataset/retinanet_classes.csv'

        numImgAno = '!python keras-retinanet/keras_retinanet/bin/train.py --batch-size 2 --steps '+ str(len(glob.glob(path + '/*.xml'))//2) +' --epochs 20 --weights resnet50_coco_best_v2.1.0.h5 --snapshot-path snapshots csv dataset/retinanet_train.csv dataset/retinanet_classes.csv'

        data['cells'][13]['source'][0] = numImgAno
        data['cells'][38]['source'][0] = numImg

        # modificamos las tecnicas
        tec = 'myTechniques = ['
        for p in tecnhiques:
            tec = tec + '\'' + str(p) + '\','
        tec1 = tec[:len(tec) - 1]
        tec1 = tec1 + ']\n'
        data['cells'][28]['source'][0] = tec1
        opt = 'option = \'' + option + '\'\n'
        data['cells'][29]['source'][0] = opt
        data['cells'][30]['source'][0] = 'tta(retinaResnet50,myTechniques,pathImg,option,' + str(conf) + ')'

    with open(notebook, 'w') as json_file:
        json.dump(data, json_file, indent=4)

    # Invocamos a la funcion con dichos parametros y mostramos el resultado por pantalla
    images = list(paths.list_files(path, validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".xml")))
    os.mkdir(path + '/dataset')  # carpeta
    os.mkdir(path + '/dataset/unlabelled')  # donde tenemos las imágenes sin anotar
    os.mkdir(path + '/dataset/annotations')
    os.mkdir(path + '/dataset/images')
    f = open(path + '/dataset/retinanet_classes.csv', 'w')
    data = []
    i = 0
    f = open(os.path.join(path, 'dataset',"retinanet_classes.csv"), 'w')
    for l in clasesSinRep:
        f.write(l+','+str(i)+'\n')
        i = i +1

    for i in images:
        shutil.copy(i, path + '/dataset/')

    os.mkdir(path + '/dataset/Anotadas')
    fichsXml = glob.glob(path + "/dataset/*.xml")
    for f in fichsXml:  ## copiamos las imagenes que tienen xml y los xml dentro de VOCdataset
        shutil.move(f, path + '/dataset/Anotadas/')
        shutil.move(path + '/dataset/' + os.path.split(f)[1].split('.')[0] + '.jpg', path + '/dataset/Anotadas/')
    datasetSplit(path + '/dataset/Anotadas/', path + '/dataset/Anotadas/', path + '/dataset/Anotadas/', 0.75)
    generaFicheroTrain(path + '/dataset/Anotadas/')
    generaFicheroTest(path + '/dataset/Anotadas/')
    # movemos los archivos xml a la carpeta Annotations
    fichsXmlAnoTrain = glob.glob(path + "/dataset/Anotadas/train/*.xml")
    fichsImgAnoTrain = glob.glob(path + "/dataset/Anotadas/*.xml")
    for j in fichsXmlAnoTrain:
        shutil.move(j, path + '/dataset/annotations/')
    for i in fichsImgAnoTrain:
        shutil.move(i, path + '/dataset/annotations/')
    fichsXmlAnoTest = glob.glob(path + "/dataset/Anotadas/train/*.jpg")
    fichsImgAnoTest = glob.glob(path + "/dataset/Anotadas/*.jpg")
    for j in fichsXmlAnoTest:
        shutil.move(j, path + '/dataset/images/')
    for i in fichsImgAnoTest:
        shutil.move(i, path + '/dataset/images/')

    shutil.move(path + '/dataset/Anotadas/train.txt', path + '/dataset/train.txt')
    shutil.move(path + '/dataset/Anotadas/test.txt', path + '/dataset/test.txt')
    shutil.rmtree(path + '/dataset/Anotadas')
    imagesSinAno = glob.glob(path + '/dataset/*.jpg')
    for i in imagesSinAno:
        shutil.move(i, path + '/dataset/unlabelled/')

    shutil.make_archive(path + "/dataset", "zip", path,"dataset")
    shutil.rmtree(path + "/dataset")

def datasetSplit( Nproyecto, darknetPath, pathImages, porcentaje):
    listaFicheros = list(paths.list_files(pathImages,validExts=(".jpg")))
    train_list,test_list, _ ,_ = train_test_split(listaFicheros, listaFicheros, train_size=porcentaje)
    #creamos la estructura de carpetas, la primera contendra las imagenes del entrenamiento
    os.makedirs(os.path.join(darknetPath , Nproyecto , 'train', 'JPEGImages'))
    #esta carpeta contendra las anotaciones de las imagenes de entrenamiento
    os.makedirs(os.path.join(darknetPath , Nproyecto , 'train', 'labels'))
    #y esta ultima carpeta va a contener tanto las imagenes como los ficheros de anotaciones del test
    os.makedirs(os.path.join(darknetPath , Nproyecto , 'test', 'JPEGImages'))
    #para las imagenes de entrenamiento
    for file in train_list:
        #obtenemos el fichero .txt asociado
        ficherolabel = file[0:file.rfind('.')]+'.xml'
        #obetenemos el nombre de los ficheros
        name = os.path.basename(file).split('.')[0]
        #movemos las imagenes a la carpeta JpegImages
        shutil.copy(file, os.path.join(darknetPath , Nproyecto , 'train', 'JPEGImages',name+'.jpg'))
        #movemos las anotaciones a la carpeta
        shutil.copy(ficherolabel,os.path.join(darknetPath , Nproyecto , 'train', 'labels',name+'.xml'))
    #para las imagenes de entrenamiento
    for file in test_list:
        #obtenemos el fichero .txt asociado
        ficherolabel = file[0:file.rfind('.')]+'.xml'
        #obetenemos el nombre de los ficheros
        name = os.path.basename(file).split('.')[0]
        #movemos las imagenes a la carpeta JpegImages
        shutil.copy(file, os.path.join(darknetPath , Nproyecto , 'test', 'JPEGImages',name+'.jpg'))
        #movemos las anotaciones a la carpeta
        shutil.copy(ficherolabel, os.path.join(darknetPath , Nproyecto , 'test', 'JPEGImages',name+'.xml'))

def generaFicheroTrain(darknetPath):
    #creamos el fichero train.txt
    f = open (os.path.join(darknetPath,"train.txt"), 'w')
    #listamos todos los ficheros .jpg del conjunto de entrenamiento
    files = os.listdir(os.path.join(darknetPath, "train/JPEGImages/"))
    #recorremos la lista e imprimimos una imagen por linea
    for l in files:
        f.write(l.split('.')[0] +'\n')

def generaFicheroTest(darknetPath):
    #creamos el fichero test.txt
    f = open(os.path.join(darknetPath,"test.txt"), 'w')
    #listamos todos los ficheros .jpg del conjunto de test
    files = os.listdir(os.path.join(darknetPath, "test/JPEGImages/"))
    #images = list(paths.list_files(darknetPath, validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")))
    #recorremos la lista e imprimimos una imagen por linea
    for l in files:
        start, ext = os.path.splitext(l)
        if ext==('.jpg'):
            #si es una imagen la guardamos
            f.write(l.split('.')[0]+'\n')
