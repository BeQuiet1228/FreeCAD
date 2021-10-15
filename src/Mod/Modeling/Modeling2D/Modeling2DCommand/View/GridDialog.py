# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GridDialog.ui'
#
# Created: Wed Dec  2 13:47:58 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(472, 80)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridSize = QtGui.QSpinBox(Dialog)
        self.gridSize.setProperty("value", 10)
        self.gridSize.setObjectName("gridSize")
        self.gridLayout.addWidget(self.gridSize, 0, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pb_OK = QtGui.QPushButton(Dialog)
        self.pb_OK.setObjectName("pb_OK")
        self.gridLayout.addWidget(self.pb_OK, 1, 0, 1, 3)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 4)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.gridSize.setSuffix(QtGui.QApplication.translate("Dialog", "mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "网格大小：", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_OK.setText(QtGui.QApplication.translate("Dialog", "确定", None, QtGui.QApplication.UnicodeUTF8))

