# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import CommonGui
import File.FileCommand.TextUI.FileTextView
import File.FileCommand.M3DFile.M3DFileUtil
from Physics.PhysicsCommand.BoundPalMain import BoundSettingTreeShow, BoundSettingTree
from Physics.PhysicsCommand.ObservePalMain import ObserveSettingTreeShow,ObserveSettingTree
from Common.Tools import ObjectsTools,DocumentTools
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication
import json
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
def ModifythejosnFile():
    '''
    这个函数是为了在修改json文件后，打开老文件没有key值的bug而设置的函数，
    只需要在这个函数给相关的key一个默认值就好了
    '''
    # FreeCAD.Console.PrintError('\n已经进入修改json的函数\n')
    JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
    FA_Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
    for i in JSON_CADComment.keys():
        if JSON_CADComment[i]['Dlg_Type'] == 'Obs_Type':
            # 观察部分新添加了几个变量站在这里设置默认值
            if not 'name2' in JSON_CADComment[i]:
                JSON_CADComment[i]['name2'] = ''
            if not "Particle_Statistics" in JSON_CADComment[i]:
                JSON_CADComment[i]["Particle_Statistics"] = False
            if not "Particle_Collected" in JSON_CADComment[i]:
                JSON_CADComment[i]["Particle_Collected"] = False
            if not "Particle_Emitted" in JSON_CADComment[i]:
                JSON_CADComment[i]["Particle_Emitted"] = False
            if not "Particle_Destroyed" in JSON_CADComment[i]:
                JSON_CADComment[i]["Particle_Destroyed"] = False
            if not "phase1" in JSON_CADComment[i]:
                JSON_CADComment[i]["phase1"] = "phase1"
            if not "Particle_Statistics" in JSON_CADComment[i]:
                JSON_CADComment[i]["Particle_Statistics"] = "EMIT_EPS"
            if not "Particle" in JSON_CADComment[i]:
                JSON_CADComment[i]["Particle"] = "CHARGE"
            if not "ParticleType" in JSON_CADComment[i]:
                JSON_CADComment[i]["ParticleType"] = "ELECTRON"
            if not "interval_Checked" in JSON_CADComment[i]:
                JSON_CADComment[i]["interval_Checked"] = False
            if not "interval" in JSON_CADComment[i]:
                JSON_CADComment[i]["interval"] = ""
            
        if JSON_CADComment[i]['Dlg_Type'] == 'ExP_Type':
            if not 'source_type' in JSON_CADComment[i]:
                JSON_CADComment[i]['source_type'] = '未指定'

    for i in FA_Comment.keys():
        if i == "WorkSpaceSettings":
            if not "WhetherToHitOkOrNot" in FA_Comment[i]:
                FA_Comment[i]["WhetherToHitOkOrNot"] = False
        if i == "TimeDomainComputing":
            if not "Types" in FA_Comment[i]:
                FA_Comment[i]["Types"] = "ALL"
            if not "EveryNum" in FA_Comment[i]:
                FA_Comment[i]["EveryNum"] = "1"
            if not "MaxNum" in FA_Comment[i]:
                FA_Comment[i]["MaxNum"] = "50000"
            if not "isChecked_part" in FA_Comment[i]:
                FA_Comment[i]["isChecked_part"] = False
            if not "checkBoxStep" in FA_Comment[i]:
                FA_Comment[i]["checkBoxStep"] = False
            if not "computeTimeInterval" in FA_Comment[i]:
                FA_Comment[i]["computeTimeInterval"] = "1"
            if not "is_re" in FA_Comment[i]:
                FA_Comment[i]["is_re"] = False
            if not "is_nonre" in FA_Comment[i]:
                FA_Comment[i]["is_nonre"] = True

    FreeCAD.ActiveDocument.Begin = json.dumps(JSON_CADComment)
    FreeCAD.ActiveDocument.Comment = json.dumps(FA_Comment)
    # FreeCAD.Console.PrintError('\n已经执行修改json的函数\n')
# ---------------------------------
# @Author:wzj                     
# @Date:2019-04-25  '这个变量存储着全局窗口对象【一个key值（独一无二的unique）对应一个窗口对象】
# Extremely important
# Extremely important
ObjectDict={}  ## Extremely important
# Extremely important
# Extremely important
def sayz(msg):
    FreeCAD.Console.PrintMessage('-----------------------------------------')
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')
class NewDocument:
    def Activated(self): 
        dlg = CommonGui.CoordinateSystemUI.CoordinateSystemDialog()
        dlg.exec_()
        doc=None
        if dlg.Result == "2D":
            FreeCADGui.activateWorkbench("Modeling2DWorkbench")
            doc=FreeCAD.newDocument()
            FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
            FreeCAD.ActiveDocument.CoordinateSystem = dlg.CoordinateSystem

        if dlg.Result == "3D":
            FreeCADGui.activateWorkbench("Modeling3DWorkbench")
            '''
            author:@fubiao
            新建文档时，增加一个空的三维对象，之后的布尔求交都在这个对象上进行
            '''
            doc=FreeCAD.newDocument()
            
            if doc:
                FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
                FreeCAD.ActiveDocument.CoordinateSystem = dlg.CoordinateSystem

            # show m3dFile by mx
            File.FileCommand.TextUI.FileTextView.FileView().showThisSubWindow()

        if doc:
            toplevel = QApplication.topLevelWidgets()

            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":
                    tr1 = i.findChild(QtGui.QTreeWidget, 'treeWidget_boundSettingTree')
                    if not tr1:
                        boundTree = BoundSettingTree()
                        boundTree.show()
                    tr2 = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
                    if not tr2:
                        observeTree = ObserveSettingTree()
                        observeTree.show()
        #初始化当前文档
        if doc:
            DocumentTools.otherDocInit()
            # DocumentTools.initDocument(doc)
            # DocumentTools.initParamObj(doc)
            # FreeCADGui.doCommand("from Modeling.Common.Tools import DocumentTools")

        # 新建文档时将属性窗口调出
        mainWindow = FreeCADGui.getMainWindow()
        propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
        propertyView.setVisible(True)


    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/document-new.svg"
        MenuText = "新建(N)..."
        Accel = "Ctrl+N"
        ToolTip = "创建一个新空白文档"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return False
        else:
            return True

# override default function File->Open
class OpenDocument:
    '''
    @Author:wzj
    @Date:2019-04-25
    @Brief:这个函数用于加载工程项目时读取项目里面的信息并作相应处理 OpenDocument-->打开 NewDocument-->新建
    '''        
    def Activated(self):
        FreeCAD.Console.PrintMessage("OPEN\n")
        try:
            # FreeCAD.Console.PrintError('\n已经进入打开文档\n')
            toplevel = QApplication.topLevelWidgets()
            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":    
                    tr = i.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel')
                    tr1 = i.findChild(QtGui.QTreeWidget, 'treeWidget_boundSettingTree')
                    if not tr1:
                        boundTree = BoundSettingTree()
                        boundTree.show()
                    tr2 = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
                    if not tr2:
                        observeTree = ObserveSettingTree()
                        observeTree.show()
            BoundSettingTreeShow()
            ObserveSettingTreeShow()

            # show m3dFile by mx
            File.FileCommand.TextUI.FileTextView.FileView().showThisSubWindow()
            # @lizhenguang
            ModifythejosnFile()
            # FreeCAD.Console.PrintError('\n已经结束打开文档\n')
        except:
            FreeCAD.Console.PrintError('\n打开文档异常\n')
            pass

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/document-open.svg"
        MenuText = "Open"
        Accel = "Ctrl+O"
        ToolTip = "Open a document"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

    # def IsActive(self):
    #     if FreeCADGui.ActiveDocument:
    #         return False
    #     else:
    #         return True

class ActivatedDocument:
    '''
    @Author:wzj
    @Date:2019-04-25
    @Brief:这个函数用于激活工程项目时切换分支树中的工作目录
    '''      
    def Activated(self):
        try:
            toplevel = QApplication.topLevelWidgets()
            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":    
                    tr = i.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel')
                    tr1 = i.findChild(QtGui.QTreeWidget, 'treeWidget_boundSettingTree')
                    if not tr1:
                        boundTree = BoundSettingTree()
                        boundTree.show()
                    tr2 = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
                    if not tr2:
                        observeTree = ObserveSettingTree()
                        observeTree.show()
            BoundSettingTreeShow()
            ObserveSettingTreeShow()
        except:
            pass        
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/document-open.svg"
        MenuText = "Open"
        Accel = "Ctrl+O"
        ToolTip = "Open a document"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}                
FreeCADGui.addCommand('Std_New', NewDocument())
# '''
# @Author:wzj
# @Date:2019-04-25
# @Brief:这两个是王忠杰添加的用于自定义打开和自定义激活的命令---它被C++代码调用
# '''  
FreeCADGui.addCommand('Customize_Open', OpenDocument())
FreeCADGui.addCommand('Customize_Activated', ActivatedDocument())

#     '''
#     @Author:wzj
#     @Date:2019-04-23
#     @Brief:这个函数用于开始页面自动加载控制台操作面板【Tab】并让他一直存活
#     '''
