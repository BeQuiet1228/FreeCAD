# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'polarWidget.ui'
#
# Created: Fri Apr 16 14:45:52 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!
import FreeCAD
from PySide import QtCore, QtGui
from Model3D.Tools import Completer
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(370, 97)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_numberPolar = QtGui.QLabel(Form)
        self.label_numberPolar.setObjectName("label_numberPolar")
        self.gridLayout.addWidget(self.label_numberPolar, 0, 0, 1, 1)
        self.label_centerAxis = QtGui.QLabel(Form)
        self.label_centerAxis.setObjectName("label_centerAxis")
        self.gridLayout.addWidget(self.label_centerAxis, 1, 0, 1, 1)
        self.comboBox_centerAxis = QtGui.QComboBox(Form)
        self.comboBox_centerAxis.setObjectName("comboBox_centerAxis")
        self.comboBox_centerAxis.addItem("")
        self.comboBox_centerAxis.addItem("")
        self.comboBox_centerAxis.addItem("")
        self.gridLayout.addWidget(self.comboBox_centerAxis, 1, 1, 1, 1)
        self.lineEdit_numberPolar = Completer.AutoCompleteEdit(Form)
        self.lineEdit_numberPolar.setText("")
        self.lineEdit_numberPolar.setObjectName("lineEdit_numberPolar")
        self.gridLayout.addWidget(self.lineEdit_numberPolar, 0, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_numberPolar.setText(QtGui.QApplication.translate("Form", "Number Polar:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_centerAxis.setText(QtGui.QApplication.translate("Form", "Center Axis:", None, QtGui.QApplication.UnicodeUTF8))
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            self.comboBox_centerAxis.setItemText(0, QtGui.QApplication.translate("Form", "X", None, QtGui.QApplication.UnicodeUTF8))
            self.comboBox_centerAxis.setItemText(1, QtGui.QApplication.translate("Form", "Y", None, QtGui.QApplication.UnicodeUTF8))
            self.comboBox_centerAxis.setItemText(2, QtGui.QApplication.translate("Form", "Z", None, QtGui.QApplication.UnicodeUTF8))
        else:
            self.comboBox_centerAxis.setItemText(0, QtGui.QApplication.translate("Form", "Z", None, QtGui.QApplication.UnicodeUTF8))

