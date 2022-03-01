# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'RunOptionsDialog.ui'
#
# Created: Fri May 21 16:18:05 2021
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog_RunOptionsDlg(object):
    def setupUi(self, Dialog_RunOptionsDlg):
        Dialog_RunOptionsDlg.setObjectName("Dialog_RunOptionsDlg")
        Dialog_RunOptionsDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog_RunOptionsDlg.resize(220, 140)
        Dialog_RunOptionsDlg.setMinimumSize(QtCore.QSize(0, 0))
        Dialog_RunOptionsDlg.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtGui.QVBoxLayout(Dialog_RunOptionsDlg)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.checkBox_show_structureChart = QtGui.QCheckBox(Dialog_RunOptionsDlg)
        self.checkBox_show_structureChart.setChecked(True)
        self.checkBox_show_structureChart.setObjectName("checkBox_show_structureChart")
        self.horizontalLayout_3.addWidget(self.checkBox_show_structureChart)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.checkBox_paused_when_start = QtGui.QCheckBox(Dialog_RunOptionsDlg)
        self.checkBox_paused_when_start.setObjectName("checkBox_paused_when_start")
        self.horizontalLayout_4.addWidget(self.checkBox_paused_when_start)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.pushButton_ok = QtGui.QPushButton(Dialog_RunOptionsDlg)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_7.addWidget(self.pushButton_ok)
        self.verticalLayout_2.addLayout(self.horizontalLayout_7)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog_RunOptionsDlg)
        QtCore.QMetaObject.connectSlotsByName(Dialog_RunOptionsDlg)
        Dialog_RunOptionsDlg.setTabOrder(self.pushButton_ok, self.checkBox_show_structureChart)
        Dialog_RunOptionsDlg.setTabOrder(self.checkBox_show_structureChart, self.checkBox_paused_when_start)

    def retranslateUi(self, Dialog_RunOptionsDlg):
        Dialog_RunOptionsDlg.setWindowTitle(QtGui.QApplication.translate("Dialog_RunOptionsDlg", "运行选项设置", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_show_structureChart.setText(QtGui.QApplication.translate("Dialog_RunOptionsDlg", "开始计算时显示结构图", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_paused_when_start.setText(QtGui.QApplication.translate("Dialog_RunOptionsDlg", "开始计算时处于暂停状态", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ok.setText(QtGui.QApplication.translate("Dialog_RunOptionsDlg", "确定", None, QtGui.QApplication.UnicodeUTF8))

