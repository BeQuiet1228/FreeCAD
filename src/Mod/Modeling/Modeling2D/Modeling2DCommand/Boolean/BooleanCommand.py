# encoding:utf-8
import FreeCAD
import FreeCADGui
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools import UpdateBoolean2D


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
        UpdateBoolean2D.UpdateBoolean.boolean(Tools2D.getAllValidModelObj())
        pass

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/布尔运算.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateBool',
            '布尔运算')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateBoolen',
            'Boolean')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('UpdateBooleanCommand', BooleanCommand())


class PartBooleanCommand:
    """
    部分布尔运算界面按钮
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        Tools2D.sayz("长度为="+str(len(Tools2D.getPartValidModelObj())))
        UpdateBoolean2D.UpdateAutoFilletBoolean.boolean(Tools2D.getPartValidModelObj())
        pass

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/布尔运算.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateBool',
            '部分布尔运算')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateBoolen',
            'Boolean')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('UpdateFilletBool', PartBooleanCommand())


# # 通过名称来添加工程相关的object project@#$
# class Project:
#     def __init__(self):
#         if FreeCAD.ActiveDocument() is None:
#             return
#         pro_obj = FreeCAD.ActiveDocument.getObject("project@#$")
#         if pro_obj is None:
#             pass
#         else:
#             pass
#             # return pro_obj


