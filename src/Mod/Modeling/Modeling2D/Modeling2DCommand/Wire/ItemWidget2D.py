# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ItemWidget2D.ui'
#
# Created: Wed Nov  4 12:58:21 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from Modeling.Common.Tools import Completer

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(283, 45)
        self.verticalLayout = QtGui.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.le_y = Completer.AutoCompleteEdit(Form)
        self.le_y.setObjectName("le_y")
        self.gridLayout_2.addWidget(self.le_y, 0, 2, 1, 1)
        self.lb_name = QtGui.QLabel(Form)
        self.lb_name.setObjectName("lb_name")
        self.gridLayout_2.addWidget(self.lb_name, 0, 0, 1, 1)
        self.le_x = Completer.AutoCompleteEdit(Form)
        self.le_x.setObjectName("le_x")
        self.gridLayout_2.addWidget(self.le_x, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_name.setText(QtGui.QApplication.translate("Form", "Point1:", None, QtGui.QApplication.UnicodeUTF8))

