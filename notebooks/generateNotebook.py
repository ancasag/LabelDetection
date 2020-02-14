import notebooks.notebookMaskRCNN
import notebooks.notebookYolo
import notebooks.notebookMxNetSSD
import notebooks.notebookEfficient
import notebooks.notebookRetinaNet
import notebooks.notebookFSAF
import notebooks.notebookFCOS
import sys
try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import *
from libs.ustr import ustr


def selectModel(self,rb_efi,rb_fsaf,rb_fcos,rb_mask,rb_mxnet,rb_reti, rb_yolo, path, tecnhiques, conf,option):

    if rb_efi == True:
        notebooks.notebookEfficient.notebookEfficient(path, tecnhiques, conf, option)
    elif rb_fsaf == True:
        notebooks.notebookFSAF.notebookFSAF(path, tecnhiques, conf, option)
    elif rb_fcos == True:
        notebooks.notebookFCOS.notebookFCOS(path, tecnhiques, conf, option)
    elif rb_mask == True:
        notebooks.notebookMaskRCNN.notebookMaskRCNN(path, tecnhiques, conf, option)
    elif rb_mxnet == True:
        notebooks.notebookMxNetSSD.notebookSSD(path, tecnhiques, conf, option)
    elif rb_reti == True:
        notebooks.notebookRetinaNet.notebookRetinaNet(path, tecnhiques, conf, option)
    elif rb_yolo == True:
        notebooks.notebookYolo.notebookYOLO(path, tecnhiques, conf, option)

