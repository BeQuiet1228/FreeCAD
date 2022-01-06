# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'linearWidget.ui'
#
# Created: Fri Apr 16 14:45:39 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from Model3D.Tools import Completer

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(370, 191)
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_intervalX = QtGui.QLabel(Form)
        self.label_intervalX.setObjectName("label_intervalX")
        self.gridLayout.addWidget(self.label_intervalX, 0, 0, 1, 1)
        self.lineEdit_intervalX = Completer.AutoCompleteEdit(Form)
        self.lineEdit_intervalX.setText("")
        self.lineEdit_intervalX.setObjectName("lineEdit_intervalX")
        self.gridLayout.addWidget(self.lineEdit_intervalX, 0, 1, 1, 1)
        self.label_intervalY = QtGui.QLabel(Form)
        self.label_intervalY.setObjectName("label_intervalY")
        self.gridLayout.addWidget(self.label_intervalY, 1, 0, 1, 1)
        self.lineEdit_intervalY = Completer.AutoCompleteEdit(Form)
        self.lineEdit_intervalY.setText("")
        self.lineEdit_intervalY.setObjectName("lineEdit_intervalY")
        self.gridLayout.addWidget(self.lineEdit_intervalY, 1, 1, 1, 1)
        self.label_intervalZ = QtGui.QLabel(Form)
        self.label_intervalZ.setObjectName("label_intervalZ")
        self.gridLayout.addWidget(self.label_intervalZ, 2, 0, 1, 1)
        self.lineEdit_intervalZ = Completer.AutoCompleteEdit(Form)
        self.lineEdit_intervalZ.setText("")
        self.lineEdit_intervalZ.setObjectName("lineEdit_intervalZ")
        self.gridLayout.addWidget(self.lineEdit_intervalZ, 2, 1, 1, 1)
        self.label_number = QtGui.QLabel(Form)
        self.label_number.setObjectName("label_number")
        self.gridLayout.addWidget(self.label_number, 3, 0, 1, 1)
        self.lineEdit_number = Completer.AutoCompleteEdit(Form)
        self.lineEdit_number.setText("")
        self.lineEdit_number.setObjectName("lineEdit_number")
        self.gridLayout.addWidget(self.lineEdit_number, 3, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_intervalX.setText(QtGui.QApplication.translate("Form", "Interval X:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_intervalY.setText(QtGui.QApplication.translate("Form", "Interval Y:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_intervalZ.setText(QtGui.QApplication.translate("Form", "Interval Z:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_number.setText(QtGui.QApplication.translate("Form", "Number:", None, QtGui.QApplication.UnicodeUTF8))

