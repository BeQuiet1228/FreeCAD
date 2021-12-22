# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TreeStructPal.ui'
#
# Created: Fri Nov 01 20:19:13 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DockWidget_plotTree(object):
    def setupUi(self, DockWidget_plotTree):
        DockWidget_plotTree.setObjectName("DockWidget_plotTree")
        DockWidget_plotTree.setWindowModality(QtCore.Qt.NonModal)
        DockWidget_plotTree.resize(369, 442)
        DockWidget_plotTree.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        DockWidget_plotTree.setAcceptDrops(False)
        DockWidget_plotTree.setAutoFillBackground(False)
        DockWidget_plotTree.setInputMethodHints(QtCore.Qt.ImhNone)
        DockWidget_plotTree.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        DockWidget_plotTree.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        DockWidget_plotTree.setWindowTitle("")
        self.dockWidget_plotTree = QtGui.QWidget()
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        self.dockWidget_plotTree.setPalette(palette)
        self.dockWidget_plotTree.setAutoFillBackground(True)
        self.dockWidget_plotTree.setObjectName("dockWidget_plotTree")
        self.gridLayout = QtGui.QGridLayout(self.dockWidget_plotTree)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget_plotTree = QtGui.QTreeWidget(self.dockWidget_plotTree)
        self.treeWidget_plotTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_plotTree.setObjectName("treeWidget_plotTree")
        self.gridLayout.addWidget(self.treeWidget_plotTree, 0, 0, 1, 1)
        DockWidget_plotTree.setWidget(self.dockWidget_plotTree)

        self.retranslateUi(DockWidget_plotTree)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_plotTree)

    def retranslateUi(self, DockWidget_plotTree):
        self.treeWidget_plotTree.headerItem().setText(0, QtGui.QApplication.translate("DockWidget_plotTree", "分类", None, QtGui.QApplication.UnicodeUTF8))

