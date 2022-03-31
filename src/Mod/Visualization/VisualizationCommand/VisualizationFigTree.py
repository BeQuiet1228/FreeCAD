# -*- coding: UTF-8 -*-

from PySide import QtGui, QtCore
from pylab import *
import os

import FreeCAD
import FreeCADGui
import vPlot
import VisualizationResult
import VisualizationPlot
import subprocess
import json

import LoadingMain
loading = LoadingMain.LoadingWidget()
loading.setWindowFlags(QtCore.Qt.FramelessWindowHint)
loading.setAttribute(QtCore.Qt.WA_TranslucentBackground)

class DisplayFigTree(QtGui.QDockWidget):
    def __init__(self, parent=None):
        super(DisplayFigTree, self).__init__(parent)
        self.ui = VisualizationGui.plotTree.TreeStructPal.Ui_DockWidget_plotTree()
        self.ui.setupUi(self)

        # 解决QTreeWidget中的内容超出边界后自动隐藏的问题
        self.ui.treeWidget_plotTree.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.treeWidget_plotTree.header().setStretchLastSection(False)
        self.ui.treeWidget_plotTree.setAutoScroll(False)

        # 去除标题栏
        self.setTitleBarWidget(QtGui.QWidget(None))

        app = QtGui.qApp
        aw = app.activeWindow()
        mw = FreeCADGui.getMainWindow()
        # 获取Combo View
        if mw:
            dw = mw.findChild(QtGui.QDockWidget, 'Combo View')
            # 获取Combo View 下的comiTab
            if dw:
                self.qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
                # 将结果目录作为一个tab添加到Combo View下
                # self.qtab.addTab(self, u'绘图结果')
                self.qtab.insertTab(self.qtab.count()-1, self, u'绘图结果')
                # 将树形目录设置为当前 Tab
                self.qtab.setCurrentWidget(self)
                tabBar = self.qtab.tabBar()
                tabBar.setTabButton(self.qtab.currentIndex(), QtGui.QTabBar.RightSide, None)
            else:
                sayz('combiTab is not found')
        else:
            sayz('Combo View is not found')
        self.treeIndex = self.qtab.indexOf(self)
        # 将结果目录作为一个活动面板添加到界面中
        # aw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
        self.ui.treeWidget_plotTree.itemClicked['QTreeWidgetItem*', 'int'].connect(self.onClick)
        mdi = vPlot.getMdiArea()
        mdi.subWindowActivated.connect(self.updateTreeNode)

    def onClick(self, item, column):
        fig, flag = vPlot.figure(True, item.text(0))
        # mdi = vPlot.getMdiArea()
        # subWindowList = mdi.subWindowList()
        # for subWindow in subWindowList:
        #     # 如果窗口名和item名一致则激活窗口
        #     if subWindow.windowTitle() == item.text(0):
        #         mdi.setActiveSubWindow(subWindow)

    # 设置与当前窗口匹配的树节点
    def updateTreeNode(self, subWindow):
        # subWindow非noneType
        if subWindow:
            subWindowName = subWindow.windowTitle()
            rootCount = self.ui.treeWidget_plotTree.topLevelItemCount()
            # 遍历所有的树节点
            for i in range(rootCount):
                rootItem = self.ui.treeWidget_plotTree.topLevelItem(i)
                secondCount = rootItem.childCount()
                for j in range(secondCount):
                    second = rootItem.child(j)
                    secondName = second.text(0)
                    thirdCount = second.childCount()
                    # 器件结构情况
                    if thirdCount == 0:
                        if secondName == subWindowName:
                            self.ui.treeWidget_plotTree.setCurrentItem(second)
                    else:
                        for k in range(thirdCount):
                            third = second.child(k)
                            thirdName = third.text(0)
                            if thirdName == subWindowName:
                                self.ui.treeWidget_plotTree.setCurrentItem(third)

    def show(self, *args, **kwargs):
        super(DisplayFigTree, self).show()
        self.setAutoFillBackground(True)

figTree = DisplayFigTree()
def showfigTree():
    mw = FreeCADGui.getMainWindow()
    # 获取Combo View
    if mw:
        dw = mw.findChild(QtGui.QDockWidget, 'Combo View')
        # 获取Combo View 下的comiTab
        if dw:
            tab = dw.findChild(QtGui.QTabWidget, 'combiTab')
        else:
            sayz('combiTab is not found')
    else:
        sayz('Combo View is not found')

    tab.setCurrentIndex(figTree.treeIndex)
    tree = figTree.ui.treeWidget_plotTree
    tree.clear()

    figTree.show()

    # 添加根节点
    # 对应饿rootIndex依次为0，1，2，3，4，5
    addChild(figTree.ui, u"二维等位图")
    addChild(figTree.ui, u"相空间图")
    addChild(figTree.ui, u"时间观测图")
    addChild(figTree.ui, u"器件结构图")
    addChild(figTree.ui, u"二维矢量图")
    addChild(figTree.ui, u"空间变化图")

def addChild(tree, itemName):
    item = QtGui.QTreeWidgetItem()
    item.setText(0, itemName)
    item.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Group.svg"))
    tree.treeWidget_plotTree.addTopLevelItem(item)

def getItemDataByfigName(figName,rootIndex):
    """
    用来根据figName得到其对应的item的ItemData
    itemData: [index,order,figName]
            len(index)，为1时，代表次节点，index为所在根节点指数；
                        为2时，代表item，index[0]所在根节点指数，index[1]为所在次结点指数
            order：为0时，代表次结点，为1时，代表item，为同一figName的序号
            figName:图名
    """
    FreeCAD.Console.PrintMessage("getItemDataByfigName +++++++++++++++++++++++++++++++++ \n")
    # 遍历rootIndex对应根节点下所有的子节点
    rootItem = figTree.ui.treeWidget_plotTree.topLevelItem(rootIndex)
    # 获得该根节点下的所有子结点数
    subCount = rootItem.childCount()
    index = [rootIndex]
    FreeCAD.Console.PrintMessage("getItemDataByfigName +++++++++++++++++++++++++++++++++ \n")
    # 存放该figName的所有序号
    orderList = []
    for j in range(subCount):
        # 得到第二级的item
        subItem = rootItem.child(j)
        # 得到该item对应的itemData
        subItemdata = subItem.data(0, QtCore.Qt.UserRole)
        # 根据图名确定在该次结点下
        if figName ==  subItemdata[2]:
            # 在index中加入次结点指数
            index.append(j)
            # 得到该次结点的子结点数
            thirdCount = subItem.childCount()
            for k in range(thirdCount):
                third = subItem.child(k)
                thirdItemdata = third.data(0, QtCore.Qt.UserRole)
                # 得到该次结点下所有item的order
                orderList.append(int(thirdItemdata[1]))
    FreeCAD.Console.PrintMessage("getItemDataByfigName +++++++++++++++++++++++++++++++++ \n")
    if orderList !=[]:
        order = max(orderList)
    else:
        order = 0
    FreeCAD.Console.PrintMessage("getItemDataByfigName +++++++++++++++++++++++++++++++++ \n")
    itemData = [index,order,figName]
    return itemData

def addSubChild(itemName, itemData):
    """
    用来添加次结点或item
    :param tree:
    :param itemName:
    :param itemData: [index,order,figName]
            len(index)，为1时，代表次节点，index为所在根节点指数；
                        为2时，代表item，index[0]所在根节点指数，index[1]为所在次结点指数
            order：为0时，代表次结点，为1时，代表item，为同一figName的序号
            figName:图名
    :return:
    """
    item = QtGui.QTreeWidgetItem()
    # 之前没有绘过这类图，即没有该图的次结点
    if len(itemData[0]) == 1:
        # 得到根节点指数
        rootIndex = itemData[0][0]
        # 添加次结点
        item.setData(0, QtCore.Qt.UserRole, itemData)
        item.setText(0, itemName)
        figTree.ui.treeWidget_plotTree.topLevelItem(rootIndex).addChild(item)
        # 添加次结点下item
        subitem = QtGui.QTreeWidgetItem()
        # 根据item获取其指数
        subindex = figTree.ui.treeWidget_plotTree.topLevelItem(rootIndex).indexOfChild(item)
        data = [[rootIndex,subindex],1,itemName]
        subitem.setData(0, QtCore.Qt.UserRole, data)
        subitem.setText(0, str(itemName)+"_1")
        figTree.ui.treeWidget_plotTree.topLevelItem(rootIndex).child(subindex).addChild(subitem)
    # 之前绘过这类图，order+1，新添一个item
    elif len(itemData[0]) == 2:
        rootIndex = itemData[0][0]
        subindex = itemData[0][1]
        data = itemData
        # 将得到的order加1
        data[1] = itemData[1]+1
        item.setData(0, QtCore.Qt.UserRole, data)
        item.setText(0, str(itemName)+"_"+str(data[1]))
        figTree.ui.treeWidget_plotTree.topLevelItem(rootIndex).child(subindex).addChild(item)

def addStrcutItem(itemName,rootIndex):
    """
    由于器件结构没有次结点，这个函数单独添加
    :param itemName:
    :param rootIndex: 根节点指数
    :return:
    """
    item = QtGui.QTreeWidgetItem()
    item.setText(0, itemName)
    figTree.ui.treeWidget_plotTree.topLevelItem(rootIndex).addChild(item)

def removeTreeNode(subWindow):
    """
    删除subWindow时删除对应树结构中item
    :param subWindow:
    :return:
    """
    # subWindow非noneType
    if subWindow:
        subWindowName = subWindow.windowTitle()
        rootCount = figTree.ui.treeWidget_plotTree.topLevelItemCount()
        # 遍历所有的树节点
        for i in range(rootCount):
            rootItem = figTree.ui.treeWidget_plotTree.topLevelItem(i)
            secondCount = rootItem.childCount()
            for j in range(secondCount):
                second = rootItem.child(j)
                secondName = second.text(0)
                thirdCount = second.childCount()
                # 器件结构情况
                if thirdCount == 0:
                    if secondName == subWindowName:
                        rootItem.removeChild(second)
                else:
                    for k in range(thirdCount):
                        third = second.child(k)
                        thirdName = third.text(0)
                        if thirdName == subWindowName:
                            second.removeChild(third)
                            # 为1时将第二层也删除
                            if thirdCount == 1:
                                rootItem.removeChild(second)

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')

def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')