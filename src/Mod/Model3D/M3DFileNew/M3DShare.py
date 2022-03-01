# encoding: utf-8
# 此文件为M3D的公共函数
import FreeCAD
from Model3D.Tools import Tools3D

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","


def getCoodinatePara():
    # 获取与坐标系相关的函数参数
    functionParameters = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular' or coodinate == 'Rectangular':
        functionParameters = "(T,X,Y,Z) = "
    elif coodinate == u'Polar' or coodinate == 'Polar':
        functionParameters = u"(T,R,P,Z) = "
    elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
        functionParameters = u"(T,Z,R,P) = "
    else:
        Tools3D.sayz("请选择正确的坐标系")
    return functionParameters


def getCoodinateParaWithPort():
    # 获取与坐标系相关的函数参数
    functionParameters = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular' or coodinate == 'Rectangular':
        functionParameters = "(X,Y,Z) = "
    elif coodinate == u'Polar' or coodinate == 'Polar':
        functionParameters = u"(R,P,Z) = "
    elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
        functionParameters = u"(Z,R,P) = "
    else:
        Tools3D.sayz("请选择正确的坐标系")
    return functionParameters



def getTimerM3D(obj):
    # 获取物理设置中定时器设置的m3d
    if obj.timer == "默认定时器":
        Timer_name = "DefTimer"
    elif obj.timer == "仅开始时刻":
        Timer_name = "TSYS$FIRST"
    elif obj.timer == "仅结束时刻":
        Timer_name = "TSYS$LAST"
    else:
        Timer_name = obj.timer
    return Timer_name


class PointCoordinates:
    # 把每个点的坐标抽象出来,此处为物理设置的点坐标抽象
    def point1(self, obj):
        temp_m3d = ""
        temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + obj.point1_Z
        return temp_m3d

    def point2(self, obj):
        temp_m3d = ""
        temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + obj.point2_Z
        return temp_m3d


def Mark(obj):
    temp_m3d = ""
    if obj.isMarkX:
        temp_m3d += "MARK"+blankSpace+obj.Label+blankSpace+"X1"
        temp_m3d += blankSpace+"SIZE"+blankSpace+obj.MarkX+semicolon+newLine
    if obj.isMarkY:
        temp_m3d += "MARK"+blankSpace+obj.Label+blankSpace+"X2"
        temp_m3d += blankSpace+"SIZE"+blankSpace+obj.MarkY+semicolon+newLine
    if obj.isMarkZ:
        temp_m3d += "MARK" + blankSpace + obj.Label + blankSpace + "X3"
        temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkZ + semicolon + newLine
    return temp_m3d