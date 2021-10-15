# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FiledSettingDialog.ui'
#
# Created: Mon Nov 30 16:16:32 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog_FieldSettingDlg(object):
    def setupUi(self, Dialog_FieldSettingDlg):
        Dialog_FieldSettingDlg.setObjectName("Dialog_FieldSettingDlg")
        Dialog_FieldSettingDlg.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog_FieldSettingDlg.resize(557, 662)
        Dialog_FieldSettingDlg.setMinimumSize(QtCore.QSize(0, 0))
        Dialog_FieldSettingDlg.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.gridLayout_4 = QtGui.QGridLayout(Dialog_FieldSettingDlg)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.groupBox_WorkSpace_X = QtGui.QGroupBox(Dialog_FieldSettingDlg)
        self.groupBox_WorkSpace_X.setObjectName("groupBox_WorkSpace_X")
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_WorkSpace_X)
        self.gridLayout_2.setObjectName("gridLayout_2")
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 3, 0, 1, 1)
        self.horizontalLayout_start = QtGui.QHBoxLayout()
        self.horizontalLayout_start.setObjectName("horizontalLayout_start")
        self.checkBox_magenetic_x = QtGui.QCheckBox(self.groupBox_WorkSpace_X)
        self.checkBox_magenetic_x.setObjectName("checkBox_magenetic_x")
        self.horizontalLayout_start.addWidget(self.checkBox_magenetic_x)
        self.LineEdit_magenetic_x = QtGui.QTextEdit(self.groupBox_WorkSpace_X)
        self.LineEdit_magenetic_x.setMaximumSize(QtCore.QSize(16777215, 60))
        self.LineEdit_magenetic_x.setObjectName("LineEdit_magenetic_x")
        self.horizontalLayout_start.addWidget(self.LineEdit_magenetic_x)
        self.label_2 = QtGui.QLabel(self.groupBox_WorkSpace_X)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_start.addWidget(self.label_2)
        self.gridLayout_2.addLayout(self.horizontalLayout_start, 0, 0, 1, 1)
        self.horizontalLayout_start_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_start_2.setObjectName("horizontalLayout_start_2")
        self.checkBox_magenetic_y = QtGui.QCheckBox(self.groupBox_WorkSpace_X)
        self.checkBox_magenetic_y.setObjectName("checkBox_magenetic_y")
        self.horizontalLayout_start_2.addWidget(self.checkBox_magenetic_y)
        self.LineEdit_magenetic_y = QtGui.QTextEdit(self.groupBox_WorkSpace_X)
        self.LineEdit_magenetic_y.setMaximumSize(QtCore.QSize(16777215, 60))
        self.LineEdit_magenetic_y.setObjectName("LineEdit_magenetic_y")
        self.horizontalLayout_start_2.addWidget(self.LineEdit_magenetic_y)
        self.label_3 = QtGui.QLabel(self.groupBox_WorkSpace_X)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_start_2.addWidget(self.label_3)
        self.gridLayout_2.addLayout(self.horizontalLayout_start_2, 2, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_WorkSpace_X, 0, 0, 1, 1)
        self.groupBox_WorkSpace_Y = QtGui.QGroupBox(Dialog_FieldSettingDlg)
        self.groupBox_WorkSpace_Y.setObjectName("groupBox_WorkSpace_Y")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_WorkSpace_Y)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_start_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_start_6.setObjectName("horizontalLayout_start_6")
        self.checkBox_electric_x = QtGui.QCheckBox(self.groupBox_WorkSpace_Y)
        self.checkBox_electric_x.setObjectName("checkBox_electric_x")
        self.horizontalLayout_start_6.addWidget(self.checkBox_electric_x)
        self.LineEdit_electric_x = QtGui.QTextEdit(self.groupBox_WorkSpace_Y)
        self.LineEdit_electric_x.setMaximumSize(QtCore.QSize(16777215, 60))
        self.LineEdit_electric_x.setObjectName("LineEdit_electric_x")
        self.horizontalLayout_start_6.addWidget(self.LineEdit_electric_x)
        self.label_8 = QtGui.QLabel(self.groupBox_WorkSpace_Y)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_start_6.addWidget(self.label_8)
        self.gridLayout_3.addLayout(self.horizontalLayout_start_6, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem2, 0, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem3, 2, 0, 1, 1)
        self.horizontalLayout_start_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_start_5.setObjectName("horizontalLayout_start_5")
        self.checkBox_electric_y = QtGui.QCheckBox(self.groupBox_WorkSpace_Y)
        self.checkBox_electric_y.setObjectName("checkBox_electric_y")
        self.horizontalLayout_start_5.addWidget(self.checkBox_electric_y)
        self.LineEdit_electric_y = QtGui.QTextEdit(self.groupBox_WorkSpace_Y)
        self.LineEdit_electric_y.setMaximumSize(QtCore.QSize(16777215, 60))
        self.LineEdit_electric_y.setObjectName("LineEdit_electric_y")
        self.horizontalLayout_start_5.addWidget(self.LineEdit_electric_y)
        self.label_5 = QtGui.QLabel(self.groupBox_WorkSpace_Y)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_start_5.addWidget(self.label_5)
        self.gridLayout_3.addLayout(self.horizontalLayout_start_5, 3, 0, 1, 1)
        spacerItem4 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_3.addItem(spacerItem4, 4, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_WorkSpace_Y, 1, 0, 1, 1)
        self.groupBox_WorkSpace_Z = QtGui.QGroupBox(Dialog_FieldSettingDlg)
        self.groupBox_WorkSpace_Z.setObjectName("groupBox_WorkSpace_Z")
        self.gridLayout = QtGui.QGridLayout(self.groupBox_WorkSpace_Z)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem5 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 0, 0, 1, 1)
        spacerItem6 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem6, 2, 0, 1, 1)
        self.horizontalLayout_end_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_end_7.setObjectName("horizontalLayout_end_7")
        self.textEdit_filed_custom = QtGui.QTextEdit(self.groupBox_WorkSpace_Z)
        self.textEdit_filed_custom.setObjectName("textEdit_filed_custom")
        self.horizontalLayout_end_7.addWidget(self.textEdit_filed_custom)
        self.gridLayout.addLayout(self.horizontalLayout_end_7, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_WorkSpace_Z, 2, 0, 1, 1)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem7)
        self.pushButton_ok = QtGui.QPushButton(Dialog_FieldSettingDlg)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout_10.addWidget(self.pushButton_ok)
        self.gridLayout_4.addLayout(self.horizontalLayout_10, 3, 0, 1, 1)

        self.retranslateUi(Dialog_FieldSettingDlg)
        QtCore.QMetaObject.connectSlotsByName(Dialog_FieldSettingDlg)

    def retranslateUi(self, Dialog_FieldSettingDlg):
        Dialog_FieldSettingDlg.setWindowTitle(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "场设置", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_WorkSpace_X.setTitle(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "静磁场设置", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_magenetic_x.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "X方向FBXST(X,Y,Z)=", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_magenetic_x.setHtml(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.0</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "Tesla", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_magenetic_y.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "Y方向FBXST(X,Y,Z)=", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_magenetic_y.setHtml(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.0</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "Tesla", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_WorkSpace_Y.setTitle(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "静电场设置", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_electric_x.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "X方向FBXST(X,Y,Z)=", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_electric_x.setHtml(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.0</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "V/m", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_electric_y.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "Y方向FBXST(X,Y,Z)=", None, QtGui.QApplication.UnicodeUTF8))
        self.LineEdit_electric_y.setHtml(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">0.0</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "V/m", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_WorkSpace_Z.setTitle(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "场自定义", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit_filed_custom.setHtml(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_ok.setText(QtGui.QApplication.translate("Dialog_FieldSettingDlg", "确定", None, QtGui.QApplication.UnicodeUTF8))

