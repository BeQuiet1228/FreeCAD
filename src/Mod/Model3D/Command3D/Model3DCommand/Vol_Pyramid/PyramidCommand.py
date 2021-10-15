# encoding:utf-8
import FreeCAD
import FreeCADGui
import PyramidInstance
import PyramidDialogMain
from Model3D.Tools import Tools3D


class CreateAnnularCommand:
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
        obj = PyramidInstance.getObject()
        # 在这里打开Ui
        Form = PyramidDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Pyramid.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '金字塔体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '金字塔体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVolPyramid_3D', CreateAnnularCommand())


