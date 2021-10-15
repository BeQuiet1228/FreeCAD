# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MarkDlg.ui'
#
# Created: Thu May 14 16:53:20 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
import Modeling
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(528, 119)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboBox_obj = QtGui.QComboBox(Dialog)
        self.comboBox_obj.setObjectName("comboBox_obj")
        self.comboBox_obj.addItem("")
        self.gridLayout.addWidget(self.comboBox_obj, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.comboBox_x = QtGui.QComboBox(Dialog)
        self.comboBox_x.setObjectName("comboBox_x")
        self.comboBox_x.addItem("")
        self.comboBox_x.addItem("")
        self.comboBox_x.addItem("")
        self.gridLayout.addWidget(self.comboBox_x, 0, 3, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_size = Modeling.Common.Tools.Completer.AutoCompleteEdit(Dialog)
        self.lineEdit_size.setObjectName("lineEdit_size")
        self.gridLayout.addWidget(self.lineEdit_size, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.checkBox_min = QtGui.QCheckBox(Dialog)
        self.checkBox_min.setObjectName("checkBox_min")
        self.gridLayout.addWidget(self.checkBox_min, 1, 1, 1, 1)
        self.checkBox_mid = QtGui.QCheckBox(Dialog)
        self.checkBox_mid.setObjectName("checkBox_mid")
        self.gridLayout.addWidget(self.checkBox_mid, 1, 2, 1, 1)
        self.checkBox_max = QtGui.QCheckBox(Dialog)
        self.checkBox_max.setObjectName("checkBox_max")
        self.gridLayout.addWidget(self.checkBox_max, 1, 3, 1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_ok = QtGui.QPushButton(Dialog)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_3.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtGui.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_3.addWidget(self.pushButton_cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "MARK", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "MARK对象：", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_obj.setItemText(0, QtGui.QApplication.translate("Dialog", "未指定", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "方向：", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_x.setItemText(0, QtGui.QApplication.translate("Dialog", "X1", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_x.setItemText(1, QtGui.QApplication.translate("Dialog", "X2", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox_x.setItemText(2, QtGui.QApplication.translate("Dialog", "X3", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "大小：", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit_size.setText(QtGui.QApplication.translate("Dialog", "1mm", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("Dialog", "MARK位置：", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_min.setText(QtGui.QApplication.translate("Dialog", "MINIMUM", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_mid.setText(QtGui.QApplication.translate("Dialog", "MIDPOINT", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_max.setText(QtGui.QApplication.translate("Dialog", "MAXIMUM", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ok.setText(QtGui.QApplication.translate("Dialog", "确定", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_cancel.setText(QtGui.QApplication.translate("Dialog", "取消", None, QtGui.QApplication.UnicodeUTF8))

