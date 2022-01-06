# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import CommonGui
from Modeling.Modeling2D.Tools import Tools2D, InitDoc, FileView
# from Common.Tools import ObjectsTools, DocumentTools
from PySide import QtGui, QtCore


# ---------------------------------
# @Author:wzj                     
# @Date:2019-04-25  '这个变量存储着全局窗口对象【一个key值（独一无二的unique）对应一个窗口对象】

# Extremely important
# Extremely important
ObjectDict = {}  # Extremely important
# Extremely important
# Extremely important


def sayz(msg):
    FreeCAD.Console.PrintMessage('-----------------------------------------')
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage('\n')


class NewDocument:
    def Activated(self):
        # dlg = CommonGui.CoordinateSystemUI.CoordinateSystemDialog()
        dlg = CommonGui.CoordinateSystemDialogMain.ShowDialog()
        dlg.exec_()
        doc=None
        if not dlg.isKeepData:
            return
        else:
            pass
        if dlg.Result == "3DText":
            FreeCAD.newDocumentM3dText()
            return
        if dlg.Result == "2DText":
            FreeCAD.newDocumentM2dText()
            return

        if dlg.Result == "new3D":
            FreeCADGui.activateWorkbench("Modeling3DWorkbench")
            doc = FreeCAD.newDocumentM3dMod()
            docObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Param")
            docObj.addProperty("App::PropertyFloat", "justForAnalysis")
            if doc:
                FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
                FreeCAD.ActiveDocument.CoordinateSystem = dlg.CoordinateSystem
                # 此处暂时用Comment来记录当前是3D建模，该变量会在DisplayDialog部分调用
                FreeCAD.ActiveDocument.Comment = "new3D"
                from Model3D.Tools import FileView3D
                # show m3dFile by @wangzhenguo
                #FileView3D.FileView().showThisSubWindow()
                FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)

        if dlg.Result == "2D":
            FreeCADGui.activateWorkbench("Modeling2DWorkbench")
            doc=FreeCAD.newDocumentM2dMod()
            # 新增参数
            docObj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Param")
            docObj.addProperty("App::PropertyFloat", "justForAnalysis")
            docObj.addProperty("App::PropertyStringList", "DynamicData").DynamicData
            docObj.addProperty("App::PropertyString", "Type", "", "Type of Ojecy").Type = "Variable"
            docObj.setEditorMode('Type', 2)
            docObj.setEditorMode("DynamicData", 1)

            if doc:
                FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
                FreeCAD.ActiveDocument.CoordinateSystem = dlg.CoordinateSystem
                # 此处暂时用Comment来记录当前是2D建模，该变量会在DisplayDialog部分调用
                FreeCAD.ActiveDocument.Comment = "2D"
                # show m2dFile by lzg
                #FileView.FileView().showThisSubWindow()
                FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)


        # 初始化当前文档
        if doc:
            if dlg.Result == "2D":
                InitDoc.otherDocInit()
            else:
                from Model3D.Tools import InitDoc3D
                InitDoc3D.otherDocInit()

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
        # FreeCAD.Console.PrintMessage("OPEN\n")
        # try:
        #     FreeCAD.Console.PrintError('\n打开文档\n')
        #     toplevel = QApplication.topLevelWidgets()
        #     for i in toplevel:
        #         if i.metaObject().className() == "Gui::MainWindow":
        #             tr = i.findChild(QtGui.QTreeWidget, 'treeWidget_OperatingPanel')
        #             tr1 = i.findChild(QtGui.QTreeWidget, 'treeWidget_boundSettingTree')
        #             if not tr1:
        #                 boundTree = BoundSettingTree()
        #                 boundTree.show()
        #             tr2 = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
        #             if not tr2:
        #                 observeTree = ObserveSettingTree()
        #                 observeTree.show()
        #     BoundSettingTreeShow()
        #     ObserveSettingTreeShow()
        #
        #     # show m3dFile by mx
        #     File.FileCommand.TextUI.FileTextView.FileView().showThisSubWindow()
        #     # @lizhenguang
        #     ModifythejosnFile()
        #     # FreeCAD.Console.PrintError('\n已经结束打开文档\n')
        # except:
        #     FreeCAD.Console.PrintError('\n打开文档异常\n')
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
        # if True:
        #     toplevel = QApplication.topLevelWidgets()
        #     mwdf = None
        #     for i in toplevel:
        #         if i.metaObject().className() == "MainWindowDef":
        #             mwdf = i
        #             break
        #     wid = None
        #     for i in mwdf.children():
        #         if i.metaObject().className() == "QWidget":
        #             wid = i
        #             break
        #     for i in wid.children():
        #         if i.metaObject().className() == "Gui::MainWindow":
        #             tr = i.findChild(QtGui.QTreeWidget, 'treeWidget_OperatingPanel')
        #             tr1 = i.findChild(QtGui.QTreeWidget, 'treeWidget_boundSettingTree')
        #             if not tr1:
        #                 boundTree = BoundSettingTree()
        #                 boundTree.show()
        #             tr2 = i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
        #             if not tr2:
        #                 observeTree = ObserveSettingTree()
        #                 observeTree.show()
        #     BoundSettingTreeShow()
        #     ObserveSettingTreeShow()
        # except:
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
