# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'CollectionOutputDialog.ui'
#
# Created: Sun Jul 31 15:42:28 2022
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(489, 142)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 12, 471, 121))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.collection_label = QtGui.QLabel(self.layoutWidget)
        self.collection_label.setObjectName("collection_label")
        self.gridLayout_2.addWidget(self.collection_label, 0, 0, 1, 1)
        self.input_body = QtGui.QComboBox(self.layoutWidget)
        self.input_body.setEnabled(True)
        self.input_body.setObjectName("input_body")
        self.gridLayout_2.addWidget(self.input_body, 0, 1, 1, 1)
        self.path_label = QtGui.QLabel(self.layoutWidget)
        self.path_label.setObjectName("path_label")
        self.gridLayout_2.addWidget(self.path_label, 1, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.path = QtGui.QLineEdit(self.layoutWidget)
        self.path.setEnabled(True)
        self.path.setText("")
        self.path.setObjectName("path")
        self.gridLayout.addWidget(self.path, 0, 0, 1, 1)
        self.pushButton = QtGui.QPushButton(self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 1, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_ok = QtGui.QPushButton(self.layoutWidget)
        self.pb_ok.setEnabled(True)
        self.pb_ok.setObjectName("pb_ok")
        self.horizontalLayout.addWidget(self.pb_ok)
        self.pb_cancel = QtGui.QPushButton(self.layoutWidget)
        self.pb_cancel.setEnabled(True)
        self.pb_cancel.setObjectName("pb_cancel")
        self.horizontalLayout.addWidget(self.pb_cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 2, 0, 1, 2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pb_ok, self.pb_cancel)
        Dialog.setTabOrder(self.pb_cancel, self.input_body)
        Dialog.setTabOrder(self.input_body, self.path)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "收集体导出", None, QtGui.QApplication.UnicodeUTF8))
        self.collection_label.setText(QtGui.QApplication.translate("Dialog", "指定收集体：", None, QtGui.QApplication.UnicodeUTF8))
        self.path_label.setText(QtGui.QApplication.translate("Dialog", "输出文件路径：", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Dialog", "Select path", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_ok.setText(QtGui.QApplication.translate("Dialog", "确定", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_cancel.setText(QtGui.QApplication.translate("Dialog", "取消", None, QtGui.QApplication.UnicodeUTF8))

