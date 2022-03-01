# -*- coding: utf-8 -*-
import FreeCAD

from Modeling.Modeling2D.Modeling2DCommand.NetStepSetting import NetStepSettingInstance
from Modeling.Modeling2D.Tools import Tools2D, ToolsForDisplay
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
import PartChipic


class AreaFunction(object):
    def __init__(self):
        # self.obj = None
        FreeCAD.ActiveDocument.openTransaction("CreateAreaFunction")
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "AreaFunction")
        FreeCAD.ActiveDocument.commitTransaction()
        self.__setProperty(self.obj)

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.AreaFunction
        self.obj.addProperty("App::PropertyString", "expression").expression = "x^2+y^2-1"
        self.obj.addProperty("App::PropertyInteger", "precision").precision = 50
        Tools2D.addCommonPropertyToObject(obj)
        Tools2D.addAttributeToObject(obj)

        AreaFunctionProxy(obj)
        # just set it to something different from None (this assignment is needed to run an internal notification)
        obj.ViewObject.Proxy = 0


def getObject():
    """
    创建obj并添加与AreaRan相关的属性，然后返回obj
    """
    areaFunIns = AreaFunction()
    return areaFunIns.obj


class AreaFunctionProxy:
    def __init__(self, obj):
        "Add some custom properties to our box feature"
        obj.Proxy = self

    def execute(self, fp):
        self.redaw(fp)
        ToolsForDisplay.setColors(fp)

    def redaw(self, fp):
        sys = FreeCAD.ActiveDocument.CoordinateSystem
        # 获取工作区间
        workPlane = NetStepSettingInstance.getObject()
        x1 = workPlane.point1_X
        x2 = workPlane.point2_X
        y1 = workPlane.point1_Y
        y2 = workPlane.point2_Y
        x1 = FreeCAD.Units.Quantity(x1).Value
        x2 = FreeCAD.Units.Quantity(x2).Value
        y1 = FreeCAD.Units.Quantity(y1).Value
        y2 = FreeCAD.Units.Quantity(y2).Value
        if x1 == x2:
            x2 += 1
        if y1 == y2:
            y2 += 1

        fp.Shape = PartChipic.makeFuncMesh(20,                  # type
                                           fp.expression,       # func
                                           x1, x2,                # xMax, xMin
                                           y1, y2,                # yMax, yMin
                                           0, 0,                # zMax, zMin
                                           sys,                 # 坐标系
                                           str(fp.precision),   # 精度
                                           fp.Attribute)        # 属性

    # def redraw(self,obj):
    #    from Modeling3D.Tools import  OtherTools
    #    expressionStr=OtherTools.parseExpressionStr(obj.Expression.replace(" ",""))
    #    import re
    #    expressionStr=re.sub(r"\b[r|R]\b","(sqrt(x*x+y*y))",expressionStr)
    #    expressionStr=re.sub(r"\btheta\b","(atan(y/x))",expressionStr,flags=re.IGNORECASE)
    #    expressionStr=OtherTools.parseFunctionObjStr(expressionStr)
    #    simobj=FreeCAD.ActiveDocument.getObject("SIMUVOLUME")
    #    try:
    #       obj.Shape=PartChipic.makeFuncMesh(20,expressionStr,simobj.point1_X,simobj.point2_X,simobj.point1_Y,simobj.point2_Y,0,0,0,"")
    #    except:
    #         from Modeling.Common.Tools import DocumentTools
    #         DocumentTools.printErrorMessage("Redraw 2DAreaFunction Failed!")
    #
    # def execute(self, fp):
    #    if self.flagExcute:
    #       self.redraw(fp)
    #       self.flagExcute=False


