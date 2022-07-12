# encoding:utf-8
import FreeCAD
import FreeCADGui
import SpecialConeInstance
import SpecialConeDialogMain
from Model3D.Tools import Tools3D


class CreateSpecialConeCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
           return
        obj = SpecialConeInstance.getObject()
        # 在这里打开Ui
        Form = SpecialConeDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_SpecialCone.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '圆台体',
            '圆台体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '圆台体',
            '圆台体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create_3D_SpecialCone', CreateSpecialConeCommand())