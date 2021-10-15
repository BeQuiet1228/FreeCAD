# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MacroParticleDialog.ui'
#
# Created: Fri May 21 16:15:33 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(409, 145)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.LineEdit_max = QtGui.QLineEdit(Dialog)
        self.LineEdit_max.setEnabled(True)
        self.LineEdit_max.setObjectName("LineEdit_max")
        self.gridLayout.addWidget(self.LineEdit_max, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.LineEdit_every = QtGui.QLineEdit(Dialog)
        self.LineEdit_every.setEnabled(True)
        self.LineEdit_every.setObjectName("LineEdit_every")
        self.gridLayout.addWidget(self.LineEdit_every, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.typeComboBox = QtGui.QComboBox(Dialog)
        self.typeComboBox.setEnabled(True)
        self.typeComboBox.setObjectName("typeComboBox")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.typeComboBox.addItem("")
        self.gridLayout.addWidget(self.typeComboBox, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_ok = QtGui.QPushButton(Dialog)
        self.pb_ok.setEnabled(True)
        self.pb_ok.setObjectName("pb_ok")
        self.horizontalLayout.addWidget(self.pb_ok)
        self.pb_cancel = QtGui.QPushButton(Dialog)
        self.pb_cancel.setEnabled(True)
        self.pb_cancel.setObjectName("pb_cancel")
        self.horizontalLayout.addWidget(self.pb_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pb_ok, self.pb_cancel)
        Dialog.setTabOrder(self.pb_cancel, self.typeComboBox)
        Dialog.setTabOrder(self.typeComboBox, self.LineEdit_every)
        Dialog.setTabOrder(self.LineEdit_every, self.LineEdit_max)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "宏粒子合并", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_max.setText(QtGui.QApplication.translate("Dialog", "100000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "最大宏粒子数：", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "每个网格区粒子数：", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_every.setText(QtGui.QApplication.translate("Dialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "粒子种类：", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "ALL", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "ELECTRON", None, QtGui.QApplication.UnicodeUTF8))
        self.typeComboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "PROTON", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_ok.setText(QtGui.QApplication.translate("Dialog", "确定", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_cancel.setText(QtGui.QApplication.translate("Dialog", "取消", None, QtGui.QApplication.UnicodeUTF8))

