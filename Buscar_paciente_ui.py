# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Victoria Catalina\Documents\GitHub\Trabajo-Final\Buscar_paciente.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 166)
        self.textoingresarcedula = QtWidgets.QLabel(Dialog)
        self.textoingresarcedula.setGeometry(QtCore.QRect(30, 30, 191, 16))
        self.textoingresarcedula.setObjectName("textoingresarcedula")
        self.Cedula = QtWidgets.QLineEdit(Dialog)
        self.Cedula.setGeometry(QtCore.QRect(240, 30, 113, 22))
        self.Cedula.setObjectName("Cedula")
        self.SALIR = QtWidgets.QPushButton(Dialog)
        self.SALIR.setGeometry(QtCore.QRect(230, 90, 93, 28))
        self.SALIR.setObjectName("SALIR")
        self.boton_buscar = QtWidgets.QPushButton(Dialog)
        self.boton_buscar.setGeometry(QtCore.QRect(90, 90, 93, 28))
        self.boton_buscar.setObjectName("boton_buscar")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textoingresarcedula.setText(_translate("Dialog", "INGRESE CEDULA DEL PACIENTE"))
        self.SALIR.setText(_translate("Dialog", "SALIR"))
        self.boton_buscar.setText(_translate("Dialog", "BUSCAR"))
