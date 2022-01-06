# encoding:utf-8
import FreeCAD
import FreeCADGui
import ParallelepipedalInstance
import ParallelepipedalDialogMain
from Model3D.Tools import Tools3D


class CreateParallelepipedalCommand:
    """
    注册平行六面体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = ParallelepipedalInstance.getObject()
        # 在这里打开Ui
        Form = ParallelepipedalDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Parallelepipedal.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '平行六面体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '平行六面体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolParallelepipedal_3D', CreateParallelepipedalCommand())
