# encoding:utf-8
import FreeCAD
import FreeCADGui
import RhombusInstance
import RhombusDialogMain
from Model3D.Tools import Tools3D


class CreateRhombusCommand:
    """
    注册菱形体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = RhombusInstance.getObject()
        # 在这里打开Ui
        Form = RhombusDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Rhombus.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '菱形体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '菱形体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolRhombus_3D', CreateRhombusCommand())



