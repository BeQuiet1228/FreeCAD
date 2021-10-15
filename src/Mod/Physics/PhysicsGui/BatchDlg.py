# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\User Files\Desktop\Code\PICGUIC\FREECAD\build\Mod\Physics\PhysicsGui\BatchDlg.ui'
#
# Created: Thu Dec 26 17:00:54 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(932, 696)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setSpacing(11)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit_params = QtGui.QTextEdit(Dialog)
        self.textEdit_params.setObjectName("textEdit_params")
        self.gridLayout.addWidget(self.textEdit_params, 1, 1, 1, 1)
        self.textEdit_original = QtGui.QTextEdit(Dialog)
        self.textEdit_original.setReadOnly(True)
        self.textEdit_original.setObjectName("textEdit_original")
        self.gridLayout.addWidget(self.textEdit_original, 1, 0, 1, 1)
        self.textEdit_statusInfo = QtGui.QTextEdit(Dialog)
        self.textEdit_statusInfo.setReadOnly(True)
        self.textEdit_statusInfo.setObjectName("textEdit_statusInfo")
        self.gridLayout.addWidget(self.textEdit_statusInfo, 5, 0, 1, 2)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 2)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_cancel = QtGui.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton_help = QtGui.QPushButton(Dialog)
        self.pushButton_help.setObjectName("pushButton_help")
        self.horizontalLayout.addWidget(self.pushButton_help)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_start = QtGui.QPushButton(Dialog)
        self.pushButton_start.setObjectName("pushButton_start")
        self.horizontalLayout.addWidget(self.pushButton_start)
        self.gridLayout.addLayout(self.horizontalLayout, 6, 0, 1, 2)
        spacerItem2 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 2)
        self.gridLayout.setRowStretch(1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "批处理", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "原M3D文件：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "状态消息：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "参数定义：", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_cancel.setText(QtGui.QApplication.translate("Dialog", "取消", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_help.setText(QtGui.QApplication.translate("Dialog", "帮助", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_start.setText(QtGui.QApplication.translate("Dialog", "开始", None, QtGui.QApplication.UnicodeUTF8))

