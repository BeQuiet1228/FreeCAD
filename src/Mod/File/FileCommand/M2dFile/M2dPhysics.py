# encoding:utf-8
import M2dObject
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","

#####################################################
# temp_m2d是与点/线/面有关的命令，放进指定的容器中         #
# temp_m2d_pap放到str_properties_and_processes容器中  #
# temp_m2d_ap放到str_all_plots容器中                  #
#####################################################


# 物理设置大部分都有两个返回值
def Driv(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    # 修改与坐标系相关的函数参数
    functionParameters = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular' or coodinate == 'Rectangular':
        functionParameters = ".JFUNC(T,X,Y) = "
    elif coodinate == u'Polar' or coodinate == 'Polar':
        pass
    elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
        functionParameters = ".JFUNC(T,Z,R) = "
    else:
        Tools2D.sayz("请选择正确的坐标系")
    if obj.sourceType == "点电流源":
        temp_m2d += "POINT"+blankSpace+obj.Label+blankSpace+obj.point1_X+blankSpace+obj.point1_Y+semicolon+newLine
        temp_m2d_pap += "FUNCTION"+blankSpace+obj.Label+functionParameters+obj.function+semicolon+newLine
        temp_m2d_pap += "DRIVER" + blankSpace + obj.electricCurrentDensity + blankSpace + obj.Label + ".JFUNC" \
                        + blankSpace + obj.assignSource + semicolon + newLine
    else:
        if obj.assignSource == "未指定":
            temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL" + blankSpace
            temp_m2d += M2dObject.PointCoordinates().point1(obj)
            temp_m2d += M2dObject.PointCoordinates().point2(obj)
            temp_m2d += semicolon + newLine
            temp_m2d_pap += "FUNCTION" + blankSpace + obj.Label + functionParameters + obj.function + semicolon + newLine
            temp_m2d_pap += "DRIVER" + blankSpace + obj.electricCurrentDensity + blankSpace + obj.Label + \
                            ".JFUNC" + blankSpace + obj.Label + semicolon + newLine
        else:
            temp_m2d_pap += "FUNCTION" + blankSpace + obj.Label + functionParameters + obj.function + semicolon + newLine
            temp_m2d_pap += "DRIVER" + blankSpace + obj.electricCurrentDensity + blankSpace + obj.Label \
                            + ".JFUNC" + blankSpace + obj.assignSource + semicolon + newLine
    return temp_m2d, temp_m2d_pap


def Foil(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    temp_m2d_cp = ""
    if obj.isCheckCustom:
        material = obj.customMaterial
    elif obj.isCheckDefault:
        material = obj.defaultMaterial
        # 此处默认GOLD材料属性
        temp_m2d_cp += "MATERIAL GOLD ATOMIC_NUMBER 79 ATOMIC_MASS 196.967 MASS_DENSITY 1.e4;"+newLine+newLine
    else:
        # 如果进入此分支将是致命的错误
        print("材料选项输入错误")
        material = "材料选项输入错误"
    if obj.foilType == "未指定":
        temp_m2d += "LINE"+blankSpace+obj.Label+blankSpace+"CONFORMAL"+blankSpace
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj)
        temp_m2d += semicolon+newLine
        temp_m2d_pap += "FOIL"+blankSpace+material+blankSpace+obj.foilThickness+blankSpace+obj.Label+semicolon+newLine
    else:
        temp_m2d_pap += "FOIL"+blankSpace+material+blankSpace+obj.foilThickness+blankSpace+obj.foilType+semicolon+newLine
    return temp_m2d_cp, temp_m2d, temp_m2d_pap


def Inductor(obj):
    """
    该函数有两个返回值
    return1: temp_m2d -> ...
    return2: temp_m2d_pap -> ...
    """
    temp_m2d = ""
    temp_m2d_pap = ""
    if obj.inductorType == "未指定":
        temp_m2d += "LINE"+blankSpace+obj.Label+blankSpace+"CONFORMAL"+blankSpace
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj)
        temp_m2d += semicolon+newLine
        temp_m2d_pap += "INDUCTOR" + blankSpace + obj.Label + blankSpace + obj.coilDiameter
    else:
        temp_m2d_pap += "INDUCTOR" + blankSpace + obj.inductorType + blankSpace + obj.coilDiameter
    if obj.isCheckSelfInductor:
        temp_m2d_pap += blankSpace + "INDUCTANCE" + blankSpace + obj.selfInductorCoefficient + semicolon + newLine
    else:
        temp_m2d_pap += semicolon + newLine
    return temp_m2d, temp_m2d_pap


def FreeSpace(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    if obj.orthogonalProjectionPlane == "未指定":
        temp_m2d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL" + blankSpace
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj)
        temp_m2d += semicolon+newLine
        temp_m2d += M2dObject.Mark(obj)
        # 临时变量FreeSpaceName,用来接收obj.Label或指定的观测面名字
        FreeSpaceName = obj.Label
    else:
        FreeSpaceName = obj.orthogonalProjectionPlane
    if obj.isCustomConductivity:
        temp_m2d_pap += "FUNCTION" + blankSpace + FreeSpaceName + ".F(Xn) = " + obj.customConductivity + semicolon + newLine
    temp_m2d_pap += "FREESPACE" + blankSpace + FreeSpaceName + blankSpace
    if obj.isPositive:
        temp_m2d_pap += "POSITIVE" + blankSpace
    elif obj.isNegative:
        temp_m2d_pap += "NEGATIVE" + blankSpace
    else:
        print("正向，反向属性输入错误")
    if obj.isCheckNormal1:
        temp_m2d_pap += "X1" + blankSpace + obj.absorb
    elif obj.isCheckNormal2:
        temp_m2d_pap += "X2" + blankSpace + obj.absorb
    else:
        print("吸收方向选取错误")
    if obj.isCustomConductivity:
        temp_m2d_pap += blankSpace + "CONDUCTIVITY" + blankSpace + FreeSpaceName + ".F"
    temp_m2d_pap += semicolon + newLine
    return temp_m2d, temp_m2d_pap


def Port(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    # 临时变量
    temp_m2d_FT = ""
    # 归一化临时变量
    temp_m2d_nor=""
    # circuit输入时间临时变量
    temp_m2d_cir=""
    # Mark临时变量
    temp_m2d_mark = ""
    # 与别名有关的观测命令
    temp_m2d_ObserveName = ""
    # portName用来接收obj.Label，还是投影线的指定线的名字
    # ftValue用来表示FT的值，解决输入长度过长的问题
    ftValue = ""
    # 修改与坐标系相关的函数参数
    functionParameters = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular' or coodinate == 'Rectangular':
        functionParameters = "(X,Y) = "
    elif coodinate == u'Polar' or coodinate == 'Polar':
        pass
    elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
        functionParameters = "(Z,R) = "
    else:
        Tools2D.sayz("请选择正确的坐标系")
    if obj.orthogonalProjectionPlane == "未指定":
        portName = obj.Label
        temp_m2d += "LINE"+blankSpace+obj.Label + blankSpace+"CONFORMAL"+blankSpace
        # 这里判断一下，起点和终点。把数值大的当作终点
        temp = ""
        # if obj.isCheckNormal1:
        #     temp += obj.point1_Y.replace(' ', '') + "-" + obj.point2_Y.replace(' ', '')
        # else:
        #     temp += obj.point1_X.replace(' ', '') + "-" + obj.point2_X.replace(' ', '')
        # obj.setExpression("helper", temp)
        # if float(obj.helper) >= 0:
        #     temp_m2d += newLine + tab + obj.point2_X + comma + obj.point2_Y
        #     temp_m2d += newLine + tab + obj.point1_X + comma + obj.point1_Y
        # else:
        #     temp_m2d += newLine + tab + obj.point1_X + comma + obj.point1_Y
        #     temp_m2d += newLine + tab + obj.point2_X + comma + obj.point2_Y
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj)
        temp_m2d += semicolon+newLine
        temp_m2d_mark += M2dObject.Mark(obj)
    else:
        portName = obj.orthogonalProjectionPlane
    if 0 <= len(str(obj.FT)) < 60:
        ftValue = obj.FT
    elif 60 <= len(str(obj.FT)) < 120:
        ftValue = obj.FT[0:len(str(obj.FT))/2]
        ftValue += newLine + tab + obj.FT[len(str(obj.FT))/2:]
    elif 120 <= len(str(obj.FT)) < 180:
        ftValue = obj.FT[0:len(str(obj.FT))/3]
        ftValue += newLine + tab + obj.FT[len(str(obj.FT))/3:len(str(obj.FT))/3*2]
        ftValue += newLine + tab + obj.FT[len(str(obj.FT))/3*2:]
    else:
        ftValue = obj.FT[0:len(str(obj.FT))/4]
        ftValue += newLine + tab + obj.FT[len(str(obj.FT)) / 4:len(str(obj.FT)) / 4 * 2]
        ftValue += newLine + tab + obj.FT[len(str(obj.FT)) / 4 * 2:len(str(obj.FT)) / 4 * 3]
        ftValue += newLine + tab + obj.FT[len(str(obj.FT)) / 4 * 3:]
    if obj.isCheckFT:
        temp_m2d_pap += "FUNCTION"+blankSpace + portName + ".F(T) = " + ftValue + semicolon + newLine
        if obj.isCheckNormalization:
            # temp_m2d += "LINE"+blankSpace+portName+blankSpace+"CONFORMAL"+blankSpace
            # temp_m2d += M2dObject.PointCoordinates().point1(obj)
            # temp_m2d += M2dObject.PointCoordinates().point2(obj)
            # temp_m2d += semicolon + newLine
            temp_m2d_nor += newLine+tab+"NORMALIZATION"+blankSpace+"VOLTAGE"+blankSpace+portName
        if obj.isCircuit:
            temp_m2d_cir += newLine + tab + "CIRCUIT" + blankSpace + obj.circuit+blankSpace+portName\
                            +".F"+blankSpace+"OBS$"+obj.observeName + semicolon
            temp_m2d_ObserveName += newLine + "OBSERVE" + blankSpace + "FIELD_INTEGRAL E.DL" +blankSpace + portName +\
                                    blankSpace + "suffix"+blankSpace+obj.observeName

    if obj.isCheckNormal1 == True and obj.isCheckNormal2 == False:
        if obj.isCheckGE2:
            temp_m2d_pap += "FUNCTION"+blankSpace+portName+".GE2"+functionParameters+obj.GE2+semicolon+newLine
            if obj.isCheckFT:
                temp_m2d_FT += newLine+tab+"INCOMING" + blankSpace + portName + ".F"+blankSpace+"FUNCTION"
                temp_m2d_FT += blankSpace + "E2"+blankSpace+portName+".GE2"
    elif obj.isCheckNormal1 == False and obj.isCheckNormal2 == True:
        if obj.isCheckGE2:
            temp_m2d_pap += "FUNCTION"+blankSpace+portName + ".GE1" + functionParameters + obj.GE1 + semicolon + newLine
            if obj.isCheckFT:
                temp_m2d_FT += newLine+tab+"INCOMING" + blankSpace + portName + ".F"+blankSpace+"FUNCTION"
                temp_m2d_FT += blankSpace+"E1"+blankSpace+portName+".GE1"
    else:
        print("法向选取有误")
        temp_m2d_pap += "法向选取有误"
    if obj.isCheckGE3:
        temp_m2d_pap += "FUNCTION" + blankSpace+portName + ".GE3" + functionParameters + obj.GE3 + semicolon+newLine
        if obj.isCheckFT:
            if obj.isCheckGE2 == True or obj.isCheckGE1 == True:
                temp_m2d_FT += blankSpace+"E3"+blankSpace+portName+".GE3"
            else:
                temp_m2d_FT += newLine + tab + "INCOMING" + blankSpace + portName + ".F" + blankSpace + "FUNCTION"
                temp_m2d_FT += blankSpace + "E3" + blankSpace + portName + ".GE3"
    direct = ""
    if obj.isNegative:
        direct = "NEGATIVE"
    if obj.isPositive:
        direct = "POSITIVE"
    temp_m2d_pap += "PORT"+blankSpace+ portName + blankSpace + direct
    if obj.isCheckVPORT:
        temp_m2d_pap += newLine+tab+"PHASE_VELOCITY"+blankSpace+obj.VPORT
    if obj.isCheckSCALE:
        temp_m2d_pap += newLine+tab+"EXPANSION"+blankSpace+obj.SCALE
    temp_m2d_pap = temp_m2d_pap+temp_m2d_FT+temp_m2d_nor+temp_m2d_cir
    temp_m2d_pap += temp_m2d_ObserveName
    temp_m2d_pap += semicolon + newLine
    temp_m2d += temp_m2d_mark
    return temp_m2d, temp_m2d_pap


def Symmry(obj):
    temp_m2d = ""
    temp_m2d_pap = ""
    temp_m2d_pap += "SYMMETRY"+blankSpace
    if obj.symmetricalType == "轴对称":
        temp_m2d_pap += "AXIAL" + blankSpace
    elif obj.symmetricalType == "镜像对称":
        temp_m2d_pap += "MIRROR" + blankSpace
    elif obj.symmetricalType == "周期对称":
        temp_m2d_pap += "PERIODIC" + blankSpace
    else:
        print("对称类型输入有误")
    if obj.orthogonalProjectionPlane == "未指定":
        temp_m2d += "LINE" + blankSpace + obj.Label + blankSpace + "CONFORMAL" + blankSpace
        temp_m2d += M2dObject.PointCoordinates().point1(obj)
        temp_m2d += M2dObject.PointCoordinates().point2(obj)
        temp_m2d += semicolon + newLine
        temp_m2d += M2dObject.Mark(obj)
        # 专门为周期对称计算增加的命令
        if obj.symmetricalType == "周期对称":
            temp_m2d += newLine + "AREA" + blankSpace + obj.Label + "P" + blankSpace + "CONFORMAL" + blankSpace
            if obj.isCheckNormal1:
                temp_m2d += newLine + tab + str(obj.helper).replace(' ', '') + comma + obj.point1_Y
                temp_m2d += newLine + tab + str(obj.helper).replace(' ', '') + comma + obj.point2_Y
            elif obj.isCheckNormal2:
                temp_m2d += newLine + tab + obj.point1_X + comma + str(obj.helper).replace(' ', '')
                temp_m2d += newLine + tab + obj.point2_X + comma + str(obj.helper).replace(' ', '')
            temp_m2d += semicolon + newLine
            if obj.isMarkX:
                temp_m2d += "MARK" + blankSpace + obj.Label + "P" + blankSpace + "X1"
                temp_m2d += blankSpace + "SIZE" + blankSpace + obj.MarkX + semicolon + newLine
            if obj.isMarkY:
                temp_m2d += "MARK" + blankSpace + obj.Label + "P" + blankSpace + "X2"
                temp_m2d += blankSpace + "SIZE" + blankSpace + obj.MarkY + semicolon + newLine
        temp_m2d_pap += obj.Label+blankSpace
    else:
        temp_m2d_pap += obj.orthogonalProjectionPlane+blankSpace
    if obj.isPositive:
        temp_m2d_pap += "POSITIVE"
        if obj.symmetricalType == "周期对称":
            if obj.orthogonalProjectionPlane == "未指定":
                temp_m2d_pap += blankSpace+obj.Label+"P" + blankSpace + "NEGATIVE"
            else:
                temp_m2d_pap += blankSpace + obj.assignType + blankSpace + "NEGATIVE"
    elif obj.isNegative:
        temp_m2d_pap += "NEGATIVE"
        if obj.symmetricalType == "周期对称":
            if obj.orthogonalProjectionPlane == "未指定":
                temp_m2d_pap += blankSpace+obj.Label+"P" + blankSpace + "POSITIVE"
            else:
                temp_m2d_pap += blankSpace + obj.assignType + blankSpace + "POSITIVE"
    else:
        print("请选择正确的正向反向")
    temp_m2d_pap += semicolon + newLine
    return temp_m2d, temp_m2d_pap


def Mark(obj):
    temp_m2d = ""
    temp_m2d += "MARK" + blankSpace + obj.markObject + blankSpace + obj.direction + blankSpace
    if obj.isMINIMUM:
        temp_m2d += "MINIMUM" + blankSpace
    if obj.isMIDPOINT:
        temp_m2d += "MIDPOINT" + blankSpace
    if obj.isMAXIMUM:
        temp_m2d += "MAXIMUM" + blankSpace
    temp_m2d += "SIZE" + blankSpace + obj.size + semicolon + newLine
    return temp_m2d