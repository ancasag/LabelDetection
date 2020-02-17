# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tipyModel.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    genera = False
    def setupUi(self, Ui_Dialog):
        Ui_Dialog.setObjectName("Dialog")
        Ui_Dialog.resize(531, 293)
        # Esto hay que añadirlo para luego poder cerrar el dialogo
        self.dialog = Ui_Dialog

        self.buttonBox = QtWidgets.QDialogButtonBox(Ui_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(150, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label = QtWidgets.QLabel(Ui_Dialog)
        self.label.setGeometry(QtCore.QRect(10, 20, 341, 17))
        self.label.setObjectName("label")
        self.radioButton = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton.setGeometry(QtCore.QRect(40, 50, 112, 23))
        self.radioButton.setChecked(True)
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_2.setGeometry(QtCore.QRect(40, 90, 112, 23))
        self.radioButton_2.setObjectName("radioButton_2")
        self.radioButton_3 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_3.setGeometry(QtCore.QRect(40, 130, 181, 23))
        self.radioButton_3.setObjectName("radioButton_3")
        self.radioButton_4 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_4.setGeometry(QtCore.QRect(230, 50, 121, 23))
        self.radioButton_4.setObjectName("radioButton_4")
        self.radioButton_5 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_5.setGeometry(QtCore.QRect(230, 90, 112, 23))
        self.radioButton_5.setObjectName("radioButton_5")
        self.radioButton_6 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_6.setGeometry(QtCore.QRect(230, 130, 112, 23))
        self.radioButton_6.setObjectName("radioButton_6")
        self.radioButton_7 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_7.setGeometry(QtCore.QRect(380, 50, 121, 23))
        self.radioButton_7.setObjectName("radioButton_7")
        self.radioButton_8 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_8.setGeometry(QtCore.QRect(380, 90, 112, 23))
        self.radioButton_8.setObjectName("radioButton_8")
        self.radioButton_9 = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_9.setGeometry(QtCore.QRect(380, 130, 112, 23))
        self.radioButton_9.setObjectName("radioButton_9")
        self.line = QtWidgets.QFrame(Ui_Dialog)
        self.line.setGeometry(QtCore.QRect(10, 170, 501, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_2 = QtWidgets.QLabel(Ui_Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 190, 341, 20))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(Ui_Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(380, 190, 113, 25))
        self.lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lineEdit.setCursorPosition(3)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName("lineEdit")
        #self.lineEdit.text('0.4')

        # Aquí se conecta el botón de Ok con la funcionalidad que quieres.
        # En concreto, el método de actualizar que se define luego.
        self.buttonBox.accepted.connect(self.actualizar)
        self.retranslateUi(Ui_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Ui_Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Choose the type of model you are going to use:"))
        self.radioButton.setText(_translate("Dialog", "YOLO"))
        self.radioButton_2.setText(_translate("Dialog", "MXnet - SSD"))
        self.radioButton_3.setText(_translate("Dialog", "MXnet - Faster R-CNN"))
        self.radioButton_4.setText(_translate("Dialog", "MXnet - YOLO"))
        self.radioButton_5.setText(_translate("Dialog", "Mask R-CNN"))
        self.radioButton_6.setText(_translate("Dialog", "RetinaNet"))
        self.radioButton_7.setText(_translate("Dialog", "Efficient - Det"))
        self.radioButton_8.setText(_translate("Dialog", "FSAF"))
        self.radioButton_9.setText(_translate("Dialog", "FCOS"))
        self.label_2.setText(_translate("Dialog", "Select the level of confidence (between 0 and 1) :"))
        self.lineEdit.setText(_translate("Dialog", "0.4"))

    def actualizar(self):
        self.genera = True
        #ahora miramos el resultado de los checkBox
        rb1 = self.radioButton.isChecked()
        rb2 = self.radioButton_2.isChecked()
        rb3 = self.radioButton_3.isChecked()
        rb4 = self.radioButton_4.isChecked()
        rb5 = self.radioButton_5.isChecked()
        rb6 = self.radioButton_6.isChecked()
        rb7 = self.radioButton_7.isChecked()
        rb8 = self.radioButton_8.isChecked()
        rb9 = self.radioButton_9.isChecked()
        le = self.lineEdit.text()


        self.rb_1 = rb1
        self.rb_2 = rb2
        self.rb_3 = rb3
        self.rb_4 = rb4
        self.rb_5 = rb5
        self.rb_6 = rb6
        self.rb_7 = rb7
        self.rb_8 = rb8
        self.rb_9 = rb9
        self.le_1 = le

        # Se cierra el dialogo
        self.dialog.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

