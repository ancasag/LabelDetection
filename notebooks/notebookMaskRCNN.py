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
def notebookMaskRCNN (path, tecnhiques, conf, option):
    #primero realizamos una copia del fichero en la carpeta de las imagenes
    #shutil.copy('notebooks/MaskRCNNExampleDD.ipynb', path+'/MaskRCNN.ipynb')
    url = "https://www.dropbox.com/s/ikvftirzgfpw1vl/MaskRCNNExampleDD.ipynb?dl=1"
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename='MaskRCNNExampleDD.ipynb', reporthook=t.update_to)

    os.rename('MaskRCNNExampleDD.ipynb', path + '/MaskRCNN.ipynb', )
    notebook = path+'/MaskRCNN.ipynb'
    with open(notebook) as json_file:
        data = json.load(json_file)
        data['metadata']['colab']['name']='MaskRCNN.ipynb'
        clases = []
        final = []
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

        listaCla = 'listClasses = ['
        for p in clasesSinRep:
            listaCla = listaCla+'\''+str(p)+'\','
        listaCla1 = listaCla[:len(listaCla) - 1]
        listaCla1 = listaCla1 + ']\n'

        # Invocamos a la funcion con dichos parametros y mostramos el resultado por pantalla
        images = list(paths.list_files(path, validExts=(".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".xml")))
        os.mkdir(path + '/dataset')  # carpeta
        os.mkdir(path + '/dataset/unlabelled')  # donde tenemos las imágenes sin anotar
        os.mkdir(path + '/dataset/test')
        os.mkdir(path + '/dataset/train')
        f = open(path + '/dataset/classes.names', 'w')
        for p in clasesSinRep:
            f.write(p + '\n')
        f.close()
        os.mkdir(path + '/dataset/test/annots')
        os.mkdir(path + '/dataset/test/images')  # donde tenemos los archivos train.txt y test.txt
        os.mkdir(path + '/dataset/train/annots')  # donde tenemos los archivos train.txt y test.txt
        os.mkdir(path + '/dataset/train/images')

        for i in images:
            shutil.copy(i, path + '/dataset/')

        fichsXml = glob.glob(path + "/dataset/*.xml")
        os.mkdir(path + '/dataset/Anotadas/')
        for f in fichsXml:  ## copiamos las imagenes que tienen xml y los xml dentro de VOCdataset
            shutil.move(f, path + '/dataset/Anotadas/')
            shutil.move(path + '/dataset/' + os.path.split(f)[1].split('.')[0] + '.jpg', path + '/dataset/Anotadas/')
        datasetSplit(path + '/dataset/Anotadas/', path + '/dataset/Anotadas/', path + '/dataset/Anotadas/', 0.75)
        # movemos los archivos train a la carpeta train
        fichsXmlAnoTrain = glob.glob(path + "/dataset/Anotadas/train/labels/*")
        fichsImgAnoTrain = glob.glob(path + "/dataset/Anotadas/train/JPEGImages/*")
        for j in fichsXmlAnoTrain:
            shutil.move(j, path + '/dataset/train/annots/')
        for i in fichsImgAnoTrain:
            shutil.move(i, path + '/dataset/train/images/')
        # movemos los archivos train a la carpeta train
        fichsXmlAnoTest = glob.glob(path + "/dataset/Anotadas/test/JPEGImages/*.xml")
        fichsImgAnoTest = glob.glob(path + "/dataset/Anotadas/test/JPEGImages/*.jpg")
        for j in fichsXmlAnoTest:
            shutil.move(j, path + '/dataset/test/annots/')
        for i in fichsImgAnoTest:
            shutil.move(i, path + '/dataset/test/images/')

        shutil.rmtree(path + '/dataset/Anotadas')

        imagesSinAno = glob.glob(path + '/dataset/*.jpg')
        for i in imagesSinAno:
            shutil.move(i, path + '/dataset/unlabelled/')

        numImg = 'numImg = '+ str(len(glob.glob(path+'/*.jpg')))
        numImgAno = 'numImg = ' + str(len(glob.glob(path + '/*.xml')))
        numImgTest = 'numTest = '+str(len(glob.glob(path+'/dataset/test/images/*.jpg')))
        data['cells'][10]['source'][0] = listaCla1
        data['cells'][10]['source'][1] = numImgAno
        data['cells'][13]['source'][0] = numImgTest
        data['cells'][33]['source'][0] = listaCla1
        data['cells'][33]['source'][1] = numImg

        # modificamos las tecnicas
        tec = 'myTechniques = ['
        for p in tecnhiques:
            tec = tec+'\''+str(p)+'\','
        tec1 = tec[:len(tec) - 1]
        tec1 = tec1 + ']\n'
        data['cells'][23]['source'][0] = tec1
        opt = 'option = \''+option+'\'\n'
        data['cells'][24]['source'][0] = opt
        data['cells'][26]['source'][0] = 'tta(maskRcnn,myTechniques,pathImg,option,'+str(conf)+')'
    with open(notebook,'w') as json_file:
        json.dump(data,json_file, indent=4)

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

