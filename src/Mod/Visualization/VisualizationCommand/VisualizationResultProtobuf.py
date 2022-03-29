# -*- coding: UTF-8 -*-

import sys
import os
import json
#  修改str 的默认编码格式，由 ascii 改为 utf8
reload(sys)
sys.setdefaultencoding('utf8')

from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
from pylab import *

import FreeCAD
import FreeCADGui
import VisualizationGui
import VisualizationPlot
import vPlot
import data_pb2
import numpy as np


count = 0
class FigTree(QDockWidget):
    def __init__(self, parent=None):
        super(FigTree, self).__init__(parent)
        self.ui = VisualizationGui.TreeStructPal.Ui_DockWidget_resultTree()
        self.ui.setupUi(self)

        # 解决QTreeWidget中的内容超出边界后自动隐藏的问题
        self.ui.treeWidget_resultFig.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.treeWidget_resultFig.header().setStretchLastSection(False)
        self.ui.treeWidget_resultFig.setAutoScroll(False)

        # 设置每一个项的图标
        topLevelCount=self.ui.treeWidget_resultFig.topLevelItemCount()
        for i in range(topLevelCount):
            topLevelItem=self.ui.treeWidget_resultFig.topLevelItem(i)
            topLevelItem.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Group.svg"))
            childCount1=topLevelItem.childCount()
            for j in range(childCount1):
                child1=topLevelItem.child(j)
                child1.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Item.svg"))
                childCount2=child1.childCount()
                for k in range(childCount2):
                    child2=child1.child(k)
                    child2.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Item.svg"))

        # 去除标题栏
        self.setTitleBarWidget(QtGui.QWidget(None))

        global count
        app = QtGui.qApp
        aw = app.activeWindow()
        mw = FreeCADGui.getMainWindow()
        # 获取Combo View
        if mw:
            dw = mw.findChild(QtGui.QDockWidget, 'Combo View')
            # 获取Combo View 下的comiTab
            if dw:
                qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
                # 将结果目录作为一个tab添加到Combo View下
                if count == 0:
                    # qtab.addTab(self, u'导入结果')
                    qtab.insertTab(qtab.count()-1, self, u'导入结果')
                else:
                    # qtab.addTab(self, u'导入结果' + str(count))
                    qtab.insertTab(qtab.count()-1, self, u'导入结果' + str(count))
                count += 1
                qtab.setCurrentWidget(self)
            else:
                FreeCAD.Console.PrintMessage('combiTab is not found\n')
        else:
            FreeCAD.Console.PrintMessage('Combo View is not found\n')
        # 将结果目录作为一个活动面板添加到界面中
        # aw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
        self.ui.treeWidget_resultFig.itemClicked['QTreeWidgetItem*', 'int'].connect(self.onClick)
        mdi = vPlot.getMdiArea()
        mdi.subWindowActivated.connect(self.updateTreeNode)

    def onClick(self, item, column):
        # 添加shade选项
        self.createContextMenu(item)
        mdi = vPlot.getMdiArea()
        # 获取当前节点对应的子窗口是否打开
        subWindow = isExisted(mdi, item, 'line')
        # 若存在该节点名称对应的子窗口，则激活该窗口，否则重建一个窗口，重绘图像
        if subWindow:
            mdi.setActiveSubWindow(subWindow)
        else:
            parent = item.parent()
            if parent is not None:
                parent = parent.text(0)
            data = item.data(0, QtCore.Qt.UserRole)
            if parent == u'二维等位图':
                x_label, y_label, time, component, range_start, range_end, range_min, range_max, step, figname = contourInfo(data)
                a, b, c = getData3(data)
                # 判断a、b、c的数据量关系是否符合要求
                assert len(c) == len(a) * len(b), 'contour: len(c) != len(a) * len(b)'
                # 新建一个窗口
                fig = vPlot.figure(figname)
                # 绘制等位图
                VisualizationPlot.drawContour(x_label, y_label, time, component, range_format(range_start),
                                              range_format(range_end), range_min, range_max, step, a, b, c, 'line')
            elif parent == u'二维等位图的三维展示':
                x_label, y_label, time, component, range_start, range_end, range_min, range_max, step, figname = contourInfo(data)
                a, b, c = getData3(data)
                # 判断a、b、c的数据量关系是否符合要求
                assert len(c) == len(a) * len(b), 'contour: len(c) != len(a) * len(b)'
                # 新建一个窗口
                figname = figname + '3D'
                fig = vPlot.figure(figname)
                # 绘制等位图
                VisualizationPlot.drawContour3D(x_label, y_label, time, component, range_format(range_start),
                                              range_format(range_end), range_min, range_max, step, a, b, c)
            elif parent == u'时间变化图':
                x_label, y_label, type, range_min, range_max, figname = observeInfo(data)
                x, y = getData2(data)
                fig = vPlot.figure(figname)
                VisualizationPlot.drawObserve(x_label, y_label, type, range_format(range_min), range_format(range_max), x, y)
            elif parent == u'相空间图':
                x_label, y_label, particle, time, figname = phasespaceInfo(data)
                data = data.data_lists[0]
                dim = data.dim
                size = len(data.list)
                data = np.array(data.list).reshape(dim,int(size/dim))
                x = data[0]
                y = data[1]
                z = data[2]
                fig = vPlot.figure(figname)
                VisualizationPlot.drawPhasespace(x_label, y_label, particle, time, x, y,z)
            elif parent == u'空间变化图':
                x_label, y_label, time, component, range_min, range_max, figname = rangeInfo(data)
                x, y = getData2(data)
                fig = vPlot.figure(figname)
                VisualizationPlot.drawRange(x_label, y_label, time, component, range_format(range_min), range_format(range_max), x, y)
            elif parent == u'二维矢量图':
                x_label, y_label, component, time, cut_position, max_vector, figname = vectorInfo(data)
                a, b, c = getData3(data)
                # 判断a、b、c的数据量关系是否符合要求
                assert len(c) == 2 * len(a) * len(b), 'vector: len(c) != 2 * len(a) * len(b)'
                fig = vPlot.figure(figname)
                VisualizationPlot.drawVector(x_label, y_label, component, time, cut_position, max_vector, a, b, c)
            elif parent == u'三维等位图':
                # h5文件路径
                filename = data[0]
                # data所在分组
                figname = data[1][0]

                # 获取Mod文件夹路径
                file_path = os.path.dirname(__file__)
                exe_path = os.path.dirname(os.path.dirname(file_path))

                # 传文件路径绘图
                os.popen(exe_path + '\\Visualization\\vPlot3DProtobuf\\Vis3DProto.exe ' + filename + ' CONTOUR3D ' + figname).read()

            elif parent == u'三维矢量图':
                # h5文件路径
                filename = data[0]
                # 三维矢量图名字和三个data所在分组
                figname = data[1] + '/'+ data[2][0][0] + '/'+data[2][1][0] + '/' + data[2][2][0]

                # 获取Mod文件夹路径
                file_path = os.path.dirname(__file__)
                exe_path = os.path.dirname(os.path.dirname(file_path))

                # 传文件路径绘图
                os.popen(exe_path + '\\Visualization\\vPlot3DProtobuf\\Vis3DProto.exe ' + filename + ' VECTOR3D ' + figname).read()

    # 创建菜单
    def createContextMenu(self, item):
        parent = item.parent()
        if parent is not None:
            parent = parent.text(0)
        datapath = item.data(0, QtCore.Qt.UserRole)
        if parent == u'二维等位图':
            self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            # 创建QMenu
            self.contextMenu = QtGui.QMenu(self)
            self.actionA = self.contextMenu.addAction('Show shade')
            # 将动作与处理函数相关联, 使用lambda可以传递额外的参数
            self.actionA.triggered.connect(lambda: self.showShade(item))
            self.contextMenu.move(QtGui.QCursor().pos())
            self.contextMenu.show()

    # 绘制contour shade
    def showShade(self, item):
        mdi = vPlot.getMdiArea()
        subWindow = isExisted(mdi, item, 'shade')
        if subWindow:
            mdi.setActiveSubWindow(subWindow)
        else:
            datapath = item.data(0, QtCore.Qt.UserRole)
            x_label, y_label, time, component, range_start, range_end, range_min, range_max, step, figname = contourInfo(datapath)
            a, b, c = getData3(datapath)
            # 判断a、b、c的数据量关系是否符合要求
            assert len(c) == len(a) * len(b), 'contour: len(c) != len(a) * len(b)'
            figname = figname + '_Shade'
            fig = vPlot.figure(figname)
            VisualizationPlot.drawContour(x_label, y_label, time, component, range_format(range_start), range_format(range_end), range_min, range_max, step, a, b, c, 'shade')

    # 设置与当前窗口匹配的树节点
    def updateTreeNode(self, subWindow):
        # subWindow非noneType
        if subWindow:
            subWindowName = subWindow.windowTitle()
            rootCount = self.ui.treeWidget_resultFig.topLevelItemCount()
            # 遍历所有的树节点
            for i in range(rootCount):
                rootItem = self.ui.treeWidget_resultFig.topLevelItem(i)
                secondCount = rootItem.childCount()
                for j in range(secondCount):
                    second = rootItem.child(j)
                    secondName = second.text(0)
                    thirdCount = second.childCount()
                    if thirdCount == 0:
                        if secondName == subWindowName:
                            self.ui.treeWidget_resultFig.setCurrentItem(second)
                    else:
                        for k in range(thirdCount):
                            third = second.child(k)
                            thirdName = third.text(0)
                            if thirdName == subWindowName or thirdName+'_Shade' == subWindowName:
                                self.ui.treeWidget_resultFig.setCurrentItem(third)

    def show(self, *args, **kwargs):
        super(FigTree, self).show()
        self.setAutoFillBackground(True)


# path: json格式的h5文件路径
def showResultTree(target, filename):
    # 显示树形结构
    tree = FigTree()
    tree.show()
    vector3dNameList = []

    # 读取数据
    for everydata in target.data:
        # 二维等位图
        if everydata.type == 0:
            # 获取等位图的附加信息
            x_label, y_label, time, component, range_start, range_end, range_min, range_max, step, figname = contourInfo(
                everydata)
            # 树形目录添加子节点
            addChild(tree.ui, [0, 0], figname, everydata)
            addChild(tree.ui, [0, 1], figname + '3D', everydata)
        # 三维等位图
        elif everydata.type == 5:
            # 获取图的名称
            figname = contour3DInfo(everydata)
            # 将h5文件名和subgroup名记录在树节点中
            arg = [filename, everydata.location]
            # 树形目录添加子节点
            addChild(tree.ui, [0, 2], figname, arg)
        # 时间变化图
        elif everydata.type == 1:
            # 获取时间变化图的附加信息
            x_label, y_label, type, range_min, range_max, figname = observeInfo(everydata)
            # 添加子节点
            addChild(tree.ui, 1, figname, everydata)
        # 相空间图
        elif everydata.type == 2:
            x_label, y_label, particle, time, figname = phasespaceInfo(everydata)
            addChild(tree.ui, 2, figname, everydata)
        # 空间变化图
        elif everydata.type == 3:
            x_label, y_label, time, component, range_min, range_max, figname = rangeInfo(everydata)
            addChild(tree.ui, 3, figname, everydata)
        # 二维矢量图
        elif everydata.type == 4:
            x_label, y_label, component, time, cut_position, max_vector, figname = vectorInfo(everydata)
            addChild(tree.ui, [4, 0], figname, everydata)
        # 三维等位图
        elif everydata.type == 6:
            if everydata.id not in vector3dNameList:
                vector3dNameList.append(everydata.id)
                # 获取图的名称
                figname, vector3dLocations = vector3DInfo(target.data, everydata)
                # 将h5文件名和subgroup名记录在树节点中
                arg = [filename, figname, vector3dLocations]
                if len(vector3dLocations) == 3:
                    # 树形目录添加子节点
                    addChild(tree.ui, [4, 1], figname, arg)
    # binaryFilePath = filename[:-3]
    # try:
    #     f = open(binaryFilePath, "rb")
    #     target = data_pb2.allData()
    #     target.ParseFromString(f.read())
    #     vector3dNameList = []
    #
    #     # 读取数据
    #     for everydata in target.data:
    #         # 二维等位图
    #
    #         if everydata.type == 0:
    #
    #             # 获取等位图的附加信息
    #             x_label, y_label, time, component, range_start, range_end, range_min, range_max, step, figname = contourInfo(everydata)
    #
    #             # 树形目录添加子节点
    #             addChild(tree.ui, [0, 0], figname, everydata)
    #             addChild(tree.ui, [0, 1], figname + '3D', everydata)
    #
    #             # 根据subgroup目录下的文件数判断是否是三维等位图
    #             # sayz(os.path.basename(root))
    #             # if len([name for name in os.listdir(root) if os.path.isfile(os.path.join(root, name))]) == 1:
    #             #     # 当前路径的文件名
    #             #     dirname = os.path.basename(root)
    #             #     # 将h5文件名和subgroup名记录在树节点中
    #             #     arg = [filename, dirname]
    #             #     addChild(tree.ui, [0, 2], dirname, arg)
    #
    #             # # 获取等位图的数据
    #             # a, b, c = getData3(root)
    #             # # 判断a、b、c的数据量关系是否符合要求
    #             # assert len(c) == len(a) * len(b), 'contour: len(c) != len(a) * len(b)'
    #             # # 新建一个窗口
    #             # fig = vPlot.figure(figname)
    #             # # 绘制等位图
    #             # VisualizationPlot.drawContour(x_label, y_label, time, component, range_format(range_start),
    #             #                                   range_format(range_end), range_min, range_max, step, a, b, c)
    #
    #         # 三维等位图
    #         elif everydata.type == 5:
    #
    #             # 获取图的名称
    #             figname = contour3DInfo(everydata)
    #             # 将h5文件名和subgroup名记录在树节点中
    #             arg = [filename, everydata.location]
    #             # 树形目录添加子节点
    #             addChild(tree.ui, [0, 2], figname, arg)
    #
    #         # 时间变化图
    #         elif everydata.type == 1:
    #             # 获取时间变化图的附加信息
    #             x_label, y_label, type, range_min, range_max, figname = observeInfo(everydata)
    #             # 添加子节点
    #             addChild(tree.ui, 1, figname, everydata)
    #             # # 获取时间变化图的数据
    #             # x, y = getData2(root, 'dsetGrd.json')
    #             # fig = vPlot.figure(figname)
    #             # VisualizationPlot.drawObserve(x_label, y_label, type, range_format(range_min), range_format(range_max), x, y)
    #         # 相空间图
    #         elif everydata.type == 2:
    #             x_label, y_label, particle, time, figname = phasespaceInfo(everydata)
    #             addChild(tree.ui, 2, figname, everydata)
    #             # x, y = getData2(root, 'dsetPar.json')
    #             # fig = vPlot.figure(figname)
    #             # VisualizationPlot.drawPhasespace(x_label, y_label, particle, time, x, y)
    #         # 空间变化图
    #         elif everydata.type == 3:
    #             x_label, y_label, time, component, range_min, range_max, figname = rangeInfo(everydata)
    #             addChild(tree.ui, 3, figname, everydata)
    #             # x, y = getData2(root, 'dsetGrd.json')
    #             # fig = vPlot.figure(figname)
    #             # VisualizationPlot.drawRange(x_label, y_label, time, component, range_format(range_min), range_format(range_max), x, y)
    #         # 二维矢量图
    #         elif everydata.type == 4:
    #
    #             x_label, y_label, component, time, cut_position, max_vector, figname = vectorInfo(everydata)
    #
    #             addChild(tree.ui, [4, 0], figname, everydata)
    #
    #             # a, b, c = getData3(root)
    #             # # 判断a、b、c的数据量关系是否符合要求
    #             # assert len(c) == 2 * len(a) * len(b), 'vector: len(c) != 2 * len(a) * len(b)'
    #             # fig = vPlot.figure(figname)
    #             # VisualizationPlot.drawVector(x_label, y_label, component, time, cut_position, max_vector, a, b, c)
    #
    #         # 三维等位图
    #         elif everydata.type == 6:
    #             if everydata.id not in vector3dNameList:
    #                 vector3dNameList.append(everydata.id)
    #                 # 获取图的名称
    #                 figname, vector3dLocations = vector3DInfo(target.data, everydata)
    #
    #                 # 将h5文件名和subgroup名记录在树节点中
    #                 arg = [filename, figname, vector3dLocations]
    #                 # sayz(vector3dLocations)
    #                 if len(vector3dLocations) == 3:
    #                     # 树形目录添加子节点
    #                     addChild(tree.ui, [4, 1], figname, arg)
    #     f.close()
    #
    # except IOError:
    #     sayz ("Could not open file.Creating a new one.")


# 判断树节点对应的图像窗口是否打开
def isExisted(mdi, treeItem, tag):
    subWindowList = mdi.subWindowList()
    for subWindow in subWindowList:
        if tag == 'line'and subWindow.windowTitle() == treeItem.text(0):
            # print treeItem.data(0, QtCore.Qt.UserRole)
            sayz(treeItem.text(0))
            return subWindow
        elif tag == 'shade' and subWindow.windowTitle() == treeItem.text(0)+'_Shade':
            sayz(treeItem.text(0)+'_Shade')
            return subWindow
    return False

# 添加子节点
def addChild(tree, level, itemName, itemData):
    item = QtGui.QTreeWidgetItem()
    item.setText(0, itemName)
    item.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Item.svg"))
    # 树节点存放路径
    item.setData(0, QtCore.Qt.UserRole, itemData)
    if type(level) != list:
        tree.treeWidget_resultFig.topLevelItem(level).addChild(item)
    else:
        tree.treeWidget_resultFig.topLevelItem(level[0]).child(level[1]).addChild(item)

# 读取等位图的信息
def contourInfo(contourdata):
    x_label, y_label, time, component, range_start, range_end, range_min, range_max, step = '','','','','','','','',''
    attribute = contourdata.attributes.attribute
    location = contourdata.location[0]
    # x轴标注
    if 'attr9' in attribute:
        x_label = attribute['attr9']
    else:
        sayz( 'no attr9 in ' + location)
    # y轴标注
    if 'attr11' in attribute:
        y_label = attribute['attr11']
    else:
        sayz( 'no attr11 in ' + location)
    # 观察时间
    if 'attr13' in attribute:
        attr13 = attribute['attr13']
        time = attr13.split('TIME', 1)[1].replace("SEC", "").replace(" ", "")
    else:
        sayz( 'no attr13 in ' + location)
    # 观察分量
    if 'attr15' in attribute:
        attr15 = attribute['attr15'].split(' ', 3)
        component = attr15[1] + attr15[3]
    else:
        sayz( 'no attr15 in ' + location)
    # 等值区域
    if 'attr17' in attribute:
        attr17 = attribute['attr17'].split(' ', 4)
        range_start = attr17[2]
        range_end = attr17[4]
    else:
        sayz( 'no attr17 in ' + location)
    # 等值范围
    if 'attr19' in attribute:
        attr19 = attribute['attr19'].split(' ', 4)
        range_min = attr19[2]
        range_max = attr19[4]
    else:
        sayz( 'no attr19 in ' + location)
    # 等值步长
    if 'attr21' in attribute:
        attr21 = attribute['attr21'].split(' ', 3)
        step = attr21[3]
    else:
        sayz( 'not attr21 in ' + location)

    # 图像名
    figname = contourdata.location[0] + '_' + attr15[1]
    # 使用replace前先将unicode转str
    figname = figname.replace('Group_', '').replace('Group', '')
    return x_label, y_label, time, component, range_start, range_end, range_min, range_max, step, figname

# 读取时间变化图的信息
def observeInfo(observedata):
    x_label, y_label, type, range_min, range_max =  '','','','',''
    attribute = observedata.attributes.attribute
    location = observedata.location[0]
    # x轴标注
    if 'attr8' in attribute:
        x_label = attribute['attr8']
    else:
        sayz( 'no attr8 in ' + location)
    # y轴标注
    if 'attr10' in attribute:
        y_label = attribute['attr10']
    else:
        sayz( 'no attr10 in ' + location)
    # 观察类型
    if 'attr14' in attribute:
        attr14 = attribute['attr14']
        type = attr14.split('COMPONENT', 1)[0]
    else:
        sayz( 'no attr14 in ' + location)
    # 观察范围
    if 'attr16' in attribute:
        attr16 = attribute['attr16'].split(' ', 4)
        range_min = attr16[2]
        range_max = attr16[4]
    else:
        sayz( 'no attr16 in ' + location)
    # 图像名
    figname = observedata.location[0] + '_' + type
    # 使用replace前先将unicode转str
    figname = figname.replace('Group_', '').replace('Group', '')
    return x_label, y_label, type, range_min, range_max, figname

# 读取相空间图的信息
def phasespaceInfo(phasespacedata):
    x_label, y_label, particle, time = '','','',''
    attribute = phasespacedata.attributes.attribute
    location = phasespacedata.location[0]
    # x轴标注
    if 'attr8' in attribute:
        x_label = attribute['attr8']
    else:
        sayz( 'no attr8 in ' + location)
    # y轴标注
    if 'attr10' in attribute:
        y_label = attribute['attr10']
    else:
        sayz( 'no attr10 in ' + location)
    # 观察时间和粒子分量
    if 'attr14' in attribute:
        attr14 = attribute['attr14']
        frag_attr14 = attr14.split('OF', 1)[1]
        frag_attr14 = frag_attr14.split('AT', 1)[0]
        particle = frag_attr14.replace(' VS. ', '对')
        time = attr14.split(':', 1)[1].replace("SEC", "").replace(" ", "")
    else:
        sayz( 'no attr14 in ' + location)

    # 图像名
    figname = phasespacedata.location[0] + '_' + particle
    # 使用replace前先将unicode转str
    figname = figname.replace('Group_', '').replace('Group', '')
    return x_label, y_label, particle, time, figname

# 读取空间变化图的信息
def rangeInfo(rangedata):
    x_label, y_label, time, component, range_min, range_max = '','','','','',''
    attribute = rangedata.attributes.attribute
    location = rangedata.location[0]
    # x轴标注
    if 'attr8' in attribute:
        x_label = attribute['attr8']
    else:
        sayz( 'no attr8 in ' + location)
    # y轴标注
    if 'attr10' in attribute:
        y_label = attribute['attr10']
    else:
        sayz( 'no attr10 in ' + location)
    # 观察时间
    if 'attr12' in attribute:
        attr12 = attribute['attr12']
        time = attr12.split(':', 1)[1].replace("SEC", "").replace(" ", "")
    else:
        sayz( 'no attr12 in ' + location)
    # 分量曲线
    if 'attr14' in attribute:
        attr14 = attribute['attr14']
        component = attr14.split('COMPONENT', 1)[0]
    # 观察范围
    if 'attr16' in attribute:
        attr16 = attribute['attr16'].split(' ', 4)
        range_min = attr16[2]
        range_max = attr16[4]
    else:
        sayz( 'no attr16 in ' + location)

    # 图像名
    figname = rangedata.location[0] + '_' + component
    # 使用replace前先将unicode转str
    figname = figname.replace('Group_', '').replace('Group', '')
    return x_label, y_label, time, component, range_min, range_max, figname

def vectorInfo(vectordata):
    x_label, y_label, component, time, cut_position, max_vector = '','','','','',''
    attribute = vectordata.attributes.attribute
    location = vectordata.location[0]
    # x轴标注
    if 'attr8' in attribute:
        x_label = attribute['attr8']
    else:
        sayz('no attr8 in ' + location)
    # y轴标注
    if 'attr10' in attribute:
        y_label = attribute['attr10']
    else:
        sayz( 'no attr10 in ' + location)
    # 观察分量
    if 'attr12' in attribute:
        attr12 = attribute['attr12']
        component = attr12.split(' ', 3)[3].replace('(', '').replace(')', '').replace(',', '对')
    else:
        sayz( 'no attr12 in ' + location)
    # 观察时间
    if 'attr14' in attribute:
        attr14 = attribute['attr14']
        time = attr14.split(' ', 4)[3]
    else:
        sayz( 'no attr12 in ' + location)
    # 横切位置、最大矢量
    if 'attr16' in attribute:
        attr16 = attribute['attr16']
        attr16_arr = attr16.split(',', 1)
        cut_position = attr16_arr[0].split(' ', 2)[2]
        max_vector = attr16_arr[1].split(' ', 3)[3]
    else:
        sayz( 'no attr16 in ' + location)

    # 图像名
    figname = vectordata.location[0] + '_' + component
    # 使用replace前先将unicode转str
    figname = figname.replace('Group_', '').replace('Group', '')
    return x_label, y_label, component, time, cut_position, max_vector, figname

# 获取contour3D文件名
def contour3DInfo(contour3Ddata):
    # 图像名
    figname = contour3Ddata.location[0]
    # 使用replace前先将unicode转str
    figname = figname.replace('Group_', '').replace('Group', '')
    return figname

# 获取vector3D文件名
def vector3DInfo(alldata, vector3Ddata):
    vector3dLocations = []
    numList = []
    for everydata in alldata:

        if everydata.type == 6:
            if everydata.id == vector3Ddata.id:
                num = everydata.location[0][-1:]
                if num not in numList:
                    numList.append(num)
                    vector3dLocations.append(everydata.location)
    # 图像名
    figname = vector3Ddata.id
    # 返回图像名和vector3d数据
    return figname,vector3dLocations

# 读取时间变化图、空间变化图、相空间图的数据
def getData2(data):
    data = data.data_lists[0]
    dim = data.dim
    size = len(data.list)
    data = np.array(data.list).reshape(dim,int(size/dim))
    x = data[0]
    y = data[1]
    return x, y

# 读取等位图、矢量图的数据
def getData3(data):

    a = data.data_lists[0].list
    b = data.data_lists[1].list
    c = data.data_lists[2].list

    return a, b, c

# 观察范围格式规范函数
def range_format(num):
    num = num.replace('(', '').replace(')', '')
    num_arr = num.split(',', 2)
    for index in range(len(num_arr)):
        if float(num_arr[index]) >= 0:
            num_arr[index] = '+' + num_arr[index].replace(' ', '')
        else:
            num_arr[index] = '-' + num_arr[index].replace(' ', '')
    return '[' + num_arr[0] + ',' + num_arr[1] + ',' + num_arr[2] + ']'

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')