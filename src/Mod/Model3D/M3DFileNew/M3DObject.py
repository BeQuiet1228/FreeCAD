# encoding:utf-8
# 此文件存放点、线、面、体的m3d
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Tools.ObjectTools import Attribute
import re

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","

# 坐标字典
coordinateDict = {"Rectangular": ["X", "Y", "Z"],
                  "Polar": ["R", "Theta", "Z"],
                  "Cylindrical": ["Z", "R", "Theta"]}


def Point(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    temp_m3d += "POINT" + blankSpace + obj.Label + blankSpace + point1_x_value + blankSpace + point1_y_value \
                + blankSpace + point1_z_value + semicolon + newLine
    return temp_m3d, temp_m3d_pap


# 点线面的坐标与物理设置有表达式引擎不同，单独抽象出来
def CoordinatesToObject(obj):
    temp_m3d = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    point2_z_value = str(obj.user_point2_z).replace(' ', '')
    temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
    temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point2_z_value
    if hasattr(obj, "Point3X"):
        point3_x_value = str(obj.user_point3_x).replace(' ', '')
        point3_y_value = str(obj.user_point3_y).replace(' ', '')
        point3_z_value = str(obj.user_point3_z).replace(' ', '')
        temp_m3d += newLine + tab + point3_x_value + comma + point3_y_value + comma + point3_z_value
    if hasattr(obj, "Point4X"):
        point4_x_value = str(obj.user_point4_x).replace(' ', '')
        point4_y_value = str(obj.user_point4_y).replace(' ', '')
        point4_z_value = str(obj.user_point4_z).replace(' ', '')
        temp_m3d += newLine + tab + point4_x_value + comma + point4_y_value + comma + point4_z_value
    if hasattr(obj, "Point5X"):
        point5_x_value = str(obj.user_point5_x).replace(' ', '')
        point5_y_value = str(obj.user_point5_y).replace(' ', '')
        point5_z_value = str(obj.user_point5_z).replace(' ', '')
        temp_m3d += newLine + tab + point5_x_value + comma + point5_y_value + comma + point5_z_value
    if hasattr(obj, "Point6X"):
        point6_x_value = str(obj.user_point6_x).replace(' ', '')
        point6_y_value = str(obj.user_point6_y).replace(' ', '')
        point6_z_value = str(obj.user_point6_z).replace(' ', '')
        temp_m3d += newLine + tab + point6_x_value + comma + point6_y_value + comma + point6_z_value
    if hasattr(obj, "Point7X"):
        point7_x_value = str(obj.user_point7_x).replace(' ', '')
        point7_y_value = str(obj.user_point7_y).replace(' ', '')
        point7_z_value = str(obj.user_point7_z).replace(' ', '')
        temp_m3d += newLine + tab + point7_x_value + comma + point7_y_value + comma + point7_z_value
    if hasattr(obj, "Point8X"):
        point8_x_value = str(obj.user_point8_x).replace(' ', '')
        point8_y_value = str(obj.user_point8_y).replace(' ', '')
        point8_z_value = str(obj.user_point8_z).replace(' ', '')
        temp_m3d += newLine + tab + point8_x_value + comma + point8_y_value + comma + point8_z_value
    return temp_m3d


# 通用属性抽象出来，单独处理
def ShareAttribute(obj):
    temp_m3d_pap = ""
    if obj.Attribute == Attribute.NotDefine:
        pass
    elif obj.Attribute == Attribute.Conductor:
        temp_m3d_pap += "CONDUCTOR" + blankSpace + obj.Label + semicolon + newLine
    elif obj.Attribute == Attribute.Custom:
        if obj.C_SIGMA == "Isotropy":
            temp_m3d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA1 + semicolon + newLine
        elif obj.C_SIGMA == "Anisotropy":
            temp_m3d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA1 + \
                            blankSpace + "X1" + semicolon + newLine
            temp_m3d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA2 + \
                            blankSpace + "X2" + semicolon + newLine
            temp_m3d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA3 + \
                            blankSpace + "X3" + semicolon + newLine
        if obj.RDC == "Isotropy":
            temp_m3d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS1 + semicolon + newLine
        elif obj.RDC == "Anisotropy":
            temp_m3d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS1 + \
                            blankSpace + "X1" + semicolon + newLine
            temp_m3d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS2 + \
                            blankSpace + "X2" + semicolon + newLine
            temp_m3d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS3 + \
                            blankSpace + "X3" + semicolon + newLine
    elif obj.Attribute == Attribute.Void or obj.Attribute == Attribute.Vacuo:
        temp_m3d_pap += "VOID" + blankSpace + obj.Label + semicolon + newLine
    else:
        temp_m3d_pap += "无法识别的属性类型"
    return temp_m3d_pap


def Mark(obj):
    temp_m3d = ""
    if obj.isMarkX:
        temp_m3d += "MARK" + blankSpace + obj.Label + blankSpace + "X1"
        if obj.isCheckMinX:
            temp_m3d += blankSpace + "MINIMUN"
        if obj.isCheckMidX:
            temp_m3d += blankSpace + "MIDPOINT"
        if obj.isCheckMaxX:
            temp_m3d += blankSpace + "MAXIMUM"
        temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkX + semicolon + newLine
    if obj.isMarkY:
        temp_m3d += "MARK" + blankSpace + obj.Label + blankSpace + "X2"
        if obj.isCheckMinY:
            temp_m3d += blankSpace + "MINIMUN"
        if obj.isCheckMidY:
            temp_m3d += blankSpace + "MIDPOINT"
        if obj.isCheckMaxY:
            temp_m3d += blankSpace + "MAXIMUM"
        temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkY + semicolon + newLine
    if obj.isMarkZ:
        temp_m3d += "MARK" + blankSpace + obj.Label + blankSpace + "X3"
        if obj.isCheckMinZ:
            temp_m3d += blankSpace + "MINIMUN"
        if obj.isCheckMidZ:
            temp_m3d += blankSpace + "MIDPOINT"
        if obj.isCheckMaxZ:
            temp_m3d += blankSpace + "MAXIMUM"
        temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkZ + semicolon + newLine
    return temp_m3d


def Line(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "LINE" + blankSpace + obj.Label + blankSpace + "OBLIQUE"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    return temp_m3d, temp_m3d_pap


def LineConformal(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    # 判断起点
    # 终点的坐标
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    point2_z_value = str(obj.user_point2_z).replace(' ', '')

    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular':
        if obj.Normal == "X" or obj.Normal == "x":
            temp = obj.Point1X - obj.Point2X
        elif obj.Normal == "Y" or obj.Normal == "y":
            temp = obj.Point1Y - obj.Point2Y
        else:
            temp = obj.Point1Z - obj.Point2Z
    elif coodinate == u"Polar":
        if obj.Normal == "R" or obj.Normal == "r":
            temp = obj.Point1X - obj.Point2X
        elif obj.Normal == "Theta":
            temp = obj.Point1Y - obj.Point2Y
        else:
            temp = obj.Point1Z - obj.Point2Z
    else:
        if obj.Normal == "Z" or obj.Normal == "z":
            temp = obj.Point1X - obj.Point2X
        elif obj.Normal == "R" or obj.Normal == "r":
            temp = obj.Point1Y - obj.Point2Y
        else:
            temp = obj.Point1Z - obj.Point2Z

    if float(temp) >= 0:
        temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point2_z_value
        temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
    else:
        temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
        temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point2_z_value
    temp_m3d += semicolon + newLine
    return temp_m3d, temp_m3d_pap


def AreaComformal(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    point2_z_value = str(obj.user_point2_z).replace(' ', '')

    temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    # 判断起点和终点
    temp1 = obj.Point1X.Value - obj.Point2X.Value
    temp2 = obj.Point1Y.Value - obj.Point2Y.Value
    temp3 = obj.Point1Z.Value - obj.Point2Z.Value

    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if (coodinate == u'Rectangular' and obj.Normal == "X") or (coodinate == u"Polar" and obj.Normal == "R") or \
            (coodinate == u"Cylindrical" and obj.Normal == "Z"):
        if float(temp2) < 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp2) > 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp2) < 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp2) > 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        else:
            Tools3D.sayz(u"请输入正确的坐标值")

    elif (coodinate == u'Rectangular' and obj.Normal == "Y") or \
            (coodinate == u"Polar" and (obj.Normal == "Theta" or obj.Normal == u"θ")) or (
            coodinate == u"Cylindrical" and obj.Normal == "R"):
        if float(temp1) < 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp1) < 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        else:
            Tools3D.sayz(u"请输入正确的坐标值")

    elif (coodinate == u'Rectangular' and obj.Normal == "Z") or \
            (coodinate == u"Polar" and obj.Normal == "Z") or \
            (coodinate == u"Cylindrical" and obj.Normal == "Theta"):
        if float(temp1) < 0 and float(temp2) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp2) < 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) < 0 and float(temp2) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp2) > 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        else:
            Tools3D.sayz(u"请输入正确的坐标值")

    else:
        Tools3D.sayz("选取法向错误")
    return temp_m3d, temp_m3d_pap


def Rectangle(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    point2_z_value = str(obj.user_point2_z).replace(' ', '')

    temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "RECTANGULAR"
    # 判断起点和终点
    temp1 = obj.Point1X.Value - obj.Point2X.Value
    temp2 = obj.Point1Y.Value - obj.Point2Y.Value
    temp3 = obj.Point1Z.Value - obj.Point2Z.Value

    coodinate = FreeCAD.ActiveDocument.CoordinateSystem

    if (coodinate == u'Rectangular' and obj.Normal == "X") or (coodinate == u"Polar" and obj.Normal == "R") or \
            (coodinate == u"Cylindrical" and obj.Normal == "Z"):
        if float(temp2) < 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp2) > 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp2) < 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp2) > 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        else:
            Tools3D.sayz(u"请输入正确的坐标值")


    elif (coodinate == u'Rectangular' and obj.Normal == "Y") or \
 \
            (coodinate == u"Polar" and (obj.Normal == "Theta" or obj.Normal == u"θ")) or (

            coodinate == u"Cylindrical" and obj.Normal == "R"):
        if float(temp1) < 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp3) < 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
        elif float(temp1) < 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp3) > 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point2_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        else:
            Tools3D.sayz(u"请输入正确的坐标值")


    elif (coodinate == u'Rectangular' and obj.Normal == "Z") or \
 \
            (coodinate == u"Polar" and obj.Normal == "Z") or \
 \
            (coodinate == u"Cylindrical" and obj.Normal == "Theta"):
        if float(temp1) < 0 and float(temp2) < 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp2) < 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) < 0 and float(temp2) > 0:
            temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        elif float(temp1) > 0 and float(temp2) > 0:
            temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point1_z_value
            temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
        else:
            Tools3D.sayz(u"请输入正确的坐标值")
    return temp_m3d, temp_m3d_pap


def AreaPolygonal(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    length = obj.NumbersOfPoints
    temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "POLYGONAL" + newLine + tab
    for index in range(length):
        temp_m3d += str(getattr(obj, "user_point" + str(index + 1) + "_x")).replace(' ', '') \
                    + comma \
                    + str(getattr(obj, "user_point" + str(index + 1) + "_y")).replace(' ', '') + comma \
                    + str(getattr(obj, "user_point" + str(index + 1) + "_z")).replace(' ', '')
        temp_m3d += newLine + tab
    temp_m3d += getattr(obj, "user_point1_x").replace(' ', '') + comma + getattr(obj, "user_point1_y").replace(' ', '') \
                + comma + getattr(obj, "user_point1_z").replace(' ', '') + semicolon + newLine
    return temp_m3d, temp_m3d_pap


def AreaFunction(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    Precison_value = str(obj.Precision).replace(' ', '')
    temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "FUNCTION"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += newLine + tab + obj.Expression
    temp_m3d += newLine + tab + Precison_value
    temp_m3d += semicolon + newLine
    return temp_m3d, temp_m3d_pap


def VolConformal(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolAnnular(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    point1_radius_value = str(obj.user_radius1).replace(' ', '')
    point2_radius_value = str(obj.user_radius2).replace(' ', '')
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "ANNULAR"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += newLine + tab + point1_radius_value + comma + point2_radius_value
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolCylinder(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    point1_radius_value = str(obj.user_radius1).replace(' ', '')
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "CYLINDRICAL"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += newLine + tab + point1_radius_value
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolSpecialCone(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    radius_value1 = str(obj.user_radius1).replace(' ', '')
    radius_value2 = str(obj.user_radius2).replace(' ', '')
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "CONE"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += newLine + tab + radius_value1 + comma + radius_value2
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolSpherical(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    radius_value = str(obj.user_radius1).replace(' ', '')
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "SPHERICAL"
    temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
    temp_m3d += newLine + tab + radius_value
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolToroidal_Section(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    radius_value1 = str(obj.user_radius1).replace(' ', '')
    radius_value2 = str(obj.user_radius2).replace(' ', '')
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "TOROIDAL_SECTION"
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    point2_z_value = str(obj.user_point2_z).replace(' ', '')
    temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
    temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point2_z_value
    temp_m3d += newLine + tab + radius_value2 + comma + radius_value1
    if hasattr(obj, "Point3X"):
        point3_x_value = str(obj.user_point3_x).replace(' ', '')
        point3_y_value = str(obj.user_point3_y).replace(' ', '')
        point3_z_value = str(obj.user_point3_z).replace(' ', '')
        temp_m3d += newLine + tab + point3_x_value + comma + point3_y_value + comma + point3_z_value
    if hasattr(obj, "Point4X"):
        point4_x_value = str(obj.user_point4_x).replace(' ', '')
        point4_y_value = str(obj.user_point4_y).replace(' ', '')
        point4_z_value = str(obj.user_point4_z).replace(' ', '')
        temp_m3d += newLine + tab + point4_x_value + comma + point4_y_value + comma + point4_z_value
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolAnnular_Section(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    radius_value1 = str(obj.user_radius1).replace(' ', '')
    radius_value2 = str(obj.user_radius2).replace(' ', '')
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "ANNULAR_SECTION"

    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point1_z_value = str(obj.user_point1_z).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    point2_z_value = str(obj.user_point2_z).replace(' ', '')
    point3_x_value = str(obj.user_point3_x).replace(' ', '')
    point3_y_value = str(obj.user_point3_y).replace(' ', '')
    point3_z_value = str(obj.user_point3_z).replace(' ', '')
    point4_x_value = str(obj.user_point4_x).replace(' ', '')
    point4_y_value = str(obj.user_point4_y).replace(' ', '')
    point4_z_value = str(obj.user_point4_z).replace(' ', '')

    temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
    temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point2_z_value
    temp_m3d += newLine + tab + radius_value1 + comma + radius_value2
    temp_m3d += newLine + tab + point3_x_value + comma + point3_y_value + comma + point3_z_value
    temp_m3d += newLine + tab + point4_x_value + comma + point4_y_value + comma + point4_z_value

    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolFunction(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == "Rectangular":
        functionParameters = ".F(X,Y,Z) = "
    elif coodinate == "Polar":
        functionParameters = ".F(R,THETA,Z) = "
    else:
        functionParameters = ".F(Z,R,THETA) = "
    temp_m3d += "FUNCTION" + blankSpace + obj.Label + functionParameters + obj.Expression + semicolon + newLine
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "FUNCTIONAL" + blankSpace + obj.Label+".F"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolParallelepipedal(obj):
    temp_m3d = ""
    temp_m3d_pap = ""

    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "PARALLELEPIPEDAL"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolPyramid(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "ANNULAR"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolWedge(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "WEDGE"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolRhombus(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "RHOMBUS"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolExtruded(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "EXTRUDED"
    temp_m3d += newLine + tab + obj.Line
    temp_m3d += newLine + tab + obj.Area
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolTetrahedron(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "TETRAHEDRON"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolHelical(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    radius_value1 = str(obj.user_radius1).replace(' ', '')
    radius_value2 = str(obj.user_radius2).replace(' ', '')
    pitch_value = str(obj.user_pitch).replace(' ', '')
    width_value = str(obj.user_width).replace(' ', '')
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "HELICAL"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += newLine + tab + radius_value1 + comma + radius_value2 + comma + pitch_value + comma + width_value
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolRevolution(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "ROTATE"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += newLine + tab + obj.Area
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolArray(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    baseObj = ObjectTools.getObjByLabel(obj.BaseType)

    originLabel = baseObj.Label
    newLabel = "Arr_" + originLabel + "'i'"

    temp_m3d += "do" + blankSpace + "i=0" + comma
    # 循环次数
    if obj.ArrayType == "linear":
        temp_m3d += str(obj.linerNumber - 1)
    elif obj.ArrayType == "ortho":
        temp_m3d += str(obj.number1 * obj.number2 - 1)
    else:
        temp_m3d += str(obj.numberPolar - 1)
    temp_m3d += semicolon + newLine
    # 针对字符串太长作出的调整
    temp_m3d += ArrayCoorLenth(obj)

    temp_m3d += "VOLUME" + blankSpace + newLabel + blankSpace
    # Base物体类型
    if obj.BaseObjType == ObjectTools.ObjectType.Vol_Conformal:
        temp_m3d += "CONFORMAL"
    elif obj.BaseObjType == ObjectTools.ObjectType.Vol_Annular:
        temp_m3d += "ANNULAR"
    elif obj.BaseObjType == ObjectTools.ObjectType.Vol_Cylinder:
        temp_m3d += "CYLINDRICAL"
    elif obj.BaseObjType == ObjectTools.ObjectType.Vol_SpecialCone:
        temp_m3d += "CONE"
    elif obj.BaseObjType == ObjectTools.ObjectType.Vol_Spherical:
        temp_m3d += "SPHERICAL"
    elif obj.BaseObjType == ObjectTools.ObjectType.Vol_Annular_Section:
        temp_m3d += "ANNULAR_SECTION"
    else:
        Tools3D.sayz("Error! Object Type is not supported.")
        Tools3D.sayz("Attention: The created M3D is wrong!")

    # 对于环形区域体的阵列，其base物体坐标和半径M3D的显示顺序如下：
    # ... ANNULAR_SECTION point1 point2 radius_inner radius_outer point3 point4 ...
    # 因此，单独设置M3D
    if obj.BaseObjType == ObjectTools.ObjectType.Vol_Annular_Section:
        temp_m3d += BaseCoordRadius_ArrayOfAnnularSection(obj)
    else:
        temp_m3d += BaseCoordinates_Array(obj)
        temp_m3d += BaseRadius_Array(obj)
    temp_m3d += semicolon + newLine

    baseObj.Label = newLabel
    temp_m3d += Mark(baseObj)
    temp_m3d += "ENDDO" + semicolon + newLine

    temp_m3d_pap += "do" + blankSpace + "i=0" + comma
    # 循环次数
    if obj.ArrayType == "linear":
        temp_m3d_pap += str(obj.linerNumber - 1)
    elif obj.ArrayType == "ortho":
        temp_m3d_pap += str(obj.number1 * obj.number2 - 1)
    else:
        temp_m3d_pap += str(obj.numberPolar - 1)
    temp_m3d_pap += semicolon + newLine
    temp_m3d_pap += ShareAttribute(baseObj)
    temp_m3d_pap += "ENDDO" + semicolon + newLine

    baseObj.Label = originLabel
    return temp_m3d, temp_m3d_pap


def ParamArray(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    basedata = ""
    list = obj.BaseObjData
    temp_m3d += "do" + blankSpace + "i=" + str(obj.IFrom) + comma + str(obj.ITo) + semicolon + newLine
    temp_m3d += "VOLUME" + blankSpace + obj.Label + "'i'" + blankSpace
    if obj.BaseObjType == "正投影体":
        temp_m3d += "CONFORMAL" + blankSpace
        basedata = list[0] + comma + list[1] + comma + list[2] + comma + list[3] + comma + list[4] + comma + list[
            5] + semicolon + newLine
    elif obj.BaseObjType == "球形体":
        temp_m3d += "SPHERICAL" + blankSpace
        basedata = list[0] + comma + list[1] + comma + list[2] + comma + list[3] + semicolon + newLine
    elif obj.BaseObjType == "圆柱体":
        temp_m3d += "CYLINDRICAL" + blankSpace
        basedata = list[0] + comma + list[1] + comma + list[2] + comma + list[3] + comma + list[4] + comma + list[5] \
                   + comma + list[6] + semicolon + newLine
    elif obj.BaseObjType == "环形体":
        temp_m3d += "ANNULAR" + blankSpace
        basedata = list[0] + comma + list[1] + comma + list[2] + comma + list[3] + comma + list[4] + comma + list[5] \
                   + comma + list[6] + comma + list[7] + semicolon + newLine
    elif obj.BaseObjType == "圆台体":
        temp_m3d += "CONE" + blankSpace
        basedata = list[0] + comma + list[1] + comma + list[2] + comma + list[3] + comma + list[4] + comma + list[5] \
                   + comma + list[6] + comma + list[7] + semicolon + newLine
    elif obj.BaseObjType == "环形区域体":
        temp_m3d += "ANNULAR_SECTION" + blankSpace
        basedata = list[0] + comma + list[1] + comma + list[2] + comma + list[3] + comma + list[4] + comma + list[5] \
                   + comma + list[6] + comma + list[7] + comma + list[8] + comma + list[9] + comma + list[10] \
                   + comma + list[11] + comma + list[12] + comma + list[13] + semicolon + newLine
    else:
        pass
    temp_m3d += basedata
    if obj.isMarkX:
        temp_m3d += "MARK" + blankSpace + obj.Label + "'i'" + blankSpace + "X1"
        temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkX + semicolon + newLine
    if obj.isMarkY:
        temp_m3d += "MARK" + blankSpace + obj.Label + "'i'" + blankSpace + "X2"
        temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkY + semicolon + newLine
    if obj.isMarkZ:
        temp_m3d += "MARK" + blankSpace + obj.Label + "'i'" + blankSpace + "X3"
        temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkZ + semicolon + newLine
    temp_m3d += "ENDDO" + semicolon + newLine
    temp_m3d_pap += "do" + blankSpace + "i=" + str(obj.IFrom) + comma + str(obj.ITo) + semicolon + newLine
    if obj.Attribute == Attribute.NotDefine:
        pass
    elif obj.Attribute == Attribute.Conductor:
        temp_m3d_pap += "CONDUCTOR" + blankSpace + obj.Label + "'i'" + semicolon + newLine
    elif obj.Attribute == Attribute.Custom:
        temp_m3d_pap += "CONDUCTANCE" + blankSpace + obj.Label + "'i'" + semicolon + newLine
    elif obj.Attribute == Attribute.Void or obj.Attribute == Attribute.Vacuo:
        temp_m3d_pap += "VOID" + blankSpace + obj.Label + "'i'" + semicolon + newLine
    temp_m3d_pap += "ENDDO" + semicolon + newLine
    return temp_m3d, temp_m3d_pap


# 草图拉伸体
def VolDraft_Extrude(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    curCoordinate = FreeCAD.ActiveDocument.CoordinateSystem
    baseAreaObj = ObjectTools.getObjByLabel(obj.Area)
    if hasattr(baseAreaObj, "Normal"):
        point1_x = str(baseAreaObj.user_point1_x).replace(' ', '')
        point1_y = str(baseAreaObj.user_point1_y).replace(' ', '')
        point1_z = str(baseAreaObj.user_point1_z).replace(' ', '')
        point2_x = str(baseAreaObj.user_point2_x).replace(' ', '')
        point2_y = str(baseAreaObj.user_point2_y).replace(' ', '')
        point2_z = str(baseAreaObj.user_point2_z).replace(' ', '')
        if baseAreaObj.Normal == coordinateDict[curCoordinate][0]:
            temp = str(baseAreaObj.Point1X) + "-" + str(obj.Length)
            obj.setExpression("helper", temp)
            temp_m3d += newLine + tab + str(obj.helper).replace(' ', '') + comma + point1_y + comma + \
                        point1_z + newLine + tab + point2_x + comma + point2_y + comma + point2_z

        elif baseAreaObj.Normal == coordinateDict[curCoordinate][1]:
            temp = str(baseAreaObj.Point1Y) + "-" + str(obj.Length)
            obj.setExpression("helper", temp)
            temp_m3d += newLine + tab + point1_x + comma + str(obj.helper).replace(' ', '') + comma + \
                        point1_z + newLine + tab + point2_x + comma + point2_y + comma + point2_z

        elif baseAreaObj.Normal == coordinateDict[curCoordinate][2]:
            temp = str(baseAreaObj.Point1Z) + "-" + str(obj.Length)
            obj.setExpression("helper", temp)
            temp_m3d += newLine + tab + point1_x + comma + point2_x + comma + str(obj.helper).replace(' ', '') \
                        + newLine + tab + point2_x + comma + point2_y + comma + point2_z
        else:
            Tools3D.sayz("正交投影面，法向选取有误\n")
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


def VolDraft_Revolution(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "ROTATE"
    temp_m3d += CoordinatesToObject(obj)
    temp_m3d += newLine + tab + obj.Area
    temp_m3d += semicolon + newLine
    temp_m3d += Mark(obj)
    temp_m3d_pap += ShareAttribute(obj)
    return temp_m3d, temp_m3d_pap


# 对于VolArray阵列体的BaseObj，单独设置坐标M3D，obj表示阵列体
def BaseCoordinates_Array(obj):

    baseObj = ObjectTools.getObjByLabel(obj.BaseType)
    curCoordinate = FreeCAD.ActiveDocument.CoordinateSystem

    temp_m3d = ""
    intervalX = str(obj.user_point_x).replace(' ', '')
    intervalY = str(obj.user_point_y).replace(' ', '')
    intervalZ = str(obj.user_point_z).replace(' ', '')
    interval1 = str(obj.user_interval1).replace(' ', '')
    interval2 = str(obj.user_interval2).replace(' ', '')
    num1 = str(obj.number1).replace(' ', '')
    numPolar = str(obj.numberPolar).replace(' ', '')

    if obj.ArrayType == "linear":
        if hasattr(baseObj, "Point1X"):
            point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
            point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
            point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point1_x_value + "+i*" + intervalX + comma + \
                        point1_y_value + "+i*" + intervalY + comma + \
                        point1_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point2X"):
            point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
            point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
            point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point2_x_value + "+i*" + intervalX + comma + \
                        point2_y_value + "+i*" + intervalY + comma + \
                        point2_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point3X"):
            point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
            point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
            point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point3_x_value + "+i*" + intervalX + comma + \
                        point3_y_value + "+i*" + intervalY + comma + \
                        point3_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point4X"):
            point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
            point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
            point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point4_x_value + "+i*" + intervalX + comma + \
                        point4_y_value + "+i*" + intervalY + comma + \
                        point4_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point5X"):
            point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
            point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
            point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point5_x_value + "+i*" + intervalX + comma + \
                        point5_y_value + "+i*" + intervalY + comma + \
                        point5_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point6X"):
            point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
            point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
            point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point6_x_value + "+i*" + intervalX + comma + \
                        point6_y_value + "+i*" + intervalY + comma + \
                        point6_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point7X"):
            point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
            point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
            point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point7_x_value + "+i*" + intervalX + comma + \
                        point7_y_value + "+i*" + intervalY + comma + \
                        point7_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point8X"):
            point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
            point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
            point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point8_x_value + "+i*" + intervalX + comma + \
                        point8_y_value + "+i*" + intervalY + comma + \
                        point8_z_value + "+i*" + intervalZ

    elif obj.ArrayType == "ortho":

        if obj.orthoFace == "XY":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point1_z_value
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point2_z_value
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point3_z_value
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point4_z_value
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point5_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point5_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point5_z_value
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point6_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point6_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point6_z_value
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point7_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point7_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point7_z_value
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point8_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point8_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point8_z_value

        elif obj.orthoFace == "XZ" or curCoordinate == "Polar":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_y_value + comma + \
                            point1_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_y_value + comma + \
                            point2_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_y_value + comma + \
                            point3_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_y_value + comma + \
                            point4_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point5_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point5_y_value + comma + \
                            point5_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point6_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point6_y_value + comma + \
                            point6_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point7_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point7_y_value + comma + \
                            point7_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point8_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point8_y_value + comma + \
                            point8_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2

        elif obj.orthoFace == "YZ":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + comma + \
                            point1_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + comma + \
                            point2_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + comma + \
                            point3_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + comma + \
                            point4_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point5_x_value + comma + \
                            point5_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point5_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point6_x_value + comma + \
                            point6_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point6_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point7_x_value + comma + \
                            point7_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point7_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point8_x_value + comma + \
                            point8_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point8_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2

        elif curCoordinate == "Cylindrical":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point1_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_z_value
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point2_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_z_value
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point3_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_z_value
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point4_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_z_value
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point5_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point5_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point5_z_value
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point6_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point6_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point6_z_value
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point7_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point7_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point7_z_value
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point8_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point8_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point8_z_value

        else:
            Tools3D.sayz("Create M3D in Ortho Failed! Please Check ArrayType.")
            return
    else:
        if curCoordinate == "Rectangular":
            if obj.centerAxis == "X":
                if hasattr(baseObj, "Point1X"):
                    point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                    point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                    point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point1_x_value + comma + "yy1'i'" + comma + "zz1'i'"

                if hasattr(baseObj, "Point2X"):
                    point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                    point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                    point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point2_x_value + comma + "yy2'i'" + comma + "zz2'i'"

                if hasattr(baseObj, "Point3X"):
                    point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                    point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                    point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point3_x_value + comma + "yy3'i'" + comma + "zz3'i'"

                if hasattr(baseObj, "Point4X"):
                    point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                    point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                    point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point4_x_value + comma + "yy4'i'" + comma + "zz4'i'"

                if hasattr(baseObj, "Point5X"):
                    point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                    point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                    point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point5_x_value + comma + "yy5'i'" + comma + "zz5'i'"

                if hasattr(baseObj, "Point6X"):
                    point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                    point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                    point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point6_x_value + comma + "yy6'i'" + comma + "zz6'i'"

                if hasattr(baseObj, "Point7X"):
                    point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                    point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                    point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point7_x_value + comma + "yy7'i'" + comma + "zz7'i'"

                if hasattr(baseObj, "Point8X"):
                    point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                    point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                    point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point8_x_value + comma + "yy8'i'" + comma + "zz8'i'"

            elif obj.centerAxis == "Y":
                if hasattr(baseObj, "Point1X"):
                    point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                    point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                    point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                 "xx1'i'" + comma + point1_y_value + comma + "zz1'i'"

                if hasattr(baseObj, "Point2X"):
                    point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                    point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                    point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx2'i'" + comma + point2_y_value + comma + "zz2'i'"

                if hasattr(baseObj, "Point3X"):
                    point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                    point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                    point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx3'i'" + comma + point3_y_value + comma + "zz3'i'"

                if hasattr(baseObj, "Point4X"):
                    point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                    point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                    point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx4'i'" + comma + point4_y_value + comma + "zz4'i'"

                if hasattr(baseObj, "Point5X"):
                    point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                    point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                    point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx5'i'" + comma + point5_y_value + comma + "zz5'i'"

                if hasattr(baseObj, "Point6X"):
                    point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                    point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                    point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx6'i'" + comma + point6_y_value + comma + "zz6'i'"

                if hasattr(baseObj, "Point7X"):
                    point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                    point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                    point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx7'i'" + comma + point7_y_value + comma + "zz7'i'"

                if hasattr(baseObj, "Point8X"):
                    point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                    point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                    point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx8'i'" + comma + point8_y_value + comma + "zz8'i'"

            else:
                if hasattr(baseObj, "Point1X"):
                    point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                    point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                    point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx1'i'" + comma + "yy1'i'" + comma + point1_z_value

                if hasattr(baseObj, "Point2X"):
                    point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                    point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                    point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx2'i'" + comma + "yy2'i'" + comma + point2_z_value

                if hasattr(baseObj, "Point3X"):
                    point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                    point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                    point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx3'i'" + comma + "yy3'i'" + comma + point3_z_value

                if hasattr(baseObj, "Point4X"):
                    point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                    point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                    point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx4'i'" + comma + "yy4'i'" + comma + point4_z_value

                if hasattr(baseObj, "Point5X"):
                    point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                    point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                    point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx5'i'" + comma + "yy5'i'" + comma + point5_z_value

                if hasattr(baseObj, "Point6X"):
                    point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                    point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                    point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx6'i'" + comma + "yy6'i'" + comma + point6_z_value

                if hasattr(baseObj, "Point7X"):
                    point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                    point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                    point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx7'i'" + comma + "yy7'i'" + comma + point7_z_value

                if hasattr(baseObj, "Point8X"):
                    point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                    point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                    point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                "xx8'i'" + comma + "yy8'i'" + comma + point8_z_value

        elif curCoordinate == "Polar":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + comma + \
                            point1_y_value + "+i*360deg/" + numPolar + comma + \
                            point1_z_value
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + comma + \
                            point2_y_value + "+i*360deg/" + numPolar + comma + \
                            point2_z_value
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + comma + \
                            point3_y_value + "+i*360deg/" + numPolar+ comma + \
                            point3_z_value
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + comma + \
                            point4_y_value + "+i*360deg/" + numPolar + comma + \
                            point4_z_value
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point5_x_value + comma + \
                            point5_y_value + "+i*360deg/" + numPolar + comma + \
                            point5_z_value
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point6_x_value + comma + \
                            point6_y_value + "+i*360deg/" + numPolar + comma + \
                            point6_z_value
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point7_x_value + comma + \
                            point7_y_value + "+i*360deg/" + numPolar + comma + \
                            point7_z_value
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point8_x_value + comma + \
                            point8_y_value + "+i*360deg/" + numPolar + comma + \
                            point8_z_value

        else:
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + comma + \
                            point1_y_value + comma + \
                            point1_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + comma + \
                            point2_y_value + comma + \
                            point2_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + comma + \
                            point3_y_value + comma + \
                            point3_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + comma + \
                            point4_y_value + comma + \
                            point4_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point5_x_value + comma + \
                            point5_y_value + comma + \
                            point5_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point6_x_value + comma + \
                            point6_y_value + comma + \
                            point6_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point7_x_value + comma + \
                            point7_y_value + comma + \
                            point7_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point8_x_value + comma + \
                            point8_y_value + comma + \
                            point8_z_value + "+i*360deg/" + numPolar

    return temp_m3d


# 对于VolArray阵列体的BaseObj，如果有半径，设置半径的M3D，obj表示阵列体
def BaseRadius_Array(obj):
    baseObj = ObjectTools.getObjByLabel(obj.BaseType)
    temp_m3d = ""
    if hasattr(baseObj, "user_radius1"):
        radius1_value = str(baseObj.user_radius1).replace(' ', '')
        temp_m3d += newLine + tab
        temp_m3d += radius1_value
        if hasattr(baseObj, "user_radius2"):
            radius2_value = str(baseObj.user_radius2).replace(' ', '')
            temp_m3d += comma + radius2_value
    return temp_m3d


# 针对环形区域体的阵列，单独设置其Base物体坐标和半径的M3D显示顺序
def BaseCoordRadius_ArrayOfAnnularSection(obj):
    baseObj = ObjectTools.getObjByLabel(obj.BaseType)
    curCoordinate = FreeCAD.ActiveDocument.CoordinateSystem

    temp_m3d = ""
    intervalX = str(obj.user_point_x).replace(' ', '')
    intervalY = str(obj.user_point_y).replace(' ', '')
    intervalZ = str(obj.user_point_z).replace(' ', '')
    interval1 = str(obj.user_interval1).replace(' ', '')
    interval2 = str(obj.user_interval2).replace(' ', '')
    num1 = str(obj.number1).replace(' ', '')
    numPolar = str(obj.numberPolar).replace(' ', '')

    if obj.ArrayType == "linear":
        if hasattr(baseObj, "Point1X"):
            point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
            point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
            point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point1_x_value + "+i*" + intervalX + comma + \
                        point1_y_value + "+i*" + intervalY + comma + \
                        point1_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point2X"):
            point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
            point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
            point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point2_x_value + "+i*" + intervalX + comma + \
                        point2_y_value + "+i*" + intervalY + comma + \
                        point2_z_value + "+i*" + intervalZ

        temp_m3d += BaseRadius_Array(obj)

        if hasattr(baseObj, "Point3X"):
            point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
            point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
            point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point3_x_value + "+i*" + intervalX + comma + \
                        point3_y_value + "+i*" + intervalY + comma + \
                        point3_z_value + "+i*" + intervalZ
        if hasattr(baseObj, "Point4X"):
            point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
            point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
            point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
            temp_m3d += newLine + tab + \
                        point4_x_value + "+i*" + intervalX + comma + \
                        point4_y_value + "+i*" + intervalY + comma + \
                        point4_z_value + "+i*" + intervalZ

    elif obj.ArrayType == "ortho":

        if obj.orthoFace == "XY":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point1_z_value
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point2_z_value

            temp_m3d += BaseRadius_Array(obj)

            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point3_z_value
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_y_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point4_z_value

        elif obj.orthoFace == "XZ" or curCoordinate == "Polar":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_y_value + comma + \
                            point1_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_y_value + comma + \
                            point2_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2

            temp_m3d += BaseRadius_Array(obj)

            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_y_value + comma + \
                            point3_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_y_value + comma + \
                            point4_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2

        elif obj.orthoFace == "YZ":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + comma + \
                            point1_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + comma + \
                            point2_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2

            temp_m3d += BaseRadius_Array(obj)

            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + comma + \
                            point3_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + comma + \
                            point4_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_z_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2

        elif curCoordinate == "Cylindrical":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point1_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point1_z_value
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point2_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point2_z_value

            temp_m3d += BaseRadius_Array(obj)

            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point3_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point3_z_value
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + "+(i-MODULO(i," + num1 + ")/" + num1 + "*" + interval2 + comma + \
                            point4_y_value + "+MODULO(i," + num1 + ")*" + interval1 + comma + \
                            point4_z_value

        else:
            Tools3D.sayz("Create M3D in Ortho Failed! Please Check ArrayType.")
            return

    else:
        if curCoordinate == "Rectangular":
            if obj.centerAxis == "X":
                if hasattr(baseObj, "Point1X"):
                    point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                    point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                    point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point1_x_value + comma + \
                                point1_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point1_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point1_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point1_y_value + "*sin(((2*PI)/" + numPolar + ")*i)"
                if hasattr(baseObj, "Point2X"):
                    point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                    point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                    point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point2_x_value + comma + \
                                point2_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point2_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point2_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point2_y_value + "*sin(((2*PI)/" + numPolar + ")*i)"

                temp_m3d += BaseRadius_Array(obj)

                if hasattr(baseObj, "Point3X"):
                    point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                    point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                    point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point3_x_value + comma + \
                                point3_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point3_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point3_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point3_y_value + "*sin(((2*PI)/" + numPolar + ")*i)"
                if hasattr(baseObj, "Point4X"):
                    point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                    point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                    point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point4_x_value + comma + \
                                point4_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point4_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point4_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point4_y_value + "*sin(((2*PI)/" + numPolar + ")*i)"

            elif obj.centerAxis == "Y":
                if hasattr(baseObj, "Point1X"):
                    point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                    point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                    point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point1_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point1_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point1_y_value + comma + \
                                point1_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point1_x_value + "*sin(((2*PI)/" + numPolar + ")*i)"
                if hasattr(baseObj, "Point2X"):
                    point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                    point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                    point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point2_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point2_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point2_y_value + comma + \
                                point2_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point2_x_value + "*sin(((2*PI)/" + numPolar + ")*i)"

                temp_m3d += BaseRadius_Array(obj)

                if hasattr(baseObj, "Point3X"):
                    point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                    point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                    point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point3_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point3_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point3_y_value + comma + \
                                point3_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point3_x_value + "*sin(((2*PI)/" + numPolar + ")*i)"
                if hasattr(baseObj, "Point4X"):
                    point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                    point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                    point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point4_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point4_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point4_y_value + comma + \
                                point4_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point4_x_value + "*sin(((2*PI)/" + numPolar + ")*i)"

            else:
                if hasattr(baseObj, "Point1X"):
                    point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                    point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                    point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point1_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point1_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point1_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point1_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point1_z_value
                if hasattr(baseObj, "Point2X"):
                    point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                    point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                    point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point2_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point2_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point2_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point2_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point2_z_value

                temp_m3d += BaseRadius_Array(obj)

                if hasattr(baseObj, "Point3X"):
                    point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                    point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                    point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point3_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point3_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point3_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point3_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point3_z_value
                if hasattr(baseObj, "Point4X"):
                    point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                    point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                    point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                    temp_m3d += newLine + tab + \
                                point4_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + point4_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point4_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + point4_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + comma + \
                                point4_z_value

        elif curCoordinate == "Polar":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + comma + \
                            point1_y_value + "+i*360deg/" + numPolar + comma + \
                            point1_z_value
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + comma + \
                            point2_y_value + "+i*360deg/" + numPolar + comma + \
                            point2_z_value

            temp_m3d += BaseRadius_Array(obj)

            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + comma + \
                            point3_y_value + "+i*360deg/" + numPolar+ comma + \
                            point3_z_value
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + comma + \
                            point4_y_value + "+i*360deg/" + numPolar + comma + \
                            point4_z_value

        else:
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point1_x_value + comma + \
                            point1_y_value + comma + \
                            point1_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point2_x_value + comma + \
                            point2_y_value + comma + \
                            point2_z_value + "+i*360deg/" + numPolar

            temp_m3d += BaseRadius_Array(obj)

            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point3_x_value + comma + \
                            point3_y_value + comma + \
                            point3_z_value + "+i*360deg/" + numPolar
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += newLine + tab + \
                            point4_x_value + comma + \
                            point4_y_value + comma + \
                            point4_z_value + "+i*360deg/" + numPolar

    return temp_m3d


# 针对阵列体正交坐标系下，并选择polar。坐标系信息太长的处理
def ArrayCoorLenth(obj):
    baseObj = ObjectTools.getObjByLabel(obj.BaseType)
    curCoordinate = FreeCAD.ActiveDocument.CoordinateSystem
    temp_m3d = ""
    numPolar = str(obj.numberPolar).replace(' ', '')
    if curCoordinate == "Rectangular" and obj.ArrayType == "polar":
        if obj.centerAxis == "X":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += "yy1'i'" + "=" + point1_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point1_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz1'i'" + "=" + point1_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point1_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine

            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += "yy2'i'" + "=" + point2_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point2_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz2'i'" + "=" + point2_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point2_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += "yy3'i'" + "=" + point3_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point3_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz3'i'" + "=" + point3_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point3_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += "yy4'i'" + "=" + point4_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point4_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz4'i'" + "=" + point4_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point4_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += "yy5'i'" + "=" + point5_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point5_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz5'i'" + "=" + point5_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point5_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += "yy6'i'" + "=" + point6_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point6_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz6'i'" + "=" + point6_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point6_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += "yy7'i'" + "=" + point7_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point7_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz7'i'" + "=" + point7_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point7_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += "yy8'i'" + "=" + point8_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point8_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz8'i'" + "=" + point8_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point8_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine

        elif obj.centerAxis == "Y":
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += "xx1'i'" + "=" + point1_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point1_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz1'i'" + "=" + point1_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point1_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += "xx2'i'" + "=" + point2_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point2_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz2'i'" + "=" + point2_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point2_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += "xx3'i'" + "=" + point3_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point3_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz3'i'" + "=" + point3_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point3_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += "xx4'i'" + "=" + point4_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point4_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz4'i'" + "=" + point4_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point4_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += "xx5'i'" + "=" + point5_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point5_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz5'i'" + "=" + point5_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point5_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += "xx6'i'" + "=" + point6_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point6_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz6'i'" + "=" + point6_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point6_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += "xx7'i'" + "=" + point7_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point7_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz7'i'" + "=" + point7_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point7_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += "xx8'i'" + "=" + point8_x_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point8_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "zz8'i'" + "=" + point8_z_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point8_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine

        else:
            if hasattr(baseObj, "Point1X"):
                point1_x_value = str(baseObj.user_point1_x).replace(' ', '')
                point1_y_value = str(baseObj.user_point1_y).replace(' ', '')
                point1_z_value = str(baseObj.user_point1_z).replace(' ', '')
                temp_m3d += "xx1'i'" + "=" + point1_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point1_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy1'i'" + "=" + point1_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point1_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine

            if hasattr(baseObj, "Point2X"):
                point2_x_value = str(baseObj.user_point2_x).replace(' ', '')
                point2_y_value = str(baseObj.user_point2_y).replace(' ', '')
                point2_z_value = str(baseObj.user_point2_z).replace(' ', '')
                temp_m3d += "xx2'i'" + "=" + point2_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point2_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy2'i'" + "=" + point2_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point2_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point3X"):
                point3_x_value = str(baseObj.user_point3_x).replace(' ', '')
                point3_y_value = str(baseObj.user_point3_y).replace(' ', '')
                point3_z_value = str(baseObj.user_point3_z).replace(' ', '')
                temp_m3d += "xx3'i'" + "=" + point3_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point3_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy3'i'" + "=" + point3_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point3_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point4X"):
                point4_x_value = str(baseObj.user_point4_x).replace(' ', '')
                point4_y_value = str(baseObj.user_point4_y).replace(' ', '')
                point4_z_value = str(baseObj.user_point4_z).replace(' ', '')
                temp_m3d += "xx4'i'" + "=" + point4_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point4_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy4'i'" + "=" + point4_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point4_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point5X"):
                point5_x_value = str(baseObj.user_point5_x).replace(' ', '')
                point5_y_value = str(baseObj.user_point5_y).replace(' ', '')
                point5_z_value = str(baseObj.user_point5_z).replace(' ', '')
                temp_m3d += "xx5'i'" + "=" + point5_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point5_z_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy5'i'" + "=" + point5_z_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point5_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point6X"):
                point6_x_value = str(baseObj.user_point6_x).replace(' ', '')
                point6_y_value = str(baseObj.user_point6_y).replace(' ', '')
                point6_z_value = str(baseObj.user_point6_z).replace(' ', '')
                temp_m3d += "xx6'i'" + "=" + point6_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point6_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy6'i'" + "=" + point6_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point6_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point7X"):
                point7_x_value = str(baseObj.user_point7_x).replace(' ', '')
                point7_y_value = str(baseObj.user_point7_y).replace(' ', '')
                point7_z_value = str(baseObj.user_point7_z).replace(' ', '')
                temp_m3d += "xx7'i'" + "=" + point7_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point7_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy7'i'" + "=" + point7_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point7_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
            if hasattr(baseObj, "Point8X"):
                point8_x_value = str(baseObj.user_point8_x).replace(' ', '')
                point8_y_value = str(baseObj.user_point8_y).replace(' ', '')
                point8_z_value = str(baseObj.user_point8_z).replace(' ', '')
                temp_m3d += "xx8'i'" + "=" + point8_x_value + "*cos(((2*PI)/" + numPolar + ")*i)+" + \
                            point8_y_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
                temp_m3d += "yy8'i'" + "=" + point8_y_value + "*cos(((2*PI)/" + numPolar + ")*i)-" + \
                            point8_x_value + "*sin(((2*PI)/" + numPolar + ")*i)" + semicolon + newLine
    return temp_m3d
