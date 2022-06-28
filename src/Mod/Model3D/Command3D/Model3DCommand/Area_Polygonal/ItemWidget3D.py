# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ItemWidget3D.ui'
#
# Created: Fri May 21 14:45:17 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from Model3D.Tools import Completer

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(425, 50)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_name = QtGui.QLabel(Form)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.lineEdit_pointz = Completer.AutoCompleteEdit(Form)
        self.lineEdit_pointz.setObjectName("lineEdit_pointz")
        self.gridLayout.addWidget(self.lineEdit_pointz, 0, 5, 1, 2)
        self.lineEdit_pointx = Completer.AutoCompleteEdit(Form)
        self.lineEdit_pointx.setObjectName("lineEdit_pointx")
        self.gridLayout.addWidget(self.lineEdit_pointx, 0, 1, 1, 2)
        self.lineEdit_pointy = Completer.AutoCompleteEdit(Form)
        self.lineEdit_pointy.setObjectName("lineEdit_pointy")
        self.gridLayout.addWidget(self.lineEdit_pointy, 0, 3, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_pointx, self.lineEdit_pointy)
        Form.setTabOrder(self.lineEdit_pointy, self.lineEdit_pointz)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_name.setText(QtGui.QApplication.translate("Form", "Point1:", None, QtGui.QApplication.UnicodeUTF8))

