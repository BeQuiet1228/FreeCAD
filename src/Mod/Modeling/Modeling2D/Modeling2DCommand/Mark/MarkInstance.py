#-*- coding: utf-8 -*-
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType


class Mark(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateMark")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Mark")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty()
    
    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.MARK
        # stringList是一个列表，正交投影面会有很多指定面
        self.obj.addProperty("App::PropertyString", "markObject").markObject = "未指定"
        # 有多种方向，所以用StringList
        self.obj.addProperty("App::PropertyString", "direction").direction = "X1"
        self.obj.addProperty("App::PropertyBool", "isMINIMUM").isMINIMUM = False
        self.obj.addProperty("App::PropertyBool", "isMIDPOINT").isMIDPOINT = False
        self.obj.addProperty("App::PropertyBool", "isMAXIMUM").isMAXIMUM = False
        self.obj.addProperty("App::PropertyString", "size").size = "1mm"


def getObject():
    """
    创建obj并添加与Mark相关的属性，然后返回obj
    """
    markIns = Mark()
    return markIns.obj
