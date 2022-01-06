# -*- coding: utf8 -*-
import math

import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D
from PySide import QtGui


class VolComformal:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        正投影体
        1.考虑两个点的x,y,z坐标任一方向坐标不能相同
        """
        coordinate = FreeCAD.ActiveDocument.CoordinateSystem
        if coordinate == 'Rectangular':
            length = abs(fp.Point1X.Value - fp.Point2X.Value)
            width = abs(fp.Point1Y.Value - fp.Point2Y.Value)
            height = abs(fp.Point1Z - fp.Point2Z)
            direction = FreeCAD.Vector(0, 0, 1)
            start_point = FreeCAD.Vector(min(fp.Point1X.Value, fp.Point2X.Value),
                                         min(fp.Point1Y.Value, fp.Point2Y.Value),
                                         min(fp.Point1Z.Value, fp.Point2Z.Value))
            try:
                fp.Shape = Part.makeBox(length, width, height, start_point, direction)
            except:
                Tools3D.sayz(u"point1和point2的X,Y,Z方向坐标不能相同。")
                Tools3D.sayz("Redraw Conformal Failed!")

        else:
            if fp.Point1X.Value != fp.Point2X.Value and fp.Point1Y.Value != fp.Point2Y.Value and fp.Point1Z.Value != fp.Point2Z.Value:
                # 数据处理
                if coordinate == "Polar":
                    if fp.Point1X.Value < 0 or fp.Point2X < 0:
                        Tools3D.sayz(u"R不能为负")
                        Tools3D.sayz("Redraw Conformal Failed!")
                        return
                    else:
                        height = abs(fp.Point1Z.Value - fp.Point2Z.Value)
                        h_bottom = min(fp.Point1Z.Value, fp.Point2Z.Value)
                        h_top = max(fp.Point1Z.Value, fp.Point2Z.Value)
                        minRadius = min(fp.Point1X.Value, fp.Point2X.Value)
                        maxRadius = max(fp.Point1X.Value, fp.Point2X.Value)
                        angle_start = fp.Point1Y.Value % 360.0
                        angle_end = fp.Point2Y.Value % 360.0
                        # 始末位置的角度，采用弧度制
                        theta_start = (fp.Point1Y.Value % 360.0) * math.pi / 180.0
                        theta_end = (fp.Point2Y.Value % 360.0) * math.pi / 180.0
                else:
                    if fp.Point1Y.Value < 0 or fp.Point2Y < 0:
                        Tools3D.sayz(u"R不能为负")
                        Tools3D.sayz("Redraw Conformal Failed!")
                        return
                    else:
                        height = abs(fp.Point1X.Value - fp.Point2X.Value)
                        h_bottom = min(fp.Point1X.Value, fp.Point2X.Value)
                        h_top = max(fp.Point1X.Value, fp.Point2X.Value)
                        minRadius = min(fp.Point1Y.Value, fp.Point2Y.Value)
                        maxRadius = max(fp.Point1Y.Value, fp.Point2Y.Value)
                        angle_start = fp.Point1Z.Value % 360.0
                        angle_end = fp.Point2Z.Value % 360.0
                        theta_start = (fp.Point1Z.Value % 360.0) * math.pi / 180.0
                        theta_end = (fp.Point2Z.Value % 360.0) * math.pi / 180.0

                normalVec = FreeCAD.Vector(0, 0, height)
                o_bottom = FreeCAD.Vector(0, 0, h_bottom)
                o_top = FreeCAD.Vector(0, 0, h_top)
                angle = math.fabs(theta_end - theta_start)

                # 建模(采用环形区域体Annular_Section建模方法)
                if angle == 0:
                    # 夹角为0，则说明投影出的是一个完整的环形体
                    if minRadius == 0:
                        minRadius = 0.00002
                    e1 = Part.makeCircle(minRadius, o_bottom, normalVec)
                    e2 = Part.makeCircle(maxRadius, o_bottom, normalVec)
                    wires = [e1, e2]
                    line = Part.makeLine(o_bottom, o_top)
                    path = Part.Wire(line)
                    shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
                    fp.Shape = path.makePipe(shapeCircle)
                    return
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

                    # new_建弧path
                    # arc = Part.makeCircle(maxRadius, o_bottom, normalVec, angle_start, angle_end)
                    # # arcShape = arc.toShape()
                    # path = Part.Wire(arc)

                    # new_建模
                    # 生成底面上环形扇面
                    R = Part.makeLine(point_inner_start, point_outer_start)
                    face = path.makePipe(R)

                    # 底面沿高扫掠，生成环形区域体
                    RCenter = (point_inner_start + point_outer_start) / 2.0
                    h = Part.makeLine(RCenter, RCenter + normalVec)
                    h_path = Part.Wire(h)
                    fp.Shape = h_path.makePipe(face)


                    # 老3D建模方法
                    # tempP1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
                    # tempP2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
                    # tempP3 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point1Y.Value, fp.Point2Z.Value)
                    # tempP4 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point2Z.Value)
                    #
                    # if tempP1 == tempP4:
                    #     # tempP4=tempP4.add(FreeCAD.Vector(0,0,0.01))
                    #     fp.Shape = getArcObj(fp.Point1, fp.Point2)
                    #
                    # line2 = Part.makeLine(tempP1, tempP4)
                    # shapeCir = getArcObj(FreeCAD.Vector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point2Z.Value),
                    #                      FreeCAD.Vector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value))
                    # path = Part.Wire(line2)
                    # fp.Shape = path.makePipe(shapeCir)


                    # 在起始位置处创建轮廓矩形rectangle，并生成矩形面rectangleFace
                    # point_inner_start = FreeCAD.Vector(minRadius * math.cos(theta_start),
                    #                                    minRadius * math.sin(theta_start), h_bottom)
                    #
                    # rectangle = Part.makePolygon([point_inner_start,
                    #                               point_outer_start,
                    #                               point_outer_start.add(normalVec),
                    #                               point_inner_start.add(normalVec),
                    #                               point_inner_start])
                    # # 矩形面沿路径弧扫掠，生成一个环形区域体
                    # rectangleFace = Part.makeFace([Part.Wire(rectangle)], "Part::FaceMakerBullseye")
                    # fp.Shape = path.makePipe(rectangleFace)
                    return

            else:
                Tools3D.sayz(u"point1和point2的任一坐标均不能相同。")
                Tools3D.sayz("Redraw Conformal Failed!")


class GetProperty:
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolConformal_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Conformal)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Conformal", "正投影体")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Conformal
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0.01
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0.01
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y").Point2Y = 360
            obj.addProperty("App::PropertyDistance", "Point2Z").Point2Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z").Point2Z = 360
        Tools3D.addHelperProperty(obj, 2)
        Tools3D.getHelperValue(obj)
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)


def getObject():
    """
    返回获取的obj
    """
    volComformalObj = GetProperty()
    VolComformal(volComformalObj.obj)
    Tools3D.ViewProvider(volComformalObj.obj.ViewObject)
    return volComformalObj.obj


# 极坐标系下两个点得到扇形
def getArcObj(polarPoint1, polarPoint2):
    tempP1 = Tools3D.pointToRecVec(polarPoint1)
    tempP2 = Tools3D.pointToRecVec(FreeCAD.Vector(polarPoint2.x, polarPoint1.y, polarPoint2.z))

    startAngle = polarPoint1.y
    endAngle = polarPoint2.y
    dir = FreeCAD.Vector(0, 0, 2)
    # 这样设置可以生成面片
    if startAngle == endAngle:
        endAngle = startAngle + 0.01
    if tempP1 == tempP2:
        # 排除polarPoint.x为0
        if not polarPoint2 == 0.0:
            resultShape = Part.makeCircle(math.fabs(polarPoint2.x), FreeCAD.Vector(0, 0, tempP1.z), dir, startAngle,
                                          endAngle)
        else:
            resultShape = Part.makeSphere(0.0001, tempP1)
    else:
        if math.fabs(startAngle - endAngle) == 360:
            wires = []
            if not polarPoint1.x == 0.0:
                arcLine1 = Part.makeCircle(math.fabs(polarPoint1.x), FreeCAD.Vector(0, 0, tempP1.z), dir, polarPoint1.y,
                                           polarPoint2.y)
                wires.append(arcLine1)
            if not polarPoint2.x == 0.0:
                arcLine2 = Part.makeCircle(math.fabs(polarPoint2.x), FreeCAD.Vector(0, 0, tempP2.z), dir, polarPoint1.y,
                                           polarPoint2.y)
                wires.append(arcLine2)
            shapeCircle = Part.makeFace(wires, "Part::FaceMakerBullseye")
            resultShape = shapeCircle
        else:
            line = Part.makeLine(tempP1, tempP2)
            linePath = Part.makeCircle(math.fabs((polarPoint1.x + polarPoint2.x) / 2), FreeCAD.Vector(0, 0, tempP1.z),
                                       dir, startAngle, endAngle)
            path = Part.Wire(linePath)
            resultShape = path.makePipe(line)
    return resultShape
