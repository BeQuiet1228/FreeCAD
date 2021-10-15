# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

class Ui_DockWidget_boundSettingTree(object):
    def setupUi(self, DockWidget_boundSettingTree):
        DockWidget_boundSettingTree.setObjectName("DockWidget_boundSettingTree")
        DockWidget_boundSettingTree.setWindowModality(QtCore.Qt.NonModal)
        DockWidget_boundSettingTree.resize(369, 442)
        DockWidget_boundSettingTree.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        DockWidget_boundSettingTree.setAcceptDrops(False)
        DockWidget_boundSettingTree.setAutoFillBackground(False)
        DockWidget_boundSettingTree.setInputMethodHints(QtCore.Qt.ImhNone)
        DockWidget_boundSettingTree.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        DockWidget_boundSettingTree.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        DockWidget_boundSettingTree.setWindowTitle("")
        self.dockWidget_boundSettingTree = QtGui.QWidget()
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
        self.dockWidget_boundSettingTree.setPalette(palette)
        self.dockWidget_boundSettingTree.setAutoFillBackground(True)
        self.dockWidget_boundSettingTree.setObjectName("dockWidget_boundSettingTree")
        self.treeWidget_boundSettingTree = QtGui.QTreeWidget(self.dockWidget_boundSettingTree)
        self.treeWidget_boundSettingTree.setGeometry(QtCore.QRect(10, 10, 351, 381))
        self.treeWidget_boundSettingTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_boundSettingTree.setObjectName("treeWidget_boundSettingTree")

        # 将树形目录设置为随外边框拉伸
        self.gridLayout = QtGui.QGridLayout(self.dockWidget_boundSettingTree)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.treeWidget_boundSettingTree, 0, 0, 1, 1)

        DockWidget_boundSettingTree.setWidget(self.dockWidget_boundSettingTree)

        self.retranslateUi(DockWidget_boundSettingTree)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_boundSettingTree)

    def retranslateUi(self, DockWidget_boundSettingTree):
        self.treeWidget_boundSettingTree.headerItem().setText(0, QtGui.QApplication.translate("DockWidget_boundSettingTree", "分类", None, QtGui.QApplication.UnicodeUTF8))

