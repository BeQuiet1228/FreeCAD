# encoding:utf-8
import FreeCAD
import FreeCADGui
import Point3DInstance
from Model3D.Tools import Tools3D
import Point3DDialogMain


class CreatePoint3DCommand:
    """
    注册Foil命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = Point3DInstance.getObject()
        # 在这里打开Ui
        Form = Point3DDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Point.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '点')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '点')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePoint_3D', CreatePoint3DCommand())


