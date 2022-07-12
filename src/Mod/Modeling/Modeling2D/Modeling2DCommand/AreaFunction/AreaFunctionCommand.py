# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import AreaFunctionInstance
import AreaFunctionDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class Function2D():
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/函数面.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFunctionArea',
            '函数面')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFunctionArea',
            'FunctionArea')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def Activated(self):
        obj = AreaFunctionInstance.getObject()
        Form = AreaFunctionDlgMain.ShowDialog(obj, True)
        Form.exec_()

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


FreeCADGui.addCommand('CreateFunction2D', Function2D())
