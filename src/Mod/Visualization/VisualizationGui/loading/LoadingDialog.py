# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LoadingDialog.ui'
#
# Created: Mon Apr  1 21:22:46 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Dialog_loading(object):
    def setupUi(self, Dialog_loading):
        Dialog_loading.setObjectName("Dialog_loading")
        Dialog_loading.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog_loading.resize(152, 152)
        self.label_pic = QtGui.QLabel(Dialog_loading)
        self.label_pic.setGeometry(QtCore.QRect(30, 10, 100, 100))
        self.label_pic.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_pic.setAlignment(QtCore.Qt.AlignCenter)
        self.label_pic.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_pic.setObjectName("label_pic")
        self.label = QtGui.QLabel(Dialog_loading)
        self.label.setGeometry(QtCore.QRect(10, 120, 131, 20))
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(False)
        self.label.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label.setObjectName("label")

        self.retranslateUi(Dialog_loading)
        QtCore.QMetaObject.connectSlotsByName(Dialog_loading)

    def retranslateUi(self, Dialog_loading):
        Dialog_loading.setWindowTitle(QtGui.QApplication.translate("Dialog_loading", "Loading...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_pic.setText(QtGui.QApplication.translate("Dialog_loading", "pic ", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog_loading", "<html><head/><body><p><span style=\" font-weight:600; color:#3a7fff;\">正在处理，请稍后...</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

