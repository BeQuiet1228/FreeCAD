# -*- coding: UTF-8 -*-

from GetParameterByCommand import *
import File.FileCommand.TextUI.FileTextView
import Modeling.Common.Tools.ModelingByM3dFile as ModelingByM3dFile
import Modeling.Common.Tools.ObjectsTools as ObjectsTools
import Modeling.Common.Tools.UnitTools as UnitTools
import Modeling.Common.Tools.CoordinateSystemTools as CoordinateSystemTools
from enum import Enum
import FreeCAD
import json
import _winreg
import numpy as np
import File.FileCommand.M3DFile.M3DFileUtil
import re
"""
解析m3d文件
"""


class ParseM3DFile:

    class __KeywordInCommand(Enum):
        """
        不同命令组类型对应的关键字
        """
        FUNCTION = "FUNCTION"
        START = "START"
        STOP = "STOP"
        SYSTEM = "SYSTEM"
        POINT = "POINT"
        LINE = "LINE"
        AREA = "AREA"
        VOLUME = "VOLUME"
        DURATION = "DURATION"
        TIMER = "TIMER"
        MARK = "MARK"
        AUTOGRID = "AUTOGRID"
        SYMMETRY = "SYMMETRY"
        PORT = "PORT"
        CONDUCTANCE = "CONDUCTANCE"
        DIELECTRIC = "DIELECTRIC"
        CONDUCTOR = "CONDUCTOR"
        VOID = "VOID"
        MATERIAL = "MATERIAL"
        EMISSION = "EMISSION"
        EMIT = "EMIT"
        MAXWELL = "MAXWELL"
        MODE = "MODE"
        TIME_STEP = "TIME_STEP"
        CONTINUITY = "CONTINUITY"
        PRESET = "PRESET"
        GRAPHICS = "GRAPHICS"
        DUMP = "DUMP"
        HEADER = "HEADER"
        OBSERVE = "OBSERVE"
        DISPLAY = "DISPLAY"
        CONTOUR = "CONTOUR"
        VECTOR = "VECTOR"
        PHASESPACE = "PHASESPACE"
        RANGE = "RANGE"
        INDUCTOR = "INDUCTOR"
        FOIL = "FOIL"
        FREESPACE = "FREESPACE"
        DO = "do"
        POPULATE = "POPULATE"
        GASGAS = "GASGAS"
        # EMISSION = "EMISSION"
        SPECIES="SPECIES"

    class __StrInit(Enum):
        """
        不同命令组类型对应的字符串
        """
        exclamatory = "!"
        strStart = "! ==============================================================================!"
        strHeaderSystem = ""
        strParameter = "! PARAMETER"
        strDefineObjects = "! DEFINE OBJECTS"
        strPanelObjects = "! PANEL OBJECTS"
        strGenerateGrid = "! GENERATE GRID/MESH"
        strCommonPresets = "! COMMON PRESETS"
        strPropertiesAndProcesses = "! PROPERTIES AND PROCESSES"
        strSimulationSettings = "! SIMULATION SETTINGS"
        strAllPlots = "! ALL PLOTS"
        strDumpOptions = "! DUMP OPTIONS"
        strRunOptions = "! RUN OPTIONS"
        strRun = "! RUN"

    class __CoordinateSystem(Enum):
        rectangularSys = "R"
        polarSys = "P"
        cylindricalSys = "C"

    class __LineType(Enum):
        conformal = "CONFORMAL"
        oblique = "OBLIQUE"

    class __AreaType(Enum):
        conformal = "CONFORMAL"
        rectangular = "RECTANGULAR"
        polygonal = "POLYGONAL"

    class __VolumeType(Enum):
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
        extruded = "EXTRUDED"
        rotate = "ROTATE"
        helical = "HELICAL"
        toroidalSection = "TOROIDAL_SECTION"

    def __init__(self, path=r"C:\Users\\WuZiNing\Desktop\2222.m3d"):

        # 定义不同命令组类型对应的字符串列表
        self.__headerSystemStrList = [[],[]]
        # 我认为下面这个变量便是我所查找的点
        self. __parameterStrList = []
        self.__objectStrList = [[]]
        self.__panelObjectStrList = [[]]
        self.__meshStrList = []
        self.__commonPresetsStrList = []
        self.__propertiesAndProcesses = []
        self.__emission = []
        self.__attribute = []
        self.__commonBoundary = []
        self.__otherModelsStrList = []
        self.__simulationSettingsStrList = []
        self.__allPlotsStrList = []
        self.__dumpOptionsStrList = []
        self.__runOptionsStrList = []
        self.__runStrList = []

        # 定义有关文件的属性
        self.__fileStrList = []
        self.__CommandsList = []
        self.path = path

        # 定义当前坐标系
        self.coordinateSystem = ""

    def __isCorrectFile(self):
        import os.path
        if os.path.splitext(self.path)[1] ==".m3d" or os.path.splitext(self.path)[1] ==".obj":
            return True
        else:
            return False

    def setfileStrList(self,fileStrList):
        "为属性赋值"
        self.__fileStrList = fileStrList

    def getFileContent(self):
        if self.__isCorrectFile() == True:
            f = open(self.path, "r")
            self.__fileStrList = f.readlines()
            f.close()
            # 去掉最后的换行符
            for i in range(len(self.__fileStrList)):
                self.__fileStrList[i] =self.__fileStrList[i][:-1]

            return self.__fileStrList
        else:
            return "该文件不是.m3d或.obj文件"

    def sortCommands(self):
        """
        将具体的命令组分拣到不同命令组类型对应的List中

        :param fileStrList: m3d中所有line
        :return: void
        """

        listType = ""
        index = 0
        # flag2标志是否是循环体，如果是，为0，两个!!放在一起
        flag2 = True
        for line in self.__fileStrList:
            sayz("line:")
            sayz(line)
            flag = True
            # index表示当前遍历的的line在__fileStrList中的指数
            index = index + 1
            # 每个__StrInit.strStart后面是一大类的名称

            if line == self.__StrInit.strStart:
                flag = False
                listType = self.__fileStrList[index]

            if flag:
                if listType == self.__StrInit.strHeaderSystem:
                    # 调用函数将line分为Header和System两类
                    self.__sortHeaderSystemStrList(line)
                    continue
                elif listType == self.__StrInit.strParameter:
                    self.__parameterStrList.append(line)
                    continue
                elif listType == self.__StrInit.strDefineObjects:
                    # 调用函数将line每个体分为一类
                    flag2 = self.__sortObjectStrList(line,flag2)
                    continue
                elif listType == self.__StrInit.strPanelObjects:
                    # 调用函数将line每个体分为一类
                    self.__sortPanelObjectStrList(line)
                    continue
                elif listType == self.__StrInit.strGenerateGrid:
                    self.__meshStrList.append(line)
                    continue
                elif listType == self.__StrInit.strCommonPresets:
                    self.__commonPresetsStrList.append(line)
                    continue
                elif listType == self.__StrInit.strPropertiesAndProcesses:
                    self.__sortPropertiesAndProcesses(line)
                    continue
                elif listType == self.__StrInit.strSimulationSettings:
                    self.__simulationSettingsStrList.append(line)
                    continue
                elif listType == self.__StrInit.strAllPlots:
                    self.__sortAllPlotsStrList(line)
                    continue
                elif listType == self.__StrInit.strDumpOptions:
                    self.__dumpOptionsStrList.append(line)
                    continue
                elif listType == self.__StrInit.strRunOptions:
                    self.__runOptionsStrList.append(line)
                    continue
                elif listType == self.__StrInit.strRun:
                    self.__runStrList.append(line)
                    continue

        self.__furtherSortPropertiesAndProcesses()

    def __sortHeaderSystemStrList(self, line):

        """
        将具体的命令组分拣到不同命令组类型对应的List中
        __headerSystemStrList[0]：存放header命令及注释
        __headerSystemStrList[1]：存放system命令及注释
        :return: void
        """
        if self.__KeywordInCommand.HEADER in line:
            self.__headerSystemStrList[0].append(line)
        elif self.__KeywordInCommand.SYSTEM in line:
            self.__headerSystemStrList[1].append(line)

    def __sortObjectStrList(self, line,flag):

        """
        将具体的命令组分拣到不同命令组类型对应的List中
        一个体的命令及注释放在一个一维list中
        :return: void
        """

        # 如果是以"!!"开头，就增加list一维维度
        if line.startswith("!!"):
            if flag:
                self.__objectStrList.append([])
                # flag标志是循环体，为False，两个!!放在一起
            flag = True
        dim = np.array(self.__objectStrList).shape[0] - 1
        if line.startswith("do"):
            flag = False
        self.__objectStrList[dim].append(line)
        return flag

    def __sortPanelObjectStrList(self, line):

        """
        将具体的命令组分拣到不同命令组类型对应的List中
        一个体的命令及注释放在一个一维list中
        :return: void
        """

        # 如果是以"!!"开头，就增加list一维维度
        if line.startswith("!!"):
            self.__panelObjectStrList.append([])
        dim = np.array(self.__panelObjectStrList).shape[0] - 1
        self.__panelObjectStrList[dim].append(line)

    def __sortAllPlotsStrList(self, line):
        """
        将allport中的字符串，按面板进行划分
        一个面板对应一个数组
        :return: void
        """

        # 去除"allport字符串堆的标志行
        if line == self.__StrInit.strAllPlots:
            return

        # 同一个面板的放入一个list中，再总体放入__allPlotsStrList中
        if line == "":
            self.__allPlotsStrList.append([])
        else:
            self.__allPlotsStrList[len(self.__allPlotsStrList)-1].append(line)

    def __sortPropertiesAndProcesses(self, line):
        """将该分类下的字符串按空行分，并放在不同的列表里"""
        # FreeCAD.Console.PrintError(str(line)+'\n\n\n')
        # 去除字符串堆的标志行
        if line == self.__StrInit.strPropertiesAndProcesses:
            return
        # 同一个面板的字符串行放在一起
        if line == "":
            # 去除上一个组合起的字符串最后的换行符
            size = len(self.__propertiesAndProcesses)
            if size > 0:
                lastStrLen = len(self.__propertiesAndProcesses[size - 1])
                self.__propertiesAndProcesses[size - 1] = self.__propertiesAndProcesses[size - 1][0:lastStrLen-1]

            self.__propertiesAndProcesses.append("")
        else:
            # 同一个面板的字符串行放在一起，并用\n连接
            size = len(self.__propertiesAndProcesses)
            self.__propertiesAndProcesses[size - 1] = self.__propertiesAndProcesses[size - 1] + line + "\n"

    def __furtherSortPropertiesAndProcesses(self):
        """将__propertiesAndProcesses中的字符串细分"""

        for str in self.__propertiesAndProcesses:
            FreeCAD.Console.PrintError("\n\n__propertiesAndProcesses中的字符串:   " + str)
            # 发射面板
            if self.__KeywordInCommand.EMISSION in str:
                self.__emission.append(str)
            # 将Populate等依然加入发射部分，因为在概念上同属于发射部分
            if self.__KeywordInCommand.POPULATE in str:
                self.__emission.append(str)
            if self.__KeywordInCommand.GASGAS in str:
                self.__emission.append(str)
            # 常用边界
            if self.__KeywordInCommand.PORT in str or \
                            self.__KeywordInCommand.FREESPACE in str or \
                            self.__KeywordInCommand.SYMMETRY in str:
                self.__commonBoundary.append(str)

            # 自定义属性
            if self.__KeywordInCommand.VOID in str or \
                    self.__KeywordInCommand.CONDUCTOR in str or \
                    self.__KeywordInCommand.CONDUCTANCE in str or \
                    self.__KeywordInCommand.DIELECTRIC in str:
                self.__attribute.append(str)

            # 激励电源面板和其他模型
            if self.__KeywordInCommand.FOIL in str or \
                    self.__KeywordInCommand.INDUCTOR in str:
                self.__otherModelsStrList.append(str)

    def getCoordinateSystem(self):
        """获取坐标系"""
        for line in self.__headerSystemStrList[1]:
            if line.startswith(self.__KeywordInCommand.SYSTEM):
                self.coordinateSystem = getSystem(line)
                if self.coordinateSystem == self.__CoordinateSystem.rectangularSys:
                    return "Rectangular"
                elif self.coordinateSystem == self.__CoordinateSystem.polarSys:
                    return "Polar"
                elif self.coordinateSystem == self.__CoordinateSystem.cylindricalSys:
                    return "Cylindrical"

    ########################## 以下是根据m3d文件获取全局变量 ##########################

    def getGlobalVariableList(self):
        """
            :param: parameterStrList 所有全局变量相关命令
            :return: globalVariableList 全局变量参数列表
        """
        globalVariableList = []
        # 去掉最后三行参数和换行
        # for line in self.__parameterStrList[:-6]:
        for line in self.__parameterStrList: 
            result = getParameter(line)
            # FreeCAD.Console.PrintMessage("\nParameter:\n")
            # FreeCAD.Console.PrintMessage(result)
            if result is not None:
                globalVariableList.append(result)
        return globalVariableList

    ########################## 以下是根据m3d文件获取几何建参数 ##########################

    def __getObjectType(self, bigType, smallType):
        """
        传回几何体的类型
        :param: bigType 几何体的大类：LINE，AREA，VOLUME
        :param: smallType，几何体的小类
        :return: ObjectType ：ObjectsTools中定义的objectType类型
        """
        objectType = ""

        if bigType == "LINE":
            if smallType == self.__LineType.conformal:
                objectType = ObjectsTools.ObjectType.Line_Conformal
            elif smallType == self.__LineType.oblique:
                objectType = ObjectsTools.ObjectType.Line_Oblique
        elif bigType == "AREA":
            if smallType == self.__AreaType.conformal:
                objectType = ObjectsTools.ObjectType.Area_Conformal
            elif smallType == self.__AreaType.polygonal:
                objectType = ObjectsTools.ObjectType.Area_Polygonal
            elif smallType == self.__AreaType.rectangular:
                objectType = ObjectsTools.ObjectType.Area_Rectangular
        elif bigType == "VOLUME":
            if smallType == self.__VolumeType.annular:
                objectType = ObjectsTools.ObjectType.Vol_Annular
            elif smallType == self.__VolumeType.annularSection:
                objectType = ObjectsTools.ObjectType.Vol_Annular_Section
            elif smallType == self.__VolumeType.cone:
                objectType = ObjectsTools.ObjectType.Vol_SpecialCone
            elif smallType == self.__VolumeType.conformal:
                objectType = ObjectsTools.ObjectType.Vol_Conformal
            elif smallType == self.__VolumeType.cylindrical:
                objectType = ObjectsTools.ObjectType.Vol_Cylinder
            elif smallType == self.__VolumeType.parallelepipedal:
                objectType = ObjectsTools.ObjectType.Vol_Parallelepipedal
            elif smallType == self.__VolumeType.spherical:
                objectType = ObjectsTools.ObjectType.Vol_Spherical
            elif smallType == self.__VolumeType.wedge:
                objectType = ObjectsTools.ObjectType.Vol_Wedge
            elif smallType == self.__VolumeType.tetrahedron:
                objectType = ObjectsTools.ObjectType.Vol_Tetrahedron
            elif smallType == self.__VolumeType.pyramid:
                objectType = ObjectsTools.ObjectType.Vol_Pyramid
            elif smallType == self.__VolumeType.rhombus:
                objectType = ObjectsTools.ObjectType.Vol_Rhombus
            elif smallType == self.__VolumeType.extruded:
                objectType = ObjectsTools.ObjectType.Vol_Extruded
            elif smallType == self.__VolumeType.rotate:
                objectType = ObjectsTools.ObjectType.Vol_Revolution
            elif smallType == self.__VolumeType.helical:
                objectType = ObjectsTools.ObjectType.Vol_Helical
            elif smallType == self.__VolumeType.toroidalSection:
                objectType = ObjectsTools.ObjectType.Vol_Toroidal_Section
            elif smallType==self.__VolumeType.functional:
                objectType = ObjectsTools.ObjectType.Vol_Function

        return objectType

    def __getMarkParameterList(self,objectName,parameterList):
        """
            :param: objectName Mark对应的几何体的名称
            :param: parameterList，参数列表
                    parameterList[0] objectName为要设置非均匀网格的几何体名称,
                    parameterList[1] 对应的坐标轴
                    parameterList[3] 对应坐标轴上的值
            :return: isX1、isX2、isX3为是否选择对应的坐标轴，boolean型, X1Size、X2Size,、X3Size为对应坐标轴上的值
            """
        isX1 = False
        isX2 = False
        isX3 = False
        X1Size = "DX1"
        X2Size = "DX2"
        X3Size = "DX3"
        # @lzg
        ismin1 = False
        ismid1 = False
        ismax1 = False
        ismin2 = False
        ismid2 = False
        ismax2 = False
        ismin3 = False
        ismid3 = False
        ismax3 = False
        for list in parameterList:
            if list[0] == objectName:
                if list[1] == "X1":
                    isX1 = True
                    X1Size = list[3]
                    ismin1 = list[4]
                    ismid1 = list[5]
                    ismax1 = list[6]
                elif list[1] == "X2":
                    isX2 = True
                    X2Size = list[3]
                    ismin2 = list[4]
                    ismid2 = list[5]
                    ismax2 = list[6]
                elif list[1] == "X3":
                    isX3 = True
                    X3Size = list[3]
                    ismin3 = list[4]
                    ismid3 = list[5]
                    ismax3 = list[6]

        markParameterList = [isX1, isX2, isX3, X1Size, X2Size, X3Size,
                            ismin1, ismid1, ismax1,
                            ismin2, ismid2, ismax2,
                            ismin3, ismid3, ismax3]
        return markParameterList

    def __getAttributeParameterList(self,objectName):
        """
        :param: objectName 对应的几何体的名称
        :return: [isConductor,isVoid] 是否为理想导体，是否为真空区域
        """
        # 找到objectName匹配的属性后，sign置为1，跳出循环
        sign = 0
        # 如果没有找到objectName对应的自定义属性，flag为0，否则为1
        flag = 0
        # 初始化Custom参数属性
        RelativeDielectricConstant = "NotDefine"
        ConductivitySIGMA = "NotDefine"
        ConductivitySIGMAValue= str(0.05)
        SetEPS = str(1.0)
        SetEPS2 = str(0.0)
        SetEPS3 = str(0.0)
        CS_EPS1 = str(1.0)
        CS_EPS2 = str(1.0)
        CS_EPS3 = str(1.0)

        # 遍历所有属性命令
        for commandStr in self.__attribute:
            if objectName in commandStr:
                attributeList = commandStr.split("\n")
                for line in attributeList:
                    attribute = getAttributeParameter(line)
                    if attribute is not None:
                        if objectName == attribute[1]:
                            sign = 1
                            if attribute[0] == "CONDUCTOR":
                                return ["Conductor"]
                            elif attribute[0] == "VOID":
                                return ["Vacuo"]
                            elif attribute[0] == "CONDUCTANCE":
                                # FreeCAD.Console.PrintError('\n已经进入设置conductance的语句\n')
                                flag = 1
                                ConductivitySIGMA = attribute[4]
                                # 此处额外保留原有的一个属性
                                # ConductivitySIGMAValue = '0'
                                if attribute[3] == 0:
                                    CS_EPS1 = attribute[2]
                                elif attribute[3] == 1:
                                    CS_EPS1 = attribute[2]
                                elif attribute[3] == 2:
                                    CS_EPS2 = attribute[2]
                                elif attribute[3] == 3:
                                    CS_EPS3 = attribute[2]

                            elif attribute[0] == "DIELECTRIC":
                                flag = 1
                                if attribute[3] == 0:
                                    SetEPS = attribute[2]
                                    RelativeDielectricConstant = "Isotropy"
                                elif attribute[3] == 1:
                                    SetEPS = attribute[2]
                                    RelativeDielectricConstant = "Anisotropy"
                                elif attribute[3] == 2:
                                    SetEPS2 = attribute[2]
                                    RelativeDielectricConstant = "Anisotropy"
                                else:
                                    SetEPS3 = attribute[2]
                                    RelativeDielectricConstant = "Anisotropy"
                if sign:
                    if flag:
                        return ["Custom", ConductivitySIGMA, ConductivitySIGMAValue, RelativeDielectricConstant, SetEPS, SetEPS2, SetEPS3,CS_EPS1, CS_EPS2, CS_EPS3]
                    else:
                        return ["NotDefine"]

        return ["NotDefine"]

    def __getPointParameterList(self,parameterList,pointNameList):
        """
        :param: parameterList 点参数列表
                parameterList[i]:[ponitName, coordinates]点名字和坐标点列表
        :param: pointNameList，点名字列表
        :return: pointParameterList[]：所有点的坐标点列表
        """
        # 新老版本兼容问题
        if parameterList==[]:
            return []

        i = 0
        pointParameterList = []
        for name in pointNameList:
            if name == parameterList[i][0]:
                pointParameterList.append(parameterList[i][1])

            i = i+1
        FreeCAD.Console.PrintMessage("zhaozhou111\n")
        return pointParameterList

    def __getVertexGeometryParameterList(self,type,parameterList):
        parameter = []
        if len(parameterList[1]) == 1:
            # 获取几何体中点名字列表
            pointNameList = parameterList[1][0][2:]
            # 获取所有点的坐标列表
            pointParameterList = self.__getPointParameterList(parameterList[0], pointNameList[0])
            # 获取网格数据，传入参数为几何体的名称和几何体的网格命令参数
            markParameterList = self.__getMarkParameterList(parameterList[1][0][0], parameterList[2])
            # 获取attribute参数列表
            attributeParameterList = self.__getAttributeParameterList(parameterList[1][0][0])
            # FreeCAD.Console.PrintError('\n'+str(attributeParameterList)+'\n')
            # 加入几何体名字
            parameter.append(parameterList[1][0][0])
            # @fubiao 这里列表得再加一个[]
            # 加入点的坐标列表
            FreeCAD.Console.PrintMessage("\n初始点的格式\n")
            FreeCAD.Console.PrintMessage(pointNameList)
            if  pointParameterList==[]:
                parameter.extend(pointNameList[0])
            else:
                parameter.extend(pointParameterList)
            # 加入attribute参数
            if type == "VOLUME":
                parameter.append(attributeParameterList)
            # 加入网格参数
            parameter.extend(markParameterList)
            # 得到几何体类型
            objectType = self.__getObjectType(type,parameterList[1][0][1])
            if objectType != "":
                return [objectType,parameter]

    def __getRadiusVolumeParameterList(self,type,parameterList,num):
        parameter = []
        if len(parameterList[1]) == 1:
            # 去掉前两个名字和类型参数
            plist = parameterList[1][0][2:]
            # 获取点名字列表
            pointNameList = plist[0][:num]
            # 最后一个参数
            radiusList = plist[0][num:]

            # 获取所有点的坐标列表
            pointParameterList = self.__getPointParameterList(parameterList[0], pointNameList)
            # 在这里比较点的信息的不同
            FreeCAD.Console.PrintMessage("\n初始点的信息：\n")
            FreeCAD.Console.PrintMessage(pointNameList)
            FreeCAD.Console.PrintMessage("\n处理之后点的信息：\n")
            FreeCAD.Console.PrintMessage(pointParameterList)

            # 获取网格数据，传入参数为几何体的名称和几何体的网格命令参数
            markParameterList = self.__getMarkParameterList(parameterList[1][0][0], parameterList[2])
            # 获取attribute参数列表
            attributeParameterList = self.__getAttributeParameterList(parameterList[1][0][0])
            # FreeCAD.Console.PrintError('\n一个半径的体的attribute列表:'+str(attributeParameterList)+'\n')
            # 加入几何体名字
            parameter.append(parameterList[1][0][0])
            # 加入点的坐标列表
            # 这里我尽量不进行太多修改，虽然会对后来的重建造成不便
            if pointParameterList==[]:
                parameter.extend(pointNameList)
            else:
                parameter.extend(pointParameterList)
            # 加入半径参数
            parameter.extend(radiusList)
            # 加入attribute参数
            if type == "VOLUME":
                parameter.append(attributeParameterList)
            # 加入网格参数
            parameter.extend(markParameterList)
            # 得到几何体类型
            objectType = self.__getObjectType(type,parameterList[1][0][1])
            if objectType != "":
                # FreeCAD.Console.PrintMessage("\n内部的是否已被修改:\n")
                # FreeCAD.Console.PrintMessage([objectType,parameter])
                return [objectType,parameter]

    def __getSectionVolumeParameterList(self,type,parameterList):
        parameter = []
        if len(parameterList[1]) == 1:
            # 去掉前两个名字和类型参数
            plist = parameterList[1][0][2:]
            # 获取点名字列表
            pointNameList = plist[0][0:2]
            pointNameList.extend(plist[0][4:6])
            # 获取半径参数
            radiusList = plist[0][2:4]
            # 获取所有点的坐标列表
            pointParameterList = self.__getPointParameterList(parameterList[0], pointNameList)
            # 获取网格数据，传入参数为几何体的名称和几何体的网格命令参数
            markParameterList = self.__getMarkParameterList(parameterList[1][0][0], parameterList[2])
            # 获取attribute参数列表
            attributeParameterList = self.__getAttributeParameterList(parameterList[1][0][0])
            # 加入几何体名字
            parameter.append(parameterList[1][0][0])
            # 加入点的坐标列表
            parameter.extend(pointParameterList[0:2])
            # 加入半径参数
            parameter.extend(radiusList)
            # 加入点的坐标列表
            parameter.extend(pointParameterList[2:4])
            # 加入attribute参数
            parameter.append(attributeParameterList)
            # 加入网格参数
            parameter.extend(markParameterList)
            # 得到几何体类型
            objectType = self.__getObjectType(type,parameterList[1][0][1])
            if objectType != "":
                return [objectType,parameter]

    def __getExtrudedVolumeParameterList(self,type,parameterList):
        """获取挤出体参数列表"""
        parameter = []
        if len(parameterList[1]) == 1:
            # 去掉前两个名字和类型参数
            plist = parameterList[1][0][2:]
            # 获取线面名字列表
            labelList = plist[0][0:2]
            # 获取网格数据，传入参数为几何体的名称和几何体的网格命令参数
            markParameterList = self.__getMarkParameterList(parameterList[1][0][0], parameterList[2])
            # 获取attribute参数列表
            attributeParameterList = self.__getAttributeParameterList(parameterList[1][0][0])
            # 加入几何体名字
            parameter.append(parameterList[1][0][0])
            # 加入线面名字列表
            parameter.extend(labelList)
            # 加入attribute参数
            parameter.append(attributeParameterList)
            # 加入网格参数
            parameter.extend(markParameterList)
            # 得到几何体类型
            objectType = self.__getObjectType(type,parameterList[1][0][1])
            if objectType != "":
                return [objectType,parameter]

    def __getRevolutionVolumeParameterList(self,type,parameterList):
        """获取旋转体参数列表"""
        parameter = []
        if len(parameterList[1]) == 1:
            # 去掉前两个名字和类型参数
            plist = parameterList[1][0][2:]
            # 获取点名字列表
            pointNameList = plist[0][0:2]
            # 获取面名字
            areaLabel = plist[0][2]
            # 获取所有点的坐标列表
            pointParameterList = self.__getPointParameterList(parameterList[0], pointNameList)
            # 获取网格数据，传入参数为几何体的名称和几何体的网格命令参数
            markParameterList = self.__getMarkParameterList(parameterList[1][0][0], parameterList[2])
            # 获取attribute参数列表
            attributeParameterList = self.__getAttributeParameterList(parameterList[1][0][0])
            # 加入几何体名字
            parameter.append(parameterList[1][0][0])
            # 加入点的坐标列表
            parameter.extend(pointParameterList[0:2])
            # 加入面名字
            parameter.extend([areaLabel])
            # 加入attribute参数
            parameter.append(attributeParameterList)
            # 加入网格参数
            parameter.extend(markParameterList)
            # 得到几何体类型
            objectType = self.__getObjectType(type,parameterList[1][0][1])
            if objectType != "":
                return [objectType,parameter]

    def __getHelicalVolumeParameterList(self, type, parameterList):
        """得到螺旋体的参数列表"""
        parameter = []
        if len(parameterList[1]) == 1:
            # 去掉前两个名字和类型参数
            plist = parameterList[1][0][2:]
            # 获取点名字列表
            pointNameList = plist[0][0:2]
            pointNameList.extend(plist[0][4:5])
            # 获取半径参数
            radiusList = plist[0][2:4]
            radiusList.extend(plist[0][5:7])
            # 获取所有点的坐标列表
            pointParameterList = self.__getPointParameterList(parameterList[0], pointNameList)
            # 获取网格数据，传入参数为几何体的名称和几何体的网格命令参数
            markParameterList = self.__getMarkParameterList(parameterList[1][0][0], parameterList[2])
            # 获取attribute参数列表
            attributeParameterList = self.__getAttributeParameterList(parameterList[1][0][0])
            # 加入几何体名字
            parameter.append(parameterList[1][0][0])
            # 加入点的坐标列表
            parameter.extend(pointParameterList[0:2])
            # 加入半径参数
            parameter.extend(radiusList[0:2])
            # 加入点的坐标列表
            parameter.extend(pointParameterList[2:4])
            # 加入半径参数
            parameter.extend(radiusList[2:4])
            # 加入attribute参数
            parameter.append(attributeParameterList)
            # 加入网格参数
            parameter.extend(markParameterList)
            # 得到几何体类型
            objectType = self.__getObjectType(type, parameterList[1][0][1])
            if objectType != "":
                return [objectType, parameter]
    def __getFunctionVolumeParameterList(self,type, parameterList):
        parameter = []
        if len(parameterList[1]) == 1:
            # 获取函数体中点名字列表
            pointNameList = parameterList[1][0][2][1:]

            # 获取所有点的坐标列表
            pointParameterList = self.__getPointParameterList(parameterList[0], pointNameList)
            # 获取网格数据，传入参数为几何体的名称和几何体的网格命令参数
            markParameterList = self.__getMarkParameterList(parameterList[1][0][0], parameterList[2])
            # 获取attribute参数列表
            attributeParameterList = self.__getAttributeParameterList(parameterList[1][0][0])
            # 加入几何体名字
            parameter.append(parameterList[1][0][0])
            # @fubiao 这里列表得再加一个[]
            # 加入点的坐标列表
            parameter.extend(pointParameterList)
            #函数表达式
            parameter.append(parameterList[4][0][1])
            # 加入attribute参数
            if type == "VOLUME":
                parameter.append(attributeParameterList)
            # 加入网格参数
            parameter.extend(markParameterList)
            # 得到几何体类型
            objectType = self.__getObjectType(type,parameterList[1][0][1])
            if objectType != "":
                return [objectType,parameter]

    def getModlelingParameterList(self, ObjectStrList=[]):
        """
        获得所有模型的参数列表
        解析命令list为具体的参数
        :return: void
        """
        # 将体进行大致分类
        vertexVolume = ["CONFORMAL", "PARALLELEPIPEDAL", "PYRAMID", "WEDGE", "TETRAHEDRON", "RHOMBUS","OBLIQUE"]
        oneRadiusVolume = ["CYLINDRICAL", "SPHERICAL"]
        twoRadiusVolume = ["CONE", "ANNULAR", ]
        sectionVolume = ["ANNULAR_SECTION","TOROIDAL_SECTION"]
        # 最后返回的模型参数列表
        modlelingParamerList = []
        # 每个list中存储一个几何体的所有信息

        # 以生硬的方式直接复制参数阵列体开始和结束位置

        # 默认为解析几何建模信息
        if ObjectStrList == []:
            ObjectStrList = self.__objectStrList

        FreeCAD.Console.PrintMessage("\nlist中有那些信息？\n")
        FreeCAD.Console.PrintMessage(ObjectStrList)

        for list in ObjectStrList:
            # parameterList[0]存储点的信息，parameterList[1]存储线面体的信息，parameterList[2]存储网格的信息,parameterList[3]存储阵列体do信息
            # parameterList[4]函数体字符串
            FTO = []
            parameterList = [[],[],[],[],[]]
            # 存放阵列体do命令行和名字注释
            arrayStr = []
            commandType = []
            flag_param=True
            # 考虑到参数阵列体的存在，仅仅是一个flag不足以考虑所有的情况
            flag = True
            # 这个量用于存储阵列体的点的开头
            Array_PName=[]
            for line in list:
                # 以POINT开头的命令调用对应函数获取对应参数
                if line.startswith(self.__KeywordInCommand.POINT):
                    #阵列体的点信息是否是这里生成的,yes
                    # 如果说存在以Point开头的元素那也就是说不是参数阵列体
                    flag_param = False
                    parameterList[0].append(getPointParameter(line))
                    commandType = self.__KeywordInCommand.POINT
                # 以LINE开头的命令调用对应函数获取对应参数
                elif line.startswith(self.__KeywordInCommand.LINE):
                    parameterList[1].append(getLineParameter(line))
                    commandType = self.__KeywordInCommand.LINE
                    # type = parameterList[-1][1]
                # 以AREA开头的命令调用对应函数获取对应参数
                elif line.startswith(self.__KeywordInCommand.AREA):
                    parameterList[1].append(getAreaParameter(line))
                    commandType = self.__KeywordInCommand.AREA
                # 以VOLUME开头的命令调用对应函数获取对应参数
                elif line.startswith(self.__KeywordInCommand.VOLUME):
                    #我希望在这里找到后缀名
                    parameterList[1].append(getVolumeParameter(line))
                    # FreeCAD.Console.PrintMessage("\n我希望在这里找到vol_array\n")
                    # FreeCAD.Console.PrintMessage(parameterList[1])
                    commandType = self.__KeywordInCommand.VOLUME
                    # FreeCAD.Console.PrintMessage("\ntest0:\n")
                    # FreeCAD.Console.PrintMessage(line)
                    # FreeCAD.Console.PrintMessage("\ntest1:\n")
                    # FreeCAD.Console.PrintMessage(parameterList[1])
                    # 只有是阵列体的时候找后缀名才有意义
                    if flag==False:
                        for i in range(len(parameterList[1][0][-1])):
                            if parameterList[1][0][-1][i][0]!="A":
                                continue
                            index_beg = 0;
                            try:
                                index_beg=parameterList[1][0][-1][i].index(".",index_beg,len(parameterList[1][0][-1][0])-1)
                                # index_end=parameterList[1][0][-1][0].index(" ",index_beg+1,len(parameterList[1][0][-1][0])-1)
                            except:
                                continue
                            else:
                                Array_PName.append(parameterList[1][0][-1][i][index_beg + 1:])
                                continue
                # 以Mark开头的命令调用对应函数获取对应参数
                elif line.startswith(self.__KeywordInCommand.MARK):
                    parameterList[2].append(getMarkParameter(line))
                # 函数FUNCTION开头的命令
                elif line.startswith(self.__KeywordInCommand.FUNCTION):
                    parameterList[4].append(getFunctionParameter(line))
                # 以do开头的命令调用对应函数获取对应参数
                elif line.startswith(self.__KeywordInCommand.DO):
                    #找到DO这个关键字就说明是阵列体
                    flag = False
                    arrayStr.append(line)
                    if flag_param == True:
                        # 即这是参数阵列体
                        [temp,i_start,i_end,temp2]=re.split("=|,|;",line)
                        FTO.append(i_start)
                        FTO.append(i_end)
                        # FreeCAD.Console.PrintMessage("\n关于开始和结束位置的格式\n")
                        # FreeCAD.Console.PrintMessage(FTO)

                # else:
                #     # 阵列体以Ponit 之后字符串的后缀开头
                if flag:
                    if line.startswith("!!"):
                        arrayStr.append(line)



            if flag==False:
                for i in range(len(Array_PName)):
                    #先将原数据清空
                    parameterList[0][i][1] = []
                    index_i=0
                    for line in list:
                        #我希望在这里找到我重新定义的点并将其赋值给parameterList[0]
                        Name_len = len(Array_PName[i])
                        # FreeCAD.Console.PrintMessage("\n i get it \n")
                        # FreeCAD.Console.PrintMessage(line[0:Name_len]+"\t"+Array_PName[i])
                        if line[0:Name_len]==Array_PName[i]:
                            try:
                                index_equ = line.index("=")
                            except:
                                continue
                            else:
                                parameterList[0][i][1].append(line[index_equ+1:-1])
                                index_i+=1


            # 不是阵列体基础模型
            if flag:
                parameter = []
                if commandType == self.__KeywordInCommand.POINT:
                    # parameter = []
                    if len(parameterList[0]) == 1:
                        # 得到点的网格数据，传入参数为点的名称和点的网格命令参数
                        markParameterList = self.__getMarkParameterList(parameterList[0][0][0],parameterList[2])
                        # 加入点的名字和坐标参数
                        parameter.extend(parameterList[0][0])
                        # 加入网格参数
                        parameter.extend(markParameterList)
                        modlelingParamerList.append([ObjectsTools.ObjectType.Point,parameter])
                # 线
                elif commandType == self.__KeywordInCommand.LINE:

                    # 斜线
                    if parameterList[1][0][1] in oneRadiusVolume:
                        parameter = self.__getRadiusVolumeParameterList("LINE", parameterList, -1)
                    # 其他线
                    else:
                        parameter = self.__getVertexGeometryParameterList("LINE", parameterList)
                    if parameter is not None:
                        modlelingParamerList.append(parameter)
                # 面
                elif commandType == self.__KeywordInCommand.AREA:
                    parameter = self.__getVertexGeometryParameterList("AREA", parameterList)
                    if parameter is not None:
                        modlelingParamerList.append(parameter)
                # 体
                elif commandType == self.__KeywordInCommand.VOLUME:

                    # 都是顶点的体
                    if parameterList[1][0][1] in vertexVolume:

                        parameter = self.__getVertexGeometryParameterList( "VOLUME", parameterList)

                    # 有一个半径的体
                    elif parameterList[1][0][1] in oneRadiusVolume:
                        parameter = self.__getRadiusVolumeParameterList("VOLUME", parameterList, -1)

                    # 有两个半径的体
                    elif parameterList[1][0][1] in twoRadiusVolume:
                        parameter = self.__getRadiusVolumeParameterList("VOLUME", parameterList, -2)

                    # 两个部分体
                    elif parameterList[1][0][1] in sectionVolume:

                        parameter = self.__getSectionVolumeParameterList("VOLUME", parameterList)
                    # 挤出体
                    elif parameterList[1][0][1] == self.__VolumeType.extruded:

                        parameter = self.__getExtrudedVolumeParameterList("VOLUME", parameterList)

                    # 旋转体
                    elif parameterList[1][0][1] == self.__VolumeType.rotate:

                        parameter = self.__getRevolutionVolumeParameterList("VOLUME", parameterList)

                    # 螺旋体
                    elif parameterList[1][0][1] == self.__VolumeType.helical:

                        parameter = self.__getHelicalVolumeParameterList("VOLUME", parameterList)
                    elif parameterList[1][0][1]==self.__VolumeType.functional:

                        parameter = self.__getFunctionVolumeParameterList("VOLUME", parameterList)

                    if parameter is not None:
                            modlelingParamerList.append(parameter)
            # 是阵列体基础模型
            else:
                # 存放阵列体的点坐标信息
                pointCoordinateStrList = []
                for pointParameter in parameterList[0]:
                    coordinates = pointParameter[1]
                    pointCoordinateStrList.append(coordinates)
                self.getCoordinateSystem()
                [arrayName, arrayType, args, pointCoordinatesList] = getArrayParameter(self.coordinateSystem, arrayStr, pointCoordinateStrList)
                if flag_param == True:
                    #如果是参数阵列体，那这个就应该被换掉
                    args[-5]=FTO
                # 赋予基础体的点坐标信息
                for index in range(len(parameterList[0])):
                    parameterList[0][index][1]= pointCoordinatesList[index]

                # 基础模型参数列表
                baseModlelingParamerList = []
                parameter = []
                if commandType == self.__KeywordInCommand.POINT:
                    if len(parameterList[0]) == 1:
                        # 得到点的网格数据，传入参数为点的名称和点的网格命令参数
                        markParameterList = self.__getMarkParameterList(parameterList[0][0][0],parameterList[2])
                        # 加入点的名字和坐标参数
                        parameter.extend(parameterList[0][0])
                        # 加入网格参数
                        parameter.extend(markParameterList)
                        baseModlelingParamerList = [ObjectsTools.ObjectType.Point,parameter]
                # 线
                elif commandType == self.__KeywordInCommand.LINE:

                    # 斜线
                    if parameterList[1][0][1] in oneRadiusVolume:
                        parameter = self.__getRadiusVolumeParameterList("LINE", parameterList, -1)
                    # 其他线
                    else:
                        parameter = self.__getVertexGeometryParameterList("LINE", parameterList)
                    if parameter is not None:
                        baseModlelingParamerList = parameter
                # 面
                elif commandType == self.__KeywordInCommand.AREA:
                    parameter = self.__getVertexGeometryParameterList("AREA", parameterList)
                    if parameter is not None:
                        baseModlelingParamerList = parameter
                # 体
                elif commandType == self.__KeywordInCommand.VOLUME:

                    # 都是顶点的体
                    if parameterList[1][0][1] in vertexVolume:
                        FreeCAD.Console.PrintMessage("\n正投影体似乎缺少了什么")
                        FreeCAD.Console.PrintMessage(parameterList)
                        parameter = self.__getVertexGeometryParameterList( "VOLUME", parameterList)

                    # 有一个半径的体
                    elif parameterList[1][0][1] in oneRadiusVolume:
                        parameter = self.__getRadiusVolumeParameterList("VOLUME", parameterList, -1)

                    # 有两个半径的体
                    elif parameterList[1][0][1] in twoRadiusVolume:
                        # FreeCAD.Console.PrintMessage("\ntest:\n")
                        # FreeCAD.Console.PrintMessage(parameterList[1])
                        # FreeCAD.Console.PrintMessage("\ntest2:\n")
                        # FreeCAD.Console.PrintMessage(parameterList)
                        parameter = self.__getRadiusVolumeParameterList("VOLUME", parameterList, -2)
                        # FreeCAD.Console.PrintMessage("\n如果执行的是这里，那问题很有可能就在这里： \n")
                        # FreeCAD.Console.PrintMessage(parameter)
                    # 两个部分体
                    elif parameterList[1][0][1] in sectionVolume:

                        parameter = self.__getSectionVolumeParameterList("VOLUME", parameterList)
                    # 挤出体
                    elif parameterList[1][0][1] == self.__VolumeType.extruded:

                        parameter = self.__getExtrudedVolumeParameterList("VOLUME", parameterList)

                    # 旋转体
                    elif parameterList[1][0][1] == self.__VolumeType.rotate:

                        parameter = self.__getRevolutionVolumeParameterList("VOLUME", parameterList)

                    # 螺旋体
                    elif parameterList[1][0][1] == self.__VolumeType.helical:

                        parameter = self.__getHelicalVolumeParameterList("VOLUME", parameterList)

                    if parameter is not None:
                            baseModlelingParamerList = parameter
                if baseModlelingParamerList != []:
                    baseName = baseModlelingParamerList[1][0]
                    FreeCAD.Console.PrintMessage("\nbaseModelingParamerList:\n")
                    FreeCAD.Console.PrintMessage(baseModlelingParamerList)
                    infoList = [arrayName, baseName, arrayType]
                    infoList.extend(args)
                    if flag_param==False:
                        modlelingParamerList.append([ObjectsTools.ObjectType.Vol_Array, infoList, baseModlelingParamerList])
                    else:
                        modlelingParamerList.append([ObjectsTools.ObjectType.Vol_ParamArray, infoList, baseModlelingParamerList])
        return modlelingParamerList

    ########################## 以下是根据m3d文件获取ProjectSetting面板参数 ##########################

    def __getHeaderCommandsStr(self):
        """将Header部分的命令拼接成字符串"""
        headerCommandsStr = ""
        for line in self.__headerSystemStrList[0]:
            headerCommandsStr = headerCommandsStr + line + "\n"
        return headerCommandsStr

    def __getWorkSpaceSettingCommandsStr(self):
        """将WorkSpaceSetting部分的命令拼接成字符串"""
        workSpaceSettingCommandsStr = ""
        for line in self.__meshStrList:
            workSpaceSettingCommandsStr = workSpaceSettingCommandsStr + line + "\n"
        return workSpaceSettingCommandsStr

    def __getStepParameterList(self):
        """"得到WorkSpaceSetting中步长参数"""
        stepParameterList = ['1mm','1mm','1mm']
        # 得到最后三行参数和换行
        for line in self.__parameterStrList[-6:]:
            result = getParameter(line)
            # FreeCAD.Console.PrintMessage("\nParameter:\n")
            # FreeCAD.Console.PrintMessage(result)
            if result is not None:
                if result[0] == "DX1":
                    stepParameterList[0] = result[1]
                elif result[0] == "DX2":
                    stepParameterList[1] = result[1]
                elif result[0] == "DX3":
                    stepParameterList[2] = result[1]
        return stepParameterList

    def __getCommonPresetsCommandsStr(self):
        """将strCommonPresets部分的命令拼接成字符串"""
        commonPresetsCommandsStr = ""
        for line in self.__commonPresetsStrList:
            commonPresetsCommandsStr = commonPresetsCommandsStr + line + "\n"
        return commonPresetsCommandsStr

    def __getSimulationSettingsStrCommandsStr(self):
        """将simulationSettingsStr部分的命令拼接成字符串"""
        simulationSettingCommandsStr = ""
        for line in self.__simulationSettingsStrList:
            simulationSettingCommandsStr = simulationSettingCommandsStr + line + "\n"
        return simulationSettingCommandsStr

    def __getDumpOptionsStrCommandsStr(self):
        """将dumpOptionsStr部分的命令拼接成字符串"""
        dumpOptionsCommandsStr = ""
        for line in self.__dumpOptionsStrList:
            dumpOptionsCommandsStr = dumpOptionsCommandsStr + line + "\n"
        return dumpOptionsCommandsStr

    def __getRunOptionsStrCommandsStr(self):
        """将runOptionsStr部分的命令拼接成字符串"""
        runOptionsCommandsStr = ""
        for line in self.__runOptionsStrList:
            runOptionsCommandsStr = runOptionsCommandsStr + line + "\n"
        return runOptionsCommandsStr

    def getProjectSettingList(self):
        """得到工程性面板的参数列表"""
        # 用来存放工程性面板的参数列表
        projectSettingList = []

        # 得到header部分命令字符串
        headerCommandsStr = self.__getHeaderCommandsStr()
        # 得到header部分参数
        headerParameter = getHeaderParameter(headerCommandsStr)
        # 判断传回参数是否有意义


        if headerParameter != ["","","",""]:
            projectSettingList.append(["ModelingInfo", headerParameter])


        # 得到WorkSpaceSetting中步长参数
        [x1Step, x2Step, x3Step] = self.__getStepParameterList()
        # 得到WorkSpaceSetting部分命令字符串
        workSpaceSettingCommandsStr = self.__getWorkSpaceSettingCommandsStr()
        # 得到WorkSpaceSetting部分参数
        workSpaceSettingParameter = getWorkSpaceSettingParameter(workSpaceSettingCommandsStr)

        [name, x1Start, x1Stop, x2Start, x2Stop, x3Start, x3Stop] = workSpaceSettingParameter
        # 判断传回参数是否有意义,没意义说明未启用，传回False
        if workSpaceSettingParameter != ["", "", "", "", "", "", ""]:
            projectSettingList.append(["WorkSpaceSettings", [name, [x1Start, x1Stop, x1Step], [x2Start, x2Stop, x2Step], [x3Start, x3Stop, x3Step],True]])
        else:
            projectSettingList.append(["WorkSpaceSettings", [name, [x1Start, x1Stop, x1Step], [x2Start, x2Stop, x2Step],
                                                             [x3Start, x3Stop, x3Step], False]])

        # 得到CommonPresets部分命令字符串
        commonPresetsCommandsStr = self.__getCommonPresetsCommandsStr()


        # 得到Materical部分参数
        matericalParameter = getMatericalParameter(commonPresetsCommandsStr)
        if matericalParameter != ["", "", "", "", [False, ""], [False, ""]]:
            projectSettingList.append(["NewMaterical",matericalParameter])

        # @fubiao 得到SPECIES 参数
        speciesParameter = getSpeciesParameter(commonPresetsCommandsStr)
        if speciesParameter != ["", "", "", ""]:
            projectSettingList.append(["Species",speciesParameter])

        # 得到FiledSetting部分参数
        filedSettingParameter = getFiledSettingParameter(commonPresetsCommandsStr)

        if filedSettingParameter != [[False, ""], [False, ""], [False, ""], [False, ""], [False, ""], [False, ""], ""]:
            projectSettingList.append(["FiledSetting", filedSettingParameter])

        # 得到TimeDomainComputing部分参数
        simulationSettingCommandsStr = self.__getSimulationSettingsStrCommandsStr()

        timeDomainComputingParameter = getTimeDomainComputingParameter(simulationSettingCommandsStr)
        if timeDomainComputingParameter[1] != "error":
            projectSettingList.append(["TimeDomainComputing", timeDomainComputingParameter])


        # 得到DataProcessingSetting部分参数
        dumpOptionsCommandsStr = self.__getDumpOptionsStrCommandsStr()
        dataProcessingSettingParameter = getDataProcessingSettingParameter(dumpOptionsCommandsStr)

        if dataProcessingSettingParameter[-1] != [False,False]:
            projectSettingList.append(["DataProcessingSetting",dataProcessingSettingParameter])


        # 得到RunOptions部分参数
        runOptionsCommandsStr = self.__getRunOptionsStrCommandsStr()
        runOptionsParameter = getRunOptionsParameter(runOptionsCommandsStr)

        projectSettingList.append(["RunOptions", runOptionsParameter])

        return projectSettingList


    ########################## 以下是根据m3d文件获取物理参数 ##########################
    def __getPanelObjectStr(self, panelName):
        """获得某个面板对应的体的m3d文件部分"""
        for objectStr in self.__panelObjectStrList:
            if "!!" in objectStr[0]:
                if panelName == objectStr[0].split("!!")[1].split(" ")[0]:
                    return [objectStr]
        return None

    def __getDefinedObjectStr(self, ObjectName):
        """获得某个定义的体的m3d文件部分"""
        for objectStr in self.__objectStrList:
            if "!!" in objectStr[0]:
                if ObjectName == objectStr[0].split("!!")[1]:
                    return [objectStr]

        return None

    def __getInitStartPointCoordinate(self):

        self.getCoordinateSystem()
        if self.coordinateSystem == self.__CoordinateSystem.rectangularSys:
            return ["0mm", "0mm", "0mm"]
        elif self.coordinateSystem == self.__CoordinateSystem.polarSys:
            return ["0mm", "0deg", "0mm"]
        elif self.coordinateSystem == self.__CoordinateSystem.cylindricalSys:
            return ["0mm", "0mm", "0deg"]

    def __getInitStopPointCoordinate(self):

        self.getCoordinateSystem()
        if self.coordinateSystem == self.__CoordinateSystem.rectangularSys:
            return ["0mm", "0mm", "0mm"]
        elif self.coordinateSystem == self.__CoordinateSystem.polarSys:
            return ["0mm", "360deg", "0mm"]
        elif self.coordinateSystem == self.__CoordinateSystem.cylindricalSys:
            return ["0mm", "0mm", "360deg"]

    def __getPortParameterList(self, panelName, mainCommandStr, extraCommandStr):
        """获得Port的参数列表"""
        parameter = getPortParameter(mainCommandStr)

        direction = parameter[1]
        isPhaseVelocity = parameter[2]
        phaseVelocity = parameter[3]
        isScale = parameter[4]
        scale = parameter[5]
        isFt = parameter[6]
        ftVal = parameter[7]
        isGeFirst = parameter[8]
        geFirstName = parameter[9]
        geFirstVal = parameter[10]
        isGeSecond = parameter[11]
        geSecondName = parameter[12]
        geSecondVal = parameter[13]
        isNormalization = parameter[14]
        normalizationLine = parameter[15]
        isLaplacian = parameter[16]
        laplacianFirst = parameter[17]
        laplacianSecond = parameter[18]
        laplaceNumber1 = parameter[19]
        laplaceNumber2 = parameter[20]
        laplaceNumber3 = parameter[21]
        laplaceNumber4 = parameter[22]
        laplaceNumber5 = parameter[23]
        laplacianThrid = parameter[24]
        laplacianFourth = parameter[25]
        laplacianFifth = parameter[26]
        laplace_num = parameter[27]
        circuit_Checked = parameter[28]
        circuit = parameter[29]
        observe_name =  parameter[30]

        if extraCommandStr == None:
            # 指定正交投影面
            isAppointArea = True
            areaName = parameter[0]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(areaName))[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]
            isNewConformalLine = False

        # 指定投影面但未指定正交投影线，新建了线
        elif isNormalization and len(extraCommandStr[0])<6:
            sayz("len(extraCommandStr[0])<6")
            sayz(len(extraCommandStr[0]))
            # 指定正交投影面
            isAppointArea = True
            areaName = parameter[0]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(areaName))[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]
            isNewConformalLine = True
        else:
            # 没有指定正交投影面
            isAppointArea = False
            areaName = "未指定"
            sayz("len(extraCommandStr[0])")
            sayz(len(extraCommandStr[0]))
            sayz(extraCommandStr[0])
            # 如果指定了线上电压归一化，处理一下在获得点参数
            if isNormalization:
                # 标记第一次出现非空字符串
                flag = 0
                for i in range(0,len(extraCommandStr[0])):
                    if extraCommandStr[0][i] != "":
                        flag = i
                        break
                # 去除定义线的最后两行，删除一行后，标号改变，冉蔚上一行的标号
                extraCommandStr[0].remove(extraCommandStr[0][flag + 4])
                # extraCommandStr[0].remove(extraCommandStr[0][flag + 4])

            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]
            isNewConformalLine = True

        isX1 = objectList[3]
        isX2 = objectList[4]
        isX3 = objectList[5]
        X1Size = objectList[6]
        X2Size = objectList[7]
        X3Size = objectList[8]

        return [panelName, direction,
                isPhaseVelocity, phaseVelocity,
                isScale, scale,
                isFt, ftVal,
                isGeFirst, geFirstName, geFirstVal,
                isGeSecond, geSecondName, geSecondVal,
                isNormalization, isNewConformalLine, normalizationLine,
                isLaplacian, laplacianFirst, laplacianSecond,
                isAppointArea, areaName, startPointCoordinates, stopPointCoordinates,
                isX1, isX2, isX3, X1Size, X2Size, X3Size,
                laplaceNumber1,laplaceNumber2,
                laplacianThrid,laplacianFourth,laplacianFifth,
                laplaceNumber3,laplaceNumber4,laplaceNumber5,
                laplace_num,
                circuit_Checked,circuit,
                observe_name]

    def __getFreeParameterList(self, panelName, mainCommandStr, extraCommandStr):
        """获得Free的参数列表"""
        parameter = getFreeParameter(mainCommandStr)

        xType = parameter[1]
        trendType = parameter[2]
        component = parameter[3]
        conductivityList = parameter[4]

        if extraCommandStr == None:
            # 指定正交投影面
            areaName = parameter[0]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(areaName))[0][1]

        else:
            # 没有指定正交投影面
            areaName = "未指定"
            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]

        startPointCoordinates = objectList[1]
        stopPointCoordinates = objectList[2]
        isX1 = objectList[4]
        isX2 = objectList[5]
        isX3 = objectList[6]
        X1Size = objectList[7]
        X2Size = objectList[8]
        X3Size = objectList[9]

        return [panelName,
                areaName,
                startPointCoordinates,
                stopPointCoordinates,
                xType,
                trendType,
                component,
                conductivityList,
                isX1, isX2, isX3, X1Size, X2Size, X3Size]

    def __getSymmetryParameterList(self, panelName, mainCommandStr, extraCommandStr):
        """获得Symmetry的参数列表"""
        parameter = getSymParameter(mainCommandStr)

        # 初始化
        type = parameter[0]
        trendTypeList = parameter[1]
        normalPeriod = "0deg"
        normal1=False
        normal2=False
        normal3=False

        if extraCommandStr == None:
            # 指定正交投影面
            lineOrArea1 = parameter[2]
            lineOrArea2 = parameter[3]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(lineOrArea1))[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        else:
            # 没有指定正交投影面
            lineOrArea1 = "未指定"
            lineOrArea2 = "未指定"
            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        isX1 = objectList[3]
        isX2 = objectList[4]
        isX3 = objectList[5]
        X1Size = objectList[6]
        X2Size = objectList[7]
        X3Size = objectList[8]
        # 根据startPoint和stopPoin求得法向方向
        if startPointCoordinates[0]==stopPointCoordinates[0]:
            normal1=True
        elif startPointCoordinates[1]==stopPointCoordinates[1]:
            normal2=True
        else:
            normal3=True
        # 从注释中提取法向周期
        try:
            normalPeriod=extraCommandStr[0][0].split(" ")[1]
        except:
            normalPeriod=""
    
        return [panelName,
                lineOrArea1,
                startPointCoordinates,
                stopPointCoordinates,
                [normal1, normal2, normal3],
                trendTypeList,
                [type, lineOrArea2],
                normalPeriod,
                [isX1, isX2, isX3],
                [X1Size, X2Size, X3Size]]

    def __getContourParameterList(self, panelName, mainCommandStr, extraCommandStr):
        """获得Contour的参数列表"""
        parameter = getContourParameter(mainCommandStr)

        field = parameter[1]
        timerName = parameter[2]
        isShade = parameter[3]

        if extraCommandStr == None:
            # 指定正交投影面
            isAppointArea = True
            areaName = parameter[0]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(areaName))[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        else:
            # 没有指定正交投影面
            isAppointArea = False
            areaName = "未指定"
            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        return [panelName, field, timerName, isShade,
                isAppointArea, areaName, startPointCoordinates, stopPointCoordinates]

    def __getVectorParameterList(self, panelName, mainCommandStr, extraCommandStr):
        """获得Vector的参数列表"""
        parameter = getVectorParameter(mainCommandStr)

        field1 = parameter[0]
        field2 = parameter[1]
        timerName = parameter[3]
        isNumber = parameter[4]
        number1 = parameter[5]
        number2 = parameter[6]

        if extraCommandStr == None:
            # 指定正交投影面
            isAppointArea = True
            areaName = parameter[2]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(areaName))[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        else:
            # 没有指定正交投影面
            isAppointArea = False
            areaName = "未指定"
            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        return [field1, field2, panelName, timerName, isNumber, number1, number2,
                isAppointArea, areaName, startPointCoordinates, stopPointCoordinates]

    def __getPhasespaceParameterList(self, panelName, mainCommandStr):
        """获得Phasespace的参数列表"""
        parameter = getPhasespaceParameter(mainCommandStr)
        parameter.insert(0, panelName)

        return parameter

    def __getRangeParameterList(self, panelName, mainCommandStr, extraCommandStr):
        """获得Range的参数列表"""
        parameter = getRangeParameter(mainCommandStr)

        field = parameter[1]
        timerName = parameter[2]
        isFFT = parameter[3]
        isMagnitude = parameter[4]
        isComplex = parameter[5]

        if extraCommandStr == None:
            # 指定正交投影线
            isAppointLine = True
            lineName = parameter[0]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(lineName))[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        else:
            # 指定正交投影线
            isAppointLine = False
            lineName = "未指定"
            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        return [panelName, field, timerName, isFFT, isMagnitude, isComplex,
                isAppointLine, lineName, startPointCoordinates, stopPointCoordinates]

    def __getObserveParameterList(self, panelName, mainCommandStr, extraCommandStr):
        """获得Range的参数列表"""
        # FreeCAD.Console.PrintError('\n'+str(mainCommandStr)+'\n')
        parameter = getObserveParameter(mainCommandStr)

        isField = parameter[0][0]
        isFieldIntegral = parameter[0][1]
        isFieldPower = parameter[0][2]
        isFieldEnergy = parameter[0][3]
        isParticleStatistics = parameter[0][4]
        isParticleCollected=parameter[0][5]
        isParticleEmitted = parameter[0][6]
        isParticleDestroyed = parameter[0][7]

        field = [parameter[1][0],parameter[1][2]]

        isFFT = parameter[2][0]
        fftType = parameter[2][1]
        # @fubiao
        isFreq=parameter[2][2]
        freqFrom = parameter[2][3]
        freqTo = parameter[2][4]

        isTime = parameter[3][0]
        timeFrom = parameter[3][1]
        timeTo = parameter[3][2]

        isInterval = parameter[4][0]
        interval = parameter[4][1]

        isFilter = parameter[5][0]
        filterType = parameter[5][1]
        timePara = parameter[5][2]

        name2 = parameter[6][0]

        if extraCommandStr == None:
            # 指定
            isAppoint = True
            appointName = parameter[1][1]

            #初始化
            startPointCoordinates = self.__getInitStartPointCoordinate()
            stopPointCoordinates = self.__getInitStopPointCoordinate()

            # if isEmitEps:
            #     obverseType = "EMIT"
            # else:
            objectType = self.getModlelingParameterList(self.__getDefinedObjectStr(appointName))[0][0]
            objectList = self.getModlelingParameterList(self.__getDefinedObjectStr(appointName))[0][1]
            if objectType == ObjectsTools.ObjectType.Point:
                obverseType = "POINT"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = self.__getInitStopPointCoordinate()
            elif objectType == ObjectsTools.ObjectType.Line_Conformal:
                obverseType = "LINE"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]
            elif objectType == ObjectsTools.ObjectType.Area_Conformal:
                obverseType = "AREA"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]
            elif objectType == ObjectsTools.ObjectType.Vol_Conformal:
                obverseType = "VOLUME"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]

        else:
            # 没有指定
            isAppoint = False
            appointName = "未指定"

            # 初始化
            obverseType = "POINT"
            startPointCoordinates = self.__getInitStartPointCoordinate()
            stopPointCoordinates = self.__getInitStopPointCoordinate()

            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            objectType = self.getModlelingParameterList(extraCommandStr)[0][0]
            if objectType == ObjectsTools.ObjectType.Point:
                obverseType = "POINT"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = self.__getInitStopPointCoordinate()
            elif objectType == ObjectsTools.ObjectType.Line_Conformal:
                obverseType = "LINE"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]
            elif objectType == ObjectsTools.ObjectType.Area_Conformal:
                obverseType = "AREA"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]
            elif objectType == ObjectsTools.ObjectType.Vol_Conformal:
                obverseType = "VOLUME"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]

        return [panelName,
                isField, isFieldIntegral, isFieldPower, isFieldEnergy, isParticleStatistics,
                isParticleCollected,isParticleEmitted,isParticleDestroyed, field,
                isFFT, fftType, isFreq,freqFrom, freqTo,
                isTime, timeFrom, timeTo,
                isInterval,interval,
                isFilter, filterType, timePara,
                obverseType, isAppoint, appointName, startPointCoordinates, stopPointCoordinates,name2]

    def __getTimerParameterList(self, mainCommandStr):
        """获得Timer的参数列表"""
        parameter = getTimerParameter(mainCommandStr)
        return parameter

    def __getDriverParameterList(self, mainCommandStr):
        """获得Driver的参数列表"""
        parameter = getDriverParameter(mainCommandStr)
        FreeCAD.Console.PrintError("\nmainCommandStr:"+str(mainCommandStr))

        [name, currentDensity, funExpression] = parameter

        # 获得附加命令对应的文件部分
        extraCommandStr = self.__getPanelObjectStr(name)
        FreeCAD.Console.PrintError("\nextraCommandStr:"+str(extraCommandStr))

        if extraCommandStr is not None:

            # 初始化
            Current_Source = u"点电流源"
            startPointCoordinates = self.__getInitStartPointCoordinate()
            stopPointCoordinates = self.__getInitStopPointCoordinate()

            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            objectType = self.getModlelingParameterList(extraCommandStr)[0][0]
            if objectType == ObjectsTools.ObjectType.Point:
                Current_Source = u"点电流源"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = self.__getInitStopPointCoordinate()
            elif objectType == ObjectsTools.ObjectType.Line_Conformal:
                Current_Source = u"线电流源"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]
            elif objectType == ObjectsTools.ObjectType.Area_Conformal:
                Current_Source = u"面电流源"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]
            elif objectType == ObjectsTools.ObjectType.Vol_Conformal:
                Current_Source = u"体电流源"
                startPointCoordinates = objectList[1]
                stopPointCoordinates = objectList[2]

            return [name, Current_Source, startPointCoordinates, stopPointCoordinates, currentDensity, funExpression]
        else:
            sayz("没找到对应电流源")

    def __getFoilParameterList(self,mainCommandStr, panelName=" "):
        """获得Foil的参数列表"""
        parameter = getFoilParameter(mainCommandStr)

        [name, thick, isDIY, DITMaterial, isDefault, defaultMaterial] = parameter

        # 获得附加命令对应的文件部分
        extraCommandStr = self.__getPanelObjectStr(name)

        if extraCommandStr == None:
            # 指定正交投影体
            areaName = parameter[0]
            startPointCoordinates = self.__getInitStartPointCoordinate()
            stopPointCoordinates = self.__getInitStopPointCoordinate()

        else:
            # 没有指定正交投影体
            areaName = u"未指定"
            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        startPointCoordinates.extend(stopPointCoordinates)
        return [panelName, areaName, startPointCoordinates,
                thick, isDIY, DITMaterial, isDefault, defaultMaterial]

    def __getInductorParameterList(self, mainCommandStr):
        """获得Inductor的参数列表"""
        parameter = getInductorParameter(mainCommandStr)

        [name, diameter, isInductance, inductance] = parameter

        # 获得附加命令对应的文件部分
        extraCommandStr = self.__getPanelObjectStr(name)

        if extraCommandStr == None:
            # 指定正交投影线
            lineName = parameter[0]
            startPointCoordinates = self.__getInitStartPointCoordinate()
            stopPointCoordinates = self.__getInitStopPointCoordinate()

        else:
            # 指定正交投影线
            lineName = u"未指定"
            objectList = self.getModlelingParameterList(extraCommandStr)[0][1]
            startPointCoordinates = objectList[1]
            stopPointCoordinates = objectList[2]

        startPointCoordinates.extend(stopPointCoordinates)
        return [name, lineName, startPointCoordinates,
                diameter, isInductance, inductance]

    def getPhysicsParameterList(self):
        # FreeCAD.Console.PrintError('\n\n ni fan zhuan \n\n\n')
        returnList = []

        # print "===========================__panelObjectStrList"
        # print self.__panelObjectStrList
        # 查看面板对应的体

        # print "===========================__allPlotsStrList"
        # print self.__allPlotsStrList
        # 获得allPlot对应的参数
        for panelList in self.__allPlotsStrList:
            sayz("panelList")
            sayz(panelList)
            panelName = "error panelName"

            # 对于obs面板
            obsStr = ""
            obsNum = 0

            for panelLine in panelList:
                # 每个panelList的第一行都是"!!" + 面板名称的格式，获取对应的面板名称
                if panelLine.startswith("!!"):
                    panelName = panelLine[2:len(panelLine)]

                # 获得每个面板对应的基本命令参数

                # Timer
                if panelLine.startswith(self.__KeywordInCommand.TIMER):
                    # 获得主命令对应的文件部分
                    mainCommandStr = panelLine
                    # 获得参数列表
                    parameter = self.__getTimerParameterList(mainCommandStr)
                    # 加入到返回列表中
                    if parameter[0] == "DefTimer":
                        returnList.append(["DefTimer_Type", parameter])
                    else:
                        returnList.append(["Timer_Type", parameter])

                # Cntr
                elif panelLine.startswith(self.__KeywordInCommand.CONTOUR):
                    # 获得主命令对应的文件部分
                    mainCommandStr = panelLine
                    # 获得附加命令对应的文件部分
                    extraCommandStr = self.__getPanelObjectStr(panelName)
                    # 获得参数列表
                    parameter = self.__getContourParameterList(panelName, mainCommandStr, extraCommandStr)
                    # 加入到返回列表中
                    returnList.append(["Cntr_Type", parameter])

                # Vec
                elif panelLine.startswith(self.__KeywordInCommand.VECTOR):
                    # 获得主命令对应的文件部分
                    mainCommandStr = panelLine
                    # 获得附加命令对应的文件部分
                    extraCommandStr = self.__getPanelObjectStr(panelName)
                    # 获得参数列表
                    parameter = self.__getVectorParameterList(panelName, mainCommandStr, extraCommandStr)
                    # 加入到返回列表中
                    returnList.append(["Vec_Type", parameter])

                # Pha
                elif panelLine.startswith(self.__KeywordInCommand.PHASESPACE):
                    # 获得主命令对应的文件部分
                    mainCommandStr = panelLine
                    # 获得参数列表
                    parameter = self.__getPhasespaceParameterList(panelName, mainCommandStr)
                    # 加入到返回列表中
                    returnList.append(["Pha_Type", parameter])

                # Ran
                elif panelLine.startswith(self.__KeywordInCommand.RANGE):
                    # 获得主命令对应的文件部分
                    mainCommandStr = panelLine
                    # 获得附加命令对应的文件部分
                    extraCommandStr = self.__getPanelObjectStr(panelName)
                    # 获得参数列表
                    parameter = self.__getRangeParameterList(panelName, mainCommandStr, extraCommandStr)
                    # 加入到返回列表中
                    returnList.append(["Ran_Type", parameter])

                # Obs
                elif panelLine.startswith(self.__KeywordInCommand.OBSERVE):

                    obsStr = obsStr + panelLine + "\n"
                    obsNum = obsNum + 1

                    # 遇到obs的最后一行
                    if obsNum == len(panelList)-1:
                        # 获得主命令对应的文件部分
                        mainCommandStr = obsStr
                        # 获得附加命令对应的文件部分
                        extraCommandStr = self.__getPanelObjectStr(panelName)
                        # 获得参数列表
                        parameter = self.__getObserveParameterList(panelName, mainCommandStr, extraCommandStr)
                        # 加入到返回列表中
                        returnList.append(["Obs_Type", parameter])

                elif panelLine.startswith(self.__KeywordInCommand.SPECIES):
                    FreeCAD.Console.PrintError("SPECIES:"+str(panelLine)+"\n")

        # print "===========================__emission"
        # print self.__emission
        # 发射面板对应的参数
        # FreeCAD.Console.PrintError("\nself.__emission：  "+str(self.__emission))
        for panel in self.__emission:
            # EmB
            if "BEAM" in panel:
                parameter = getEmBParameter(panel)
                returnList.append(["EMB_Type", parameter])
            # EmE
            if "EXPLOSIVE" in panel:
                parameter = getEmEParameter(panel)
                returnList.append(["EME_Type", parameter])
            # EmB
            if "GYRO" in panel:
                parameter = getEmGParameter(panel)
                returnList.append(["EMG_Type", parameter])
            # EmB
            if "HIGH_FIELD" in panel:
                parameter = getEmHParameter(panel)
                returnList.append(["EMH_Type", parameter])
            # EmB
            if "THERMIONIC" in panel:
                parameter = getEmTParameter(panel)
                returnList.append(["EMT_Type", parameter])
            # Populate
            if "POPULATE" in panel:
                # FreeCAD.Console.PrintError("\n进入到设置populate 变量的过程")
                parameter = getPopulateParameter(panel)
                returnList.append(["Populate_Type", parameter])
            # Gasgas
            if "GASGAS" in panel:
                parameter = getGasgasParameter(panel)
                returnList.append(["Gasgas_Type", parameter])
            # SECONDARY
            if "SECONDARY" in panel:
                parameter = getEmseParameter(panel)
                returnList.append(["EmSE_Type", parameter])

        # print "===========================__commonBoundary"
        # print self.__commonBoundary
        # 获得常用边界对应的参数
        for panel in self.__commonBoundary:
            # 获得面板名称
            panelNameLine = panel.split("\n")[0]
            panelName = panelNameLine[2:len(panelNameLine)]

            if self.__KeywordInCommand.PORT in panel:
                # 获得主命令对应的文件部分
                mainCommandStr = panel
                # 获得附加命令对应的文件部分
                extraCommandStr = self.__getPanelObjectStr(panelName)
                # 获得参数列表
                parameter = self.__getPortParameterList(panelName, mainCommandStr, extraCommandStr)
                # FreeCAD.Console.PrintError(str(mainCommandStr)+'\n\n\n')
                # 加入到返回列表中
                returnList.append(["Port_Type", parameter])

            if self.__KeywordInCommand.FREESPACE in panel:
                # 获得主命令对应的文件部分
                mainCommandStr = panel
                # 获得附加命令对应的文件部分
                extraCommandStr = self.__getPanelObjectStr(panelName)
                # 获得参数列表
                parameter = self.__getFreeParameterList(panelName, mainCommandStr, extraCommandStr)
                # 加入到返回列表中
                returnList.append(["Free_Type", parameter])

            if self.__KeywordInCommand.SYMMETRY in panel:
                # 获得主命令对应的文件部分
                mainCommandStr = panel
                # 获得附加命令对应的文件部分
                extraCommandStr = self.__getPanelObjectStr(panelName)
                # 获得参数列表
                parameter = self.__getSymmetryParameterList(panelName, mainCommandStr, extraCommandStr)
                # 加入到返回列表中
                returnList.append(["Sym_Type", parameter])


        # 获得otherModels对应的参数
        # FreeCAD.Console.PrintError("\n进入获得otherModels对应的参数::"+str(self.__otherModelsStrList))
        for otherModelsStr in self.__otherModelsStrList:
            panelName=""
            # FreeCAD.Console.PrintError("\n进入获得otherModels对应的参数")
            if otherModelsStr.startswith("!!"):
                indexN=otherModelsStr.find("\n")
                panelName = otherModelsStr[2:indexN]
                otherModelsStr=otherModelsStr[indexN+1:]
            # 激励电源
            if otherModelsStr.startswith(self.__KeywordInCommand.FUNCTION) and self.__KeywordInCommand.INDUCTOR in otherModelsStr:
                # 获得参数列表
                FreeCAD.Console.PrintError("\n进入激励电源选项")
                parameter = self.__getDriverParameterList(otherModelsStr)
                # 加入到返回列表中
                if parameter is not None:
                    returnList.append(["ExP_Type", parameter])

            # foil
            elif otherModelsStr.startswith(self.__KeywordInCommand.FOIL):
                # 获得参数列表
                parameter = self.__getFoilParameterList(otherModelsStr,panelName=panelName)
                # 加入到返回列表中
                # FreeCAD.Console.PrintError('\n'+str(parameter)+'\n')
                returnList.append(["Foil_Type", parameter])

            # inductor
            elif otherModelsStr.startswith(self.__KeywordInCommand.INDUCTOR):
                # 获得参数列表
                parameter = self.__getInductorParameterList(otherModelsStr)
                # 加入到返回列表中
                returnList.append(["Ind_Type", parameter])

        return returnList

def sayz(msg):
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")

    ########################## 测试 ##########################

    def test(self):
        """"""
        # self.getFileContent()
        # #
        # self.sortCommands()
        # #
        # # self.__getPhysicsParameterList()
        # #
        # # ProjectSettingList = self.__getProjectSettingList()
        # #
        # # OtherModelsParameterList = self.__getOtherModelsParameterList()
        #
        # # self.__getPanelObjectsParameterList()
        #
        #
        # print("=======================!!!!!!!!!!\n")
        # print(self.__objectStrList)
        # print("=======================!!!!!!!!!!\n")
        #
        # modlelingParamerList = self.getModlelingParameterList(self.__objectStrList)
        #
        # print("=========2222==============!!!!!!!!!!\n")
        # print(modlelingParamerList)
        # print("=========22222==============!!!!!!!!!!\n")

        # globalList = self.__getGlobalVariableList(self.__parameterStrList)
        # ModelingByM3dFile.setGlobalVariable(globalList)

        # sys = self.getCoordinateSystem()
        #
        # ModelingByM3dFile.newDoc(sys)
        # FreeCAD.Console.PrintMessage('sys')
        # FreeCAD.Console.PrintMessage(sys)
        # ModelingByM3dFile.modelingByParameter(modlelingParamerList)
        # FreeCAD.Console.PrintMessage('modlelingParamerList')
        # FreeCAD.Console.PrintMessage(modlelingParamerList)
        # return modlelingParamerList
