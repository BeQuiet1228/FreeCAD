# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PointWidget.ui'
#
# Created: Fri Mar  5 09:32:06 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from Model3D.Tools import Completer

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(514, 154)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 4, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        self.label_y2 = QtGui.QLabel(Form)
        self.label_y2.setObjectName("label_y2")
        self.gridLayout.addWidget(self.label_y2, 0, 5, 1, 1)
        self.label_x2 = QtGui.QLabel(Form)
        self.label_x2.setObjectName("label_x2")
        self.gridLayout.addWidget(self.label_x2, 0, 2, 1, 1)
        self.lineEdit_pointx = Completer.AutoCompleteEdit(Form)
        self.lineEdit_pointx.setObjectName("lineEdit_pointx")
        self.gridLayout.addWidget(self.lineEdit_pointx, 1, 1, 1, 3)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 9, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 6, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_z2 = QtGui.QLabel(Form)
        self.label_z2.setObjectName("label_z2")
        self.gridLayout.addWidget(self.label_z2, 0, 8, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 7, 1, 1)
        self.lineEdit_pointz = Completer.AutoCompleteEdit(Form)
        self.lineEdit_pointz.setObjectName("lineEdit_pointz")
        self.gridLayout.addWidget(self.lineEdit_pointz, 1, 7, 1, 3)
        self.lineEdit_pointy = Completer.AutoCompleteEdit(Form)
        self.lineEdit_pointy.setObjectName("lineEdit_pointy")
        self.gridLayout.addWidget(self.lineEdit_pointy, 1, 4, 1, 3)
        self.lineEdit_radius = Completer.AutoCompleteEdit(Form)
        self.lineEdit_radius.setObjectName("lineEdit_radius")
        self.gridLayout.addWidget(self.lineEdit_radius, 2, 1, 1, 3)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_y2.setText(QtGui.QApplication.translate("Form", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_x2.setText(QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Point:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_z2.setText(QtGui.QApplication.translate("Form", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Radius:", None, QtGui.QApplication.UnicodeUTF8))

