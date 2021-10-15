# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PointWidget.ui'
#
# Created: Fri May 21 15:13:58 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from Model3D.Tools import Completer

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(408, 92)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_y2 = QtGui.QLabel(Form)
        self.label_y2.setObjectName("label_y2")
        self.gridLayout.addWidget(self.label_y2, 0, 6, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.lineEdit_point2y = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2y.setObjectName("lineEdit_point2y")
        self.gridLayout.addWidget(self.lineEdit_point2y, 2, 4, 1, 4)
        self.label_z2 = QtGui.QLabel(Form)
        self.label_z2.setObjectName("label_z2")
        self.gridLayout.addWidget(self.label_z2, 0, 9, 1, 1)
        self.lineEdit_point1x = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1x.setObjectName("lineEdit_point1x")
        self.gridLayout.addWidget(self.lineEdit_point1x, 1, 1, 1, 3)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_x2 = QtGui.QLabel(Form)
        self.label_x2.setObjectName("label_x2")
        self.gridLayout.addWidget(self.label_x2, 0, 2, 1, 1)
        self.lineEdit_point1y = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1y.setObjectName("lineEdit_point1y")
        self.gridLayout.addWidget(self.lineEdit_point1y, 1, 4, 1, 4)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 7, 1, 1)
        self.lineEdit_point2x = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2x.setObjectName("lineEdit_point2x")
        self.gridLayout.addWidget(self.lineEdit_point2x, 2, 1, 1, 3)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 4, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 0, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 0, 8, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 0, 3, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 0, 10, 1, 1)
        self.lineEdit_point1z = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1z.setObjectName("lineEdit_point1z")
        self.gridLayout.addWidget(self.lineEdit_point1z, 1, 8, 1, 3)
        self.lineEdit_point2z = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2z.setObjectName("lineEdit_point2z")
        self.gridLayout.addWidget(self.lineEdit_point2z, 2, 8, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        Form.setTabOrder(self.lineEdit_point1x, self.lineEdit_point1y)
        Form.setTabOrder(self.lineEdit_point1y, self.lineEdit_point1z)
        Form.setTabOrder(self.lineEdit_point1z, self.lineEdit_point2x)
        Form.setTabOrder(self.lineEdit_point2x, self.lineEdit_point2y)
        Form.setTabOrder(self.lineEdit_point2y, self.lineEdit_point2z)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_y2.setText(QtGui.QApplication.translate("Form", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Point_2", None, QtGui.QApplication.UnicodeUTF8))
        self.label_z2.setText(QtGui.QApplication.translate("Form", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Point_1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_x2.setText(QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))

