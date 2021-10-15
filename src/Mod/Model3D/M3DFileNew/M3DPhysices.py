# encoding:utf-8
# 此文件存放波导端口、吸收边界、对称边界、螺旋线圈、空间电流源、箔片、电感、新型材料定义、宏粒子合并、新型粒子定义、MARK
import M3DObject, M3DShare
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","


def Port(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    # 临时变量
    temp_m3d_FT = ""
    # 归一化临时变量
    temp_m3d_nor=""
    # circuit输入时间临时变量
    temp_m3d_cir=""
    # Mark临时变量
    temp_m3d_mark = ""
    # 与别名有关的观测命令
    temp_m3d_ObserveName = ""
    # portName用来接收obj.Label，还是投影线的指定线的名字
    # ftValue用来表示FT的值，解决输入长度过长的问题
    ftValue = ""
    # 修改与坐标系相关的函数参数
    functionParameters = M3DShare.getCoodinateParaWithPort()
    if obj.orthogonalProjectionPlane == "未指定":
        portName = obj.Label
        # temp_m3d += "AREA"+blankSpace+obj.Label + blankSpace+"CONFORMAL"+blankSpace
        # 这里判断一下，起点和终点。把数值大的当作终点
        # temp = ""
        # if obj.isCheckNormal1:
        #     temp += obj.point1_Y.replace(' ', '') + "-" + obj.point2_Y.replace(' ', '')
        # else:
        #     temp += obj.point1_X.replace(' ', '') + "-" + obj.point2_X.replace(' ', '')
        # obj.setExpression("helper", temp)
        # if float(obj.helper) >= 0:
        #     temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y
        #     temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y
        # else:
        #     temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y
        #     temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y
        point1_x_value = str(obj.point1_X).replace(' ', '')
        point1_y_value = str(obj.point1_Y).replace(' ', '')
        point1_z_value = str(obj.point1_Z).replace(' ', '')
        point2_x_value = str(obj.point2_X).replace(' ', '')
        point2_y_value = str(obj.point2_Y).replace(' ', '')
        point2_z_value = str(obj.point2_Z).replace(' ', '')

        temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL"
        #
        temp1 = ""
        temp2 = ""
        temp3 = ""
        # 判断起点和终点
        # helper1 = int(obj.point1_X) - int(obj.point2_X)
        # helper2 = int(obj.point1_Y) - int(obj.point2_Y)
        # helper3 = int(obj.point1_Y) - int(obj.point2_Y)
        temp1 += obj.point1_X.replace(' ', '') + "-" + obj.point2_X.replace(' ', '')
        temp2 += obj.point1_Y.replace(' ', '') + "-" + obj.point2_Y.replace(' ', '')
        temp3 += obj.point1_Z.replace(' ', '') + "-" + obj.point2_Z.replace(' ', '')
        obj.setExpression("helper1", temp1)
        obj.setExpression("helper2", temp2)
        obj.setExpression("helper3", temp3)
        # coodinate = FreeCAD.ActiveDocument.CoordinateSystem

        if obj.isCheckNormal1:
            if obj.helper2.Value <= 0 and obj.helper3.Value <= 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point2_z_value + semicolon + newLine
            elif obj.helper2.Value > 0 and obj.helper3.Value < 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
            elif obj.helper2.Value < 0 and obj.helper3.Value > 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
            elif obj.helper2.Value > 0 and obj.helper3.Value > 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point2_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
            else:
                Tools3D.sayz(u"请输入正确的坐标值")

        elif obj.isCheckNormal2:
            if obj.helper1.Value <= 0 and obj.helper3.Value <= 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
            elif obj.helper1.Value > 0 and obj.helper3.Value < 0:
                temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value + semicolon + newLine
            elif obj.helper1.Value < 0 and obj.helper3.Value > 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point2_z_value
                temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
            elif obj.helper1.Value > 0 and obj.helper3.Value > 0:
                temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point2_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
            else:
                Tools3D.sayz(u"请输入正确的坐标值")

        elif obj.isCheckNormal3:
            if obj.helper1.Value <= 0 and obj.helper2.Value <= 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
            elif obj.helper1.Value > 0 and obj.helper2.Value < 0:
                temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value + semicolon + newLine
            elif obj.helper1.Value < 0 and obj.helper2.Value > 0:
                temp_m3d += newLine + tab + point1_x_value + comma + point2_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point2_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
            elif obj.helper1.Value > 0 and obj.helper2.Value > 0:
                temp_m3d += newLine + tab + point2_x_value + comma + point2_y_value + comma + point1_z_value
                temp_m3d += newLine + tab + point1_x_value + comma + point1_y_value + comma + point1_z_value + semicolon + newLine
            else:
                Tools3D.sayz(u"请输入正确的坐标值")
        # temp_m3d += M3DShare.PointCoordinates().point1(obj)
        # temp_m3d += M3DShare.PointCoordinates().point2(obj)
        # temp_m3d += semicolon+newLine
        temp_m3d_mark += M3DShare.Mark(obj)
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
        temp_m3d_pap += "FUNCTION"+blankSpace + portName + ".F(T) = " + ftValue + semicolon + newLine
        if obj.isCheckNormalization:
            temp_normalization = str(obj.normalization).replace('.LINE', '')
            if temp_normalization != "未指定":
                temp_obj = ObjectTools.getObjByLabel(temp_normalization)
                if hasattr(temp_obj, "Type") and temp_obj.Type == ObjectTools.ObjectType.Area_Conformal:
                    temp_m3d += "LINE"+blankSpace+portName+".LINE"+blankSpace+"CONFORMAL"+blankSpace
                    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
                    if coodinate == u'Rectangular':
                        if obj.isCheckNormal1:
                            temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(obj.helper/2).replace(' ', '')
                            temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(obj.helper/2).replace(' ', '')
                        elif obj.isCheckNormal2:
                            temp_m3d += newLine + tab + str(obj.helper/2).replace(' ', '') + comma + obj.point1_Y + comma + obj.point1_Z
                            temp_m3d += newLine + tab + str(obj.helper/2).replace(' ', '') + comma + obj.point2_Y + comma + obj.point2_Z
                        elif obj.isCheckNormal3:
                            temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper/2).replace(' ', '') + comma + obj.point1_Z
                            temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper/2).replace(' ', '') + comma + obj.point2_Z
                    elif coodinate == u"Polar":
                        if obj.isCheckNormal1:
                            temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper0/2).replace(' ',
                                                                                                       '') + comma + obj.point1_Z
                            temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper0/2).replace(' ',
                                                                                                       '') + comma + obj.point2_Z
                        elif obj.isCheckNormal2:
                            temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(obj.helper/2).replace(
                                ' ', '')
                            temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(obj.helper/2).replace(
                                ' ', '')
                        elif obj.isCheckNormal3:
                            temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper0/2).replace(' ',
                                                                                                       '') + comma + obj.point1_Z
                            temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper0/2).replace(' ',
                                                                                                       '') + comma + obj.point2_Z
                    # elif coodinate == u"Cylinder":
                    else:
                        if obj.isCheckNormal1:
                            temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(obj.helper0/2).replace(
                                ' ', '')
                            temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(obj.helper0/2).replace(
                                ' ', '')
                        elif obj.isCheckNormal2:
                            temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(obj.helper0/2).replace(
                                ' ', '')
                            temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(obj.helper0/2).replace(
                                ' ', '')
                        elif obj.isCheckNormal3:
                            temp_m3d += newLine + tab + str(obj.helper/2).replace(' ',
                                                                                '') + comma + obj.point1_Y + comma + obj.point1_Z
                            temp_m3d += newLine + tab + str(obj.helper/2).replace(' ',
                                                                                '') + comma + obj.point2_Y + comma + obj.point2_Z
                    temp_m3d +=semicolon + newLine
            # 归一化和名字一样的情况
            if temp_normalization==obj.Label:
                temp_m3d += "LINE" + blankSpace + portName + ".LINE" + blankSpace + "CONFORMAL" + blankSpace
                coodinate = FreeCAD.ActiveDocument.CoordinateSystem
                if coodinate == u'Rectangular':
                    if obj.isCheckNormal1:
                        temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(
                            obj.helper / 2).replace(' ', '')
                        temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(
                            obj.helper / 2).replace(' ', '')
                    elif obj.isCheckNormal2:
                        temp_m3d += newLine + tab + str(obj.helper / 2).replace(' ',
                                                                                '') + comma + obj.point1_Y + comma + obj.point1_Z
                        temp_m3d += newLine + tab + str(obj.helper / 2).replace(' ',
                                                                                '') + comma + obj.point2_Y + comma + obj.point2_Z
                    elif obj.isCheckNormal3:
                        temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper / 2).replace(' ',
                                                                                                       '') + comma + obj.point1_Z
                        temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper / 2).replace(' ',
                                                                                                       '') + comma + obj.point2_Z
                elif coodinate == u"Polar":
                    if obj.isCheckNormal1:
                        temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper0 / 2).replace(' ',
                                                                                                        '') + comma + obj.point1_Z
                        temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper0 / 2).replace(' ',
                                                                                                        '') + comma + obj.point2_Z
                    elif obj.isCheckNormal2:
                        temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(
                            obj.helper / 2).replace(
                            ' ', '')
                        temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(
                            obj.helper / 2).replace(
                            ' ', '')
                    elif obj.isCheckNormal3:
                        temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper0 / 2).replace(' ',
                                                                                                        '') + comma + obj.point1_Z
                        temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper0 / 2).replace(' ',
                                                                                                        '') + comma + obj.point2_Z
                # elif coodinate == u"Cylinder":
                else:
                    if obj.isCheckNormal1:
                        temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(
                            obj.helper0 / 2).replace(
                            ' ', '')
                        temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(
                            obj.helper0 / 2).replace(
                            ' ', '')
                    elif obj.isCheckNormal2:
                        temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(
                            obj.helper0 / 2).replace(
                            ' ', '')
                        temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(
                            obj.helper0 / 2).replace(
                            ' ', '')
                    elif obj.isCheckNormal3:
                        temp_m3d += newLine + tab + str(obj.helper / 2).replace(' ',
                                                                                '') + comma + obj.point1_Y + comma + obj.point1_Z
                        temp_m3d += newLine + tab + str(obj.helper / 2).replace(' ',
                                                                                '') + comma + obj.point2_Y + comma + obj.point2_Z
                temp_m3d += semicolon + newLine
            # temp_m2d += M2dObject.PointCoordinates().point1(obj)
            # temp_m2d += M2dObject.PointCoordinates().point2(obj)
            # temp_m3d += semicolon + newLine
            temp_m3d_nor += newLine+tab+"NORMALIZATION"+blankSpace+"VOLTAGE"+blankSpace+obj.normalization
        if obj.isCircuit:
            temp_m3d_cir += newLine + tab + "CIRCUIT" + blankSpace + obj.circuit+blankSpace+portName\
                            +".F"+blankSpace+"OBS$"+obj.observeName + semicolon
            temp_m3d_ObserveName += newLine + "OBSERVE" + blankSpace + "FIELD_INTEGRAL E.DL" +blankSpace + portName +\
                                    blankSpace + "suffix"+blankSpace+obj.observeName

    if obj.isCheckNormal1 == True :
        if obj.isCheckGE2:
            temp_m3d_pap += "FUNCTION"+blankSpace+portName+".GE2"+functionParameters+obj.GE2+semicolon+newLine
            if obj.isCheckFT:
                temp_m3d_FT += newLine+tab+"INCOMING" + blankSpace + portName + ".F"+blankSpace+"FUNCTION"
                temp_m3d_FT += blankSpace + "E2"+blankSpace+portName+".GE2"
        if obj.isCheckGE3:
            temp_m3d_pap += "FUNCTION"+blankSpace+portName+".GE3"+functionParameters+obj.GE3+semicolon+newLine
            if obj.isCheckFT and (obj.isCheckGE2 == False):
                temp_m3d_FT += newLine+tab+"INCOMING" + blankSpace + portName + ".F"+blankSpace+"FUNCTION"
                temp_m3d_FT += blankSpace + "E3"+blankSpace+portName+".GE3"
            elif obj.isCheckFT and obj.isCheckGE2:
                temp_m3d_FT += blankSpace + "E3" + blankSpace + portName + ".GE3"

    elif obj.isCheckNormal2 == True:
        if obj.isCheckGE2:
            temp_m3d_pap += "FUNCTION"+blankSpace+portName + ".GE1" + functionParameters + obj.GE2 + semicolon + newLine
            if obj.isCheckFT:
                temp_m3d_FT += newLine+tab+"INCOMING" + blankSpace + portName + ".F"+blankSpace+"FUNCTION"
                temp_m3d_FT += blankSpace+"E1"+blankSpace+portName+".GE1"
        if obj.isCheckGE3:
            temp_m3d_pap += "FUNCTION"+blankSpace+portName+".GE3"+functionParameters+obj.GE3+semicolon+newLine
            if obj.isCheckFT and (obj.isCheckGE1 == False):
                temp_m3d_FT += blankSpace + "E3" + blankSpace + portName + ".GE3"
            #     Tools3D.sayz("运行的是哪一个222")
            # elif obj.isCheckFT and obj.isCheckGE1:
            #     temp_m3d_FT += newLine + tab + "INCOMING" + blankSpace + portName + ".F" + blankSpace + "FUNCTION"
            #     temp_m3d_FT += blankSpace + "E3" + blankSpace + portName + ".GE3"
            #     Tools3D.sayz("运行的是哪一个22233333")
    elif obj.isCheckNormal3 == True:
        if obj.isCheckGE2:
            temp_m3d_pap += "FUNCTION" + blankSpace + portName + ".GE1" + functionParameters + obj.GE2 + semicolon + newLine
            if obj.isCheckFT:
                temp_m3d_FT += newLine + tab + "INCOMING" + blankSpace + portName + ".F" + blankSpace + "FUNCTION"
                temp_m3d_FT += blankSpace + "E1" + blankSpace + portName + ".GE1"
        if obj.isCheckGE3:
            temp_m3d_pap += "FUNCTION" + blankSpace + portName + ".GE2" + functionParameters + obj.GE3 + semicolon + newLine
            if obj.isCheckFT and (obj.isCheckGE1 == False):
                temp_m3d_FT += blankSpace + "E2" + blankSpace + portName + ".GE2"
            # elif obj.isCheckFT and obj.isCheckGE1:
            #     temp_m3d_FT += newLine + tab + "INCOMING" + blankSpace + portName + ".F" + blankSpace + "FUNCTION"
            #     temp_m3d_FT += blankSpace + "E2" + blankSpace + portName + ".GE2"
    else:
        print("法向选取有误")
        temp_m3d_pap += "法向选取有误"

    # if obj.isCheckGE3:
    #     temp_m3d_pap += "FUNCTION" + blankSpace+portName + ".GE3" + functionParameters + obj.GE3 + semicolon+newLine
    #     if obj.isCheckFT:
    #         if obj.isCheckGE2 == True or obj.isCheckGE1 == True:
    #             temp_m3d_FT += blankSpace+"E3"+blankSpace+portName+".GE3"
    #         else:
    #             temp_m3d_FT += newLine + tab + "INCOMING" + blankSpace + portName + ".F" + blankSpace + "FUNCTION"
    #             temp_m3d_FT += blankSpace + "E3" + blankSpace + portName + ".GE3"
    if obj.isCheckLapras:
        if obj.isCheckFT:
            temp_m3d_FT += newLine + tab + "INCOMING" + blankSpace + portName + ".F" + blankSpace + "LAPLACIAN" + blankSpace + str(obj.laprasNumbers)
            spin_num = obj.laprasNumbers
            if spin_num >= 1:
                temp_m3d_FT += blankSpace + obj.lapras1 + blankSpace + str(obj.lapras1Value)
            if spin_num >= 2:
                temp_m3d_FT += blankSpace + obj.lapras2 + blankSpace + str(obj.lapras2Value)
            if spin_num >= 3:
                temp_m3d_FT += blankSpace + obj.lapras3 + blankSpace + str(obj.lapras3Value)
            if spin_num >= 4:
                temp_m3d_FT += blankSpace + obj.lapras4 + blankSpace + str(obj.lapras4Value)
            if spin_num == 5:
                temp_m3d_FT += blankSpace + obj.lapras5 + blankSpace + str(obj.lapras5Value)

    direct = ""
    if obj.isNegative:
        direct = "NEGATIVE"
    if obj.isPositive:
        direct = "POSITIVE"
    temp_m3d_pap += "PORT"+blankSpace+ portName + blankSpace + direct
    if obj.isCheckVPORT:
        temp_m3d_pap += newLine+tab+"PHASE_VELOCITY"+blankSpace+obj.VPORT
    if obj.isCheckSCALE:
        temp_m3d_pap += newLine+tab+"EXPANSION"+blankSpace+obj.SCALE
    if obj.isCheckLapras:
        pass

    temp_m3d_pap = temp_m3d_pap+temp_m3d_FT+temp_m3d_nor+temp_m3d_cir
    temp_m3d_pap += temp_m3d_ObserveName
    temp_m3d_pap += semicolon + newLine
    temp_m3d += temp_m3d_mark
    return temp_m3d, temp_m3d_pap


def FreeSpace(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    if obj.orthogonalProjectionPlane == "未指定":
        temp_m3d += "VOLUME" + blankSpace + obj.Label + blankSpace + "CONFORMAL" + blankSpace
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj)
        temp_m3d += semicolon+newLine
        temp_m3d += M3DShare.Mark(obj)
        # 临时变量FreeSpaceName,用来接收obj.Label或指定的观测面名字
        FreeSpaceName = obj.Label
    else:
        FreeSpaceName = obj.orthogonalProjectionPlane
    if obj.isCustomConductivity:
        temp_m3d_pap += "FUNCTION" + blankSpace + FreeSpaceName + ".F(Xn) = " + obj.customConductivity + semicolon + newLine
    temp_m3d_pap += "FREESPACE" + blankSpace + FreeSpaceName + blankSpace
    if obj.isPositive:
        temp_m3d_pap += "POSITIVE" + blankSpace
    elif obj.isNegative:
        temp_m3d_pap += "NEGATIVE" + blankSpace
    else:
        print("正向，反向属性输入错误")
    if obj.isCheckNormal1:
        temp_m3d_pap += "X1" + blankSpace + obj.absorb
    elif obj.isCheckNormal2:
        temp_m3d_pap += "X2" + blankSpace + obj.absorb
    elif obj.isCheckNormal3:
        temp_m3d_pap += "X3" + blankSpace + obj.absorb
    else:
        print("吸收方向选取错误")
    if obj.isCustomConductivity:
        temp_m3d_pap += blankSpace + "CONDUCTIVITY" + blankSpace + FreeSpaceName + ".F"
    temp_m3d_pap += semicolon + newLine
    return temp_m3d, temp_m3d_pap


def Symmry(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d_pap += "SYMMETRY"+blankSpace
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if obj.symmetricalType == "轴对称":
        temp_m3d_pap += "AXIAL" + blankSpace
    elif obj.symmetricalType == "镜像对称":
        temp_m3d_pap += "MIRROR" + blankSpace
    elif obj.symmetricalType == "周期对称":
        temp_m3d_pap += "PERIODIC" + blankSpace
    else:
        print("对称类型输入有误")
    if obj.orthogonalProjectionPlane == "未指定":
        temp_m3d += "AREA" + blankSpace + obj.Label + blankSpace + "CONFORMAL" + blankSpace
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj)
        temp_m3d += semicolon + newLine
        temp_m3d += M3DShare.Mark(obj)
        # 专门为周期对称计算增加的命令
        if obj.symmetricalType == "周期对称":
            temp_m3d += newLine + "AREA" + blankSpace + obj.Label + "P" + blankSpace + "CONFORMAL" + blankSpace
            if obj.isCheckNormal1:
                temp_m3d += newLine + tab + str(obj.helper).replace(' ', '') + comma + obj.point1_Y + comma + obj.point1_Z
                temp_m3d += newLine + tab + str(obj.helper).replace(' ', '') + comma + obj.point2_Y + comma + obj.point2_Z
            elif obj.isCheckNormal2:
                if coodinate == u'Polar':
                    temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper1).replace(' ',
                                                                                               '') + comma + obj.point1_Z
                    temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper1).replace(' ',
                                                                                               '') + comma + obj.point1_Z
                else:
                    temp_m3d += newLine + tab + obj.point1_X + comma + str(obj.helper).replace(' ', '') + comma + obj.point1_Z
                    temp_m3d += newLine + tab + obj.point2_X + comma + str(obj.helper).replace(' ', '') + comma + obj.point1_Z

            elif obj.isCheckNormal3:
                if coodinate == u"Cylindrical":
                    temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(obj.helper1).replace(
                        ' ', '')
                    temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(obj.helper1).replace(
                        ' ', '')
                else:
                    temp_m3d += newLine + tab + obj.point1_X + comma + obj.point1_Y + comma + str(obj.helper).replace(' ', '')
                    temp_m3d += newLine + tab + obj.point2_X + comma + obj.point2_Y + comma + str(obj.helper).replace(' ', '')
            temp_m3d += semicolon + newLine
            if obj.isMarkX:
                temp_m3d += "MARK" + blankSpace + obj.Label + "P" + blankSpace + "X1"
                temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkX + semicolon + newLine
            if obj.isMarkY:
                temp_m3d += "MARK" + blankSpace + obj.Label + "P" + blankSpace + "X2"
                temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkY + semicolon + newLine
            if obj.isMarkZ:
                temp_m3d += "MARK" + blankSpace + obj.Label + "P" + blankSpace + "X3"
                temp_m3d += blankSpace + "SIZE" + blankSpace + obj.MarkZ + semicolon + newLine
        temp_m3d_pap += obj.Label+blankSpace
    else:
        temp_m3d_pap += obj.orthogonalProjectionPlane+blankSpace
    if obj.isPositive:
        temp_m3d_pap += "POSITIVE"
        if obj.symmetricalType == "周期对称":
            if obj.orthogonalProjectionPlane == "未指定":
                temp_m3d_pap += blankSpace+obj.Label+"P" + blankSpace + "NEGATIVE"
            else:
                temp_m3d_pap += blankSpace + obj.assignType + blankSpace + "NEGATIVE"
    elif obj.isNegative:
        temp_m3d_pap += "NEGATIVE"
        if obj.symmetricalType == "周期对称":
            if obj.orthogonalProjectionPlane == "未指定":
                temp_m3d_pap += blankSpace+obj.Label+"P" + blankSpace + "POSITIVE"
            else:
                temp_m3d_pap += blankSpace + obj.assignType + blankSpace + "POSITIVE"
    else:
        print("请选择正确的正向反向")
    temp_m3d_pap += semicolon + newLine
    return temp_m3d, temp_m3d_pap


def Solend(obj):
    temp_m3d_pap = ""
    temp_m3d_pap += "SOLENOID" + blankSpace + obj.Label + blankSpace
    if obj.uniformParam == "None":
        temp_m3d_pap += "0" + blankSpace + "0" + blankSpace + "0" + blankSpace + "0" + blankSpace + "0" + blankSpace
    elif obj.uniformParam == "RZ因子":
        temp_m3d_pap += "1" + blankSpace + obj.factorR + blankSpace + obj.factorZ + blankSpace + "0" + blankSpace + "0" + blankSpace
    elif obj.uniformParam == "其他":
        temp_m3d_pap += "2" + blankSpace + obj.dutyCycle + blankSpace + obj.radiusInner + blankSpace + obj.radiusOuter \
                        + blankSpace + obj.permeability + blankSpace
    temp_m3d_pap += obj.coreZ + blankSpace + obj.coreR + blankSpace + obj.innerRadius + blankSpace + obj.outerRadius \
                    + blankSpace + obj.coilCurrent + blankSpace + obj.coilHalf + blankSpace + obj.turnRatio \
                    + blankSpace + obj.angleTheta + blankSpace + obj.anglePhi
    temp_m3d_pap += semicolon + newLine
    return temp_m3d_pap


def Driv(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    # 修改与坐标系相关的函数参数
    functionParameters = ""
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular' or coodinate == 'Rectangular':
        functionParameters = ".JFUNC(T,X,Y,Z) = "
    elif coodinate == u'Polar' or coodinate == 'Polar':
        functionParameters = ".JFUNC(T,R,P,Z) = "
    elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
        functionParameters = ".JFUNC(T,Z,R,P) = "
    else:
        Tools3D.sayz("请选择正确的坐标系")

    if obj.sourceType == "点电流源":
        objname = "POINT"
        # if obj.assignSource == "未指定":
        #     temp_m3d += "POINT"+blankSpace+obj.Label+blankSpace+obj.point1_X+blankSpace+obj.point1_Y+semicolon+newLine
        #     temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + functionParameters + obj.function + semicolon + newLine
        #     temp_m3d_pap += "DRIVER" + blankSpace + obj.electricCurrentDensity + blankSpace + obj.Label + \
        #                     ".JFUNC" + blankSpace + obj.Label + semicolon + newLine
        # else:
        #     temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + functionParameters + obj.function + semicolon + newLine
        #     temp_m3d_pap += "DRIVER" + blankSpace + obj.electricCurrentDensity + blankSpace + obj.Label + ".JFUNC" \
        #                 + blankSpace + obj.assignSource + semicolon + newLine
    elif obj.sourceType == "线电流源":
        objname = "LINE"
    elif obj.sourceType == "面电流源":
        objname = "AREA"
    elif obj.sourceType == "体电流源":
        objname = "VOLUME"
    else:
        objname = None
        Tools3D.sayz("错误")

    if obj.orthogonalProjectionPlane == "未指定":
        temp_m3d += objname + blankSpace + obj.Label + blankSpace + "CONFORMAL" + blankSpace
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj)
        temp_m3d += semicolon + newLine
        temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + functionParameters + obj.function + semicolon + newLine
        temp_m3d_pap += "DRIVER" + blankSpace + obj.electricCurrentDensity + blankSpace + obj.Label + \
                            ".JFUNC" + blankSpace + obj.Label + semicolon + newLine
    else:
        temp_m3d_pap += "FUNCTION" + blankSpace + obj.Label + functionParameters + obj.function + semicolon + newLine
        temp_m3d_pap += "DRIVER" + blankSpace + obj.electricCurrentDensity + blankSpace + obj.Label \
                            + ".JFUNC" + blankSpace + obj.orthogonalProjectionPlane + semicolon + newLine
    return temp_m3d, temp_m3d_pap


def Foil(obj):
    temp_m3d = ""
    temp_m3d_pap = ""
    temp_m3d_cp = ""
    if obj.isCheckCustom:
        material = obj.customMaterial
    elif obj.isCheckDefault:
        material = obj.defaultMaterial
        # 此处默认GOLD材料属性
        temp_m3d_cp += "MATERIAL GOLD ATOMIC_NUMBER 79 ATOMIC_MASS 196.967 MASS_DENSITY 1.e4;"+newLine+newLine
    else:
        # 如果进入此分支将是致命的错误
        print("材料选项输入错误")
        material = "材料选项输入错误"
    if obj.foilType == "未指定":
        temp_m3d += "VOLUME"+blankSpace+obj.Label+blankSpace+"CONFORMAL"+blankSpace
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj)
        temp_m3d += semicolon+newLine
        temp_m3d_pap += "FOIL"+blankSpace+material+blankSpace+obj.foilThickness+blankSpace+obj.Label+semicolon+newLine
    else:
        temp_m3d_pap += "FOIL"+blankSpace+obj.foilType+blankSpace+obj.foilThickness+blankSpace+material+semicolon+newLine
    return temp_m3d_cp, temp_m3d, temp_m3d_pap


def Inductor(obj):
    """
    该函数有两个返回值
    return1: temp_m3d -> ...
    return2: temp_m3d_pap -> ...
    """
    temp_m3d = ""
    temp_m3d_pap = ""
    if obj.inductorType == "未指定":
        temp_m3d += "LINE"+blankSpace+obj.Label+blankSpace+"CONFORMAL"+blankSpace
        temp_m3d += M3DShare.PointCoordinates().point1(obj)
        temp_m3d += M3DShare.PointCoordinates().point2(obj)
        temp_m3d += semicolon+newLine
        temp_m3d_pap += "INDUCTOR" + blankSpace + obj.Label + blankSpace + obj.coilDiameter
    else:
        temp_m3d_pap += "INDUCTOR" + blankSpace + obj.inductorType + blankSpace + obj.coilDiameter
    if obj.isCheckSelfInductor:
        temp_m3d_pap += blankSpace + "INDUCTANCE" + blankSpace + obj.selfInductorCoefficient + semicolon + newLine
    else:
        temp_m3d_pap += semicolon + newLine
    return temp_m3d, temp_m3d_pap


def NewMaterial(obj):
    """
        新型材料
        返回值：temp_m3d_cp
    """
    temp_m3d_cp = ""
    temp_m3d_cp += "MATERIAL" + blankSpace + obj.Label + blankSpace + "ATOMIC_NUMBER" + blankSpace + obj.atomicNumber + \
                blankSpace + "ATOMIC_MASS" + blankSpace + obj.atomicMassNumber + blankSpace + "MASS_DENSITY" + \
                blankSpace + obj.atomicDesity

    if obj.isconductivity:
        temp_m3d_cp += blankSpace + "CONDUCTIVITY" + blankSpace + obj.conductivity
    if obj.isdielectricConstant:
        temp_m3d_cp += blankSpace + "PERMITTIVITY" + blankSpace + obj.dielectricConstant

    temp_m3d_cp += semicolon + newLine
    return temp_m3d_cp


def MacParticle(obj):
    """
        宏粒子合并
        返回值：temp_m3d_ss
    """
    temp_m3d_ss = ""
    temp_m3d_ss += "MERGE" + blankSpace + "SPECIES" + blankSpace + obj.particleType + blankSpace + "MAXN_PERCELL" + \
                   blankSpace + obj.every + blankSpace + "MAXN_WHOLE" + blankSpace + obj.max + semicolon + newLine
    return temp_m3d_ss


def NewParticle(obj):
    """
        新型粒子
        返回值：temp_m3d_cp
    """
    temp_m3d_cp = ""
    temp_m3d_cp += "SPECIES" + blankSpace + obj.Label + blankSpace + "CHARGE" + blankSpace + obj.powerUnit + \
                   blankSpace + "MASS" + blankSpace + obj.mass + blankSpace + obj.protonMassUnit + semicolon + newLine
    return temp_m3d_cp


def Mark(obj):
    """
        Mark
        返回值：temp_m3d
    """
    temp_m3d = ""
    temp_m3d += "MARK" + blankSpace + obj.markObject + blankSpace + obj.direction + blankSpace
    if obj.isMINIMUM:
        temp_m3d += "MINIMUM" + blankSpace
    if obj.isMIDPOINT:
        temp_m3d += "MIDPOINT" + blankSpace
    if obj.isMAXIMUM:
        temp_m3d += "MAXIMUM" + blankSpace
    temp_m3d += "SIZE" + blankSpace + obj.size + semicolon + newLine
    return temp_m3d
