# encoding:utf-8
import FreeCAD
import FreeCADGui
import LineConformalInstance
import LineConformalDialogMain
from Model3D.Tools import Tools3D


class CreateLineConformalCommand:
    """
    注册圆环体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = LineConformalInstance.getObject()
        # 在这里打开Ui
        Form = LineConformalDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Line_Conformal.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '正投影线')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '正投影线')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateLineConformal_3D', CreateLineConformalCommand())


