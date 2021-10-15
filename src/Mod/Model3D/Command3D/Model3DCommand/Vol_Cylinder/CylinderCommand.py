# encoding:utf-8
import FreeCAD
import FreeCADGui
import CylinderInstance
import CylinderDialogMain
from Model3D.Tools import Tools3D


class CreateCylinderCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = CylinderInstance.getObject()
        # 在这里打开Ui
        Form = CylinderDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Cylinder.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '创建圆柱体',
            '圆柱体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '圆柱体',
            '圆柱体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create_3D_Cylinder', CreateCylinderCommand())