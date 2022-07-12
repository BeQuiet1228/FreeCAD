# -*- coding: utf8 -*-
import FreeCAD
import Part
import math
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolParallelepipedal:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        建模过程：
        1.以两条棱：棱12和棱13建立平行四边形
        2.以余下一条棱：棱14为路径，平行四边形沿路径扫掠形成平行六面体

        错误情况分析：
        1.三条棱长度大于0
        2.三条棱中任意两条都不共线
        3.三条棱不共面

        """
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        point3 = Tools3D.transToRecVector(fp.Point3X.Value, fp.Point3Y.Value, fp.Point3Z.Value)
        point4 = Tools3D.transToRecVector(fp.Point4X.Value, fp.Point4Y.Value, fp.Point4Z.Value)

        # 平行六面体的三条棱向量
        Vector_12 = point2.sub(point1)
        Vector_13 = point3.sub(point1)
        Vector_14 = point4.sub(point1)

        if Vector_12.Length == 0.0:
            Tools3D.sayz("棱12坐标有误，请重新输入!")
            return
        elif Vector_13.Length == 0.0:
            Tools3D.sayz("棱13坐标有误，请重新输入!")
            return
        elif Vector_14.Length == 0.0:
            Tools3D.sayz("棱14坐标有误，请重新输入!")
            return
        elif Vector_12.getAngle(Vector_13)*180/math.pi == 0.0 or Vector_12.getAngle(Vector_13)*180/math.pi == 180.0:
            Tools3D.sayz("棱12和棱13共线，请重新输入!")
            return
        elif Vector_12.getAngle(Vector_14)*180/math.pi == 0.0 or Vector_12.getAngle(Vector_14)*180/math.pi == 180.0:
            Tools3D.sayz("棱12和棱14共线，请重新输入!")
            return
        elif Vector_13.getAngle(Vector_14)*180/math.pi == 0.0 or Vector_13.getAngle(Vector_14)*180/math.pi == 180.0:
            Tools3D.sayz("棱13和棱14共线，请重新输入!")
            return
        else:
            # 求三向量构成的行列式的值，若值为0，则三向量共面，不能构成平行六面体
            detValue = Vector_12.x * Vector_13.y * Vector_14.z + \
                       Vector_13.x * Vector_14.y * Vector_12.z + \
                       Vector_14.x * Vector_12.y * Vector_13.z - \
                       Vector_12.x * Vector_14.y * Vector_13.z - \
                       Vector_13.x * Vector_12.y * Vector_14.z - \
                       Vector_14.x * Vector_13.y * Vector_12.z
            if detValue == 0:
                Tools3D.sayz("三条棱共面，请重新输入!")
                return
            else:
                try:
                    # 确定该平行四边形最后一点temp_point，以棱12，13为两邻边，构造平行四边形
                    temp_point = point2.add(Vector_13)
                    parallelogram = Part.makePolygon([point1, point2, temp_point, point3, point1])
                    paraFace = Part.makeFace([Part.Wire(parallelogram)], "Part::FaceMakerBullseye")
                    # 创建路径，即棱14
                    edge14 = Part.makeLine(point1, point4)
                    path = Part.Wire(edge14)
                    # 平行四边形沿棱14扫掠形成平行六面体
                    fp.Shape = path.makePipe(paraFace)
                    return
                except:
                    Tools3D.sayz("Redraw Parallelepipedal Failed!")

class Parallelepipedal:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolParallelepipedal_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Parallelepipedal)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Parallelepipedal", "平行六面体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Parallelepipedal
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = -0.01
            obj.addProperty("App::PropertyDistance", "Point3Y").Point3Y = 0
            obj.addProperty("App::PropertyDistance", "Point3Z").Point3Z = 0.01
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y").Point4Y = 0.02
            obj.addProperty("App::PropertyDistance", "Point4Z").Point4Z = 0
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = 0
            obj.addProperty("App::PropertyAngle", "Point3Y").Point3Y = 0
            obj.addProperty("App::PropertyDistance", "Point3Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = 0
            obj.addProperty("App::PropertyAngle", "Point4Y").Point4Y = 0
            obj.addProperty("App::PropertyDistance", "Point4Z").Point4Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = 0
            obj.addProperty("App::PropertyDistance", "Point3Y").Point3Y = 0
            obj.addProperty("App::PropertyAngle", "Point3Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y").Point4Y = 0
            obj.addProperty("App::PropertyAngle", "Point4Z").Point4Z = 0

        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 4)
        Tools3D.getHelperValue(obj)

def getObject():
    """
    返回获取的obj
    """
    parallelepipedal = Parallelepipedal()
    VolParallelepipedal(parallelepipedal.obj)
    Tools3D.ViewProvider(parallelepipedal.obj.ViewObject)
    return parallelepipedal.obj
