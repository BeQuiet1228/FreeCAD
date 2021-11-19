# -*- coding: UTF-8 -*-
###################################################################
# author: maxin
# describe: 对不同操作所需要更新的命令组进行组合
###################################################################

from CHIPICCommand import *
import FreeCAD
# import Modeling.Common.Tools.ObjectsTools



NEWLINE = "\n"

class CoordinateSystem(Enum):
    rectangularSys = "R"
    polarSys = "P"
    cylindricalSys = "C"
    rectangular4 = "(T,X,Y,Z)"
    polar4 = "(T,R,P,Z)"
    cylindrical4 = "(T,Z,R,P)"
    rectangular3 = "(X,Y,Z)"
    polar3 = "(R,P,Z)"
    cylindrical3 = "(Z,R,P)"


def isNum(var):
    # 判断是否是数字类型
    if isinstance(var, int) or isinstance(var, long) or isinstance(var, float) or isinstance(var, complex):
        return True
    else:
        return False
def isNumber(n):
    # 判断是否为数字 @lizhenguang
    result=True
    try:
        num=float(n)
        result = num == num
    except :
        result=False
    return result
def isNumjustforTimeStep(n):
    '''
    这个函数是单独为时间步长设置的，仅用作测试，不建议使用
    '''
    for i in n:
        if i in'0123456789.':
            pass
        else:
            return False
    return True



def isBool(var):
    # 判断是否是bool类型
    if isinstance(var, bool):
        return True
    else:
        return False


def isList(var):
    # 判断是否是list类型
    if isinstance(var, list):
        return True
    else:
        return False


def getHeaderCommands(organization, author, device, remarks):

    """
    
    :param organization: 机构
    :param author: 作者
    :param device: 模型
    :param remarks: 备注
    :return: 
    """

    headerOrganization = Header(Header.Parameter.organization, organization)
    headerAuthor = Header(Header.Parameter.author, author)
    headerDevice = Header(Header.Parameter.device, device)
    headerRemarks = Header(Header.Parameter.remarks, remarks)

    returnStr = NEWLINE + headerOrganization.getNotes() + \
                NEWLINE + headerOrganization.getHeaderStr() + \
                NEWLINE + headerAuthor.getHeaderStr() + \
                NEWLINE + headerDevice.getHeaderStr() + \
                NEWLINE + headerRemarks.getHeaderStr() + \
                NEWLINE

    return returnStr


def getSystemCommands(coordinateSystem):

    """
    :param coordinateSystem: 当前坐标系
    :return: 
    """

    returnStr = ""

    if coordinateSystem == "R":
        system = System(System.Type.cartesian)
        returnStr = NEWLINE + system.getNotes() + NEWLINE + system.getSystemStr() + NEWLINE
    elif coordinateSystem == "P":
        system = System(System.Type.polar)
        returnStr = NEWLINE + system.getNotes() + NEWLINE + system.getSystemStr() + NEWLINE
    elif coordinateSystem == "C":
        system = System(System.Type.cylindrical)
        returnStr = NEWLINE + system.getNotes() + NEWLINE + system.getSystemStr() + NEWLINE
    else:
        return "System命令生成，请检查coordinateSystem"

    return returnStr


def getParameterCommands(name, val):
    """
    :param name: 参数名
    :param content: 参数值
    :return: 
    """
    # FreeCAD.Console.PrintMessage("LOG 1")
    #表示为注释
    if val=="!COMMENT":
        return NEWLINE + name  + NEWLINE
    if isNum(val):
        val = val.__str__()

    return NEWLINE + name + " = " + val + ";" + NEWLINE


def getPointCommands(ponitName, coordinates):
    "ponitName为点名称，coordinates点坐标列表"

    # 生成对应的注释
    pointCommandsStr = newline + "!!" + ponitName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(coordinates):
        return "point命令生成：请检查coordinates是否为list类型"

    for index in range(len(coordinates)):
        if isNum(coordinates[index]):
            coordinates[index] = coordinates[index].__str__()
    ## 生成具体命令
    point = Point(ponitName, coordinates)
    pointCommandsStr = pointCommandsStr + point.getPonitStr() + NEWLINE

    return pointCommandsStr
# 专为阵列体准备的函数，但是我并不认为它会被调用
def Array_getPointCommands(ponitName, coordinates):
    "ponitName为点名称，coordinates点坐标列表"

    # 生成对应的注释
    pointCommandsStr = newline + "!!" + ponitName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(coordinates):
        return "point命令生成：请检查coordinates是否为list类型"

    for index in range(len(coordinates)):
        if isNum(coordinates[index]):
            coordinates[index] = coordinates[index].__str__()
    ## 生成具体命令
    point = Array_Point(ponitName, coordinates)
    pointCommandsStr = pointCommandsStr + point.getPonitStr() + NEWLINE

    return pointCommandsStr

def getLineCommands(lineName, lineType, startPointCoordinates, stopPointCoordinates):
    "lineName为线名称，lineType为线类型(CONFORMAL)，startPointCoordinates、stopPointCoordinates点坐标列表"

    # 生成对应的注释
    lineCommandsStr = NEWLINE + "!!" + lineName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(startPointCoordinates):
        return "line命令生成：请检查startPointCoordinates是否为list类型"

    if not isList(stopPointCoordinates):
        return "line命令生成：请检查stopPointCoordinates是否为list类型"

    ## 对lineType是否为符合规范的常量进行判断
    if lineType!=Line.Type.conformal:
        return "line命令生成：请检查lineType"

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    for index in range(len(stopPointCoordinates)):
        if isNum(stopPointCoordinates[index]):
            stopPointCoordinates[index] = stopPointCoordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    startPointName = lineName+".LO"
    startPoint = Point(startPointName, startPointCoordinates)
    lineCommandsStr = lineCommandsStr + startPoint.getPonitStr() + NEWLINE

    stopPointName = lineName + ".HI"
    stopPoint = Point(stopPointName, stopPointCoordinates)
    lineCommandsStr = lineCommandsStr + stopPoint.getPonitStr() + NEWLINE

    ###生成线命令
    line = Line(lineName, lineType, [startPointName, stopPointName])
    lineCommandsStr = lineCommandsStr + line.getLineStr() + NEWLINE

    return lineCommandsStr

# 专为阵列体准备的函数，但我并不认为它会被调用
def Array_getLineCommands(lineName, lineType, startPointCoordinates, stopPointCoordinates):
    "lineName为线名称，lineType为线类型(CONFORMAL)，startPointCoordinates、stopPointCoordinates点坐标列表"

    # 生成对应的注释
    lineCommandsStr = NEWLINE + "!!" + lineName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(startPointCoordinates):
        return "line命令生成：请检查startPointCoordinates是否为list类型"

    if not isList(stopPointCoordinates):
        return "line命令生成：请检查stopPointCoordinates是否为list类型"

    ## 对lineType是否为符合规范的常量进行判断
    if lineType!=Line.Type.conformal:
        return "line命令生成：请检查lineType"

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    for index in range(len(stopPointCoordinates)):
        if isNum(stopPointCoordinates[index]):
            stopPointCoordinates[index] = stopPointCoordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    startPointName = lineName+".LO"
    startPoint = Array_Point(startPointName, startPointCoordinates)
    lineCommandsStr = lineCommandsStr + startPoint.getPonitStr() + NEWLINE

    stopPointName = lineName + ".HI"
    stopPoint = Array_Point(stopPointName, stopPointCoordinates)
    lineCommandsStr = lineCommandsStr + stopPoint.getPonitStr() + NEWLINE

    ###生成线命令
    line = Line(lineName, lineType, [startPointName, stopPointName])
    lineCommandsStr = lineCommandsStr + line.getLineStr() + NEWLINE

    return lineCommandsStr


def getObliqueLineCommands(lineName, startPointCoordinates, stopPointCoordinates):
    "lineName为线名称，startPointCoordinates、stopPointCoordinates点坐标列表,baseradius半径"

    # 生成对应的注释
    lineCommandsStr = NEWLINE + "!!" + lineName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(startPointCoordinates):
        return "line命令生成：请检查startPointCoordinates是否为list类型"

    if not isList(stopPointCoordinates):
        return "line命令生成：请检查stopPointCoordinates是否为list类型"

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    for index in range(len(stopPointCoordinates)):
        if isNum(stopPointCoordinates[index]):
            stopPointCoordinates[index] = stopPointCoordinates[index].__str__()

    # if isNum(baseradius):
    #     baseradius = baseradius.__str__()

    ## 生成具体命令
    ### 生成点命令
    startPointName = lineName+".LO"
    startPoint = Point(startPointName, startPointCoordinates)
    lineCommandsStr = lineCommandsStr + startPoint.getPonitStr() + NEWLINE

    stopPointName = lineName + ".HI"
    stopPoint = Point(stopPointName, stopPointCoordinates)
    lineCommandsStr = lineCommandsStr + stopPoint.getPonitStr() + NEWLINE

    ###生成线命令
    lineType = Line.Type.oblique
    line = Line(lineName, lineType, [startPointName, stopPointName])
    lineCommandsStr = lineCommandsStr + line.getLineStr() + NEWLINE

    return lineCommandsStr

# 专为阵列体准备的函数
def Array_getObliqueLineCommands(lineName, startPointCoordinates, stopPointCoordinates):
    "lineName为线名称，startPointCoordinates、stopPointCoordinates点坐标列表,baseradius半径"

    # 生成对应的注释
    lineCommandsStr = NEWLINE + "!!" + lineName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(startPointCoordinates):
        return "line命令生成：请检查startPointCoordinates是否为list类型"

    if not isList(stopPointCoordinates):
        return "line命令生成：请检查stopPointCoordinates是否为list类型"

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    for index in range(len(stopPointCoordinates)):
        if isNum(stopPointCoordinates[index]):
            stopPointCoordinates[index] = stopPointCoordinates[index].__str__()

    # if isNum(baseradius):
    #     baseradius = baseradius.__str__()

    ## 生成具体命令
    ### 生成点命令
    startPointName = lineName+".LO"
    startPoint = Array_Point(startPointName, startPointCoordinates)
    lineCommandsStr = lineCommandsStr + startPoint.getPonitStr() + NEWLINE

    stopPointName = lineName + ".HI"
    stopPoint = Array_Point(stopPointName, stopPointCoordinates)
    lineCommandsStr = lineCommandsStr + stopPoint.getPonitStr() + NEWLINE

    ###生成线命令
    lineType = Line.Type.oblique
    line = Line(lineName, lineType, [startPointName, stopPointName])
    lineCommandsStr = lineCommandsStr + line.getLineStr() + NEWLINE

    return lineCommandsStr

def getAreaCommands(areaName, areaType, startPointCoordinates, stopPointCoordinates,explanatoryName=""):
    "areaName为面名称，areaType为面类型，startPointCoordinates、stopPointCoordinates点坐标列表，后续还需要兼容新的面类型"
    if explanatoryName=="":
        explanatoryName=areaName
    # 生成对应的注释
    areaCommandsStr = NEWLINE + "!!" + explanatoryName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(startPointCoordinates):
        return "area命令生成：请检查startPointCoordinates是否为list类型"

    if not isList(stopPointCoordinates):
        return "area命令生成：请检查stopPointCoordinates是否为list类型"

    if areaType != Area.Shape.conformal and areaType != Area.Shape.functional and \
        areaType != Area.Shape.rectangular:
        return "area命令生成：请检查areaType"

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    for index in range(len(stopPointCoordinates)):
        if isNum(stopPointCoordinates[index]):
            stopPointCoordinates[index] = stopPointCoordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    startPointName = areaName + ".LO"
    startPoint = Point(startPointName, startPointCoordinates)
    areaCommandsStr = areaCommandsStr + startPoint.getPonitStr() + NEWLINE

    stopPointName = areaName + ".HI"
    stopPoint = Point(stopPointName, stopPointCoordinates)
    areaCommandsStr = areaCommandsStr + stopPoint.getPonitStr() + NEWLINE

    ###生成面命令
    area = Area(areaName, areaType, [startPointName, stopPointName])
    areaCommandsStr = areaCommandsStr + area.getAreaStr() + NEWLINE

    return areaCommandsStr

# 专为阵列体准备的函数
def Array_getAreaCommands(areaName, areaType, startPointCoordinates, stopPointCoordinates,explanatoryName=""):
    "areaName为面名称，areaType为面类型，startPointCoordinates、stopPointCoordinates点坐标列表，后续还需要兼容新的面类型"
    if explanatoryName=="":
        explanatoryName=areaName
    # 生成对应的注释
    areaCommandsStr = NEWLINE + "!!" + explanatoryName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(startPointCoordinates):
        return "area命令生成：请检查startPointCoordinates是否为list类型"

    if not isList(stopPointCoordinates):
        return "area命令生成：请检查stopPointCoordinates是否为list类型"

    if areaType != Area.Shape.conformal and areaType != Area.Shape.functional and \
        areaType != Area.Shape.rectangular:
        return "area命令生成：请检查areaType"

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    for index in range(len(stopPointCoordinates)):
        if isNum(stopPointCoordinates[index]):
            stopPointCoordinates[index] = stopPointCoordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    startPointName = areaName + ".LO"
    startPoint = Array_Point(startPointName, startPointCoordinates)
    areaCommandsStr = areaCommandsStr + startPoint.getPonitStr() + NEWLINE

    stopPointName = areaName + ".HI"
    stopPoint = Array_Point(stopPointName, stopPointCoordinates)
    areaCommandsStr = areaCommandsStr + stopPoint.getPonitStr() + NEWLINE

    ###生成面命令
    area = Area(areaName, areaType, [startPointName, stopPointName])
    areaCommandsStr = areaCommandsStr + area.getAreaStr() + NEWLINE

    return areaCommandsStr


def getPolygonalAreaCommands(areaName, pointCoordinatesList):
    "areaName为多边形面名称，pointCoordinatesList点坐标列表"

    # 生成对应的注释
    areaCommandsStr = NEWLINE + "!!" + areaName + NEWLINE

    # 用来存放point名字
    pointNameList = []

    # i用来标记点的名字
    i = 1
    for pointCoordinates in pointCoordinatesList:

        # 生成命令
        ## 对坐标点的数据类型进行判断
        if not isList(pointCoordinates):
            return "ConformalVolume命令生成：请检查nearPointCoordinates是否为list类型"

        for index in range(len(pointCoordinates)):
            if isNum(pointCoordinates[index]):
                pointCoordinates[index] = pointCoordinates[index].__str__()

        ## 生成具体命令
        ### 生成点命令
        pointName = areaName + ".P" + str(i)
        point = Point(pointName, pointCoordinates)
        areaCommandsStr = areaCommandsStr + point.getPonitStr() + NEWLINE
        pointNameList.append(pointName)

        # 点的名字递增
        i = i + 1

    ###生成面命令
    areaType = Area.Shape.polygonal
    area = Area(areaName, areaType, pointNameList)
    areaCommandsStr = areaCommandsStr + area.getAreaStr() + NEWLINE

    return areaCommandsStr

# 专为阵列体准备的函数
def Array_getPolygonalAreaCommands(areaName, pointCoordinatesList):
    "areaName为多边形面名称，pointCoordinatesList点坐标列表"

    # 生成对应的注释
    areaCommandsStr = NEWLINE + "!!" + areaName + NEWLINE

    # 用来存放point名字
    pointNameList = []

    # i用来标记点的名字
    i = 1
    for pointCoordinates in pointCoordinatesList:

        # 生成命令
        ## 对坐标点的数据类型进行判断
        if not isList(pointCoordinates):
            return "ConformalVolume命令生成：请检查nearPointCoordinates是否为list类型"

        for index in range(len(pointCoordinates)):
            if isNum(pointCoordinates[index]):
                pointCoordinates[index] = pointCoordinates[index].__str__()

        ## 生成具体命令
        ### 生成点命令
        pointName = areaName + ".P" + str(i)
        point = Array_Point(pointName, pointCoordinates)
        areaCommandsStr = areaCommandsStr + point.getPonitStr() + NEWLINE
        pointNameList.append(pointName)

        # 点的名字递增
        i = i + 1

    ###生成面命令
    areaType = Area.Shape.polygonal
    area = Area(areaName, areaType, pointNameList)
    areaCommandsStr = areaCommandsStr + area.getAreaStr() + NEWLINE

    return areaCommandsStr


def getConformalVolumeCommands(volumeName, nearPointCoordinates, farPointCoordinates):
    "volumeName为投影体名称，volumeType为CONFORMAL类型，nearPointCoordinates、farPointCoordinates点坐标列表"

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(nearPointCoordinates):
        return "ConformalVolume命令生成：请检查nearPointCoordinates是否为list类型"

    if not isList(farPointCoordinates):
        return "ConformalVolume命令生成：请检查farPointCoordinates是否为list类型"

    for index in range(len(nearPointCoordinates)):
        if isNum(nearPointCoordinates[index]):
            nearPointCoordinates[index] = nearPointCoordinates[index].__str__()

    for index in range(len(farPointCoordinates)):
        if isNum(farPointCoordinates[index]):
            farPointCoordinates[index] = farPointCoordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    nearPointName = volumeName + ".LO"
    nearPoint =Point(nearPointName, nearPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + nearPoint.getPonitStr() + NEWLINE

    farPointName = volumeName + ".HI"
    farPoint = Point(farPointName, farPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + farPoint.getPonitStr() + NEWLINE

    ###生成线命令
    volumeType = Volume.Shape.conformal
    volume = Volume(volumeName, volumeType, [nearPointName, farPointName])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr
# 专为阵列体单独生成的函数
def Array_getConformalVolumeCommands(volumeName, nearPointCoordinates, farPointCoordinates):
    "volumeName为投影体名称，volumeType为CONFORMAL类型，nearPointCoordinates、farPointCoordinates点坐标列表"

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(nearPointCoordinates):
        return "ConformalVolume命令生成：请检查nearPointCoordinates是否为list类型"

    if not isList(farPointCoordinates):
        return "ConformalVolume命令生成：请检查farPointCoordinates是否为list类型"

    for index in range(len(nearPointCoordinates)):
        if isNum(nearPointCoordinates[index]):
            nearPointCoordinates[index] = nearPointCoordinates[index].__str__()

    for index in range(len(farPointCoordinates)):
        if isNum(farPointCoordinates[index]):
            farPointCoordinates[index] = farPointCoordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    nearPointName = volumeName + ".CLO"
    nearPoint =Array_Point(nearPointName, nearPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + nearPoint.getPonitStr() + NEWLINE
    #FreeCAD.Console.PrintError(volumeCommandsStr)

    farPointName = volumeName + ".CHI"
    farPoint = Array_Point(farPointName, farPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + farPoint.getPonitStr() + NEWLINE

    ###生成线命令
    volumeType = Volume.Shape.conformal
    volume = Volume(volumeName, volumeType, [nearPointName, farPointName])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    # temp_zhushi 
    #FreeCAD.Console.PrintError(volumeCommandsStr)

    return volumeCommandsStr

def getConeVolumeCommands(volumeName, basePointCoordinates, topPointCoordinates, baseradius, topradius):
    "volumeName为圆锥名称，volumeType为CONE类型，basePointCoordinates、topPointCoordinates点坐标列表,baseradius为底半径，topradius为顶半径"

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(basePointCoordinates):
        return "ConeVolume命令生成：请检查basePointCoordinates是否为list类型"

    if not isList(topPointCoordinates):
        return "ConeVolume命令生成：请检查topPointCoordinates是否为list类型"

    for index in range(len(basePointCoordinates)):
        if isNum(basePointCoordinates[index]):
            basePointCoordinates[index] = basePointCoordinates[index].__str__()

    for index in range(len(topPointCoordinates)):
        if isNum(topPointCoordinates[index]):
            topPointCoordinates[index] = topPointCoordinates[index].__str__()

    if isNum(baseradius):
        baseradius = baseradius.__str__()

    if isNum(topradius):
        topradius = topradius.__str__()


    ## 生成具体命令
    ### 生成点命令
    basePointName = volumeName + ".P1"
    basePoint = Point(basePointName, basePointCoordinates)
    volumeCommandsStr = volumeCommandsStr + basePoint.getPonitStr() + NEWLINE

    topPointName = volumeName + ".P2"
    topPoint = Point(topPointName, topPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + topPoint.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.cone
    volume = Volume(volumeName, volumeType, [basePointName, topPointName, baseradius, topradius])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getConeVolumeCommands(volumeName, basePointCoordinates, topPointCoordinates, baseradius, topradius):
    "volumeName为圆锥名称，volumeType为CONE类型，basePointCoordinates、topPointCoordinates点坐标列表,baseradius为底半径，topradius为顶半径"

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(basePointCoordinates):
        return "ConeVolume命令生成：请检查basePointCoordinates是否为list类型"

    if not isList(topPointCoordinates):
        return "ConeVolume命令生成：请检查topPointCoordinates是否为list类型"

    for index in range(len(basePointCoordinates)):
        if isNum(basePointCoordinates[index]):
            basePointCoordinates[index] = basePointCoordinates[index].__str__()

    for index in range(len(topPointCoordinates)):
        if isNum(topPointCoordinates[index]):
            topPointCoordinates[index] = topPointCoordinates[index].__str__()

    if isNum(baseradius):
        baseradius = baseradius.__str__()

    if isNum(topradius):
        topradius = topradius.__str__()


    ## 生成具体命令
    ### 生成点命令
    basePointName = volumeName + ".P1"
    basePoint = Array_Point(basePointName, basePointCoordinates)
    volumeCommandsStr = volumeCommandsStr + basePoint.getPonitStr() + NEWLINE

    topPointName = volumeName + ".P2"
    topPoint = Array_Point(topPointName, topPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + topPoint.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.cone
    volume = Volume(volumeName, volumeType, [basePointName, topPointName, baseradius, topradius])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getCylindricalVolumeCommands(volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radius):
    """
    volumeType为CYLINDRICAL类型
    :param volumeName: 名称
    :param centerPoint1Coordinates: 中心点1坐标列表
    :param centerPoint2Coordinates: 中心点2坐标列表
    :param radius: 半径
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(centerPoint1Coordinates):
        return "CylindricalVolume命令生成：请检查centerPoint1Coordinates是否为list类型"

    if not isList(centerPoint2Coordinates):
        return "CylindricalVolume命令生成：请检查centerPoint2Coordinates是否为list类型"

    for index in range(len(centerPoint1Coordinates)):
        if isNum(centerPoint1Coordinates[index]):
            centerPoint1Coordinates[index] = centerPoint1Coordinates[index].__str__()

    for index in range(len(centerPoint2Coordinates)):
        if isNum(centerPoint2Coordinates[index]):
            centerPoint2Coordinates[index] = centerPoint2Coordinates[index].__str__()

    if isNum(radius):
        radius = radius.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, centerPoint1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, centerPoint2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.cylindrical
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radius])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def Array_getCylindricalVolumeCommands(volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radius):
    """
    volumeType为CYLINDRICAL类型
    :param volumeName: 名称
    :param centerPoint1Coordinates: 中心点1坐标列表
    :param centerPoint2Coordinates: 中心点2坐标列表
    :param radius: 半径
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(centerPoint1Coordinates):
        return "CylindricalVolume命令生成：请检查centerPoint1Coordinates是否为list类型"

    if not isList(centerPoint2Coordinates):
        return "CylindricalVolume命令生成：请检查centerPoint2Coordinates是否为list类型"

    for index in range(len(centerPoint1Coordinates)):
        if isNum(centerPoint1Coordinates[index]):
            centerPoint1Coordinates[index] = centerPoint1Coordinates[index].__str__()

    for index in range(len(centerPoint2Coordinates)):
        if isNum(centerPoint2Coordinates[index]):
            centerPoint2Coordinates[index] = centerPoint2Coordinates[index].__str__()

    if isNum(radius):
        radius = radius.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, centerPoint1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, centerPoint2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.cylindrical
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radius])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr



def getAnnularVolumeCommands(volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radiusInner, radiusOuter):
    """
    volumeType为Annular类型
    :param volumeName: 名称
    :param centerPoint1Coordinates: 中心点1坐标列表
    :param centerPoint2Coordinates: 中心点2坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(centerPoint1Coordinates):
        return "AnnularVolume命令生成：请检查centerPoint1Coordinates是否为list类型"

    if not isList(centerPoint2Coordinates):
        return "AnnularVolume命令生成：请检查centerPoint2Coordinates是否为list类型"

    for index in range(len(centerPoint1Coordinates)):
        if isNum(centerPoint1Coordinates[index]):
            centerPoint1Coordinates[index] = centerPoint1Coordinates[index].__str__()

    for index in range(len(centerPoint2Coordinates)):
        if isNum(centerPoint2Coordinates[index]):
            centerPoint2Coordinates[index] = centerPoint2Coordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, centerPoint1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, centerPoint2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.annular
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getAnnularVolumeCommands(volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radiusInner, radiusOuter):
    """
    volumeType为Annular类型
    :param volumeName: 名称
    :param centerPoint1Coordinates: 中心点1坐标列表
    :param centerPoint2Coordinates: 中心点2坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(centerPoint1Coordinates):
        return "AnnularVolume命令生成：请检查centerPoint1Coordinates是否为list类型"

    if not isList(centerPoint2Coordinates):
        return "AnnularVolume命令生成：请检查centerPoint2Coordinates是否为list类型"

    for index in range(len(centerPoint1Coordinates)):
        if isNum(centerPoint1Coordinates[index]):
            centerPoint1Coordinates[index] = centerPoint1Coordinates[index].__str__()

    for index in range(len(centerPoint2Coordinates)):
        if isNum(centerPoint2Coordinates[index]):
            centerPoint2Coordinates[index] = centerPoint2Coordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, centerPoint1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, centerPoint2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.annular
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getAnnularSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                    point3Coordinates, point4Coordinates):
    """
    volumeType为AnnularSection类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "AnnularSectionVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "AnnularSectionVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "AnnularSectionVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "AnnularSectionVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.annularSection
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getAnnularSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                    point3Coordinates, point4Coordinates):
    """
    volumeType为AnnularSection类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "AnnularSectionVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "AnnularSectionVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "AnnularSectionVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "AnnularSectionVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Array_Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Array_Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.annularSection
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr


def getParallelepipedalVolumeCommands(volumeName, point1Coordinates, point2Coordinates,
                                    point3Coordinates, point4Coordinates):
    """
    volumeType为Parallelepipedal类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P0"
    point1 = Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P1"
    point2 = Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P2"
    point3 = Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P3"
    point4 = Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.parallelepipedal
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成
def Array_getParallelepipedalVolumeCommands(volumeName, point1Coordinates, point2Coordinates,
                                    point3Coordinates, point4Coordinates):
    """
    volumeType为Parallelepipedal类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "ParallelepipedalVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P0"
    point1 = Array_Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P1"
    point2 = Array_Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P2"
    point3 = Array_Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P3"
    point4 = Array_Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.parallelepipedal
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getSphericalVolumeCommands(volumeName, pointCoordinates, radius):
    """
    volumeType为Spherical类型
    :param volumeName: 名称
    :param pointCoordinates: 点1坐标列表
    :param radius: 内半径
    :return: 
    """

    FreeCAD.Console.PrintMessage("Opening")

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(pointCoordinates):
        return "AnnularSectionVolume命令生成：请检查pointCoordinates是否为list类型"

    for index in range(len(pointCoordinates)):
        if isNum(pointCoordinates[index]):
            pointCoordinates[index] = pointCoordinates[index].__str__()

    if isNum(radius):
        radius = radius.__str__()

    ## 生成具体命令
    ### 生成点命令
    pointName = volumeName + ".P"
    # FreeCAD.Console.PrintMessage(pointName[-2:])
    point = Point(pointName, pointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point.getPonitStr() + NEWLINE


    ###生成体命令
    volumeType = Volume.Shape.spherical
    volume = Volume(volumeName, volumeType, [pointName, radius])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getSphericalVolumeCommands(volumeName, pointCoordinates, radius):
    """
    volumeType为Spherical类型
    :param volumeName: 名称
    :param pointCoordinates: 点1坐标列表
    :param radius: 内半径
    :return:
    """

    FreeCAD.Console.PrintMessage("Opening")

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(pointCoordinates):
        return "AnnularSectionVolume命令生成：请检查pointCoordinates是否为list类型"

    for index in range(len(pointCoordinates)):
        if isNum(pointCoordinates[index]):
            pointCoordinates[index] = pointCoordinates[index].__str__()

    if isNum(radius):
        radius = radius.__str__()

    ## 生成具体命令
    ### 生成点命令
    pointName = volumeName + ".P"
    # FreeCAD.Console.PrintMessage(pointName[-2:])
    point = Array_Point(pointName, pointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point.getPonitStr() + NEWLINE


    ###生成体命令
    volumeType = Volume.Shape.spherical
    volume = Volume(volumeName, volumeType, [pointName, radius])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getWedgeVolumeCommands(volumeName, point1Coordinates, point2Coordinates,point3Coordinates, point4Coordinates,
                                    point5Coordinates, point6Coordinates):
    """
    volumeType为Wedge类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :param point5Coordinates: 点5坐标列表
    :param point6Coordinates: 点6坐标列表
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "WedgeVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "WedgeVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "WedgeVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "WedgeVolume命令生成：请检查point4Coordinates是否为list类型"

    if not isList(point5Coordinates):
        return "WedgeVolume命令生成：请检查point5Coordinates是否为list类型"

    if not isList(point6Coordinates):
        return "WedgeVolume命令生成：请检查point6Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    for index in range(len(point5Coordinates)):
        if isNum(point5Coordinates[index]):
            point5Coordinates[index] = point5Coordinates[index].__str__()

    for index in range(len(point6Coordinates)):
        if isNum(point6Coordinates[index]):
            point6Coordinates[index] = point6Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    point5Name = volumeName + ".P5"
    point5 = Point(point5Name, point5Coordinates)
    volumeCommandsStr = volumeCommandsStr + point5.getPonitStr() + NEWLINE

    point6Name = volumeName + ".P6"
    point6 = Point(point6Name, point6Coordinates)
    volumeCommandsStr = volumeCommandsStr + point6.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.wedge
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name, point5Name, point6Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

#专为阵列体准备的函数
def Array_getWedgeVolumeCommands(volumeName, point1Coordinates, point2Coordinates,point3Coordinates, point4Coordinates,
                                    point5Coordinates, point6Coordinates):
    """
    volumeType为Wedge类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :param point5Coordinates: 点5坐标列表
    :param point6Coordinates: 点6坐标列表
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "WedgeVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "WedgeVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "WedgeVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "WedgeVolume命令生成：请检查point4Coordinates是否为list类型"

    if not isList(point5Coordinates):
        return "WedgeVolume命令生成：请检查point5Coordinates是否为list类型"

    if not isList(point6Coordinates):
        return "WedgeVolume命令生成：请检查point6Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    for index in range(len(point5Coordinates)):
        if isNum(point5Coordinates[index]):
            point5Coordinates[index] = point5Coordinates[index].__str__()

    for index in range(len(point6Coordinates)):
        if isNum(point6Coordinates[index]):
            point6Coordinates[index] = point6Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Array_Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Array_Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    point5Name = volumeName + ".P5"
    point5 = Array_Point(point5Name, point5Coordinates)
    volumeCommandsStr = volumeCommandsStr + point5.getPonitStr() + NEWLINE

    point6Name = volumeName + ".P6"
    point6 = Array_Point(point6Name, point6Coordinates)
    volumeCommandsStr = volumeCommandsStr + point6.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.wedge
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name, point5Name, point6Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getTetrahedronVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates):
    """
    volumeType为tetrahedron类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "TetrahedronVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "TetrahedronVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "TetrahedronVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "TetrahedronVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.tetrahedron
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 负责旋转体生成的函数
def getRotateVolumeCommands(volumeName,Point1Coordinates,Point2Coordinates,Area):
    """
    :param volumeName:名称
    :param Point1Coordinates:Axis_Base_Point坐标
    :param Point2Coordinates: Axis_Top_Point坐标
    :param Area: 面名
    :return:
    """
    # 生成的对应注释
    volumeCommandsStr = NEWLINE + "!!" +volumeName+NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(Point1Coordinates):
        return "TetrahedronVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(Point2Coordinates):
        return "TetrahedronVolume命令生成：请检查point2Coordinates是否为list类型"

    for index in range(len(Point1Coordinates)):
        if isNum(Point1Coordinates[index]):
            Point1Coordinates[index] = Point1Coordinates[index].__str__()

    for index in range(len(Point2Coordinates)):
        if isNum(Point2Coordinates[index]):
            Point2Coordinates[index] = Point2Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".LO"
    point1 = Point(point1Name, Point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".HI"
    point2 = Point(point2Name, Point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE


    ###生成体命令
    volumeType = Volume.Shape.rotate
    volume = Volume(volumeName, volumeType, [point1Name, point2Name,Area])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getTetrahedronVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates):
    """
    volumeType为tetrahedron类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "TetrahedronVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "TetrahedronVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "TetrahedronVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "TetrahedronVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Array_Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Array_Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.tetrahedron
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr


def getPyramidVolumeCommands(volumeName, point1Coordinates, point2Coordinates,point3Coordinates, point4Coordinates,
                                    point5Coordinates):
    """
    volumeType为Pyramid类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :param point5Coordinates: 点5坐标列表
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "PyramidVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "PyramidVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "PyramidVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "PyramidVolume命令生成：请检查point4Coordinates是否为list类型"

    if not isList(point5Coordinates):
        return "PyramidVolume命令生成：请检查point5Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    for index in range(len(point5Coordinates)):
        if isNum(point5Coordinates[index]):
            point5Coordinates[index] = point5Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    point5Name = volumeName + ".P5"
    point5 = Point(point5Name, point5Coordinates)
    volumeCommandsStr = volumeCommandsStr + point5.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.pyramid
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name, point5Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getPyramidVolumeCommands(volumeName, point1Coordinates, point2Coordinates,point3Coordinates, point4Coordinates,
                                    point5Coordinates):
    """
    volumeType为Pyramid类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :param point5Coordinates: 点5坐标列表
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "PyramidVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "PyramidVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "PyramidVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "PyramidVolume命令生成：请检查point4Coordinates是否为list类型"

    if not isList(point5Coordinates):
        return "PyramidVolume命令生成：请检查point5Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    for index in range(len(point5Coordinates)):
        if isNum(point5Coordinates[index]):
            point5Coordinates[index] = point5Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Array_Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Array_Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    point5Name = volumeName + ".P5"
    point5 = Array_Point(point5Name, point5Coordinates)
    volumeCommandsStr = volumeCommandsStr + point5.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.pyramid
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name, point5Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getRhombusVolumeCommands(volumeName, point1Coordinates, point2Coordinates,point3Coordinates, point4Coordinates,
                                    point5Coordinates, point6Coordinates, point7Coordinates, point8Coordinates):
    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "RhombusVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "RhombusVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "RhombusVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "RhombusVolume命令生成：请检查point4Coordinates是否为list类型"

    if not isList(point5Coordinates):
        return "RhombusVolume命令生成：请检查point5Coordinates是否为list类型"
    
    if not isList(point6Coordinates):
        return "RhombusVolume命令生成：请检查point6Coordinates是否为list类型"

    if not isList(point7Coordinates):
        return "RhombusVolume命令生成：请检查point7Coordinates是否为list类型"

    if not isList(point8Coordinates):
        return "RhombusVolume命令生成：请检查point8Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    for index in range(len(point5Coordinates)):
        if isNum(point5Coordinates[index]):
            point5Coordinates[index] = point5Coordinates[index].__str__()
            
    for index in range(len(point6Coordinates)):
        if isNum(point6Coordinates[index]):
            point6Coordinates[index] = point6Coordinates[index].__str__()

    for index in range(len(point7Coordinates)):
        if isNum(point7Coordinates[index]):
            point7Coordinates[index] = point7Coordinates[index].__str__()

    for index in range(len(point8Coordinates)):
        if isNum(point8Coordinates[index]):
            point8Coordinates[index] = point8Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    point5Name = volumeName + ".P5"
    point5 = Point(point5Name, point5Coordinates)
    volumeCommandsStr = volumeCommandsStr + point5.getPonitStr() + NEWLINE

    point6Name = volumeName + ".P6"
    point6 = Point(point6Name, point6Coordinates)
    volumeCommandsStr = volumeCommandsStr + point6.getPonitStr() + NEWLINE

    point7Name = volumeName + ".P7"
    point7 = Point(point7Name, point7Coordinates)
    volumeCommandsStr = volumeCommandsStr + point7.getPonitStr() + NEWLINE

    point8Name = volumeName + ".P8"
    point8 = Point(point8Name, point8Coordinates)
    volumeCommandsStr = volumeCommandsStr + point8.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.rhombus
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name,
                                             point5Name, point6Name, point7Name, point8Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getRhombusVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                             point5Coordinates, point6Coordinates, point7Coordinates, point8Coordinates):
    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "RhombusVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "RhombusVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "RhombusVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "RhombusVolume命令生成：请检查point4Coordinates是否为list类型"

    if not isList(point5Coordinates):
        return "RhombusVolume命令生成：请检查point5Coordinates是否为list类型"

    if not isList(point6Coordinates):
        return "RhombusVolume命令生成：请检查point6Coordinates是否为list类型"

    if not isList(point7Coordinates):
        return "RhombusVolume命令生成：请检查point7Coordinates是否为list类型"

    if not isList(point8Coordinates):
        return "RhombusVolume命令生成：请检查point8Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    for index in range(len(point5Coordinates)):
        if isNum(point5Coordinates[index]):
            point5Coordinates[index] = point5Coordinates[index].__str__()

    for index in range(len(point6Coordinates)):
        if isNum(point6Coordinates[index]):
            point6Coordinates[index] = point6Coordinates[index].__str__()

    for index in range(len(point7Coordinates)):
        if isNum(point7Coordinates[index]):
            point7Coordinates[index] = point7Coordinates[index].__str__()

    for index in range(len(point8Coordinates)):
        if isNum(point8Coordinates[index]):
            point8Coordinates[index] = point8Coordinates[index].__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Array_Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Array_Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    point5Name = volumeName + ".P5"
    point5 = Array_Point(point5Name, point5Coordinates)
    volumeCommandsStr = volumeCommandsStr + point5.getPonitStr() + NEWLINE

    point6Name = volumeName + ".P6"
    point6 = Array_Point(point6Name, point6Coordinates)
    volumeCommandsStr = volumeCommandsStr + point6.getPonitStr() + NEWLINE

    point7Name = volumeName + ".P7"
    point7 = Array_Point(point7Name, point7Coordinates)
    volumeCommandsStr = volumeCommandsStr + point7.getPonitStr() + NEWLINE

    point8Name = volumeName + ".P8"
    point8 = Array_Point(point8Name, point8Coordinates)
    volumeCommandsStr = volumeCommandsStr + point8.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.rhombus
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, point3Name, point4Name,
                                             point5Name, point6Name, point7Name, point8Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr


def getToroidalSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                    point3Coordinates, point4Coordinates):
    """
    volumeType为AnnularSection类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return: 
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.toroidalSection
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getToroidalSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                    point3Coordinates, point4Coordinates):
    """
    volumeType为AnnularSection类型
    :param volumeName: 名称
    :param point1Coordinates: 点1坐标列表
    :param point2Coordinates: 点2坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :param point3Coordinates: 点3坐标列表
    :param point4Coordinates: 点4坐标列表
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(point1Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point1Coordinates是否为list类型"

    if not isList(point2Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point2Coordinates是否为list类型"

    if not isList(point3Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point3Coordinates是否为list类型"

    if not isList(point4Coordinates):
        return "ToroidalSectionVolume命令生成：请检查point4Coordinates是否为list类型"

    for index in range(len(point1Coordinates)):
        if isNum(point1Coordinates[index]):
            point1Coordinates[index] = point1Coordinates[index].__str__()

    for index in range(len(point2Coordinates)):
        if isNum(point2Coordinates[index]):
            point2Coordinates[index] = point2Coordinates[index].__str__()

    for index in range(len(point3Coordinates)):
        if isNum(point3Coordinates[index]):
            point3Coordinates[index] = point3Coordinates[index].__str__()

    for index in range(len(point4Coordinates)):
        if isNum(point4Coordinates[index]):
            point4Coordinates[index] = point4Coordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, point1Coordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, point2Coordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Array_Point(point3Name, point3Coordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    point4Name = volumeName + ".P4"
    point4 = Array_Point(point4Name, point4Coordinates)
    volumeCommandsStr = volumeCommandsStr + point4.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.toroidalSection
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter, point3Name, point4Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getExtrudedVolumeCommands(volumeName, areaLabel, lineLabel):
    """
    volumeType为AnnularSection类型
    :param volumeName: 名称
    :param areaLabel: 面名称
    :param lineLabel: 线名称
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE


    ## 生成具体命令
    ###生成体命令
    volumeType = Volume.Shape.extruded
    volume = Volume(volumeName, volumeType, [areaLabel, lineLabel])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getHelicalVolumeCommands(volumeName, basePointCoordinates, topPointCoordinates, radiusInner,radiusOuter, startPointCoordinates, pitch, width):
    """
    volumeType为Helical类型
    :param volumeName: 名称
    :param basePointCoordinates: 基点坐标列表
    :param topPointCoordinates: 顶点坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :param startPointCoordinates: 弧段起点坐标列表
    :param pitch: 螺旋节距
    :param width: 螺旋线径向宽度
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(basePointCoordinates):
        return "HelicalVolume命令生成：请检查basePointCoordinates是否为list类型"

    if not isList(topPointCoordinates):
        return "HelicalVolume命令生成：请检查topPointCoordinates是否为list类型"

    if not isList(startPointCoordinates):
        return "HelicalVolume命令生成：请检查startPointCoordinates是否为list类型"

    for index in range(len(basePointCoordinates)):
        if isNum(basePointCoordinates[index]):
            basePointCoordinates[index] = basePointCoordinates[index].__str__()

    for index in range(len(topPointCoordinates)):
        if isNum(topPointCoordinates[index]):
            topPointCoordinates[index] = topPointCoordinates[index].__str__()

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    if isNum(pitch):
        pitch = pitch.__str__()

    if isNum(width):
        width = width.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Point(point1Name, basePointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Point(point2Name, topPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Point(point3Name, startPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.helical
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter, point3Name, pitch, width])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

# 专为阵列体生成的函数
def Array_getHelicalVolumeCommands(volumeName, basePointCoordinates, topPointCoordinates, radiusInner,radiusOuter, startPointCoordinates, pitch, width):
    """
    volumeType为Helical类型
    :param volumeName: 名称
    :param basePointCoordinates: 基点坐标列表
    :param topPointCoordinates: 顶点坐标列表
    :param radiusInner: 内半径
    :param radiusOuter: 外半径
    :param startPointCoordinates: 弧段起点坐标列表
    :param pitch: 螺旋节距
    :param width: 螺旋线径向宽度
    :return:
    """

    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(basePointCoordinates):
        return "HelicalVolume命令生成：请检查basePointCoordinates是否为list类型"

    if not isList(topPointCoordinates):
        return "HelicalVolume命令生成：请检查topPointCoordinates是否为list类型"

    if not isList(startPointCoordinates):
        return "HelicalVolume命令生成：请检查startPointCoordinates是否为list类型"

    for index in range(len(basePointCoordinates)):
        if isNum(basePointCoordinates[index]):
            basePointCoordinates[index] = basePointCoordinates[index].__str__()

    for index in range(len(topPointCoordinates)):
        if isNum(topPointCoordinates[index]):
            topPointCoordinates[index] = topPointCoordinates[index].__str__()

    for index in range(len(startPointCoordinates)):
        if isNum(startPointCoordinates[index]):
            startPointCoordinates[index] = startPointCoordinates[index].__str__()

    if isNum(radiusInner):
        radiusInner = radiusInner.__str__()

    if isNum(radiusOuter):
        radiusOuter = radiusOuter.__str__()

    if isNum(pitch):
        pitch = pitch.__str__()

    if isNum(width):
        width = width.__str__()

    ## 生成具体命令
    ### 生成点命令
    point1Name = volumeName + ".P1"
    point1 = Array_Point(point1Name, basePointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point1.getPonitStr() + NEWLINE

    point2Name = volumeName + ".P2"
    point2 = Array_Point(point2Name, topPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point2.getPonitStr() + NEWLINE

    point3Name = volumeName + ".P3"
    point3 = Array_Point(point3Name, startPointCoordinates)
    volumeCommandsStr = volumeCommandsStr + point3.getPonitStr() + NEWLINE

    ###生成体命令
    volumeType = Volume.Shape.helical
    volume = Volume(volumeName, volumeType, [point1Name, point2Name, radiusInner, radiusOuter, point3Name, pitch, width])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr

def getFunctionVolumeCommands(volumeName,coordinateSystem, Point_1,Point_2,functionStr):
    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    # 生成命令
    ## 对坐标点的数据类型进行判断
    if not isList(Point_1):
        return "HelicalVolume命令生成：请检查basePointCoordinates是否为list类型"

    if not isList(Point_2):
        return "HelicalVolume命令生成：请检查topPointCoordinates是否为list类型"

    for index in range(len(Point_1)):
        if isNum(Point_1[index]):
            Point_1[index] = Point_1[index].__str__()

    for index in range(len(Point_2)):
        if isNum(Point_2[index]):
            Point_2[index] = Point_2[index].__str__()
    
    funNameStr=""
    if coordinateSystem==CoordinateSystem.rectangularSys:
        funNameStr=volumeName+".F(X,Y,Z)"
    elif  coordinateSystem==CoordinateSystem.polarSys:
        funNameStr=volumeName+".F(R,THETA,Z)"
    else:
        funNameStr=volumeName+".F(Z,R,THETA)"
    # func=Function(funNameStr,functionStr)
    func=Function(functionName=funNameStr,functionExpression=functionStr)
    # FUNCTION vloumName.F() = funstr
    volumeCommandsStr=volumeCommandsStr+func.getFunctionStr()+NEWLINE

    point1Name = volumeName + ".LO"
    point1=Point(point1Name,Point_1)
    volumeCommandsStr=volumeCommandsStr+point1.getPonitStr()+NEWLINE

    point2Name = volumeName + ".HI"
    point2=Point(point2Name,Point_2)
    volumeCommandsStr=volumeCommandsStr+point2.getPonitStr()+NEWLINE

    volumeType = Volume.Shape.functional
    volume = Volume(volumeName,volumeType,[volumeName+".F",point1Name,point2Name])
    volumeCommandsStr = volumeCommandsStr + volume.getVolumeStr() + NEWLINE

    return volumeCommandsStr


def getArrayVolumeCommands(coordinateSystem,arrayParameterList,baseType, baseParameterList,markStr):
    """
    volumeType为Array类型
    :param arrayParameterList: 阵列体的参数
    :param baseParameterList: 阵列体的基础物体参数
    :return:
    """
    baseParameterList[0]="Arr_"+baseParameterList[0]
    centerAxis = "X"
    orthoFace = "XY"
    numY = "1"
    if coordinateSystem == "R":
        system = System.Type.cartesian
        [label, baseObj, arrayType, centerAxis, orthoFace, numX, numY, numZ, num, numPolar, stepX, stepY, stepZ] = arrayParameterList
        array = Array(system,arrayType, centerAxis, orthoFace, numX, numY, numZ, num, numPolar, stepX, stepY, stepZ)
        # 生成对应的注释
        volumeCommandsStr = NEWLINE + "!!" + label + NEWLINE
        volumeCommandsStr = volumeCommandsStr + array.getArrayStr() + NEWLINE

    else:
        if coordinateSystem == "P":
            system = System.Type.polar
        else:
            system = System.Type.cylindrical
        [label, baseObj, arrayType, numR, numZ, num, numPolar, stepR, stepTheta, stepZ] = arrayParameterList
        array = Array(system,arrayType,centerAxis,orthoFace,numR, numY, numZ, num, numPolar, stepR, stepTheta, stepZ)
        # 生成对应的注释
        volumeCommandsStr = NEWLINE + "!!" + label + NEWLINE
        volumeCommandsStr = volumeCommandsStr + array.getArrayStr() + NEWLINE

    # 生成基础模型命令
    import Modeling.Common.Tools.ObjectsTools as ObjectsTools
    #增加名字尾缀
    baseParameterList[0] = baseParameterList[0] + '\'i\''
    # 点
    if baseType == ObjectsTools.ObjectType.Point:
        [ponitName, coordinates] = baseParameterList
        # 将坐标扩展
        coordinates = array.getCoordinateStr(coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getPointCommands(ponitName, coordinates)

    # 线
    elif (baseType == ObjectsTools.ObjectType.Line_Conformal):
        [lineName, lineType, startPointCoordinates, stopPointCoordinates] = baseParameterList
        startPointCoordinates = array.getCoordinateStr(startPointCoordinates)
        stopPointCoordinates = array.getCoordinateStr(stopPointCoordinates)
        lineType = Line.Type.conformal
        volumeCommandsStr = volumeCommandsStr + Array_getLineCommands(lineName, lineType, startPointCoordinates, stopPointCoordinates)

    # 面
    elif(baseType == ObjectsTools.ObjectType.Area_Conformal or
          baseType == ObjectsTools.ObjectType.Area_Rectangular):
        [areaName, areaType, startPointCoordinates, stopPointCoordinates] = baseParameterList
        startPointCoordinates = array.getCoordinateStr(startPointCoordinates)
        stopPointCoordinates = array.getCoordinateStr(stopPointCoordinates)
        if areaType == ObjectsTools.ObjectType.Area_Conformal:
            areaType = Area.Shape.conformal
        else:
            areaType = Area.Shape.rectangular
        volumeCommandsStr = volumeCommandsStr + Array_getAreaCommands(areaName, areaType, startPointCoordinates, stopPointCoordinates)

    # 斜线
    elif baseType == ObjectsTools.ObjectType.Line_Oblique:
        [lineName, startPointCoordinates, stopPointCoordinates,baseradius] = baseParameterList
        startPointCoordinates = array.getCoordinateStr(startPointCoordinates)
        stopPointCoordinates = array.getCoordinateStr(stopPointCoordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getObliqueLineCommands(lineName, startPointCoordinates, stopPointCoordinates,baseradius)

    # 多边形面
    elif baseType == ObjectsTools.ObjectType.Area_Polygonal:
        [areaName, pointCoordinatesList] = baseParameterList
        for index in range(len(pointCoordinatesList)):
            pointCoordinatesList[index] = array.getCoordinateStr(pointCoordinatesList[index])
        volumeCommandsStr = volumeCommandsStr + Array_getPolygonalAreaCommands(areaName, pointCoordinatesList)

    # 投影体
    elif baseType == ObjectsTools.ObjectType.Vol_Conformal:
        [volumeName, nearPointCoordinates, farPointCoordinates] = baseParameterList
        nearPointCoordinates = array.getCoordinateStr(nearPointCoordinates)
        farPointCoordinates = array.getCoordinateStr(farPointCoordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getConformalVolumeCommands(volumeName, nearPointCoordinates, farPointCoordinates)

    # 圆锥或圆台
    elif baseType == ObjectsTools.ObjectType.Vol_SpecialCone:
        [volumeName, basePointCoordinates, topPointCoordinates, baseradius, topradius] = baseParameterList
        basePointCoordinates = array.getCoordinateStr(basePointCoordinates)
        topPointCoordinates = array.getCoordinateStr(topPointCoordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getConeVolumeCommands(volumeName, basePointCoordinates, topPointCoordinates, baseradius, topradius)

    # 环形体
    elif baseType == ObjectsTools.ObjectType.Vol_Annular:
        [volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radiusInner, radiusOuter] = baseParameterList
        centerPoint1Coordinates = array.getCoordinateStr(centerPoint1Coordinates)
        centerPoint2Coordinates = array.getCoordinateStr(centerPoint2Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getAnnularVolumeCommands(volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radiusInner, radiusOuter)

    # 圆柱
    elif baseType == ObjectsTools.ObjectType.Vol_Cylinder:
        [volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radius] = baseParameterList
        centerPoint1Coordinates = array.getCoordinateStr(centerPoint1Coordinates)
        centerPoint2Coordinates = array.getCoordinateStr(centerPoint2Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getCylindricalVolumeCommands(volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radius)

    # 平行六面体
    elif baseType == ObjectsTools.ObjectType.Vol_Parallelepipedal:
        [volumeName, point1Coordinates, point2Coordinates,
                                          point3Coordinates, point4Coordinates] = baseParameterList
        point1Coordinates = array.getCoordinateStr(point1Coordinates)
        point2Coordinates = array.getCoordinateStr(point2Coordinates)
        point3Coordinates = array.getCoordinateStr(point3Coordinates)
        point4Coordinates = array.getCoordinateStr(point4Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getParallelepipedalVolumeCommands(volumeName, point1Coordinates, point2Coordinates,
                                          point3Coordinates, point4Coordinates)

    # 球体
    elif baseType == ObjectsTools.ObjectType.Vol_Spherical:
        [volumeName, pointCoordinates, radius] = baseParameterList
        pointCoordinates = array.getCoordinateStr(pointCoordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getSphericalVolumeCommands(volumeName, pointCoordinates, radius)

    # 棱锥体
    elif baseType == ObjectsTools.ObjectType.Vol_Pyramid:
        [volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                                 point5Coordinates] = baseParameterList
        point1Coordinates = array.getCoordinateStr(point1Coordinates)
        point2Coordinates = array.getCoordinateStr(point2Coordinates)
        point3Coordinates = array.getCoordinateStr(point3Coordinates)
        point4Coordinates = array.getCoordinateStr(point4Coordinates)
        point5Coordinates = array.getCoordinateStr(point5Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getPyramidVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                                 point5Coordinates)

    # 部分圆环体
    elif baseType == ObjectsTools.ObjectType.Vol_Toroidal_Section:
        [volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                         point3Coordinates, point4Coordinates] = baseParameterList
        point1Coordinates = array.getCoordinateStr(point1Coordinates)
        point2Coordinates = array.getCoordinateStr(point2Coordinates)
        point3Coordinates = array.getCoordinateStr(point3Coordinates)
        point4Coordinates = array.getCoordinateStr(point4Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getToroidalSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                         point3Coordinates, point4Coordinates)

    # 楔形体
    elif baseType == ObjectsTools.ObjectType.Vol_Wedge:
        [volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                               point5Coordinates, point6Coordinates] = baseParameterList
        point1Coordinates = array.getCoordinateStr(point1Coordinates)
        point2Coordinates = array.getCoordinateStr(point2Coordinates)
        point3Coordinates = array.getCoordinateStr(point3Coordinates)
        point4Coordinates = array.getCoordinateStr(point4Coordinates)
        point5Coordinates = array.getCoordinateStr(point5Coordinates)
        point6Coordinates = array.getCoordinateStr(point6Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getWedgeVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                               point5Coordinates, point6Coordinates)

    # 四面体
    elif baseType == ObjectsTools.ObjectType.Vol_Tetrahedron:
        [volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates] = baseParameterList
        point1Coordinates = array.getCoordinateStr(point1Coordinates)
        point2Coordinates = array.getCoordinateStr(point2Coordinates)
        point3Coordinates = array.getCoordinateStr(point3Coordinates)
        point4Coordinates = array.getCoordinateStr(point4Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getTetrahedronVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates)

    # 菱形体
    elif baseType == ObjectsTools.ObjectType.Vol_Rhombus:
        [volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                                 point5Coordinates, point6Coordinates, point7Coordinates, point8Coordinates] = baseParameterList
        point1Coordinates = array.getCoordinateStr(point1Coordinates)
        point2Coordinates = array.getCoordinateStr(point2Coordinates)
        point3Coordinates = array.getCoordinateStr(point3Coordinates)
        point4Coordinates = array.getCoordinateStr(point4Coordinates)
        point5Coordinates = array.getCoordinateStr(point5Coordinates)
        point6Coordinates = array.getCoordinateStr(point6Coordinates)
        point7Coordinates = array.getCoordinateStr(point7Coordinates)
        point8Coordinates = array.getCoordinateStr(point8Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getRhombusVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                                 point5Coordinates, point6Coordinates, point7Coordinates, point8Coordinates)

    # 部分环面体
    elif baseType == ObjectsTools.ObjectType.Vol_Annular_Section:
        [volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                        point3Coordinates, point4Coordinates] = baseParameterList
        point1Coordinates = array.getCoordinateStr(point1Coordinates)
        point2Coordinates = array.getCoordinateStr(point2Coordinates)
        point3Coordinates = array.getCoordinateStr(point3Coordinates)
        point4Coordinates = array.getCoordinateStr(point4Coordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getAnnularSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,
                                        point3Coordinates, point4Coordinates)

    # 挤出体
    elif baseType == ObjectsTools.ObjectType.Vol_Extruded:
        [volumeName, areaLabel, lineLabel] = baseParameterList
        volumeCommandsStr = volumeCommandsStr + getExtrudedVolumeCommands(volumeName, areaLabel, lineLabel)

    # 螺旋体
    elif baseType == ObjectsTools.ObjectType.Vol_Helical:
        [volumeName, basePointCoordinates, topPointCoordinates, radiusInner,radiusOuter, startPointCoordinates, pitch, width] = baseParameterList
        basePointCoordinates = array.getCoordinateStr(basePointCoordinates)
        topPointCoordinates = array.getCoordinateStr(topPointCoordinates)
        startPointCoordinates = array.getCoordinateStr(startPointCoordinates)
        volumeCommandsStr = volumeCommandsStr + Array_getHelicalVolumeCommands(volumeName, basePointCoordinates, topPointCoordinates, radiusInner,radiusOuter, startPointCoordinates, pitch, width)

    volumeCommandsStr = volumeCommandsStr + NEWLINE + markStr + NEWLINE + "ENDDO;"+ NEWLINE
    return volumeCommandsStr

# @fubiap 参数阵列体
def getParamArrayVolumeCommands(volumeName, baseObjType, start, end,baseObjData,extraContentMark):
    '''
    volumeName: 参数阵列体的名称
    baseObjType: 基础模型的类型
    start:i开始
    end:i结束
    baseObjData: 基础模型的数据
    '''
    # 生成对应的注释
    volumeCommandsStr = NEWLINE + "!!" + volumeName + NEWLINE

    doStr="do i="+start+","+end+";"+NEWLINE
    volumeCommandsStr=volumeCommandsStr+doStr

    # !!volum'i'
    itemStr="!!"+volumeName+"\'i\'"+NEWLINE
    volumeCommandsStr=volumeCommandsStr+itemStr
    ## 生成具体命令
    ### 生成点命令
    volName = volumeName + "\'i\'"
    vol = Volume(volumeName=volName,shape=baseObjType,args=baseObjData )
    volumeCommandsStr = volumeCommandsStr + vol.getVolumeStr() + NEWLINE

    volumeCommandsStr=volumeCommandsStr+extraContentMark+"ENDDO;"+ NEWLINE
    return volumeCommandsStr



def getMarkCommands(objectName, isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                   ismin_1 = False, ismid_1 = False, ismax_1 = False,
                   ismin_2 = False, ismid_2 = False, ismax_2 = False,
                   ismin_3 = False, ismid_3 = False, ismax_3 = False):

    "objectName为要设置非均匀网格的几何体名称, isX1、isX2,、isX3为是否选择了对应的坐标轴，boolean型, X1Size、X2Size,、X3Size为对应坐标轴上的值，目前存在的问题是默认修饰符为SIZE"

    # 生成对应的注释
    markCommandsStr = ""

    # 生成命令
    ## 对X1Size, X2Size, X3Size的数据类型进行判断
    if isNum(X1Size):
        X1Size = X1Size.__str__()

    if isNum(X2Size):
        X2Size = X2Size.__str__()

    if isNum(X3Size):
        X3Size = X3Size.__str__()

    ## 生成具体命令
    markModification= Mark.Modification.size
    if isBool(isX1):
        if isX1:
            mark1 = Mark(objectName, Mark.Direction.x1, markModification, X1Size, ismin_1, ismid_1, ismax_1)
            markCommandsStr = markCommandsStr + mark1.getMarkStr() + NEWLINE
    else:
        return "mark命令生成：请检查isX1的值"

    if isBool(isX2):
        if isX2:
            mark2 = Mark(objectName, Mark.Direction.x2, markModification, X2Size, ismin_2, ismid_2, ismax_2)
            markCommandsStr = markCommandsStr + mark2.getMarkStr() + NEWLINE
    else:
        return "mark命令生成：请检查isX2的值"

    if isBool(isX3):
        if isX3:
            mark3 = Mark(objectName, Mark.Direction.x3, markModification, X3Size, ismin_3, ismid_3, ismax_3)
            markCommandsStr = markCommandsStr + mark3.getMarkStr() + NEWLINE
    else:
        return "mark命令生成：请检查isX3的值"

    return markCommandsStr


def getVoidCommands(objectName,thiscontent=""):
    "设置真空属性，objectName为对象名称"

    # 生成命令
    void = Void(objectName)
    voidCommandsStr=""
    if thiscontent!="":
        # 提取content中的关键字do i=...;
        #                     CONDUCTOR 体'i';
        import re
        doStrs=re.findall(r"\bdo.*",thiscontent)
        doStr=""
        if len(doStrs)>0:
            doStr=doStrs[0]
        # 提取体'i'
        objNames=re.findall(r"!![\S].*\'i\'",thiscontent)
        objName=""
        if len(objNames):
            objectName=objNames[0].replace("!!","")
        void = Void(objectName)

        voidCommandsStr = NEWLINE +doStr+NEWLINE+void.getVoidStr()+NEWLINE+"ENDDO;"+ NEWLINE
    else:
        voidCommandsStr = NEWLINE +void.getVoidStr()+ NEWLINE
    return voidCommandsStr


def getConductorCommands(objectName,thiscontent=""):
    "设置理想导体属性，objectName为对象名称"

    # 生成命令
    conductor = Conductor(objectName)
    conductorCommandsStr=""
    if thiscontent!="":
        # 提取content中的关键字do i=...;
        #                     CONDUCTOR 体'i';
        import re
        doStrs=re.findall(r"\bdo.*",thiscontent)
        doStr=""
        if len(doStrs)>0:
            doStr=doStrs[0]
        # 提取体'i'
        objNames=re.findall(r"!![\S].*\'i\'",thiscontent)
        objName=""
        if len(objNames):
            objectName=objNames[0].replace("!!","")
        conductor = Conductor(objectName)
        conductorCommandsStr = NEWLINE +doStr+NEWLINE+conductor.getConductorStr()+NEWLINE+" ENDDO;"+ NEWLINE
    else:
        conductorCommandsStr = NEWLINE + conductor.getConductorStr() + NEWLINE

    return conductorCommandsStr


def getVolumeDIYAttributeCommands(volumeName,
                                  isconductance="", sigma="",
                                  isDielectric=True, isotropy=True, permittivity1="", permittivity2="", permittivity3="",
                                  eps1 = '',eps2 = '', eps3 = '',
                                  thiscontent=""):
    """
    设置体的自定义属性
    :param volumeName: 体的名称
    :param isconductance: 是否选择设置电导率
    :param sigma: 电导率
    :param isDielectric: 是否选择设置相对介电常数
    :param isotropy: 是否各项同性
    :param permittivity1: 介电常数1，各向同性时，填写介电常数1
    :param permittivity2: 介电常数2
    :param permittivity3: 介电常数3
    :param thisContent (@fuiao): 若是阵列体，改参数不为空，从该参数中提取有用信息
    :return: 
    """
    # 对传入的参数的类型转换
    if isNum(sigma):
        sigma = sigma.__str__()

    if isNum(permittivity1):
        permittivity1 = permittivity1.__str__()

    if isNum(permittivity2):
        permittivity2 = permittivity2.__str__()

    if isNum(permittivity3):
        permittivity3 = permittivity3.__str__()
    if isNum(eps1):
        eps1 = eps1.__str__()
    if isNum(eps2):
        eps2 = eps2.__str__()
    if isNum(eps3):
        eps3 = eps3.__str__()


    # 生成具体命令组
    returnStr = NEWLINE + ""

    # if isBool(isconductance):
    #     if isconductance:
    #         # 是阵列体
    #         if thiscontent!="":
                
    #             # 提取content中的关键字do i=...;
    #             #                     CONDUCTOR 体'i';
    #             import re
    #             doStrs=re.findall(r"\bdo.*",thiscontent)
    #             doStr=""
    #             if len(doStrs)>0:
    #                 doStr=doStrs[0]
    #             # 提取体'i'
    #             objNames=re.findall(r"!![\S].*\'i\'",thiscontent)
    #             objName=""
    #             if len(objNames):
    #                 objectName=objNames[0].replace("!!","")
    #             # conductor = Conductor(objectName)
    #             conductance = Conductance(objectName, sigma)
    #             returnStr = returnStr +doStr+NEWLINE+conductance.getConductanceStr()+ NEWLINE
    #         else:
    #             conductance = Conductance(volumeName, sigma)
    #             returnStr = returnStr + conductance.getConductanceStr() + NEWLINE
    # else:
    #     return "体定义属性命令生成，请检查isconductance"
    # 修改后的customM3D代码 @ lizhenguang
    # FreeCAD.Console.PrintError('\n已经进入attribute的函数\n')
    if isconductance == 'Isotropy' or isconductance == 'Anisotropy':
        # 是阵列体
        if thiscontent!="":    
            # 提取content中的关键字do i=...;
            #                     CONDUCTOR 体'i';
            import re
            doStrs=re.findall(r"\bdo.*",thiscontent)
            doStr=""
            if len(doStrs)>0:
                doStr=doStrs[0]
            # 提取体'i'
            objNames=re.findall(r"!![\S].*\'i\'",thiscontent)
            objName=""
            if len(objNames):
                objectName=objNames[0].replace("!!","")
            # conductor = Conductor(objectName)
            conductance = Conductance(objectName,eps1,eps2,eps3,isconductance)
            returnStr = returnStr +doStr+NEWLINE+conductance.getConductanceStr()+ NEWLINE
        else:
            conductance = Conductance(volumeName,eps1,eps2,eps3,isconductance)
            returnStr = returnStr + conductance.getConductanceStr() + NEWLINE
    elif isconductance == 'NotDefine':
        pass

    if isBool(isDielectric):
        if isDielectric:
            if isBool(isotropy):
                #是阵列体
                if thiscontent!="":
                    # 提取content中的关键字do i=...;
                    #                     CONDUCTOR 体'i';
                    import re
                    doStrs=re.findall(r"\bdo.*",thiscontent)
                    doStr=""
                    if len(doStrs)>0:
                        doStr=doStrs[0]
                    # 提取体'i'
                    objNames=re.findall(r"!![\S].*\'i\'",thiscontent)
                    objName=""
                    if len(objNames):
                        objectName=objNames[0].replace("!!","")
                    # conductor = Conductor(objectName)
                    # conductance = Conductance(objectName, sigma)
                    
                    dielectric = Dielectric(objectName, isotropy, permittivity1, permittivity2, permittivity3)
                    if isconductance:
                        returnStr = returnStr +dielectric.getDielectricStr() + NEWLINE
                    else:
                        returnStr = returnStr+doStr+NEWLINE+dielectric.getDielectricStr() + NEWLINE
                else:
                    dielectric = Dielectric(volumeName, isotropy, permittivity1, permittivity2, permittivity3)
                    returnStr = returnStr + dielectric.getDielectricStr() + NEWLINE                   
            else:
                return "体定义属性命令生成，请检查isotropy"
    else:
        return "体定义属性命令生成，请检查isDielectric"
    if thiscontent!="":
        returnStr=returnStr+"ENDDO;"+NEWLINE
    return returnStr


def getPortCommands(panelName, coordinateSystem, name, direction,
                    isPhaseVelocity=False, phaseVelocity="",
                    isScale=False, scale="",
                    isFt=False, ftVal="",
                    isGeFirst=False, geFirstName="", geFirstVal="",
                    isGeSecond=False, geSecondName="", geSecondVal="",
                    isNormalization=False, normalizationLine="",
                    isLaplacian=False, laplacianFirst="", laplacianSecond="",
                    laplacenumber1="",laplacenumber2="",
                    laplacianThird="", laplacianFourth="",laplacianFifth="",
                    laplacenumber3="",laplacenumber4="",laplacenumber5="",
                    laplace_num = "",
                    circuit_Checked = False,circuit = "",observe_name = ""
                    ):
    """
    port面板对应的命令组
    name为波导端口名称
    direction为波导端口的法向，POSITIVE 或 NEGATIVE
    
    以下为可选参数
    isPhaseVelocity、phaseVelocity对应于相对相速比
    isScale、scale相对于法向修正
    isFt、ftVal相对于输入场时间分布
    isGeFirst、geFirstName、geFirstVal相对于空间分布的第一个空,geFirstName请以 GE* 命名
    isGeSecond、geSecondName、geSecondVal相对于空间分布的第二个空，geSecondName请以 GE* 命名
    isNormalization、normalizationLine相对于电压归一化
    isLaplacian、laplacianFirst、laplacianSecind相对于拉普拉斯的两个选项
    """
    

    portCommandsStr = NEWLINE + "!!" + panelName + NEWLINE

    # 定义有关函数的命令
    coordinateSystemStr = ""
    if coordinateSystem == CoordinateSystem.rectangularSys:
        coordinateSystemStr = CoordinateSystem.rectangular3
    elif coordinateSystem == CoordinateSystem.polarSys:
        coordinateSystemStr = CoordinateSystem.polar3
    elif coordinateSystem == CoordinateSystem.cylindricalSys:
        coordinateSystemStr = CoordinateSystem.cylindrical3
    else:
        "EmE命令生成：请检查coordinateSystem的类型"

    if isBool(isFt):
        if isFt:
            FtName = name + ".F(T)"
            funFt = Function(type=Function.Type.expression, functionName=FtName, functionExpression=ftVal)
            portCommandsStr = portCommandsStr + funFt.getFunctionStr() + newline
    else:
        return "port命令生成：请检查isFt的类型"

    if isBool(isGeFirst):
        if isGeFirst:
            geFirstFunctionName = name + "." + geFirstName + coordinateSystemStr
            geFirst = Function(type=Function.Type.expression, functionName=geFirstFunctionName, functionExpression=geFirstVal)
            portCommandsStr = portCommandsStr + geFirst.getFunctionStr() + newline
    else:
        return "port命令生成：请检查isGeFirst的类型"

    if isBool(isGeSecond):
        if isGeSecond:
            geSecondFunctionName = name + "." + geSecondName + coordinateSystemStr
            geSecond = Function(type=Function.Type.expression, functionName=geSecondFunctionName, functionExpression=geSecondVal)
            portCommandsStr = portCommandsStr + geSecond.getFunctionStr() + newline
    else:
        return "port命令生成：请检查isGeSecond的类型"

    # 定义Port的命令
    ## 检查常量字符串是否符合规范
    if direction!=Port.DirectionType.positive and direction!=Port.DirectionType.negative and direction!="":
        return "port命令生成：请检查direction"

    if geFirstName!="GE1" and geFirstName!="GE2" and geFirstName!="GE3" and geFirstName!="":
        return "port命令生成：请检查geFirstName"

    if geSecondName!="GE1" and geSecondName!="GE2" and geSecondName!="GE3" and geSecondName!="":
        return "port命令生成：请检查geSecondName"

    ## 生成具体命令
    port = Port(name, direction,
                isPhaseVelocity, phaseVelocity,
                isScale, scale,
                isFt,
                isGeFirst, geFirstName,
                isGeSecond, geSecondName,
                isNormalization, normalizationLine,
                isLaplacian, laplacianFirst, laplacianSecond,
                laplacenumber1,laplacenumber2,
                laplacianThird, laplacianFourth,laplacianFifth,
                laplacenumber3,laplacenumber4,laplacenumber5,
                laplace_num,
                circuit_Checked,circuit,observe_name)
    portCommandsStr = portCommandsStr + port.getPortStr() + newline

    return portCommandsStr
def getNewMarkCommands(name = "", mark_obj = "", direction = "", 
                        isChecked_min = False, isChecked_mid = False , isChecked_max = False, size = ""):
    '''
    param name:...
    param name:
    param name:
    param name:
    '''
    returnStr = NEWLINE + "!!" + name + NEWLINE

    mark_instance = Mark_sup(name, mark_obj, direction, isChecked_min, isChecked_mid, isChecked_max, size)

    returnStr = returnStr + mark_instance.getMarkStr() + NEWLINE

    return returnStr
    
def getEmSECommands(name,energySec,maxNum,WEIGHT_FACTOR,ENERGY_DISTRIBUTION,min_energy,
                    max_energy,ANGLE_DISTRIBUTION,isCheck_WF,isCheck_ED,isCheck_AD,
                    notInclude1,notInclude2,include1,include2,Emitter,
                    isEmit,isExclude1,isExclude2,isInclude1,isInclude2):
    '''
    param name:二次发射名称
    param energySec:二次发射能量
    param maxNum:最大发射数对应能量
    param WEIGHT_FACTOR:权重系数
    param ENERGY_DISTRIBUTION:能量分布
    param min_energy:最小能量
    param max_energy:最大能量
    param ANGLE_DISTRIBUTION:角分布
    param isCheck_WF:是否选择权重系数
    param isCheck_ED:是否选择能量分布
    param isCheck_AD:是否选择角分布
    '''
    returnStr = NEWLINE + "!!" + name + NEWLINE

    if isBool(isCheck_ED):
        if isCheck_ED:
            FtName = "FED_" + name + "(EN)"
            funFt = Function(type=Function.Type.expression, functionName=FtName, functionExpression=ENERGY_DISTRIBUTION)
            returnStr = returnStr + funFt.getFunctionStr() + newline
    else:
        return "EmSE命令生成：请检查isCheck_ED的类型"

    if isBool(isCheck_AD):
        if isCheck_AD:
            FtName =  "FAD_" + name + "(CT)"
            funFt = Function(type=Function.Type.expression, functionName=FtName, functionExpression=ANGLE_DISTRIBUTION)
            returnStr = returnStr + funFt.getFunctionStr() + newline
    else:
        return "EmSE命令生成：请检查isCheck_AD的类型"

    EmSE_instance = EmSE(name,energySec,maxNum,WEIGHT_FACTOR,ENERGY_DISTRIBUTION,min_energy,
                    max_energy,ANGLE_DISTRIBUTION,isCheck_WF,isCheck_ED,isCheck_AD)
    returnStr = returnStr + EmSE_instance.getEmSEstr() + NEWLINE
    ## 定义具体EMIT命令
    if isBool(isEmit):
        if isEmit:
            emit = Emit(name, Emitter,
                        isExclude1, notInclude1, isExclude2, notInclude2,
                        isInclude1, include1, isInclude2, include2)
            returnStr = returnStr + emit.getEmitStr() + NEWLINE
    else:
        return "EmSE命令生成：请检查isEmit的类型"

    return returnStr

def getMergeCommands(name,Types,everyNum,maxNum):
    # FreeCAD.Console.PrintError("\n进入加载get的数据过程")
    returnStr = NEWLINE + "!!" + name + NEWLINE

    Merge_instance = Merge(name,Types,everyNum,maxNum)

    returnStr = returnStr + Merge_instance.getMergeStr() + NEWLINE
    # FreeCAD.Console.PrintError("\n执行完get的数据过程")
    return returnStr

def getGasgasCommands(name,Types,pressure,temperature):
    
    returnStr = NEWLINE + "!!" + name + NEWLINE

    Gas_instance = Gasgas(name,Types,pressure,temperature)

    returnStr = returnStr + Gas_instance.getGasgasStr() + NEWLINE

    return returnStr

def getSpeciesCommands(name,powerUnitl,quality,massUnit):

    returnStr = NEWLINE + "!!" + name + NEWLINE

    species_instance = Species(name,powerUnitl,quality,massUnit)
    returnStr = returnStr + species_instance.getSpeciesStr() + NEWLINE

    FreeCAD.Console.PrintError("\n执行完get的数据过程")
    return returnStr

def getPopulateCommands(name,types,volume,X1,Y1,Z1,X2,Y2,Z2,density,temp):
    '''
    param name:名称
    param types:粒子类型
    param volume: 指定的正交投影体
    param X1:每个网格宏粒子数
    param Y1:每个网格宏粒子数
    param Z1:每个网格宏粒子数
    param X2: 电子平均速度
    param Y2: 电子平均速度
    param Z2: 电子平均速度
    param denisty:电荷密度
    param temp:温度
    '''
    returnStr = NEWLINE + "!!" + name + NEWLINE
    # FreeCAD.Console.PrintError("\n进入get函数")
    populate_instance = Populate(name,types,volume,X1,Y1,Z1,X2,Y2,Z2,density,temp)

    returnStr = returnStr + populate_instance.getPopulateStr() + NEWLINE

    return returnStr

def getFreespaceCommands(panelName, freeSpaceName, trendType, xType, component, isConductivity, funExpression):
    """
    吸收边界
    :param freeSpaceName: 吸收边界名称
    :param trendType: 传播方向-正向或反向，填写 POSITIVE NEGATIVE
    :param xType: 传播方向-x/y/z，填写X1 X2 X3
    :param component: 吸收分量
    :param isConductivity: 是否滴定仪传导率
    :param funExpression: 传导率的表达式
    :return: 
    """

    # 检查trendType
    if trendType != Freespace.TrendType.positive and trendType != Freespace.TrendType.negative:
        return "Freespace命令生成，请检查trendType"

    # 检查xType
    if xType != Freespace.XType.x1 and xType != Freespace.XType.x2 and xType != Freespace.XType.x3:
        return "Freespace命令生成，请检查xType"

    returnStr = NEWLINE + "!!" + panelName + NEWLINE

    # 生成命令组
    if isBool(isConductivity):
        if isConductivity:
            # 生成函数命令
            funName = freeSpaceName + ".F(Xn)"
            function = Function(Function.Type.expression, funName, funExpression)
            returnStr = returnStr + function.getFunctionStr() + NEWLINE

        # 生成Freespace命令
        funName = freeSpaceName + ".F"
        freespace = Freespace(freeSpaceName, trendType, xType, component, isConductivity, funName)
        returnStr = returnStr + freespace.getFreespaceStr() + NEWLINE
    else:
        return "Freespace命令生成，请检查isConductivity"

    return returnStr


def getSymmetryCommands(panelName, type="", trendType="", lineOrArea1="",lineOrArea2=""):
    """
    对称边界
    :param type: 对称类型 AXIAL、MIRROR、PERIODIC    
    :param trendType: 方向 POSITIVE、NEGATIVE
    :param lineOrArea1: 正交投影面名称
    :param lineOrArea2: 对称类型中的名称
    :return: 
    """

    # 检查常变量
    if type != Symmetry.Type.axial and type != Symmetry.Type.mirror and type != Symmetry.Type.periodic:
        return "Symmetry命令生成，请检查type"

    if trendType != Symmetry.TrendType.positive and trendType != Symmetry.TrendType.negative:
        return "Symmetry命令生成，请检查trendType"

    symmetry = Symmetry(type, trendType, lineOrArea1, lineOrArea2)
    returnStr = NEWLINE + "!!" + panelName + NEWLINE + symmetry.getSymmetryStr() + NEWLINE

    return returnStr


def getEmBCommands(coordinateSystem, emitName, BeamJ, BeamV,
                   isSpecies=False, species="",
                   isNumber=False, creationRate="",
                   isTiming=False, timingType="", stepMultiple="",
                   isSurfaceSpacing=False, surfaceSpacing="",
                   isOutwardSpacing=False, outwardSpacing="", dn="",
                   isEmit=False, mobject="",
                   isExclude1=False, excludeVolume1="", isExclude2=False, excludeVolume2="",
                   isInclude1=False, includeVolume1="", isInclude2=False, includeVolume2=""
                   ):
    """
    EmB面板对应的命令组
    
    emitName 为名称
    beamJ 为束电流密度对应的函数表达式
    BeamV 为束电压参量对应的函数表达式
    
    以下为发射选项可选参数
    isSpecies, species 为发射选项-粒子类型，species为 ELECTRON 或 PROTON
    isNumber, creationRate 为发射选项-产生率
    isTiming, timingType, stepMultiple 为发射选项-发射间隔，timingType为 TIMING 或 RANDOM_TIMING
    isSurfaceSpacing, surfaceSpacing 为发射选项-沿表面分布，surfaceSpacing为 RANDOM 或 UNIFORM 或 FIXED
    isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 FIXED
    
    以下为发射区域选项
    isEmit, mobject 为发射区域选项-发射体
    isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
    isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
    """

    EmBCommandsStr = NEWLINE + ""

    # 定义有关函数

    coordinateSystemStr = ""
    if coordinateSystem == CoordinateSystem.rectangularSys:
        coordinateSystemStr = CoordinateSystem.rectangular4
    elif coordinateSystem == CoordinateSystem.polarSys:
        coordinateSystemStr = CoordinateSystem.polar4
    elif coordinateSystem == CoordinateSystem.cylindricalSys:
        coordinateSystemStr = CoordinateSystem.cylindrical4
    else:
        "EmB命令生成：请检查coordinateSystem的类型"

    if isBool(isOutwardSpacing):
        if isOutwardSpacing:
            DnName = emitName + ".Dn" + coordinateSystemStr
            funDn = Function(type=Function.Type.expression, functionName=DnName, functionExpression=dn)
            EmBCommandsStr = EmBCommandsStr + funDn.getFunctionStr() + newline
    else:
        return "EmB命令生成：请检查isOutwardSpacing的类型"

    BeamJName = emitName + ".BeamJ" + coordinateSystemStr
    funBeamJ = Function(type=Function.Type.expression, functionName=BeamJName, functionExpression=BeamJ)
    EmBCommandsStr = EmBCommandsStr + funBeamJ.getFunctionStr() + newline

    BeamVName = emitName + ".BeamV" + coordinateSystemStr
    funBeamV = Function(type=Function.Type.expression, functionName=BeamVName, functionExpression=BeamV)
    EmBCommandsStr = EmBCommandsStr + funBeamV.getFunctionStr() + newline

    # 定义EMISSION命令
    ## 检查常量字符串是否符合规范
    if species != EmissionOption.SpeciesType.electron and species != EmissionOption.SpeciesType.proton and species != "":
        return "EmB命令生成：请检查species"

    if timingType != EmissionOption.TimingType.timing and timingType != EmissionOption.TimingType.random_timing and timingType != "":
        return "EmB命令生成：请检查timingType"

    if surfaceSpacing != EmissionOption.SpacingType.random and surfaceSpacing != EmissionOption.SpacingType.uniform \
            and surfaceSpacing != EmissionOption.SpacingType.fixed and surfaceSpacing != "":
        return "EmB命令生成：请检查surfaceSpacing"

    if outwardSpacing != EmissionOption.SpacingType.random and outwardSpacing != EmissionOption.SpacingType.fixed and outwardSpacing != "":
        return "EmB命令生成：请检查outwardSpacing"

    ## 转换数据类型
    if isNum(creationRate):
        creationRate = creationRate.__str__()

    if isNum(stepMultiple):
        stepMultiple = stepMultiple.__str__()

    ## 定义具体EMISSION命令
    emissionBeam = EmissionBeam(emitName)
    EmBCommandsStr = EmBCommandsStr + emissionBeam.getEmissionBeamStr()

    emissionOptions = EmissionOption(emitName,
                 isSpecies, species,
                 isNumber, creationRate,
                 isTiming, timingType, stepMultiple,
                 isSurfaceSpacing, surfaceSpacing,
                 isOutwardSpacing, outwardSpacing)
    EmBCommandsStr = EmBCommandsStr + emissionOptions.getEmissionExplosiveStr() + newline

    ## 定义具体EMIT命令
    if isBool(isEmit):
        if isEmit:
            emit = Emit(emitName, mobject,
                        isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                        isInclude1, includeVolume1, isInclude2, includeVolume2)
            EmBCommandsStr = EmBCommandsStr + emit.getEmitStr() + newline
    else:
        return "EmB命令生成：请检查isEmit的类型"

    return EmBCommandsStr


def getEmECommands(coordinateSystem, emitName,
                         isTField=False, TField="",
                         isRField=False, RField="",
                         isCharg=False, Charg="",
                         isFRate=False, FRate="",
                         isSpecies=False, species="",
                         isNumber=False, creationRate="",
                         isTiming=False, timingType="", stepMultiple="",
                         isSurfaceSpacing=False, surfaceSpacing="",
                         isOutwardSpacing=False, outwardSpacing="", dn="",
                         isEmit=False, mobject="",
                         isExclude1=False, excludeVolume1="", isExclude2=False, excludeVolume2="",
                         isInclude1=False, includeVolume1="", isInclude2=False, includeVolume2=""
                         ):
    """
    EmE面板对应的命令组

    emitName 为名称
    isTField, TField 为极限场值对应的函数表达式
    isRField, RField 为空间余场对应的函数表达式
    isCharg, Charg 为最小电荷对应的函数表达式
    isFRate, FRate 为等离子体产生率对应的函数表达式

    以下为发射选项可选参数
    isSpecies, species 为发射选项-粒子类型，species为 ELECTRON 或 PROTON
    isNumber, creationRate 为发射选项-产生率
    isTiming, timingType, stepMultiple 为发射选项-发射间隔，timingType为 TIMING 或 RANDOM_TIMING
    isSurfaceSpacing, surfaceSpacing 为发射选项-沿表面分布，surfaceSpacing为 RANDOM 或 UNIFORM 或 FIXED
    isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 FIXED

    以下为发射区域选项
    isEmit, mobject 为发射区域选项-发射体
    isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
    isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
    """

    EmECommandsStr = NEWLINE + ""

    # 定义有关函数

    coordinateSystemStr = ""
    if coordinateSystem == CoordinateSystem.rectangularSys:
        coordinateSystemStr = CoordinateSystem.rectangular4
    elif coordinateSystem == CoordinateSystem.polarSys:
        coordinateSystemStr = CoordinateSystem.polar4
    elif coordinateSystem == CoordinateSystem.cylindricalSys:
        coordinateSystemStr = CoordinateSystem.cylindrical4
    else:
        "EmE命令生成：请检查coordinateSystem的类型"

    if isBool(isOutwardSpacing):
        if isOutwardSpacing:
            DnName = emitName + ".Dn" + coordinateSystemStr
            funDn = Function(type=Function.Type.expression, functionName=DnName, functionExpression=dn)
            EmECommandsStr = EmECommandsStr + funDn.getFunctionStr() + newline
    else:
        return "EmE命令生成：请检查isOutwardSpacing的类型"

    if isBool(isTField):
        if isTField:
            TFieldName = emitName + ".TField" + coordinateSystemStr
            funTField = Function(type=Function.Type.expression, functionName=TFieldName, functionExpression=TField)
            EmECommandsStr = EmECommandsStr + funTField.getFunctionStr() + newline
    else:
        return "EmE命令生成：请检查isTField的类型"

    if isBool(isRField):
        if isRField:
            RFieldName = emitName + ".RField" + coordinateSystemStr
            funRField = Function(type=Function.Type.expression, functionName=RFieldName, functionExpression=RField)
            EmECommandsStr = EmECommandsStr + funRField.getFunctionStr() + newline
    else:
        return "EmE命令生成：请检查isRField的类型"

    if isBool(isFRate):
        if isFRate:
            FRateName = emitName + ".FRate" + coordinateSystemStr
            funFRate = Function(type=Function.Type.expression, functionName=FRateName, functionExpression=FRate)
            EmECommandsStr = EmECommandsStr + funFRate.getFunctionStr() + newline
    else:
        return "EmE命令生成：请检查isFRate的类型"

    if isBool(isCharg):
        if isCharg:
            ChargName = emitName + ".Charg" + coordinateSystemStr
            funCharg= Function(type=Function.Type.expression, functionName=ChargName, functionExpression=Charg)
            EmECommandsStr = EmECommandsStr + funCharg.getFunctionStr() + newline
    else:
        return "EmE命令生成：请检查isCharg的类型"


    # 定义EMISSION命令
    ## 检查常量字符串是否符合规范
    if species != EmissionOption.SpeciesType.electron and species != EmissionOption.SpeciesType.proton and species!="":
        return "EmE命令生成：请检查species"

    if timingType != EmissionOption.TimingType.timing and timingType != EmissionOption.TimingType.random_timing and timingType!="":
        return "EmE命令生成：请检查timingType"

    if surfaceSpacing != EmissionOption.SpacingType.random and surfaceSpacing != EmissionOption.SpacingType.uniform \
            and surfaceSpacing != EmissionOption.SpacingType.fixed and surfaceSpacing!="":
        return "EmE命令生成：请检查surfaceSpacing"

    if outwardSpacing != EmissionOption.SpacingType.random and outwardSpacing != EmissionOption.SpacingType.uniform \
        and outwardSpacing!="" and outwardSpacing != EmissionOption.SpacingType.fixed:
        return "EmE命令生成：请检查outwardSpacing"

    ## 转换数据类型
    if isNum(creationRate):
        creationRate = creationRate.__str__()

    if isNum(stepMultiple):
        stepMultiple = stepMultiple.__str__()

    ## 定义具体EMISSION命令
    emissionExplosive = EmissionExplosive(emitName, isTField, isRField, isCharg, isFRate)
    EmECommandsStr = EmECommandsStr + emissionExplosive.getEmissionExplosiveStr()
    # 由于沿外表面分布是几个发射的共有部分，但是eme属性略微不一样，所以在此处进行单独修改 @lzg
    # FreeCAD.Console.PrintError('\neme的沿外表面分布：'+str(outwardSpacing))
    if outwardSpacing != 'RANDOM':
        outwardSpacing = 'FIXED'

    emissionOptions = EmissionOption(emitName,
                                     isSpecies, species,
                                     isNumber, creationRate,
                                     isTiming, timingType, stepMultiple,
                                     isSurfaceSpacing, surfaceSpacing,
                                     isOutwardSpacing, outwardSpacing)
    EmECommandsStr = EmECommandsStr + emissionOptions.getEmissionExplosiveStr() + newline

    ## 定义具体EMIT命令
    if isBool(isEmit):
        if isEmit:
            emit = Emit(emitName, mobject,
                        isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                        isInclude1, includeVolume1, isInclude2, includeVolume2)
            EmECommandsStr = EmECommandsStr + emit.getEmitStr() + newline
    else:
        return "EmE命令生成：请检查isEmit的类型"

    return EmECommandsStr


def getEmGCommands(coordinateSystem, emitName, It, Bg, Pl, Pt, Dgc, pointCoordinates, isX1=False, isX2=False, isX3=False,
                   isSpecies=False, species="",
                   isNumber=False, creationRate="",
                   isTiming=False, timingType="", stepMultiple="",
                   isSurfaceSpacing=False, surfaceSpacing="",
                   isOutwardSpacing=False, outwardSpacing="", dn="",
                   isEmit=False, mobject="",
                   isExclude1=False, excludeVolume1="", isExclude2=False, excludeVolume2="",
                   isInclude1=False, includeVolume1="", isInclude2=False, includeVolume2=""
                   ):
    """
    EmG面板对应的命令组

    emitName 为名称
    It 为束电流
    Bg 为引导磁场
    Pl 为纵向动量
    Pt 为横向动量
    Dgc 为引导半径
    isX1, isX2, isX3 为引导轴线方向，X1为选择第一个，X2为选择第二个，X3为选择第三个
    pointCoordinates 为发射中心坐标，列表型数据

    以下为发射选项可选参数
    isSpecies, species 为发射选项-粒子类型，species为 ELECTRON 或 PROTON
    isNumber, creationRate 为发射选项-产生率
    isTiming, timingType, stepMultiple 为发射选项-发射间隔，timingType为 TIMING 或 RANDOM_TIMING
    isSurfaceSpacing, surfaceSpacing 为发射选项-沿表面分布，surfaceSpacing为 RANDOM 或 UNIFORM 或 FIXED
    isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 FIXED

    以下为发射区域选项
    isEmit, mobject 为发射区域选项-发射体
    isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
    isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
    """

    EmGCommandsStr = NEWLINE + ""

    # 定义有关函数
    coordinateSystemStr = ""
    if coordinateSystem == CoordinateSystem.rectangularSys:
        coordinateSystemStr = CoordinateSystem.rectangular4
    elif coordinateSystem == CoordinateSystem.polarSys:
        coordinateSystemStr = CoordinateSystem.polar4
    elif coordinateSystem == CoordinateSystem.cylindricalSys:
        coordinateSystemStr = CoordinateSystem.cylindrical4
    else:
        "EmG命令生成：请检查coordinateSystem的类型"

    if isBool(isOutwardSpacing):
        if isOutwardSpacing:
            DnName = emitName + ".Dn" + coordinateSystemStr
            funDn = Function(type=Function.Type.expression, functionName=DnName, functionExpression=dn)
            EmGCommandsStr = EmGCommandsStr + funDn.getFunctionStr() + newline
    else:
        return "EmG命令生成：请检查isOutwardSpacing的类型"

    ItName = emitName + ".I(T)"
    funIt = Function(type=Function.Type.expression, functionName=ItName, functionExpression=It)
    EmGCommandsStr = EmGCommandsStr + funIt.getFunctionStr() + newline

    # 定义有关点
    if not isList(pointCoordinates):
        return "EmG命令生成：请检查pointCoordinates是否为list类型"

    ponitName = emitName + ".CPT"
    point = Point(ponitName, pointCoordinates)
    EmGCommandsStr = EmGCommandsStr + point.getPonitStr() + newline

    # 定义EMISSION命令
    ## 检查常量字符串是否符合规范
    if species != EmissionOption.SpeciesType.electron and species != EmissionOption.SpeciesType.proton and species != "":
        return "EmG命令生成：请检查species"

    if timingType != EmissionOption.TimingType.timing and timingType != EmissionOption.TimingType.random_timing and timingType != "":
        return "EmG命令生成：请检查timingType"

    if surfaceSpacing != EmissionOption.SpacingType.random and surfaceSpacing != EmissionOption.SpacingType.uniform \
            and surfaceSpacing != EmissionOption.SpacingType.fixed and surfaceSpacing != "":
        return "EmG命令生成：请检查surfaceSpacing"

    if outwardSpacing != EmissionOption.SpacingType.random and outwardSpacing != EmissionOption.SpacingType.fixed and outwardSpacing != "":
        return "EmG命令生成：请检查outwardSpacing"

    ## 转换数据类型
    if isNum(creationRate):
        creationRate = creationRate.__str__()

    if isNum(stepMultiple):
        stepMultiple = stepMultiple.__str__()

    ## 定义具体EMISSION命令
    direction = EmissionGyro.Direction.x1  # 默认为x1
    if isBool(isX1):
        if isX1:
            direction = EmissionGyro.Direction.x1
    else:
        return "EmG命令生成：请检查isX1的类型"

    if isBool(isX2):
        if isX2:
            direction = EmissionGyro.Direction.x2
    else:
        return "EmG命令生成：请检查isX2的类型"

    if isBool(isX3):
        if isX3:
            direction = EmissionGyro.Direction.x3
    else:
        return "EmG命令生成：请检查isX3的类型"

    emissionGyro = EmissionGyro(emitName, Bg, Pl, Pt, Dgc, direction)
    EmGCommandsStr = EmGCommandsStr + emissionGyro.getEmissionGyroStr()

    emissionOptions = EmissionOption(emitName,
                                     isSpecies, species,
                                     isNumber, creationRate,
                                     isTiming, timingType, stepMultiple,
                                     isSurfaceSpacing, surfaceSpacing,
                                     isOutwardSpacing, outwardSpacing)
    EmGCommandsStr = EmGCommandsStr + emissionOptions.getEmissionExplosiveStr() + newline

    ## 定义具体EMIT命令
    if isBool(isEmit):
        if isEmit:
            emit = Emit(emitName, mobject,
                        isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                        isInclude1, includeVolume1, isInclude2, includeVolume2)
            EmGCommandsStr = EmGCommandsStr + emit.getEmitStr() + newline
    else:
        return "EmG命令生成：请检查isEmit的类型"

    return EmGCommandsStr


def getEmHCommands(coordinateSystem, emitName, A, B, PHI,
                   isSpecies=False, species="",
                   isNumber=False, creationRate="",
                   isTiming=False, timingType="", stepMultiple="",
                   isSurfaceSpacing=False, surfaceSpacing="",
                   isOutwardSpacing=False, outwardSpacing="", dn="",
                   isEmit=False, mobject="",
                   isExclude1=False, excludeVolume1="", isExclude2=False, excludeVolume2="",
                   isInclude1=False, includeVolume1="", isInclude2=False, includeVolume2=""
                   ):
    """
    EmH面板对应的命令组

    emitName 为名称
    A 为常数A
    B 为常数B
    PHI 为工作函数

    以下为发射选项可选参数
    isSpecies, species 为发射选项-粒子类型，species为 ELECTRON 或 PROTON
    isNumber, creationRate 为发射选项-产生率
    isTiming, timingType, stepMultiple 为发射选项-发射间隔，timingType为 TIMING 或 RANDOM_TIMING
    isSurfaceSpacing, surfaceSpacing 为发射选项-沿表面分布，surfaceSpacing为 RANDOM 或 UNIFORM 或 FIXED
    isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 FIXED

    以下为发射区域选项
    isEmit, mobject 为发射区域选项-发射体
    isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
    isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
    """

    EmHCommandsStr = NEWLINE + ""

    # 定义有关函数
    coordinateSystemStr = ""
    if coordinateSystem == CoordinateSystem.rectangularSys:
        coordinateSystemStr = CoordinateSystem.rectangular4
    elif coordinateSystem == CoordinateSystem.polarSys:
        coordinateSystemStr = CoordinateSystem.polar4
    elif coordinateSystem == CoordinateSystem.cylindricalSys:
        coordinateSystemStr = CoordinateSystem.cylindrical4
    else:
        "EmH命令生成：请检查coordinateSystem的类型"

    if isBool(isOutwardSpacing):
        if isOutwardSpacing:
            DnName = emitName + ".Dn" + coordinateSystemStr
            funDn = Function(type=Function.Type.expression, functionName=DnName, functionExpression=dn)
            EmHCommandsStr = EmHCommandsStr + funDn.getFunctionStr() + newline
    else:
        return "EmH命令生成：请检查isOutwardSpacing的类型"

    PHIName = emitName + ".PHI" + coordinateSystemStr
    funPHI = Function(type=Function.Type.expression, functionName=PHIName, functionExpression=PHI)
    EmHCommandsStr = EmHCommandsStr + funPHI.getFunctionStr() + newline

    # 定义EMISSION命令
    ## 检查常量字符串是否符合规范
    if species != EmissionOption.SpeciesType.electron and species != EmissionOption.SpeciesType.proton and species != "":
        return "EmH命令生成：请检查species"

    if timingType != EmissionOption.TimingType.timing and timingType != EmissionOption.TimingType.random_timing and timingType != "":
        return "EmH命令生成：请检查timingType"

    if surfaceSpacing != EmissionOption.SpacingType.random and surfaceSpacing != EmissionOption.SpacingType.uniform \
            and surfaceSpacing != EmissionOption.SpacingType.fixed and surfaceSpacing != "":
        return "EmH命令生成：请检查surfaceSpacing"

    if outwardSpacing != EmissionOption.SpacingType.random and outwardSpacing != EmissionOption.SpacingType.fixed and outwardSpacing != "":
        return "EmH命令生成：请检查outwardSpacing"

    ## 转换数据类型
    if isNum(creationRate):
        creationRate = creationRate.__str__()

    if isNum(stepMultiple):
        stepMultiple = stepMultiple.__str__()

    ## 定义具体EMISSION命令
    emissionHighfield = EmissionHighfield(emitName, A, B)
    EmHCommandsStr = EmHCommandsStr + emissionHighfield.getEmissionHighfieldStr()

    emissionOptions = EmissionOption(emitName,
                                     isSpecies, species,
                                     isNumber, creationRate,
                                     isTiming, timingType, stepMultiple,
                                     isSurfaceSpacing, surfaceSpacing,
                                     isOutwardSpacing, outwardSpacing)
    EmHCommandsStr = EmHCommandsStr + emissionOptions.getEmissionExplosiveStr() + newline

    ## 定义具体EMIT命令
    if isBool(isEmit):
        if isEmit:
            emit = Emit(emitName, mobject,
                        isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                        isInclude1, includeVolume1, isInclude2, includeVolume2)
            EmHCommandsStr = EmHCommandsStr + emit.getEmitStr() + newline
    else:
        return "EmG命令生成：请检查isEmit的类型"

    return EmHCommandsStr


def getEmTCommands(coordinateSystem, emitName, WF, TP,
                   isSpecies=False, species="",
                   isNumber=False, creationRate="",
                   isTiming=False, timingType="", stepMultiple="",
                   isSurfaceSpacing=False, surfaceSpacing="",
                   isOutwardSpacing=False, outwardSpacing="", dn="",
                   isEmit=False, mobject="",
                   isExclude1=False, excludeVolume1="", isExclude2=False, excludeVolume2="",
                   isInclude1=False, includeVolume1="", isInclude2=False, includeVolume2=""
                   ):
    """
    EmH面板对应的命令组

    emitName 为名称
    WF 为工作函数
    TP 为工作温度

    以下为发射选项可选参数
    isSpecies, species 为发射选项-粒子类型，species为 ELECTRON 或 PROTON
    isNumber, creationRate 为发射选项-产生率
    isTiming, timingType, stepMultiple 为发射选项-发射间隔，timingType为 TIMING 或 RANDOM_TIMING
    isSurfaceSpacing, surfaceSpacing 为发射选项-沿表面分布，surfaceSpacing为 RANDOM 或 UNIFORM 或 FIXED
    isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 FIXED

    以下为发射区域选项
    isEmit, mobject 为发射区域选项-发射体
    isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
    isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
    """

    EmTCommandsStr = NEWLINE + ""

    # 定义有关函数
    coordinateSystemStr = ""
    if coordinateSystem == CoordinateSystem.rectangularSys:
        coordinateSystemStr = CoordinateSystem.rectangular4
    elif coordinateSystem == CoordinateSystem.polarSys:
        coordinateSystemStr = CoordinateSystem.polar4
    elif coordinateSystem == CoordinateSystem.cylindricalSys:
        coordinateSystemStr = CoordinateSystem.cylindrical4
    else:
        "EmG命令生成：请检查coordinateSystem的类型"

    if isBool(isOutwardSpacing):
        if isOutwardSpacing:
            DnName = emitName + ".Dn" + coordinateSystemStr
            funDn = Function(type=Function.Type.expression, functionName=DnName, functionExpression=dn)
            EmTCommandsStr = EmTCommandsStr + funDn.getFunctionStr() + newline
    else:
        return "EmG命令生成：请检查isOutwardSpacing的类型"

    WFName = emitName + ".WF" + coordinateSystemStr
    funWF = Function(type=Function.Type.expression, functionName=WFName, functionExpression=WF)
    EmTCommandsStr = EmTCommandsStr + funWF.getFunctionStr() + newline

    TPName = emitName + ".TP" + coordinateSystemStr
    funTP= Function(type=Function.Type.expression, functionName=TPName, functionExpression=TP)
    EmTCommandsStr = EmTCommandsStr + funTP.getFunctionStr() + newline

    # 定义EMISSION命令
    ## 检查常量字符串是否符合规范
    if species != EmissionOption.SpeciesType.electron and species != EmissionOption.SpeciesType.proton and species != "":
        return "EmT命令生成：请检查species"

    if timingType != EmissionOption.TimingType.timing and timingType != EmissionOption.TimingType.random_timing and timingType != "":
        return "EmT命令生成：请检查timingType"

    if surfaceSpacing != EmissionOption.SpacingType.random and surfaceSpacing != EmissionOption.SpacingType.uniform \
            and surfaceSpacing != EmissionOption.SpacingType.fixed and surfaceSpacing != "":
        return "EmT命令生成：请检查surfaceSpacing"

    if outwardSpacing != EmissionOption.SpacingType.random and outwardSpacing != EmissionOption.SpacingType.fixed and outwardSpacing != "":
        return "EmT命令生成：请检查outwardSpacing"

    ## 转换数据类型
    if isNum(creationRate):
        creationRate = creationRate.__str__()

    if isNum(stepMultiple):
        stepMultiple = stepMultiple.__str__()

    ## 定义具体EMISSION命令
    emissionThermionic = EmissionThermionic(emitName)
    EmTCommandsStr = EmTCommandsStr + emissionThermionic.getEmissionExplosiveStr()

    emissionOptions = EmissionOption(emitName,
                                     isSpecies, species,
                                     isNumber, creationRate,
                                     isTiming, timingType, stepMultiple,
                                     isSurfaceSpacing, surfaceSpacing,
                                     isOutwardSpacing, outwardSpacing)
    EmTCommandsStr = EmTCommandsStr + emissionOptions.getEmissionExplosiveStr() + newline

    ## 定义具体EMIT命令
    if isBool(isEmit):
        if isEmit:
            emit = Emit(emitName, mobject,
                        isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                        isInclude1, includeVolume1, isInclude2, includeVolume2)
            EmTCommandsStr = EmTCommandsStr + emit.getEmitStr() + newline
    else:
        return "EmT命令生成：请检查isEmit的类型"

    return EmTCommandsStr


def getTimerCommands(timerName, type, numType, stratTime="", stopTime="", timeIncrement="", triggerTimes=""):
    """    
    :param timerName: 定时器名称
    :param type: 定时器类型，PERIODIC 或 DISCRETE
    :param numType: 定时基准类型，INTEGER 或 REAL
    :param stratTime: 起始时刻
    :param stopTime: 结束时刻
    :param timeIncrement: 定时周期
    :param triggerTimes: 离散触发时间列表，暂时还没有实现
    :return: 
    """

    # 判断常变量是否符合要求
    if type != Timer.Type.periodic and type != Timer.Type.discrete:
        return "Timer命令生成，请检查type的值"

    if numType != Timer.NumType.integer and numType != Timer.NumType.real:
        return "Timer命令生成，请检查numType的值"

    # 生成具体命令
    timerCommandsStr = NEWLINE + "!!" + timerName + NEWLINE

    timer =Timer(timerName, type, numType, stratTime, stopTime, timeIncrement, triggerTimes)
    timerCommandsStr = timerCommandsStr + timer.getTimerStr() + NEWLINE

    return timerCommandsStr


def getContourCommands(panelName, name, field, timerName, isShade=False):
    """
    等位图观测面板对应的命令组
    :param panelName: 面板名称
    :param name: 投影面名称
    :param field: 对应观测场
    :param timerName: 对应定时器，默认的有DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
    :param isShade: 对应是否等值线填充显示
    :return: 
    """
    returnStr = NEWLINE + "!!" + panelName + NEWLINE

    contour = Contour(field, name, timerName, isShade)
    returnStr = returnStr + contour.getContourStr() + NEWLINE

    return returnStr


def getVectorCommands(panelName, field1, field2, name, timerName, isNumber=False, number1="", number2=""):

    """
    矢量图观测
    :param panelName: 面板名称
    :param field1: 观测场1
    :param field2: 观测场2
    :param name: 对应面板名称或投影面名称
    :param timerName: 定时器，默认的有DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
    :param isNumber: 是否指定矢量个数
    :param number1: 矢量个数第一个空
    :param number2: 矢量个数第二个空
    :return: 
    """

    returnStr = NEWLINE + "!!" + panelName + NEWLINE

    vector = Vector(field1, field2, name, timerName, isNumber, number1, number2)
    returnStr = returnStr + vector.getVectorStr() + NEWLINE

    return returnStr


def getPhasespaceCommands(panelName, horizontalAxis, verticalAxis,
                 timerName,
                 species,
                 isThickness=False, direction="", thickness1="", thickness2="",
                 isSuffix=False, suffix=""):
    """
    粒子相空间观测
    :param panelName: 面板名称
    :param horizontalAxis: 横轴显示
    :param verticalAxis: 纵轴显示
    :param timerName: 定时器,默认的有DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
    :param species: 粒子类型，ELECTRON、PROTON、ALL中的一种
    :param isThickness: 是否显示厚度
    :param direction: 显示厚度- 方向，X1、X2、X3中的一种
    :param thickness1: 显示厚度 - 数据1
    :param thickness2: 显示厚度 - 数据2
    :param isSuffix: 是否有后缀
    :param suffix: 后缀值
    :return: 
    """

    # 检查常变量是否符合规范
    if species!=Phasespace.SpeciesType.all and species!=Phasespace.SpeciesType.proton and species!=Phasespace.SpeciesType.electron:
        return "Phasespace命令组生成：请检查species"

    if direction!=Phasespace.Direction.x1 and direction!=Phasespace.Direction.x2 and direction!=Phasespace.Direction.x3:
        return "Phasespace命令组生成：请检查direction"

    phasespace = Phasespace(horizontalAxis, verticalAxis, timerName, species,
                 isThickness, direction, thickness1, thickness2,
                 isSuffix, suffix)

    returnStr = NEWLINE + "!!" + panelName + NEWLINE
    returnStr = returnStr + phasespace.getPhasespaceStr() + NEWLINE

    return returnStr


def getRangeCommands(panelName, name, field, timerName, isFFT=False, isMagnitude=False, isComplex=False):
    """
    空间观测
    :param panelName: 面板名称
    :param field: 分类子项的具体值
    :param name: 空间观测线或
    :param timerName: 定时器，默认的有DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
    :param isFFT: 是否进行快速傅里叶变化
    :param isMagnitude: 是否进行实分析
    :param isComplex: 是否进行复分析
    :return: 
    """
    range = Range(field, name, timerName, isFFT, isMagnitude, isComplex)

    returnStr = NEWLINE + "!!" + panelName + NEWLINE
    returnStr = returnStr + range.getRangeStr() + NEWLINE

    return returnStr


def getObserveCommands(panelName, isField=False, isFieldIntegral=False, isFieldPower=False, isFieldEnergy=False, isParticleStatistics=False,
                        isParticleCollected=False,isParticleEmitted=False,isParticleDestroyed=False,
                        field="", objectName="",
                        isFFT=False, fftType="", isFreq=False,freqFrom="", freqTo="",
                        isTime=False, timeFrom="", timeTo="",
                        isInterval=False, interval="",
                        isFilter=False, filterType="", timePara="",name2 = ''):
    """
    时间观测
    :param panelName:面板名称
    :param isField: 是否选择了场分类项
    :param isFieldIntegral: 是否选择了场积分分类项
    :param isFieldPower: 是否选择了场功率分类项
    :param isFieldEnergy: 是否选择了场能量分类项
    :param isEmitEps: 是否选择了粒子统计
    :param isParticleCollected: 是否选择了收集的粒子
    :param isParticleEmitted：是否选择了发射的粒子
    :param isParticleDestroyed：是否选择了湮灭的粒子
    :param field: 观测项对应的分类子项
    :param objectName: 引用的物体的名称
    
    以下是可选项
    :param isFFT: 是否进行快速傅里叶变换
    :param fftType: FFT类型，这里的值为 MAGNITUDE（实分析）、COMPLEX（复分析）
    :param freqFrom: 频率范围起点
    :param freqTo: 频率范围终点
    :param isTime: 是否选择时间范围
    :param timeFrom: 时间范围起点
    :param timeTo: 时间范围重点
    :param isInterval：是否观察间隔
    :param interval：观察间隔
    :param isFilter: 是否数据显示平滑处理
    :param filterType: 平滑处理类型，这里的值为 STEP（时间平均）、LO_PASS（RC分析）
    :param timePara: RC分析
    :return: 
    """

    # 检查常变量是否符合要求
    if fftType != ObserveOptionFFT.FFTType.complex and fftType != ObserveOptionFFT.FFTType.magnitude:
        return "observe命令生成，请检查fftType"

    if filterType != ObserveOptionFilter.FilterType.step and filterType != ObserveOptionFilter.FilterType.loPass:
        return "observe命令生成，请检查filterType"

    returnStr = ""

    # 生成原始命令
    if isBool(isField):
        if isField:
            observeField = ObserveField(field[0], objectName,name2)
            returnStr = returnStr + observeField.getObserveFieldStr()
    else:
        return "observe命令生成，请检查isField"

    if isBool(isFieldIntegral):
        if isFieldIntegral:
            observeFieldIntegral = ObserveFieldIntegral(field[0], objectName,name2)
            returnStr = returnStr + observeFieldIntegral.getObserveFieldIntegralStr()
    else:
        return "observe命令生成，请检查isFieldIntegral"

    if isBool(isFieldPower):
        if isFieldPower:
            observeFieldPower = ObserveFieldPower(field[0], objectName,name2)
            returnStr = returnStr + observeFieldPower.getObserveFieldPowerStr()
    else:
        return "observe命令生成，请检查isFieldPower"

    if isBool(isFieldEnergy):
        if isFieldEnergy:
            observeFieldEnergy = ObserveFieldEnergy(field[0], objectName,name2)
            returnStr = returnStr + observeFieldEnergy.getObserveFieldEnergyStr()
    else:
        return "observe命令生成，请检查isFieldEnergy"

    if isBool(isParticleStatistics):
        if isParticleStatistics:
            observeParticleStatistics = ObserveParticleStatistics(field[0],field[1],objectName,name2)
            returnStr = returnStr + observeParticleStatistics.getObserveParticleStatisticsStr()
    else:
        return "observe命令生成，请检查isParticleStatistics"

    if isBool(isParticleCollected):
        if isParticleCollected:
            observeParticle = ObserveParticle("COLLECTED",field[0],field[1],objectName,name2)
            returnStr = returnStr + observeParticle.getObserveParticleStr()
    else:
        return "observe命令生成，请检查isParticleCollected"

    if isBool(isParticleEmitted):
        if isParticleEmitted:
            observeParticle = ObserveParticle("EMITTED",field[0],field[1],objectName,name2)
            returnStr = returnStr + observeParticle.getObserveParticleStr()
    else:
        return "observe命令生成，请检查isParticleEmitted"

    if isBool(isParticleDestroyed):
        if isParticleDestroyed:
            observeParticle = ObserveParticle("DESTROYED",field[0],field[1],objectName,name2)
            returnStr = returnStr + observeParticle.getObserveParticleStr()
    else:
        return "observe命令生成，请检查isParticleDestroyed"

    # 生成带可选项的命令
    returnStrOri = returnStr[0:len(returnStr)-1]

    if isBool(isFilter):
        if isFilter:
            returnStr = returnStr + newline + returnStrOri
            observeOptionFilter = ObserveOptionFilter(filterType, timePara)
            returnStr = returnStr + observeOptionFilter.getObserveOptionFilterStr()
    else:
        return "observe命令生成，请检查isFilter"

    if isBool(isFFT):
        if isFFT:
            returnStr = returnStr + newline + returnStrOri
            observeOptionFFT = ObserveOptionFFT(fftType,isFreq,freqFrom,freqTo)
            returnStr = returnStr + observeOptionFFT.getObserveOptionFFTStr()
            # 由于额外带了一行多余的m3d，进行修改，修改待确定@ lizhenguang
            # observeOptionFFT = ObserveOptionFFT(fftType, freqFrom, freqTo)
            # returnStr = returnStrOri + observeOptionFFT.getObserveOptionFFTStr()
    else:
        return "observe命令生成，请检查isFFT"
    # if isBool(isFreq):
    #     if isFreq:
    #         returnStr = returnStr + newline + returnStrOri
    #         observeOptionFreq = ObserveOptionFreq(freqFrom, freqTo)
    #         returnStr = returnStr + observeOptionFreq.getObserveOptionFreqStr()

    # else:
    #     return "observe命令生成，请检查isFFT"
    
    if isBool(isTime):
        if isTime:
            returnStr = returnStr + newline + returnStrOri
            observeOptionTime = ObserveOptionTime(timeFrom, timeTo)
            returnStr = returnStr + observeOptionTime.getObserveOptionTimeStr()
    else:
        return "observe命令生成，请检查isFFT"

    if isBool(isInterval):
        if isInterval:
            returnStr = returnStr + newline + returnStrOri
            observeOptionInterval = ObserveOptionInterval(interval)
            returnStr = returnStr + observeOptionInterval.getObserveOptionIntervalStr()
    else:
        return "observe命令生成，请检查isFFT"

    # if name2 == '':
    #     pass
    # else:
    #     returnStr = returnStr.replace(';','') + ' ' + 'suffix' + ' ' + str(name2) + 'Voltage' + ';'
    return NEWLINE + "!!" + panelName + NEWLINE + returnStr + newline


def getSolendCommands(type, name, zCenter, rCenter, innerRadius, outerRadius, coilCurrent, coilRadius, coilNum,
                      theta, phi, rFactor, zFactor, spaceRatio, innerRadius2, outerRadius2, magneticRatio):
    """
    螺旋线线圈
    :param type: 匀场环因子 none rz other
    :param name: 名称
    :param zCenter: z中心
    :param rCenter: r中心
    :param innerRadius: 左 内半径
    :param outerRadius: 左 外半径
    :param coilCurrent: 线圈电流
    :param coilRadius: 线圈半长
    :param coilNum: 线圈匝数
    :param theta: theta角度
    :param phi: phi角度
    :param rFactor: r因子
    :param zFactor: z因子
    :param spaceRatio: 占空比
    :param innerRadius2: 右 内半径
    :param outerRadius2: 右 外半径
    :param magneticRatio: 磁导率
    :return: 
    """
    # 检查类型
    if type != Solenoid.Type.none and type != Solenoid.Type.rz and type != Solenoid.Type.other:
        return "Solenoid命令生成，请检查type"
    else:
        solenoid = Solenoid(type, name, zCenter, rCenter, innerRadius, outerRadius, coilCurrent, coilRadius, coilNum,
                            theta, phi, rFactor, zFactor, spaceRatio, innerRadius2, outerRadius2, magneticRatio)
        return NEWLINE + solenoid.getSolenoidStr() + NEWLINE


def getFoilCommands(name, thick, isDIY, DITMaterial, isDefault, defaultMaterial,type=''):
    """

    :param name: 名称
    :param thick: 厚度
    :param isDIY: 是否为自定义材料
    :param DITMaterial: 自定义材料名称
    :param isDefault: 是否为默认材料
    :param defaultMaterial: 默认材料名称
    :param type :类型箔片
    :return: 
    """
    returnStr=""
    returnStr = NEWLINE + "!!" + name + NEWLINE
    if not isBool(isDIY):
        return "Foil命令生成，请检查isDIY"

    if not isBool(isDefault):
        return "Foil命令生成，请检查isDefault"

    if isDefault and isDIY:
        return "Foil命令生成，isDefault与isDIY不能都是true"
    elif not isDefault and not isDIY:
        return "Foil命令生成，isDefault与isDIY不能都是False"
    elif isDefault:
        material = defaultMaterial
    elif isDIY:
        material = DITMaterial

    if type == u'未指定':
        foil = Foil(name, thick, material)
    else :
        foil = Foil(type, thick, material)
    return returnStr + foil.getFoilStr() + NEWLINE


def getInductorCommands(name, diameter, isInductance, inductance):
    """
    电感
    :param name:名称 
    :param diameter:线圈直径 
    :param isInductance: 是否设置自感系数
    :param inductance: 自感系数
    :return: 
    """

    if isBool(isInductance):
        inductor = Inductor(name, diameter, isInductance, inductance)
        return NEWLINE + inductor.getInductorStr() + NEWLINE
    else:
        return "Inductor命令生成，请检查isInductance"


def getDriverCommands(coordinateSystem, name, currentDensity, funExpression,source_type):
    """
    空间电流源
    :param coordinateSystem: 坐标系标识
    :param name: 名称
    :param currentDensity: 指定电流密度 
    :param funExpression: 函数表达式
    :param source_type:具体指定的点线面或体
    :return: 
    """

    returnStr = NEWLINE

    # 定义函数的命令

    coordinateSystemStr = ""
    if coordinateSystem == CoordinateSystem.rectangularSys:
        coordinateSystemStr = CoordinateSystem.rectangular4
    elif coordinateSystem == CoordinateSystem.polarSys:
        coordinateSystemStr = CoordinateSystem.polar4
    elif coordinateSystem == CoordinateSystem.cylindricalSys:
        coordinateSystemStr = CoordinateSystem.cylindrical4
    else:
        "Driver命令生成：请检查coordinateSystem的类型"

    funName = name + ".JFUNC" + coordinateSystemStr
    fun = Function(type=Function.Type.expression, functionName=funName, functionExpression=funExpression)
    returnStr = returnStr + fun.getFunctionStr() + NEWLINE

    # 获得drive命令
    funName = name + ".JFUNC"
    drive = Driver(name, currentDensity, funName,source_type)
    returnStr = returnStr + drive.getDriverStr() + NEWLINE

    return returnStr

def getTimeComputationCommands(time="", algorithm="",
                       isPattern=False, pattern="",
                       isStep=False, step="",
                       isChargeAlgorithm=False,
                       Types = "",
                       EveryNum = "",MaxNum = "",
                       isChecked_part = False,
                       checkBoxStep = False,
                       computeTimeInterval = "1",
                       is_re = False,
                       is_nonre = False):
    """
    
    :param time: 计算时间
    :param algorithm: 设置场算法 CENTERED \ HIGH_Q \ BIASED
    :param isPattern: 是否设置模式
    :param pattern: 模式 TE \ TM \ EM
    :param isStep: 是否设置步长
    :param step: 步长
    :param isChargeAlgorithm: 是否设置电荷连续性算法
    :return: 
    """
    returnStr = NEWLINE
    # KINEMATICS 命令@lzg
    if isBool(checkBoxStep):
        if checkBoxStep:
            kine = Kinematics(computeTimeInterval,is_re,is_nonre)
            returnStr = returnStr + kine.getKinematicsStr() + NEWLINE
    # 生成maxwell命令
    if algorithm!=Maxwell.Type.biased and algorithm!=Maxwell.Type.high_q and algorithm!=Maxwell.Type.centered:
        return "时域计算设置，请检查algorithm"

    maxwell = Maxwell(algorithm)
    returnStr = returnStr + maxwell.getMaxwellStr() + NEWLINE

    # 生成mode命令
    if isBool(isPattern):
        if isPattern:
            if pattern != Mode.Type.TE and pattern != Mode.Type.TM and pattern != Mode.Type.EM:
                return "时域计算设置，请检查pattern"

            if pattern==Mode.Type.EM:
                pattern = Mode.Type.BOTH

            mode = Mode(pattern)
            returnStr = returnStr + mode.getModeStr() + NEWLINE
    else:
        return "时域计算设置，请检查isPattern"

    # 生成time_step命令
    if isBool(isStep):
        if isStep:
            # FreeCAD.Console.PrintError('\n step::'+str(type(step)))
            # FreeCAD.Console.PrintError('\n step::'+str(type(step)))
            if isNum(step):
                step = step.__str__()

            step_instance = TimeStep(step)
            
            if isNumber(step): 
                returnStr = returnStr + step_instance.getTimeStepStr() + NEWLINE
            else:
                returnStr = returnStr + step_instance.getTimeStepStrWithoutUnits() + NEWLINE 
    else:
        return "时域计算设置，请检查isStep"

    # 生成continuity命令
    if isBool(isChargeAlgorithm):
        if isChargeAlgorithm:
            continuity = Continuity(Continuity.Type.conserved)
            returnStr = returnStr + continuity.getContinuityStr() + NEWLINE
    else:
        return "时域计算设置，请检查isChargeAlgorithm"
    

    # 生成duration命令
    if isNum(time):
        time = time.__str__()
    duration = Duration(time)
    # @lizhenguang
    if isNumber(time):
    # if isNumjustforTimeStep(time):
        returnStr = returnStr + duration.getDurationStr() + NEWLINE
    else:
        returnStr = returnStr + duration.getDurationwithoutunits() + NEWLINE
    # @lizhenugyang
    if isChecked_part:
        name = ''
        FreeCAD.Console.PrintError("\n进入加载get的数据过程")
        Merge_instance = Merge(name,Types,EveryNum,MaxNum)
        returnStr = returnStr + Merge_instance.getMergeStr() + NEWLINE
        FreeCAD.Console.PrintError("\n执行完get的数据过程")

    return returnStr


def getDataExportCommands(fileName, isObs=True, isRan=True, isCntr=True, isVec=True, isPha=True,
                          isPrefix=False, prefix="",
                          isSuffix=False, suffix="",
                          isASCII=True):
    """
    
    :param fileName: 文件命（无后缀）
    :param isObs: 导出数据是否包括时间观测
    :param isRan: 导出数据是否包括空间观测
    :param isCntr: 导出数据是否包括等位图观测
    :param isVec: 导出数据是否包括矢量图观测
    :param isPha: 导出数据是否包括相空间观测
    :param isPrefix: 是否设置前缀
    :param prefix: 前缀
    :param isSuffix: 是否设置后缀
    :param suffix: 后缀
    :param isASCII: 导出格式是否为文本格式, 没有选择的话则默认为二进制格式
    :return: 
    """

    returnStr =NEWLINE

    # 生成NAME
    if len(fileName.split("."))>1:
        fileName = fileName.split(".")[0] + "_TIME"
    dump = Dump(Dump.Type.name, fileName)
    returnStr = returnStr + dump.getDumpStr() + NEWLINE

    # 生成PREFIX
    if isBool(isPrefix):
        if isPrefix:
            prefix = "\""+ prefix + "\""
            dump = Dump(Dump.Type.prefix, prefix)
            returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isPrefix"

    # 生成SUFFIX
    if isBool(isSuffix):
        if isSuffix:
            suffix = "\""+ suffix + "\""
            dump = Dump(Dump.Type.suffix, suffix)
            returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isSuffix"

    # 生成FORMAT
    if isBool(isASCII):
        if isASCII:
            format = Dump.FormatType.ascii
        else:
            format = Dump.FormatType.binary

        dump = Dump(Dump.Type.format, format)
        returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isASCII"

    # 生成TYPE
    if isBool(isObs):
        if isObs:
            dump = Dump(Dump.Type.type, Dump.DataType.observe)
            returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isObs"

    if isBool(isRan):
        if isRan:
            dump = Dump(Dump.Type.type, Dump.DataType.range)
            returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isRan"

    if isBool(isCntr):
        if isCntr:
            dump = Dump(Dump.Type.type, Dump.DataType.contour)
            returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isCntr"

    if isBool(isVec):
        if isVec:
            dump = Dump(Dump.Type.type, Dump.DataType.vector)
            returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isVec"

    if isBool(isPha):
        if isPha:
            dump = Dump(Dump.Type.type, Dump.DataType.phasespace)
            returnStr = returnStr + dump.getDumpStr() + NEWLINE
    else:
        return "数据处理设置，请检查isPha"

    return returnStr


def getRunOptionCommands(isDisplay=True, isPause=False):
    """
    :param isDisplay: 开始计算时是否显示结构图
    :param isPause: 开始计算时处于暂停状态
    :return: 
    """
    returnStr = NEWLINE

    if isBool(isPause):
        if isPause:
            returnStr = returnStr + "GRAPHICS PAUSE;" + NEWLINE
    else:
        return "运行选项设置，请检查isPause"

    if isBool(isDisplay):
        if isDisplay:
            returnStr = returnStr + "DISPLAY ;" + NEWLINE
    else:
        return "运行选项设置，请检查isDisplay"

    return returnStr


def getPresetCommands(coordinateSystem="P",
                      isSetB1=False, setB1="", isSetB2=False, setB2="", isSetB3=False, setB3="",
                      isSetE1=False, setE1="", isSetE2=False, setE2="", isSetE3=False, setE3="",
                      diySet=""):
    """
    
    :param isSetB1: 是否进行静磁场1设置
    :param setB1: 静磁场1设置
    :param isSetB2: 是否进行静磁场2设置
    :param setB2: 静磁场2设置
    :param isSetB3: 是否进行静磁场3设置
    :param setB3: 静磁场3设置
    :param isSetE1: 是否进行静电场1设置
    :param setE1: 静电场1设置
    :param isSetE2: 是否进行静电场2设置
    :param setE2: 静电场2设置
    :param isSetE3: 是否进行静电场3设置
    :param setE3: 静电场3设置
    :param diySet: 场的自定义
    :return: 
    """
    returnStr = NEWLINE + diySet + NEWLINE
    if isBool(isSetB1):
        if isSetB1:
            preset = Preset(Preset.Type.B1ST, coordinateSystem)            
            function = Function(functionName=preset.getFunN(), functionExpression=setB1)

            returnStr = returnStr + function.getFunctionStr() + NEWLINE
            returnStr = returnStr + preset.getPresetStr() + NEWLINE
    else:
        return "场环境设置，请检查isSetB1"
    
    if isBool(isSetB2):
        if isSetB2:
            preset = Preset(Preset.Type.B2ST, coordinateSystem)            
            function = Function(functionName=preset.getFunN(), functionExpression=setB2)

            returnStr = returnStr + function.getFunctionStr() + NEWLINE
            returnStr = returnStr + preset.getPresetStr() + NEWLINE
    else:
        return "场环境设置，请检查isSetB2"
    
    if isBool(isSetB3):
        if isSetB3:
            preset = Preset(Preset.Type.B3ST, coordinateSystem)            
            function = Function(functionName=preset.getFunN(), functionExpression=setB3)

            returnStr = returnStr + function.getFunctionStr() + NEWLINE
            returnStr = returnStr + preset.getPresetStr() + NEWLINE
    else:
        return "场环境设置，请检查isSetB3"
    
    if isBool(isSetE1):
        if isSetE1:
            preset = Preset(Preset.Type.E1ST, coordinateSystem)            
            function = Function(functionName=preset.getFunN(), functionExpression=setE1)

            returnStr = returnStr + function.getFunctionStr() + NEWLINE
            returnStr = returnStr + preset.getPresetStr() + NEWLINE
    else:
        return "场环境设置，请检查isSetE1"
    
    if isBool(isSetE2):
        if isSetE2:
            preset = Preset(Preset.Type.E2ST, coordinateSystem)            
            function = Function(functionName=preset.getFunN(), functionExpression=setE2)

            returnStr = returnStr + function.getFunctionStr() + NEWLINE
            returnStr = returnStr + preset.getPresetStr() +NEWLINE
    else:
        return "场环境设置，请检查isSetE2"
    
    if isBool(isSetE3):
        if isSetE3:
            preset = Preset(Preset.Type.E3ST, coordinateSystem)            
            function = Function(functionName=preset.getFunN(), functionExpression=setE3)

            returnStr = returnStr + function.getFunctionStr() + NEWLINE
            returnStr = returnStr + preset.getPresetStr() +NEWLINE
    else:
        return "场环境设置，请检查isSetE3"
    
    return returnStr


def getWorkAreaCommands(name, x1Start, x1Stop, x2Start, x2Stop, x3Start, x3Stop):
    """
    工作区域设置命令
    :param name: 名称
    :param x1Start: 第一个坐标范围起
    :param x1Stop: 第一个坐标范围至
    :param x2Start: 第二个坐标范围起
    :param x2Stop: 第二个坐标范围至
    :param x3Start: 第三个坐标范围起
    :param x3Stop: 第三个坐标范围至
    :return: 
    """
    returnStr = NEWLINE

    point1 = Point(name+".LO", [x1Start, x2Start, x3Start])
    returnStr = returnStr + point1.getPonitStr() + NEWLINE

    point2 = Point(name + ".HI", [x1Stop, x2Stop, x3Stop])
    returnStr = returnStr + point2.getPonitStr() + NEWLINE

    volume = Volume(name, "CONFORMAL", [name+".LO", name + ".HI"])
    returnStr = returnStr + volume.getVolumeStr() + NEWLINE

    returnStr = returnStr + getMarkCommands(name, True, True, True, "DX1", "DX2", "DX3")

    returnStr = returnStr + NEWLINE + "AUTOGRID ;" + NEWLINE

    return returnStr


def getMaterialCommands(name="", atomicNumber="", atomicMass="", massDensity="",
                 isConductivity=False, conductivity="",
                 isPermittivity=False, permittivity=""):
    """
    
    :param name: 
    :param atomicNumber: 
    :param atomicMass: 
    :param massDensity: 
    :param conductivity: 
    :param permittivity: 
    :return: 
    """
    material = Material(name, atomicNumber, atomicMass, massDensity,
                 isConductivity, conductivity,
                 isPermittivity, permittivity)

    returnStr = NEWLINE + material.getMaterialStr() + NEWLINE

    return returnStr





###############################测试##############################################

# print getSystemCommands("R")
#
# print getHeaderCommands("organization", "author", "device", "remarks")
#
# print getParameterCommands("CA", "sas")
#
# print getPointCommands("ponitN", ["1mm",2,3])
#
# print getLineCommands("lineN", "CONFORMAL", [1, 2, 3], [2, 3, 4])
#
# print getAreaCommands("areaN", "CONFORMAL", [1, 2, "255m"], [2, 3, 4])
#
# print getConformalVolumeCommands("conformalVolumeN", [1, 2, 3], [2, 3, 4])
#
# print getConeVolumeCommands("coneVolumeN", [1, 2, 3], [2, 3, 4],12,86)
#
# print getCylindricalVolumeCommands("CylindricalVolumeN", [1, 2, 3], [2, 3, 4],12)
#
# print getAnnularVolumeCommands("AnnularVolumeN", [1, 2, 3], [2, 3, 4],12,15)
#
# print getAnnularSectionVolumeCommands("AnnularSVolumeN", [1, 2, 3], [2, 3, 4],12,15,[1, 2, 3], [2, 3, 4])
#
# print getParallelepipedalVolumeCommands("ParaVolumeN", [1, 2, 3], [2, 3, 4],[1, 2, 3], [2, 3, 4])
#
# print getSphericalVolumeCommands("SpVolumeN", [1, 2, 3], 11)
#
# print getWedgeVolumeCommands("ParaVolumeN", [1, 1, 3], [2, 2, 4],[3, 3, 3], [4, 4, 4],[5, 5, 3], [6, 6, 4])
#
# print getTetrahedronVolumeCommands("ParaVolumeN", [1, 1, 3], [2, 2, 4],[3, 3, 3], [4, 4, 4])
#
# print getPyramidVolumeCommands("ParaVolumeN", [1, 1, 3], [2, 2, 4],[3, 3, 3], [4, 4, 4],[5, 5, 3])
#
# print getRhombusVolumeCommands("volumeName", [1, 1, 3], [2, 2, 4],[3, 3, 3], [4, 4, 4],[5, 5, 3],
#                                                     [6, 3, 3], [7, 4, 4], [8, 5, 3])
#
# print getMarkCommands("markN", isX1=True, isX3=True, X1Size="2mm", X3Size=3)
#
# print getVoidCommands("voidN")
#
# print getConductorCommands("conductorN")
#
# print(getVolumeDIYAttributeCommands("volume",
#                                     isconductance=True, sigma="ss",
#                                     isDielectric=False, isotropy=False, permittivity1="aa", permittivity2="ss",
#                                     permittivity3="bb"))
#
# print getPortCommands("portN","POSITIVE",
#                       isPhaseVelocity=True, phaseVelocity="1",
#                       isScale=True, scale="2",
#                       isFt=True, ftVal="5.e5*t",
#                       isGeFirst=True, geFirstName="GE1", geFirstVal="0",
#                       isGeSecond=False, geSecondName="GE3", geSecondVal="0.0",
#                       isNormalization=True, normalizationLine="line",
#                       isLaplacian=True, laplacianFirst="va", laplacianSecond="vb")
#
#
# print getFreespaceCommands("freeSpaceName", "NEGATIVE", "X1", "ALL", True, "1.0*Xn*Xn")
#
# print getEmBCommands("emitName", "0.254", "0.256",
#                    isSpecies=True, species="ELECTRON",
#                    isNumber=True, creationRate="3",
#                    isTiming=True, timingType="TIMING", stepMultiple="1",
#                    isSurfaceSpacing=True, surfaceSpacing="RANDOM",
#                    isOutwardSpacing=False, outwardSpacing="", dn="",
#                    isEmit=True, mobject="obj",
#                    isExclude1=True, excludeVolume1="exv1", isExclude2=False, excludeVolume2="",
#                    isInclude1=True, includeVolume1="inv2", isInclude2=True, includeVolume2="aa"
#                    )
#
# print getEmECommands(1,"ExplosiveName",
#                          isTField=True, TField="0.2",
#                          isRField=False, RField="5.23",
#                          isCharg=True, Charg="12.3",
#                          isFRate=True, FRate="12.5",
#                          isSpecies=True, species="ELECTRON",
#                          isNumber=True, creationRate="3",
#                          isTiming=True, timingType="TIMING", stepMultiple="1",
#                          isSurfaceSpacing=True, surfaceSpacing="RANDOM",
#                          isOutwardSpacing=True, outwardSpacing="RANDOM", dn="0.25",
#                          isEmit=True, mobject="obj",
#                          isExclude1=True, excludeVolume1="exv1", isExclude2=False, excludeVolume2="",
#                          isInclude1=True, includeVolume1="inv2", isInclude2=True, includeVolume2="aa"
#                          )
#
# print getEmGCommands("EmG", "1", "2", "3", "4", "5", ["1","1","1"], isX1=False, isX2=False, isX3=False,
#                          isSpecies=True, species="ELECTRON",
#                          isNumber=True, creationRate="3",
#                          isTiming=True, timingType="TIMING", stepMultiple="1",
#                          isSurfaceSpacing=True, surfaceSpacing="RANDOM",
#                          isOutwardSpacing=True, outwardSpacing="RANDOM", dn="0.25",
#                          isEmit=True, mobject="obj",
#                          isExclude1=True, excludeVolume1="exv1", isExclude2=False, excludeVolume2="",
#                          isInclude1=True, includeVolume1="inv2", isInclude2=True, includeVolume2="aa"
#                          )
#
# print getEmHCommands("EmH", "A", "B", "PHI12345",
#                          isSpecies=True, species="ELECTRON",
#                          isNumber=True, creationRate="3",
#                          isTiming=True, timingType="TIMING", stepMultiple="1",
#                          isSurfaceSpacing=True, surfaceSpacing="RANDOM",
#                          isOutwardSpacing=True, outwardSpacing="RANDOM", dn="0.25",
#                          isEmit=True, mobject="obj",
#                          isExclude1=True, excludeVolume1="exv1", isExclude2=False, excludeVolume2="",
#                          isInclude1=True, includeVolume1="inv2", isInclude2=True, includeVolume2="aa"
#                          )
#
# print getEmTCommands("EmT", "WFsdfsd", "TPdfsd",
#                          isSpecies=True, species="ELECTRON",
#                          isNumber=True, creationRate="3",
#                          isTiming=True, timingType="TIMING", stepMultiple="1",
#                          isSurfaceSpacing=True, surfaceSpacing="RANDOM",
#                          isOutwardSpacing=True, outwardSpacing="RANDOM", dn="0.25",
#                          isEmit=True, mobject="obj",
#                          isExclude1=True, excludeVolume1="exv1", isExclude2=False, excludeVolume2="",
#                          isInclude1=True, includeVolume1="inv2", isInclude2=True, includeVolume2="aa"
#                          )
#
# print getTimerCommands("timer", "PERIODIC", "INTEGER", stratTime="11", stopTime="11", timeIncrement="啊啊", triggerTimes="")
#
# print getContourCommands("E1", "areaName", "TSYS$FIRST", isShade=True)
#
# print getVectorCommands("E1", "E3", "areaName", "TSYS$FIRST", isNumber=True, number1="20", number2="20")
#
# print getPhasespaceCommands("X1", "X3","timerName", "PROTON",
#                  isThickness=True, direction="X1", thickness1="2", thickness2="3",
#                  isSuffix=True, suffix="phase")
#
# print getRangeCommands("lineName", "B1", "timerName", isFFT=True, isMagnitude=True, isComplex=False)
#
# print getObserveCommands(isField=True, isFieldIntegral=False, isFieldPower=False, isFieldEnergy=False, isEmitEps=False,
#                         field="E1", objectName="VolmPoly",
#                         isFFT=True, fftType="MAGNITUDE", freqFrom="0", freqTo="10",
#                         isTime=True, timeFrom="0", timeTo="10",
#                         isFilter=True, filterType="STEP", timePara="0.05")
#
# print getSymmetryCommands(type="PERIODIC", trendType="POSITIVE", lineOrArea1="qq", lineOrArea2="weixin")
#
# print getTimeComputationCommands(time=30, algorithm="HIGH_Q",
#                        isPattern=True, pattern="EM",
#                        isStep=True, step=0.02,
#                        isChargeAlgorithm=True)
#
# print getDataExportCommands("test", isObs=True, isRan=False, isCntr=True, isVec=True, isPha=True,
#                           isPrefix=True, prefix="ss",
#                           isSuffix=True , suffix="cc",
#                           isASCII=False)
#
# print getRunOptionCommands(isDisplay=True, isPause=True)
#
# print getPresetCommands(coordinateSystem="P",
#                       isSetB1=True, setB1="sss", isSetB2=True, setB2="ccc", isSetB3=True, setB3="vvv",
#                       isSetE1=True, setE1="aada", isSetE2=True, setE2="bbb", isSetE3=True, setE3="wwwaasf",
#                       diySet="wwwww")
#
# print getWorkAreaCommands("SIMUVOLUME", "0mm", "amm", "smm", "amm", "xmm", "234mm")
#
# print getMaterialCommands(name="mx", atomicNumber="1", atomicMass="2", massDensity="3",
#                  isConductivity=True, conductivity="4",
#                  isPermittivity=True, permittivity="5")
#
# print getSolendCommands("other", "name", "zCenter", "rCenter", "innerRadius", "outerRadius", "coilCurrent", "coilRadius", "coilNum",
#                  "theta", "phi", "rFactor", "zFactor", "spaceRatio", "innerRadius2", "outerRadius2", "magneticRatio")
#
# print getInductorCommands("name", "diameter", False, "inductance")
#
# print getDriverCommands("R", "name", "currentDensity", "funExpression")
#
# print getFoilCommands("name", "thick", False, "DITMaterial", True, "defaultMaterial")
