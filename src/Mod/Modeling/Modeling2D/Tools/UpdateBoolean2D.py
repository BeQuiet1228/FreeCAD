# coding=utf-8
import FreeCAD as App
from Modeling.Modeling2D.Tools import Tools2D
import FreeCADGui
import FreeCAD
import time

model_list_old = []


class UpdateBoolean:
    def __init__(self):
        pass

    @staticmethod
    def fuse(basObj, obj):
        if basObj.isNull():
            return obj
        else:
            return basObj.fuse(obj)

    @staticmethod
    def cut(basObj, obj):
        """布尔差"""
        if basObj.isNull():
            return basObj
        else:
            return basObj.cut(obj)

    @staticmethod
    def boolean(obj_list):
        import time
        start_time = time.time()
        if len(obj_list) == 0:
            hideAllModels()
            return
        for i in obj_list:
            if i.Shape is None:
                Tools2D.sayz("存在shape为None的体:  " + str(i.Label))
        basObj = obj_list[0].Shape
        for obj in obj_list:
            # 部分模型数据出现错误时回到是isValid()抛出异常，需要提前判断当前Shape是否为空
            if obj.Shape.isNull():
                Tools2D.sayz(obj.Label + "的Shape存在问题，将其剔除布尔运算，请检查该模型")
                continue
            if not obj.Shape.isValid():
                Tools2D.sayz(obj.Label + "的Shape存在问题，将其剔除布尔运算，请检查该模型")
                continue
            if obj.Attribute == Tools2D.Attribute.Conductor or obj.Attribute == Tools2D.Attribute.Custom:
                basObj = UpdateBoolean.fuse(basObj, obj.Shape)
            elif obj.Attribute == Tools2D.Attribute.Vacuo or obj.Attribute == Tools2D.Attribute.Void:
                basObj = UpdateBoolean.cut(basObj, obj.Shape)
        App.ActiveDocument.ResultShape.Shape = basObj
        # 布尔运算完隐藏当前除Result之外的所有模型
        hideAllModels()
        end_time = time.time()
        Tools2D.sayz("当前布尔运算的时间为"+str(end_time-start_time)+"s\n")


def hideAllModels():
    model_list = Tools2D.getAllModelObjects()
    for i in model_list:
        if hasattr(i, "Type"):
            if i.Type == Tools2D.ObjectType.Line or i.Type == Tools2D.ObjectType.LineConformal:
                FreeCADGui.getDocument(App.ActiveDocument.Name).getObject(i.Name).Visibility = True
                continue
        FreeCADGui.getDocument(App.ActiveDocument.Name).getObject(i.Name).Visibility = False


class UpdateAutoFilletBoolean:
    def __init__(self):
        pass

    @staticmethod
    def fuse(basObj, obj):
        if basObj.isNull():
            return obj
        else:
            return basObj.fuse(obj)

    @staticmethod
    def cut(basObj, obj):
        """布尔差"""
        if basObj.isNull():
            return basObj
        else:
            return basObj.cut(obj)

    @staticmethod
    def boolean(obj_list):
        if len(obj_list) == 0:
            return
        for i in obj_list:
            if i.Shape is None:
                Tools2D.sayz("存在shape为None的体:  " + str(i.Label))
        basObj = obj_list[0].Shape
        for obj in obj_list:
            # 部分模型数据出现错误时回到是isValid()抛出异常，需要提前判断当前Shape是否为空
            if obj.Shape.isNull():
                Tools2D.sayz(obj.Label + "的Shape存在问题，将其剔除布尔运算，请检查该模型")
                continue
            if not obj.Shape.isValid():
                Tools2D.sayz(obj.Label + "的Shape存在问题，将其剔除布尔运算，请检查该模型")
                continue
            if obj.Attribute == Tools2D.Attribute.Conductor or obj.Attribute == Tools2D.Attribute.Custom:
                basObj = UpdateBoolean.fuse(basObj, obj.Shape)
            elif obj.Attribute == Tools2D.Attribute.Vacuo or obj.Attribute == Tools2D.Attribute.Void:
                basObj = UpdateBoolean.cut(basObj, obj.Shape)
        App.ActiveDocument.ResultShape.Shape = basObj
        hidePartModels()


def hidePartModels():
    model_list = Tools2D.getAllModelObjects()
    for i in model_list:
        if hasattr(i, "Type") and hasattr(i, "IsAutoFillet") and i.IsAutoFillet:
            FreeCADGui.getDocument(App.ActiveDocument.Name).getObject(i.Name).Visibility = False
