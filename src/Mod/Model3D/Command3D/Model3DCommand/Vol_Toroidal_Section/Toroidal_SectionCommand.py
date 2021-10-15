# encoding:utf-8
import FreeCAD
import FreeCADGui
import Toroidal_SectionInstance
import Toroidal_SectionDialogMain
from Model3D.Tools import Tools3D


class CreateToroidal_SectionCommand:
    """
    注册圆环区域体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = Toroidal_SectionInstance.getObject()
        # 在这里打开Ui
        Form = Toroidal_SectionDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Toroidal_Section.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '圆环区域体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '圆环区域体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolToroidal_Section_3D', CreateToroidal_SectionCommand())


