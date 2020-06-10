# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FileTextEditor.ui'
#
# Created: Mon Jan 21 16:38:07 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_TextEditor(object):
    def setupUi(self, TextEditor):
        TextEditor.setObjectName("TextEditor")
        TextEditor.resize(423, 426)
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.gridLayout = QtGui.QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName("gridLayout")
        self.textEdit = QtGui.QTextEdit(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 0, 0, 1, 1)
        TextEditor.setWidget(self.dockWidgetContents)

        self.retranslateUi(TextEditor)
        QtCore.QMetaObject.connectSlotsByName(TextEditor)

    def retranslateUi(self, TextEditor):
        TextEditor.setWindowTitle(QtGui.QApplication.translate("TextEditor", "File Text Editor", None, QtGui.QApplication.UnicodeUTF8))

