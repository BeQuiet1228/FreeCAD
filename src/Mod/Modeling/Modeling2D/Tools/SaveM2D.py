# -*- coding: utf-8 -*-
import os
import FreeCAD
import FreeCADGui

import Modeling
from Modeling.Modeling2D.Tools import InitDoc
from Modeling.Modeling2D.Tools.FileView import FileView


class SaveM2D:
    def Activated(self):
        # 更改M2D的名字，确保M2D的名字与工程名一致
        flag = FileView().isThisSubWindow()
        if flag:
            FileView().setTitle(FreeCAD.ActiveDocument.Label)
        projectName = FreeCAD.ActiveDocument.FileName
        self.path = os.path.splitext(projectName)[0]+".m2d"
        self.saveM2DFile()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/file-save-as.svg"
        MenuText = "saveAsM2D"
        Accel = "Ctrl+2"
        ToolTip = "saveAsM2D"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

    def saveM2DFile(self):
        from File.FileCommand.M2dFile.M2DContainer import setM2DToInterface
        # 输出到文件
        fo = open(self.path, "w+")
        m2d = setM2DToInterface()
        fo.write(m2d.encode("UTF-8"))
        fo.close()


class InitWhenOpenFcStd2d:
    def Activated(self):
        # noinspection PyBroadException
        try:
            FreeCAD.addDocumentObserver(InitDoc.DocumentObservers())
            # 如果当前工程没有对应的M2D显示界面则创建一个新的
            FreeCADGui.runCommand("CreateM2D")

            # Modeling.Modeling2D.Modeling2DCommand.Grid.GridCommand.showGrid()
            FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
            showAllObjs()
            # FreeCADGui.runCommand("AdjustView")
        except:
            FreeCAD.Console.PrintError("初始化文件失败\n")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/file-save-as.svg"
        MenuText = "initM2D"
        Accel = "Ctrl+2"
        ToolTip = "saveAsM2D"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}


def showAllObjs():
    """
    显示所有模型
    :return:
    """
    try:
        obj_list = FreeCAD.ActiveDocument.Objects
        for i in obj_list:
            i.ViewObject.Visibility = True
            # 部分模型需要重新计算才能显示出来，虽然会消耗计算机性能但是没办法
            try:
                i.recompute()
            except:
                FreeCAD.Console.PrintError(i.Label + " 重新计算时出现错误")
    except:
        pass


FreeCADGui.addCommand('M2d_Save', SaveM2D())
FreeCADGui.addCommand('InitWhenOpenFcStd2d', InitWhenOpenFcStd2d())
