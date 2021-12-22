# encoding:utf-8
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import Attribute
from Modeling.Modeling2D.Tools.Tools2D import sayz


blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","

def Point(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # for i in expression_list:
    #     if i[0] == "X":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Y":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    temp_m2d += "POINT"+blankSpace+obj.Label + blankSpace + point1_x_value + blankSpace + point1_y_value + semicolon + newLine
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


# 把每个点的坐标抽象出来,此处物理设置的点坐标抽象
class PointCoordinates:
    def point1(self, obj):
        temp_m2d = ""
        temp_m2d += newLine + tab + obj.point1_X + comma + obj.point1_Y
        return temp_m2d

    def point2(self, obj):
        temp_m2d = ""
        temp_m2d += newLine + tab + obj.point2_X + comma + obj.point2_Y
        return temp_m2d


# 点线面的坐标与物理设置有表达式引擎不同，单独抽象出来
def CoordinatesToObject(obj):
    temp_m2d = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # for i in expression_list:
    #     if i[0] == "x1_helper":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "y1_helper":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "x2_helper":
    #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "y2_helper":
    #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
    temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value
    temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value
    temp_m2d += semicolon + newLine
    return temp_m2d


# 通用属性抽象出来，单独处理
def ShareAttribute(obj):
    temp_m2d_pap = ""
    if obj.Attribute == Attribute.NotDefine:
        pass
    elif obj.Attribute == Attribute.Conductor:
        temp_m2d_pap += "CONDUCTOR" + blankSpace + obj.Label + semicolon + newLine
    elif obj.Attribute == Attribute.Custom:
        # 如果不存在自定义属性，添加该属性
        if not hasattr(obj, "C_SIGMA"):
            Tools2D.completionProperties(obj)
        # # # 属性的ui没做下拉框，先生成一下简单的m2d。等做了属性的ui,再打开后续的代码
        # temp_m2d_pap += "CUSTOM" + blankSpace + obj.Label + semicolon + newLine
        if obj.C_SIGMA == "Isotropy":
            temp_m2d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA1 + semicolon + newLine
        elif obj.C_SIGMA == "Anisotropy":
            temp_m2d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA1 + \
                            blankSpace + "X1" + semicolon + newLine
            temp_m2d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA2 + \
                            blankSpace + "X2" + semicolon + newLine
            temp_m2d_pap += "CONDUCTANCE" + blankSpace + obj.Label + blankSpace + obj.SIGMA3 + \
                            blankSpace + "X3" + semicolon + newLine
        if obj.RDC == "Isotropy":
            temp_m2d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS1 + semicolon + newLine
        elif obj.RDC == "Anisotropy":
            temp_m2d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS1 + \
                            blankSpace + "X1" + semicolon + newLine
            temp_m2d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS2 + \
                            blankSpace + "X2" + semicolon + newLine
            temp_m2d_pap += "DIELECTRIC" + blankSpace + obj.Label + blankSpace + obj.EPS3 + \
                            blankSpace + "X3" + semicolon + newLine
    elif obj.Attribute == Attribute.Void or obj.Attribute == Attribute.Vacuo:
        temp_m2d_pap += "VOID" + blankSpace + obj.Label + semicolon + newLine
    else:
        temp_m2d_pap += "无法识别的属性类型"
    return temp_m2d_pap


# 网格命令抽象出来单独处理
def Mark(obj):
    temp_m2d = ""
    if obj.isMarkX:
        temp_m2d += "MARK"+blankSpace+obj.Label+blankSpace+"X1"
        if obj.isCheckMinX:
            temp_m2d += blankSpace+"MINIMUN"
        if obj.isCheckMidX:
            temp_m2d += blankSpace+"MIDPOINT"
        if obj.isCheckMaxX:
            temp_m2d += blankSpace+"MAXIMUM"
        temp_m2d += blankSpace+"SIZE"+blankSpace+obj.MarkX+semicolon+newLine
    if obj.isMarkY:
        temp_m2d += "MARK"+blankSpace+obj.Label+blankSpace+"X2"
        if obj.isCheckMinY:
            temp_m2d += blankSpace+"MINIMUN"
        if obj.isCheckMidY:
            temp_m2d += blankSpace+"MIDPOINT"
        if obj.isCheckMaxY:
            temp_m2d += blankSpace+"MAXIMUM"
        temp_m2d += blankSpace+"SIZE"+blankSpace+obj.MarkY+semicolon+newLine
    return temp_m2d


def Line(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    temp_m2d += "LINE"+blankSpace+obj.Label+blankSpace+"OBLIQUE"
    temp_m2d += CoordinatesToObject(obj)
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


def LineConformal(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    temp_m2d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    # 判断起点终点的坐标
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # for i in expression_list:
    #     if i[0] == "x1_helper":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "y1_helper":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "x2_helper":
    #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "y2_helper":
    #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
    if obj.normal == "X" or obj.normal == "x":
        temp = obj.y1_helper.Value - obj.y2_helper.Value
    elif obj.normal == "Y" or obj.normal == "y":
        temp = obj.x1_helper.Value - obj.x2_helper.Value
    elif obj.normal == "Z" or obj.normal == "z":
        temp = obj.y1_helper.Value - obj.y2_helper.Value
    elif obj.normal == "R" or obj.normal == "r":
        temp = obj.x1_helper.Value - obj.x2_helper.Value
    else:
        temp = obj.y1_helper.Value - obj.y2_helper.Value
    if float(temp) >= 0:
        temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value
        temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value
    else:
        temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value
        temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value
    # temp_m2d += M2dObject.PointCoordinates().point1(obj)
    # temp_m2d += M2dObject.PointCoordinates().point2(obj)
    temp_m2d += semicolon + newLine
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


def AreaComformal(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # for i in expression_list:
    #     if i[0] == "Point1X":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point1Y":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point2X":
    #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point2Y":
    #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
    temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
    # 判断起点和终点
    temp1 = obj.Point1X.Value - obj.Point2X.Value
    temp2 = obj.Point1Y.Value - obj.Point2Y.Value
    if float(temp1) < 0 and float(temp2) < 0:
        temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value
        temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value + semicolon + newLine
    elif float(temp1) > 0 and float(temp2) < 0:
        temp_m2d += newLine + tab + point2_x_value + comma + point1_y_value
        temp_m2d += newLine + tab + point1_x_value + comma + point2_y_value + semicolon + newLine
    elif float(temp1) < 0 and float(temp2) > 0:
        temp_m2d += newLine + tab + point1_x_value + comma + point2_y_value
        temp_m2d += newLine + tab + point2_x_value + comma + point1_y_value + semicolon + newLine
    elif float(temp1) > 0 and float(temp2) > 0:
        temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value
        temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value + semicolon + newLine
    else:
        sayz(u"请输入正确的坐标值")
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


def Rectangle(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # for i in expression_list:
    #     if i[0] == "Point1X":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point1Y":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point2X":
    #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point2Y":
    #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
    temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "RECTANGULAR"
    # 判断起点和终点
    temp1 = obj.Point1X.Value - obj.Point2X.Value
    temp2 = obj.Point1Y.Value - obj.Point2Y.Value
    if float(temp1) < 0 and float(temp2) < 0:
        temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value
        temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value + semicolon + newLine
    elif float(temp1) > 0 and float(temp2) < 0:
        temp_m2d += newLine + tab + point2_x_value + comma + point1_y_value
        temp_m2d += newLine + tab + point1_x_value + comma + point2_y_value + semicolon + newLine
    elif float(temp1) < 0 and float(temp2) > 0:
        temp_m2d += newLine + tab + point1_x_value + comma + point2_y_value
        temp_m2d += newLine + tab + point2_x_value + comma + point1_y_value + semicolon + newLine
    elif float(temp1) > 0 and float(temp2) > 0:
        temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value
        temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value + semicolon + newLine
    else:
        sayz(u"请输入正确的坐标值")
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


def Circle(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    radius_value = str(obj.user_radius).replace(' ', '')
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # # 如果表达式引擎中存在对应数据，则使用表达式引擎中的数据
    # for i in expression_list:
    #     if i[0] == "Radius":
    #         radius_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "x_helper":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "y_helper":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CIRCLE" + blankSpace + \
                point1_x_value + blankSpace + point1_y_value + blankSpace + radius_value
    temp_m2d += semicolon + newLine
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


def Sector(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    radius_value = str(obj.user_radius).replace(' ', '')
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # # 如果表达式引擎中存在对应数据，则使用表达式引擎中的数据
    # for i in expression_list:
    #     if i[0] == "Radius":
    #         radius_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "X":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Y":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    if obj.Quadrant == "第一象限":
        quadrant = "1"
    elif obj.Quadrant == "第二象限":
        quadrant = "2"
    elif obj.Quadrant == "第三象限":
        quadrant = "3"
    elif obj.Quadrant == "第四象限":
        quadrant = "4"
    else:
        quadrant = "1"
    temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "QUARTERROUND" + blankSpace + quadrant + blankSpace + \
                point1_x_value + blankSpace + point1_y_value + blankSpace + radius_value
    temp_m2d += semicolon + newLine
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


def Fillet(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    radius_value = str(obj.user_radius).replace(' ', '')
    point1_x_value = str(obj.user_point1_x).replace(' ', '')
    point1_y_value = str(obj.user_point1_y).replace(' ', '')
    point2_x_value = str(obj.user_point2_x).replace(' ', '')
    point2_y_value = str(obj.user_point2_y).replace(' ', '')
    startAngle_value = str(obj.user_startAngle).replace(' ', '')
    endAngle_value = str(obj.user_endAngle).replace(' ', '')
    # expression_list = obj.ExpressionEngine
    # for i in expression_list:
    #     if i[0] == "Radius":
    #         radius_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point1X":
    #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point1Y":
    #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point2X":
    #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
    #     elif i[0] == "Point2Y":
    #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
    temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "FILLET"
    temp_m2d += newLine + tab + point1_x_value + comma + point1_y_value
    temp_m2d += newLine + tab + point2_x_value + comma + point2_y_value
    temp_m2d += newLine + tab + radius_value + blankSpace + startAngle_value + blankSpace + endAngle_value
    temp_m2d += semicolon + newLine
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap


def AreaPolygonal(obj):
    temp_m2d = ""
    temp_m2d_pap = ""

    PointList = obj.Points
    length = len(PointList)
    temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "POLYGONAL" + newLine + tab
    # for index in range(length):
    #     temp_m2d += str((PointList[index])[0]) + "m" + comma + str((PointList[index])[1]) + "m"
    #     temp_m2d += newLine + tab
    for index in range(length):
        temp_m2d += str(getattr(obj, "user_point" + str(index + 1) + "_x")).replace(' ', '') \
                    + comma \
                    + str(getattr(obj, "user_point" + str(index + 1) + "_y")).replace(' ', '')
        temp_m2d += newLine + tab
    temp_m2d += str(obj.user_point1_x).replace(' ', '') + comma + str(obj.user_point1_y).replace(' ', '') + semicolon + newLine
    temp_m2d += Mark(obj)
    temp_m2d_pap += ShareAttribute(obj)
    return temp_m2d, temp_m2d_pap

