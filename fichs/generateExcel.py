import os
from lxml import etree
import xlsxwriter
import numpy as np


def generaExcel(carpeta):
    # creamos el excel y la fila de las cabeceras
    archivo = carpeta.split('/')
    wb = xlsxwriter.Workbook(carpeta+'/'+archivo[len(archivo)-1]+'.xlsx')
    ws = wb.add_worksheet('Datas')

    style0 = wb.add_format({'bold': True, 'font_color': 'white', 'fg_color': '0x10'})
    # style0.set_font_color('red')
    # -------------------------------------
    path = carpeta
    # Lista vacia para incluir los xmls
    lstFiles = []
    # Lista con todos los ficheros del directorio:
    lstDir = os.walk(path)  # os.walk()Lista directorios y ficheros
    # Crea una lista de los ficheros xml que existen en el directorio y los incluye a la lista.
    for root, dirs, files in lstDir:
        for fichero in files:
            (nombreFichero, extension) = os.path.splitext(fichero)
            if (extension == ".xml"):
                lstFiles.append(nombreFichero + extension)

    col = 0 # contador que me va a permitir ir quitando las columnas que me solicitan
    lstFiles.sort()
    # escribimos la cabecera
    ws.write(0, 0, 'Image name', style0)
    ws.set_column(0, 0, 25)
    clases = []
    final = []
    for fichero in lstFiles:
        # variables que vamos a necesitar
        dicc = {}
        doc = etree.parse(carpeta+'/' + fichero)
        filename = doc.getroot()  # buscamos la raiz de nuestro xml
        nomImagen = filename.find("filename")
        #ws.write(i, 0, nomImagen.text.split('/')[len(nomImagen.text.split('/'))-1])
        # Listamos todos los objetos que encontremos en nuestro xml
        objetos = filename.findall("object")
        for objeto in objetos:
            name = objeto.find("name").text
            clases.append(name)
            if name in dicc:
                dicc[name] += 1
            else:
                dicc[name] =1

        final.append([nomImagen.text.split('/')[len(nomImagen.text.split('/'))-1],dicc])

    clasesSinRep = np.unique(clases)

    j = 1

    for img in final:#recorremos el vector para sacar cada imagen
        i = 1
        ws.write(j,0,img[0])#escribimos el nombre de la imagen
        for clase in clasesSinRep:
            ws.write(0, i, clase)
            l = 0
            while l < len(img[1]):
                if clase in img[1]:
                    ws.write(j, i, img[1][clase])
                else:
                    ws.write(j, i, 0)
                l = l+1
            i = i + 1
        j= j + 1

    wb.close()

