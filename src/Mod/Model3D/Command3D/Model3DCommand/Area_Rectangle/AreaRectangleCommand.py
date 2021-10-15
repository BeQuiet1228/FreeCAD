# encoding:utf-8
import FreeCAD
import FreeCADGui
import AreaRectangleInstance
import AreaRectangleDialogMain
from Model3D.Tools import Tools3D


class CreateAreaRectangleCommand:
    """
    注册圆环体命令
    """
    def IsActive(self):
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            if FreeCADGui.ActiveDocument:
                return True
            else:
                return False
        # 极坐标和柱坐标没有矩形面
        else:
            pass

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = AreaRectangleInstance.getObject()
        # 在这里打开Ui
        Form = AreaRectangleDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Area_Rectangular.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '矩形面')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '矩形面')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateAreaRectangle_3D', CreateAreaRectangleCommand())


