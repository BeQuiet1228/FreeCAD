# encoding:utf-8
import FreeCAD
import FreeCADGui
import AreaFunctionInstance
from Model3D.Tools import Tools3D
import AreaFunctionDialogMain


class CreateAreaFunctionCommand:
    """
    函数面
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = AreaFunctionInstance.getObject()
        # 在这里打开Ui
        Form = AreaFunctionDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3DFunctionArea.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '函数面')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '函数面')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateAreaFunction_3D', CreateAreaFunctionCommand())


