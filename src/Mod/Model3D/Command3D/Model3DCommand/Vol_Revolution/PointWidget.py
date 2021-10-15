# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PointWidget.ui'
#
# Created: Thu Mar  4 11:48:38 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from Model3D.Tools import Completer

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(440, 118)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_9 = QtGui.QLabel(Form)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 0, 1, 1)
        self.comboBox_baseArea = QtGui.QComboBox(Form)
        self.comboBox_baseArea.setObjectName("comboBox_baseArea")
        self.gridLayout.addWidget(self.comboBox_baseArea, 0, 1, 1, 6)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.label_x2 = QtGui.QLabel(Form)
        self.label_x2.setObjectName("label_x2")
        self.gridLayout.addWidget(self.label_x2, 1, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 4, 1, 1)
        self.label_y2 = QtGui.QLabel(Form)
        self.label_y2.setObjectName("label_y2")
        self.gridLayout.addWidget(self.label_y2, 1, 5, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 1, 6, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 1, 7, 1, 1)
        self.label_z2 = QtGui.QLabel(Form)
        self.label_z2.setObjectName("label_z2")
        self.gridLayout.addWidget(self.label_z2, 1, 8, 1, 1)
        spacerItem5 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem5, 1, 9, 1, 1)
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.lineEdit_point1x = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1x.setObjectName("lineEdit_point1x")
        self.gridLayout.addWidget(self.lineEdit_point1x, 2, 1, 1, 3)
        self.lineEdit_point1y = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1y.setObjectName("lineEdit_point1y")
        self.gridLayout.addWidget(self.lineEdit_point1y, 2, 4, 1, 3)
        self.lineEdit_point1z = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point1z.setObjectName("lineEdit_point1z")
        self.gridLayout.addWidget(self.lineEdit_point1z, 2, 7, 1, 3)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.lineEdit_point2x = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2x.setObjectName("lineEdit_point2x")
        self.gridLayout.addWidget(self.lineEdit_point2x, 3, 1, 1, 3)
        self.lineEdit_point2y = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2y.setObjectName("lineEdit_point2y")
        self.gridLayout.addWidget(self.lineEdit_point2y, 3, 4, 1, 3)
        self.lineEdit_point2z = Completer.AutoCompleteEdit(Form)
        self.lineEdit_point2z.setObjectName("lineEdit_point2z")
        self.gridLayout.addWidget(self.lineEdit_point2z, 3, 7, 1, 3)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("Form", "BaseArea:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_x2.setText(QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))
        self.label_y2.setText(QtGui.QApplication.translate("Form", "Y", None, QtGui.QApplication.UnicodeUTF8))
        self.label_z2.setText(QtGui.QApplication.translate("Form", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Point_Base:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Point_Top:", None, QtGui.QApplication.UnicodeUTF8))

