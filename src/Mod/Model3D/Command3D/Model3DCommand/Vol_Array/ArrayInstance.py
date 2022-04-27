# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
import re
import math


class CreateArray:
    """
    by zby
    参数阵列体的建模在DialogMian文件中进行。execute直接做pass处理
    具体的建模流程
    在点击确定获取文本框中的信息时，首先通过下拉框的索引判断模型类型
    然后再进入该模型对应的数据处理逻辑
    以start_i和end_i为起始和结束进行循环
    输入数据通过getTheValue（对应属性App::PropertyDistance情况下）和getOtherValue（对应属性App::PropertyAngle情况下）函数进行处理
    如果输入数据中含有‘i'，则其替换为目前的循环逻辑计数，然后调用特定参数获取函数获取函数的值
    如果不含，则借助帮助属性helper1或helper2，直接进行一般数据处理流程，函数返回帮助属性储存的FreeCad建模需求数据
    得到数据后，调用ArrayInstance中单独写的绘图建模函数获取shape
    （该函数直接输入建模数据，返回值为模型的shape）h
    完成一次循环获取到shape后，将shape放入list中
    在所有循环完成后，如果list中的shape数量不为零，则统一为它们进行布尔运算
    完成后即得到建模结果
    """
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def redraw(self,obj):
        objs = obj.Shapes
        theFirstShape = None
        otherShapes = []


        if len(obj.Shapes) <= 0:
            obj.Shapes = None
        elif len(obj.Shapes) == 1:
            obj.Shape = obj.Shapes[0]
        else:
            theFirstShape = obj.Shapes[0]
            otherShapes = obj.Shapes[1:]
            obj.Shape = theFirstShape.multiFuse(otherShapes)

    def execute(self, fp):
        """

        """
        pass
        # self.redraw(fp)


class Array:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolArray')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Vol_Parameter")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Array", "阵列体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_ParamArray
        obj.addProperty("App::PropertyInteger", "Order").Order = 999
        # obj.addProperty("App::PropertyInteger", "NumbersOfPoints", "Object of a PolygonalArea", "").NumbersOfPoints = 3
        obj.addProperty("App::PropertyString", "Attribute", "Attribute", "Conformal of Object").Attribute = "NotDefine"
        obj.addProperty("App::PropertyString", "MarkX", "NonUniformGrid", "").MarkX = "DX1"
        obj.addProperty("App::PropertyString", "MarkY", "NonUniformGrid", "").MarkY = "DX2"
        obj.addProperty("App::PropertyString", "MarkZ", "NonUniformGrid", "").MarkZ = "DX3"
        obj.addProperty("App::PropertyBool", "isMarkX", "NonUniformGrid", "").isMarkX = True
        obj.addProperty("App::PropertyBool", "isMarkY", "NonUniformGrid", "").isMarkY = True
        obj.addProperty("App::PropertyBool", "isMarkZ", "NonUniformGrid", "").isMarkZ = True
        obj.addProperty("App::PropertyString", "BaseObjType", "Object of a ParamArray", "").BaseObjType = "正投影体"
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyStringList", "BaseObjData", "Object of a ParamArray", "").BaseObjData =["xli'i'", "yli'i'", "zli'i'", "xlf'i'", "ylf'i'", "zlf'i'"]
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyStringList", "BaseObjData", "Object of a ParamArray", "").BaseObjData =["rli'i'", "theta_i'i'", "zli'i'", "rlf'i'", "theta_f'i'", "zlf'i'"]
        else:
            obj.addProperty("App::PropertyStringList", "BaseObjData", "Object of a ParamArray", "").BaseObjData =["zli'i'", "rli'i'", "theta_i'i'", "zlf'i'", "rlf'i'", "theta_f'i'"]
        obj.addProperty("App::PropertyInteger", "IFrom", "Object of a ParamArray", "start i").IFrom = 1
        obj.addProperty("App::PropertyInteger", "ITo", "Object of a ParamArray", "end i").ITo = 2
        obj.addProperty("App::PropertyDistance", "Helper1").Helper1 = 0
        obj.addProperty("App::PropertyAngle", "Helper2").Helper2 = 0

def getObject():
    array = Array()
    CreateArray(array.obj)
    Tools3D.ViewProvider(array.obj.ViewObject)
    return array.obj


def drawSpherical(p1, p2, p3, radius):
        point=Tools3D.transToRecVector(p1, p2, p3)
        if radius <= 0:
            Tools3D.sayz("半径有误，请重新输入")
            return None
        else:
            try:
                return Part.makeSphere(radius, point)
            except:
                Tools3D.sayz("Redraw Spherical Failed!")
                return None


def drawComformal(p1, p2, p3, p4, p5, p6):
    coordinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coordinate == 'Rectangular':
        length = abs(p1 - p4)
        width = abs(p2 - p5)
        height = abs(p3 - p6)
        direction = FreeCAD.Vector(0, 0, 1)
        start_point = FreeCAD.Vector(min(p1, p4),
                                     min(p2, p5),
                                     min(p3, p6))
        try:
            return Part.makeBox(length, width, height, start_point, direction)
        except:
            Tools3D.sayz(u"point1和point2的X,Y,Z方向坐标不能相同。")
            Tools3D.sayz("Redraw Conformal Failed!")
            return
    else:
        if p1 != p4 and p2 != p5 and p3 != p6:
            # 数据处理
            if coordinate == "Polar":
                if p1 < 0 or p4 < 0:
                    Tools3D.sayz(u"R不能为负")
                    Tools3D.sayz("Redraw Conformal Failed!")
                    return
                else:
                    height = abs(p3 - p6)
                    h_bottom = min(p3, p6)
                    h_top = max(p3, p6)
                    minRadius = min(p1, p4)
                    maxRadius = max(p1, p4)
                    angle_start = p2 % 360.0
                    angle_end = p5 % 360.0
                    # 始末位置的角度，采用弧度制
                    theta_start = (p2 % 360.0) * math.pi / 180.0
                    theta_end = (p5 % 360.0) * math.pi / 180.0
            else:
                if p2 < 0 or p5 < 0:
                    Tools3D.sayz(u"R不能为负")
                    Tools3D.sayz("Redraw Conformal Failed!")
                    return
                else:
                    height = abs(p1 - p4)
                    h_bottom = min(p1, p4)
                    h_top = max(p1, p4)


                    minRadius = min(p2, p5)
                    maxRadius = max(p2, p5)
                    angle_start = p3 % 360.0
                    angle_end = p6 % 360.0
                    theta_start = (p3 % 360.0) * math.pi / 180.0
                    theta_end = (p6 % 360.0) * math.pi / 180.0

            normalVec = FreeCAD.Vector(0, 0, height)
            o_bottom = FreeCAD.Vector(0, 0, h_bottom)
            o_top = FreeCAD.Vector(0, 0, h_top)
            angle = math.fabs(theta_end - theta_start)

            # 建模(采用环形区域体Annular_Section建模方法)
            if angle == 0:
                # 夹角为0，则说明投影出的是一个完整的环形体
                if minRadius == 0:
                    minRadius = 0.000000001
                e1 = Part.makeCircle(minRadius, o_bottom, normalVec)
                e2 = Part.makeCircle(maxRadius, o_bottom, normalVec)
                wires = [e1, e2]
                line = Part.makeLine(o_bottom, o_top)
                path = Part.Wire(line)
                shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
                return path.makePipe(shapeCircle)
            else:
                sinValue = math.sin(angle / 4.0)
                cosValue = math.cos(angle / 4.0)
                # 四元数
                q = FreeCAD.Rotation(sinValue * FreeCAD.Vector(0, 0, 1).x, sinValue * FreeCAD.Vector(0, 0, 1).y,
                                     sinValue * FreeCAD.Vector(0, 0, 1).z, cosValue)
                # 确定底面外弧上起始位置和终点位置
                point_outer_start = FreeCAD.Vector(maxRadius * math.cos(theta_start),
                                                   maxRadius * math.sin(theta_start), h_bottom)
                point_outer_end = FreeCAD.Vector(maxRadius * math.cos(theta_end),
                                                 maxRadius * math.sin(theta_end), h_bottom)
                # 确定底面内弧起点
                point_inner_start = FreeCAD.Vector(minRadius * math.cos(theta_start),
                                                   minRadius * math.sin(theta_start), h_bottom)
                # 绕底面圆旋转后的点
                vOrigin = q.multVec(point_outer_start.sub(o_bottom))
                vPoint = vOrigin.add(o_bottom)

                # 创建路径弧path
                arc = Part.ArcOfCircle(point_outer_start, vPoint, point_outer_end)
                arcShape = arc.toShape()
                path = Part.Wire(arcShape)

                # 生成底面上环形扇面
                R = Part.makeLine(point_inner_start, point_outer_start)
                face = path.makePipe(R)

                # 底面沿高扫掠，生成环形区域体
                RCenter = (point_inner_start + point_outer_start) / 2.0
                h = Part.makeLine(RCenter, RCenter + normalVec)
                h_path = Part.Wire(h)
                return h_path.makePipe(face)


def drawCylinder(p1, p2, p3, p4, p5, p6, radius):
    point1 = Tools3D.transToRecVector(p1, p2, p3)
    point2 = Tools3D.transToRecVector(p4, p5, p6)
    normal = point2.sub(point1)
    height = normal.Length
    try:
        if radius <= 0:
            # 警告用户数据错误及错误原因
            Tools3D.sayz("错误，半径不能小于等于零")
            return None
        else:
            if point1 != point2:
                return Part.makeCylinder(radius, height, point1, normal, 360)
            else:
                return None

    except:
        Tools3D.sayz("Redraw Cylinder Failed!")


def drawAnnular(p1, p2, p3, p4, p5, p6, radius1, radius2):
    point1 = Tools3D.transToRecVector(p1, p2, p3)
    point2 = Tools3D.transToRecVector(p4, p5, p6)
    dir = point2 - point1
    if not dir.Length:
        Tools3D.sayz(u"point1和point2重合，请重新输入!")
        return

    if radius1 < 0 or radius2 <= 0 or radius1 >= radius2:
        Tools3D.sayz("半径有误，请重新输入")
        return
    if radius1 == 0:
        # 内半径为0的情况，建模为圆柱
        return Part.makeCylinder(radius2, dir.Length, point1, dir, 360)
    e1 = Part.makeCircle(radius1, point1, dir)
    e2 = Part.makeCircle(radius2, point1, dir)
    wires = [e1, e2]
    try:
        line = Part.makeLine(point1, point2)
        path = Part.Wire(line)
        shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
        return path.makePipe(shapeCircle)
    except:
        Tools3D.sayz("Redraw Annular Failed!")

def drawSpecialCone(p1, p2, p3, p4, p5, p6, radius1, radius2):
    point1 = Tools3D.transToRecVector(p1, p2, p3)
    point2 = Tools3D.transToRecVector(p4, p5, p6)
    vector = point2 - point1
    height = point1.distanceToPoint(point2)
    # 上下半径相等为圆柱，也可以按圆台画法绘制
    # 圆环
    try:
        if height == 0:
            # 警告用户数据错误及错误原因
            Tools3D.sayz("错误，高不能等于零")
            pass
        # 圆环，台，锥
        else:
            if radius1 == 0 and radius2 == 0:
                # 警告用户数据错误及错误原因
                Tools3D.sayz("错误。上下半径不能同时等于零")
                pass
                # fp.Shape = Part.makeCylinder(fp.Radius_Bottom.Value, height, point1, vector, 360)
            elif radius1 < 0 or radius2 < 0:
                Tools3D.sayz("错误。上下半径不能小于零")
            else:
                return Part.makeCone(radius1, radius2, height, point1, vector)
    except:
        Tools3D.sayz("Redraw SpecialCone Failed!")


def drawAnnularSection(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, radius1, radius2):
    point1 = Tools3D.transToRecVector(p1, p2, p3)
    point2 = Tools3D.transToRecVector(p4, p5, p6)
    point3 = Tools3D.transToRecVector(p7, p8, p9)
    point4 = Tools3D.transToRecVector(p10, p11, p12)

    # 底面法向量，表示环形区域体底部到顶部的方向，其长度表示环形区域体的高度
    normalVec = point2.sub(point1)
    normalizedVec = point2.sub(point1).normalize()

    if not normalVec.Length:
        Tools3D.sayz("坐标有误，请重新输入!")
        return
    elif radius1 < 0.0 or radius2 <= 0.0 or radius1 >= radius2:
        Tools3D.sayz("半径有误，请重新输入")
        return
    else:
        # 以底面为基准，将Vector_1to3、Vector_1to4投影到底面
        Vector_1to3 = point3.sub(point1)
        Vector_1to3_projectToPlane = Vector_1to3.projectToPlane(FreeCAD.Vector(0.0, 0.0, 0.0), normalizedVec)
        Vector_1to4 = point4.sub(point1)
        Vector_1to4_projectToPlane = Vector_1to4.projectToPlane(FreeCAD.Vector(0.0, 0.0, 0.0), normalizedVec)

        if Vector_1to3_projectToPlane.Length == 0.0:
            Tools3D.sayz("起点坐标有误，请重新输入!")
            return
        elif Vector_1to4_projectToPlane.Length == 0.0:
            Tools3D.sayz("终点坐标有误，请重新输入!")
            return
        else:
            # 确定Vector_1to3_projectToPlane与弧段的交点位置，即弧段的内外起始位置
            # k_start为比例因子，确定起始位置内外半径长度与投影向量长的比值
            innerRadius = max(radius1, 0.00003)
            outerRadius = max(radius2, 0.00003)

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
                    if radius1 == 0:
                        e1 = Part.makeCircle(0.00002, point1, normalizedVec)
                    else:
                        e1 = Part.makeCircle(radius1, point1, normalizedVec)
                    e2 = Part.makeCircle(radius2, point1, normalizedVec)
                    wires = [e1, e2]
                    line = Part.makeLine(point1, point2)
                    path = Part.Wire(line)
                    shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
                    return path.makePipe(shapeCircle)
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
                    return h_path.makePipe(face)

            except:
                Tools3D.sayz("Redraw Annular_Section Failed!")
