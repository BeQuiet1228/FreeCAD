# -*- coding: utf-8 -*-
import os
import FreeCAD
import FreeCADGui
import InitDoc3D
from FileView3D import FileView


class SaveM3D:
    def Activated(self):
        # 更改M2D的名字，确保M2D的名字与工程名一致
        flag = FileView().isThisSubWindow()
        if flag:
            FileView().setTitle(FreeCAD.ActiveDocument.Label)
        projectName = FreeCAD.ActiveDocument.FileName
        self.path = os.path.splitext(projectName)[0]+".m3d"
        self.saveM3DFile()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/file-save-as.svg"
        MenuText = "saveAsM3D"
        Accel = "Ctrl+3"
        ToolTip = "saveAsM3D"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}

    def saveM3DFile(self):
        from Model3D.M3DFileNew.M3DContainer import setM3DToInterface
        # 输出到文件
        fo = open(self.path, "w+")
        m3d = setM3DToInterface()
        fo.write(m3d.encode("UTF-8"))
        fo.close()


class InitWhenOpenFcStd3d:
    def Activated(self):
        # noinspection PyBroadException
        try:
            FreeCAD.addDocumentObserver(InitDoc3D.DocumentObservers())
            # 如果当前工程没有对应的M3D显示界面则创建一个新的
            FreeCADGui.runCommand("CreateM3D")

            FreeCADGui.ActiveDocument.ActiveView.setAxisCross(True)
            showAllObjs()
        except:
            FreeCAD.Console.PrintError("初始化文件失败\n")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/file-save-as.svg"
        MenuText = "initM3D"
        Accel = "Ctrl+3"
        ToolTip = "saveAsM3D"
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


FreeCADGui.addCommand('M3d_Save', SaveM3D())
FreeCADGui.addCommand('InitWhenOpenFcStd3d', InitWhenOpenFcStd3d())
