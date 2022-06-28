# encoding:utf-8
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D, ObjectTools

class RefreshCommand:
    """
    注册圆环体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        obj = FreeCAD.ActiveDocument.Param
        if obj:
            model_list = obj.InList
            for i in model_list:
                i.recompute()
        # 上面筛选可能会遗漏以下模型
        # 要把挤出体和旋转体，投影挤出体，阵列体，参数阵列体也重新生成
        objs = ObjectTools.getAllObjects()
        target_objs = [ObjectTools.ObjectType.Vol_Extruded, ObjectTools.ObjectType.Vol_Revolution,
                       ObjectTools.ObjectType.Vol_Draft_Extrude, ObjectTools.ObjectType.Vol_Array,
                       ObjectTools.ObjectType.Vol_ParamArray]
        for i in objs:
            if i.Type in target_objs:
                i.recompute()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Area_Conformal.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '正投影面')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '正投影面')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Refresh_3D', RefreshCommand())


class RefreshVolume:
    """
    注册圆环体命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        objs = ObjectTools.getAllObjects()
        target_objs = [ObjectTools.ObjectType.Vol_Extruded, ObjectTools.ObjectType.Vol_Revolution]
        for i in objs:
            if i.Type in target_objs:
                i.recompute()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Area_Conformal.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '正投影面')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFoil',
            '正投影面')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('RefreshVolume_3D', RefreshVolume())
