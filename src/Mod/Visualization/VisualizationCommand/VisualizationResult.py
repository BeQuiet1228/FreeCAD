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
import subprocess

import FreeCAD
import FreeCADGui
import VisualizationGui
import VisualizationPlot
import vPlot

count = 0


class FigTree(QDockWidget):
    def __init__(self, h5FilePath,parent=None):
        super(FigTree, self).__init__(parent)
        import time as testtime
        t = testtime.time()
        self.ui = VisualizationGui.TreeStructPal.Ui_DockWidget_resultTree()
        self.ui.setupUi(self)

        # self.ui.treeWidget_resultFig.setDragDropMode(self.InternalMove)
        # self.ui.treeWidget_resultFig.setDragEnabled(True)
        # self.ui.treeWidget_resultFig.setDropIndicatorShown(True)
        # self.ui.treeWidget_resultFig.setDragDropMode(self.ui.treeWidget_resultFig.DragDrop)
        # self.ui.treeWidget_resultFig.setDefaultDropAction(QtCore.Qt.MoveAction)
        # self.ui.treeWidget_resultFig.setContentsMargins(0, 0, 0, 0)

        # 解决QTreeWidget中的内容超出边界后自动隐藏的问题
        self.ui.treeWidget_resultFig.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.treeWidget_resultFig.header().setStretchLastSection(False)
        self.ui.treeWidget_resultFig.setAutoScroll(False)
        self.ui.treeWidget_resultFig.expandAll()

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
        mw = FreeCADGui.getMainWindow()
        # aw = app.activeWindow()
        # 获取Combo View
        if mw:
            dw = mw.findChild(QtGui.QDockWidget, 'Combo View')
            # 获取Combo View 下的comiTab
            if dw:
                self.qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
                # 将结果目录作为一个tab添加到Combo View下
                if count == 0:
                    # self.qtab.addTab(self, u'打开结果')
                    self.qtab.insertTab(self.qtab.count()-1, self, u'打开结果')
                else:
                    # self.qtab.addTab(self, u'打开结果' + str(count))
                    self.qtab.insertTab(self.qtab.count()-1, self, u'打开结果' + str(count))
                count += 1
                # 将树形目录设置为当前 Tab
                self.qtab.setCurrentWidget(self)

                self.qtab.setTabsClosable(True)
                self.qtab.tabCloseRequested.connect(self.closeTab)
                tabBar = self.qtab.tabBar()
                tabBar.setTabButton(0, QtGui.QTabBar.RightSide, None)
                tabBar.setTabButton(count+1, QtGui.QTabBar.RightSide, None)
            else:
                sayz('Combo View is not found')
        else:
            sayz('ActiveWindow is not found')

        # 将结果目录作为一个活动面板添加到界面中
        # aw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self)
        self.ui.treeWidget_resultFig.itemClicked['QTreeWidgetItem*', 'int'].connect(self.onClick)
        self.ui.treeWidget_resultFig.itemDoubleClicked['QTreeWidgetItem*', 'int'].connect(self.onDoubleClick)
        mdi = vPlot.getMdiArea()
        mdi.subWindowActivated.connect(self.updateTreeNode)

        self.h5FilePath = h5FilePath
        # 获取二维器件结构数据
        self.StructData, self.HeadList = getData(self.h5FilePath, "Group_kmat", "2D_struct", "2D_struct")
        # sayz(self.HeadList)
        if self.HeadList is not None and self.HeadList != []:
            self.cutDict = getcutData(self.StructData, self.HeadList,None,None,None)
            # sayz(self.cutDict)
        else:
            self.cutDict = None
        sayzerr("得到器件结构用时")
        sayzerr(testtime.time() - t)

    # 简单复制
    def closeTab(self,index):
        app = QtGui.qApp
        aw = app.activeWindow()
        if aw:
            dw = aw.findChild(QtGui.QDockWidget, 'Combo View')
            if dw:
                qtab = dw.findChild(QtGui.QTabWidget, 'combiTab')
        FreeCAD.Console.PrintMessage(self.qtab)
        widget =qtab.widget(index)
        if widget is not None:
            widget.deleteLater()
        #简单复制
    def onClick(self, item, column):
        
        # 设置item为被选中状态
        # item.setBackground(0,QtGui.QBrush(QtGui.QColor("#D3D3D3")))
        item.setForeground(0,QtGui.QBrush(QtGui.QColor("grey")))
        # item.setSelected(True)
        # FreeCAD.Console.PrintMessage("111\n")

        mdi = vPlot.getMdiArea()
        # closeOtherSubWindows(mdi, item, 'line')
        # 获取当前节点对应的子窗口是否打开
        # subWindow = isExisted(mdi, item, 'line')
        # # 若存在该节点名称对应的子窗口，则激活该窗口，否则重建一个窗口，重绘图像
        # if subWindow:
        #     mdi.setActiveSubWindow(subWindow)

        parent = item.parent()
        if parent is not None:
            parent = parent.text(0)
        datapath = item.data(0, QtCore.Qt.UserRole)
        sayz("dapapath\n")
        sayz(datapath)
        itemName = item.text(0)
        if parent == u'二维等位图':
            # 新建一个窗口
            figname = itemName
            fig,flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])

            import time as testtime
            t = testtime.time()
            # flag判断需不需要重新绘图
            if not flag:
                filename = datapath[0]
                subGroupName = datapath[1]

                try:
                    # 获取对应的等位图数据
                    contourData, headList = getData(filename, "Group_fild", "2D_contour", subGroupName)
                    # 获取对应的属性信息
                    x_label, y_label, time, component, range_start, range_end, range_min, range_max, step = contourInfo(
                        headList)
                    a,b,c = dealContourData(contourData,[x_label, y_label])
                except:
                    sayz("等位图数据信息获取错误")
                finally:
                    sayz("绘制等位图")
                try:
                    # 根据横纵坐标名确定截面名字
                    
                    cut_figName = x_label.split(" ", 1)[0] + "-" + y_label.split(" ", 1)[0]
                    FreeCAD.Console.PrintMessage(cut_figName + "\n")  
                    cut_figName2 = y_label.split(" ", 1)[0] + "-" + x_label.split(" ", 1)[0]
                    FreeCAD.Console.PrintMessage(cut_figName2 + "\n")
                    cutx,cuty,cutz = getcutXYZ(range_start)
                    
                    FreeCAD.Console.PrintMessage("VR+++++++++++++++++++++\n")
                    # 获取二维器件结构数据
                    if self.StructData is not None and self.HeadList is not None:
                        cutDict = getcutData(self.StructData, self.HeadList,cutx,cuty,cutz)
                    else:
                        cutDict = self.cutDict
                    
                    if cutDict is not None:
                        FreeCAD.Console.PrintMessage("VR+++++++++++++++++++++\n")
                        # 得到剖面图数据
                        cutAB,xyAll, cutpos, system, isExchange = getStruct2D(cutDict[3], cut_figName, cut_figName2)

                        # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                        fig.setVisible(False)
                        FreeCAD.Console.PrintMessage("VR+++++++++++++++++++++\n")
                        # 绘制等位图
                        VisualizationPlot.drawContour(None, None, x_label, y_label,system, time, component,
                                                      range_format(range_start),
                                                      range_format(range_end), range_min, range_max, step, a, b, c,
                                                      'line', 0)
                        FreeCAD.Console.PrintMessage("VR+++++++++++++++++++++\n")
                        VisualizationPlot.drawCut(cutAB,xyAll, "contour-contour", cutDict, cutpos, system, isExchange)
                except:
                    sayz("器件结构信息获取错误")
                finally:
                    fig.setVisible(True)
            sayzerr("二维等位图用时")
            sayzerr(testtime.time()-t)
        elif parent == u'时间变化图':
            figname = itemName
            fig,flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])
            import time as testtime
            t = testtime.time()
            if not flag:
                filename = datapath[0]
                subGroupName = datapath[1]
                try:
                    data, headList = getData(filename, "Group_grid", "2D_observe", subGroupName)
                    x, y = None, None
                    if data is not None and data.shape[0] > 1:
                        x = data[0]
                        y = data[1]
                    x_label, y_label, type, range_min, range_max = observeInfo(headList)
                    VisualizationPlot.drawObserve(x_label, y_label, type, range_format(range_min), range_format(range_max), x, y)
                finally:
                    sayz("绘制时间变化图")
            sayzerr("时间变化图用时")
            sayzerr(testtime.time() - t)
        elif parent == u'相空间图':

            import time as testtime
            t = testtime.time()
            # 根据figname判断是否已经存在改fig，存在则不重绘，直接显示
            figname = itemName
            fig,flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])
            if not flag:
                filename = datapath[0]
                subGroupName = datapath[1]
                try:
                    data, headList = getData(filename, "Group_part", "2D_phaseSpace", subGroupName)
                    x, y ,z = None, None,None
                    if data is not None and data.shape[0]>1:
                        x = data[0]
                        y = data[1]
                        z = data[2]
                    x_label, y_label, particle, time = phasespaceInfo(headList)
                    if self.cutDict is not None:
                        
                        system=self.cutDict[3].values()[0][1]
                        if particle is not None:
                            if system == "cylindrical":
                                import re
                                # particle = particle.replace('1','2').replace('2','3').replace('3','1')
                                list1=[i.start() for i in re.finditer('1', particle)]
                                list2=[i.start() for i in re.finditer('2', particle)]
                                list3=[i.start() for i in re.finditer('3', particle)]
                                particle = list(particle)
                                for i in list1:
                                    particle[i]='2'
                                for i in list2:
                                    particle[i]='3'
                                for i in list3:
                                    particle[i]='1'
                                particle = ''.join(particle)
                            if "P" not in particle:
                                fig.setVisible(False)

                                
                                cut_figName = x_label.split(" ", 1)[0] + "-" + y_label.split(" ", 1)[0]
                                cut_figName2 = y_label.split(" ", 1)[0] + "-" + x_label.split(" ", 1)[0]
                                cutAB, xyAll,cutpos, system, isExchange = getStruct2D(self.cutDict[3], cut_figName, cut_figName2)
                                # data, headList = getData(filename, "Group_kmat", "2D_struct", "2D_struct")
                                
                                # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见   
                                VisualizationPlot.drawCut(cutAB,xyAll, None, self.cutDict, cutpos, system, isExchange)
                                VisualizationPlot.drawPhasespace(None, None, x_label, y_label, particle, time, x, y,z)
                                fig.setVisible(True)
                            else:
                                VisualizationPlot.drawPhasespace(None, None, x_label, y_label, particle, time, x, y,z)
                finally:
                    sayz("绘制相空间图")
            sayzerr("相空间图用时")
            sayzerr(testtime.time()-t)
        elif parent == u'空间变化图':
            figname = itemName
            fig,flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])
            if not flag:
                filename = datapath[0]
                subGroupName = datapath[1]
                try:
                    data, headList = getData(filename, "Group_grid", "2D_rangers", subGroupName)
                    x, y = None, None
                    if data is not None and data.shape[0] > 1:
                        x = data[0]
                        y = data[1]

                    x_label, y_label, time, component, range_min, range_max = rangeInfo(headList)

                    VisualizationPlot.drawRange(x_label, y_label, time, component, range_format(range_min), range_format(range_max), x, y)
                finally:
                    sayz("绘制空间变化图")
        elif parent == u'二维矢量图':
            FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
            figname = itemName
            fig, flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])
            if not flag:
                filename = datapath[0]
                subGroupName = datapath[1]
                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                data, headList = getData(filename, "Group_fild", "2D_vectors", subGroupName)
                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                a, b, c = None, None, None
                if data is not None and data.shape[0] > 2:
                    a = data[0]
                    b = data[1]
                    c = data[2]
                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                x_label, y_label, component, time, cut_position, max_vector = vectorInfo(headList)
                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")

                cut_figName = x_label.split(" ", 1)[0].split("(m)")[0] + "-" + y_label.split(" ", 1)[0].split("(m)")[0]
                cut_figName2 = y_label.split(" ", 1)[0].split("(m)")[0] + "-" + x_label.split(" ", 1)[0].split("(m)")[0]
                # 将X2-X3等cut_figname进行规范化
                cut_figName = cut_figName.replace("X1", "X").replace("X2", "Y").replace("X3", "Z")
                cut_figName2 = cut_figName2.replace("X1", "X").replace("X2", "Y").replace("X3", "Z")
                # data, headList = getData(filename, "Group_kmat", "2D_struct", "2D_struct")
                cutx, cuty, cutz = getVectorCut(self.HeadList, cut_figName, cut_figName2,
                                                                    cut_position)
                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                if self.StructData is not None and self.HeadList is not None:
                    # 获取二维器件结构数据
                    cutDict = getcutData(self.StructData, self.HeadList, cutx, cuty, cutz)
                else:
                    cutDict = self.cutDict
                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                if cutDict is not None:
                    FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                    cutAB, xyAll, cutpos, system, isExchange = getStruct2D(cutDict[3], cut_figName, cut_figName2)
                    # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                    FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                    fig.setVisible(False)
                    FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                    VisualizationPlot.drawCut(cutAB,xyAll,None, self.cutDict, cutpos, system, isExchange)
                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                VisualizationPlot.drawVector(None, None, x_label, y_label, component, time, cut_position, max_vector, a, b, c)

                FreeCAD.Console.PrintMessage("2D_vectors+++++++++++++++++++++\n")
                fig.setVisible(True)
                sayz("绘制二位矢量图")
        elif parent == u'三维等位图':
            import time
            filename = datapath[0]
            figname = datapath[1]

            # 先把UTF-8转成万国码在转成GBK
            filename = filename.decode('utf-8').encode('gbk')
            figname = figname.decode('utf-8').encode('gbk')

            # 获取Mod文件夹路径
            file_path = os.path.dirname(__file__)
            exe_path = os.path.dirname(os.path.dirname(file_path))

            # 传文件路径绘图
            minAngle = "4"
            p = subprocess.Popen(exe_path + '\\Package\\visualizationPlot3D\\Visualization3D.exe ' + '"' + filename + '"' + ' '+'"' + filename + '"'+ ' None'+ ' CONTOUR3D ' + '"' + figname + '"')
            # 输出当前进程的执行状况
            # sayz(p.poll())
            sayz(item.text(0)+u"开始绘制...")

        elif parent == u'三维矢量图':
            filename = datapath[0]
            fignameList = datapath[1]
            # 三个数据来源信息,一个数据图名信息,以"#"隔开,
            figname = fignameList[0]+"#"+fignameList[1]+"#"+fignameList[2]+"#"+itemName

            # 先把UTF-8转成万国码在转成GBK
            filename = filename.decode('utf-8').encode('gbk')
            figname = figname.decode('utf-8').encode('gbk')
            # 获取Mod文件夹路径
            file_path = os.path.dirname(__file__)
            exe_path = os.path.dirname(os.path.dirname(file_path))
            # sayz(exe_path)
            # 传文件路径绘图
            # sayz(filename)
            # sayz(figname)
            minAngle = "4"
            subprocess.Popen(exe_path + '\\Package\\visualizationPlot3D\\Visualization3D.exe ' + '"' + filename + '"' + ' '+'"' + filename + '"'+ ' None'+ ' VECTOR3D ' + '"' + figname + '"')
            sayz(item.text(0) + u"开始绘制...")

        elif parent == u'三维立体图':

            filename = datapath[0]

            # 先把UTF-8转成万国码在转成GBK
            filename = filename.decode('utf-8').encode('gbk')

            file_path = os.path.dirname(__file__)
            exe_path = os.path.dirname(os.path.dirname(file_path))
            minAngle = "0"
            subprocess.Popen(exe_path + '\\Package\\visualizationPlot3D\\Visualization3D.exe ' + '"' + filename + '"' + ' '+'"' + filename + '"'+ ' None'+ ' STRUCT3D ' + 'None')
            sayz(item.text(0) + u"开始绘制...")

        elif parent == u'剖面结构图':
            figname = itemName
            fig,flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])
            if not flag:

                filename = datapath[0]

                # data, headList = getData(filename, "Group_kmat", "2D_struct", "2D_struct")
                if self.cutDict is not None:
                    cutAB, xyAll,cutpos, system, isExchange = getStruct2D(self.cutDict[3], figname, figname)
                    VisualizationPlot.drawCut(cutAB,xyAll, figname, self.cutDict, cutpos, system, None)
        elif parent == u'三维粒子图':

            filename = datapath[0]

            # 先把UTF-8转成万国码在转成GBK
            filename = filename.decode('utf-8').encode('gbk')

            file_path = os.path.dirname(__file__)
            exe_path = os.path.dirname(os.path.dirname(file_path))
            minAngle = "0"
            subprocess.Popen(exe_path + '\\Package\\visualizationPlot3D\\Visualization3D.exe ' + '"' + filename + '"' + ' '+'"' + filename + '"'+ ' None'+ ' PHASESPACE3D ' + 'None')
            sayz(item.text(0) + u"开始绘制...")
    # 执行exe文件，并输出exe中的log
    def execute(self, cmd):
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
        popen.stdout.close()
        return_code = popen.wait()
        if return_code:
            raise subprocess.CalledProcessError(return_code, cmd)

    def onDoubleClick(self, item, column):
        # 添加shade选项
        self.createContextMenu(item)

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
            self.actionA = self.contextMenu.addAction("Show in shade")
            self.actionB = self.contextMenu.addAction("Geometric ratio show in line")
            self.actionC = self.contextMenu.addAction("Geometric ratio show in shade")
            self.actionD = self.contextMenu.addAction("Show in 3D")
            # 将动作与处理函数相关联, 使用lambda可以传递额外的参数
            # 0为等差绘制，1为等比绘制
            self.actionA.triggered.connect(lambda: self.showShade(item,'shade',0))
            self.actionB.triggered.connect(lambda: self.showShade(item, 'line',1))
            self.actionC.triggered.connect(lambda: self.showShade(item,'shade', 1))
            self.actionD.triggered.connect(lambda: self.show3D(item))
            self.contextMenu.move(QtGui.QCursor().pos())
            self.contextMenu.show()

    # 绘制contour shade
    def showShade(self, item,type,isRatio):
        import time as testtime
        t=testtime.time()
        mdi = vPlot.getMdiArea()
        # subWindow = isExisted(mdi, item, type)
        # if subWindow:
        #     mdi.setActiveSubWindow(subWindow)
        #     sayz('subWindow')

        itemName = item.text(0)
        # 判断是否等比的绘制等位图
        if not isRatio:
            figname = itemName + '_Shade'
        else:
            if type == 'shade':
                figname=itemName + '_Shade_GeometricRatio'
            else:
                figname = itemName + '_GeometricRatio'
        sayz('figname')
        datapath = item.data(0, QtCore.Qt.UserRole)
        fig, flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])
        # flag判断需不需要重新绘图
        if not flag:

            filename = datapath[0]
            subGroupName = datapath[1]
            try:
                # 获取对应的等位图数据
                contourData, headList = getData(filename, "Group_fild", "2D_contour", subGroupName)
                # 获取对应的属性信息
                x_label, y_label, time, component, range_start, range_end, range_min, range_max, step = contourInfo(
                    headList)
                # a = contourData[0]
                # b = contourData[1]
                # c = contourData[2]
                a,b,c = dealContourData(contourData,[x_label, y_label])

            finally:
                sayz("绘制等位图")
            try:
                # 根据横纵坐标名确定截面名字
                cut_figName = x_label.split(" ", 1)[0] + "-" + y_label.split(" ", 1)[0]
                cut_figName2 = y_label.split(" ", 1)[0] + "-" + x_label.split(" ", 1)[0]
                cutx, cuty, cutz = getcutXYZ(range_start)
                # 获取二维器件结构数据
                if self.StructData is not None and self.HeadList is not None:
                    cutDict = getcutData(self.StructData, self.HeadList, cutx, cuty, cutz)
                else:
                    cutDict = self.cutDict
                if cutDict is not None:

                    # 得到剖面图数据
                    cutAB, xyAll, cutpos, system, isExchange = getStruct2D(cutDict[3], cut_figName, cut_figName2)

                    # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                    fig.setVisible(False)
                    VisualizationPlot.drawContour(None, None, x_label, y_label, system, time, component,
                                                  range_format(range_start),
                                                  range_format(range_end), range_min, range_max, step, a, b, c, type,
                                                  isRatio)

                    VisualizationPlot.drawCut(cutAB, xyAll,  "contour-contour", cutDict, cutpos, system, isExchange)
            finally:
                fig.setVisible(True)
        sayzerr("二维等位图用时")
        sayzerr(testtime.time() - t)
    def show3D(self, item):
        import time as testtime
        t=testtime.time()
        mdi = vPlot.getMdiArea()
        # subWindow = isExisted(mdi, item, '3D')
        # if subWindow:
        #     mdi.setActiveSubWindow(subWindow)

        itemName = item.text(0)
        # 新建一个窗口
        figname = itemName + '_3D'
        datapath = item.data(0, QtCore.Qt.UserRole)
        fig, flag = vPlot.figure(False, figname,datapath[0].split('/')[-1])
        # flag判断需不需要重新绘图
        if not flag:
            itemName = item.text(0)

            filename = datapath[0]
            subGroupName = datapath[1]
            try:
                # 获取对应的等位图数据
                contourData, headList = getData(filename, "Group_fild", "2D_contour", subGroupName)
                # 获取对应的属性信息
                x_label, y_label, time, component, range_start, range_end, range_min, range_max, step = contourInfo(
                    headList)
                a,b,c = dealContourData(contourData,[x_label, y_label])

                # 根据横纵坐标名确定截面名字
                cut_figName = x_label.split(" ", 1)[0] + "-" + y_label.split(" ", 1)[0]
                cut_figName2 = y_label.split(" ", 1)[0] + "-" + x_label.split(" ", 1)[0]
                cutx, cuty, cutz = getcutXYZ(range_start)
                # 获取二维器件结构数据
                if self.StructData is not None and self.HeadList is not None:
                    cutDict = getcutData(self.StructData, self.HeadList, cutx, cuty, cutz)
                else:
                    cutDict = self.cutDict
                if cutDict is not None:
                    # 得到剖面图数据
                    cutAB, xyAll, cutpos, system, isExchange = getStruct2D(cutDict[3], cut_figName, cut_figName2)
                    # 绘制等位图
                    VisualizationPlot.drawContour3D(x_label, y_label, system, time, component, range_format(range_start),
                                                    range_format(range_end), range_min, range_max, step, a, b, c)
            finally:
                sayz("绘制二维等位图3D模式")
        sayzerr("二维等位图用时")
        sayzerr(testtime.time() - t)
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
# filename：h5文件名
def showResultTree(h5FilePath):
    #为了修改hdf5柱坐标系下相空间图名字有问题的bug，需要获取system
    StructData,HeadList = getData(h5FilePath, "Group_kmat", "2D_struct", "2D_struct")
        # sayz(self.HeadList)
    if HeadList is not None and HeadList != []:
        cutDict = getcutData(StructData, HeadList,None,None,None)
        system=cutDict[3].values()[0][1]
    else:
        system = None
    StructData = None
    HeadList = None
    import time as testtime
    t = testtime.time()
    # 显示树形结构
    tree = FigTree(h5FilePath)
    tree.show()
    # 三维立体图
    arg = [h5FilePath]
    figName = u'器件结构图'
    addChild(tree.ui, 5, figName, arg)
    addChild(tree.ui, 7, u"三维粒子图", arg)
    # 根据h5 文件路径获得所有图的属性信息来得到图名
    figNameInfo = getFigNameInfo(h5FilePath)
    
    if figNameInfo != None:
        # 获取三维矢量图名
        vector3DNameInfo = getVector3DName(figNameInfo)

        # 读取属性数据
        # info[0]是图形类型，info[1]是图形数据所在subgroup名称，存入item中用来找到其对应的数据
        # info[2]是该subgroup对应的所有属性信息列表

        for info in figNameInfo:

            # 等位图
            if info[0] == "2D_contour":
                try:
                    time = info[2][12].split('TIME', 1)[1].replace("SEC", "").replace(" ", "")
                    component = info[2][14].strip().split(' ', 3)[1]
                    figname = info[1]+'_'+component+'_'+time
                    arg = [h5FilePath, info[1]]
                    # 树形目录添加子节点
                    addChild(tree.ui, [0, 0], figname, arg)
                finally:
                    pass

            # 三维等位图
            elif info[0] == "3D_fieldem":
                try:
                    component = info[2][14].strip().split(' ', 3)[1]
                    # 将h5文件名和subgroup名记录在树节点中
                    arg = [h5FilePath, info[1]]
                    figname = info[1]+'_'+component
                    # 树形目录添加子节点
                    addChild(tree.ui, [0, 1], figname, arg)
                finally:
                    pass

            elif info[0] == "2D_observe":
                try:
                    field = info[2][3].strip().split('-',1)[0]
                    type = info[2][13].strip().split('COMPONENT', 1)[0]
                    figname = info[1]+'_'+field+'_'+type
                    arg = [h5FilePath, info[1]]
                    # 添加子节点
                    addChild(tree.ui, 1, figname, arg)
                finally:
                    pass

            elif info[0] == "2D_phaseSpace":
                try:
                    FreeCAD.Console.PrintMessage("init_2D_phaseSpace1\n")
                    particle = info[2][11].split('OF', 1)[1].split('AT', 1)[0].strip()
                    FreeCAD.Console.PrintMessage("init_2D_phaseSpace1\n")
                    if system is not None:
                        FreeCAD.Console.PrintMessage("init_2D_phaseSpace2\n")
                        if system == "cylindrical":
                            import re
                            # particle = particle.replace('1','2').replace('2','3').replace('3','1')
                            list1=[i.start() for i in re.finditer('1', particle)]
                            list2=[i.start() for i in re.finditer('2', particle)]
                            list3=[i.start() for i in re.finditer('3', particle)]
                            particle = list(particle)
                            for i in list1:
                                particle[i]='2'
                            for i in list2:
                                particle[i]='3'
                            for i in list3:
                                particle[i]='1'
                            particle = ''.join(particle)
                        FreeCAD.Console.PrintMessage("init_2D_phaseSpace3\n")
                        # 得到item名字
                        figname = info[1] + "_" + particle
                        FreeCAD.Console.PrintMessage("init_2D_phaseSpace4\n")
                        arg = [h5FilePath, info[1]]
                        # 添加子节点
                        addChild(tree.ui, 2, figname, arg)
                finally:
                    pass

            elif info[0] == "2D_rangers":
                try:
                    component = info[2][13].split('COMPONENT', 1)[0]
                    # 得到item名字
                    figname = info[1] + "_" + component
                    arg = [h5FilePath, info[1]]
                    # 添加子结点
                    addChild(tree.ui, 3, figname, arg)
                finally:
                    pass

            elif info[0] == "2D_vectors":
                try:
                    component = info[2][11].strip().split(' ', 3)[3].replace('(', '').replace(')', '').replace(',', 'VS')
                    figname = info[1].strip() + "_" + component
                    arg = [h5FilePath, info[1]]
                    addChild(tree.ui, [4, 0], figname, arg)
                finally:
                    pass

            # 二维器件结构图
            elif info[0] == "2D_struct":
                try:
                    # 得到三个剖面图的名字
                    nameX,nameY,nameZ = struct2DInfo(info[2])
                    arg = [h5FilePath, info[1]]
                    
                    # 添加三个子结点
                    if nameX != None:
                        addChild(tree.ui, 6, nameX, arg)
                        addChild(tree.ui, 6, nameY, arg)
                        addChild(tree.ui, 6, nameZ, arg)
                finally:
                    pass


        # 三维矢量图
        for figname in vector3DNameInfo.keys():
            # 获取图的信息
            value = vector3DNameInfo[figname]
            if len(value) == 3:
                # 保证vector3d的三个数据不重复
                if len({value[0][-1:],value[1][-1:],value[2][-1:]})==3:
                    arg = [h5FilePath, value]
                    # 树形目录添加子节点
                    addChild(tree.ui, [4, 1], figname, arg)
    sayzerr("建立树状结构用时")
    sayzerr(testtime.time()-t)
# 判断树节点对应的图像窗口是否打开
def isExisted(mdi, treeItem, tag):
    figtype = treeItem.text(0).split('_')[-1]
    subWindowList = mdi.subWindowList()
    for subWindow in subWindowList:
        if tag == 'line'and subWindow.windowTitle() == treeItem.text(0):
            # print treeItem.data(0, QtCore.Qt.UserRole)
            sayz(treeItem.text(0))
            return subWindow
        elif tag == 'shade' and subWindow.windowTitle() == treeItem.text(0)+'_Shade':
            sayz(treeItem.text(0)+'_Shade')
            return subWindow
        elif tag == 'line' and subWindow.windowTitle() == treeItem.text(0)+'_GeometricRatio':
            sayz(treeItem.text(0)+'_GeometricRatio')
            return subWindow
        elif tag == 'shade' and subWindow.windowTitle() == treeItem.text(0)+'_Shade_GeometricRatio':
            sayz(treeItem.text(0)+'_Shade_GeometricRatio')
            return subWindow
        elif tag == '3D' and subWindow.windowTitle() == treeItem.text(0)+'_3D':
            sayz(treeItem.text(0) + '_3D')
            return subWindow
    sayz("isExisted")
    return False

def closeOtherSubWindows(mdi, treeItem, tag):
    subWindowList = mdi.subWindowList()
    for subWindow in subWindowList:
        if tag == 'line'and subWindow.windowTitle() == treeItem.text(0):
            continue
        elif tag == 'shade' and subWindow.windowTitle() == treeItem.text(0)+'_Shade':
            continue
        elif tag == 'line' and subWindow.windowTitle() == treeItem.text(0)+'_GeometricRatio':
            continue
        elif tag == 'shade' and subWindow.windowTitle() == treeItem.text(0)+'_Shade_GeometricRatio':
            continue
        elif tag == '3D' and subWindow.windowTitle() == treeItem.text(0)+'_3D':
            continue
        else:
            subWindow.close()

    # mdi = vPlot.getMdiArea()
    # subWindowList = mdi.subWindowList()
    # for subWindowItem in subWindowList:
    #     subWindowItem.close()

# 添加子节点
def addChild(tree, level, itemName, itemData):
    item = QtGui.QTreeWidgetItem()
    item.setText(0, itemName)
    # 树节点存放路径
    item.setData(0, QtCore.Qt.UserRole, itemData)
    item.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Item.svg"))
    if type(level) != list:
        tree.treeWidget_resultFig.topLevelItem(level).addChild(item)
    else:
        tree.treeWidget_resultFig.topLevelItem(level[0]).child(level[1]).addChild(item)

def dealContourData(contourData,labelList):
    a, b, c = None,None,None
    try:
        a = contourData[0]
        b = contourData[1]
        c = contourData[2]

        # thea角向
        if "R*cos(Phi)" in labelList[0] or "R*cos(Phi)" in labelList[1]:
            # 判断是不是完整数据
            if not round(b[-1]-b[0],3) == 6.283:
                # 不是完整数据的话需要补一列数据，使theta从0到2*pi闭合
                # theta列对应增加第一个数据，等位值列对应增加该theta的对应的等位值
                b.append(b[0]+2*np.pi)
                c.extend(c[0:len(a)])
                # sayz(b)
                # sayz(c[-len(a):-1])

        #r作为y轴
        elif "R" in labelList[1]:
            pass
        # r作为x轴
        elif "R" in labelList[0]:
            pass
    finally:

        return a,b,c

# 读取等位图的信息
def contourInfo(headValue):
    x_label, y_label, time, component, range_start, range_end, range_min, range_max, step = None,None,None, None, None, None, None, None, None
    try:
        # x轴标注
        x_label = headValue[8].strip().replace("))", ")")
        # y轴标注
        y_label = headValue[10].strip().replace("))", ")")
        # 观察分量
        time = headValue[12].strip().split('TIME', 1)[1].replace("SEC", "").replace(" ", "")
        attr15 = headValue[14].strip().split(' ', 3)
        # 观察分量
        component = attr15[1] + attr15[3]
        # 等值区域
        range = headValue[16].strip().split('FROM', 1)[1].split('TO', 1)
        range_start = range[0]
        range_end = range[1]
        # 等值范围
        range = headValue[18].strip().split(':', 1)[1].split('TO', 1)
        range_min = range[0].replace(' ', '')
        range_max = range[1].replace(' ', '')
        # 等值步长
        step = headValue[20].strip().split(' ', 3)[3]
    except:
        
        sayzerr("the HeadValueList's Length is at least 21")
    return x_label, y_label, time, component, range_start, range_end, range_min, range_max, step

# 读取时间变化图的信息
def observeInfo(headValue):
    x_label, y_label, type, range_min, range_max = None,None,None,None,None
    try:
        # x轴标注
        x_label = headValue[7].strip()
        # y轴标注
        y_label = headValue[9].strip()
        # 观察类型
        type = headValue[13].strip().split('COMPONENT', 1)[0]
        # 观察范围,获取()中的内容
        import re
        range = re.findall('[(](.*?)[)]', headValue[15])
        # range = headValue[15].strip().split('FROM',1)[1].split('TO', 1)
        range_min = ''
        range_max = ''
        if len(range)>1:
            range_min = '(' + range[0] + ')'
            range_max = '(' + range[1] + ')'
        elif len(range)>0:
            range_min = '(' + range[0] + ')'
    except:
        
        sayzerr("the HeadValueList's Length is at least 16")

    return x_label, y_label, type, range_min, range_max

# 读取相空间图的信息
def phasespaceInfo(headValue):
    x_label, y_label, particle, time = None,None,None,None
    try:
        x_label = headValue[7].strip().replace("))", ")")
        y_label = headValue[9].strip().replace("))", ")")
        particle = headValue[11].strip().split('OF', 1)[1].split('AT', 1)[0].strip()
        time = headValue[11].strip().split(':', 1)[1].replace("SEC", "").replace(" ", "")
    finally:
        return x_label, y_label, particle, time

# 读取空间变化图的信息
def rangeInfo(headValue):
    x_label, y_label, time, component, range_min, range_max = None, None, None, None, None,None
    try:
        # x轴标注
        x_label = headValue[7].strip()

        # 观察时间
        time = headValue[11].strip().split(':', 1)[1].replace("SEC", "").replace(" ", "")
        # 分量曲线
        component = headValue[13].strip().split('COMPONENT', 1)[0]
        # y轴标注
        y_label = component+'('+headValue[9].strip()+')'
        # 观察范围
        range = headValue[15].strip().split('FROM', 1)[1].split('TO', 1)
        range_min = range[0]
        range_max = range[1]
    except:
        
        sayzerr("the HeadValueList's Length is at least 16")

    return x_label, y_label, time, component, range_min, range_max

# 获取二维矢量图的信息
def vectorInfo(headValue):
    x_label, y_label, component, time, cut_position, max_vector = None,None,None,None,None,None
    try:
        # x轴标注
        x_label = headValue[7].strip()
        # y轴标注
        y_label = headValue[9].strip()
        # 观察分量
        component = headValue[11].strip().split(' ', 3)[3].replace('(', '').replace(')', '').replace(',', 'VS')
        # 观察时间
        time = headValue[13].strip().split(' ', 4)[2]
        # 横切位置、最大矢量
        if "," in headValue[15]:
            cut_direction = headValue[15].strip().split(',', 1)[0].split(' ', 2)[1]
            cut_position = headValue[15].strip().split(',', 1)[0].split(' ', 2)[2]
            max_vector = headValue[15].strip().split(',', 1)[1].split(' ', 3)[3]
        else:
            cut_direction = headValue[15].split('=')[0]
            cut_position = headValue[15].split('=')[1]
            max_vector = "0"
    except:
        
        sayzerr("the HeadValueList's Length is at least 16")
    return x_label, y_label, component, time, cut_position, max_vector

def getVectorCut(headList,cut_figName,cut_figName2, cut_position):
    cutX, cutY, cutZ = None,None,None
    try:
        # 根据横纵坐标轴及横切位置确定截面
        # sayz("aa"+cut_position+"aaa")
        cut_position = float(cut_position.split('(')[0])
        if 'cartesian' in headList[3]:
            # if "X" in cut_direction:
            #     cutX = float(cut_position)
            # elif "Y" in cut_direction:
            #     cutY = float(cut_position)
            # elif "Z" in cut_direction:
            #     cutZ = float(cut_position)
            if "Y-Z" in cut_figName or "Y-Z" in cut_figName2:
                cutX = cut_position
            elif "Z-X" in cut_figName or "Z-X" in cut_figName2:
                cutY = cut_position
            elif "X-Y" in cut_figName or "X-Y" in cut_figName2:
                cutZ = cut_position

        elif 'cylindrical'in headList[3]:
            # if "Z" in cut_direction:
            #     cutX = float(cut_position)
            # elif "R" in cut_direction:
            #     cutY = float(cut_position)
            # elif "PHI" in cut_direction:
            #     cutZ = float(cut_position)
            if "R*cos(Phi)-R*sin(Phi)" in cut_figName or "R*cos(Phi)-R*sin(Phi)" in cut_figName2:
                cutX = cut_position
            elif "Phi-Z" in cut_figName or "Phi-Z" in cut_figName2:
                cutY = cut_position
            elif "Z-R" in cut_figName or "Z-R" in cut_figName2:
                cutZ = cut_position
        elif 'polar'in headList[3]:

            if "Phi-Z" in cut_figName or "Phi-Z" in cut_figName2:
                cutX = cut_position
            elif "Z-R" in cut_figName or "Z-R" in cut_figName2:
                cutY = cut_position
            elif "R*cos(Phi)-R*sin(Phi)" in cut_figName or "R*cos(Phi)-R*sin(Phi)" in cut_figName2:
                cutZ = cut_position

    finally:
        return cutX, cutY, cutZ

# 获取二维器件结构的信息
def struct2DInfo(headvalue):
    temp = None
    if len(headvalue) < 4:
        temp = headvalue[2]
    else:
        temp = headvalue[3]

    if 'cartesian' in temp:
        nameX = "Y-Z"
        nameY = "Z-X"
        nameZ = "X-Y"
    elif 'cylindrical'in temp:
        nameX = "R*cos(Phi)-R*sin(Phi)"
        nameY = "Phi-Z"
        nameZ = "Z-R"
    elif 'polar'in temp:
        nameX = "Phi-Z"
        nameY = "Z-R"
        nameZ = "R*cos(Phi)-R*sin(Phi)"
    else:
        sayzerr("system is wrong")
        return None,None,None
    return nameX,nameY,nameZ

# 获取contour3D文件名
def contour3DInfo(root):
    # 图像名
    figname = os.path.basename(root)
    # 使用replace前先将unicode转str
    figname = figname.replace('Group_', '').replace('Group', '') + "_3D"
    return figname

# 获取vector3D文件名
def vector3DInfo(root):
    # 图像名
    figname = os.path.basename(root) + "_3D"
    return figname

# 获取vector3D文件名
def getVector3DName(figNameInfo):
    vectorNameDict = {}
    for info in figNameInfo:
        if info[0] == "3D_fieldem":
            # key的规则为dataset首字母_时间
            key = info[2][-1][:1]+"_"+info[2][1].split("    ")[1].strip()
            # 如果键不在字典中,则添加键并将值设为default
            # value规则为groupName_subGroupName_dataSetName
            value = "Group_fild_" + info[1] + "_" + info[2][-1]
            if key not in vectorNameDict:
                vectorNameDict[key]=[value]
            # 确保数据名最后一个字符为1,2,3中一个,且数据不重复
            if (value not in vectorNameDict[key]) and (value[-1:] in ['1','2','3']):
                vectorNameDict[key].append(value)

    return vectorNameDict
# 获得二维器件结构剖面数据
def dealStruct2D(data,system,cutX,cutY,cutZ):
    import time as testtime
    t = testtime.time()


    mx1 = data[0]
    mx2 = data[1]
    mx3 = data[2]
    num1 = len(mx1)
    num2 = len(mx2)
    num3 = len(mx3)
    struct_data = data[3]

    # yz 面 y 的索引
    indexX_yList = []
    # yz 面 z 的索引
    indexX_zList = []

    # xz 面 x 的索引
    indexY_xList = []
    # xz 面 z 的索引
    indexY_zList = []

    # xy 面 x 的索引
    indexZ_xList = []
    # xy 面 y 的索引
    indexZ_yList = []

    # 得到切面的索引
    # 传入切面位置为None或者不在数据范围内,则截取中间位置
    if cutX == None or (cutX> max(mx1) or cutX<min(mx1)):

        if "cartesian" == system:
            # cutX = find_close_fast(mx1, (max(mx1)-min(mx1)) / 2+min(mx1)) + 1
            cutX = (num1+1)/2
        elif "cylindrical" == system:
            # cutX = find_close_fast(mx1, (max(mx1)-min(mx1)) / 2+min(mx1)) + 1
            cutX = (num1 + 1) / 2
        elif "polar" == system:
            # cutX = find_close_fast(mx1, (max(mx1)-min(mx1)) / 2+min(mx1)) + 1
            cutX = (num1 + 1) / 2
        else:
            sayzerr("system is wrong")
            return
    else:
        cutX = find_close_fast(mx1, cutX) + 1

    if cutY == None or (cutY> max(mx2) or cutY<min(mx2)):
        if "cartesian" == system:
            # cutY = find_close_fast(mx2, (max(mx2)-min(mx2)) / 2+min(mx2)) + 1
            cutY = (num2 + 1) / 2
        elif "cylindrical" == system:
            # cutY = find_close_fast(mx2, (max(mx2)-min(mx2)) / 2+min(mx2)) + 1
            cutY = (num2 + 1) / 2
        #设置切面位置为0°
        elif "polar" == system:
            cutY = 1
        else:
            sayzerr("system is wrong")
            return
    else:
        cutY = find_close_fast(mx2, cutY) + 1

    if cutZ == None or (cutZ> max(mx3) or cutZ<min(mx3)):
        if "cartesian" == system:
            # cutZ = find_close_fast(mx3, (max(mx3)-min(mx3)) / 2+min(mx3)) + 1
            cutZ = (num3 + 1) / 2
        # 设置切面位置为0°
        elif "cylindrical" == system:
            cutZ = 1
        elif "polar" == system:
            # cutZ = find_close_fast(mx3, (max(mx3)-min(mx3)) / 2+min(mx3)) + 1
            cutZ = (num3 + 1) / 2
        else:
            sayzerr("system is wrong")
            return
    else:
        cutZ = find_close_fast(mx3, cutZ) + 1

    struct_data = struct_data.T
    # 保存剖面数据
    # 获取struct中cutX切面的索引
    color = [1,2,3,4,5,6,7,8, 9, 10, 11, 12, 13, 14, 15, 16]

    for c in color:
        colorFlag = np.floor_divide(struct_data[3],pow(2,c))
        #根据切片和颜色分类
        index_x = np.where((struct_data[0]==cutX) & (colorFlag==1))
        # 得到其对应的yz数据
        indexX_yList.append(struct_data[1][index_x])
        indexX_zList.append(struct_data[2][index_x])

        index_y = np.where((struct_data[1] == cutY) & (colorFlag==1))
        indexY_xList.append(struct_data[0][index_y])
        indexY_zList.append(struct_data[2][index_y])


        index_z = np.where((struct_data[2] == cutZ) & (colorFlag==1))
        indexZ_xList.append(struct_data[0][index_z])
        indexZ_yList.append(struct_data[1][index_z])

    # for i in range(struct_data.shape[0]):
    #     if struct_data[i][0] == cutX:
    #         indexX_y.append(struct_data[i][1])
    #         indexX_z.append(struct_data[i][2])
    #     if struct_data[i][1] == cutY:
    #         indexY_x.append(struct_data[i][0])
    #         indexY_z.append(struct_data[i][2])
    #     if struct_data[i][2] == cutZ:
    #         indexZ_x.append(struct_data[i][0])
    #         indexZ_y.append(struct_data[i][1])

    listX_withColor, listY_withColor, listZ_withColor,=[],[],[]
    listXAll_withColor, listYAll_withColor, listZAll_withColor = [],[],[]

    for i in range(0,len(color)):
        indexX_y = indexX_yList[i]
        indexX_z = indexX_zList[i]
        indexY_z = indexY_zList[i]
        indexY_x = indexY_xList[i]
        indexZ_y = indexZ_yList[i]
        indexZ_x = indexZ_xList[i]
        # yz面数据
        listX = []
        # xz面数据
        listY = []
        # xy面数据
        listZ = []

        # 由于柱坐标的kmt顺序不同，cutX和cutZ以theta和r作为连续加1迭代的x

        if "cylindrical" == system:
            classified_indexX_y, classified_indexX_z = group_consecutives(indexX_y, indexX_z, num2, num3)
            classified_indexY_z, classified_indexY_x = group_consecutives(indexY_z, indexY_x, num3, num1)
            classified_indexZ_y, classified_indexZ_x = group_consecutives(indexZ_y, indexZ_x, num2, num1)
            listX.append(classified_indexX_y)
            listX.append(classified_indexX_z)
            listY.append(classified_indexY_z)
            listY.append(classified_indexY_x)
            listZ.append(classified_indexZ_y)
            listZ.append(classified_indexZ_x)
            # 存放完整的未合并过的切面索引
            listXAll = [indexX_y[np.where((indexX_y<num2) & (indexX_z<num3))],indexX_z[np.where((indexX_y<num2) & (indexX_z<num3))]]
            listYAll = [indexY_z[np.where((indexY_z < num3) & (indexY_x < num1))],
                        indexY_x[np.where((indexY_z < num3) & (indexY_x < num1))]]
            listZAll = [indexZ_y[np.where((indexZ_y < num2)& (indexZ_x < num1))],
                        indexZ_x[np.where((indexZ_y < num2) & (indexZ_x < num1))]]

        else:
            classified_indexX_y, classified_indexX_z = group_consecutives(indexX_y, indexX_z, num2, num3)

            classified_indexY_x, classified_indexY_z = group_consecutives(indexY_x, indexY_z, num1, num3)

            classified_indexZ_x, classified_indexZ_y = group_consecutives(indexZ_x, indexZ_y, num1, num2)


            listX.append(classified_indexX_y)
            listX.append(classified_indexX_z)
            listY.append(classified_indexY_x)
            listY.append(classified_indexY_z)
            listZ.append(classified_indexZ_x)
            listZ.append(classified_indexZ_y)
            # 存放完整的未合并过的切面索引
            listXAll = [indexX_y[np.where((indexX_y < num2) & (indexX_z < num3))],
                        indexX_z[np.where((indexX_y < num2) & (indexX_z < num3))]]
            listYAll = [indexY_x[np.where((indexY_x < num1) & (indexY_z < num3))],
                        indexY_z[np.where((indexY_x < num1) & (indexY_z < num3))]]
            listZAll = [indexZ_x[np.where((indexZ_x < num1) & (indexZ_y < num2))],
                        indexZ_y[np.where((indexZ_x < num1) & (indexZ_y < num2))]]
        listX_withColor.append(listX)
        listY_withColor.append(listY)
        listZ_withColor.append((listZ))
        listXAll_withColor.append(listXAll)
        listYAll_withColor.append(listYAll)
        listZAll_withColor.append(listZAll)
    sayz("处理切面数据时间")
    sayz(testtime.time()-t)
    return listX_withColor, listY_withColor, listZ_withColor,listXAll_withColor, listYAll_withColor, listZAll_withColor

# 读取时间变化图、空间变化图、相空间图数据
def getData(h5FilePath,groupname, subgroupname, subsubgroupname):
    data, headList = None,None
    try:
        # 用于控制部分读取数据，数据所在subgroup未知，所以读取所在组存在数据的第一个
        if subsubgroupname == None:
            allData = getFiaData(h5FilePath, groupname, subgroupname, "null")
        # 用于打开hdf5文件读取数据
        else:
            allData = getFiaData(h5FilePath, groupname, subgroupname,subsubgroupname)
        
        FreeCAD.Console.PrintMessage("getData +++++++++++++++++++++++++++++++++ \n")
        # 获得该图对应的属性信息
        headList = allData[0]
        # 获得该图对应的数据
        data = allData[1]
        # 获得该图数据对应的维度信息
        size = allData[2]
        FreeCAD.Console.PrintMessage("getData +++++++++++++++++++++++++++++++++ \n")
        # 读取时间变化图、空间变化图、相空间图数据
        if len(allData[1]) == 1:
            data = data[0]
            size = size[0]
            # 将数据转换为对应维度
            data = np.array(data).reshape(size[0],size[1]).T
            # 得到横纵坐标轴数据
        # 读取二维等位图数据
        elif len(allData[1]) == 3:

            pass
        # 读取二维器件结构数据
        elif len(allData[1]) == 4:
            # 将数据转换为对应维度的举证
            data[3] = np.array(data[3]).astype(np.int16).reshape(size[3][0],size[3][1])

        data = np.array(data)
        if len(allData[1]) != 4 and subgroupname == "2D_struct":
            FreeCAD.Console.PrintMessage("getData +++++++++++++++++++++++++++++++++ \n")
            data = allData
        headList = np.array(headList)
    finally:
        return data, headList
def getcutData(data, headList,cutX,cutY,cutZ):
    FreeCAD.Console.PrintMessage("getcutData +++++++++++++++++++++++++++++++++ \n")
    cutdict = None
    try:
        if len(headList) == 4:
            system = headList[3].strip().replace("\n", "")
            listX, listY, listZ ,listXAll,listYAll,listZAll= dealStruct2D(data, system,cutX,cutY,cutZ)

            nameX, nameY, nameZ = struct2DInfo(headList)
            cutdict = [data[0], data[1], data[2],
                    {nameX: ["X", system, listX,listXAll], nameY: ["Y", system, listY,listYAll], nameZ: ["Z", system, listZ,listZAll]}]
        else:
            system = headList[2].strip().replace("\n", "")
            FreeCAD.Console.PrintMessage("getcutData +++++++++++++++++++++++++++++++++ \n")
            temp = [None,None,None,headList[2]]
            FreeCAD.Console.PrintMessage("getcutData +++++++++++++++++++++++++++++++++ \n")
            nameX, nameY, nameZ = struct2DInfo(temp)
            FreeCAD.Console.PrintMessage("getcutData +++++++++++++++++++++++++++++++++ \n")
            cutdict = [data[0], data[1], data[2],
                    {nameX: ["X", system, None,None], nameY: ["Y", system, None,None], nameZ: ["Z", system, None,None]},"llssb"]
            FreeCAD.Console.PrintMessage("getcutData +++++++++++++++++++++++++++++++++ \n")
    finally:
        return cutdict

"""
isExchange：将要绘制的剖面图 x、y 是否互换, True-互换, False/None：未互换
"""
def getStruct2D(cutdict,figName,figName2):
    try:
        # 判断是否存在数据
        FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
        FreeCAD.Console.PrintMessage(str(figName)+ "||" + str(figName2) +"||" + str(cutdict) +"\n")
        if cutdict.has_key(figName2):
            data = cutdict[figName2]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            xy = data[2]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            # 未合并之前的索引
            xyAll = data[3]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            cutpos = data[0]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            system = data[1]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            isExchange = True
        elif cutdict.has_key(figName):

            data = cutdict[figName]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            xy = data[2]
            # 未合并之前的索引
            xyAll = data[3]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            cutpos = data[0]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            system = data[1]
            FreeCAD.Console.PrintMessage("getStruct2D +++++++++++++++++++++++++++++++++ \n")
            isExchange = False
        else:
            return None,None,None,None,None,None,None
    except:
        sayzerr("the struct data is bad")
    else:
        return xy, xyAll,cutpos, system, isExchange

# C++传回的数据
def getFiaData(filename, groupname, subgroupname, subsubgroupname):
    # filename = "E:\\PICGUI\\QuestionFeedback\\temp (3).h5"
    # groupname = "Group_fild"
    # subgroupname = "2D_contour"
    # subsubgroupname = "subGroup111"


    import time
    t = time.time()
    data = None
    try:
        data = FreeCAD.getFigDataFromH5File(filename, groupname, subgroupname, subsubgroupname)
        FreeCAD.Console.PrintMessage(str(len(data)) + "getFiaData +++++++++++++++++++++++++++++++++ \n")
        sayzerr(filename)

    finally:
        sayzerr("C++传回数据用时")
        sayzerr(time.time() - t)
        return data

def getFigNameInfo(filename):
    # filename = "E:\\PICGUI\\QuestionFeedback\\temp (3).h5"

    import time
    t = time.time()
    sayzerr(filename)
    sayz(type(filename))
    data = None
    try:
        data = FreeCAD.getFigNameInfoListFromH5File(filename)
        sayz("成功传回2")
    finally:
        sayzerr("C++传回头部数据用时")
        sayzerr(time.time()-t)
        return data

# def getCutCoordinate(cutFigName,range):
#     NaneList = ["Y-Z","R*cos(Phi)-R*sin(Phi)","Phi-Z","Z-X","Phi-Z"]


# 观察范围格式规范函数
def range_format(num):

    num = num.replace(' ', '')
    num = num.replace('(', '').replace(')', '')
    num_arr = num.split(',', 2)
    if len(num_arr)>1:
        # sayz(num_arr)
        for index in range(len(num_arr)):
            if float(num_arr[index]) >= 0 and (not num_arr[index].startswith("+")) and (not num_arr[index].startswith("-")):
                num_arr[index] = '+' + num_arr[index].replace(' ', '')
            else:
                num_arr[index] = num_arr[index].replace(' ', '')
        if len(num_arr)  < 3:
            return '[' + num_arr[0] + ',' + num_arr[1] + ']'
        
        return '[' + num_arr[0] + ',' + num_arr[1] + ',' + num_arr[2] + ']'
    else:
        return num

# 观察范围格式规范函数
def getcutXYZ(num):
    num = num.replace(' ', '')
    num = num.replace('(', '').replace(')', '')
    num_arr = num.split(',', 2)
    # sayz(num_arr)
    for index in range(len(num_arr)):
        num_arr[index] = num_arr[index].replace(' ', '')
    if len(num_arr) == 2:
        num_arr.append("0")
    return float(num_arr[0]),float(num_arr[1]),float(num_arr[2])

# 快速找到中间值的索引
def find_close_fast(arr, e):

    low = 0
    high = len(arr) - 1
    idx = -1

    while low <= high:
        mid = int((low + high) / 2)
        if e == arr[mid] or mid == low:
            idx = mid
            break
        elif e > arr[mid]:
            low = mid
        elif e < arr[mid]:
            high = mid

    if idx + 1 < len(arr) and abs(e - arr[idx]) > abs(e - arr[idx + 1]):
        idx += 1
    return idx

# 根据数字间距划分数组
def group_consecutives(vals1, vals2, range1, range2, step=1):
    run1 = []
    run2 = []
    result1 = [run1]
    result2 = [run2]
    expect = None
    for i in range(len(vals1)):
        if (vals1[i] == expect) or (expect is None):
            if vals1[i] < range1:
                run1.append(vals1[i])
            else:
                run1.append(range1-1)
            if vals2[i] < range2:
                run2.append(vals2[i])
            else:
                run2.append(range2 - 1)

        else:

            if vals1[i] < range1:
                run1 = [vals1[i]]
            else:
                run1= [range1 - 1]
            if vals2[i] < range2:
                run2 = [vals2[i]]
            else:
                run2=[range2 - 1]
            result1.append(run1)
            result2.append(run2)
        expect = vals1[i] + step

    return result1, result2

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')

def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')