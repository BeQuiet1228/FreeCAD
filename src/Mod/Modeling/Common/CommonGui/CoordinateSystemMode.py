# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CoordinateSystemMode.ui'
#
# Created: Thu Dec 31 10:41:38 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(318, 259)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.create2DButton = QtGui.QPushButton(Form)
        self.create2DButton.setObjectName("create2DButton")
        self.gridLayout_2.addWidget(self.create2DButton, 1, 0, 1, 1)
        self.create3DTextButton = QtGui.QPushButton(Form)
        self.create3DTextButton.setObjectName("create3DTextButton")
        self.gridLayout_2.addWidget(self.create3DTextButton, 3, 0, 1, 1)
        self.create3DButton = QtGui.QPushButton(Form)
        self.create3DButton.setObjectName("create3DButton")
        self.gridLayout_2.addWidget(self.create3DButton, 0, 0, 1, 1)
        self.create2DTextButton = QtGui.QPushButton(Form)
        self.create2DTextButton.setObjectName("create2DTextButton")
        self.gridLayout_2.addWidget(self.create2DTextButton, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.create2DButton.setText(QtGui.QApplication.translate("Form", "Create 2D Doucment", None, QtGui.QApplication.UnicodeUTF8))
        self.create3DTextButton.setText(QtGui.QApplication.translate("Form", "Create 3D Text Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.create3DButton.setText(QtGui.QApplication.translate("Form", "Create 3D Doucment", None, QtGui.QApplication.UnicodeUTF8))
        self.create2DTextButton.setText(QtGui.QApplication.translate("Form", "Create 2D Text Edit", None, QtGui.QApplication.UnicodeUTF8))

