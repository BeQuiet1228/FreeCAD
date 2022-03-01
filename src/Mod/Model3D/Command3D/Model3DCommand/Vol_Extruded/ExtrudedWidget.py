# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ExtrudedWidget.ui'
#
# Created: Mon Mar 15 15:17:32 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(386, 66)
        self.gridLayout_2 = QtGui.QGridLayout(Form)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_name = QtGui.QLabel(Form)
        self.label_name.setObjectName("label_name")
        self.gridLayout.addWidget(self.label_name, 0, 0, 1, 1)
        self.comboBox_Line = QtGui.QComboBox(Form)
        self.comboBox_Line.setObjectName("comboBox_Line")
        self.gridLayout.addWidget(self.comboBox_Line, 0, 1, 1, 1)
        self.label_area = QtGui.QLabel(Form)
        self.label_area.setObjectName("label_area")
        self.gridLayout.addWidget(self.label_area, 1, 0, 1, 1)
        self.comboBox_Area = QtGui.QComboBox(Form)
        self.comboBox_Area.setObjectName("comboBox_Area")
        self.gridLayout.addWidget(self.comboBox_Area, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.label_name.setText(QtGui.QApplication.translate("Form", "Line", None, QtGui.QApplication.UnicodeUTF8))
        self.label_area.setText(QtGui.QApplication.translate("Form", "Area", None, QtGui.QApplication.UnicodeUTF8))

