# -*- coding: utf8 -*-
import math

import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class VolHelical:
    def __init__(self, obj):
        obj.Proxy = self
        # self.flagPlacement = True
        # self.placementBefore = obj.Placement

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
        建模过程：
        1.找到起始点StartPoint在底面，即基准点BasePoint所在，以top-base为法向的平面上的投影，确定起始位置
        2.求出螺旋体将要旋转的角度
        3.建立螺旋线，建立螺旋体起始位置的矩形
        4.矩形面沿螺旋线扫掠生成螺旋体，旋转后得到以StartPoint投影为起始位置的螺旋体

        错误情况分析：
        1.方向：点12重合，环形区域体高度为0且方向不能确定
        2.半径：外半径为0或负，内半径为负，或者内半径大于外半径
        3.螺距为0或负，或者螺旋体线条沿轴向的宽为负
            边界情况分析：
            1.内半径等于外半径 ——> 由一条线段沿螺旋线扫掠而成，建模出的图形为一圈螺旋面 ——> 不属于三维立体范畴
            2.内半径等于0 ——> 以外径为长，width为宽的矩形沿螺旋线扫掠而成，形成螺旋体
            3.螺旋线轴宽等于0 ——> 螺旋体线条沿轴向的宽为0，建模出的图形为一圈螺旋面 ——> 不属于三维立体范畴

        """

        pointBase = Tools3D.transToRecVector(fp.PointBaseX.Value, fp.PointBaseY.Value, fp.PointBaseZ.Value)
        pointTop = Tools3D.transToRecVector(fp.PointTopX.Value, fp.PointTopY.Value, fp.PointTopZ.Value)
        pointStart = Tools3D.transToRecVector(fp.PointStartX.Value, fp.PointStartY.Value, fp.PointStartZ.Value)

        normalVec = pointTop.sub(pointBase)

        if normalVec.Length == 0:
            Tools3D.sayz("坐标有误，请重新输入!")
            return
        elif fp.RadiusInside.Value < 0.0 or fp.RadiusOut.Value <= 0.0 or fp.RadiusInside.Value >= fp.RadiusOut.Value:
            Tools3D.sayz("半径有误，请重新输入")
            return
        elif fp.Pitch.Value <= 0.0:
            Tools3D.sayz("螺距有误，请重新输入")
            return
        elif fp.Width.Value <= 0.0:
            Tools3D.sayz("螺旋线轴宽有误，请重新输入")
            return
        else:
            try:
                # 这里需要对pointStart进行处理，因为需要将这个点定位到过base点，法向为top-base的平面上，向该平面投影
                pointStartToPlane = pointStart.projectToPlane(pointBase, normalVec)
                # 再将这个点移至距base点RadiusInside与RadiusOut中点距离处,这里取中点防止两个点都为0
                if pointStartToPlane == pointBase:
                    startPointFormCenter = pointBase
                else:
                    k = ((fp.RadiusInside.Value + fp.RadiusOut.Value) / 2) / pointStartToPlane.distanceToPoint(pointBase)
                    normal_pointStartToPlane_pointBase = pointStartToPlane.sub(pointBase)
                    startPointFormCenter = k * normal_pointStartToPlane_pointBase.add(pointBase)

                # 旋转三个点，使得base和top与Z轴重合
                rot = getQuatAfterRotation(pointTop)
                zTop = rot.multVec(pointTop)
                zStart = rot.multVec(startPointFormCenter)
                # 将z映射到XOY面上
                if not zStart.z == 0:
                    zStart = FreeCAD.Vector(zStart.x, zStart.y, 0)
                # 此时的zStart与x轴正向的角度
                angle = getAngleWithXByVector(zStart)

                # 构建螺旋线，创建路径
                height = pointBase.distanceToPoint(pointTop)
                helixLine = Part.makeHelix(fp.Pitch.Value, height, (fp.RadiusInside.Value + fp.RadiusOut.Value) / 2)
                path = Part.Wire(helixLine)

                # 为了能得到目标螺旋体，需要求出起点位置的矩形，让矩形沿着螺旋线扫掠，得出
                rectPoint1 = FreeCAD.Vector(fp.RadiusInside.Value, 0, -fp.Width / 2)
                rectPoint2 = FreeCAD.Vector(fp.RadiusOut.Value, 0, -fp.Width / 2)
                rectPoint3 = FreeCAD.Vector(fp.RadiusOut.Value, 0, fp.Width / 2)
                rectPoint4 = FreeCAD.Vector(fp.RadiusInside.Value, 0, fp.Width / 2)

                recWire = Part.makePolygon([rectPoint1, rectPoint2, rectPoint3, rectPoint4, rectPoint1])
                # recFace = Part.makeFace(recWire, "Part::FaceMakerBullseye")

                # 矩形沿路径扫掠管道，创建螺旋体
                fp.Shape = path.makePipeShell([recWire], True, True)

                # 旋转，使得螺旋体以StartPoint为起始点
                rot1 = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle)
                rot2 = rot.inverted()
                rot = rot2.multiply(rot1)
                fp.Placement.Rotation = rot
                fp.Placement.move(pointBase)

                # if self.flagPlacement:
                #     self.flagPlacement = False
                #     tempPlacementBefore = self.placementBefore
                #
                #     # 矩形沿路径扫掠管道，创建螺旋体
                #     fp.Shape = path.makePipeShell([recWire], True, True)
                #
                #     # 旋转，使得螺旋体以StartPoint为起始点
                #     rot1 = FreeCAD.Rotation(FreeCAD.Vector(0, 0, 1), angle)
                #     rot2 = rot.inverted()
                #     rot = rot2.multiply(rot1)
                #     fp.Placement.Rotation = rot
                #     fp.Placement.move(pointBase)
                #     self.placementBefore = tempPlacementBefore
                #     self.flagPlacement = True

                return
            except:
                Tools3D.sayz("Redraw Helical Failed!")


# 某个向量映射到XOY面与x轴正方向之间的夹角 0-pi
def getAngleWithXByVector(vec):
    vecXDir = FreeCAD.Vector(1, 0, 0)
    #先将vec映射到XOY面上
    vecXOY = FreeCAD.Vector(vec.x, vec.y, 0)
    if vecXOY.Length == 0.0:
        return 0.0
    else:
        angle = math.acos((vecXDir.dot(vecXOY))/(vecXDir.Length*vecXOY.Length))*180/math.pi
        if vecXOY.y<0:
            angle = 360-angle
        return angle


# 某个向量与z轴正方向之间的夹角 0-pi
def getAngleWithZByVector(vec):
    vecZDir = FreeCAD.Vector(0, 0, 1)
    angle = math.acos(vec.dot(vecZDir)/vec.Length*vecZDir.Length)*180/math.pi
    if vec.y < 0:
        angle = 360-angle
    return angle


# 将某个向量旋转到Z轴方向上后的四元数
def getQuatAfterRotation(vec):
    dirVec = FreeCAD.Vector(0, 0, 1)
    # 判断vec是否已在Z轴上
    if vec.x == 0 and vec.y == 0:
        return FreeCAD.Rotation(0, 0, 0, 1)
    else:
        # 先通过叉乘求得旋转轴
        axis = vec.cross(dirVec)
        axis.normalize()
        # 求出旋转角度
        angle = getAngleWithZByVector(vec)
        # 得出四元数
        rot = FreeCAD.Rotation(axis, angle)
        return rot

class Helical:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('CreateVolHelical_3D')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", ObjectTools.ObjectType.Vol_Helical)
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Helical", "螺旋体")
        FreeCAD.ActiveDocument.commitTransaction()

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Vol_Helical
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "PointBaseX").PointBaseX = 0
            obj.addProperty("App::PropertyDistance", "PointBaseY").PointBaseY = 0
            obj.addProperty("App::PropertyDistance", "PointBaseZ").PointBaseZ = 0
            obj.addProperty("App::PropertyDistance", "PointTopX").PointTopX = 0
            obj.addProperty("App::PropertyDistance", "PointTopY").PointTopY = 0
            obj.addProperty("App::PropertyDistance", "PointTopZ").PointTopZ = 0.05
            obj.addProperty("App::PropertyDistance", "PointStartX").PointStartX = 0.01
            obj.addProperty("App::PropertyDistance", "PointStartY").PointStartY = 0
            obj.addProperty("App::PropertyDistance", "PointStartZ").PointStartZ = 0
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "PointBaseX").PointBaseX = 0
            obj.addProperty("App::PropertyAngle", "PointBaseY").PointBaseY = 0
            obj.addProperty("App::PropertyDistance", "PointBaseZ").PointBaseZ = 0
            obj.addProperty("App::PropertyDistance", "PointTopX").PointTopX = 0
            obj.addProperty("App::PropertyAngle", "PointTopY").PointTopY = 0
            obj.addProperty("App::PropertyDistance", "PointTopZ").PointTopZ = 0
            obj.addProperty("App::PropertyDistance", "PointStartX").PointStartX = 0
            obj.addProperty("App::PropertyAngle", "PointStartY").PointStartY = 0
            obj.addProperty("App::PropertyDistance", "PointStartZ").PointStartZ = 0
        else:
            obj.addProperty("App::PropertyDistance", "PointBaseX").PointBaseX = 0
            obj.addProperty("App::PropertyDistance", "PointBaseY").PointBaseY = 0
            obj.addProperty("App::PropertyAngle", "PointBaseZ").PointBaseZ = 0
            obj.addProperty("App::PropertyDistance", "PointTopX").PointTopX = 0
            obj.addProperty("App::PropertyDistance", "PointTopY").PointTopY = 0
            obj.addProperty("App::PropertyAngle", "PointTopZ").PointTopZ = 0
            obj.addProperty("App::PropertyDistance", "PointStartX").PointStartX = 0
            obj.addProperty("App::PropertyDistance", "PointStartY").PointStartY = 0
            obj.addProperty("App::PropertyAngle", "PointStartZ").PointStartZ = 0

        obj.addProperty("App::PropertyDistance", "RadiusInside").RadiusInside = 0.005
        obj.addProperty("App::PropertyDistance", "RadiusOut").RadiusOut = 0.01
        obj.addProperty("App::PropertyDistance", "Pitch").Pitch = 0.005
        obj.addProperty("App::PropertyDistance", "Width").Width = 0.001
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHeHelperProperty(obj)
        Tools3D.getHeHelperValue(obj)

def getObject():
    """
    返回获取的obj
    """
    helical = Helical()
    VolHelical(helical.obj)
    Tools3D.ViewProvider(helical.obj.ViewObject)
    return helical.obj
