# -*- coding: utf-8 -*-

from PySide import QtCore, QtGui

class Ui_DockWidget_observeSettingTree(object):
    def setupUi(self, DockWidget_observeSettingTree):
        DockWidget_observeSettingTree.setObjectName("DockWidget_observeSettingTree")
        DockWidget_observeSettingTree.setWindowModality(QtCore.Qt.NonModal)
        DockWidget_observeSettingTree.resize(369, 442)
        DockWidget_observeSettingTree.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        DockWidget_observeSettingTree.setAcceptDrops(False)
        DockWidget_observeSettingTree.setAutoFillBackground(False)
        DockWidget_observeSettingTree.setInputMethodHints(QtCore.Qt.ImhNone)
        DockWidget_observeSettingTree.setFeatures(QtGui.QDockWidget.NoDockWidgetFeatures)
        DockWidget_observeSettingTree.setAllowedAreas(QtCore.Qt.NoDockWidgetArea)
        DockWidget_observeSettingTree.setWindowTitle("")
        self.dockWidget_observeSettingTree = QtGui.QWidget()
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
        self.dockWidget_observeSettingTree.setPalette(palette)
        self.dockWidget_observeSettingTree.setAutoFillBackground(True)
        self.dockWidget_observeSettingTree.setObjectName("dockWidget_observeSettingTree")
        self.treeWidget_observeSettingTree = QtGui.QTreeWidget(self.dockWidget_observeSettingTree)
        self.treeWidget_observeSettingTree.setGeometry(QtCore.QRect(10, 10, 351, 381))
        self.treeWidget_observeSettingTree.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_observeSettingTree.setObjectName("treeWidget_observeSettingTree")

        # 将树形目录设置为随外边框拉伸
        self.gridLayout = QtGui.QGridLayout(self.dockWidget_observeSettingTree)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.addWidget(self.treeWidget_observeSettingTree, 0, 0, 1, 1)

        DockWidget_observeSettingTree.setWidget(self.dockWidget_observeSettingTree)

        self.retranslateUi(DockWidget_observeSettingTree)
        QtCore.QMetaObject.connectSlotsByName(DockWidget_observeSettingTree)

    def retranslateUi(self, DockWidget_observeSettingTree):
        self.treeWidget_observeSettingTree.headerItem().setText(0, QtGui.QApplication.translate("DockWidget_observeSettingTree", "分类", None, QtGui.QApplication.UnicodeUTF8))

