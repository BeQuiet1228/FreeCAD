# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ParticleDefineDialog.ui'
#
# Created: Fri May 21 16:17:20 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(402, 117)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.LineEdit_Name = QtGui.QLineEdit(Dialog)
        self.LineEdit_Name.setObjectName("LineEdit_Name")
        self.gridLayout.addWidget(self.LineEdit_Name, 0, 1, 1, 1)
        self.LineEdit_Quality = QtGui.QLineEdit(Dialog)
        self.LineEdit_Quality.setObjectName("LineEdit_Quality")
        self.gridLayout.addWidget(self.LineEdit_Quality, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 2, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.LineEdit_Unitl = QtGui.QLineEdit(Dialog)
        self.LineEdit_Unitl.setObjectName("LineEdit_Unitl")
        self.gridLayout.addWidget(self.LineEdit_Unitl, 0, 3, 1, 1)
        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 1, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pb_ok = QtGui.QPushButton(Dialog)
        self.pb_ok.setObjectName("pb_ok")
        self.horizontalLayout.addWidget(self.pb_ok)
        self.pb_cancel = QtGui.QPushButton(Dialog)
        self.pb_cancel.setObjectName("pb_cancel")
        self.horizontalLayout.addWidget(self.pb_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pb_ok, self.pb_cancel)
        Dialog.setTabOrder(self.pb_cancel, self.LineEdit_Name)
        Dialog.setTabOrder(self.LineEdit_Name, self.LineEdit_Unitl)
        Dialog.setTabOrder(self.LineEdit_Unitl, self.LineEdit_Quality)
        Dialog.setTabOrder(self.LineEdit_Quality, self.comboBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "质量：", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "粒子名称:", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_Name.setText(QtGui.QApplication.translate("Dialog", "IONS", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_Quality.setText(QtGui.QApplication.translate("Dialog", "28", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "电量单位：", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "质子质量单位：", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_Unitl.setText(QtGui.QApplication.translate("Dialog", "+1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(0, QtGui.QApplication.translate("Dialog", "PROTON", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(1, QtGui.QApplication.translate("Dialog", "ELECTRON", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.setItemText(2, QtGui.QApplication.translate("Dialog", "AMU", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_ok.setText(QtGui.QApplication.translate("Dialog", "确定", None, QtGui.QApplication.UnicodeUTF8))
        self.pb_cancel.setText(QtGui.QApplication.translate("Dialog", "取消", None, QtGui.QApplication.UnicodeUTF8))

