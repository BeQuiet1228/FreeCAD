# -*- coding: UTF-8 -*-
###################################################################
# author: maxin
# describe: 对CHIPIC中规定的命令进行追个分析
###################################################################
import FreeCAD
from enum import Enum
import re

# 定义一些用到的字符
blankSpace = " "
doubleQuotation = "\""
semicolon = ";"
notesLine = "!=======================================================================!\n"
exclamatory = "!"
comma = ","
newline = "\n"
tab = "\t"
symbolPoint = "."
equalSign = "="

# 定义涉及到的关键字
keywordInCommand = ["FUNCTION",
                    "START", "STOP",
                    "SYSTEM", "POINT", "LINE", "AREA", "VOLUME",
                    "DURATION", "TIMER", "MARK", "AUTOGRID",
                    "SYMMETRY", "PORT", "FREESPACE",
                    "CONDUCTANCE", "DIELECTRIC", "CONDUCTOR", "VOID", "MATERIAL", "FOIL", "INDUCTOR", "DRIVER",
                    "EMISSION", "EMIT",
                    "MAXWELL", "MODE", "TIME_STEP",
                    "CONTINUITY",
                    "PRESET",
                    "GRAPHICS", "DUMP", "HEADER",
                    "OBSERVE",
                    "DISPLAY", "CONTOUR", "VECTOR", "PHASESPACE", "RANGE",
                    "KINEMATICS"]

# 判断是数还是字符串
def isNumber(n):
    result=True
    try:
        num=float(n)
        result = num == num
    except ValueError:
        result=False
    return result
##############################第一章 变量与函数命令##############################
class Function:
    # 定义函数，为其它命令参数调用
    class Type(Enum):
        expression = "expression"
        data = "data"

    def __init__(self, type="expression", functionName="", functionExpression="", pairs="", datas=""):
        self.command = "FUNCTION"
        self.type = type
        self.functionName = functionName
        self.functionExpression = functionExpression
        self.pairs = pairs
        self.datas = datas

    def __encoded(self):
        if self.type == self.Type.expression:
            return self.command + blankSpace + \
                   self.functionName + blankSpace + \
                   equalSign + blankSpace + \
                   self.functionExpression + semicolon
        if self.type == self.Type.data:
            datasStr = ""
            for index in range(0,len(self.datas),self.pairs):
                datasStr = datasStr + self.datas[index] + comma + self.datas[index+1] + blankSpace

            return self.command + blankSpace + \
                   self.functionName + blankSpace + \
                   "DATA" + blankSpace + \
                   self.pairs + blankSpace + \
                   datasStr + semicolon

    def __decoded(self, str):
        strs = re.split(" = |;", str)
        if self.type == self.Type.expression:
            self.functionName = strs[0].split(' ')[1]
            self.functionExpression = strs[1]
        if self.type == self.Type.data:
            strs = re.split(" |;", str)
            self.functionName = strs[1]
            self.pairs = strs[3]

        return self

    def getFunctionStr(self):
        return self.__encoded()

    def getFunctionObject(self, str):
        return self.__decoded(str)


###############################第四章 执行命令##################################
class Start:
    "开始进行仿真，如果在前面的任何一个命令中有错误，仿真就会结束"

    def __init__(self):
        self.command = "START"

    def __encoded(self):
        return self.command + blankSpace + semicolon

    def getStartStr(self):
        return self.__encoded()


class Stop:
    "开始进行仿真，如果在前面的任何一个命令中有错误，仿真就会结束"

    def __init__(self):
        self.command = "STOP"

    def __encoded(self):
        return self.command + blankSpace + semicolon

    def getStopStr(self):
        return self.__encoded()


###############################第五章 对象命令##################################
class System:
    "用来指定坐标系"
    class Type(Enum):
        cartesian = "CARTESIAN"
        cylindrical = "CYLINDRICAL"
        polar = "POLAR"

    def __init__(self ,type=""):
        self.command = "SYSTEM"
        self.type = type

    def __encoded(self):
        return self.command + blankSpace + \
                self.type + semicolon

    def __decoded(self, systemStr):

        self.command = "POINT"
        "去掉末尾分号"
        systemStr = systemStr.split(semicolon)[0]
        seg = systemStr.split(blankSpace)
        self.type = seg[1]

        return self

    def getNotes(self):
        return exclamatory + self.command

    def getSystemStr(self):
        return self.__encoded()

    def getSystem(self, systemStr):
        return self.__decoded(systemStr)


class Point:
    "指定空间二维点"
    def __init__(self, pName="", coordinates=""):
        self.command = "POINT"
        self.pName = pName
        self.coordinates = coordinates

    def __encoded(self):

        coordinateStr = ""
        for index in range(len(self.coordinates)):
            if index == 0:
                coordinateStr = coordinateStr + self.coordinates[index]
            else:
                coordinateStr = coordinateStr + comma + blankSpace + self.coordinates[index]

        return self.command + blankSpace + \
                self.pName + blankSpace + \
               coordinateStr + semicolon

    def __decoded(self, ponitStr):

        self.command = "POINT"
        "去掉末尾分号"
        ponitStr = ponitStr.split(semicolon)[0]
        seg = ponitStr.split(comma + blankSpace)

        if len(seg) == 3:
            coordinates = [seg[0],seg[1],seg[2]]
        else:
            coordinates = seg
        self.pName = seg[0].split(blankSpace)[1]
        coordinates[0] = seg[0].split(blankSpace,2)[2]
        self.coordinates = coordinates

        return self

    def getPonitStr(self):
        return self.__encoded()

    def getPoint(self, pointStr):
        return self.__decoded(pointStr)

class Array_Point:
    "专为array指定空间二维点"
    def __init__(self, pName="", coordinates=""):
        self.command = "POINT"
        self.pName = pName
        self.coordinates = coordinates
        # if(pName[-1]=="P"):
        #     self.param_name=self.pName[-1:]+"x"
        # else:
        #     self.param_name = self.pName[-2:] + "x"
        self.loc = pName.index(".")
        self.param_name=self.pName[self.loc+1:]+"x"

    def __encoded(self):
        #为了实现例如代数的形式这里需要进行修改

        new_Point=""
        coordinateStr = ""
        for index in range(len(self.coordinates)):
            if index == 0:
                new_Point=new_Point+blankSpace+self.param_name+str(index)+"\'i\'"
                coordinateStr = coordinateStr +self.param_name+str(index)+"\'i\'"+equalSign+ self.coordinates[index]+semicolon
            else:
                new_Point=new_Point+blankSpace+self.param_name+str(index)+"\'i\'"
                coordinateStr = coordinateStr + newline + self.param_name+str(index) +"\'i\'"+ equalSign + self.coordinates[index]+semicolon


        return coordinateStr+newline+self.command + blankSpace + \
                self.pName + blankSpace + \
               new_Point+semicolon

    def __decoded(self, ponitStr):

        self.command = "POINT"
        "去掉末尾分号"
        ponitStr = ponitStr.split(semicolon)[0]
        seg = ponitStr.split(comma + blankSpace)

        if len(seg) == 3:
            coordinates = [seg[0],seg[1],seg[2]]
        else:
            coordinates = seg
        self.pName = seg[0].split(blankSpace)[1]
        coordinates[0] = seg[0].split(blankSpace,2)[2]
        self.coordinates = coordinates

        return self

    def getPonitStr(self):
        return self.__encoded()

    def getPoint(self, pointStr):
        return self.__decoded(pointStr)


class Line:
    "空间中定义一条直线"

    class Type(Enum):
        conformal = "CONFORMAL"
        oblique = "OBLIQUE"

    def __init__(self, lName="", type="", vals=""):
        self.command = "LINE"
        self.lName = lName
        self.type = type
        self.vals = vals

    def __encoded(self):

        if self.type == self.Type.conformal or self.type == self.Type.oblique:
            pointsStr = ""
            for val in self.vals:
                pointsStr = pointsStr + val + blankSpace

            return self.command + blankSpace + \
                   self.lName + blankSpace + \
                   self.type + blankSpace + \
                   pointsStr + semicolon
        else:
            return "error type"

    def __decoded(self, lineStr):

        self.command = "LINE"
        seg = lineStr.split(blankSpace)
        self.lName = seg[1]
        self.type = seg[2]
        "去掉末尾分号"
        self.vals = seg[3:-1]
        return self

    def getLineStr(self):
        return self.__encoded()

    def getLine(self, lineStr):
        return self.__decoded(lineStr)


class Area:
    "确定空间区域"

    class Shape(Enum):
        conformal = "CONFORMAL"
        rectangular = "RECTANGULAR"
        functional = "FUNCTIONAL"
        polygonal = "POLYGONAL"

    def __init__(self, areaName="", shape="", vals=""):
        self.command = "AREA"
        self.areaName = areaName
        self.shape = shape
        self.vals = vals

    def __encoded(self):

        valsStr = ""
        for val in self.vals:
            valsStr = valsStr + val + blankSpace

        if self.shape == self.Shape.conformal:
            return self.command + blankSpace + \
                    self.areaName + blankSpace + \
                    self.Shape.conformal + blankSpace + \
                    valsStr + semicolon

        elif self.shape == self.Shape.rectangular:
            return self.command + blankSpace + \
                    self.areaName + blankSpace + \
                    self.Shape.rectangular + blankSpace + \
                    valsStr + semicolon

        elif self.shape == self.Shape.functional:
            return self.command + blankSpace + \
                    self.areaName + blankSpace + \
                    self.Shape.functional + blankSpace + \
                    self.vals + semicolon

        elif self.shape == self.Shape.polygonal:
            return self.command + blankSpace + \
                    self.areaName + blankSpace + \
                    self.Shape.polygonal + blankSpace + \
                    valsStr + semicolon
        else:
            return "error shape"

    def __decoded(self, areaStr):

        self.command = "AREA"
        seg = areaStr.split(blankSpace)
        self.areaName = seg[1]
        self.shape = seg[2]
        "去掉末尾分号"
        self.vals = seg[3:-1]
        return self

    def getAreaStr(self):
        return self.__encoded()

    def getArea(self, areaStr):
        return self.__decoded(areaStr)


class Volume:
    "用来定义一个具有特定形状的体(仅用于三维模拟)"

    class Shape(Enum):
        annular = "ANNULAR"
        annularSection = "ANNULAR_SECTION"
        cone = "CONE"
        conformal = "CONFORMAL"
        cylindrical = "CYLINDRICAL"
        functional = "FUNCTIONAL"
        parallelepipedal = "PARALLELEPIPEDAL"
        spherical = "SPHERICAL"
        wedge = "WEDGE"
        tetrahedron = "TETRAHEDRON"
        pyramid = "PYRAMID"
        rhombus = "RHOMBUS"
        toroidalSection = "TOROIDAL_SECTION"
        extruded = "EXTRUDED"
        helical = "HELICAL"
        rotate="ROTATE"


    def __init__(self, volumeName="", shape="", args=""):
        self.command = "VOLUME"
        self.volumeName = volumeName
        self.shape = shape
        self.args = args

    def __encoded(self):
        argsStr = ""
        # FreeCAD.Console.PrintError("Args: "+str(self.args)+"\n")
        #为了区分参数阵列体做了这个判断
        if isinstance(self.args,list):
            for arg in self.args:
                argsStr = argsStr + arg + blankSpace
        else:
            argsStr=self.args
        return self.command + blankSpace + \
                self.volumeName + blankSpace + \
                self.shape + blankSpace + \
                argsStr + semicolon

    def __decoded(self, volumeStr):

        self.command = "AREA"
        seg = volumeStr.split(blankSpace)
        self.volumeName = seg[1]
        self.shape = seg[2]
        "去掉末尾分号"
        # 关于新旧版本工程不兼容的问题
        if seg[-1]==';':
            # 新版本
            self.args = seg[3:-1]
        elif seg[-1][-1]==';':
            # 旧版本
            seg[-1]=seg[-1][:-1]
            self.args=seg[3:]
        FreeCAD.Console.PrintMessage("\ntest_semi\n")
        FreeCAD.Console.PrintMessage(seg)
        return self

    def getVolumeStr(self):
        return self.__encoded()

    def getVolume(self, volumeStr):
        return self.__decoded(volumeStr)


class Array:

    class ArrayType(Enum):
        linear = "linear"
        ortho = "ortho"
        polar = "polar"


    def __init__(self, system="", arrayType="linear", centerAxis="X", orthoFace="XY", numX=1, numY=1, numZ=1, num=2, numPolar=1,
                 stepX="10mm", stepY="10mm", stepZ="10mm"):

        self.system = system
        self.arrayType = arrayType
        self.centerAxis = centerAxis
        self.orthoFace = orthoFace
        self.numX = numX
        self.numY = numY
        self.numZ = numZ
        self.num = num
        self.numPolar = numPolar
        self.stepX = stepX
        self.stepY = stepY
        self.stepZ = stepZ

    def __encoded(self):

        if self.system == System.Type.cartesian:
            if self.arrayType == Array.ArrayType.linear:
                if isNumber(self.num):
                    return "do i=0," + str(self.num- 1) + semicolon
                else:
                    return "do i=0," + str(self.num) +"-1" + semicolon
            elif self.arrayType == Array.ArrayType.polar:
                if isNumber(self.numPolar):
                    return "do i=0," + str(self.numPolar - 1) + semicolon
                else:
                    return "do i=0," + str(self.numPolar) + "-1" + semicolon
            else:
                if self.orthoFace == "XY":
                    if isNumber(self.numX) and isNumber(self.numY):
                        return "do i=0," +str(self.numX * self.numY -1) + semicolon
                    else:
                        return "do i=0," + str(self.numX) + "*" +str( self.numY) +"-1" + semicolon
                elif self.orthoFace == "XZ":
                    if isNumber(self.numX) and isNumber(self.numZ):
                        return "do i=0," + str(self.numX * self.numZ -1) + semicolon
                    else:
                        return "do i=0," + str(self.numX) +"*"+ str(self.numZ) +"-1" + semicolon
                else:
                    if isNumber(self.numY) and isNumber(self.numZ):
                        return "do i=0," + str(self.numY * self.numZ -1) + semicolon
                    else:
                        return "do i=0," + str(self.numY) +"*"+ str(self.numZ) +"-1" + semicolon
        else:
            if self.arrayType == Array.ArrayType.linear:
                if isNumber(self.num):
                    return "do i=0," + str(self.num- 1) + semicolon
                else:
                    return "do i=0," + str(self.num) +"-1" + semicolon
            elif self.arrayType == Array.ArrayType.polar:
                if isNumber(self.numPolar):
                    return "do i=0," + str(self.numPolar - 1) + semicolon
                else:
                    return "do i=0," + str(self.numPolar) + "-1" + semicolon
            else:
                if isNumber(self.numX) and isNumber(self.numZ):
                    return "do i=0," + str(self.numX * self.numZ - 1) + semicolon
                else:
                    return "do i=0," + str(self.numX) + "*" + str(self.numZ) + "-1" + semicolon

    def getCoordinateStr(self,coordinates):
        coordinateStr = [coordinates[0],coordinates[1],coordinates[2]]
        if self.system == System.Type.cartesian:
            if self.arrayType == Array.ArrayType.linear:
                if self.stepX != "0mm":
                    coordinateStr[0] = coordinates[0] + "+i*" + str(self.stepX)
                if self.stepY != "0mm":
                    coordinateStr[1] = coordinates[1] + "+i*" + str(self.stepY)
                if self.stepZ != "0mm":
                    coordinateStr[2] = coordinates[2] + "+i*" + str(self.stepZ)
            elif self.arrayType == Array.ArrayType.polar:
                if self.centerAxis == "X":
                    coordinateStr[1] = coordinates[1] + "*cos(((2*PI)/" + str(self.numPolar) + ")*i)-" + \
                                       coordinates[2] + "*sin(((2*PI)/" + str(self.numPolar) + ")*i)"
                    coordinateStr[2] = coordinates[2] + "*cos(((2*PI)/" + str(self.numPolar) + ")*i)+" + \
                                       coordinates[1] + "*sin(((2*PI)/" + str(self.numPolar) + ")*i)"

                elif self.centerAxis == "Y":
                    coordinateStr[0] = coordinates[0] + "*cos(((2*PI)/" + str(self.numPolar) + ")*i)-" + \
                                       coordinates[2] + "*sin(((2*PI)/" + str(self.numPolar) + ")*i)"
                    coordinateStr[2] = coordinates[2] + "*cos(((2*PI)/" + str(self.numPolar) + ")*i)+" + \
                                       coordinates[0] + "*sin(((2*PI)/" + str(self.numPolar) + ")*i)"

                elif self.centerAxis == "Z":
                    coordinateStr[0] = coordinates[0] + "*cos(((2*PI)/" + str(self.numPolar) + ")*i)+" + \
                                       coordinates[1] + "*sin(((2*PI)/" + str(self.numPolar) + ")*i)"
                    coordinateStr[1] = coordinates[1] + "*cos(((2*PI)/" + str(self.numPolar) + ")*i)-" + \
                                       coordinates[0] + "*sin(((2*PI)/" + str(self.numPolar) + ")*i)"

            else:
                if self.orthoFace == "XY":
                    coordinateStr[0] = coordinates[0] + "+MODULO(i," + str(self.numX) + ")*" + str(
                        self.stepX)
                    coordinateStr[1] = coordinates[1] + "+(i-MODULO(i," + str(self.numX) + ")/" + str(self.numX) + "*" + str(
                        self.stepY)
                elif self.orthoFace == "XZ":
                    coordinateStr[0] = coordinates[0] + "+MODULO(i," + str(self.numX) + ")*" + str(
                        self.stepX)
                    coordinateStr[2] = coordinates[2] + "+(i-MODULO(i," + str(self.numX) + ")/" + str(self.numX) + "*" + str(
                        self.stepZ)
                elif self.orthoFace == "YZ":
                    coordinateStr[1] = coordinates[1] + "+MODULO(i," + str(self.numY) + ")*" + str(
                        self.stepY)
                    coordinateStr[2] = coordinates[2] + "+(i-MODULO(i," + str(self.numY) + ")/" + str(self.numY) + "*" + str(
                        self.stepZ)
        elif self.system == System.Type.cylindrical:
            if self.arrayType == Array.ArrayType.linear:
                coordinateStr[1] = coordinates[1] + "+i*" + str(self.stepX)
                if self.stepX != "0mm":
                    coordinateStr[0] = coordinates[0] + "+i*" + str(self.stepZ)
                if self.stepZ != "0mm":
                    coordinateStr[2] = coordinates[2] + "+i*" + str(self.stepY)
            elif self.arrayType == Array.ArrayType.polar:
                coordinateStr[2] = coordinates[2] + "+i*360/" +str(self.numZ)+ "deg"
            else:
                coordinateStr[1] = coordinates[1] + "+MODULO(i," + str(self.numX) + ")*" + str(
                    self.stepX)
                coordinateStr[0] = coordinates[0] + "+(i-MODULO(i," + str(self.numX) + ")/" + str(self.numX) + "*" + str(
                    self.stepZ)
        else:
            if self.arrayType == Array.ArrayType.linear:
                coordinateStr[1] = coordinates[1] + "+i*" + str(self.stepY)
                if self.stepX != "0mm":
                    coordinateStr[0] = coordinates[0] + "+i*" + str(self.stepX)
                if self.stepZ != "0mm":
                    coordinateStr[2] = coordinates[2] + "+i*" + str(self.stepZ)
            elif self.arrayType == Array.ArrayType.polar:
                coordinateStr[1] = coordinates[1] + "+i*360/" +str(self.numZ)+ "deg"
            else:
                coordinateStr[0] = coordinates[0] + "+MODULO(i," + str(self.numX) + ")*" + str(
                    self.stepX)
                coordinateStr[2] = coordinates[2] + "+(i-MODULO(i," + str(self.numX) + ")/" + str(self.numX) + "*" + str(
                    self.stepZ)

        # coordinateStr.append("\n")

        return coordinateStr

    def __decoded(self, str):

        strs = re.split(",|;", str)
        if self.system == System.Type.cartesian:
            if self.arrayType == Array.ArrayType.linear:
                if isNumber(strs[1]):
                    self.num = int(strs[1]) +1
                else:
                    self.num = strs[1].rsplit("-1",1)[0]
            elif self.arrayType == Array.ArrayType.polar:
                if isNumber(strs[1]):
                    self.numPolar = int(strs[1]) +1
                else:
                    self.numPolar = strs[1].rsplit("-1",1)[0]
            else:
                if self.orthoFace == "XY":
                    if isNumber(strs[1]) and isNumber(self.numX):
                        self.numY  = (int(strs[1]) +1)/int(self.numX)
                    else:
                        num_y = strs[1].split(self.numX+"*",1)[1].rsplit("-1",1)[0]
                        # num_y = re.split("\*|-1", strs[1])[1]
                        if isNumber(num_y):
                            self.numY=int(num_y)
                        else:
                            self.numY=num_y
                        if isNumber(self.numX):
                            self.numX=int(self.numX)
                elif self.orthoFace == "XZ":
                    if isNumber(strs[1]) and isNumber(self.numX):
                        self.numZ  = (int(strs[1]) +1)/int(self.numX)
                    else:
                        num_z = strs[1].split(self.numX + "*", 1)[1].rsplit("-1",1)[0]
                        # num_z = re.split("\*|-1", strs[1])[1]
                        if isNumber(num_z):
                            self.numZ=int(num_z)
                        else:
                            self.numZ=num_z
                        if isNumber(self.numX):
                            self.numX=int(self.numX)
                else:
                    if isNumber(strs[1]) and isNumber(self.numY):
                        self.numZ  = (int(strs[1]) +1)/int(self.numY)
                    else:
                        num_z = strs[1].split(self.numY + "*", 1)[1].rsplit("-1",1)[0]
                        # num_z = re.split("\*|-1", strs[1])[1]
                        if isNumber(num_z):
                            self.numZ=int(num_z)
                        else:
                            self.numZ=num_z
                        if isNumber(self.numY):
                            self.numY=int(self.numY)
        else:
            if self.arrayType == Array.ArrayType.linear:
                if isNumber(strs[1]):
                    self.num = int(strs[1]) +1
                else:
                    self.num = strs[1].rsplit("-1",1)[0]
            elif self.arrayType == Array.ArrayType.polar:
                if isNumber(strs[1]):
                    self.numPolar = int(strs[1]) +1
                else:
                    self.numPolar = strs[1].rsplit("-1",1)[0]
            else:
                if isNumber(strs[1]) and isNumber(self.numX):
                    self.numZ =  (int(strs[1]) +1)/int(self.numX)
                else:
                    num_z = strs[1].split(self.numX + "*", 1)[1].rsplit("-1",1)[0]
                    # num_z = re.split("\*|-1", strs[1])[1]
                    if isNumber(num_z):
                        self.numZ = int(num_z)
                    else:
                        self.numZ = num_z
                    if isNumber(self.numX):
                        self.numX = int(self.numX)
        return self

    def decodedCoordinateStr(self, coordinateStr):

        if self.system == System.Type.cartesian:
            coordinates =  ["0mm", "0mm", "0mm"]
        elif self.system == System.Type.polar:
            coordinates = ["0mm", "0deg", "0mm"]
        elif self.system == System.Type.cylindrical:
            coordinates = ["0mm", "0mm", "0deg"]

        if self.system == System.Type.cartesian:
            if "cos(((2*PI)" in coordinateStr[1] and "cos(((2*PI)" in coordinateStr[2]:

                self.arrayType = Array.ArrayType.polar
                self.centerAxis = "X"
                self.numPolar = coordinateStr[1].split("*cos(((2*PI)/")[1].split(")*i)")[0]
                # if isNumber(self.numPolar):
                #     self.numPolar = int(self.numPolar)
                coordinates[0] = coordinateStr[0]
                coordinates[1] = coordinateStr[1].split("*cos(((2*PI)/")[0]
                coordinates[2] = coordinateStr[2].split("*cos(((2*PI)/")[0]
            elif "cos(((2*PI)" in coordinateStr[0] and "cos(((2*PI)" in coordinateStr[2]:

                self.arrayType = Array.ArrayType.polar
                self.centerAxis = "Y"
                self.numPolar = coordinateStr[0].split("*cos(((2*PI)/")[1].split(")*i)")[0]
                # if isNumber(self.numPolar):
                #     self.numPolar = int(self.numPolar)
                coordinates[1] = coordinateStr[1]
                coordinates[0] = coordinateStr[0].split("*cos(((2*PI)/")[0]
                coordinates[2] = coordinateStr[2].split("*cos(((2*PI)/")[0]
            elif "cos(((2*PI)" in coordinateStr[0] and "cos(((2*PI)" in coordinateStr[1]:

                self.arrayType = Array.ArrayType.polar
                self.centerAxis = "Z"
                self.numPolar = coordinateStr[1].split("*cos(((2*PI)/")[1].split(")*i)")[0]
                # if isNumber(self.numPolar):
                #     self.numPolar = int(self.numPolar)
                coordinates[2] = coordinateStr[2]
                coordinates[0] = coordinateStr[0].split("*cos(((2*PI)/")[0]
                coordinates[1] = coordinateStr[1].split("*cos(((2*PI)/")[0]
            elif "MODULO" in coordinateStr[0] and "MODULO" in coordinateStr[1]:
                self.arrayType = Array.ArrayType.ortho
                self.orthoFace = "XY"
                self.numX = coordinateStr[0].split("+MODULO(i,")[1].split(")*")[0]
                # if isNumber(self.numX):
                #     self.numX = int(self.numX)
                self.stepX = coordinateStr[0].split("+MODULO(i,")[1].split(")*")[1]
                self.stepY = coordinateStr[1].split("+(i-MODULO(i,")[1].rsplit("*",1)[1]
                coordinates[2] = coordinateStr[2]
                coordinates[0] = coordinateStr[0].split("+MODULO(i,")[0]
                coordinates[1] = coordinateStr[1].split("+(i-MODULO(i,")[0]
            elif "MODULO" in coordinateStr[0] and "MODULO" in coordinateStr[2]:
                self.arrayType = Array.ArrayType.ortho
                self.orthoFace = "XZ"
                self.numX = coordinateStr[0].split("+MODULO(i,")[1].split(")*")[0]
                # if isNumber(self.numX):
                #     self.numX = int(self.numX)
                self.stepX = coordinateStr[0].split("+MODULO(i,")[1].split(")*")[1]
                self.stepZ = coordinateStr[2].split("+(i-MODULO(i,")[1].rsplit("*",1)[1]
                coordinates[1] = coordinateStr[1]
                coordinates[0] = coordinateStr[0].split("+MODULO(i,")[0]
                coordinates[2] = coordinateStr[2].split("+(i-MODULO(i,")[0]
            elif "MODULO" in coordinateStr[1] and "MODULO" in coordinateStr[2]:
                self.arrayType = Array.ArrayType.ortho
                self.orthoFace = "YZ"
                self.numY = coordinateStr[1].split("+MODULO(i,")[1].split(")*")[0]
                # if isNumber(self.numY):
                #     self.numY = int(self.numY)
                self.stepY = coordinateStr[1].split("+MODULO(i,")[1].split(")*")[1]
                self.stepZ = coordinateStr[2].split("+(i-MODULO(i,")[1].rsplit("*",1)[1]
                coordinates[0] = coordinateStr[0]
                coordinates[1] = coordinateStr[1].split("+MODULO(i,")[0]
                coordinates[2] = coordinateStr[2].split("+(i-MODULO(i,")[0]
            else:
                self.arrayType = Array.ArrayType.linear
                if coordinateStr[0] == "0mm":
                    self.stepX = "0mm"
                    coordinates[0] = coordinateStr[0]
                else:
                    self.stepX = coordinateStr[0].split("+i*")[1]
                    coordinates[0] = coordinateStr[0].split("+i*")[0]
                if coordinateStr[1] == "0mm":
                    self.stepY = "0mm"
                    coordinates[1] = coordinateStr[1]
                else:
                    self.stepY = coordinateStr[1].split("+i*")[1]
                    coordinates[1] = coordinateStr[1].split("+i*")[0]
                if coordinateStr[2] == "0mm":
                    self.stepZ = "0mm"
                    coordinates[2] = coordinateStr[2]
                else:
                    self.stepZ = coordinateStr[2].split("+i*")[1]
                    coordinates[2] = coordinateStr[2].split("+i*")[0]
        else:
            if "+i*360/" in coordinateStr[1]:
                self.arrayType = Array.ArrayType.polar
                self.numZ = coordinateStr[1].split("+i*360/")[1].split("deg")[0]
                # if isNumber(self.numZ):
                #     self.numZ = int(self.numZ)
                coordinates[1] = coordinateStr[1].split("+i*360/")[0]
                coordinates[0] = coordinateStr[0]
                coordinates[2] = coordinateStr[2]
            elif "MODULO" in coordinateStr[0]:
                self.arrayType = Array.ArrayType.ortho
                self.numX = coordinateStr[0].split("+MODULO(i,")[1].split(")*")[0]
                # if isNumber(self.numX):
                #     self.numX = int(self.numX)
                self.stepX = coordinateStr[0].split("+MODULO(i,")[1].split(")*")[1]
                self.stepZ = coordinateStr[2].split("+(i-MODULO(i")[1].rsplit("*",1)[1]
                coordinates[1] = coordinateStr[1]
                coordinates[0] = coordinateStr[0].split("+MODULO(i,")[0]
                coordinates[2] = coordinateStr[2].split("+(i-MODULO(i,")[0]
            else:

                self.arrayType = Array.ArrayType.linear
                self.stepY = coordinateStr[1].split("+i*")[1]
                coordinates[1] = coordinateStr[1].split("+i*")[0]

                if coordinateStr[0] == "0mm":
                    self.stepX = 0
                    coordinates[0] = coordinateStr[0]
                else:
                    self.stepX = coordinateStr[0].split("+i*")[1]
                    coordinates[0] = coordinateStr[0].split("+i*")[0]
                if coordinateStr[2] == "0mm":
                    self.stepZ = 0
                    coordinates[2] = coordinateStr[2]
                else:
                    self.stepZ = coordinateStr[2].split("+i*")[1]
                    coordinates[2] = coordinateStr[2].split("+i*")[0]
        return coordinates

    def getArrayStr(self):
        return self.__encoded()

    def getArray(self, str):
        return self.__decoded(str)
###############################第六章 网格命令##################################
class Duration:
    "详细说明一个时间模拟中的时间段"
    # DURATION time_span ;

    def __init__(self, timeSpan=""):
        self.command = "DURATION"
        self.timeSpan = timeSpan

    def __encoded(self):
        return self.command + blankSpace +\
               self.timeSpan + "NANOSECOND" + semicolon

    def __decoded(self, durationStr):
        self.command = "DURATION"
        seg = durationStr.split(blankSpace)
        # FreeCAD.Console.PrintError('\nseg通过空格分割后:'+str(seg))
        # self.timeSpan = seg[1].split("NANOSECOND")[0]
        self.timeSpan = seg[1].replace("NANOSECOND",'').replace(';','')
        return self

    def getDurationStr(self):
        return self.__encoded()

    def getDuration(self, durationStr):
        return self.__decoded(durationStr)
    # 此处是在时间设置时不需要，如果输入的是变量，则不需要再添加“NANOSECOND” @lizheguang
    def getDurationwithoutunits(self):
        return self.command + blankSpace +\
               self.timeSpan  + semicolon


class Timer:
    "定义时间触发器"
    # TIMER timer PERIODIC { INTEGER, REAL } start_time stop_time [ time_increment ] ;
    # TIMER timer DISCRETE { INTEGER, REAL } trigger_time1 [ trigger_time2, ... ];

    class Type(Enum):
        periodic = "PERIODIC"
        discrete = "DISCRETE"

    class NumType(Enum):
        integer = "INTEGER"
        real = "REAL"

    def __init__(self ,timerName="", type="", numType="",
                 stratTime="10", stopTime="100000", timeIncrement="5000",
                 triggerTimes="10 12 15 24 85 168 468"):
        self.command = "TIMER"
        self.timerName = timerName
        self.type = type
        self.numType = numType
        self.stratTime = stratTime
        self.stopTime = stopTime
        self.timeIncrement = timeIncrement
        self.triggerTimes = triggerTimes

    def __encoded(self):
        if self.type == self.Type.periodic:
            return self.command + blankSpace + \
                   self.timerName + blankSpace + \
                   self.type + blankSpace + \
                   self.numType + blankSpace + \
                   self.stratTime + blankSpace + \
                   self.stopTime + blankSpace + \
                   self.timeIncrement + semicolon
        elif self.type == self.Type.discrete:
            triggerTimesStr = ""
            for triggerTime in self.triggerTimes:
                triggerTimesStr = triggerTimesStr + triggerTime + blankSpace

            return self.command + blankSpace + \
                   self.timerName + blankSpace + \
                   self.type + blankSpace + \
                   self.numType + blankSpace + \
                   triggerTimesStr + semicolon
        else:
            return "error type"

    def __decoded(self, timerStr):

        self.command = "TIMER"
        "去掉末尾分号"
        timerStr = timerStr.split(semicolon)[0]
        seg = timerStr.split(blankSpace)
        self.timerName = seg[1]
        self.type = seg[2]
        self.numType = seg[3]
        if self.type == self.Type.periodic:
            self.stratTime = seg[4]
            self.stopTime = seg[5]
            self.timeIncrement = seg[6]
        elif self.type == self.Type.discrete:
            "去掉末尾空格"
            self.triggerTimes = seg[4:-1]
        return self

    def getTimerStr(self):
        return self.__encoded()

    def getTimer(self, timerStr):
        return self.__decoded(timerStr)


class Mark:
    "为自动产生网格指明基于空间对象或者变量的坐标位置其对应的网格大小"

    class Direction(Enum):
        x1 = "X1"
        x2 = "X2"
        x3 = "X3"

    class Modification(Enum):
        minimum = "MINIMUM"
        midpoint = "MIDPOINT"
        maximum = "MAXIMUM"
        size = "SIZE"
        minMaxSize = "MIN MAX SIZE"

    def __init__(self, varOrObj="", direction="", modification="", cellSize="",
                ismin = False, ismid = False, ismax = False):
        self.command = "MARK"
        self.varOrObj = varOrObj
        self.direction = direction
        self.modification = modification
        self.cellSize = cellSize
        self.ismin = ismin
        self.ismid = ismid
        self.ismax = ismax

    def __encoded(self):
        # FreeCAD.Console.PrintError("\n mark: " +str(self.varOrObj)+"  "+str(self.direction)+"  "+str(self.modification)+""+str(self.cellSize))
        returnStr = ""
        returnStr = returnStr + self.command + blankSpace + \
                self.varOrObj + blankSpace + \
                self.direction + blankSpace
        # 此处添加异常处理，因为老工程的体可能不存在这几个属性@lzg
        try:
            # FreeCAD.Console.PrintError("\n开始执行mark拓展的部分")
            if self.ismin:
                returnStr = returnStr + self.Modification.minimum + blankSpace
            if self.ismid:
                returnStr = returnStr + self.Modification.midpoint + blankSpace
            if self.ismax:
                returnStr = returnStr + self.Modification.maximum + blankSpace
            # FreeCAD.Console.PrintError("\n执行完了对mark拓展的部分，且没有发生异常")
        except:
            pass
        returnStr = returnStr + self.modification + blankSpace + self.cellSize + semicolon
        return returnStr
        
        # self.command + blankSpace + \
        #         self.varOrObj + blankSpace + \
        #         self.direction + blankSpace + \
        #         self.modification + blankSpace + \
        #         self.cellSize + semicolon

    def __decoded(self, markStr):

        self.command = "MARK"
        "去掉末尾分号"
        markStr = markStr.split(semicolon)[0]
        seg = markStr.split(blankSpace)
        self.varOrObj = seg[1]
        self.direction = seg[2]
        # mark的拓展部分的命令
        if "MINIMUM" in markStr:
            self.ismin = True
        if "MIDPOINT" in markStr:
            self.ismid = True
        if "MAXIMUM" in markStr:
            self.ismax = True
        self.modification = seg[-2]
        self.cellSize = seg[-1]
        return self

    def getMarkStr(self):
        return self.__encoded()

    def getMark(self, markStr):
        return self.__decoded(markStr)


class AutoGrid:
    "由MARK产生的空间标记自动生成空间网格"
    # AUTOGRID [{ X1, X2, X3 } [ total_cells ] ] ;

    class Direction(Enum):
        x1 = "X1"
        x2 = "X2"
        x3 = "X3"

    def __init__(self, direction="", totalCells=""):
        self.command = "AUTOGRID"
        self.direction = direction
        self.totalCells = totalCells

    def __encoded(self):
        return self.command + blankSpace + \
                self.direction + blankSpace + \
                self.totalCells + semicolon

    def __decoded(self, autoGridStr):

        self.command = "AUTOGRID"
        "去掉末尾分号"
        autoGridStr = autoGridStr.split(semicolon)[0]
        seg = autoGridStr.split(blankSpace)
        self.direction = seg[1]
        self.totalCells = seg[2]
        return self

    def getAutoGridStr(self):
        return self.__encoded()

    def getAutoGrid(self, autoGridStr):
        return self.__decoded(autoGridStr)


################################第七章 外边界命令 #####################################
class Symmetry:
    "用来外部边界轴向、镜像或者周期性的对称"

    class Type(Enum):
        axial = "AXIAL" # SYMMETRY AXIAL { line, area }  POSITIVE
        mirror = "MIRROR" #SYMMETRY MIRROR { line, area }  {POSITIVE,NEGATIVE}
        periodic = "PERIODIC" #SYMMETRY PERIODIC { line, area } {POSITIVE,NEGATIVE}  { line, area } {POSITIVE,NEGATIVE};

    class TrendType(Enum):
        positive = "POSITIVE"
        negative = "NEGATIVE"

    def __init__(self, type="",trendType="",  lineOrArea1="", lineOrArea2=""):
        self.command = "SYMMETRY"
        self.type = type
        self.trendType = trendType
        self.lineOrArea1 = lineOrArea1
        self.lineOrArea2 = lineOrArea2

    def __encoded(self):
        if self.type == self.Type.axial:
            return self.command + blankSpace + \
                   self.type + blankSpace + \
                   self.lineOrArea1 + blankSpace + \
                   self.trendType + semicolon
        elif self.type == self.Type.mirror:
            return self.command + blankSpace + \
                   self.type + blankSpace + \
                   self.lineOrArea1 + blankSpace + \
                   self.trendType + semicolon
        elif self.type == self.Type.periodic:
            trendTypeOpposed = ""
            if self.trendType == self.TrendType.negative:
                trendTypeOpposed = self.TrendType.positive
            if self.trendType == self.TrendType.positive:
                trendTypeOpposed = self.TrendType.negative

            return self.command + blankSpace + \
                   self.type + blankSpace + \
                   self.lineOrArea1 + blankSpace + \
                   self.trendType + blankSpace + \
                   self.lineOrArea2 + blankSpace + \
                   trendTypeOpposed + semicolon
        else:
            return "error type"

    def __decoded(self, str):
        strs = re.split(" |;", str)

        if strs[1] == Symmetry.Type.axial:
            self.type = self.Type.axial
            self.lineOrArea1 = strs[2]
            self.trendType = strs[3]

        if strs[1] == Symmetry.Type.mirror:
            self.type = self.Type.mirror
            self.lineOrArea1 = strs[2]
            self.trendType = strs[3]

        if strs[1] == Symmetry.Type.periodic:
            self.type = self.Type.periodic
            self.lineOrArea1 = strs[2]
            self.trendType = strs[3]
            self.lineOrArea2 = strs[4]

    def getSymmetryStr(self):
        return self.__encoded()

    def getSymmetryObject(self, str):
        self.__decoded(str)
        return self


class Port:

    class DirectionType(Enum):
        positive = "POSITIVE"
        negative = "NEGATIVE"

    class OptionsType(Enum):
        phase_velocity = "PHASE_VELOCITY" # 相对相速因子
        expansion = "EXPANSION" # 法向修正
        incoming = "INCOMING"
        normalization = "NORMALIZATION" # 归一化
        laplacian = "LAPLACIAN"
        circuit = "CIRCUIT" # 电流

    "定义输入、输出端口"
    def __init__(self, areaName="", directionType="NEGATIVE",
                    isPhaseVelocity=False, phaseVelocity="1",
                    isScale=False, scale="1",
                    isFt=False,
                    isGeFirst=False, geFirstName="0.0",
                    isGeSecond=False, geSecondName="0.0",
                    isNormalization=False,normalizationLine="未指定",
                    isLaplacian=False, laplacianFirst="未指定", laplacianSecond="未指定",
                    laplacenumber1="1",laplacenumber2="0",
                    laplacianThird="未指定", laplacianFourth="未指定",laplacianFifth="未指定",
                    laplacenumber3="0",laplacenumber4="0",laplacenumber5="0",
                    laplace_num = "2",
                    circuit_Checked = False,circuit = "",observe_name = ''):
        self.command = "PORT"
        self.areaName = areaName
        self.directionType = directionType
        self.isPhaseVelocity = isPhaseVelocity
        self.phaseVelocity = phaseVelocity
        self.isScale = isScale
        self.scale = scale
        self.isFt = isFt
        self.isGeFirst = isGeFirst
        self.geFirstName = geFirstName
        self.isGeSecond = isGeSecond
        self.geSecondName = geSecondName
        self.isNormalization = isNormalization
        self.normalizationLine = normalizationLine
        self.isLaplacian = isLaplacian
        self.laplacianFirst = laplacianFirst
        self.laplacianSecond = laplacianSecond
        self.laplacianThird = laplacianThird
        self.laplacianFourth = laplacianFourth
        self.laplacianFifth = laplacianFifth

        self.circuit_Checked = circuit_Checked
        self.circuit = circuit

        self.laplacenum1 = str(laplacenumber1)
        self.laplacenum2 = str(laplacenumber2)
        self.laplacenum3 = str(laplacenumber3)
        self.laplacenum4 = str(laplacenumber4)
        self.laplacenum5 = str(laplacenumber5)

        self.observe_name = observe_name

        self.laplace_num  = laplace_num

    def __encoded(self):

        options = ""
        
        if self.isPhaseVelocity:
            options = options + newline + tab + \
                      self.OptionsType.phase_velocity + blankSpace + \
                      self.phaseVelocity + blankSpace

        if self.isScale:
            options = options + newline + tab + \
                      self.OptionsType.expansion + blankSpace + \
                      self.scale + blankSpace

        if self.isFt and self.isGeFirst or self.isFt and self.isGeSecond:
            if self.isGeFirst and self.isGeSecond:
                options = options + newline + tab + \
                          self.OptionsType.incoming + blankSpace + \
                          self.areaName + symbolPoint + "F" + blankSpace + \
                          "FUNCTION" + blankSpace + \
                          self.geFirstName[1:3] + blankSpace + \
                          self.areaName + symbolPoint + self.geFirstName + blankSpace + \
                          self.geSecondName[1:3] + blankSpace + \
                          self.areaName + symbolPoint + self.geSecondName + blankSpace
            elif self.isGeFirst and not self.isGeSecond:
                options = options + newline + tab + \
                          self.OptionsType.incoming + blankSpace + \
                          self.areaName + symbolPoint + "F" + blankSpace + \
                          "FUNCTION" + blankSpace + \
                          self.geFirstName[1:3] + blankSpace + \
                          self.areaName + symbolPoint + self.geFirstName + blankSpace
            elif not self.isGeFirst and self.isGeSecond:
                options = options + newline + tab + \
                          self.OptionsType.incoming + blankSpace + \
                          self.areaName + symbolPoint + "F" + blankSpace + \
                          "FUNCTION" + blankSpace + \
                          self.geSecondName[1:3] + blankSpace + \
                          self.areaName + symbolPoint + self.geSecondName + blankSpace
            elif not self.isGeFirst and not self.isGeSecond:
                options = options + newline + tab + \
                          self.OptionsType.incoming + blankSpace + \
                          self.areaName + symbolPoint + "F" + blankSpace

        if self.isFt and self.isLaplacian:
            if self.laplacianFirst != "" and self.laplacianSecond != "":
                options = options + newline + tab + \
                          self.OptionsType.incoming + blankSpace + \
                          self.areaName + symbolPoint + "F" + blankSpace + \
                          self.OptionsType.laplacian + blankSpace + \
                          str(self.laplace_num) + blankSpace + \
                          self.laplacianFirst + blankSpace + self.laplacenum1 + blankSpace +\
                          self.laplacianSecond + blankSpace + self.laplacenum2 + blankSpace
                # FreeCAD.Console.PrintError('\n\n\n!!!!!!!!!!!!!@@@@@@@@@@@@@###########'+str(self.laplace_num))
                if int(self.laplace_num) >= 3:
                    options = options + self.laplacianThird + blankSpace + self.laplacenum3 + blankSpace
                if int(self.laplace_num) >= 4: 
                    options = options + self.laplacianFourth + blankSpace + self.laplacenum4 + blankSpace
                if int(self.laplace_num) >= 5: 
                    options = options + self.laplacianFifth+ blankSpace + self.laplacenum5 + blankSpace
            elif self.laplacianFirst != "" and self.laplacianSecond == "":
                options = options + newline + tab + \
                          self.OptionsType.incoming + blankSpace + \
                          self.areaName + symbolPoint + "F" + blankSpace + \
                          self.OptionsType.laplacian + blankSpace + \
                          "1" + blankSpace + \
                          self.laplacianFirst + blankSpace + self.laplacenum1 + blankSpace
            elif self.laplacianFirst == "" and self.laplacianSecond != "":
                options = options + newline + tab + \
                          self.OptionsType.incoming + blankSpace + \
                          self.areaName + symbolPoint + "F" + blankSpace + \
                          self.OptionsType.laplacian + blankSpace + \
                          "1" + blankSpace + \
                          self.laplacianSecond + blankSpace + self.laplacenum2 + blankSpace

        if self.isNormalization:
            # if self.circuit_Checked is False:
            options = options + newline + tab + \
                        self.OptionsType.normalization + blankSpace + \
                        "VOLTAGE" + blankSpace + \
                        self.normalizationLine + blankSpace
            # if self.circuit_Checked :
            #     options = options + newline + tab + \
            #             self.OptionsType.normalization + blankSpace + \
            #             "VOLTAGE" + blankSpace + \
            #             self.normalizationLine + blankSpace + \
            #             newline + tab + \
            #             self.OptionsType.circuit + blankSpace + \
            #             str(self.circuit) + blankSpace + \
            #             self.areaName + symbolPoint + "F" + blankSpace + \
            #             "OBS$" + str(self.observe_name) + "Voltage" + semicolon +\
            #             newline +  \
            #             "OBSERVE FIELD_INTEGRAL E.DL" + blankSpace + \
            #             self.normalizationLine + blankSpace + \
            #             "suffix" + blankSpace + self.areaName + "Voltage"
        # 修改circuit的m3d生成逻辑 @ lizhenguang
        if self.circuit_Checked:
            options = options + newline +tab + \
                    self.OptionsType.circuit + blankSpace + \
                    str(self.circuit) + blankSpace + \
                        self.areaName + symbolPoint + "F" + blankSpace + 'OBS$' + str(self.observe_name)
       

        return self.command + blankSpace + \
               self.areaName + blankSpace + \
               self.directionType + blankSpace + \
               options + semicolon

    def __decoded(self, str):
        strs = str.split("\n")

        for line in strs:
            if line.startswith(self.command):
                lines = re.split(" |;", line)
                self.areaName = lines[1]
                self.directionType = lines[2]
            if line.startswith("\t") and self.OptionsType.phase_velocity in line:
                lines = re.split(" |;", line)
                self.isPhaseVelocity = True
                self.phaseVelocity = lines[1]
            if line.startswith("\t") and self.OptionsType.expansion in line:
                lines = re.split(" |;", line)
                self.isScale = True
                self.scale = lines[1]
            if line.startswith("\t") and ".F" in line:
                self.isFt = True
            if line.startswith("\t") and "LAPLACIAN" in line:
                lines = re.split(" |;", line)
                self.isLaplacian = True
                # FreeCAD.Console.PrintError('\n\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                # FreeCAD.Console.PrintError(lines)
                if lines[3] == "1":
                    self.laplacianFirst = lines[4]
                if lines[3] == "2":
                    self.laplace_num = lines[3]
                    self.laplacianFirst = lines[4]
                    self.laplacenum1 = lines[5]
                    self.laplacianSecond = lines[6]
                    self.laplacenum2 = lines[7]
                if lines[3] == "3":
                    self.laplace_num = lines[3]
                    self.laplacianFirst = lines[4]
                    self.laplacenum1 = lines[5]
                    self.laplacianSecond = lines[6]
                    self.laplacenum2 = lines[7]
                    self.laplacianThird= lines[8]
                    self.laplacenum3 = lines[9]
                if lines[3] == "4":
                    self.laplace_num = lines[3]
                    self.laplacianFirst = lines[4]
                    self.laplacenum1 = lines[5]
                    self.laplacianSecond = lines[6]
                    self.laplacenum2 = lines[7]
                    self.laplacianThird= lines[8]
                    self.laplacenum3 = lines[9]
                    self.laplacianFourth= lines[10]
                    self.laplacenum4 = lines[11]
                if lines[3] == "5":
                    self.laplace_num = lines[3]
                    self.laplacianFirst = lines[4]
                    self.laplacenum1 = lines[5]
                    self.laplacianSecond = lines[6]
                    self.laplacenum2 = lines[7]
                    self.laplacianThird= lines[8]
                    self.laplacenum3 = lines[9]
                    self.laplacianFourth= lines[10]
                    self.laplacenum4 = lines[11]
                    self.laplacianFifth= lines[12]
                    self.laplacenum5 = lines[13]
            if line.startswith("\t") and self.OptionsType.normalization in line:
                lines = re.split(" |;", line)
                self.isNormalization = True
                self.normalizationLine = lines[2]
            # circuit的M3D @lizhenguang
            if line.startswith("\t") and self.OptionsType.circuit in line:
                lines = re.split(" |;",line)
                self.circuit_Checked = True
                self.circuit = lines[1]
                self.observe_name = lines[3].replace('OBS$','').replace('Voltage','')
                

    def getPortStr(self):
        return self.__encoded()

    def getPortObject(self, str):
        self.__decoded(str)
        # FreeCAD.Console.PrintError('\n\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        # FreeCAD.Console.PrintError(self.laplacianFourth)
        return self
class Merge:
    class Comm_Merge(Enum):
        species = "SPECIES"
        maxn_p = "MAXN_PERCELL"
        maxn_w = "MAXN_WHOLE"
    def __init__(self,name = "",Types = "ALL",everyNum = "1",maxNum = "50000"):
        self.command = "MERGE"
        self.name = name
        self.types = str(Types)
        self.everyNum = everyNum
        self.maxNum = maxNum
    def __encode(self):
        return self.command + blankSpace + self.Comm_Merge.species + \
                blankSpace + self.types + blankSpace + self.Comm_Merge.maxn_p + blankSpace +\
                self.everyNum + blankSpace + self.Comm_Merge.maxn_w + blankSpace + self.maxNum + semicolon
    def __decoded(self,str):
        strs = re.split(" |;", str)
        self.types = strs[2]
        self.everyNum = strs[4]
        self.maxNum = strs[6]

    def getMergeStr(self):
        # FreeCAD.Console.PrintError("\n生成111")
        return self.__encode()
    def getMergeObject(self, str):
        self.__decoded(str)
        return self
class Mark_sup:
    def __init__(self, name = "", mark_obj = "", direction = "", 
                isChecked_min = False, isChecked_mid = False, isChecked_max = False, size = ""):
        self.command = "MARK"
        self.name = name
        self.mark_obj = mark_obj
        self.direction = direction
        self.isChecked_min = isChecked_min
        self.isChecked_mid = isChecked_mid
        self.isChecked_max = isChecked_max
        self.size = size
    def __encoded(self):
        returnStr = self.command + blankSpace + self.mark_obj + blankSpace + \
                    self.direction + blankSpace
        if self.isChecked_min:
            returnStr = returnStr + "MINIMUM" + blankSpace
        if self.isChecked_mid:
            returnStr = returnStr + "MIDPOINT" + blankSpace
        if self.isChecked_max:
            returnStr = returnStr + "MAXIMUM" + blankSpace
        returnStr = returnStr + "SIZE" + blankSpace + self.size + semicolon;

        return returnStr
    def getMarkStr(self):
        return self.__encoded()
    pass
class Gasgas:
    class Comm(Enum):
        gasKind = "GASKIND"
        pressure = "PRESSURE"
        temperture = "TEMPERATURE"
    def __init__(self,name = "",types= "",pre= "",temp= ""):
        self.command = "GASGAS"
        self.name = name
        self.types = types
        self.pre = pre # 压强
        self.temp = temp # 温度
    def __encode(self):
        return self.command + blankSpace + self.Comm.gasKind + blankSpace +\
                self.types + blankSpace + self.Comm.pressure + blankSpace +\
                self.pre + blankSpace + self.Comm.temperture + blankSpace +\
                self.temp + semicolon
    def getGasgasStr(self):
        return self.__encode()
    def __decoded(self, str):
        strs = str.split("\n")
        for i in strs:
            if i.startswith("!!"):
                self.name = i.replace("!!","")
            if i.startswith(self.command):
                tempStr = re.split(" |;", i )
                self.types = tempStr[2]
                self.pre = tempStr[4]
                self.temp = tempStr[6]
    def getGasgasObject(self, str):
        self.__decoded(str)
        return self
class Species:
    class Comm(Enum):
        charge = "CHARGE"
        mass = "MASS"
    def __init__(self,name = "",powerUnitl = "",quality = "",massUnit = ""):
        self.command = "SPECIES"
        self.name = name
        self.powerUnitl = powerUnitl
        self.quality = quality
        self.massUnit = massUnit
    def __decoded(self,speciesStr):
        self.command = "SPECIES"
        "去掉末尾分号"
        speciesStr = speciesStr.split(semicolon)[0]
        seg = speciesStr.split(blankSpace)
        self.name=seg[1]
        self.powerUnitl=seg[3]
        self.quality=seg[5]
        self.massUnit = seg[6]
    def __encode(self):
        return self.command + blankSpace + self.name + blankSpace +\
                self.Comm.charge + blankSpace + self.powerUnitl + blankSpace +\
                self.Comm.mass + blankSpace + self.quality + blankSpace +\
                self.massUnit + semicolon
    def getSpeciesStr(self):
        return self.__encode()
    def getSpecies(self, materialStr):
        return self.__decoded(materialStr)

class Populate:
    class Comm(Enum):
        function = "FUNCTION"
        density = "DENSITY"
        temp = "TEMPERATURE"
    def __init__(self,name = "",types = "",volume = "",X1 = "",Y1 = "",Z1 = "",X2 = "",Y2 = "",Z2 = "",density = "",temp = ""):
        self.command = "POPULATE"
        self.name = name
        self.types = types
        self.volume = volume
        self.X1 = X1
        self.Y1 = Y1
        self.Z1 = Z1
        self.X2 = X2
        self.Y2 = Y2
        self.Z2 = Z2
        self.density = density
        self.temp = temp
    def __encode(self):
        returnStr = self.command + blankSpace + self.types + blankSpace +\
                    self.volume + blankSpace + self.X1 + blankSpace +\
                    self.Y1 + blankSpace + self.Z1 + blankSpace +\
                    self.Comm.function + blankSpace + self.Comm.density + blankSpace +\
                    self.density + blankSpace + self.X2 + blankSpace +\
                    self.Y2 + blankSpace + self.Z2 + blankSpace +\
                    self.Comm.temp + blankSpace + self.temp + semicolon
        # FreeCAD.Console.PrintError("\nm3d:  "+str(returnStr))
        return returnStr
    def __decoded(self, str):
        strs = str.split("\n")
        for i in strs:
            if i.startswith("!!"):
                self.name = i.replace("!!","")
            if i.startswith(self.command):
                temp = re.split(" |;", i )
                self.types = temp[1]
                self.volume = temp[2]
                self.X1 = temp[3]
                self.Y1 = temp[4]
                self.Z1 = temp[5]
                self.density = temp[8]
                self.X2 = temp[9]
                self.Y2 = temp[10]
                self.Z2 = temp[11]
                self.temp = temp[13]
        
    def getPopulateStr(self):
        return self.__encode()
    def getPopulateObject(self, str):
        self.__decoded(str)
        return self

class EmSE:
    class Comm_EmSE(Enum):
        sec = "SECONDARY"
        model = "MODEL"
        WF = "WEIGHT_FACTOR"
        ED = "ENERGY_DISTRIBUTION"
        AD = "ANGLE_DISTRIBUTION"
    def __init__(self,name = "",energySec = "",maxNum = "",WEIGHT_FACTOR = "",ENERGY_DISTRIBUTION = "",min_energy = "",
                    max_energy = "",ANGLE_DISTRIBUTION = "",isCheck_WF = False,isCheck_ED = False,isCheck_AD =False):
        self.command = "EMISSION"
        self.name = name
        self.energySec = energySec
        self.maxNum = maxNum
        self.WEIGHT_FACTOR = WEIGHT_FACTOR
        # self.ENERGY_DISTRIBUTION = ENERGY_DISTRIBUTION
        self.ENERGY_DISTRIBUTION = "FED_" + name
        self.min_energy = min_energy
        self.max_energy = max_energy
        # self.ANGLE_DISTRIBUTION = ANGLE_DISTRIBUTION
        self.ANGLE_DISTRIBUTION = "FAD_" + name
        self.isCheck_WF = isCheck_WF
        self.isCheck_ED = isCheck_ED
        self.isCheck_AD = isCheck_AD
    def __encode(self):
        returnStr = self.command + blankSpace + self.Comm_EmSE.sec + blankSpace + \
                 self.energySec + blankSpace + self.maxNum + \
                 newline + tab + \
                 self.Comm_EmSE.model + blankSpace + self.name
        # FreeCAD.Console.PrintError("\n生成111")
        if self.isCheck_WF:
            returnStr = returnStr + newline + tab + \
                self.Comm_EmSE.WF + blankSpace + self.WEIGHT_FACTOR
        # FreeCAD.Console.PrintError("\n生成222")
        if self.isCheck_ED:
            returnStr = returnStr + newline + tab + \
                self.Comm_EmSE.ED + blankSpace + self.ENERGY_DISTRIBUTION + blankSpace+\
                self.min_energy + blankSpace + self.max_energy
        # FreeCAD.Console.PrintError("\n生成333")
        if self.isCheck_AD:
            returnStr = returnStr + newline + tab +\
                self.Comm_EmSE.AD + blankSpace + self.ANGLE_DISTRIBUTION
        # FreeCAD.Console.PrintError("\n生成444")
        returnStr = returnStr + semicolon
        return returnStr
    def __decoded(self, str):
        strs = str.split("\n")
        for i in strs:
            if i.startswith("EMISSION"):
                tempStr = re.split(" |;", i)
                # FreeCAD.Console.PrintError("\nEmse内部字符串解析  EMISSIOB:   ")
                # FreeCAD.Console.PrintError(tempStr)
                self.energySec = tempStr[2]
                self.maxNum = tempStr[3]
            if i.startswith("\tMODEL"):
                tempStr = re.split(" |;", i)
                # FreeCAD.Console.PrintError("\nEmse内部字符串解析:   ")
                # FreeCAD.Console.PrintError(tempStr)
                self.name = tempStr[1]
            if i.startswith("\tWEIGHT_FACTOR"):
                tempStr = re.split(" |;", i)
                self.WEIGHT_FACTOR = tempStr[1]
                self.isCheck_WF = True
            if i.startswith("\tENERGY_DISTRIBUTION"):
                tempStr = re.split(" |;", i)
                self.min_energy = tempStr[2]
                self.max_energy = tempStr[3]
    def getEmSEstr(self):
        return self.__encode()
    def getEmseObject(self,str):
        self.__decoded(str)
        return self
class Freespace:
    class XType(Enum):
        x1 = "X1"
        x2 = "X2"
        x3 = "X3"

    class TrendType(Enum):
        positive = "POSITIVE"
        negative = "NEGATIVE"

    def __init__(self, freeSpaceName="", trendType="NEGATIVE", xType="X1", component="B3", isConductivity= False, funName=""):

        self.command = "FREESPACE"
        self.freeSpaceName = freeSpaceName
        self.trendType = trendType
        self.xType = xType
        self.component = component
        self.isConductivity = isConductivity
        self.funName = funName

    def __encoded(self):
        returnStr = self.command + blankSpace + \
                    self.freeSpaceName + blankSpace + \
                    self.trendType + blankSpace + \
                    self.xType + blankSpace + \
                    self.component
        if self.isConductivity:
            return returnStr + blankSpace + \
                    "CONDUCTIVITY" + blankSpace + \
                    self.funName + semicolon
        else:
            return returnStr + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)
        self.freeSpaceName = strs[1]
        self.trendType = strs[2]
        self.xType = strs[3]
        self.component = strs[4]
        if strs[5] == "CONDUCTIVITY":
            self.isConductivity = True

    def getFreespaceStr(self):
        return self.__encoded()

    def getFreespaceObject(self, str):
        self.__decoded(str)
        return self


################################第九章 材料属性命令 #####################################
class Conductance:
    " 在模拟区域内的对象上赋予有限电导率特性"
    def __init__(self, volumeName="", sigma="",sigma2 = '',sigma3 = '',isconductance = ''):
        self.command = "CONDUCTANCE"
        self.volumeName = volumeName
        self.sigma = sigma
        self.sigma2 = sigma2
        self.sigma3 = sigma3
        self.isconductance = isconductance

    def __encoded(self):
        if self.isconductance == 'Anisotropy':
            return self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.sigma + blankSpace + "X1" + semicolon + newline + \
                   self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.sigma2 + blankSpace + "X2" + semicolon + newline + \
                   self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.sigma3 + blankSpace + "X3" + semicolon
        elif self.isconductance == 'Isotropy':
            return self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.sigma + semicolon

    def __decoded(self, conductanceStr):
        # self.command = "CONDUCTANCE"
        # "去掉末尾分号"
        # conductorStr = conductanceStr.split(semicolon)[0]
        # seg = conductorStr.split(blankSpace)
        # self.volumeName = seg[1]
        # self.sigma = seg[2]
        # return self
        # 调整后的解析功能 @lizhenguang
        self.command = "CONDUCTANCE"
        "去掉末尾分号"
        conductorStr = conductanceStr.split(semicolon)[0]
        seg = conductorStr.split(blankSpace)
        self.volumeName = seg[1]
        if len(seg) == 3:
            self.isconductance = 'Isotropy'
            self.sigma = seg[2]
        elif len(seg) == 4:
            self.isconductance = 'Anisotropy'
            # if seg[3] == "EPS1":
            #     self.sigma = seg[2]
            # elif seg[3] == "EPS2":
            #     self.sigma2 = seg[2]
            # elif seg[3] == "EPS3":
            #     self.sigma3 = seg[2]
            if seg[3] == "X1":
                self.sigma = seg[2]
            elif seg[3] == "X2":
                self.sigma2 = seg[2]
            elif seg[3] == "X3":
                self.sigma3 = seg[2]
        return self

    def getConductanceStr(self):
        return self.__encoded()

    def getConductance(self, conductanceStr):
        return self.__decoded(conductanceStr)


class Dielectric:
    "为模拟区域中的面积对象赋予介质属性"

    def __init__(self, volumeName="", isotropy=True, permittivity1="", permittivity2="", permittivity3=""):
        self.command = "DIELECTRIC"
        self.volumeName = volumeName
        self.isotropy = isotropy
        self.permittivity1 = permittivity1
        self.permittivity2 = permittivity2
        self.permittivity3 = permittivity3

    def __encoded(self):

        if self.isotropy:
            return self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.permittivity1 + semicolon
        else:
            return self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.permittivity1 + blankSpace + "X1" + semicolon + newline + \
                   self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.permittivity2 + blankSpace + "X2" + semicolon + newline + \
                   self.command + blankSpace + \
                   self.volumeName + blankSpace + \
                   self.permittivity3 + blankSpace + "X3" + semicolon

    def __decoded(self, dielectricStr):
        self.command = "DIELECTRIC"
        "去掉末尾分号"
        conductorStr = dielectricStr.split(semicolon)[0]
        seg = conductorStr.split(blankSpace)
        FreeCAD.Console.PrintError("\n 逆反转！！"+str(seg))
        self.volumeName = seg[1]
        if len(seg) == 3:
            self.isotropy = True
            self.permittivity1 = seg[2]
        elif len(seg) == 4:
            self.isotropy = False
            # if seg[3] == "EPS1":
            #     self.permittivity1 = seg[2]
            # elif seg[3] == "EPS2":
            #     self.permittivity2 = seg[2]
            # elif seg[3] == "EPS3":
            #     self.permittivity3 = seg[2]
            if seg[3] == "X1":
                self.permittivity1 = seg[2]
            elif seg[3] == "X2":
                self.permittivity2 = seg[2]
            elif seg[3] == "X3":
                self.permittivity3 = seg[2]
        return self

    def getDielectricStr(self):
        return self.__encoded()

    def getDielectric(self, dielectricStr):
        return self.__decoded(dielectricStr)


class Conductor:
    "给一个空间物体指明一个理想的（或初始化）传导率。其同样也可指明电子有弹性或无弹性反向散射的属性。" \
    "另外，其还可以指明一个物质的表面属性，虽然这对实际的导体属性并不起作用。"

    def __init__(self, areaOrVolume=""):
        self.command = "CONDUCTOR"
        self.areaOrVolume = areaOrVolume

    def __encoded(self):
        return self.command + blankSpace + \
                self.areaOrVolume + semicolon

    def __decoded(self, conductorStr):
        self.command = "CONDUCTOR"
        "去掉末尾分号"
        conductorStr = conductorStr.split(semicolon)[0]
        seg = conductorStr.split(blankSpace)
        self.areaOrVolume = seg[1]
        return self

    def getConductorStr(self):
        return self.__encoded()

    def getConductor(self, conductorStr):
        return self.__decoded(conductorStr)


class Void:
    "用来在一个空间物体内部挖一个空的区域"

    # VOID volume ;

    def __init__(self, volumeName=""):
        self.command = "VOID"
        self.volumeName = volumeName


    def __encoded(self):
        return self.command + blankSpace + \
               self.volumeName + semicolon

    def __decoded(self, conductorStr):
        self.command = "VOID"
        "去掉末尾分号"
        conductorStr = conductorStr.split(semicolon)[0]
        seg = conductorStr.split(blankSpace)
        self.volumeName = seg[1]
        return self

    def getVoidStr(self):
        return self.__encoded()

    def getVoid(self, voidStr):
        return self.__decoded(voidStr)


class Material:
    def __init__(self, name="", atomicNumber="1", atomicMass="1", massDensity="1",
                 isConductivity=False, conductivity="1",
                 isPermittivity=False, permittivity="1"):
        self.command = "MATERIAL"
        self.name = name
        self.atomicNumber = atomicNumber
        self.atomicMass = atomicMass
        self.massDensity = massDensity
        self.conductivity = conductivity
        self.permittivity = permittivity
        self.isConductivity = isConductivity
        self.isPermittivity = isPermittivity

    def __encoded(self):
        returnStr = self.command + blankSpace + \
               self.name + blankSpace +\
               "ATOMIC_NUMBER" + blankSpace + self.atomicNumber + blankSpace + \
               "ATOMIC_MASS" + blankSpace + self.atomicMass + blankSpace + \
               "MASS_DENSITY" + blankSpace + self.massDensity

        if self.isConductivity:
            returnStr = returnStr + blankSpace + "CONDUCTIVITY" + blankSpace + self.conductivity

        if self.isPermittivity:
            returnStr = returnStr + blankSpace + "PERMITTIVITY" + blankSpace + self.permittivity

        return returnStr + semicolon

    def __decoded(self, materialStr):
        self.command = "MATERIAL"
        "去掉末尾分号"
        materialStr = materialStr.split(semicolon)[0]
        seg = materialStr.split(blankSpace)
        self.name = seg[1]
        self.atomicNumber = seg[3]
        self.atomicMass = seg[5]
        self.massDensity = seg[7]
        if len(seg)== 10:
            self.conductivity = seg[9]
            self.isConductivity = True
        if  len(seg) == 12:
            self.permittivity = seg[11]
            self.isPermittivity = True

        return self

    def getMaterialStr(self):
        return self.__encoded()

    def getMaterial(self, materialStr):
        return self.__decoded(materialStr)


class Solenoid:
    class Type(Enum):
        none = "none"
        rz = "rz"
        other = "other"

    def __init__(self, type, name, zCenter, rCenter, innerRadius, outerRadius, coilCurrent, coilRadius, coilNum,
                 theta, phi, rFactor, zFactor, spaceRatio, innerRadius2, outerRadius2, magneticRatio):
        self.command = "SOLENOID"
        self.type = type
        self.name = name
        self.zCenter = zCenter
        self.rCenter = rCenter
        self.innerRadius = innerRadius
        self.outerRadius = outerRadius
        self.coilCurrent = coilCurrent
        self.coilRadius = coilRadius
        self.coilNum = coilNum
        self.theta = theta
        self.phi = phi
        self.rFactor = rFactor
        self.zFactor = zFactor
        self.spaceRatio = spaceRatio
        self.innerRadius2 = innerRadius2
        self.outerRadius2 = outerRadius2
        self.magneticRatio = magneticRatio

    def __encoded(self):
        if self.type == self.Type.none:
            return self.command + blankSpace + \
                   self.name + blankSpace + \
                   "0 0 0 0 0" + blankSpace + \
                   self.zCenter + blankSpace + \
                   self.rCenter + blankSpace + \
                   self.innerRadius + blankSpace + \
                   self.outerRadius + blankSpace + \
                   self.coilCurrent + blankSpace + \
                   self.coilRadius + blankSpace + \
                   self.coilNum + blankSpace + \
                   self.theta + blankSpace + \
                   self.phi + semicolon

        elif self.type == self.Type.rz:
            return self.command + blankSpace + \
                   self.name + blankSpace + \
                   "1" + blankSpace + \
                   self.rFactor + blankSpace + \
                   self.zFactor + blankSpace + \
                   "0 0" + blankSpace + \
                   self.zCenter + blankSpace + \
                   self.rCenter + blankSpace + \
                   self.innerRadius + blankSpace + \
                   self.outerRadius + blankSpace + \
                   self.coilCurrent + blankSpace + \
                   self.coilRadius + blankSpace + \
                   self.coilNum + blankSpace + \
                   self.theta + blankSpace + \
                   self.phi + semicolon

        elif self.type == self.Type.other:
            return self.command + blankSpace + \
                   self.name + blankSpace + \
                   "2" + blankSpace + \
                   self.spaceRatio + blankSpace + \
                   self.innerRadius2 + blankSpace + \
                   self.outerRadius2 + blankSpace + \
                   self.magneticRatio + blankSpace + \
                   self.zCenter + blankSpace + \
                   self.rCenter + blankSpace + \
                   self.innerRadius + blankSpace + \
                   self.outerRadius + blankSpace + \
                   self.coilCurrent + blankSpace + \
                   self.coilRadius + blankSpace + \
                   self.coilNum + blankSpace + \
                   self.theta + blankSpace + \
                   self.phi + semicolon
        else:
            return "错误的type"

    def getSolenoidStr(self):
        return self.__encoded()


class Foil:
    def __init__(self, name="", thick="", material=""):
        self.command = "FOIL"
        self.name = name
        self.thick = thick
        self.material = material

    def __encoded(self):
        return self.command + blankSpace + \
               self.name + blankSpace + \
               self.thick + blankSpace + \
               self.material + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)

        self.name = strs[1]
        self.thick = strs[2]
        self.material = strs[3]

        return self

    def getFoilStr(self):
        return self.__encoded()

    def getFoilObject(self, str):
        return self.__decoded(str)


class Inductor:
    def __init__(self, name="", diameter="", isInductance=False, inductance=""):
        self.command = "INDUCTOR"
        self.name = name
        self.diameter = diameter
        self.isInductance = isInductance
        self.inductance = inductance

    def __encoded(self):
        if self.isInductance:
            return self.command + blankSpace + \
                   self.name + blankSpace + \
                   self.diameter + blankSpace + \
                   "INDUCTANCE" + blankSpace + \
                   self.inductance + semicolon
        else:
            return self.command + blankSpace + \
                   self.name + blankSpace + \
                   self.diameter + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)

        if len(strs)>5:
            self.name = strs[1]
            self.diameter = strs[2]
            self.inductance = strs[4]
            self.isInductance = True
        else:
            self.name = strs[1]
            self.diameter = strs[2]

        return self

    def getInductorStr(self):
        return self.__encoded()

    def getInductorObject(self, str):
        return self.__decoded(str)


class Driver:
    def __init__(self, name="", currentDensity="", funName="",source_type = ""):
        self.command = "DRIVER"
        self.name = name
        self.currentDensity = currentDensity
        self.funName = funName
        self.source_type = source_type

    def __encoded(self):
        if self.source_type == "未指定":
            return self.command + blankSpace + \
               self.currentDensity + blankSpace + \
               self.funName + blankSpace + \
               self.name + semicolon
        else:
            return self.command + blankSpace + \
               self.currentDensity + blankSpace + \
               self.funName + blankSpace + \
               self.source_type + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)

        self.currentDensity = strs[1]
        self.funName = strs[2]
        self.name = strs[3]

        return self

    def getDriverStr(self):
        return self.__encoded()

    def getDriverObject(self, str):
        return self.__decoded(str)


###############################第十一章 发射过程命令##################################
class EmissionBeam:

    def __init__(self, emitName=""):
        self.command = "EMISSION BEAM"
        self.emitName = emitName

    def __encoded(self):
        return self.command + blankSpace + \
                self.emitName + symbolPoint + "BeamJ" + blankSpace + \
                self.emitName + symbolPoint + "BeamV" + blankSpace + blankSpace

    def getEmissionBeamStr(self):
        return self.__encoded()


class EmissionExplosive:
        def __init__(self, emitName="", isTField=False, isRField=False, isCharg=False, isFRate=False,):
            self.command = "EMISSION EXPLOSIVE"
            self.emitName = emitName
            self.isTField = isTField
            self.isRField = isRField
            self.isCharg = isCharg
            self.isFRate = isFRate

        def __encoded(self):
            returnStr = self.command + blankSpace

            if self.isTField:
                returnStr = returnStr + "THRESHOLD" + blankSpace + self.emitName + symbolPoint + "TField" + blankSpace

            if self.isRField:
                returnStr = returnStr + "RESIDUAL" + blankSpace + self.emitName + symbolPoint + "RField" + blankSpace

            if self.isFRate:
                returnStr = returnStr + "PLASMA" + blankSpace + self.emitName + symbolPoint + "FRate" + blankSpace

            if self.isCharg:
                returnStr = returnStr + "MINIMUM_CHARGE" + blankSpace + self.emitName + symbolPoint + "Charg" + blankSpace

            return returnStr

        def __decoded(self, str):
            if "TField" in str:
                self.isTField = True

            if "RField" in str:
                self.isRField = True

            if "Charg" in str:
                self.isCharg = True

            if "FRate" in str:
                self.isFRate = True

            return self

        def getEmissionExplosiveStr(self):
            return self.__encoded()

        def getEmissionExplosiveObject(self, str):
            return self.__decoded(str)


class EmissionGyro:

    class Direction(Enum):
        x1 = "X1"
        x2 = "X2"
        x3 = "X3"

    def __init__(self, emitName="", Bg="", Pl="", Pt="", Dgc="", direction=""):
        self.command = "EMISSION GYRO"
        self.emitName = emitName
        self.Bg = Bg
        self.Pl = Pl
        self.Pt = Pt
        self.Dgc = Dgc
        self.direction = direction

    def __encoded(self):
        return self.command + blankSpace + \
               self.emitName + symbolPoint + "I" + blankSpace + \
               self.Bg + blankSpace + \
               self.Pl + blankSpace + \
               self.Pt + blankSpace + \
               self.Dgc + blankSpace + \
               self.direction + blankSpace + \
               self.emitName + symbolPoint + "CPT" + blankSpace

    def __decoded(self, str):
        strs = re.split(" |;", str)
        self.Bg = strs[3]
        self.Pl = strs[4]
        self.Pt = strs[5]
        self.Dgc = strs[6]
        self.direction = strs[7]

        return self

    def getEmissionGyroStr(self):
        return self.__encoded()

    def getEmissionGyroObject(self, str):
        return self.__decoded(str)


class EmissionHighfield:
    def __init__(self, emitName="", a="", b=""):
        self.command = "EMISSION HIGH_FIELD"
        self.emitName = emitName
        self.a = a
        self.b = b

    def __encoded(self):
        return self.command + blankSpace + \
               self.a + blankSpace + \
               self.b + blankSpace + \
               self.emitName + symbolPoint + "PHI" + blankSpace

    def __decoded(self, str):
        strs = re.split(" |;", str)
        self.a = strs[2]
        self.b = strs[3]

        return self

    def getEmissionHighfieldStr(self):
        return self.__encoded()

    def getEmissionHighfieldObject(self, str):
        return self.__decoded(str)


class EmissionThermionic:
    def __init__(self, emitName=""):
        self.command = "EMISSION THERMIONIC"
        self.emitName = emitName

    def __encoded(self):
        return self.command + blankSpace + \
                self.emitName + symbolPoint + "WF" + blankSpace + \
                self.emitName + symbolPoint + "TP" + blankSpace

    def getEmissionExplosiveStr(self):
        return self.__encoded()


class EmissionOption:

    class SpeciesType(Enum):
        electron = "ELECTRON"
        proton = "PROTON"

    class TimingType(Enum):
        timing = "TIMING"
        random_timing = "RANDOM_TIMING"

    class SpacingType(Enum):
        random = "RANDOM"
        uniform = "UNIFORM"
        fixed = "FIXED"

    def __init__(self, emitName="",
                 isSpecies=False, species="ELECTRON",
                 isNumber=False, creationRate="0",
                 isTiming=False, timingType="RANDOM_TIMING", stepMultiple="0",
                 isSurfaceSpacing=False, surfaceSpacing="RANDOM",
                 isOutwardSpacing=False, outwardSpacing="RANDOM"):
        self.emitName = emitName
        self.isSpecies = isSpecies
        self.species = species
        self.isNumber = isNumber
        self.creationRate = creationRate
        self.isTiming = isTiming
        self.timingType = timingType
        self.stepMultiple = stepMultiple
        self.isSurfaceSpacing = isSurfaceSpacing
        self.surfaceSpacing = surfaceSpacing
        self.isOutwardSpacing = isOutwardSpacing
        self.outwardSpacing = outwardSpacing

    def __encoded(self):

        returnStr = newline + tab + "MODEL" + blankSpace + self.emitName + blankSpace

        if self.isSpecies:
            returnStr = returnStr + newline + tab + "SPECIES" + blankSpace + self.species + blankSpace

        if self.isNumber:
            returnStr = returnStr + newline + tab + "NUMBER" + blankSpace + self.creationRate + blankSpace

        if self.isTiming:
            returnStr = returnStr + newline + tab + self.timingType + blankSpace + self.stepMultiple + blankSpace

        if self.isSurfaceSpacing:
            returnStr = returnStr + newline + tab + "SURFACE_SPACING" + blankSpace + self.surfaceSpacing + blankSpace

        if self.isOutwardSpacing:
            returnStr = returnStr + newline + tab + "OUTWARD_SPACING" + blankSpace + self.outwardSpacing + blankSpace + self.emitName + symbolPoint + "Dn"

        returnStr = returnStr + semicolon

        return returnStr

    def __decoded(self, str):
        strs = str.split("\n")
        for line in strs:
            # 去除可选项中的每一行的\t
            line = line[1:len(line)]

            # 如果该粒子类型可选项
            if "MODEL" in line:
                lines = re.split(" |;", line)
                self.emitName = lines[1]

            # 如果该粒子类型可选项
            if "SPECIES" in line:
                self.isSpecies = True

                lines = re.split(" |;", line)
                self.species = lines[1]

            # 如果生产率为可选项
            if "NUMBER" in line:
                self.isNumber = True

                lines = re.split(" |;", line)
                self.creationRate = lines[1]

            # 如果发射间隔为可选项
            if "TIMING" in line:
                self.isTiming = True

                lines = re.split(" |;", line)
                self.timingType = lines[0]
                self.stepMultiple = lines[1]

            # 如果沿表面分布为可选项
            if "SURFACE_SPACING" in line:
                self.isSurfaceSpacing = True

                lines = re.split(" |;", line)
                self.surfaceSpacing = lines[1]

            # 如果沿外表面分布为可选项
            if "OUTWARD_SPACING" in line:
                self.isOutwardSpacing = True

                lines = re.split(" |;", line)
                self.outwardSpacing = lines[1]

        return self

    def getEmissionExplosiveStr(self):
        return self.__encoded()

    def getEmissionExplosiveObject(self, str):
        return self.__decoded(str)


class Emit:

    class optionType(Enum):
        exclude = "EXCLUDE"
        include = "INCLUDE"

    def __init__(self, emitName="", mobject="未指定",
                 isExclude1=False, excludeVolume1="不指定", isExclude2=False, excludeVolume2="不指定",
                 isInclude1=False, includeVolume1="不指定", isInclude2=False, includeVolume2="不指定"):
        self.command = "EMIT"
        self.emitName = emitName
        self.mobject = mobject
        self.isExclude1 = isExclude1
        self.excludeVolume1 = excludeVolume1
        self.isExclude2 = isExclude2
        self.excludeVolume2 = excludeVolume2
        self.isInclude1 = isInclude1
        self.includeVolume1 = includeVolume1
        self.isInclude2 = isInclude2
        self.includeVolume2 = includeVolume2

    def __encoded(self):

        returnStr = self.command + blankSpace + \
                self.emitName + blankSpace + \
                self.mobject + blankSpace

        if self.isExclude1:
            returnStr = returnStr + self.optionType.exclude + blankSpace + self.excludeVolume1 + blankSpace

        if self.isExclude2:
            returnStr = returnStr + self.optionType.exclude + blankSpace + self.excludeVolume2 + blankSpace

        if self.isInclude1:
            returnStr = returnStr + self.optionType.include + blankSpace + self.includeVolume1 + blankSpace

        if self.isInclude2:
            returnStr = returnStr + self.optionType.include + blankSpace + self.includeVolume2 + blankSpace

        returnStr = returnStr + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;", str)

        self.mobject = strs[2]

        excludeNum = 0
        includeNum = 0
        for i in range(3, len(strs)):
            if strs[i] == "EXCLUDE":
                if excludeNum == 0:
                    self.isExclude1 = True
                    self.excludeVolume1 = strs[i+1]
                if excludeNum == 1:
                    self.isExclude2 = True
                    self.excludeVolume2 = strs[i+1]
                excludeNum = 1
                i = i+1
            if strs[i] == "INCLUDE":
                if includeNum == 0:
                    self.isInclude1 = True
                    self.includeVolume1 = strs[i+1]
                if includeNum == 1:
                    self.isInclude2 = True
                    self.includeVolume2 = strs[i+1]
                includeNum = 1
                i = i+1

        return self

    def getEmitStr(self):
        return self.__encoded()

    def getEmitObject(self, str):
        return self.__decoded(str)


###############################第十二章 电磁场命令##################################
class Maxwell:

    class Type(Enum):
        centered = "CENTERED"
        high_q = "HIGH_Q"
        biased = "BIASED"

    def __init__(self, type=""):
        self.command = "MAXWELL"
        self.type = type

    def __encoded(self):
        return self.command + blankSpace + self.type + semicolon

    def __decoded(self,str):
        strs = re.split(" |;", str)
        self.type = strs[1]
        return self

    def getMaxwellStr(self):
        return self.__encoded()

    def getMaxwellObject(self, str):
        return self.__decoded(str)

# class Maxwell:
#
#     class Type(Enum):
#         centered = "CENTERED" # 采用中心差分算法
#         high_q = "HIGH_Q" # 采用高Q算法
#         biased = "BIASED" # 采用时偏算法 MAXWELL BIASED [alpha1 alpha2 alpha3 [iterations [coefficient, ... ] ] ];
#
#     def __init__(self, type="", gamma="", alpha1="", alpha2="", alpha3="", iterations="", coefficient=""):
#         self.command = "MAXWELL"
#         self.type = type
#         self.gamma = gamma
#         self.alpha1 = alpha1
#         self.alpha2 = alpha2
#         self.alpha3 = alpha3
#         self.iterations = iterations
#         self.coefficient = coefficient
#
#     def __encoded(self):
#         if self.type == self.Type.centered:
#             return self.command + blankSpace + \
#                    self.type + semicolon
#         elif self.type == self.Type.high_q:
#             return self.command + blankSpace + \
#                    self.type + blankSpace + \
#                    self.gamma + semicolon
#         elif self.type == self.Type.biased:
#             coefficientStr = ""
#             for index in range(len(self.coefficient)):
#                 if index == 0:
#                     coefficientStr = coefficientStr + self.coefficient[index]
#                 else:
#                     coefficientStr = coefficientStr + comma + self.coefficient[index]
#
#             return self.command + blankSpace + \
#                    self.type + blankSpace + \
#                    self.alpha1 + blankSpace + \
#                    self.alpha2 + blankSpace + \
#                    self.alpha3 + blankSpace + \
#                    self.iterations + blankSpace + \
#                    coefficientStr + semicolon
#
#     def getMaxwellStr(self):
#         return self.__encoded()

class Mode:
    class Type(Enum):
        TE = "TE"
        TM = "TM"
        EM = "EM"
        BOTH = "BOTH"

    def __init__(self, type=""):
        self.command = "MODE"
        self.type = type

    def __encoded(self):
        return self.command + blankSpace + self.type + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)
        self.type = strs[1]
        return self

    def getModeStr(self):
        return self.__encoded()

    def getModeObject(self, str):
        return self.__decoded(str)

class Kinematics:
    def __init__(self,computeTimeInterval = "1",is_re = False,is_nonre = True):
        self.command = "KINEMATICS"
        self.computeTimeInterval = computeTimeInterval
        self.is_re = is_re
        self.is_nonre = is_nonre

    def __encoded(self):
        returnStr = ""
        if self.is_re:
            returnStr = self.command + blankSpace + self.computeTimeInterval + \
                        blankSpace + "RELATIVISTIC" + semicolon
        else:
            returnStr = self.command + blankSpace + self.computeTimeInterval + \
                        blankSpace + "NONRELATIVISTIC" + semicolon
        return returnStr
    def __decoded(self,str):
        strs = re.split(" |;", str)
        self.computeTimeInterval = strs[1]
        if strs[2] == "NONRELATIVISTIC":
            self.is_re = False
            self.is_nonre = True
        else:
            self.is_re = True
            self.is_nonre = False
        return self 
    def getKinematicsStr(self):
        return self.__encoded()
    def getKinematicsObject(self, str):
        return self.__decoded(str)


class TimeStep:
    def __init__(self, step=""):
        self.command = "TIME_STEP"
        self.step = step

    def __encoded(self):
        return self.command + blankSpace + self.step + "NANOSECOND" + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)
        self.step = strs[1].split("NANOSECOND")[0]
        return self

    def getTimeStepStr(self):
        return self.__encoded()

    def getTimeStepObject(self, str):
        return self.__decoded(str)
    # 在self.step是一个变量时，调用下面这个函数
    def getTimeStepStrWithoutUnits(self):
        return self.command + blankSpace + self.step +  semicolon


###############################第十三章 带电粒子命令##################################
class Continuity:
    class Type(Enum):
        conserved = "CONSERVED"

    def __init__(self, type=""):
        self.command = "CONTINUITY"
        self.type = type

    def __encoded(self):
        return self.command + blankSpace + self.type + semicolon

    def getContinuityStr(self):
        return self.__encoded()


###############################第十四章 其他运算命令##################################
class Preset:
    "指定电磁场,静磁场,静电场的初始条件"
    class Type(Enum):
        B1ST = ["B1ST", "FBXST", "FBRST", "FBZST", "FBXST(X,Y,Z)", "FBRST(R,P,Z)", "FBZST(Z,R,P)"]
        B2ST = ["B2ST", "FBYST", "FBPST", "FBRST", "FBYST(X,Y,Z)", "FBPST(R,P,Z)", "FBRST(Z,R,P)"]
        B3ST = ["B3ST", "FBZST", "FBZST", "FBPST", "FBZST(X,Y,Z)", "FBZST(R,P,Z)", "FBPST(Z,R,P)"]
        E1ST = ["E1ST", "FEXST", "FERST", "FEZST", "FEXST(X,Y,Z)", "FERST(R,P,Z)", "FEZST(Z,R,P)"]
        E2ST = ["E2ST", "FEYST", "FEPST", "FERST", "FEYST(X,Y,Z)", "FEPST(R,P,Z)", "FERST(Z,R,P)"]
        E3ST = ["E3ST", "FEZST", "FEZST", "FEPST", "FEZST(X,Y,Z)", "FEZST(R,P,Z)", "FEPST(Z,R,P)"]

    class CoordinateSystem(Enum):
        rectangularSys = "R"
        polarSys = "P"
        cylindricalSys = "C"

    def __init__(self, type="", coordinateSystem=""):
        self.command = "PRESET"
        self.type = type
        self.coordinateSystem = coordinateSystem

    def getFunN(self):
        funN = ""
        if self.coordinateSystem == self.CoordinateSystem.rectangularSys:
            funN = 4
        if self.coordinateSystem == self.CoordinateSystem.polarSys:
            funN = 5
        if self.coordinateSystem == self.CoordinateSystem.cylindricalSys:
            funN = 6

        if self.type == self.Type.B1ST:
            return self.Type.B1ST[funN]

        if self.type == self.Type.B2ST:
            return self.Type.B2ST[funN]

        if self.type == self.Type.B3ST:
            return self.Type.B3ST[funN]

        if self.type == self.Type.E1ST:
            return self.Type.E1ST[funN]

        if self.type == self.Type.E2ST:
            return self.Type.E2ST[funN]

        if self.type == self.Type.E3ST:
            return self.Type.E3ST[funN]

    def __encoded(self):
        content = 0
        if self.coordinateSystem == self.CoordinateSystem.rectangularSys:
            content = 1
        if self.coordinateSystem == self.CoordinateSystem.polarSys:
            content = 2
        if self.coordinateSystem == self.CoordinateSystem.cylindricalSys:
            content = 3

        if self.type == self.Type.B1ST:
            return self.command + blankSpace + \
                   self.Type.B1ST[0] + blankSpace + \
                   "FUNCTION" + blankSpace + \
                   self.Type.B1ST[content] + semicolon

        if self.type == self.Type.B2ST:
            return self.command + blankSpace + \
                   self.Type.B2ST[0] + blankSpace + \
                   "FUNCTION" + blankSpace + \
                   self.Type.B2ST[content] + semicolon

        if self.type == self.Type.B3ST:
            return self.command + blankSpace + \
                   self.Type.B3ST[0] + blankSpace + \
                   "FUNCTION" + blankSpace + \
                   self.Type.B3ST[content] + semicolon

        if self.type == self.Type.E1ST:
            return self.command + blankSpace + \
                   self.Type.E1ST[0] + blankSpace + \
                   "FUNCTION" + blankSpace + \
                   self.Type.E1ST[content] + semicolon

        if self.type == self.Type.E2ST:
            return self.command + blankSpace + \
                   self.Type.E2ST[0] + blankSpace + \
                   "FUNCTION" + blankSpace + \
                   self.Type.E2ST[content] + semicolon

        if self.type == self.Type.E3ST:
            return self.command + blankSpace + \
                   self.Type.E3ST[0] + blankSpace + \
                   "FUNCTION" + blankSpace + \
                   self.Type.E3ST[content] + semicolon

    def __decoded(self, presetstr,coordinateSystem):
        self.command = "PRESET"
        "去掉末尾分号"
        presetstr = presetstr.split(semicolon)[0]
        seg = presetstr.split(blankSpace)
        if seg[1] == self.Type.B1ST[0]:
            self.type = self.Type.B1ST
        if seg[1] == self.Type.B2ST[0]:
            self.type = self.Type.B2ST
        if seg[1] == self.Type.B3ST[0]:
            self.type = self.Type.B3ST
        if seg[1] == self.Type.E1ST[0]:
            self.type = self.Type.E1ST
        if seg[1] == self.Type.E2ST[0]:
            self.type = self.Type.E2ST
        if seg[1] == self.Type.E3ST[0]:
            self.type = self.Type.E3ST
        self.coordinateSystem = coordinateSystem
        return self

    def getPresetStr(self):
        return self.__encoded()

    def getPresetObject(self, presetstr,coordinateSystem):
        return self.__decoded(presetstr,coordinateSystem)


###############################第十五章 控制输出命令##################################
class Graphics:
    "控制输出图形"
    # GRAPHICS PAUSE [duration];
    # GRAPHICS NOPAUSE;

    class Type(Enum):
        pause = "PAUSE "
        nopause = "NOPAUSE "

    def __init__(self, type="", duration=""):
        self.command = "GRAPHICS"
        self.type = type
        self.duration = duration

    def __encoded(self):
        if self.type == self.Type.pause:
            return self.command + blankSpace + \
                   self.type + blankSpace + \
                   self.duration + semicolon
        elif self.type == self.Type.nopause:
            return self.command + blankSpace + \
                   self.type + blankSpace + semicolon
        else:
            return "error type"

    def getGraphicsStr(self):
        return self.__encoded()


class Dump:
    "控制 DUMP 输出渠道设置"
    #DUMP { TYPE data_type, PREFIX prefix , SUFFIX suffix , FORMAT { ASCII, BINARY } } ;

    class Type(Enum):
        type = "TYPE"
        prefix = "PREFIX"
        suffix = "SUFFIX"
        format = "FORMAT"
        name = "NAME"

    class DataType(Enum):
        all = "ALL"
        contour = "CONTOUR"
        observe = "OBSERVE"
        phasespace = "PHASESPACE"
        range = "RANGE"
        table = "TABLE"
        vector = "VECTOR"

    class FormatType(Enum):
        ascii = "ASCII"
        binary = "BINARY"

    def __init__(self, type="", val=""):
        self.command = "DUMP"
        self.type = type
        self.val = val

    def __encoded(self):
        return self.command + blankSpace + \
                self.type + blankSpace + \
                self.val + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)
        self.type = strs[1]
        self.val = strs[2]
        return self

    def getDumpStr(self):
        return self.__encoded()

    def getDumpObject(self, str):
        return self.__decoded(str)


class Header:
    "显示模拟的相关文字信息"

    class Parameter(Enum):
        organization = "ORGANIZATION"
        author = "AUTHOR"
        device = "DEVICE"
        remarks = "REMARKS"

    def __init__(self, para="", val="NONE"):
        self.command = "HEADER"
        self.para = para
        self.val = val

    def __encoded(self):
        return self.command + blankSpace + \
               self.para + blankSpace + \
               doubleQuotation + self.val + doubleQuotation + semicolon

    def __decoded(self, str):
        strs = re.split(" |;", str)
        self.val = strs[2][1: len(strs[2])-1]
        return self

    def getNotes(self):
        return exclamatory + self.command

    def getHeaderStr(self):
        return self.__encoded()

    def getHeaderObject(self, str):
        return self.__decoded(str)


#############################第十七章 时间命令##################################
class ObserveField:

    def __init__(self, fieldType="", object="",name2 = ""):
        self.command = "OBSERVE FIELD"
        self.fieldType = fieldType
        self.object = object
        self.name2 = name2

    def __encoded(self):
        if self.name2 == '':
            return self.command + blankSpace + \
                    self.fieldType + blankSpace + \
                    self.object + semicolon
        else :
            return self.command + blankSpace + \
                    self.fieldType + blankSpace + \
                    self.object + blankSpace + 'suffix' + blankSpace + \
                    str(self.name2) + semicolon

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        self.fieldType = strs[2]
        self.object = strs[3]
        if 'suffix' in str:
            self.name2 = strs[5].replace('OBS$','')
        else:
            self.name2 = ''

    def getObserveFieldStr(self):
        return self.__encoded()

    def getObserveFieldObject(self, str):
        self.__decoded(str)
        return self


class ObserveFieldIntegral:

    class FieldType(Enum):
        edl = "E.DL"
        jda = "J.DA"
        hdl = "H.DL"

    def __init__(self, fieldType="", object="",name2 = ''):
        self.command = "OBSERVE FIELD_INTEGRAL"
        self.fieldType = fieldType
        self.object = object
        self.name2 = name2

    def __encoded(self):
        if self.name2 == '':
            return self.command + blankSpace + \
               self.fieldType + blankSpace + \
               self.object + semicolon
        else:
            return self.command + blankSpace + \
                    self.fieldType + blankSpace + \
                    self.object + blankSpace + 'suffix' + blankSpace + \
                    str(self.name2) + semicolon

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        self.fieldType = strs[2]
        self.object = strs[3]
        if 'suffix' in str:
            self.name2 = strs[5].replace('OBS$','')
        else:
            self.name2 = ''

    def getObserveFieldIntegralStr(self):
        return self.__encoded()

    def getObserveFieldIntegralObject(self, str):
        self.__decoded(str)
        return self


class ObserveFieldPower:
    class FieldType(Enum):
        sda = "S.DA"

    def __init__(self, fieldType="S.DA", object="",name2 = ''):
        self.command = "OBSERVE FIELD_POWER"
        self.fieldType = fieldType
        self.object = object
        self.name2 = name2

    def __encoded(self):
        if self.name2 == '':
            return self.command + blankSpace + \
               self.fieldType + blankSpace + \
               self.object + semicolon
        else:
            return self.command + blankSpace + \
                    self.fieldType + blankSpace + \
                    self.object + blankSpace + 'suffix' + blankSpace + \
                    str(self.name2) + semicolon

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        self.fieldType = strs[2]
        self.object = strs[3]
        if 'suffix' in str:
            self.name2 = strs[5].replace('OBS$','')
        else:
            self.name2 = ''

    def getObserveFieldPowerStr(self):
        return self.__encoded()

    def getObserveFieldPowerObject(self, str):
        self.__decoded(str)
        return self


class ObserveFieldEnergy:
    class FieldType(Enum):
        em = "EM"
        electric = "ELECTRIC"
        magnetic = "MAGNETIC"

    def __init__(self, fieldType="", object="",name2 = ''):
        self.command = "OBSERVE FIELD_ENERGY"
        self.fieldType = fieldType
        self.object = object
        self.name2 = name2

    def __encoded(self):
        if self.name2 == '':
            return self.command + blankSpace + \
               self.fieldType + blankSpace + \
               self.object + semicolon
        else:
            return self.command + blankSpace + \
                    self.fieldType + blankSpace + \
                    self.object + blankSpace + 'suffix' + blankSpace + \
                    str(self.name2) + semicolon

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        self.fieldType = strs[2]
        self.object = strs[3]
        if 'suffix' in str:
            self.name2 = strs[5].replace('OBS$','')
        else:
            self.name2 = ''

    def getObserveFieldEnergyStr(self):
        return self.__encoded()

    def getObserveFieldEnergyObject(self, str):
        self.__decoded(str)
        return self


class ObserveParticleStatistics:
    class FieldType(Enum):
        eps = "EMIT_EPS"
        charge= "CHARGE"
        energy = "ENERGY"
        vratio = "VRATIO"
    class Option(Enum):
        electron = "ELECTRON"
        ions="IONS"
        all="ALL"
    def __init__(self, fieldType="",option="phase1", object="",name2 = ''):
        self.command = "OBSERVE PARTICLE_STATISTICS"
        self.fieldType = fieldType
        self.object = object
        self.option = option
        self.name2 = name2

    def __encoded(self):
        if self.name2 == '':
            return self.command + blankSpace + \
               self.fieldType + blankSpace + \
               self.option+ blankSpace + self.object + semicolon
        else:
            return self.command + blankSpace + \
                    self.fieldType + blankSpace + \
                    self.option + blankSpace +self.object + blankSpace + 'suffix' + blankSpace + \
                    str(self.name2) + semicolon

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        self.fieldType = strs[2]
        self.option = strs[3]
        self.object = strs[4]
        if 'suffix' in str:
            self.name2 = strs[6].replace('OBS$','')
        else:
            self.name2 = ''

    def getObserveParticleStatisticsStr(self):
        return self.__encoded()

    def getObserveParticleStatisticsObject(self, str):
        self.__decoded(str)
        return self

class ObserveParticle:
    class classify(Enum):
        collected = "COLLECTED"
        emitted = "EMITTED"
        destroyed = "DESTROYED"
    class FieldType(Enum):
        charge = "CHARGE"
        current= "CURRENT"
        energy = "ENERGY"
        power = "POWER"
        voltage = "VOLTAGE"
    class Option(Enum):
        electron = "ELECTRON"
        ions="IONS"
        all="ALL"
    def __init__(self, classify="",fieldType="",option="phase1", object="",name2 = ''):
        self.command = "OBSERVE "+classify
        self.fieldType = fieldType
        self.object = object
        self.option = option
        self.name2 = name2

    def __encoded(self):
        if self.name2 == '':
            return self.command + blankSpace + \
               self.fieldType + blankSpace + \
               self.option +blankSpace + self.object + semicolon
        else:
            return self.command + blankSpace + \
                    self.fieldType + blankSpace + \
                    self.option +blankSpace + self.object + blankSpace + 'suffix' + blankSpace + \
                    str(self.name2) + semicolon

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        self.fieldType = strs[2]
        self.option = strs[3]
        self.object = strs[4]
        if 'suffix' in str:
            self.name2 = strs[6].replace('OBS$','')
        else:
            self.name2 = ''

    def getObserveParticleStr(self):
        return self.__encoded()

    def getObserveParticleObject(self, str):
        self.__decoded(str)
        return self

class ObserveOptionFFT:

    class FFTType(Enum):
        magnitude = "MAGNITUDE"
        complex = "COMPLEX"

    def __init__(self,fftType="",isFreq=False,freqFrom="",freqTo=""):
        self.fftType = fftType
        self.isFreq=isFreq
        self.freqFrom=freqFrom
        self.freqTo=freqTo

    def __encoded(self):
        '''
        根据是否是变量来判断是否添加GHZ
        '''
        if not self.isFreq:
            returnStr = " FFT" + blankSpace + self.fftType +semicolon
        else:
            returnStr = " FFT" + blankSpace + self.fftType + blankSpace + "WINDOW FREQUENCY "
            if isNumber(self.freqFrom):
                returnStr = returnStr + self.freqFrom + "GHZ"+blankSpace
            else:
                returnStr = returnStr + self.freqFrom +blankSpace
            if isNumber(self.freqTo):
                returnStr = returnStr + self.freqTo +"GHZ" + semicolon
            else:
                returnStr = returnStr + self.freqTo + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        #新加的PARTICLE_STATISTICS、COLLECTED、EMITTED、DESTROYED要多一个参数，导致解析依次往后挪1
        if "PARTICLE_STATISTICS" in str or "COLLECTED" in str or "EMITTED" in str or "DESTROYED" in str:
            if 'suffix' in str:
                self.fftType = strs[8]
                if len(strs)>=11:
                    self.isFreq=True
                else:
                    self.isFreq=False

                if self.isFreq:
                    if "GHZ" in strs[11]:
                        self.freqFrom = strs[11][0: len(strs[11]) - 3]
                    else:
                        self.freqFrom = strs[11]
                    if "GHZ" in strs[12]:
                        self.freqTo = strs[12][0: len(strs[12]) - 3]
                    else:
                        self.freqTo = str[12]
            else:
                self.fftType = strs[6]
                if len(strs)>=9:
                    self.isFreq=True
                else:
                    self.isFreq=False

                if self.isFreq:
                    if "GHZ" in strs[9]:
                        self.freqFrom = strs[9][0: len(strs[9]) - 3]
                    else:
                        self.freqFrom = strs[9]
                    if "GHZ" in strs[10]:
                        self.freqTo = strs[10][0: len(strs[10]) - 3]
                    else:
                        self.freqTo = strs[10]
        else:
            if 'suffix' in str:
                self.fftType = strs[7]
                if len(strs)>=10:
                    self.isFreq=True
                else:
                    self.isFreq=False

                if self.isFreq:
                    if "GHZ" in strs[10]:
                        self.freqFrom = strs[10][0: len(strs[10]) - 3]
                    else:
                        self.freqFrom = strs[10]
                    if "GHZ" in strs[11]:
                        self.freqTo = strs[11][0: len(strs[11]) - 3]
                    else:
                        self.freqTo = str[11]
            else:
                self.fftType = strs[5]
                if len(strs)>=8:
                    self.isFreq=True
                else:
                    self.isFreq=False

                if self.isFreq:
                    if "GHZ" in strs[8]:
                        self.freqFrom = strs[8][0: len(strs[8]) - 3]
                    else:
                        self.freqFrom = strs[8]
                    if "GHZ" in strs[9]:
                        self.freqTo = strs[9][0: len(strs[9]) - 3]
                    else:
                        self.freqTo = strs[9]
    def getObserveOptionFFTStr(self):
        return self.__encoded()

    def getObserveOptionFFTObject(self, str):
        self.__decoded(str)
        return self


class ObserveOptionFilter:
    class FilterType(Enum):
        step = "STEP"
        loPass = "LO_PASS"

    def __init__(self,filterType="", timePara=""):
        self.filterType = filterType
        self.timePara = timePara

    def __encoded(self):
        if isNumber(self.timePara):
            returnStr = " FILTER" + blankSpace + self.filterType + blankSpace + \
                    self.timePara + "NANOSECOND" + semicolon
        else:
            returnStr = " FILTER" + blankSpace + self.filterType + blankSpace + \
                    self.timePara + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        #新加的PARTICLE_STATISTICS、COLLECTED、EMITTED、DESTROYED要多一个参数，导致解析依次往后挪1
        if "PARTICLE_STATISTICS" in str or "COLLECTED" in str or "EMITTED" in str or "DESTROYED" in str:
            if 'suffix' in str:
                self.filterType = strs[8]
                if "NANOSECOND" in strs[9]:
                    self.timePara = strs[9][0: len(strs[9])-10]
                else:
                    self.timePara = strs[9]
            else:
                self.filterType = strs[6]
                if "NANOSECOND" in strs[7]:
                    self.timePara = strs[7][0: len(strs[7])-10]
                else:
                    self.timePara = strs[7]
        else:
            if 'suffix' in str:
                self.filterType = strs[7]
                if "NANOSECOND" in strs[8]:
                    self.timePara = strs[8][0: len(strs[8])-10]
                else:
                    self.timePara = strs[8]
            else:
                self.filterType = strs[5]
                if "NANOSECOND" in strs[6]:
                    self.timePara = strs[6][0: len(strs[6])-10]
                else:
                    self.timePara = strs[6]

    def getObserveOptionFilterStr(self):
        return self.__encoded()

    def getObserveOptionFilterObject(self, str):
        self.__decoded(str)
        return self


class ObserveOptionTime:
    def __init__(self, timeFrom="", timeTo=""):
        self.timeFrom = timeFrom
        self.timeTo = timeTo

    def __encoded(self):
        returnStr = " WINDOW TIME " 
        if isNumber(self.timeFrom):
            returnStr = returnStr + self.timeFrom + "NANOSECOND" +blankSpace
        else:
            returnStr = returnStr +self.timeFrom +blankSpace
        if isNumber(self.timeTo):
            returnStr = returnStr + self.timeTo + "NANOSECOND" + semicolon
        else:
            returnStr = returnStr + self.timeTo +semicolon
        # returnStr = " WINDOW TIME " + self.timeFrom + "NANOSECOND" + blankSpace + self.timeTo + "NANOSECOND" + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        #新加的PARTICLE_STATISTICS、COLLECTED、EMITTED、DESTROYED要多一个参数，导致解析依次往后挪1
        if "PARTICLE_STATISTICS" in str or "COLLECTED" in str or "EMITTED" in str or "DESTROYED" in str:
            if 'suffix' in str:
                if "NANOSECOND" in strs[9]:
                    self.timeFrom = strs[9][0: len(strs[9])-10]
                else:
                    self.timeFrom = strs[9]
                if "NANOSECOND" in strs[10]:
                    self.timeTo = strs[10][0: len(strs[10])-10]
                else:
                    self.timeTo = strs[10]
            else:
                if "NANOSECOND" in strs[7]:
                    self.timeFrom = strs[7][0: len(strs[7])-10]
                else:
                    self.timeFrom = strs[7]
                if "NANOSECOND" in strs[8]:
                    self.timeTo = strs[8][0: len(strs[8])-10]
                else:
                    self.timeTo = strs[8]
        else:
            if 'suffix' in str:
                if "NANOSECOND" in strs[8]:
                    self.timeFrom = strs[8][0: len(strs[8])-10]
                else:
                    self.timeFrom = strs[8]
                if "NANOSECOND" in strs[9]:
                    self.timeTo = strs[9][0: len(strs[9])-10]
                else:
                    self.timeTo = strs[9]
            else:
                if "NANOSECOND" in strs[6]:
                    self.timeFrom = strs[6][0: len(strs[6])-10]
                else:
                    self.timeFrom = strs[6]
                if "NANOSECOND" in strs[7]:
                    self.timeTo = strs[7][0: len(strs[7])-10]
                else:
                    self.timeTo = strs[7]

    def getObserveOptionTimeStr(self):
        return self.__encoded()

    def getObserveOptionTimeObject(self, str):
        self.__decoded(str)
        return self

class ObserveOptionInterval:
    def __init__(self, interval=""):
        self.interval = interval

    def __encoded(self):
        returnStr = " interval "+self.interval + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;|,", str)
        #新加的PARTICLE_STATISTICS、COLLECTED、EMITTED、DESTROYED要多一个参数，导致解析依次往后挪1
        if "PARTICLE_STATISTICS" in str or "COLLECTED" in str or "EMITTED" in str or "DESTROYED" in str:
            if 'suffix' in str:
                self.interval = strs[8]
            else:
                self.interval = strs[6]
        else:
            if 'suffix' in str:
                self.interval = strs[7]
            else:
                self.interval = strs[5]

    def getObserveOptionIntervalStr(self):
        return self.__encoded()

    def getObserveOptionIntervalObject(self, str):
        self.__decoded(str)
        return self

class ObserveOptionFreq:
    def __init__(self,freqFrom="",freqTo=""):
        self.freqFrom=freqFrom
        self.freqTo=freqTo

    def __encoded(self):
        returnStr=" WINDOW FREQUENCY "
        if isNumber(self.freqFrom):
            returnStr = returnStr + self.freqFrom + "GHZ"+blankSpace
        else:
            returnStr = returnStr + self.freqFrom +blankSpace
        if isNumber(self.freqTo):
            returnStr = returnStr + self.freqTo +"GHZ" + semicolon
        else:
            returnStr = returnStr + self.freqTo + semicolon
        return returnStr
        
    def __decoded(self,str):
        strs = re.split(" |;|,", str)
        #新加的PARTICLE_STATISTICS、COLLECTED、EMITTED、DESTROYED要多一个参数，导致解析依次往后挪1
        if "PARTICLE_STATISTICS" in str or "COLLECTED" in str or "EMITTED" in str or "DESTROYED" in str:
            if 'suffix' in str:
                if "GHZ" in strs[9]:
                    self.freqFrom = strs[9][0: len(strs[9])-3]
                else:
                    self.freqFrom = strs[9]
                if "GHZ" in strs[10]:
                    self.freqTo = strs[10][0: len(strs[10])-3]
                else:
                    self.freqTo = strs[10]
            else:
                if "GHZ" in strs[7]:
                    self.freqFrom = strs[7][0: len(strs[7])-3]
                else:
                    self.freqFrom = strs[7]
                if "GHZ" in strs[8]:
                    self.freqTo = strs[8][0: len(strs[8])-3]
                else:
                    self.freqTo = strs[8]
        else:
            if 'suffix' in str:
                if "GHZ" in strs[8]:
                    self.freqFrom = strs[8][0: len(strs[8])-3]
                else:
                    self.freqFrom = strs[8]
                if "GHZ" in strs[9]:
                    self.freqTo = strs[9][0: len(strs[9])-3]
                else:
                    self.freqTo = strs[9]
            else:
                if "GHZ" in strs[6]:
                    self.freqFrom = strs[6][0: len(strs[6])-3]
                else:
                    self.freqFrom = strs[6]
                if "GHZ" in strs[7]:
                    self.freqTo = strs[7][0: len(strs[7])-3]
                else:
                    self.freqTo = strs[7]
    def getObserveOptionFreqStr(self):
        return self.__encoded()
    def getObserveOptionFreqObject(self,str):
        self.__decoded(str)
        return self

#############################第十九章 二维和三维命令############################
class Display:
    "显示模拟的几何信息"

    def __init__(self, areaName=""):
        self.command = "DISPLAY"
        self.areaName = areaName

    def __encoded(self):
        return self.command + blankSpace + \
                self.areaName + semicolon

    def getDisplayStr(self):
        return self.__encoded()


class Contour:
    "等位图观测"
    # 目前甲方实现的可选参数有限

    class Timer(Enum):
        default = "DefTimer"
        start = "TSYS$FIRST"
        last = "TSYS$LAST"

    def __init__(self, field="", areaName="", timerName="", isShade=False):
        self.command = "CONTOUR"
        self.field = field
        self.areaName = areaName
        self.timerName = timerName
        self.isShade = isShade

    def __encoded(self):

        returnStr = self.command + blankSpace + \
               "FIELD" + blankSpace + self.field + blankSpace + \
               self.areaName + blankSpace + \
               self.timerName

        if self.isShade:
            returnStr = returnStr + blankSpace + "SHADE"

        returnStr = returnStr + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;", str)

        self.field = strs[2]
        self.areaName = strs[3]
        self.timerName = strs[4]
        if strs[5] == "SHADE":
            self.isShade = True
        else:
            self.isShade = False

    def getContourStr(self):
        return self.__encoded()

    def getContourObject(self, str):
        self.__decoded(str)

        return self


class Vector:
    "矢量图观测"
    class Timer(Enum):
        default = "DefTimer"
        start = "TSYS$FIRST"
        last = "TSYS$LAST"

    def __init__(self, field1="", field2="", areaName="", timerName="", isNumber=False, number1="20", number2="20"):
        self.command = "VECTOR"
        self.field1 = field1
        self.field2 = field2
        self.areaName = areaName
        self.timerName = timerName
        self.isNumber = isNumber
        self.number1 = number1
        self.number2 = number2

    def __encoded(self):

        returnStr = self.command + blankSpace + \
               "FIELD" + blankSpace + self.field1 + comma + self.field2 + blankSpace + \
               self.areaName + blankSpace + \
               self.timerName

        if self.isNumber:
            returnStr = returnStr + blankSpace + "NUMBER" + blankSpace + self.number1 + blankSpace + self.number2

        returnStr = returnStr + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;|,", str)

        self.field1 = strs[2]
        self.field2 = strs[3]
        self.areaName = strs[4]
        self.timerName = strs[5]
        if strs[6] == "NUMBER":
            self.isNumber = True
            self.number1 = strs[7]
            self.number2 = strs[8]
        else:
            self.isNumber = False
            self.number1 = "20"
            self.number2 = "20"


    def getVectorStr(self):
        return self.__encoded()

    def getVectorObject(self, str):
        self.__decoded(str)
        return self


class Phasespace:
    "粒子的相位空间"

    class Timer(Enum):
        default = "DefTimer"
        start = "TSYS$FIRST"
        last = "TSYS$LAST"

    class Direction(Enum):
        x1 = "X1"
        x2 = "X2"
        x3 = "X3"

    class SpeciesType(Enum):
        electron = "ELECTRON"
        proton = "PROTON"
        all = "ALL"

    def __init__(self, horizontalAxis="", verticalAxis="",
                 timerName="",
                 species="",
                 isThickness=False, direction="X1", thickness1="0", thickness2="0",
                 isSuffix=False, suffix="phase1"):
        self.command = "PHASESPACE"
        self.horizontalAxis = horizontalAxis
        self.verticalAxis = verticalAxis
        self.timerName = timerName
        self.species = species
        self.isThickness = isThickness
        self.direction = direction
        self.thickness1 = thickness1
        self.thickness2 = thickness2
        self.isSuffix = isSuffix
        self.suffix = suffix

    def __encoded(self):
        returnStr = self.command + blankSpace + \
                    "AXES" + blankSpace + self.horizontalAxis + comma + self.verticalAxis + blankSpace + \
                    self.timerName

        if self.species != self.SpeciesType.all:
            returnStr = returnStr + blankSpace + "SPECIES" + blankSpace + self.species

        if self.isThickness:
            returnStr = returnStr + blankSpace + "WINDOW" + blankSpace + self.direction + blankSpace + \
                        self.thickness1 + blankSpace + self.thickness2

        if self.isSuffix:
            returnStr = returnStr + blankSpace + "SUFFIX" + blankSpace + self.suffix

        returnStr = returnStr + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;|,", str)

        self.horizontalAxis = strs[2]
        self.verticalAxis = strs[3]
        self.timerName = strs[4]
        self.species = Phasespace.SpeciesType.all
        self.isThickness = False
        self.isSuffix = False

        for i in range(5, len(strs)):
            # 如果指定观测例子
            if strs[i] == "SPECIES":
                self.species = strs[i+1]

            # 如果指定厚度
            if strs[i] == "WINDOW":
                self.isThickness = True
                self.direction = strs[i+1]
                self.thickness1 = strs[i+2]
                self.thickness2 = strs[i+3]

            # 如果指定后缀
            if strs[i] == "SUFFIX":
                self.isSuffix = True
                self.suffix = strs[i+1]


    def getPhasespaceStr(self):
        return self.__encoded()

    def getPhasespaceObject(self, str):
        self.__decoded(str)

        return self


class Range:
    "空间观测"
    class Timer(Enum):
        default = "DefTimer"
        start = "TSYS$FIRST"
        last = "TSYS$LAST"

    def __init__(self, field="", lineName="", timerName="", isFFT=False, isMagnitude=False, isComplex=False):
        self.command = "RANGE"
        self.field = field
        self.lineName = lineName
        self.timerName = timerName
        self.isFFT = isFFT
        self.isMagnitude = isMagnitude
        self.isComplex = isComplex

    def __encoded(self):

        returnStr = self.command + blankSpace + \
               "FIELD" + blankSpace + self.field + blankSpace + \
               self.lineName + blankSpace + \
               self.timerName

        if self.isFFT:
            if self.isMagnitude:
                returnStr = returnStr + blankSpace + "FFT" + blankSpace + "MAGNITUDE"
            if self.isComplex:
                returnStr = returnStr + blankSpace + "FFT" + blankSpace + "COMPLEX"

        returnStr = returnStr + semicolon

        return returnStr

    def __decoded(self, str):
        strs = re.split(" |;|,", str)

        self.field = strs[2]
        self.lineName = strs[3]
        self.timerName = strs[4]
        if strs[5] == "FFT":
            self.isFFT = True
            if strs[6] == "MAGNITUDE":
                self.isMagnitude = True
                self.isComplex = False
            if strs[6] == "COMPLEX":
                self.isMagnitude = False
                self.isComplex = True
        else:
            self.isFFT = False


    def getRangeStr(self):
        return self.__encoded()

    def getRangeObject(self, str):
        self.__decoded(str)

        return self




def sayz(msg):
    FreeCAD.Console.PrintMessage(msg+"\n")






