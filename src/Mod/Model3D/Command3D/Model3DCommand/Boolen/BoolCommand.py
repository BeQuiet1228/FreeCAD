# encoding:utf-8
import FreeCAD
import FreeCADGui
from Model3D.Tools import ObjectTools, UpdataBoolen3D, Tools3D


class BooleanCommand:
    """
    布尔运算界面按钮
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        # UpdataBoolen3D.UpdateBoolean.boolean(ObjectTools.getAllValidModelObj())
        UpdataBoolen3D.UpdateBoolean.boolean(UpdataBoolen3D.boolResultList())
        pass

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/布尔运算.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateBool',
            '布尔运算')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateBoolen',
            'Boolean')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('UpdateBooleanCommand_3D', BooleanCommand())



