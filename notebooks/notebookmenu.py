# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'notebookmenu.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    genera = False
    def setupUi(self,Ui_Dialog):
        Ui_Dialog.setObjectName("Dialog")
        Ui_Dialog.resize(1011, 746)
        self.dialog = Ui_Dialog
        self.buttonBox = QtWidgets.QDialogButtonBox(Ui_Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(800, 710, 191, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons( QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.checkBox_avg = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_avg.setGeometry(QtCore.QRect(20, 220, 141, 23))
        self.checkBox_avg.setObjectName("checkBox_avg")
        self.label = QtWidgets.QLabel(Ui_Dialog)
        self.label.setGeometry(QtCore.QRect(20, 180, 331, 17))
        self.label.setObjectName("label")
        self.checkBox_biBlu = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_biBlu.setGeometry(QtCore.QRect(20, 270, 141, 23))
        self.checkBox_biBlu.setObjectName("checkBox_biBlu")
        self.checkBox_crop = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_crop.setGeometry(QtCore.QRect(20, 470, 141, 23))
        self.checkBox_crop.setObjectName("checkBox_crop")
        self.checkBox_blu = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_blu.setGeometry(QtCore.QRect(20, 320, 171, 23))
        self.checkBox_blu.setObjectName("checkBox_blu")
        self.checkBox_blur2 = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_blur2.setGeometry(QtCore.QRect(20, 420, 141, 23))
        self.checkBox_blur2.setObjectName("checkBox_blur2")
        self.checkBox_hsv = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_hsv.setGeometry(QtCore.QRect(20, 370, 171, 23))
        self.checkBox_hsv.setObjectName("checkBox_hsv")
        self.checkBox_his = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_his.setGeometry(QtCore.QRect(230, 270, 181, 23))
        self.checkBox_his.setObjectName("checkBox_his")
        self.checkBox_gam = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_gam.setGeometry(QtCore.QRect(230, 470, 151, 23))
        self.checkBox_gam.setObjectName("checkBox_gam")
        self.checkBox_ver = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_ver.setGeometry(QtCore.QRect(230, 320, 141, 23))
        self.checkBox_ver.setObjectName("checkBox_ver")
        self.checkBox_flip = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_flip.setGeometry(QtCore.QRect(230, 370, 141, 23))
        self.checkBox_flip.setObjectName("checkBox_flip")
        self.checkBox_hvflip = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_hvflip.setGeometry(QtCore.QRect(230, 420, 201, 23))
        self.checkBox_hvflip.setObjectName("checkBox_hvflip")
        self.checkBox_elas = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_elas.setGeometry(QtCore.QRect(230, 220, 181, 23))
        self.checkBox_elas.setObjectName("checkBox_elas")
        self.checkBox_inv = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_inv.setGeometry(QtCore.QRect(440, 270, 141, 23))
        self.checkBox_inv.setObjectName("checkBox_inv")
        self.checkBox_green = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_green.setGeometry(QtCore.QRect(440, 470, 161, 23))
        self.checkBox_green.setObjectName("checkBox_green")
        self.checkBox_med = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_med.setGeometry(QtCore.QRect(440, 320, 141, 23))
        self.checkBox_med.setObjectName("checkBox_med")
        self.checkBox_none = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_none.setGeometry(QtCore.QRect(440, 370, 141, 23))
        self.checkBox_none.setChecked(True)
        self.checkBox_none.setObjectName("checkBox_none")
        self.checkBox_blue = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_blue.setGeometry(QtCore.QRect(440, 420, 161, 23))
        self.checkBox_blue.setObjectName("checkBox_blue")
        self.checkBox_add = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_add.setGeometry(QtCore.QRect(440, 220, 181, 23))
        self.checkBox_add.setObjectName("checkBox_add")
        self.checkBox_sat = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_sat.setGeometry(QtCore.QRect(650, 270, 141, 23))
        self.checkBox_sat.setObjectName("checkBox_sat")
        self.checkBox_r90 = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_r90.setGeometry(QtCore.QRect(650, 470, 141, 23))
        self.checkBox_r90.setObjectName("checkBox_r90")
        self.checkBox_val = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_val.setGeometry(QtCore.QRect(650, 320, 141, 23))
        self.checkBox_val.setObjectName("checkBox_val")
        self.checkBox_resi = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_resi.setGeometry(QtCore.QRect(650, 370, 141, 23))
        self.checkBox_resi.setObjectName("checkBox_resi")
        self.checkBox_r10 = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_r10.setGeometry(QtCore.QRect(650, 420, 141, 23))
        self.checkBox_r10.setObjectName("checkBox_r10")
        self.checkBox_red = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_red.setGeometry(QtCore.QRect(650, 220, 141, 23))
        self.checkBox_red.setObjectName("checkBox_red")
        self.checkBox_drop = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_drop.setGeometry(QtCore.QRect(20, 520, 141, 23))
        self.checkBox_drop.setObjectName("checkBox_drop")
        self.checkBox_gau = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_gau.setGeometry(QtCore.QRect(230, 520, 141, 23))
        self.checkBox_gau.setObjectName("checkBox_gau")
        self.checkBox_hue = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_hue.setGeometry(QtCore.QRect(440, 520, 141, 23))
        self.checkBox_hue.setObjectName("checkBox_hue")
        self.checkBox_r180 = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_r180.setGeometry(QtCore.QRect(650, 520, 141, 23))
        self.checkBox_r180.setObjectName("checkBox_r180")
        self.checkBox_trans = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_trans.setGeometry(QtCore.QRect(860, 470, 141, 23))
        self.checkBox_trans.setObjectName("checkBox_trans")
        self.checkBox_r270 = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_r270.setGeometry(QtCore.QRect(860, 220, 141, 23))
        self.checkBox_r270.setObjectName("checkBox_r270")
        self.checkBox_shift = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_shift.setGeometry(QtCore.QRect(860, 370, 141, 23))
        self.checkBox_shift.setObjectName("checkBox_shift")
        self.checkBox_salt = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_salt.setGeometry(QtCore.QRect(860, 270, 141, 23))
        self.checkBox_salt.setObjectName("checkBox_salt")
        self.checkBox_shear = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_shear.setGeometry(QtCore.QRect(860, 420, 141, 23))
        self.checkBox_shear.setObjectName("checkBox_shear")
        self.checkBox_shar = QtWidgets.QCheckBox(Ui_Dialog)
        self.checkBox_shar.setGeometry(QtCore.QRect(860, 320, 141, 23))
        self.checkBox_shar.setObjectName("checkBox_shar")
        self.radioButton_yolo = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_yolo.setGeometry(QtCore.QRect(50, 60, 112, 23))
        self.radioButton_yolo.setChecked(True)
        self.radioButton_yolo.setObjectName("radioButton_yolo")
        self.radioButton_mask = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_mask.setGeometry(QtCore.QRect(330, 60, 112, 23))
        self.radioButton_mask.setObjectName("radioButton_mask")
        self.radioButton_mxnet = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_mxnet.setGeometry(QtCore.QRect(50, 110, 112, 23))
        self.radioButton_mxnet.setObjectName("radioButton_mxnet")
        self.radioButton_reti = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_reti.setGeometry(QtCore.QRect(330, 110, 112, 23))
        self.radioButton_reti.setObjectName("radioButton_reti")
        self.radioButton_efi = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_efi.setGeometry(QtCore.QRect(620, 60, 121, 23))
        self.radioButton_efi.setObjectName("radioButton_efi")
        self.radioButton_fcos = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_fcos.setGeometry(QtCore.QRect(860, 60, 112, 23))
        self.radioButton_fcos.setObjectName("radioButton_fcos")
        self.label_2 = QtWidgets.QLabel(Ui_Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 30, 341, 17))
        self.label_2.setObjectName("label_2")
        self.radioButton_fsaf = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_fsaf.setGeometry(QtCore.QRect(620, 110, 112, 23))
        self.radioButton_fsaf.setObjectName("radioButton_fsaf")
        self.line = QtWidgets.QFrame(Ui_Dialog)
        self.line.setGeometry(QtCore.QRect(10, 150, 991, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(Ui_Dialog)
        self.line_2.setGeometry(QtCore.QRect(10, 560, 981, 20))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.radioButton_con = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_con.setGeometry(QtCore.QRect(460, 620, 112, 23))
        self.radioButton_con.setObjectName("radioButton_con")
        self.line_3 = QtWidgets.QFrame(Ui_Dialog)
        self.line_3.setGeometry(QtCore.QRect(10, 650, 981, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_4 = QtWidgets.QLabel(Ui_Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 680, 211, 17))
        self.label_4.setObjectName("label_4")
        self.label_3 = QtWidgets.QLabel(Ui_Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 590, 211, 17))
        self.label_3.setObjectName("label_3")
        self.radioButton_aff = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_aff.setGeometry(QtCore.QRect(180, 620, 112, 23))
        self.radioButton_aff.setObjectName("radioButton_aff")
        self.lineEdit = QtWidgets.QLineEdit(Ui_Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(250, 680, 113, 25))
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.radioButton_una = QtWidgets.QRadioButton(Ui_Dialog)
        self.radioButton_una.setGeometry(QtCore.QRect(740, 620, 112, 23))
        self.radioButton_una.setObjectName("radioButton_una")
        self.btngroup1 = QtWidgets.QButtonGroup()
        self.btngroup2 = QtWidgets.QButtonGroup()

        self.btngroup1.addButton(self.radioButton_aff)
        self.btngroup1.addButton(self.radioButton_con)
        self.btngroup1.addButton(self.radioButton_una)

        self.btngroup2.addButton(self.radioButton_yolo)
        self.btngroup2.addButton(self.radioButton_mask)
        self.btngroup2.addButton(self.radioButton_reti)
        self.btngroup2.addButton(self.radioButton_mxnet)
        self.btngroup2.addButton(self.radioButton_efi)
        self.btngroup2.addButton(self.radioButton_fsaf)
        self.btngroup2.addButton(self.radioButton_fcos)
        self.radioButton_aff.setChecked(True)

        # Aquí se conecta el botón de Ok con la funcionalidad que quieres.
        # En concreto, el método de actualizar que se define luego.
        self.buttonBox.accepted.connect(self.actualizar)
        self.retranslateUi(Ui_Dialog)
        QtCore.QMetaObject.connectSlotsByName(Ui_Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.checkBox_avg.setText(_translate("Dialog", "Average blurring"))
        self.label.setText(_translate("Dialog", "Select the techniques for data distillation."))
        self.checkBox_biBlu.setText(_translate("Dialog", "Bilateral blurring"))
        self.checkBox_crop.setText(_translate("Dialog", "Crop"))
        self.checkBox_blu.setText(_translate("Dialog", "Change to lab colour"))
        self.checkBox_blur2.setText(_translate("Dialog", "Blurring"))
        self.checkBox_hsv.setText(_translate("Dialog", "Change to hsv colour"))
        self.checkBox_his.setText(_translate("Dialog", "Equalize histogram"))
        self.checkBox_gam.setText(_translate("Dialog", "Gamma correction"))
        self.checkBox_ver.setText(_translate("Dialog", "Vertical flip"))
        self.checkBox_flip.setText(_translate("Dialog", "Horizontal flip"))
        self.checkBox_hvflip.setText(_translate("Dialog", "Vertical and horizontal flip"))
        self.checkBox_elas.setText(_translate("Dialog", "Elastic deformation"))
        self.checkBox_inv.setText(_translate("Dialog", "Invert"))
        self.checkBox_green.setText(_translate("Dialog", "Raise green channel"))
        self.checkBox_med.setText(_translate("Dialog", "Median blurring"))
        self.checkBox_none.setText(_translate("Dialog", "None"))
        self.checkBox_blue.setText(_translate("Dialog", "Raise blue channel"))
        self.checkBox_add.setText(_translate("Dialog", "Add gaussian noise"))
        self.checkBox_sat.setText(_translate("Dialog", "Raise saturation"))
        self.checkBox_r90.setText(_translate("Dialog", " Rotate 90º"))
        self.checkBox_val.setText(_translate("Dialog", "Raise value"))
        self.checkBox_resi.setText(_translate("Dialog", "Resize"))
        self.checkBox_r10.setText(_translate("Dialog", "Rotate 10º"))
        self.checkBox_red.setText(_translate("Dialog", "Raise red"))
        self.checkBox_drop.setText(_translate("Dialog", "Dropout"))
        self.checkBox_gau.setText(_translate("Dialog", "Gaussian blurring"))
        self.checkBox_hue.setText(_translate("Dialog", "Raise hue"))
        self.checkBox_r180.setText(_translate("Dialog", "Rotate 180º"))
        self.checkBox_trans.setText(_translate("Dialog", "Translation"))
        self.checkBox_r270.setText(_translate("Dialog", "Rotate 270º"))
        self.checkBox_shift.setText(_translate("Dialog", "Shift channel"))
        self.checkBox_salt.setText(_translate("Dialog", "Salt and pepper"))
        self.checkBox_shear.setText(_translate("Dialog", "Shearing"))
        self.checkBox_shar.setText(_translate("Dialog", "Sharpen"))
        self.radioButton_yolo.setText(_translate("Dialog", "YOLO"))
        self.radioButton_mask.setText(_translate("Dialog", "Mask R-CNN"))
        self.radioButton_mxnet.setText(_translate("Dialog", "MXnet - SSD"))
        self.radioButton_reti.setText(_translate("Dialog", "RetinaNet"))
        self.radioButton_efi.setText(_translate("Dialog", "Efficient - Det"))
        self.radioButton_fcos.setText(_translate("Dialog", "FCOS"))
        self.label_2.setText(_translate("Dialog", "Choose the type of model you are going to create."))
        self.radioButton_fsaf.setText(_translate("Dialog", "FSAF"))
        self.radioButton_con.setText(_translate("Dialog", "Consensus"))
        self.label_4.setText(_translate("Dialog", "Select the level of confidence:"))
        self.label_3.setText(_translate("Dialog", "Select the ensemble method."))
        self.radioButton_aff.setText(_translate("Dialog", "Affirmative"))
        self.lineEdit.setText(_translate("Dialog", "0.4"))
        self.radioButton_una.setText(_translate("Dialog", "Unanimous"))

    def actualizar(self):
        self.genera = True
        #ahora miramos el resultado de los checkBox
        rbefi = self.radioButton_efi.isChecked()
        rbfsaf = self.radioButton_fsaf.isChecked()
        rbfcos = self.radioButton_fcos.isChecked()
        rbmask = self.radioButton_mask.isChecked()
        rbmxnet = self.radioButton_mxnet.isChecked()
        rbreti = self.radioButton_reti.isChecked()
        rbyolo = self.radioButton_yolo.isChecked()
        #-------------------
        rbaff = self.radioButton_aff.isChecked()
        rbcon = self.radioButton_con.isChecked()
        rbuna = self.radioButton_una.isChecked()
        #-------------------------
        le1 = self.lineEdit.text()
        # ahora miramos el resultado de los checkbox
        ch1 = self.checkBox_avg.isChecked()
        ch2 = self.checkBox_biBlu.isChecked()
        ch3 = self.checkBox_blu.isChecked()
        ch4 = self.checkBox_hsv.isChecked()
        ch5 = self.checkBox_blur2.isChecked()
        ch6 = self.checkBox_crop.isChecked()
        ch7 = self.checkBox_drop.isChecked()
        ch8 = self.checkBox_elas.isChecked()
        ch9 = self.checkBox_his.isChecked()
        ch10 = self.checkBox_ver.isChecked()
        ch11 = self.checkBox_flip.isChecked()
        ch12 = self.checkBox_hvflip.isChecked()
        ch13 = self.checkBox_gam.isChecked()
        ch14 = self.checkBox_gau.isChecked()
        ch15 = self.checkBox_add.isChecked()
        ch16 = self.checkBox_inv.isChecked()
        ch17 = self.checkBox_med.isChecked()
        ch18 = self.checkBox_none.isChecked()
        ch19 = self.checkBox_blue.isChecked()
        ch20 = self.checkBox_green.isChecked()
        ch21 = self.checkBox_hue.isChecked()
        ch22 = self.checkBox_red.isChecked()
        ch23 = self.checkBox_sat.isChecked()
        ch24 = self.checkBox_val.isChecked()
        ch25 = self.checkBox_resi.isChecked()
        ch26 = self.checkBox_r10.isChecked()
        ch27 = self.checkBox_r90.isChecked()
        ch28 = self.checkBox_r180.isChecked()
        ch29 = self.checkBox_r270.isChecked()
        ch30 = self.checkBox_salt.isChecked()
        ch31 = self.checkBox_shar.isChecked()
        ch33 = self.checkBox_shift.isChecked()
        ch34 = self.checkBox_shear.isChecked()
        ch35 = self.checkBox_trans.isChecked()

        self.rb_efi = rbefi
        self.rb_fsaf = rbfsaf
        self.rb_fcos = rbfcos
        self.rb_mask = rbmask
        self.rb_mxnet = rbmxnet
        self.rb_reti = rbreti
        self.rb_yolo = rbyolo
        self.avg = ch1
        self.bila = ch2
        self.blur = ch3
        self.chanhsv = ch4
        self.chanlab = ch5
        self.crop = ch6
        self.drop = ch7
        self.elas = ch8
        self.histo = ch9
        self.vflip = ch10
        self.hflip = ch11
        self.hvflip = ch12
        self.gamma = ch13
        self.blurGa = ch14
        self.gaunoise = ch15
        self.invert = ch16
        self.median = ch17
        self.none = ch18
        self.raiseB = ch19
        self.raiseGreen = ch20
        self.raiseHue = ch21
        self.raisered = ch22
        self.raisesatu = ch23
        self.raiseval = ch24
        self.resize = ch25
        self.rot10 = ch26
        self.rot90 = ch27
        self.rot180 = ch28
        self.rot270 = ch29
        self.saltpe = ch30
        self.sharpen = ch31
        self.sift = ch33
        self.shear = ch34
        self.trans = ch35

        self.aff = rbaff
        self.con = rbcon
        self.una = rbuna

        self.conf = le1

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
