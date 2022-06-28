# -*- coding: utf8 -*-
import FreeCAD
import Part
import math
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolAnnular_Section:
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
        4.求出矩形四个点，形成矩形面，矩形面扫掠弧生成体

        错误情况分析：
        1.方向：点12重合，环形区域体高度为0且方向不能确定
        2.半径：内半径和外半径为0或负，或者内半径大于等于外半径
        3.弧段范围：起点3或终点4在底面的投影与底面圆心重合，环形区域体区域范围无法确定
            边界情况分析：
            1.内半径等于外半径 ——> 建模出一个两边为直线，两边为弧线的平行曲面 ——>不属于三维立体范围，排除情况
            2.起始位置与终点位置在底面的投影为同一点，即始末位置投影夹角为0°或360° ——> 以360°为准，建模出一个环形体
            注：内半径为0 ——> 即横截面矩形绕其一条边旋转，形成部分圆柱体 ——> 不属于环形区域体范围，排除情况

        """
        point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
        point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
        point3 = Tools3D.transToRecVector(fp.Point3X.Value, fp.Point3Y.Value, fp.Point3Z.Value)
        point4 = Tools3D.transToRecVector(fp.Point4X.Value, fp.Point4Y.Value, fp.Point4Z.Value)

        # 底面法向量，表示环形区域体底部到顶部的方向，其长度表示环形区域体的高度
        normalVec = point2.sub(point1)
        normalizedVec = point2.sub(point1).normalize()

        if not normalVec.Length:
            Tools3D.sayz("坐标有误，请重新输入!")
            return
        elif fp.InnerRadius.Value < 0.0 or fp.OuterRadius.Value <= 0.0 or fp.InnerRadius.Value >= fp.OuterRadius.Value:
            Tools3D.sayz("半径有误，请重新输入")
            return
        else:
            # 以底面为基准，将Vector_1to3、Vector_1to4投影到底面
            Vector_1to3 = point3.sub(point1)
            Vector_1to3_projectToPlane = Vector_1to3.projectToPlane(FreeCAD.Vector(0.0,0.0,0.0), normalizedVec)
            Vector_1to4 = point4.sub(point1)
            Vector_1to4_projectToPlane = Vector_1to4.projectToPlane(FreeCAD.Vector(0.0,0.0,0.0), normalizedVec)

            if Vector_1to3_projectToPlane.Length == 0.0:
                Tools3D.sayz("起点坐标有误，请重新输入!")
                return
            elif Vector_1to4_projectToPlane.Length == 0.0:
                Tools3D.sayz("终点坐标有误，请重新输入!")
                return
            else:
                # 确定Vector_1to3_projectToPlane与弧段的交点位置，即弧段的内外起始位置
                # k_start为比例因子，确定起始位置内外半径长度与投影向量长的比值
                innerRadius = max(fp.InnerRadius.Value, 0.00003)
                outerRadius = max(fp.OuterRadius.Value, 0.00003)

                k_start_Inner = innerRadius / Vector_1to3_projectToPlane.Length
                k_start_Outer = outerRadius / Vector_1to3_projectToPlane.Length
                Vector_start_InnerIntersection = k_start_Inner * Vector_1to3_projectToPlane + point1
                Vector_start_OuterIntersection = k_start_Outer * Vector_1to3_projectToPlane + point1

                # 在这里求出顶面的弧段内外起始位置，即上述两点的正上方两点位置
                Vector_Top_start_InnerIntersection = Vector_start_InnerIntersection + normalVec
                Vector_Top_start_OuterIntersection = Vector_start_OuterIntersection + normalVec

                # 确定Vector_1to4_projectToPlane与弧段的交点位置，即弧段的内外终点位置
                # k_end为比例因子，确定终点位置外半径长度与投影向量长的比值
                k_end_Outer = outerRadius / Vector_1to4_projectToPlane.Length
                Vector_end_OuterIntersection = k_end_Outer * Vector_1to4_projectToPlane + point1

                # 以外弧为基准，确定始末位置转过的角度
                Vector_start = k_start_Outer * Vector_1to3_projectToPlane
                Vector_end = k_end_Outer * Vector_1to4_projectToPlane
                angle = Vector_start.getAngle(Vector_end) * 180.0 / math.pi

                try:
                    # 始末位置在底面的投影为同一点，建模一个完整的环形体
                    if angle == 0.0:
                        if fp.InnerRadius.Value == 0:
                            e1 = Part.makeCircle(0.00002, point1, normalizedVec)
                        else:
                            e1 = Part.makeCircle(fp.InnerRadius.Value, point1, normalizedVec)
                        e2 = Part.makeCircle(fp.OuterRadius.Value, point1, normalizedVec)
                        wires = [e1, e2]
                        line = Part.makeLine(point1, point2)
                        path = Part.Wire(line)
                        shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
                        fp.Shape = path.makePipe(shapeCircle)
                        return
                    else:
                        # 在底面圆心位置将点旋转 angle/2 度，将度数转化为弧度
                        sinValue = math.sin(angle / 4.0 * math.pi / 180.0)
                        cosValue = math.cos(angle / 4.0 * math.pi / 180.0)
                        # 四元数
                        q = FreeCAD.Rotation(sinValue * normalizedVec.x, sinValue * normalizedVec.y,
                                             sinValue * normalizedVec.z, cosValue)
                        # 绕底面圆旋转后的点
                        vOrigin = q.multVec(Vector_start)
                        # 平移到point1的位置
                        vPoint1 = vOrigin.add(point1)

                        # 创建路径弧path
                        arc = Part.ArcOfCircle(Vector_start_OuterIntersection, vPoint1,
                                               Vector_end_OuterIntersection)
                        arcShape = arc.toShape()
                        path = Part.Wire(arcShape)

                        # 生成底面上环形扇面
                        R = Part.makeLine(Vector_start_InnerIntersection, Vector_start_OuterIntersection)
                        face = path.makePipe(R)

                        # 底面沿高扫掠，生成环形区域体
                        RCenter = (Vector_start_InnerIntersection + Vector_start_OuterIntersection) / 2.0
                        h = Part.makeLine(RCenter, RCenter + normalVec)
                        h_path = Part.Wire(h)
                        fp.Shape = h_path.makePipe(face)

                        # 创建轮廓矩形rectangle，并生成矩形面rectangleFace
                        # rectangle = Part.makePolygon([Vector_start_OuterIntersection,
                        #                               Vector_start_InnerIntersection,
                        #                               Vector_Top_start_InnerIntersection,
                        #                               Vector_Top_start_OuterIntersection,
                        #                               Vector_start_OuterIntersection])
                        # rectangleFace = Part.makeFace([Part.Wire(rectangle)], "Part::FaceMakerBullseye")
                        # fp.Shape = path.makePipe(rectangleFace)
                        return

                except:
                    Tools3D.sayz("Redraw Annular_Section Failed!")


class Annular_Section:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolAnnular_Section_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Annular_Section)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Annular_Section", "环形区域体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Annular_Section
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

        obj.addProperty("App::PropertyDistance", "InnerRadius").InnerRadius = 0.005
        obj.addProperty("App::PropertyDistance", "OuterRadius").OuterRadius = 0.01
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
    annular_Section = Annular_Section()
    VolAnnular_Section(annular_Section.obj)
    Tools3D.ViewProvider(annular_Section.obj.ViewObject)
    return annular_Section.obj
