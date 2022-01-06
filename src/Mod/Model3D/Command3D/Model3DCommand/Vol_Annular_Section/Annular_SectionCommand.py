# encoding:utf-8
import FreeCAD
import FreeCADGui
import Annular_SectionInstance
import Annular_SectionDialogMain
from Model3D.Tools import Tools3D


class CreateAnnular_SectionCommand:
    """
    注册环形区域体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = Annular_SectionInstance.getObject()
        # 在这里打开Ui
        Form = Annular_SectionDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Annular_Section.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '环形区域体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '环形区域体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolAnnular_Section_3D', CreateAnnular_SectionCommand())


