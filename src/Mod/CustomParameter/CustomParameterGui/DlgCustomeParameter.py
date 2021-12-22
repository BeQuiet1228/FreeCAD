# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DlgCustomeParameter.ui'
#
# Created: Sat Oct 10 10:32:36 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui
from CustomParameter.CustomParameterCommand import CodeEdit

class Ui_Dialog_CustomParameterDlg(object):
    def setupUi(self, Dialog_CustomParameterDlg):
        Dialog_CustomParameterDlg.setObjectName("Dialog_CustomParameterDlg")
        Dialog_CustomParameterDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog_CustomParameterDlg.resize(810, 677)
        Dialog_CustomParameterDlg.setMinimumSize(QtCore.QSize(0, 0))
        Dialog_CustomParameterDlg.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_2 = QtGui.QGridLayout(Dialog_CustomParameterDlg)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.pushButton_cancel = QtGui.QPushButton(Dialog_CustomParameterDlg)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout_10.addWidget(self.pushButton_cancel)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem)
        self.pushButton_help = QtGui.QPushButton(Dialog_CustomParameterDlg)
        self.pushButton_help.setObjectName("pushButton_help")
        self.horizontalLayout_10.addWidget(self.pushButton_help)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem1)
        self.pushButton_ok = QtGui.QPushButton(Dialog_CustomParameterDlg)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_10.addWidget(self.pushButton_ok)
        self.gridLayout_2.addLayout(self.horizontalLayout_10, 1, 0, 1, 1)
        self.groupBox_WorkSpace_Z = QtGui.QGroupBox(Dialog_CustomParameterDlg)
        self.groupBox_WorkSpace_Z.setObjectName("groupBox_WorkSpace_Z")
        self.gridLayout = QtGui.QGridLayout(self.groupBox_WorkSpace_Z)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_end_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_end_7.setObjectName("horizontalLayout_end_7")
        self.textEdit_defintParam = CodeEdit.CodeEditor(self.groupBox_WorkSpace_Z)
        self.textEdit_defintParam.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.textEdit_defintParam.setSizeAdjustPolicy(QtGui.QAbstractScrollArea.AdjustIgnored)
        # self.textEdit_defintParam.setPlaceholderText("")
        self.textEdit_defintParam.setObjectName("textEdit_defintParam")
        self.horizontalLayout_end_7.addWidget(self.textEdit_defintParam)
        self.gridLayout.addLayout(self.horizontalLayout_end_7, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtGui.QLabel(self.groupBox_WorkSpace_Z)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMaximumSize(QtCore.QSize(167, 100))
        font = QtGui.QFont()
        font.setFamily("Adobe 黑体 Std R")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setFrameShape(QtGui.QFrame.WinPanel)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.textEdit_ValidInfo = QtGui.QTextEdit(self.groupBox_WorkSpace_Z)
        self.textEdit_ValidInfo.setMaximumSize(QtCore.QSize(1677, 100))
        self.textEdit_ValidInfo.setObjectName("textEdit_ValidInfo")
        self.horizontalLayout.addWidget(self.textEdit_ValidInfo)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_find = QtGui.QPushButton(self.groupBox_WorkSpace_Z)
        self.pushButton_find.setObjectName("pushButton_find")
        self.horizontalLayout_2.addWidget(self.pushButton_find)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.pushButton_undo = QtGui.QPushButton(self.groupBox_WorkSpace_Z)
        self.pushButton_undo.setObjectName("pushButton_undo")
        self.horizontalLayout_2.addWidget(self.pushButton_undo)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.pushButton_redo = QtGui.QPushButton(self.groupBox_WorkSpace_Z)
        self.pushButton_redo.setObjectName("pushButton_redo")
        self.horizontalLayout_2.addWidget(self.pushButton_redo)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_WorkSpace_Z, 0, 0, 1, 1)

        self.retranslateUi(Dialog_CustomParameterDlg)
        QtCore.QMetaObject.connectSlotsByName(Dialog_CustomParameterDlg)

    def retranslateUi(self, Dialog_CustomParameterDlg):
        Dialog_CustomParameterDlg.setWindowTitle(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "参数定义", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_cancel.setText(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "取消", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_help.setText(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "帮助", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ok.setText(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "确定", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_WorkSpace_Z.setTitle(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "参数定义", None, QtGui.QApplication.UnicodeUTF8))
#         self.textEdit_defintParam.setHtml(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
# "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\';\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "验证信息", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit_ValidInfo.setHtml(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'SimSun\';\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_find.setText(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "查找", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_undo.setText(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "撤销", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_redo.setText(QtGui.QApplication.translate("Dialog_CustomParameterDlg", "恢复", None, QtGui.QApplication.UnicodeUTF8))

