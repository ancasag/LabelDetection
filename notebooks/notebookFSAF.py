import json
import shutil
import os
from lxml import etree
import numpy as np
import glob
from imutils import paths
from sklearn.model_selection import train_test_split
import urllib.request
from tqdm import tqdm


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def notebookFSAF (path, tecnhiques, conf, option):
    #primero realizamos una copia del fichero en la carpeta de las imagenes
    #shutil.copy('notebooks/FSAFExampleDD.ipynb', path+'/FSAF.ipynb')
    url = "https://www.dropbox.com/s/anhncb4mlcdkugb/FSAFExampleDD.ipynb?dl=0"
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename='FSAFExampleDD.ipynb', reporthook=t.update_to)

    os.rename('FSAFExampleDD.ipynb', path + '/FSAF.ipynb', )
    notebook = path+'/FSAF.ipynb'
    with open(notebook) as json_file:
        data = json.load(json_file)
        data['metadata']['colab']['name']='FSAF.ipynb'
        #lista = data['cells'][12]['source'][1]
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
            dicc = {}
            doc = etree.parse(path + '/' + fichero)
            filename = doc.getroot()  # buscamos la raiz de nuestro xml
            nomImagen = filename.find("filename")
            # Listamos todos los objetos que encontremos en nuestro xml
            objetos = filename.findall("object")
            for objeto in objetos:
                name = objeto.find("name").text
                clases.append(name)


        clasesSinRep = np.unique(clases)

        listaCla = 'classes = ['
        for p in clasesSinRep:
            listaCla = listaCla+'\''+str(p)+'\','
        listaCla1 = listaCla[:len(listaCla) - 1]
        listaCla1 = listaCla1 + ']\n'

        numImgAno = '!python3 train.py --backbone resnet50 --gpu 0 --batch-size 4 --epochs 25 --steps ' + str(
            len(glob.glob(path + '/*.xml')) // 4) + ' pascalCustom datasets/VOCdataset'

        numImg = '!python3 train.py --backbone resnet50 --gpu 0 --batch-size 4 --epochs 25 --steps ' + str(
            len(glob.glob(path + '/*.jpg')) // 4) + ' pascalCustom datasets/VOCdataset'


        data['cells'][10]['source'][0] = numImgAno
        data['cells'][36]['source'][0] = numImg
        # modificamos las tecnicas
        tec = 'myTechniques = ['
        for p in tecnhiques:
            tec = tec + '\'' + str(p) + '\','
        tec1 = tec[:len(tec) - 1]
        tec1 = tec1 + ']\n'
        data['cells'][25]['source'][0] = tec1
        opt = 'option = \'' + option + '\'\n'
        data['cells'][26]['source'][0] = opt
        data['cells'][27]['source'][0] = 'tta(fsaf,myTechniques,pathImg,option,' + str(conf) + ')'
    with open(notebook,'w') as json_file:
        json.dump(data,json_file, indent=4)
    # Invocamos a la funcion con dichos parametros y mostramos el resultado por pantalla
    images = list(paths.list_files(path, validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif",".xml")))
    os.mkdir(path + '/datasets')  # carpeta
    os.mkdir(path + '/datasets/unlabelled')#donde tenemos las imágenes sin anotar
    os.mkdir(path + '/datasets/VOCdataset')
    f = open(path + '/datasets/VOCdataset/classes.names', 'w')
    for p in clasesSinRep:
        f.write(p+'\n')
    f.close()
    f1 = open(path + '/datasets/VOCdataset/classes.csv', 'w')
    i = 0
    for l in clasesSinRep:
        f1.write(l + ',' + str(i) + '\n')
        i = i + 1
    f1.close()
    os.mkdir(path + '/datasets/VOCdataset/Annotations')
    os.mkdir(path + '/datasets/VOCdataset/ImageSets')#donde tenemos los archivos train.txt y test.txt
    os.mkdir(path + '/datasets/VOCdataset/ImageSets/Main')#donde tenemos los archivos train.txt y test.txt
    os.mkdir(path + '/datasets/VOCdataset/JPEGImages')

    for i in images:
        shutil.copy(i, path + '/datasets/')

    fichsXml = glob.glob(path + "/datasets/*.xml")
    for f in fichsXml:  ## copiamos las imagenes que tienen xml y los xml dentro de VOCdataset
        shutil.move(f, path + '/datasets/VOCdataset/')
        #print(os.path.split(f)[1].split('.')[0] + '.jpg')
        shutil.move(path + '/datasets/' + os.path.split(f)[1].split('.')[0] + '.jpg', path + '/datasets/VOCdataset/')
    datasetSplit(path + '/datasets/VOCdataset/', path + '/datasets/VOCdataset/', path + '/datasets/VOCdataset/', 0.75)
    #movemos los archivos xml a la carpeta Annotations
    fichsXmlAno = glob.glob(path + "/datasets/VOCdataset/*.xml")
    fichsImgAno = glob.glob(path + "/datasets/VOCdataset/*.jpg")
    for j in fichsXmlAno:
        shutil.move(j, path+'/datasets/VOCdataset/Annotations/')
    for i in fichsImgAno:
        shutil.move(i, path+'/datasets/VOCdataset/JPEGImages/')
    generaFicheroTrain(path+'/datasets/VOCdataset/')
    generaFicheroTest(path + '/datasets/VOCdataset/')
    shutil.move(path+'/datasets/VOCdataset/train.txt', path+'/datasets/VOCdataset/ImageSets/Main/train.txt')
    shutil.move(path+'/datasets/VOCdataset/test.txt', path+'/datasets/VOCdataset/ImageSets/Main/test.txt')
    shutil.rmtree(path+'/datasets/VOCdataset/train')
    shutil.rmtree(path+'/datasets/VOCdataset/test')

    imagesSinAno = glob.glob(path+'/datasets/*.jpg')
    #imagesSinAno = list(paths.list_files(path+'/datasets/*.*', validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif")))
    for i in imagesSinAno:
        shutil.move(i, path + '/datasets/unlabelled/')

    shutil.make_archive(path + "/datasets", "zip", path,"datasets")
    shutil.rmtree(path + "/datasets")

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

