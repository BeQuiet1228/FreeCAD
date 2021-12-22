# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TreeStructPal.ui'
#
# Created: Fri Nov 01 20:17:35 2019
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_DockWidget_resultTree(object):
    def setupUi(self, DockWidget_resultTree):
        DockWidget_resultTree.setObjectName("DockWidget_resultTree")
        DockWidget_resultTree.setWindowModality(QtCore.Qt.NonModal)
        DockWidget_resultTree.resize(369, 442)
        DockWidget_resultTree.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        DockWidget_resultTree.setAcceptDrops(False)
        DockWidget_resultTree.setAutoFillBackground(False)
        DockWidget_resultTree.setInputMethodHints(QtCore.Qt.ImhNone)
        DockWidget_resultTree.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        DockWidget_resultTree.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        DockWidget_resultTree.setWindowTitle("")
        self.dockWidget_resultFig = QtGui.QWidget()
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
        self.dockWidget_resultFig.setPalette(palette)
        self.dockWidget_resultFig.setAutoFillBackground(True)
        self.dockWidget_resultFig.setObjectName("dockWidget_resultFig")
        self.gridLayout = QtGui.QGridLayout(self.dockWidget_resultFig)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget_resultFig = QtGui.QTreeWidget(self.dockWidget_resultFig)
        self.treeWidget_resultFig.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_resultFig.setObjectName("treeWidget_resultFig")
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_1 = QtGui.QTreeWidgetItem(item_0)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        item_0 = QtGui.QTreeWidgetItem(self.treeWidget_resultFig)
        self.gridLayout.addWidget(self.treeWidget_resultFig, 0, 0, 1, 1)
        DockWidget_resultTree.setWidget(self.dockWidget_resultFig)

        self.retranslateUi(DockWidget_resultTree)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_resultTree)

    def retranslateUi(self, DockWidget_resultTree):
        self.treeWidget_resultFig.headerItem().setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "分类", None, QtGui.QApplication.UnicodeUTF8))
        __sortingEnabled = self.treeWidget_resultFig.isSortingEnabled()
        self.treeWidget_resultFig.setSortingEnabled(False)
        self.treeWidget_resultFig.topLevelItem(0).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "等位图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(0).child(0).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "二维等位图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(0).child(1).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "三维等位图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(1).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "时间变化图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(2).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "相空间图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(3).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "空间变化图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(4).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "矢量图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(4).child(0).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "二维矢量图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(4).child(1).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "三维矢量图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(5).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "三维立体图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(6).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "剖面结构图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.topLevelItem(7).setText(0, QtGui.QApplication.translate("DockWidget_resultTree", "三维粒子图", None, QtGui.QApplication.UnicodeUTF8))
        self.treeWidget_resultFig.setSortingEnabled(__sortingEnabled)

