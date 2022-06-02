# coding=utf-8
import FreeCAD as App
from Model3D.Tools import ObjectTools, Tools3D
import FreeCADGui
import FreeCAD
import time


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
        startTime = time.time()
        if len(obj_list) == 0:
            hideAllModels()
            FreeCAD.ActiveDocument.ResultShape.ViewObject.Visibility = False
            return
        else:
            FreeCAD.ActiveDocument.ResultShape.ViewObject.Visibility = True
        basObj = obj_list[0]
        for i in range(1, len(obj_list)):
            if i%2 == 0:
                basObj = UpdateBoolean.fuse(basObj, obj_list[i])
            else:
                basObj = UpdateBoolean.cut(basObj, obj_list[i])

        App.ActiveDocument.ResultShape.Shape = basObj
        # 布尔运算完隐藏当前除Result之外的所有模型
        hideAllModels()
        endTime = time.time()
        Tools3D.sayz("当前布尔运算的时间为"+str(endTime-startTime)+"s\n")
        if len(ObjectTools.getAllValidModelObj()) == 1 and len(ObjectTools.getAllVolumes()) == 1:
            FreeCADGui.runCommand("Std_ViewAxo")


def hideAllModels():
    model_list = ObjectTools.getAllObjects()
    area_list = chooseAreaList()
    for i in model_list:
        if i in area_list:
            FreeCADGui.getDocument(App.ActiveDocument.Name).getObject(i.Name).Visibility = True
        else:
            FreeCADGui.getDocument(App.ActiveDocument.Name).getObject(i.Name).Visibility = False


# 被物理设置选中面的列表
def chooseAreaList():
    model_list = [ObjectTools.ObjectType.Line_Conformal, ObjectTools.ObjectType.Line_Oblique,
                  ObjectTools.ObjectType.Area_Conformal, ObjectTools.ObjectType.Area_Rectangular,
                  ObjectTools.ObjectType.Area_Polygonal, ObjectTools.ObjectType.Area_Function]
    displayArea = []
    allPhyObjs = ObjectTools.getAllPhyAndProObjects()
    for i in allPhyObjs:
        # 这里被观测设置选中的，暂时不显示，留个接口
        if hasattr(i, "orthogonalProjectionPlane") and i.Type == ObjectTools.ObjectType.PORT or \
                i.Type == ObjectTools.ObjectType.SYMT or i.Type == ObjectTools.ObjectType.DRIV:
            curObj = ObjectTools.getObjByLabel(i.orthogonalProjectionPlane)
            if hasattr(curObj, "Type") and curObj.Type in model_list:
                displayArea.append(curObj)
        if i.Type == ObjectTools.ObjectType.IND:
            curObj = ObjectTools.getObjByLabel(i.inductorType)
            if hasattr(curObj, "Type") and curObj.Type in model_list:
                displayArea.append(curObj)
    return displayArea


def boolResult(obj_list):
    """
    parameter:list
    布尔加
    """
    baseObj = obj_list[0].Shape
    shape_list = []
    for obj in obj_list:
        if obj.Shape == baseObj:
            continue
        # 部分模型数据出现错误时回到是isValid()抛出异常，需要提前判断当前Shape是否为空
        if obj.Shape.isNull():
            Tools3D.sayz(obj.Label + "的Shape存在问题，将其剔除布尔运算，请检查该模型")
            continue
        if not obj.Shape.isValid():
            Tools3D.sayz(obj.Label + "的Shape存在问题，将其剔除布尔运算，请检查该模型")
            continue
        shape_list.append(obj.Shape)
    baseObj = UpdateBoolean.fuse(baseObj, shape_list)
    return baseObj


def boolResultList():
    """
    获得布尔运算之后的列表
    parameter:[[]]
    return: list
    """
    Result_list = []
    array = ObjectTools.getBoolList()
    for i in array:
        Result_list.append(boolResult(i))
    return Result_list
