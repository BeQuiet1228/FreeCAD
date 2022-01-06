# -*- coding: UTF-8 -*-

from PySide import QtGui, QtCore
from pylab import *
import os

import FreeCAD
import FreeCADGui
import vPlot
import VisualizationFigTree
import VisualizationGui
import VisualizationResult
import VisualizationPlot
import subprocess
import json
from File.FileCommand.M3DFile.M3DFileUtil import M3DFileUtil


# 执行文件路径
EXE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# 三维可视化执行文件路径
EXE_PATH_3D = EXE_PATH + '\\Package\\visualizationPlot3D\\Visualization3D.exe '
# # 解析 h5 执行文件路径
# EXE_PATH_H5 = EXE_PATH + '\\Package\\readHdf5\\readHdf5.exe '

# 存放获取到的struct数据
STRUCTDATA = None
# 存放计算得到的切面数据
CUTDATA = None
# 存放二维器件结构的属性信息
STRUCTHEADLIST = None

def deleteData():
    """
    docstring
    """
    global STRUCTDATA
    global CUTDATA
    global STRUCTHEADLIST

    # 存放获取到的struct数据
    STRUCTDATA = None
    # 存放计算得到的切面数据
    CUTDATA = None
    # 存放二维器件结构的属性信息
    STRUCTHEADLIST = None


import LoadingMain
loading = LoadingMain.LoadingWidget()
loading.setWindowFlags(QtCore.Qt.FramelessWindowHint)
loading.setAttribute(QtCore.Qt.WA_TranslucentBackground)

class PlotTree(QtGui.QDockWidget):
    def __init__(self, parent=None):
        super(PlotTree, self).__init__(parent)
        self.ui = VisualizationGui.plotTree.TreeStructPal.Ui_DockWidget_plotTree()
        self.ui.setupUi(self)

        # 解决QTreeWidget中的内容超出边界后自动隐藏的问题
        self.ui.treeWidget_plotTree.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.ui.treeWidget_plotTree.header().setStretchLastSection(False)
        self.ui.treeWidget_plotTree.setAutoScroll(False)

        # 去除标题栏
        self.setTitleBarWidget(QtGui.QWidget(None))
        #用于标志当前是二维等位图还是三维等位图:1表示2D；6表示3D
        self.flag2DOr3D=1

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
                # self.qtab.addTab(self, u'运行结果')
                self.qtab.insertTab(self.qtab.count()-1, self, u'运行结果')
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
        # mdi = vPlot.getMdiArea()
        # mdi.subWindowActivated.connect(self.updateTreeNode)

    def onClick(self, item, column):
        """
        picInfo：图像信息，包括图像类型、索引、（路径）
        picType：图像类型，1-二维等位图，2-时间观测图，3-二维矢量图，4-空间变化图，5-相空间图，6-三维等位图，7-器件结构图
        picIndex：图像索引
        picPath：三维图对应 h5 文件路径，二维图对应 json 文件路径
        contourType：二维等位图类型
        itemName：节点名称
        h5Path：h5 文件路径
        """
        picInfo = item.data(0, QtCore.Qt.UserRole)
        picType = picInfo[0]
        picIndex = picInfo[1]
        itemName = item.text(0)
        # 恢复其余的item text
        recoverAllItemName()
        # 除了器件结构，其余图像根节点不执行任何命令
        if picIndex == 0:
            # if picType == 7:
            if picType == 4:
                # h5Path 为 h5 文件的路径，需要从任务控制部分获取
                # h5Path = "E:\\PICGUI\\data\\temp_Temp.h5"
                # readHdf5_control(h5Path, picType, picIndex)
                if FreeCAD.clientIsEnable():
                    if "[正在接收文件...]" not in itemName:
                        item.setText(0, itemName + u"[正在接收文件...]")
                FreeCAD.clientSendWinMsg(109, picType, picIndex)
            #三维粒子图
            elif picType ==8:
                if FreeCAD.clientIsEnable():
                    self.flag2DOr3D=1
                    sayz("PICTYPE==1\n")
                    if "[正在接收文件...]" not in itemName:
                        item.setText(0, itemName + u"[正在接收文件...]")
                FreeCAD.clientSendWinMsg(109, 7, 0)
            else:
                return
                pass
        else:
            if picType == 4:
                # 器件结构图数据曾经获取过，器件结构的数据第一次获取后就不再删除
                picPath = picInfo[2]
                # 三维立体图
                if picIndex == 1:
                    if len(CUTDATA) == 5:
                        figname = itemName
                        if not isExisted(figname):
                            # 新建一个窗口
                            fig,flag = vPlot.figure(True,figname)
                            # 在打开结果中新增item
                            VisualizationFigTree.addStrcutItem(figname, 3)
                            # 验证获取的器件结构数据有效
                            if CUTDATA is not None:

                                # 得到剖面图数据
                                cutAB, xyAll, cutpos, system, isExchange = VisualizationResult.getStruct2D(CUTDATA[3],
                                                                                                        figname,
                                                                                                        figname)

                                #if cutAB is not None:
                                FreeCAD.Console.PrintMessage(" +++++++++++++++++++++++++++++++++ \n")
                                VisualizationPlot.drawCut(cutAB,xyAll, figname, CUTDATA, cutpos, system, None)

                                recoverItemName(picType, picIndex)
                    else:
                        fileName = picPath
                        # strcuctDataPath = json.loads(FreeCAD.ActiveDocument.LicenseURL)
                        # strcuctFilePath = strcuctDataPath.split('_json')[0] + ".H5"
                        strcuctFilePath = os.path.dirname(fileName) + "\\TEMP.H5"
                        structNameFilePath = os.path.dirname(fileName) + "\\structName.json"
                        # 先把UTF-8转成万国码在转成GBK
                        fileName = fileName.decode('utf-8').encode('gbk')
                        strcuctFilePath = strcuctFilePath.decode('utf-8').encode('gbk')
                        structNameFilePath = structNameFilePath.decode('utf-8').encode('gbk')
                        subprocess.Popen(EXE_PATH_3D +  '"'+ fileName + '"'+ ' '+'"' + strcuctFilePath + '"'+ ' '+'"' + structNameFilePath + '"' + ' STRUCT3D ' + 'struct3D')
                        sayz(item.text(0) + u"开始绘制...")
                        recoverItemName(picType, picIndex)
                else:
                    figname = itemName
                    if not isExisted(figname):
                        # 新建一个窗口
                        fig,flag = vPlot.figure(True,figname)
                        # 在打开结果中新增item
                        VisualizationFigTree.addStrcutItem(figname, 3)
                        # 验证获取的器件结构数据有效
                        if CUTDATA is not None:

                            # 得到剖面图数据
                            cutAB, xyAll, cutpos, system, isExchange = VisualizationResult.getStruct2D(CUTDATA[3],
                                                                                                     figname,
                                                                                                     figname)

                            #if cutAB is not None:
                            FreeCAD.Console.PrintMessage(" +++++++++++++++++++++++++++++++++ \n")
                            VisualizationPlot.drawCut(cutAB,xyAll, figname, CUTDATA, cutpos, system, None)

                            recoverItemName(picType, picIndex)
            elif picType==7:
                if FreeCAD.clientIsEnable():
                    self.flag2DOr3D=7
                    sayz("PICTYPE==6\n")
                    if "[正在接收文件...]" not in itemName:
                        item.setText(0, itemName + u"[正在接收文件...]")
                FreeCAD.clientSendWinMsg(109, 1, picIndex)
            else:
                # h5Path 为 h5 文件的路径，需要从任务控制部分获取
                # h5Path = "E:\\PICGUI\\data\\temp_Temp.h5"
                # readHdf5_control(h5Path, picType, picIndex)
                if FreeCAD.clientIsEnable():
                    self.flag2DOr3D=1
                    sayz("PICTYPE==1\n")
                    if "[正在接收文件...]" not in itemName:
                        item.setText(0, itemName + u"[正在接收文件...]")
                FreeCAD.clientSendWinMsg(109, picType, picIndex)
        # loading.show()
        # loading.exec_()
        sayz(picInfo)

    def show(self, *args, **kwargs):
        super(PlotTree, self).show()
        self.setAutoFillBackground(True)

#@fubiao
CONTOUR2D=1
PHASESPACE=2
OBSERVE=3
DATASTRUCT=4
VECTOR=5
RANGE=6
CONTOUR3D=7
PHASESPACE3D = 8
# 二维等问题与三维等位图的对应关系
class Contour2DToContour3D():
    data={}


class FlagM3dEditorWorkbrenchFile():
    # 当前是否在编辑m3d文件工作台,为“”表示在Simulation工作台，否则在Editor
    flagM3dEditorWorkbrenchFile=""
    # M3d Editor 工作台下获得m3d中的数据
    M3dEditorPolt=[]
#end
plotTree = PlotTree()
# 显示绘图结果列表
VisualizationFigTree.showfigTree()
# 树节点上存放的数据格式为：[1, 1, False], 第一个表示图像类型，第二个表示图像顺序，第三个表示是否为shade图
def showPlotTree(filePath=""):
    sayz('=======================')
    sayz(filePath)
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
    tab.setCurrentIndex(plotTree.treeIndex)
    tree = plotTree.ui.treeWidget_plotTree
    tree.clear()
    # 等位图观测类型
    showType = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3"]
    plotTree.show()


    # 测试数据
    contourName = [["CONTOUR FIELD E3 ConformalArea004 DefTimer", True], ["CONTOUR FIELD B2 ConformalArea004 DefTimer", False]]
    vectorName = ["VECTOR FIELD E1,E1 ConformalArea003 DefTimer", "VECTOR FIELD E1,E1 ConformalArea003 DefTimer"]
    phasespaceName = ["PHASESPACE AXES X3,X1 DefTimer", "PHASESPACE AXES X2,X1 DefTimer",
                      "PHASESPACE AXES X3,P3 DefTimer", "PHASESPACE AXES X3,P1 DefTimer",
                      "PHASESPACE AXES X3,X1 DefTimer", "PHASESPACE AXES X2,X1 DefTimer",
                      "PHASESPACE AXES X3,P3 DefTimer", "PHASESPACE AXES X3,P1 DefTimer"]
    observeName = ["OBSERVE FIELD_INTEGRAL E.DL ConformalLine001", "OBSERVE FIELD_INTEGRAL E.DL ConformalLine001"]
    rangeName = ["RANGE FIELD E3 ConformalLine002 DefTimer", "RANGE FIELD B1ST ConformalLine002 DefTimer",
                 "RANGE FIELD B3ST ConformalLine002 DefTimer", "RANGE FIELD E3 ConformalLine002 DefTimer",
                 "RANGE FIELD B1ST ConformalLine002 DefTimer", "RANGE FIELD B3ST ConformalLine002 DefTimer"]

    if filePath=="":
        # 获取m3d文件中的图像名称
        m3dFile = M3DFileUtil()
        contourName = m3dFile.getContourGraphName()
        vectorName = m3dFile.getVectorGraphName()
        phasespaceName = m3dFile.getPhasespaceGraphName()
        observeName = m3dFile.getObserveGraphName()
        rangeName = m3dFile.getRangeGraphName()
        FlagM3dEditorWorkbrenchFile.flagM3dEditorWorkbrenchFile=""

    else:
        m3dFile = M3DFileUtil(path=filePath)
        FlagM3dEditorWorkbrenchFile.M3dEditorPolt=m3dFile.getPoltNameForM3dFileEditor()
        contourName=FlagM3dEditorWorkbrenchFile.M3dEditorPolt[0]
        vectorName=FlagM3dEditorWorkbrenchFile.M3dEditorPolt[1]
        phasespaceName=FlagM3dEditorWorkbrenchFile.M3dEditorPolt[2]
        observeName=FlagM3dEditorWorkbrenchFile.M3dEditorPolt[3]
        rangeName=FlagM3dEditorWorkbrenchFile.M3dEditorPolt[4]

        FlagM3dEditorWorkbrenchFile.flagM3dEditorWorkbrenchFile=filePath

    # FreeCAD.Console.PrintMessage("\ncontourName\n")
    # FreeCAD.Console.PrintMessage(contourName)
    # FreeCAD.Console.PrintMessage("\ncontourName\n")
    # FreeCAD.Console.PrintMessage("\nvectorName\n")
    # FreeCAD.Console.PrintMessage(vectorName)
    # FreeCAD.Console.PrintMessage("\nvectorName\n")
    # FreeCAD.Console.PrintMessage("\nphasespaceName\n")
    # FreeCAD.Console.PrintMessage(phasespaceName)
    # FreeCAD.Console.PrintMessage("\nphasespaceName\n")
    # FreeCAD.Console.PrintMessage("\nobserveName\n")
    # FreeCAD.Console.PrintMessage(observeName)
    # FreeCAD.Console.PrintMessage("\nobserveName\n")
    # FreeCAD.Console.PrintMessage("\nrangeName\n")
    # FreeCAD.Console.PrintMessage(rangeName)
    # FreeCAD.Console.PrintMessage("\nrangeName\n")

    # 去掉多余\n和！！注释
    contourNameList = []
    for command in contourName:
        if type(command) == list and len(command) >1:
            for name in command[0].split('\n'):
                if name != '' and  not ('!!' in name):
                    contourNameList.append([str(name)+'\n',command[1]])
    vectorNameList = []
    for command in vectorName:
        for name in command.split('\n'):
            if name != '' and not ('!!' in name):
                vectorNameList.append(str(name) + '\n')
    phasespaceNameList = []
    for command in phasespaceName:
        for name in command.split('\n'):
            if name != '' and not ('!!' in name):
                phasespaceNameList.append(str(name) + '\n')
    rangeNameList = []
    for command in rangeName:
        for name in command.split('\n'):
            if name != '' and not ('!!' in name):
                rangeNameList.append(str(name) + '\n')
    # 将含有FFT字段分成两部分
    observeNameList = []
    for command in observeName:
        for name in command.split('\n'):
            if name != '' and not ('!!' in name):
                #救急只举，请勿吐槽
                name = name.upper()
                if " FFT " in name:
                    observeNameList.append((name.split('FFT')[0]).rstrip() + ';\n')
                observeNameList.append(str(name) + '\n')

    # 用于测试
    if len(contourName) <= 0:
       contourName = [["CONTOUR FIELD E3 ConformalArea004 DefTimer", True],
                      ["CONTOUR FIELD B2 ConformalArea004 DefTimer", False]]

    # allName = [contourName, observeName, vectorName, rangeName, phasespaceName]
    allName = [contourNameList, phasespaceNameList, observeNameList, vectorNameList, rangeNameList]

    # sayz(allName)

    # 添加根节点
    addChild(plotTree.ui, u"二维等位图", [1, 0])
    addChild(plotTree.ui, u"相空间图", [2, 0])
    addChild(plotTree.ui, u"时间观测图", [3, 0])
    addChild(plotTree.ui, u"器件结构图", [4, 0])
    addChild(plotTree.ui, u"二维矢量图", [5, 0])
    addChild(plotTree.ui, u"空间变化图", [6, 0])
    addChild(plotTree.ui, u"三维等位图", [7, 0])
    addChild(plotTree.ui, u"三维粒子图", [8, 0])
    # addChild(plotTree.ui, u"二维等位图", [1, 0])
    # addChild(plotTree.ui, u"时间观测图", [2, 0])
    # addChild(plotTree.ui, u"二维矢量图", [3, 0])
    # addChild(plotTree.ui, u"空间变化图", [4, 0])
    # addChild(plotTree.ui, u"相空间图", [5, 0])
    # addChild(plotTree.ui, u"三维等位图", [6, 0])
    # addChild(plotTree.ui, u"器件结构图", [7, 0])

    # 添加子节点
    for i in range(len(allName)-1, -1, -1):
        for j in range(len(allName[i])):
            if i <=2:
                addChild(plotTree.ui, allName[i][j], [i + 1, j + 1, False])
            else:
                addChild(plotTree.ui, allName[i][j], [i + 2, j + 1, False])
        # 删除没有子节点的根节点
        # if len(allName[i]) <= 0:
        #     tree.takeTopLevelItem(tree.indexOfTopLevelItem(tree.topLevelItem(i)))
    Contour2DToContour3D.data={}
    # 添加三维等位图列表
    for i in range(len(contourName)):
        contourNameArray = contourName[i][0].split(" ")
        thisType = contourNameArray[2]
        if thisType in showType:
            contour3DName = contourNameArray[2] + " " + contourNameArray[3] + " " + contourNameArray[4] + " 3D"
            # addChild(plotTree.ui, contour3DName, [6, i + 1, False])
            addChild(plotTree.ui, contour3DName, [7, i + 1, False])
            Contour2DToContour3D.data[i+1]=len(Contour2DToContour3D.data)+1



#关闭分支树
def cloePlotTree():
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
    # sayz(plotTree.treeIndex)
    # sayz("lllllllllllllllll")
    tab.setCurrentIndex(plotTree.treeIndex)
    tree = plotTree.ui.treeWidget_plotTree
    tree.clear()
    plotTree.show()

# 添加树节点
def addChild(tree, itemName, itemData):
    item = QtGui.QTreeWidgetItem()
    if type(itemName) != list:
        item.setText(0, itemName)
    else:
        # 等位图中包含shade信息，itemName[1] == True (Shade)
        item.setText(0, itemName[0])
        itemData[2] = itemName[1]

    item.setData(0, QtCore.Qt.UserRole, itemData)
    rootIndex = itemData[0] - 1
    index = itemData[1]
    # 根节点
    if index == 0:
        item.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Group.svg"))
        tree.treeWidget_plotTree.addTopLevelItem(item)
    # 子节点
    else:
        item.setIcon(0, QtGui.QIcon(FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/Item.svg"))
        tree.treeWidget_plotTree.topLevelItem(rootIndex).addChild(item)

def recoverItemName(topIndex, index):
    sayz("\nREMOVE\n")
    FreeCAD.Console.PrintMessage("topIndex: "+str(topIndex)+"  index: "+str(index)+"\n")
    item=None
    #表示是期间结构
    if index<0 and topIndex==4:
        item=plotTree.ui.treeWidget_plotTree.topLevelItem(topIndex-1)
    elif index<0:
        sayz("索引错误！\n")
        return
    elif topIndex==8:
        item = plotTree.ui.treeWidget_plotTree.topLevelItem(topIndex - 1)
    else:
        item = plotTree.ui.treeWidget_plotTree.topLevelItem(topIndex-1).child(index-1)
    itemText = item.text(0)
    sayz(item.text(0))
    item.setText(0, itemText.split("[")[0])

def recoverAllItemName():

    rootCount = plotTree.ui.treeWidget_plotTree.topLevelItemCount()
    # 遍历所有的树节点
    for i in range(rootCount):
        rootItem = plotTree.ui.treeWidget_plotTree.topLevelItem(i)
        secondCount = rootItem.childCount()
        for j in range(secondCount):
            second = rootItem.child(j)
            itemText = second.text(0)
            sayz(second.text(0))
            second.setText(0, itemText.split("[")[0])

def getStuctName_control():
    if FlagM3dEditorWorkbrenchFile.flagM3dEditorWorkbrenchFile=="":
        # 获得m3d的util
        fileUtil = M3DFileUtil()
        # 获得最近的m3d字符串
        structNameStr = fileUtil.getStructNameStr()
    else:
        fileUtil = M3DFileUtil(path=FlagM3dEditorWorkbrenchFile.flagM3dEditorWorkbrenchFile)
        structNameStr=FlagM3dEditorWorkbrenchFile.M3dEditorPolt[5]
    nameStrList = structNameStr.split('\n')
    nameList = []
    
    import re
    for line in nameStrList:
        if line.endswith(";"):
            # 按空格或;分割
            name = re.split(' |;',line)[1]
            nameList.append(name)
    name_dict = {}
    name_dict['name'] = nameList
    # 获取写入路径
    nameJsonPath = FreeCAD.clientUserDir()
    with open(nameJsonPath + '\\' + "structName.json", "w") as f:
        json.dump(name_dict, f)


# 任务控制部分读取 h5 文件写出器件结构数据，调用时需要传入.h5文件路径
def readStructHdf5_control(filePath):
    # 获取器件结构数据
    global STRUCTDATA
    global STRUCTHEADLIST
    global CUTDATA

    FreeCAD.Console.PrintMessage("readStructHdf5_control +++++++++++++++++++++++++++++++++ \n")

    filePath = filePath.decode('gbk').encode('utf-8')

    try:
        STRUCTDATA, STRUCTHEADLIST = VisualizationResult.getData(filePath, "Group_kmat", "2D_struct", "2D_struct")
        CUTDATA = VisualizationResult.getcutData(STRUCTDATA, STRUCTHEADLIST, None, None, None)
        FreeCAD.Console.PrintMessage("readStructHdf5_control ----------- +++++++++++++++++++++++++++++++++ \n")
    finally:
        pass
    FreeCAD.Console.PrintMessage("readStructHdf5_control +++++++++++++++++++++++++++++++++ \n")
    if CUTDATA is not None and (len(CUTDATA) == 4 or len(CUTDATA) == 5):
        # 表示是期间结构
        item = plotTree.ui.treeWidget_plotTree.topLevelItem(3)
        FreeCAD.Console.PrintMessage("readStructHdf5_control +++++++++++++++++++++++++++++++++ \n")
        if item.childCount()<4:
            if len(CUTDATA) == 5:
                nameDict = CUTDATA[3]
                figName = nameDict.keys()[0]
                addChild(plotTree.ui, figName, [4, 1, filePath], )
                plotTree.update()
            else:
                # 在运行结果树中添加结构图的item
                # 添加三维立体
                figName = u'三维立体图'
                addChild(plotTree.ui, figName, [4, 1, filePath], )
                FreeCAD.Console.PrintMessage("readStructHdf5_control +++++++++++++++++++++++++++++++++ \n")
                # sayz(root)
                i = 1
                nameDict = CUTDATA[3]
                # sayz("file: "+str(thisFiles))
                for figName in nameDict.keys():
                    i += 1
                    addChild(plotTree.ui, figName, [4, i, filePath])
                    FreeCAD.Console.PrintMessage("readStructHdf5_control 11111111111+++++++++++++++++++++++++++++++++ \n")
                sayzerr("additem")
                plotTree.update()
        getStuctName_control()

        return 'analyze success\n'
    else:
        return 'data is incorrect'
    # return output


# 任务控制部分读取 h5 文件并绘图，调用时需要传入.h5文件路径和节点上存放list的list[2]
# list[0]图像类型,list[1]图像顺序, list[2]是否为Shade
def readHdf5_control(filePath, picType, picIndex):
    """
    filePath：h5 文件路径
    contourType：二维等位图类型
    picType：图像类型，1-二维等位图，2-时间观测图，3-二维矢量图，4-空间变化图，5-相空间图，6-三维等位图，7-器件结构图
    dataPath：json 数据路径
    """

    filePath = filePath.decode('gbk').encode('utf-8')
    # sayz(picType)
    if picType == 1:
        FreeCAD.Console.PrintMessage("flag2DOr3D:"+str(plotTree.flag2DOr3D)+"\n")
        if plotTree.flag2DOr3D==7:
            # 三维等位图

            # if not os.path.exists(filePath) and not os.path.exists(os.path.dirname(filePath) + "\\TEMP.H5"):
            #     sayzerr("contour3D data is not existed")
            #     sayz("LOG:1")
            #     sayz("CONTOUR3D:")
            #     sayz(str(CONTOUR3D))
            #     sayz("Contour2DToContour3D[picIndex]")
            #     sayz(Contour2DToContour3D.data[picIndex])
            #     # FreeCAD.Console.PrintMessage("CONTOUR3D: "+str(CONTOUR3D)+" Contour2DToContour3D: "+str(Contour2DToContour3D[picIndex])+"\n")
            #     sayz("LOG:2")
            #     recoverItemName(CONTOUR3D, Contour2DToContour3D.data[picIndex])
            #     return
            data, headList = VisualizationResult.getData(filePath, "Group_fild", "3D_fieldem", None)
            figname = headList[-1]
            # 传文件路径绘图
            # strcuctDataPath = json.loads(FreeCAD.ActiveDocument.LicenseURL)
            # strcuctFilePath = strcuctDataPath.split('_json')[0]+".H5"
            strcuctFilePath = os.path.dirname(filePath) + "\\TEMP.H5"

            structNameFilePath = os.path.dirname(filePath) + "\\structName.json"

            # 先把UTF-8转成万国码在转成GBK
            filePath = filePath.decode('utf-8').encode('gbk')
            figname = figname.decode('utf-8').encode('gbk')
            strcuctFilePath = strcuctFilePath.decode('utf-8').encode('gbk')
            structNameFilePath = structNameFilePath.decode('utf-8').encode('gbk')
            subprocess.Popen(
                EXE_PATH_3D + '"' + filePath+ '"' + ' ' + '"' + strcuctFilePath + '"' + ' ' + '"' +  structNameFilePath + '"' + ' CONTOUR3D ' + '"' + figname + '"')
            sayz(figname + u"开始绘制...")

            sayz(Contour2DToContour3D.data)
            index=Contour2DToContour3D.data[picIndex]
            sayz("picIndex: "+str(picIndex))
            sayz(index)
            recoverItemName(7,index)
        if plotTree.flag2DOr3D==1:
            # 二维等位图
            recoverItemName(picType, picIndex)
            # 等位图
            # Simulation
            if FlagM3dEditorWorkbrenchFile.flagM3dEditorWorkbrenchFile=="":
                m3dFile = M3DFileUtil()
                contourName = m3dFile.getContourGraphName()
            # M3dEditor
            else:
                contourName=FlagM3dEditorWorkbrenchFile.M3dEditorPolt[0]
            # 用于测试
            if len(contourName) <= 0:
                contourName = [["CONTOUR FIELD E3 ConformalArea004 DefTimer", True],
                            ["CONTOUR FIELD B2 ConformalArea004 DefTimer", False]]


            contourType = contourName[picIndex-1][1]

            try:
                # 获取对应的等位图数据
                contourData, headList = VisualizationResult.getData(filePath, "Group_fild", "2D_contour", None)

                # 获取对应的属性信息
                x_label, y_label, time, component, range_start, range_end, range_min, range_max, step = VisualizationResult.contourInfo(
                    headList)
                FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                # 验证获取的属性信息有效,以便可以正确绘图
                if step is not None and headList.shape[0]>14:
                    # a = contourData[0]
                    # b = contourData[1]
                    # c = contourData[2]
                    a, b, c = VisualizationResult.dealContourData(contourData, [x_label, y_label])
                    # 获取图名
                    figname = headList[-1] + '_' + headList[14].strip().split(' ', 3)[1] + '_' + time
                    FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                    #绘制等比等位图并关掉
                    import time as time2
                    t = time2.time()
                    # 验证获取的器件结构数据有效
                    if STRUCTDATA is not None:
                        FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                        cutx, cuty, cutz = VisualizationResult.getcutXYZ(range_start)
                        # 获取二维器件结构数据
                        FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                        cutDict = VisualizationResult.getcutData(STRUCTDATA, STRUCTHEADLIST, cutx, cuty, cutz)
                        FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                        cut_figName = x_label.split(" ", 1)[0] + "-" + y_label.split(" ", 1)[0]
                        cut_figName2 = y_label.split(" ", 1)[0] + "-" + x_label.split(" ", 1)[0]
                        FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                        # 得到剖面图数据
                        FreeCAD.Console.PrintMessage(str(len(cutDict)) + "+++++++++++++++++++++++++++++++++ \n")
                        cutAB, xyAll, cutpos, system, isExchange = VisualizationResult.getStruct2D(cutDict[3],
                                                                                                   cut_figName,
                                                                                                   cut_figName2)
                        # 绘制等位图
                        FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                        if not contourType:
                            # 在打开结果中新增item
                            itemData = VisualizationFigTree.getItemDataByfigName(figname, 0)
                            FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                            # 新建一个窗口，显示等比绘图
                            fig2, flag = vPlot.figure(False, figname + "_" + str(itemData[1] + 1) + "_GeometricRatio")
                            # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                            fig2.setVisible(False)
                            VisualizationPlot.drawContour(None, None, x_label, y_label, system,time, component,
                                                          VisualizationResult.range_format(range_start),
                                                          VisualizationResult.range_format(range_end), range_min, range_max,
                                                          step,
                                                          a, b, c, 'line', 1)
                        else:
                            # 在打开结果中新增item
                            itemData_shade = VisualizationFigTree.getItemDataByfigName(figname + "_Shade", 0)
                            FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")
                            # 新建一个窗口，显示等比绘图
                            fig2, flag = vPlot.figure(False, figname +"_Shade" + "_" + str(itemData_shade[1] + 1) + "_GeometricRatio")
                            # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                            fig2.setVisible(False)
                            VisualizationPlot.drawContour(None, None, x_label, y_label, system,time, component,
                                                          VisualizationResult.range_format(range_start),
                                                          VisualizationResult.range_format(range_end), range_min, range_max,
                                                          step,
                                                          a, b, c, 'shade', 1)
                        FreeCAD.Console.PrintMessage("tree contour +++++++++++++++++++++++++++++++++ \n")

                        sayz("tttttttttime1\n")
                        sayz(time2.time() - t)

                        if cutAB is not None:
                            # "contour-contour",标志等位图
                            VisualizationPlot.drawCut(cutAB,xyAll, "contour-contour", cutDict, cutpos, system, isExchange)

                        vPlot.closePlot()
                        sayz("tttttttttime2\n")
                        sayz(time2.time() - t)
                        # 绘制等位图
                        if not contourType:
                            # 在打开结果中新增item
                            # itemData = VisualizationFigTree.getItemDataByfigName(figname,0)

                            # 新建一个窗口
                            # 第一个参数为True时，代表为控制部分绘图结果，关闭时需要同时删除树结构中item
                            fig,flag = vPlot.figure(True,figname+"_"+ str(itemData[1]+1))
                            # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                            fig.setVisible(False)
                            VisualizationFigTree.addSubChild(figname,itemData)
                            VisualizationPlot.drawContour(None, None, x_label, y_label, system,time, component,
                                                        VisualizationResult.range_format(range_start),
                                                        VisualizationResult.range_format(range_end), range_min, range_max,
                                                        step,
                                                        a, b, c, 'line',0)


                        else:
                            # 在打开结果中新增item
                            # itemData = VisualizationFigTree.getItemDataByfigName(figname+"_shade", 0)

                            # 添加图
                            fig,flag = vPlot.figure(True,figname+"_Shade" +"_"+  str(itemData_shade[1] + 1))
                            # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                            fig.setVisible(False)
                            VisualizationFigTree.addSubChild(figname+"_Shade", itemData_shade)
                            VisualizationPlot.drawContour(None, None, x_label, y_label, system,time, component,
                                                        VisualizationResult.range_format(range_start),
                                                        VisualizationResult.range_format(range_end), range_min, range_max,
                                                        step,
                                                        a, b, c, 'shade',0)

                        sayz("tttttttttime3\n")
                        sayz(time2.time() - t)
                        # # 验证获取的器件结构数据有效
                        # if STRUCTDATA is not None:
                        # cutx, cuty, cutz = VisualizationResult.getcutXYZ(range_start)
                        # # 获取二维器件结构数据
                        # cutDict = VisualizationResult.getcutData(STRUCTDATA, STRUCTHEADLIST, cutx, cuty, cutz)
                        # cut_figName = x_label.split(" ", 1)[0].split("(m)")[0] + "-" + y_label.split(" ", 1)[0].split("(m)")[0]
                        # cut_figName2 = y_label.split(" ", 1)[0].split("(m)")[0] + "-" + x_label.split(" ", 1)[0].split("(m)")[0]
                        #
                        # # 得到剖面图数据
                        # cutA, cutB, cutpos, system, isExchange = VisualizationResult.getStruct2D(cutDict[3], cut_figName,
                        #                                                      cut_figName2)
                        #if cutAB is not None:
                        VisualizationPlot.drawCut(cutAB,xyAll,  "contour-contour", cutDict, cutpos, system, isExchange)
                    sayz("tttttttttime4\n")
                    sayz(time2.time()-t)
                    fig.setVisible(True)
            finally:
                sayz("绘制二维等位图")

    elif picType == 3:
        recoverItemName(picType, picIndex)
        data, headList = VisualizationResult.getData(filePath, "Group_grid", "2D_observe", None)

        # 获取时间变化图的附加信息
        x_label, y_label, type, range_min, range_max = VisualizationResult.observeInfo(headList)
        # 验证数据有效
        if x_label is not None and headList.shape[0] > 3:
            # 获取时间变化图的数据
            x, y = None, None
            if data is not None and data.shape[0] > 1:
                x = data[0]
                y = data[1]

            field = headList[3].strip().split('-', 1)[0]
            figname = headList[-1] + '_' + field + '_' + type
            # 在打开结果中新增item
            itemData = VisualizationFigTree.getItemDataByfigName(figname, 2)
            # 新建一个窗口
            fig,flag = vPlot.figure(True,figname + "_"+ str(itemData[1] + 1))
            VisualizationFigTree.addSubChild(figname, itemData)

            VisualizationPlot.drawObserve(x_label, y_label, type, VisualizationResult.range_format(range_min),
                                          VisualizationResult.range_format(range_max), x, y)
    elif picType == 5:


        data, headList = VisualizationResult.getData(filePath, "Group_fild", "2D_vectors", None)
        x_label, y_label, component, time,cut_position, max_vector = VisualizationResult.vectorInfo(
            headList)
        a, b, c = None, None, None
        if data is not None and data.shape[0] > 2:
            a = data[0]
            b = data[1]
            c = data[2]
        if x_label is not None:
            figname = headList[-1] + "_" + component
            # 在打开结果中新增item
            itemData = VisualizationFigTree.getItemDataByfigName(figname, 4)
            # 新建一个窗口
            fig,flag = vPlot.figure(True,figname + "_"+ str(itemData[1] + 1))
            VisualizationFigTree.addSubChild(figname, itemData)
            # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
            fig.setVisible(False)
            VisualizationPlot.drawVector(None, None, x_label, y_label, component, time, cut_position, max_vector, a, b, c)

            # 得到剖面图数据
            # 验证获取的器件结构数据有效
            # if CUTDATA is not None:
            if STRUCTDATA is not None:
                # 得到的坐标轴标识
                cut_figName = x_label.split(" ", 1)[0].split("(m)")[0] + "-" + y_label.split(" ", 1)[0].split("(m)")[0]
                cut_figName2 = y_label.split(" ", 1)[0].split("(m)")[0] + "-" + x_label.split(" ", 1)[0].split("(m)")[0]
                #将X2-X3等cut_figname进行规范化
                cut_figName = cut_figName.replace("X1","X").replace("X2","Y").replace("X3","Z")
                cut_figName2 = cut_figName2.replace("X1", "X").replace("X2", "Y").replace("X3", "Z")
                #根据横切位置获取截面数据
                cutx, cuty, cutz = VisualizationResult.getVectorCut(STRUCTHEADLIST, cut_figName,cut_figName2,cut_position)
                # 获取二维器件结构数据
                cutDict = VisualizationResult.getcutData(STRUCTDATA, STRUCTHEADLIST, cutx, cuty, cutz)

                cutAB, xyAll, cutpos, system, isExchange = VisualizationResult.getStruct2D(cutDict[3], cut_figName,
                                                                                         cut_figName2)

                #if cutAB is not None:
                VisualizationPlot.drawCut(cutAB,xyAll, None, CUTDATA, cutpos, system, isExchange)
            fig.setVisible(True)
            recoverItemName(picType, picIndex)
    elif picType == 6:


        data, headList = VisualizationResult.getData(filePath, "Group_grid", "2D_rangers", None)
        x_label, y_label, time, component, range_min, range_max = VisualizationResult.rangeInfo(
                headList)
        # 验证数据有效
        if x_label is not None:
            x, y = None, None
            if data is not None and data.shape[0] > 1:
                x = data[0]
                y = data[1]
            figname = headList[-1] + "_" + component
            # 在打开结果中新增item
            itemData = VisualizationFigTree.getItemDataByfigName(figname, 5)
            # 新建一个窗口
            fig,flag = vPlot.figure(True,figname + "_"+ str(itemData[1] + 1))
            VisualizationFigTree.addSubChild(figname, itemData)
            VisualizationPlot.drawRange(x_label, y_label, time, component,
                                        VisualizationResult.range_format(range_min),
                                        VisualizationResult.range_format(range_max), x, y)
            recoverItemName(picType, picIndex)
    elif picType == 2:

        data, headList = VisualizationResult.getData(filePath,"Group_part", "2D_phaseSpace", None)
        x_label, y_label, particle, time = VisualizationResult.phasespaceInfo(headList)
        # 验证数据有效
        if x_label is not None:
            sayz("1")
            x, y = None, None
            if data is not None and data.shape[0] > 1:
                x = data[0]
                y = data[1]
                z = data[2]

            sayz("2")
            figname = headList[-1] + "_" + particle
            sayz("3")
            # 在打开结果中新增item
            sayz("4")
            itemData = VisualizationFigTree.getItemDataByfigName(figname, 1)
            sayz("5")
            # 新建一个窗口
            fig,flag = vPlot.figure(True,figname + "_"+ str(itemData[1] + 1))
            sayz("6")
            VisualizationFigTree.addSubChild(figname, itemData)
            sayz("7")
            
            if CUTDATA is not None:
                system=CUTDATA[3].values()[0][1]
                
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
                        sayz("8")
                        # 为保证一起出现，先设置不可见，等会之完成后，在设置为可见
                        fig.setVisible(False)
                        VisualizationPlot.drawPhasespace(None, None, x_label, y_label, particle, time, x, y,z)
                        sayz("8.5")
                        cut_figName = x_label.split(" ", 1)[0] + "-" + y_label.split(" ", 1)[0]
                        cut_figName2 = y_label.split(" ", 1)[0] + "-" + x_label.split(" ", 1)[0]
                        # 得到剖面图数据
                        cutAB, xyAll, cutpos, system, isExchange = VisualizationResult.getStruct2D(CUTDATA[3], cut_figName,
                                                                                                        cut_figName2)
                
                        # 验证获取的器件结构数据有效
                    
                        #if cutAB is not None:
                        VisualizationPlot.drawCut(cutAB,xyAll, None, CUTDATA, cutpos, system, isExchange)
                        fig.setVisible(True)
                    else:
                        sayz("9")
                        VisualizationPlot.drawPhasespace(None, None, x_label, y_label, particle, time, x, y,z)
                sayz("10")
        recoverItemName(picType, picIndex)
    # elif picType == 7:
    #     # 三维等位图
    #     data, headList = VisualizationResult.getData(filePath, "Group_fild", "3D_fieldem", None)
    #     figname = headList[-1]
    #     minAngle = "4"
    #     # 传文件路径绘图
    #     # strcuctDataPath = json.loads(FreeCAD.ActiveDocument.LicenseURL)
    #     # strcuctFilePath = strcuctDataPath.split('_json')[0]+".H5"
    #     strcuctFilePath = os.path.dirname(filePath) + "\\TEMP.H5"
    #
    #     structNameFilePath = os.path.dirname(filePath) + "\\structName.json"
    #
    #     # 先把UTF-8转成万国码在转成GBK
    #     filePath = filePath.decode('utf-8').encode('gbk')
    #     figname = figname.decode('utf-8').encode('gbk')
    #     strcuctFilePath = strcuctFilePath.decode('utf-8').encode('gbk')
    #     structNameFilePath = structNameFilePath.decode('utf-8').encode('gbk')
    #     subprocess.Popen(
    #         EXE_PATH_3D + '"' + filePath + '"' + ' ' + '"' + strcuctFilePath + '"' + ' ' + '"' + structNameFilePath + '"' + ' CONTOUR3D ' + '"' + figname + '"')
    #     sayz(figname + u"开始绘制...")
    #     recoverItemName(picType, picIndex)
    elif picType == 7:
        figname = "phaseapace3d"
        minAngle = "4"
        # 传文件路径绘图
        # strcuctDataPath = json.loads(FreeCAD.ActiveDocument.LicenseURL)
        # strcuctFilePath = strcuctDataPath.split('_json')[0]+".H5"
        strcuctFilePath = os.path.dirname(filePath) + "\\TEMP.H5"

        structNameFilePath = os.path.dirname(filePath) + "\\structName.json"

        # 先把UTF-8转成万国码在转成GBK
        filePath = filePath.decode('utf-8').encode('gbk')
        figname = figname.decode('utf-8').encode('gbk')
        strcuctFilePath = strcuctFilePath.decode('utf-8').encode('gbk')
        structNameFilePath = structNameFilePath.decode('utf-8').encode('gbk')
        subprocess.Popen(
            EXE_PATH_3D + '"' + filePath + '"' + ' ' + '"' + strcuctFilePath + '"' + ' ' + '"' + structNameFilePath + '"' + ' PHASESPACE3D ' + '"' + figname + '"')
        sayz(figname + u"开始绘制...")

        recoverItemName(8, picIndex)
    # elif picType == 4:
    #     # 器件结构图
    #     # structdataPath = json.loads(FreeCAD.ActiveDocument.LicenseURL)
    #     structdataPath = os.path.dirname(filePath) + "\\TEMP.H5"
    #     for root, dirs, files in os.walk(structdataPath):
    #         if not os.path.exists(structdataPath + '\\DATASTRUCT\\'):
    #             sayzerr("datastruct data is not existed")
    #             #这路做了更改，因为recoverItemName索引不对
    #             recoverItemName(picType, -1)
    #             return
    #         if structdataPath + '\\DATASTRUCT' in root:
    #             figName = u'三维立体图'
    #             addChild(plotTree.ui, figName, [4, 1, filePath], )
    #             # sayz(root)
    #             i = 1
    #             for thisRoot, thisDirs, thisFiles in os.walk(root):
    #                 # sayz("file: "+str(thisFiles))
    #                 for curfile in thisFiles:
    #                     if curfile != "attribute.json" and curfile!="baseData.json":
    #                         i += 1
    #                         figName = os.path.splitext(curfile)[0].replace("_", "*")
    #                         addChild(plotTree.ui, figName, [4, i, root + "\\" + curfile])
    #                         recoverItemName(picType, -1)

def isExisted(fignName):
    """
    判断绘图窗口中是否已经存在该结构图，如果存在，则激活该窗口，否则，返回False，重新绘图
    :param fignName:图名
    :return:
    """
    mdi = vPlot.getMdiArea()
    subWindowList = mdi.subWindowList()
    for subWindow in subWindowList:
        # 如果窗口名和item名一致则激活窗口
        if subWindow.windowTitle() == fignName:
            mdi.setActiveSubWindow(subWindow)
            return True
    return False

# filePath: h5数据路径
# path: json数据路径
# contourType: 等位图类型（shade/not shade）
# def draw_one(path):
#     for root, dirs, files in os.walk(path):
#         # 等位图
#         # if path+'\\CONTOUR\\' in root:
#         #     # 获取等位图的附加信息
#         #     x_label, y_label, time, component, range_start, range_end, range_min, range_max, step, figname = VisualizationResult.contourInfo(root)
#         #     a, b, c = VisualizationResult.getData3(root)
#         #     # 判断a、b、c的数据量关系是否符合要求
#         #     assert len(c) == len(a) * len(b), 'contour: len(c) != len(a) * len(b)'
#         #     # 新建一个窗口
#         #     fig = vPlot.figure(figname)
#         #     # 绘制等位图
#         #     if not contourType:
#         #         VisualizationPlot.drawContour(x_label, y_label, time, component,
#         #                                       VisualizationResult.range_format(range_start),
#         #                                       VisualizationResult.range_format(range_end), range_min, range_max, step,
#         #                                       a, b, c, 'line')
#         #     else:
#         #         VisualizationPlot.drawContour(x_label, y_label, time, component,
#         #                                       VisualizationResult.range_format(range_start),
#         #                                       VisualizationResult.range_format(range_end), range_min, range_max, step,
#         #                                       a, b, c, 'shade')
#             # 二维等位图的三维可视化
#             # fig3Dname = figname + '3D'
#             # fig3D = vPlot.figure(fig3Dname)
#             # # 绘制等位图
#             # VisualizationPlot.drawContour3D(x_label, y_label, time, component, VisualizationResult.range_format(range_start),
#             #                                 VisualizationResult.range_format(range_end), range_min, range_max, step, a, b, c)
#         if path+'\\OBSERVE\\' in root:
#             # 获取时间变化图的附加信息
#             x_label, y_label, type, range_min, range_max, figname = VisualizationResult.observeInfo(root)
#             # 获取时间变化图的数据
#             x, y = VisualizationResult.getData2(root, 'dsetGrd.json')
#             fig = vPlot.figure(figname)
#             VisualizationPlot.drawObserve(x_label, y_label, type, VisualizationResult.range_format(range_min), VisualizationResult.range_format(range_max), x, y)
#         elif path+'\\PHASESPACE\\' in root:
#             x_label, y_label, particle, time, figname = VisualizationResult.phasespaceInfo(root)
#             x, y = VisualizationResult.getData2(root, 'dsetPar.json')
#             fig = vPlot.figure(figname)
#             VisualizationPlot.drawPhasespace(x_label, y_label, particle, time, x, y)
#         elif path+'\\RANGE\\' in root:
#             x_label, y_label, time, component, range_min, range_max, figname = VisualizationResult.rangeInfo(root)
#             x, y = VisualizationResult.getData2(root, 'dsetGrd.json')
#             fig = vPlot.figure(figname)
#             VisualizationPlot.drawRange(x_label, y_label, time, component, VisualizationResult.range_format(range_min), VisualizationResult.range_format(range_max), x, y)
#         elif path+'\\VECTOR\\' in root:
#             x_label, y_label, component, time, cut_position, max_vector, figname = VisualizationResult.vectorInfo(root)
#             a, b, c = VisualizationResult.getData3(root)
#             # 判断a、b、c的数据量关系是否符合要求
#             assert len(c) == 2 * len(a) * len(b), 'vector: len(c) != 2 * len(a) * len(b)'
#             fig = vPlot.figure(figname)
#             VisualizationPlot.drawVector(x_label, y_label, component, time, cut_position, max_vector, a, b, c)
#         # 三维等位图
#         # elif path + '\\CONTOUR3D\\' in root:
#         #     # 获取Mod文件夹路径
#         #     file_path = os.path.dirname(__file__)
#         #     exe_path = os.path.dirname(os.path.dirname(file_path))
#         #     figname = VisualizationResult.contour3DInfo(root)
#         #     # 传文件路径绘图
#         #     subprocess.Popen(exe_path + '\\Package\\visualizationPlot3D\\Visualization3D.exe ' + '"' + filePath + '"' + ' CONTOUR3D ' + '"' + root + '"')
#         #     sayz(figname + u"开始绘制...")
#         # 三维立体图
#         # elif path + '\\DATASTRUCT' in root:
#         #     figName = u'三维立体图'
#         #     addChild(plotTree.ui, figName, [7, 1, filePath], )
#         #     # sayz(root)
#         #     i = 1
#         #     for thisRoot, thisDirs, thisFiles in os.walk(root):
#         #         # sayz("file: "+str(thisFiles))
#         #         for curfile in thisFiles:
#         #             if curfile != "attribute.json":
#         #                 i += 1
#         #                 figName = os.path.splitext(curfile)[0].replace("_", "*")
#         #                 addChild(plotTree.ui, figName, [7, i, root+"\\"+curfile])

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')

def sayzerr(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintWarning('\n')