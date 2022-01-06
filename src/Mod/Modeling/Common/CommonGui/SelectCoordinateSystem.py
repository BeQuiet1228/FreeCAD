# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SelectCoordinateSystem.ui'
#
# Created: Thu Dec 31 10:40:38 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(352, 259)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.cartesianButton = QtGui.QPushButton(Form)
        self.cartesianButton.setObjectName("cartesianButton")
        self.gridLayout.addWidget(self.cartesianButton, 0, 0, 1, 1)
        self.polarButton = QtGui.QPushButton(Form)
        self.polarButton.setObjectName("polarButton")
        self.gridLayout.addWidget(self.polarButton, 1, 0, 1, 1)
        self.cylindricalButton = QtGui.QPushButton(Form)
        self.cylindricalButton.setObjectName("cylindricalButton")
        self.gridLayout.addWidget(self.cylindricalButton, 2, 0, 1, 1)
        self.cancelButton = QtGui.QPushButton(Form)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 3, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.cartesianButton.setText(QtGui.QApplication.translate("Form", "Cartesian", None, QtGui.QApplication.UnicodeUTF8))
        self.polarButton.setText(QtGui.QApplication.translate("Form", "Polar", None, QtGui.QApplication.UnicodeUTF8))
        self.cylindricalButton.setText(QtGui.QApplication.translate("Form", "Cylindrical", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("Form", "上一页", None, QtGui.QApplication.UnicodeUTF8))

