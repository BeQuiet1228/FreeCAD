# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FindDialog.ui'
#
# Created: Tue Dec 31 10:41:50 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 99)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setHorizontalSpacing(16)
        self.gridLayout.setObjectName("gridLayout")
        self.findText = QtGui.QLineEdit(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findText.sizePolicy().hasHeightForWidth())
        self.findText.setSizePolicy(sizePolicy)
        self.findText.setMinimumSize(QtCore.QSize(0, 30))
        self.findText.setObjectName("findText")
        self.gridLayout.addWidget(self.findText, 0, 0, 1, 2)
        self.findButton = QtGui.QPushButton(Dialog)
        self.findButton.setObjectName("findButton")
        self.gridLayout.addWidget(self.findButton, 0, 2, 1, 1)
        self.checkSensitive = QtGui.QCheckBox(Dialog)
        self.checkSensitive.setObjectName("checkSensitive")
        self.gridLayout.addWidget(self.checkSensitive, 1, 0, 1, 1)
        self.checkWhole = QtGui.QCheckBox(Dialog)
        self.checkWhole.setObjectName("checkWhole")
        self.gridLayout.addWidget(self.checkWhole, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.findText, self.checkSensitive)
        Dialog.setTabOrder(self.checkSensitive, self.checkWhole)
        Dialog.setTabOrder(self.checkWhole, self.findButton)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "查找", None, QtGui.QApplication.UnicodeUTF8))
        self.findButton.setText(QtGui.QApplication.translate("Dialog", "查找", None, QtGui.QApplication.UnicodeUTF8))
        self.checkSensitive.setText(QtGui.QApplication.translate("Dialog", "大小写敏感", None, QtGui.QApplication.UnicodeUTF8))
        self.checkWhole.setText(QtGui.QApplication.translate("Dialog", "整个单词", None, QtGui.QApplication.UnicodeUTF8))

