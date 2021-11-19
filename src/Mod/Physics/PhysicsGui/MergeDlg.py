# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MergeDlg.ui'
#
# Created: Sat Apr 18 16:57:19 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("宏粒子合并")
        Dialog.resize(418, 123)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.lineEdit_max = QtGui.QLineEdit(Dialog)
        self.lineEdit_max.setObjectName("lineEdit_max")
        self.gridLayout.addWidget(self.lineEdit_max, 2, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.lineEdit_every = QtGui.QLineEdit(Dialog)
        self.lineEdit_every.setObjectName("lineEdit_every")
        self.gridLayout.addWidget(self.lineEdit_every, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_ok = QtGui.QPushButton(Dialog)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtGui.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "宏粒子合并", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_max.setText(QtGui.QApplication.translate("Dialog", "100000", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "最大宏粒子数：", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "每个网格区粒子数：", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_every.setText(QtGui.QApplication.translate("Dialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "粒子种类：", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "离子", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "电子", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ok.setText(QtGui.QApplication.translate("Dialog", "确定", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_cancel.setText(QtGui.QApplication.translate("Dialog", "取消", None, QtGui.QApplication.UnicodeUTF8))

