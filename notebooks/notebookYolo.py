import json
import shutil
import os
from lxml import etree
import numpy as np
import glob
from imutils import paths
from sklearn.model_selection import train_test_split
import notebooks.pascal2yolo_1class
import urllib.request
from tqdm import tqdm


import zipfile


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def notebookYOLO (path, tecnhiques, conf, option):
    #primero realizamos una copia del fichero en la carpeta de las imagenes
    url = "https://www.dropbox.com/s/eyni0jk8brg3mrt/YOLOExampleDD.ipynb?dl=1"
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
         urllib.request.urlretrieve(url, filename='YOLOExampleDD.ipynb', reporthook=t.update_to)

    os.rename('YOLOExampleDD.ipynb', path+'/YOLO.ipynb',)
    #shutil.copy('notebooks/YOLOExampleDD.ipynb', path+'/YOLO.ipynb')
    notebook = path+'/YOLO.ipynb'
    with open(notebook) as json_file:
        data = json.load(json_file)
        data['metadata']['colab']['name']='YOLO.ipynb'
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

        listaCla = 'listClasses = ['
        for p in clasesSinRep:
            listaCla = listaCla+'\''+str(p)+'\','
        listaCla1 = listaCla[:len(listaCla) - 1]
        listaCla1 = listaCla1 + ']\n'

        # Invocamos a la funcion con dichos parametros y mostramos el resultado por pantalla
        images = list(paths.list_files(path, validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".xml")))
        os.mkdir(path + '/dataset')  # carpeta
        for i in images:
            shutil.copy(i, path + '/dataset/')
        fichsXml = glob.glob(path + "/dataset/*.xml")
        os.mkdir(path + '/dataset/Anotadas/')
        for f in fichsXml:  ## copiamos las imagenes que tienen xml y los xml dentro de VOCdataset
            shutil.move(f, path + '/dataset/Anotadas/')
            shutil.move(path + '/dataset/' + os.path.split(f)[1].split('.')[0] + '.jpg', path + '/dataset/Anotadas/')
        notebooks.pascal2yolo_1class.principal(path+'/dataset/Anotadas/')  # convertimos de xml a txt ya que yolo solo trabaja con txt
        fichsXml2 = glob.glob(path + "/dataset/Anotadas/*.xml")
        for x in fichsXml2:
            os.remove(x)
        os.remove(path+'/dataset/Anotadas/images.txt')
        datasetSplit(path + '/dataset/Anotadas/', path + '/dataset/Anotadas/', path + '/dataset/Anotadas/', 0.75)
        shutil.move(path + '/dataset/Anotadas/train',path + '/dataset/')
        shutil.move(path + '/dataset/Anotadas/test', path + '/dataset/')
        shutil.rmtree(path+'/dataset/Anotadas')
        os.mkdir(path + '/dataset/unlabelled')  # donde tenemos las imágenes sin anotar
        imagesSinAno = glob.glob(path + '/dataset/*.jpg')
        for i in imagesSinAno:
            shutil.move(i, path + '/dataset/unlabelled/')

        os.mkdir(path+'/dataset/test/labels')
        txtsTest = glob.glob(path + "/dataset/test/JPEGImages/*.txt")
        for i in txtsTest:
            shutil.move(i, path + '/dataset/test/labels')
        generaFicheroTrain(path+'/dataset/')
        generaFicheroTest(path+'/dataset/')
        generaFicherosYoloTest(path, len(clasesSinRep))
        generaFicherosYoloTrain(path, len(clasesSinRep))
        f = open(path + '/dataset/classes.names', 'w')
        for p in clasesSinRep:
            f.write(p + '\n')
        f.close()
        generaFicheroData(len(clasesSinRep), path+'/dataset')
        #modificamos las tecnicas
        tec = 'myTechniques = ['
        for p in tecnhiques:
            tec = tec+'\''+str(p)+'\','
        tec1 = tec[:len(tec) - 1]
        tec1 = tec1 + ']\n'
        data['cells'][22]['source'][0] = tec1
        opt = 'option = \''+option+'\'\n'
        data['cells'][23]['source'][0] = opt
        data['cells'][24]['source'][0] = 'tta(yolo,myTechniques,pathImg,option,'+str(conf)+')'
    with open(notebook,'w') as json_file:
        json.dump(data,json_file, indent=4)

    shutil.make_archive(path + "/dataset", "zip", path,"dataset")
    shutil.rmtree(path+"/dataset")


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
        ficherolabel = file[0:file.rfind('.')]+'.txt'
        #obetenemos el nombre de los ficheros
        name = os.path.basename(file).split('.')[0]
        #movemos las imagenes a la carpeta JpegImages
        shutil.copy(file, os.path.join(darknetPath , Nproyecto , 'train', 'JPEGImages',name+'.jpg'))
        #movemos las anotaciones a la carpeta
        shutil.copy(ficherolabel,os.path.join(darknetPath , Nproyecto , 'train', 'labels',name+'.txt'))
    #para las imagenes de entrenamiento
    for file in test_list:
        #obtenemos el fichero .txt asociado
        ficherolabel = file[0:file.rfind('.')]+'.txt'
        #obetenemos el nombre de los ficheros
        name = os.path.basename(file).split('.')[0]
        #movemos las imagenes a la carpeta JpegImages
        shutil.copy(file, os.path.join(darknetPath , Nproyecto , 'test', 'JPEGImages',name+'.jpg'))
        #movemos las anotaciones a la carpeta
        shutil.copy(ficherolabel, os.path.join(darknetPath , Nproyecto , 'test', 'JPEGImages',name+'.txt'))
def generaFicheroTrain(darknetPath):
    #creamos el fichero train.txt
    f = open (os.path.join(darknetPath,"train.txt"), 'w')
    #listamos todos los ficheros .jpg del conjunto de entrenamiento
    files = os.listdir(os.path.join(darknetPath, "train/JPEGImages/"))
    #recorremos la lista e imprimimos una imagen por linea
    for l in files:
        f.write('/content/darknet-colab/dataset/train/JPEGImages/'+l.split('.')[0] +'.jpg'+'\n')

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
            f.write('/content/darknet-colab/dataset/test/JPEGImages/'+l.split('.')[0]+'.jpg'+'\n')


def generaFicheroData(NClases, Nproyecto):
    #creamos el fichero
    f = open (os.path.join(Nproyecto +"/classes.data"),'w')
    #empezamos poniendo el numero de clases
    f.write('classes= ' + str(NClases)+'\n')
    f.write('train  = /content/darknet-colab/dataset/train.txt' +'\n')
    f.write('valid  = /content/darknet-colab/dataset/test.txt' +'\n')
    f.write('names = /content/darknet-colab/dataset/classes.names' +'\n')
    f.write('backup = /content/darknet-colab/backup'+'\n')
    f.close()

#funcion que nos genera los ficheros de YOLO
def generaFicherosYoloTrain(pathProyecto, NClases):
	#creamos el fichero yolo.cfg con la configuracion correspondiente a YOLO
	f = open (pathProyecto+"/dataset/train.cfg",'w')
	#Texto del fichero
	mensaje = """[net]
# Testing
# batch=1
# subdivisions=1
# Training
batch=64
subdivisions=16
width=416
height=416
channels=3
momentum=0.9
decay=0.0005
angle=0
saturation = 1.5
exposure = 1.5
hue=.1

learning_rate=0.001
burn_in=1000
max_batches = """+str(max(4000,2000*NClases))+"""
policy=steps
steps=400000,450000
scales=.1,.1

[convolutional]
batch_normalize=1
filters=32
size=3
stride=1
pad=1
activation=leaky

# Downsample

[convolutional]
batch_normalize=1
filters=64
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=32
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=64
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=128
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=64
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=64
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=256
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=512
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

######################

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters="""+ str((NClases + 5)*3)+"""
activation=linear


[yolo]
mask = 6,7,8
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes="""+str(NClases)+"""
num=9
jitter=.3
ignore_thresh = .7
truth_thresh = 1
random=1


[route]
layers = -4

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[upsample]
stride=2

[route]
layers = -1, 61



[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters="""+ str((NClases + 5)*3)+"""
activation=linear


[yolo]
mask = 3,4,5
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes="""+str(NClases)+"""
num=9
jitter=.3
ignore_thresh = .7
truth_thresh = 1
random=1



[route]
layers = -4

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[upsample]
stride=2

[route]
layers = -1, 36



[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters="""+ str((NClases + 5)*3)+"""
activation=linear


[yolo]
mask = 0,1,2
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes="""+str(NClases)+"""
num=9
jitter=.3
ignore_thresh = .7
truth_thresh = 1
random=1"""
	#escribimos el mensaje en el fichero
	f.write(mensaje)
	f.close()



def generaFicherosYoloTest(pathProyecto,NClases):
	#creamos el fichero yolo.cfg con la configuracion correspondiente a YOLO
	f = open (pathProyecto+"/dataset/test.cfg",'w')
	#Texto del fichero
	mensaje = """[net]
# Testing
batch=1
subdivisions=1
# Training
# batch=64
# subdivisions=16
width=416
height=416
channels=3
momentum=0.9
decay=0.0005
angle=0
saturation = 1.5
exposure = 1.5
hue=.1

learning_rate=0.001
burn_in=1000
max_batches = 500200
policy=steps
steps=400000,450000
scales=.1,.1

[convolutional]
batch_normalize=1
filters=32
size=3
stride=1
pad=1
activation=leaky

# Downsample

[convolutional]
batch_normalize=1
filters=64
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=32
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=64
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=128
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=64
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=64
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=256
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=512
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

# Downsample

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

######################

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters="""+ str((NClases + 5)*3)+"""
activation=linear


[yolo]
mask = 6,7,8
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes="""+str(NClases)+"""
num=9
jitter=.3
ignore_thresh = .7
truth_thresh = 1
random=1


[route]
layers = -4

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[upsample]
stride=2

[route]
layers = -1, 61



[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters="""+ str((NClases + 5)*3)+"""
activation=linear


[yolo]
mask = 3,4,5
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes="""+str(NClases)+"""
num=9
jitter=.3
ignore_thresh = .7
truth_thresh = 1
random=1



[route]
layers = -4

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[upsample]
stride=2

[route]
layers = -1, 36



[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters="""+ str((NClases + 5)*3)+"""
activation=linear


[yolo]
mask = 0,1,2
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes="""+str(NClases)+"""
num=9
jitter=.3
ignore_thresh = .7
truth_thresh = 1
random=1"""
	#escribimos el mensaje en el fichero
	f.write(mensaje)
	f.close()


