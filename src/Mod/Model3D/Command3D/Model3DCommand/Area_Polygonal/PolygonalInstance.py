# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import re


class CreatePolygonal:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        先获取模型的属性列表，再逐一匹配选出符合“point+数字”形式的属性，获取其存储的vector，按顺序接入drawpoints列表中，注意最后要放入point1使首尾闭合，再按顺序连线，然后形成面。
        此模型各点设置必须按多边形建模顺序完成，否则会无法形成面，提示错误，并建模出奇怪图形。
        只有在连线闭合不相交的情况下才能形成面，不报错。
        """
        temp_list = fp.PropertiesList
        drawPoints = []
        # 匹配point10以上的点
        temp_1 = []
        temp_10 = []
        for i in temp_list:
            if re.match(r'Point\d\d', i, re.I):
                temp_10.append(i)

        for i in temp_list:
            if i not in temp_10:
                if re.match(r'Point\d', i, re.I):
                    temp_1.append(i)
        temp_1.sort()
        temp_10.sort()
        result_list = temp_1 + temp_10
        for i in result_list:
            Tools3D.sayz("i="+str(i)+"\n")
            ve = getattr(fp, i)
            curPoint = Tools3D.pointToRecVec(ve)
            drawPoints.append(curPoint)

        end = getattr(fp, "Point1")
        curEndPoint = Tools3D.pointToRecVec(end)
        drawPoints.append(curEndPoint)
        if not ObjectTools.isFourPointsOnTheSamePlane(drawPoints):
            Tools3D.sayz("多边形的坐标必须在一个平面上")
            return
        wireOfPolygonal = Part.makePolygon(drawPoints)
        try:
            fp.Shape = Part.makeFace(wireOfPolygonal, "Part::FaceMakerExtrusion")
        except:
            fp.Shape = wireOfPolygonal
            Tools3D.sayz("错误")
        pass


class Polygonal:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreatePolygonal_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Area_Polygonal")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "AreaG", "面")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = "Area_Polygonal"
        obj.addProperty("App::PropertyInteger", "Order").Order = 999
        obj.addProperty("App::PropertyInteger", "NumbersOfPoints", "Object of a PolygonalArea", "").NumbersOfPoints = 3
        obj.addProperty("App::PropertyString", "MarkX", "NonUniformGrid", "").MarkX = "DX1"
        obj.addProperty("App::PropertyString", "MarkY", "NonUniformGrid", "").MarkY = "DX2"
        obj.addProperty("App::PropertyString", "MarkZ", "NonUniformGrid", "").MarkZ = "DX3"
        obj.addProperty("App::PropertyBool", "isMarkX", "NonUniformGrid", "").isMarkX = False
        obj.addProperty("App::PropertyBool", "isMarkY", "NonUniformGrid", "").isMarkY = False
        obj.addProperty("App::PropertyBool", "isMarkZ", "NonUniformGrid", "").isMarkZ = False
        obj.addProperty("App::PropertyBool", "isCheckMinX", "NonUniformGrid", "").isCheckMinX = False
        obj.addProperty("App::PropertyBool", "isCheckMidX", "NonUniformGrid", "").isCheckMidX = False
        obj.addProperty("App::PropertyBool", "isCheckMaxX", "NonUniformGrid", "").isCheckMaxX = False
        obj.addProperty("App::PropertyBool", "isCheckMinY", "NonUniformGrid", "").isCheckMinY = False
        obj.addProperty("App::PropertyBool", "isCheckMidY", "NonUniformGrid", "").isCheckMidY = False
        obj.addProperty("App::PropertyBool", "isCheckMaxY", "NonUniformGrid", "").isCheckMaxY = False
        obj.addProperty("App::PropertyBool", "isCheckMinZ", "NonUniformGrid", "").isCheckMinZ = False
        obj.addProperty("App::PropertyBool", "isCheckMidZ", "NonUniformGrid", "").isCheckMidZ = False
        obj.addProperty("App::PropertyBool", "isCheckMaxZ", "NonUniformGrid", "").isCheckMaxZ = False
        # obj.addProperty("App::PropertyVectorList", "Points", "", "").Points = []
        obj.addProperty("App::PropertyVectorDistance", "Point1", "Object of a PolygonalArea",
                        "Point of the PolygonalArea")
        obj.addProperty("App::PropertyVectorDistance", "Point2", "Object of a PolygonalArea",
                        "Point of the PolygonalArea")
        obj.addProperty("App::PropertyVectorDistance", "Point3", "Object of a PolygonalArea",
                        "Point of the PolygonalArea")
        Tools3D.addHelperProperty(obj, 3)


def getObject():
    polygonal = Polygonal()
    CreatePolygonal(polygonal.obj)
    Tools3D.ViewProvider(polygonal.obj.ViewObject)
    return polygonal.obj

