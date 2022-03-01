# -*- coding: utf8 -*-

import FreeCADGui
import FreeCAD
import Part
import math
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolToroidal_Section:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        建模过程：
        1.通过投影找到控制角度的两点与轨迹弧线之间的交点
        2.通过中心和两个端点求出这三个点中间另外一点
        3.通过弧上三个点求出这条弧线
        4.求出轮廓圆面，圆面扫掠弧生成体

        错误情况分析：
        1.方向：点12重合，圆环区域体法向不能确定
        2.半径：主半径或次半径为0或负，或者次半径大于主半径
        3.弧段范围：起点3或终点4在底面的投影与底面圆心重合，环形区域体区域范围无法确定
            边界情况分析：
            1.主半径等于次半径且非0 ——> 即一个圆绕其一条切线旋转
            2.主半径为正，次半径为0 ——> 形成一个圆环或圆弧 ——> 不属于三维立体范围，排除情况
            3.起始位置与终点位置在底面的投影为同一点，即始末位置投影夹角为0°或360° ——> 以360°为准，建模出一个圆环体
            注：主半径为0，次半径为正 ——> 即横截面圆心为point1，该圆绕直径旋转，形成部分球体 ——> 超出圆环区域体范围，不考虑

        """
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        point3 = Tools3D.transToRecVector(fp.Point3X.Value, fp.Point3Y.Value, fp.Point3Z.Value)
        point4 = Tools3D.transToRecVector(fp.Point4X.Value, fp.Point4Y.Value, fp.Point4Z.Value)

        Sym = point2.sub(point1)

        if not Sym.Length:
            Tools3D.sayz("坐标有误，请重新输入!")
            return
        elif fp.MajorRadius.Value <= 0.0 or fp.MinorRadius.Value <= 0.0 or fp.MajorRadius.Value < fp.MinorRadius.Value:
            Tools3D.sayz("半径有误，请重新输入")
            return
        else:
            # 圆环区域体对称轴单位向量，其方向表示圆环区域体的方向
            SymmetryAxis = Sym.normalize()

            # 将Vector_1to3、Vector_1to4投影到主圆环所在平面上，即由对称轴向量SymmetryAxis和圆环区域体中心的point1唯一确定的平面
            Vector_1to3 = point3.sub(point1)
            Vector_1to3_projectToPlane = Vector_1to3.projectToPlane(FreeCAD.Vector(0.0,0.0,0.0), SymmetryAxis)
            Vector_1to4 = point4.sub(point1)
            Vector_1to4_projectToPlane = Vector_1to4.projectToPlane(FreeCAD.Vector(0.0,0.0,0.0), SymmetryAxis)

            if Vector_1to3_projectToPlane.Length == 0.0:
                Tools3D.sayz("起点坐标有误，请重新输入!")
                return
            elif Vector_1to4_projectToPlane.Length == 0.0:
                Tools3D.sayz("终点坐标有误，请重新输入!")
                return
            else:
                # “MajorRadius”表示半圆环体中心点到圆形横截面中心的距离，“MinorRadius”表示圆形横截面的半径

                # 确定Vector_1to3_projectToPlane与弧段的交点位置，即弧段的起始位置
                # k_start为比例因子，确定起始位置处MajorRadius长度与投影向量长的比值
                k_start = fp.MajorRadius.Value / Vector_1to3_projectToPlane.Length
                Vector_1toPointStart = k_start * Vector_1to3_projectToPlane
                point_start = Vector_1toPointStart.add(point1)

                # 确定Vector_1to4_projectToPlane与弧段的交点位置，即弧段的终点位置
                # k_end为比例因子，确定终点位置处MajorRadius与投影向量长的比值
                k_end = fp.MajorRadius.Value / Vector_1to4_projectToPlane.Length
                Vector_1toPointEnd = k_end * Vector_1to4_projectToPlane
                point_end = Vector_1toPointEnd.add(point1)

                # 确定始末位置转过的角度
                angle = Vector_1toPointStart.getAngle(Vector_1toPointEnd) * 180 / math.pi

                try:
                    # 始末位置在底面的投影为同一点，建模一个完整的圆环体
                    if angle == 0.0 and fp.MinorRadius.Value != 0.0:
                        fp.Shape = Part.makeTorus(fp.MajorRadius.Value, fp.MinorRadius.Value, point1, SymmetryAxis)
                        return
                    elif angle == 0.0 and fp.MinorRadius.Value == 0.0:
                        fp.Shape = Part.makeCircle(fp.MajorRadius.Value, point1, SymmetryAxis)

                    # angle非0的情况
                    else:
                        # 在point1处将点旋转 angle/2 度，将度数转化为弧度
                        # q = (vNormal*sin(θ/2), cos(θ/2))  θ是需要旋转的角度
                        sinValue = math.sin(angle / 4.0 * math.pi / 180.0)
                        cosValue = math.cos(angle / 4.0 * math.pi / 180.0)

                        # 四元数
                        q = FreeCAD.Rotation(sinValue * SymmetryAxis.x,
                                             sinValue * SymmetryAxis.y,
                                             sinValue * SymmetryAxis.z,
                                             cosValue)
                        # 绕底面圆旋转后的点
                        vOrigin = q.multVec(Vector_1toPointStart)
                        # 平移到point1的位置
                        vPoint1 = vOrigin.add(point1)

                        # 创建扫掠路径arc
                        arc = Part.ArcOfCircle(point_start, vPoint1, point_end)
                        arcShape = arc.toShape()

                        # 如果次半径为0，则arc即为将建成的圆弧
                        if fp.MinorRadius.Value == 0.0:
                            fp.Shape = arcShape
                        else:
                            # 创建路径弧path
                            path = Part.Wire(arcShape)
                            # 路径弧方向normalCircle
                            normalCircle = Vector_1toPointStart.cross(SymmetryAxis)
                            # 轮廓圆边circle，并创建圆面circleFace
                            circle = Part.Circle(point_start, normalCircle, fp.MinorRadius.Value)
                            circleFace = Part.makeFace([Part.Wire(circle.toShape())], "Part::FaceMakerBullseye")
                            # 沿路径path扫掠生成管道，即为最终的Toroidal_Section
                            fp.Shape = path.makePipe(circleFace)
                    return
                except:
                    Tools3D.sayz("Redraw Toroidal_Section Failed!")


class Toroidal_Section:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolToroidal_Section_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Toroidal_Section)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Toroidal_Section", "环形区域体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Toroidal_Section
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0.01
            obj.addProperty("App::PropertyDistance", "Point3X").Point3X = 0.01
            obj.addProperty("App::PropertyDistance", "Point3Y").Point3Y = 0
            obj.addProperty("App::PropertyDistance", "Point3Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y").Point4Y = 0.01
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
        obj.addProperty("App::PropertyDistance", "MajorRadius").MajorRadius = 0.01
        obj.addProperty("App::PropertyDistance", "MinorRadius").MinorRadius = 0.005
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 4)
        Tools3D.getHelperValue(obj)
        Tools3D.addRadiusProperty(obj)
        Tools3D.getRadiusProperty(obj)


def getObject():
    """
    返回获取的obj
    """
    toroidal_Section = Toroidal_Section()
    VolToroidal_Section(toroidal_Section.obj)
    Tools3D.ViewProvider(toroidal_Section.obj.ViewObject)
    return toroidal_Section.obj
