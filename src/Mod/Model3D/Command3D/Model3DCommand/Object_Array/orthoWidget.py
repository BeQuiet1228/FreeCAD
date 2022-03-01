# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'orthoWidget.ui'
#
# Created: Fri Apr 16 15:19:39 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!
import FreeCAD
from PySide import QtCore, QtGui
from Model3D.Tools import Completer
from Model3D.Tools import Tools3D


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(370, 191)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_orthoFace = QtGui.QLabel(Form)
        self.label_orthoFace.setObjectName("label_orthoFace")
        self.gridLayout.addWidget(self.label_orthoFace, 4, 0, 1, 1)
        self.label_interval1 = QtGui.QLabel(Form)
        self.label_interval1.setObjectName("label_interval1")
        self.gridLayout.addWidget(self.label_interval1, 0, 0, 1, 1)
        self.lineEdit_interval1 = Completer.AutoCompleteEdit(Form)
        self.lineEdit_interval1.setText("")
        self.lineEdit_interval1.setObjectName("lineEdit_interval1")
        self.gridLayout.addWidget(self.lineEdit_interval1, 0, 1, 1, 1)
        self.label_number1 = QtGui.QLabel(Form)
        self.label_number1.setObjectName("label_number1")
        self.gridLayout.addWidget(self.label_number1, 2, 0, 1, 1)
        self.lineEdit_interval2 = Completer.AutoCompleteEdit(Form)
        self.lineEdit_interval2.setText("")
        self.lineEdit_interval2.setObjectName("lineEdit_interval2")
        self.gridLayout.addWidget(self.lineEdit_interval2, 1, 1, 1, 1)
        self.lineEdit_number1 = Completer.AutoCompleteEdit(Form)
        self.lineEdit_number1.setText("")
        self.lineEdit_number1.setObjectName("lineEdit_number1")
        self.gridLayout.addWidget(self.lineEdit_number1, 2, 1, 1, 1)
        self.label_interval2 = QtGui.QLabel(Form)
        self.label_interval2.setObjectName("label_interval2")
        self.gridLayout.addWidget(self.label_interval2, 1, 0, 1, 1)
        self.label_number2 = QtGui.QLabel(Form)
        self.label_number2.setObjectName("label_number2")
        self.gridLayout.addWidget(self.label_number2, 3, 0, 1, 1)
        self.lineEdit_number2 = Completer.AutoCompleteEdit(Form)
        self.lineEdit_number2.setText("")
        self.lineEdit_number2.setObjectName("lineEdit_number2")
        self.gridLayout.addWidget(self.lineEdit_number2, 3, 1, 1, 1)
        self.comboBox_orthoFace = QtGui.QComboBox(Form)
        self.comboBox_orthoFace.setObjectName("comboBox_orthoFace")
        self.comboBox_orthoFace.addItem("")
        self.comboBox_orthoFace.addItem("")
        self.comboBox_orthoFace.addItem("")
        self.gridLayout.addWidget(self.comboBox_orthoFace, 4, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_orthoFace.setText(QtGui.QApplication.translate("Form", "Ortho Face:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_interval1.setText(QtGui.QApplication.translate("Form", "Interval X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_number1.setText(QtGui.QApplication.translate("Form", "Number X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_interval2.setText(QtGui.QApplication.translate("Form", "Interval Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_number2.setText(QtGui.QApplication.translate("Form", "Number Y:", None, QtGui.QApplication.UnicodeUTF8))
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            self.comboBox_orthoFace.setItemText(0, QtGui.QApplication.translate("Form", "XY", None,
                                                                                QtGui.QApplication.UnicodeUTF8))
            self.comboBox_orthoFace.setItemText(1, QtGui.QApplication.translate("Form", "XZ", None,
                                                                                QtGui.QApplication.UnicodeUTF8))
            self.comboBox_orthoFace.setItemText(2, QtGui.QApplication.translate("Form", "YZ", None,
                                                                                QtGui.QApplication.UnicodeUTF8))
        else:
            self.comboBox_orthoFace.setItemText(0, QtGui.QApplication.translate("Form", "RZ", None,
                                                                                QtGui.QApplication.UnicodeUTF8))

