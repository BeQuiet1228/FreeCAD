# encoding:utf-8
import FreeCAD
import FreeCADGui
import WedgeInstance
import WedgeDialogMain
from Model3D.Tools import Tools3D


class CreateWedgeCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
           return
        obj = WedgeInstance.getObject()
        # 在这里打开Ui
        Form = WedgeDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Wedge.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '楔形体',
            '楔形体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '楔形体',
            '创建楔形体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create_3D_Wedge', CreateWedgeCommand())