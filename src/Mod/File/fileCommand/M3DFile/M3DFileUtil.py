# -*- coding: UTF-8 -*-

from GetCommandByParameter import *
import File.FileCommand.TextUI.FileTextView
from File.FileCommand.M3DFile.GetParameterByCommand import getTimeDomainComputingParameter
import Modeling.Common.Tools.ModelingCommandForM3dFile
import Modeling.Common.Tools.ObjectsTools
import Modeling.Common.Tools.UnitTools
from enum import Enum
import FreeCAD
import json
import _winreg
import os



"""
根据commandManager，生成m3d文件
"""
class M3DFileUtil:

    class __Classification(Enum):
        """
        定义命令组类型
        """
        HEADER_SYSTEM = 1
        PARAMETER = 2
        DEFINE_OBJECTS = 3
        GENERATE_GRID = 4
        COMMON_PRESETS = 5
        PROPERTIES_AND_PROCESSES = 6
        SIMULATION_SETTINGS = 7
        ALL_PLOTS = 8
        ALL_PLOTS_TIMER = 9
        ALL_PLOTS_VECTOR = 10
        ALL_PLOTS_CONTOUR = 11
        ALL_PLOTS_PHASESPACE = 12
        ALL_PLOTS_OBSERVE = 13
        ALL_PLOTS_RANGE = 14
        DUMP_OPTIONS = 15
        RUN_OPTIONS = 16
        RUN = 17
        PANEL_OBJECTS = 18


    class __ManagerIndex(Enum):
        """
        定义一维列表中不同列表示的意义
        """
        # 1.命令组的唯一标识符，这里用名称，几何建模和参数建模保证其唯一性，两者之间的唯一性是隐患
        COMMANDS_ID = 0
        # 2.命令组的分类
        COMMANDS_CLASSIFICATION = 1
        # 3.命令组的内容
        COMMANDS_CONTENT = 2
        # 4.命令组的附加命令
        COMMANDS_EXTRAS = 3
        # 4.1附加命令的分类
        COMMANDS_EXTRAS_CLASSIFICATION = 0
        # 4.1附加命令的内容
        COMMANDS_EXTRAS_CONTENT = 1


    class __StrInit(Enum):
        """
        不同命令组类型对应的字符串
        """
        strHeaderSystem = "\n! ==============================================================================!\n"
        strParameter = "\n! ==============================================================================!\n" \
                       "! PARAMETER\n"
        strDefineObjects = "\n! ==============================================================================!\n" \
                           "! DEFINE OBJECTS\n"
        strPanelObjects = "\n! ==============================================================================!\n" \
                           "! PANEL OBJECTS\n"
        strGenerateGrid = "\n! ==============================================================================!\n" \
                          "! GENERATE GRID/MESH\n"
        strCommonPresets = "\n! ==============================================================================!\n" \
                           "! COMMON PRESETS\n"
        strPropertiesAndProcesses = "\n! ==============================================================================!\n" \
                                    "! PROPERTIES AND PROCESSES\n"
        strSimulationSettings = "\n! ==============================================================================!\n" \
                                "! SIMULATION SETTINGS\n"
        strAllPlots = "\n! ==============================================================================!\n" \
                      "! ALL PLOTS\n"
        strDumpOptions = "\n! ==============================================================================!\n" \
                         "! DUMP OPTIONS\n"
        strRunOptions = "\n! ==============================================================================!\n" \
                        "! RUN OPTIONS\n"
        strRun = "\n! ==============================================================================!\n" \
                 "! RUN\n"


    class CoordinateSystem(Enum):
        rectangularSys = "R"
        polarSys = "P"
        cylindricalSys = "C"


    def __init__(self, commandsManager=[], path="", coordinateSystem="R"):

        # FreeCAD.Console.PrintMessage("\n这里也执行了吗？\n")

        # 定义命令管理器，这是一个二维列表，每一个命令组的相关信息存为一个一维列表
        self.commandsManager = commandsManager

        # FreeCAD.Console.PrintMessage(commandsManager)

        # 定义不同命令组类型对应的字符串
        self.__strHeaderSystem = self.__StrInit.strHeaderSystem
        self.__strParameter = self.__StrInit.strParameter
        self.__strDefineObjects = self.__StrInit.strDefineObjects
        self.__strPanelObjects = self.__StrInit.strPanelObjects
        self.__strGenerateGrid = self.__StrInit.strGenerateGrid
        self.__strCommonPresets = self.__StrInit.strCommonPresets
        self.__strPropertiesAndProcesses = self.__StrInit.strPropertiesAndProcesses
        self.__strSimulationSettings = self.__StrInit.strSimulationSettings
        self.__strAllPlots = self.__StrInit.strAllPlots
        self.__strAllPlotsTimer = ""
        self.__strAllPlotsVector = ""
        self.__strAllPlotsContour = ""
        self.__strAllPlotsPhasespace = ""
        self.__strAllPlotsObserve = ""
        self.__strAllPlotsRange = ""
        self.__strDumpOptions = self.__StrInit.strDumpOptions
        self.__strRunOptions = self.__StrInit.strRunOptions
        self.__strRun = self.__StrInit.strRun


        # 判断路径是否存在，若不存在则新建
        if not os.path.exists(FreeCAD.clientWorkpath()):
            try: os.makedirs(FreeCAD.clientWorkpath())
            except:
                FreeCAD.Console.PrintMessage("地址无效，且无法新建，请在File下configure项修改workpath\n")
            else:
                FreeCAD.Console.PrintMessage("new FILe\n")
            # os.makedirs(FreeCAD.clientWorkpath())
            # FreeCAD.Console.PrintMessage("new FIle\n")
        # 定义有关文件的属性
        self.__fileStr = ""
        if path=="":
            self.path = FreeCAD.clientWorkpath() +FreeCAD.ActiveDocument.Label.encode("gbk") +".m3d"
            # self.path=self.path.encode("gbk")
        else:
            #utf-8编码
            try:
                # FreeCAD.Console.PrintError("path:"+str(type(path)))
                self.path=path.decode("utf-8").encode("gbk")
                # self.path=path.encode("gbk")
            except:
                #unicode编码
                try:
                    self.path=path.encode("gbk")
                except:
                    #gbk编码
                    self.path=path
        # FreeCAD.Console.PrintMessage("path333:  "+str(self.path)+"\n")
        # self.path=self.path.decode("utf-8")
        # self.path=self.path.decode("utf8")


       

        # 定义当前坐标系
        self.coordinateSystem = coordinateSystem

        """
        以下进行一些初始化的操作
        """
        # 判断是否已经新建文件
        if FreeCAD.ActiveDocument != None:
            # 获取当前文件的坐标系
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                self.coordinateSystem = self.CoordinateSystem.rectangularSys

            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                self.coordinateSystem = self.CoordinateSystem.polarSys

            elif FreeCAD.ActiveDocument.CoordinateSystem == "Cylindrical":
                self.coordinateSystem = self.CoordinateSystem.cylindricalSys

            # 初始化文件中的一些参数
            self.__magicHardCoding()


    def __getDesktop(self):
        key = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
        return _winreg.QueryValueEx(key, "Desktop")[0]


    def __magicHardCoding(self):

        self.__strHeaderSystem = self.__strHeaderSystem + \
                                 getSystemCommands(self.coordinateSystem)

        #根据坐标系初始化数值
        x1Start = x1Stop = x1Step = x2Start = x2Stop = x2Step = x3Start = x3Stop = x3Step = "检查坐标系"
        if self.coordinateSystem == self.CoordinateSystem.rectangularSys:
            x1Start = "0mm"
            x1Stop = "0mm"
            x1Step = "1mm"
            x2Start = "0mm"
            x2Stop = "0mm"
            x2Step = "1mm"
            x3Start = "0mm"
            x3Stop = "0mm"
            x3Step = "1mm"
        elif self.coordinateSystem == self.CoordinateSystem.polarSys:
            x1Start = "0mm"
            x1Stop = "0mm"
            x1Step = "1mm"
            x2Start = "0deg"
            x2Stop = "360deg"
            x2Step = "1deg"
            x3Start = "0mm"
            x3Stop = "0mm"
            x3Step = "1mm"
        elif self.coordinateSystem == self.CoordinateSystem.cylindricalSys:
            x1Start = "0mm"
            x1Stop = "0mm"
            x1Step = "1mm"
            x2Start = "0mm"
            x2Stop = "0mm"
            x2Step = "1mm"
            x3Start = "0deg"
            x3Stop = "360deg"
            x3Step = "1deg"

        self.__strRun = self.__strRun + "\nSTART ;\n" + "STOP ;\n"


    def __addOrUpdateCommands(self, id, classification, content, extras=[]):
        """
        添加或更新一个命令组
        :param id: 命令组id
        :param classification:命令组分类 
        :param content: 命令组内容
        :param extras: 附加命令组，二维列表
        :return: 
        """
        isExist = False
        for index in range(len(self.commandsManager)):
            if self.commandsManager[index][self.__ManagerIndex.COMMANDS_ID] == id:
                self.commandsManager[index] = [id, classification, content, extras]
                isExist = True
                break
        # 判断如果是注释的话，isExit保持为False,不然由于前面相同的注释会被替换
        if re.search(r"!+",id):
            isExist=False
        if not isExist:
            self.commandsManager.append([id, classification, content, extras])


    def __deleteComannds(self, id):
        """
        删除一个命令组
        :param id: 命令组id
        :return: 
        """
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_ID] == id:
                self.commandsManager.remove(commands)


    def __sortCommands(self, classification, content):
        """
        将具体的命令组分拣到不同命令组类型对应的字符串中
        
        :param classification: 命令组的分类
        :param content: 具体的命令组内容
        :return: void
        """
        if classification == self.__Classification.HEADER_SYSTEM:
            self.__strHeaderSystem = self.__strHeaderSystem + content

        if classification == self.__Classification.PARAMETER:
            self.__strParameter = self.__strParameter + content

        if classification == self.__Classification.DEFINE_OBJECTS:
            self.__strDefineObjects = self.__strDefineObjects + content

        if classification == self.__Classification.PANEL_OBJECTS:
            self.__strPanelObjects = self.__strPanelObjects + content

        if classification == self.__Classification.GENERATE_GRID:
            self.__strGenerateGrid = self.__strGenerateGrid + content

        if classification == self.__Classification.COMMON_PRESETS:
            self.__strCommonPresets = self.__strCommonPresets + content

        if classification == self.__Classification.PROPERTIES_AND_PROCESSES:
            self.__strPropertiesAndProcesses = self.__strPropertiesAndProcesses + content

        if classification == self.__Classification.SIMULATION_SETTINGS:
            self.__strSimulationSettings = self.__strSimulationSettings + content

        if classification == self.__Classification.ALL_PLOTS:
            self.__strAllPlots = self.__strAllPlots + content

        if classification == self.__Classification.ALL_PLOTS_TIMER:
            self.__strAllPlotsTimer = self.__strAllPlotsTimer + content

        if classification == self.__Classification.ALL_PLOTS_VECTOR:
            self.__strAllPlotsVector = self.__strAllPlotsVector + content

        if classification == self.__Classification.ALL_PLOTS_CONTOUR:
            self.__strAllPlotsContour = self.__strAllPlotsContour + content

        if classification == self.__Classification.ALL_PLOTS_PHASESPACE:
            self.__strAllPlotsPhasespace = self.__strAllPlotsPhasespace + content

        if classification == self.__Classification.ALL_PLOTS_OBSERVE:
            self.__strAllPlotsObserve = self.__strAllPlotsObserve + content

        if classification == self.__Classification.ALL_PLOTS_RANGE:
            self.__strAllPlotsRange = self.__strAllPlotsRange + content

        if classification == self.__Classification.DUMP_OPTIONS:
            self.__strDumpOptions = self.__strDumpOptions + content

        if classification == self.__Classification.RUN_OPTIONS:
            self.__strRunOptions = self.__strRunOptions + content

        if classification == self.__Classification.RUN:
            self.__strRun = self.__strRun + content


    def __refreshM3DFileStr(self):
        """
        根据commandManager获得m3d文件的字符串

        :param commandManager: 用于管理所有命令组的变量
        :return: void
        """
        # 分拣commandsManager中的命令组
        # FreeCAD.Console.PrintMessage(self.commandsManager)
        for commands in self.commandsManager:
            if len(commands) >= 3:
                # 处理基本命令组
                self.__sortCommands(commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION],
                                    commands[self.__ManagerIndex.COMMANDS_CONTENT])
                # 处理附加命令组
                if len(commands[self.__ManagerIndex.COMMANDS_EXTRAS]) != 0:
                    for extraCommands in commands[self.__ManagerIndex.COMMANDS_EXTRAS]:
                        self.__sortCommands(extraCommands[self.__ManagerIndex.COMMANDS_EXTRAS_CLASSIFICATION],
                                            extraCommands[self.__ManagerIndex.COMMANDS_EXTRAS_CONTENT])
            else:
                return "ERROR: 请检查commandsManager中的命令组是否存入必要信息（唯一标识、分类、内容）"

        # print "==========================refreshM3DFileStr=============================="
        # print self.__strHeaderSystem
        # print self.__strParameter
        # print self.__strDefineObjects
        # print self.__strPanelObjects
        # print self.__strGenerateGrid
        # print self.__strHeaderSystem
        # print self.__strParameter
        # print self.__strDefineObjects
        # print self.__strPanelObjects
        # print self.__strGenerateGrid
        # print self.__strCommonPresets
        # print self.__strPropertiesAndProcesses
        # print self.__strAllPlots
        # print self.__strAllPlotsTimer
        # print self.__strAllPlotsVector
        # print self.__strAllPlotsContour
        # print self.__strAllPlotsPhasespace
        # print self.__strAllPlotsObserve
        # print self.__strAllPlotsRange
        # print self.__strDumpOptions
        # print self.__strRunOptions
        # print self.__strRun

        # 生成文本字符串
        self.__fileStr = self.__strHeaderSystem + self.__strParameter + self.__strDefineObjects + self.__strPanelObjects + \
                         self.__strGenerateGrid + self.__strCommonPresets + self.__strPropertiesAndProcesses + \
                         self.__strSimulationSettings + self.__strAllPlots + \
                         self.__strAllPlotsTimer + self.__strAllPlotsVector + self.__strAllPlotsContour + \
                         self.__strAllPlotsPhasespace + self.__strAllPlotsObserve + self.__strAllPlotsRange + \
                         self.__strDumpOptions + self.__strRunOptions + self.__strRun

        return self.__fileStr


    def __resetCommandsStr(self):
        """
        重置不同命令组类型对应的字符串
        :return: 
        """
        self.__strHeaderSystem = self.__StrInit.strHeaderSystem
        self.__strParameter = self.__StrInit.strParameter
        self.__strDefineObjects = self.__StrInit.strDefineObjects
        self.__strPanelObjects = self.__StrInit.strPanelObjects
        self.__strGenerateGrid = self.__StrInit.strGenerateGrid
        self.__strCommonPresets = self.__StrInit.strCommonPresets
        self.__strPropertiesAndProcesses = self.__StrInit.strPropertiesAndProcesses
        self.__strSimulationSettings = self.__StrInit.strSimulationSettings
        self.__strAllPlots = self.__StrInit.strAllPlots
        self.__strAllPlotsTimer = ""
        self.__strAllPlotsVector = ""
        self.__strAllPlotsContour = ""
        self.__strAllPlotsPhasespace = ""
        self.__strAllPlotsObserve = ""
        self.__strAllPlotsRange = ""
        self.__strDumpOptions = self.__StrInit.strDumpOptions
        self.__strRunOptions = self.__StrInit.strRunOptions
        self.__strRun = self.__StrInit.strRun

        # 添加坐标系信息
        self.__magicHardCoding()


    def __getLatestManagerWithPhysics(self):
        # 重置manager
        self.commandsManager = []

        # 更新物理部分的Comannds，实则修改manager
        self.__updatePhysicsInfo()


    def __getLatestManagerWithEngineering(self):
        # 重置manager
        self.commandsManager = []

        # 更新物理部分的Comannds，实则修改manager
        self.__updateEngineeringInfo()


    def __getLatestManagerWithModeling(self):
        # 重置manager
        self.commandsManager = []

        # 更新物理部分的Comannds，实则修改manager
        self.__updateModelingInfo()


    def getLatestM3DFileStr(self):
        # 重置各命令组对应字符串，防止多次调用时异常
        # FreeCAD.Console.PrintMessage("\n断点2\n")
        self.__resetCommandsStr()

        # 重置manager
        self.commandsManager = []

        # 更新自定义参数的Comannds，实则修改manager
        self.__updateParameterInfo()

        # 更新几何部分的Comannds，实则修改manager
        self.__updateModelingInfo()

        # 更新物理部分的Comannds，实则修改manager
        self.__updatePhysicsInfo()

        # 更新工程部分的Comannds，实则修改manager
        self.__updateEngineeringInfo()


        # 重新生成m3d文件的字符串
        self.__refreshM3DFileStr()

        # 返回文件字符串
        return self.__fileStr


    def writeToFile(self, isRefresh=False):

        if not isRefresh:
            # 重新生成m3d文件的字符串
            # FreeCAD.Console.PrintError('\n执行生成m3d之前\n')
            self.getLatestM3DFileStr()
            # FreeCAD.Console.PrintError('\n执行生成m3d之后\n')

        # 输出到文件
        fo = open(self.path, "w+")
        str = self.__fileStr
        fo.write(str.encode("UTF-8"))
        fo.close()



    def deleteFile(self):
        """删除m3d文件"""
        # 如果文件存在
        if os.path.exists(self.path):
            # 删除文件
            os.remove(self.path)
        else:
            # 则返回文件不存在
            sayz("no such file")


    def saveCommandsManager(self):
        # 将commandsManager转化为json并保存到文件对应的全局变量中
        FreeCAD.ActiveDocument.Company = json.dumps(self.commandsManager)


    ########################### 以下是为任务控制部分提供的获取不同类型图像个数的接口##########################

    def getContourGraphNum(self):

        self.__getLatestManagerWithPhysics()

        num = 0
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_CONTOUR:
                num = num + 1
        return num


    def getVectorGraphNum(self):

        self.__getLatestManagerWithPhysics()

        num = 0
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_VECTOR:
                num = num + 1
        return num


    def getPhasespaceGraphNum(self):

        self.__getLatestManagerWithPhysics()

        num = 0
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_PHASESPACE:
                num = num + 1
        return num


    def getObserveGraphNum(self):

        self.__getLatestManagerWithPhysics()

        num = 0
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_OBSERVE:
                #这里计数按照命令中分号个数+“FFT”的个数，“FFT”记为两个
                thisNum=commands[self.__ManagerIndex.COMMANDS_CONTENT].count(";")+commands[self.__ManagerIndex.COMMANDS_CONTENT].count("FFT")
                FreeCAD.Console.PrintMessage("COMMAND OBSERVER :   "+ commands[self.__ManagerIndex.COMMANDS_CONTENT]+ ";;;;;  "+str(commands[self.__ManagerIndex.COMMANDS_CONTENT].count(";"))+"FFT  :"+str(commands[self.__ManagerIndex.COMMANDS_CONTENT].count("FFT"))+"\n")
                num = num + thisNum
        return num


    def getRangeGraphNum(self):

        self.__getLatestManagerWithPhysics()

        num = 0
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_RANGE:
                num = num + 1
        return num


    def getIterationTime(self):

        self.__getLatestManagerWithEngineering()

        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.SIMULATION_SETTINGS:
                content = commands[self.__ManagerIndex.COMMANDS_CONTENT]
                return getTimeDomainComputingParameter(content)[0]


    ########################### 以下是为可视化部分提供的获取图像对应命令的接口##########################

    def getContourGraphName(self):

        self.__getLatestManagerWithPhysics()

        returnList = []
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_CONTOUR:
                content = commands[self.__ManagerIndex.COMMANDS_CONTENT]

                # 判断是否是SHADE类型
                if content[len(content)-7:len(content)-2] == "SHADE":
                    isShade = True
                else:
                    isShade = False

                returnList.append([content,isShade])
        return returnList


    def getVectorGraphName(self):

        self.__getLatestManagerWithPhysics()

        returnList = []
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_VECTOR:
                returnList.append(commands[self.__ManagerIndex.COMMANDS_CONTENT])
        return returnList


    def getPhasespaceGraphName(self):

        self.__getLatestManagerWithPhysics()

        returnList = []
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_PHASESPACE:
                returnList.append(commands[self.__ManagerIndex.COMMANDS_CONTENT])
        return returnList


    def getObserveGraphName(self):

        self.__getLatestManagerWithPhysics()

        returnList = []
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_OBSERVE:
                returnList.append(commands[self.__ManagerIndex.COMMANDS_CONTENT])
        return returnList


    def getRangeGraphName(self):

        self.__getLatestManagerWithPhysics()

        returnList = []
        for commands in self.commandsManager:
            if commands[self.__ManagerIndex.COMMANDS_CLASSIFICATION] == self.__Classification.ALL_PLOTS_RANGE:
                returnList.append(commands[self.__ManagerIndex.COMMANDS_CONTENT])
        return returnList


    def getStructNameStr(self):
        self.__getLatestManagerWithModeling()
        self.__refreshM3DFileStr()
        return self.__strPropertiesAndProcesses
    ######################################### 以下是从M3DFileEditor工作台调用的接口#####################
    import re
    def getPoltNameForM3dFileEditor(self):
        resultList=[]
        CONTOURList=[]
        VECTORList=[]
        PHASESPACEList=[]
        OBSERVEList=[]
        RANGEList=[]
        StructsName=""
        nDURATION=0
        fo=open(self.path,"r")
        text=""
        #用一个string数组来存放临时的m3d行，以便后面找对应的变量时用
        textList=[]
        for line in fo.readlines():
            # 去掉开头的空格
            text=text+line.strip()
            #append
            textList.append(text)
            if not text.startswith("!"):
                if not text.endswith(";"):
                    text=text+" "
                    pass
                else:
                    #upper()是因为关键字不区分大小写
                    #是否以CONTOUR开头
                    if text.upper().startswith("CONTOUR "):
                        if text.upper().endswith("SHADE;"):
                            CONTOURList.append([text,True])
                        else:
                            CONTOURList.append([text,False])
                        pass
                    #是否以VECTOR开头
                    elif text.upper().startswith("VECTOR "):
                        VECTORList.append(text)
                        pass
                    elif text.upper().startswith("PHASESPACE "):
                        PHASESPACEList.append(text)
                        pass
                    elif text.upper().startswith("OBSERVE "):
                        OBSERVEList.append(text)
                        pass
                    elif text.upper().startswith("RANGE "):
                        RANGEList.append(text)
                        pass
                    elif text.upper().startswith("CONDUCTANCE ") or\
                         text.upper().startswith("DIELECTRIC ") or \
                         text.upper().startswith("CONDUCTOR ") or\
                         text.upper().startswith("VOID "):
                        StructsName=StructsName+text+"\n"
                        pass
                    elif text.upper().startswith("DURATION "):
                        FreeCAD.Console.PrintMessage("DURATION\n")
                        nums=re.findall(r"\d+",text)
                        nDURATION=""
                        if len(nums)>0:
                            nDURATION=int(nums[0])
                        else:
                            try:
                                # @fubiao 这里可能用的是参数
                                nDURATION=text.split(" ")[1].replace(";","")
                                param=""
                                #找到这个参量对应的等式
                                for paramLine in textList:
                                    params=re.findall(r"\b"+nDURATION+"[^;]*[;]",paramLine,re.I)
                                    if len(params)>0:
                                        param=params[0]
                                        nDURATION=Modeling.Common.Tools.UnitTools.turnIterTime("",param)
                                        break
                            except:
                                FreeCAD.Console.PrintError("\nM3DFileUtil:getPoltNameForM3dFileEditor\n")
                        
                        pass
            text=""
        resultList=[CONTOURList,VECTORList,PHASESPACEList,OBSERVEList,RANGEList,StructsName,nDURATION]
        return resultList
        pass


    def nNumOfContourGraphNameForM3dFileEditor(self):
        pass


    def nNumOfVectorGraphNameForM3dFileEditor(self):
        pass


    def nNumOfPhasespaceGraphNameForM3dFileEditor(self):
        pass


    def nNumOfObserveGraphNameForM3dFileEditor(self):
        pass


    def nNumOfRangeGraphNameForM3dFileEditor(self):
        pass


    def getStructNameStrForM3dFileEditor(self):
        pass


    ########################## 以下为根据几何建模或参数建模更新m3d文件v2 ################################
    def __updateParameterInfo(self):
        infoList = Modeling.Common.Tools.ModelingCommandForM3dFile.getGlobalVariable()

        # FreeCAD.Console.PrintMessage("\n单位从这里输出吗？\n")
        # FreeCAD.Console.PrintMessage(infoList)
        # FreeCAD.Console.PrintMessage("\n综上\n")

        for info in infoList:
            self.updateParameter(info[0], info[1])


    def __updateModelingInfo(self):
        infoList = Modeling.Common.Tools.ModelingCommandForM3dFile.getModelingCommands()
        # print "modelingInfo"
        # print infoList
        INFO_CLASSIFICATION = 0
        INFO_PARAMETER = 1
        # FreeCAD.Console.PrintError('\n已经进入更新几何部分m3d函数\n')
        for info in infoList:
            # FreeCAD.Console.PrintError('\n进入循环还是生成m3d\n')
            # 点
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Point:
                self.updatePonitCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                         info[INFO_PARAMETER][2], info[INFO_PARAMETER][3],
                                         info[INFO_PARAMETER][4], info[INFO_PARAMETER][5],
                                         info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                         info[INFO_PARAMETER][8], info[INFO_PARAMETER][9],
                                         info[INFO_PARAMETER][10], info[INFO_PARAMETER][11],
                                         info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                         info[INFO_PARAMETER][14], info[INFO_PARAMETER][15],
                                         info[INFO_PARAMETER][16])

            # 线(Line_Conformal)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Line_Conformal:
                self.updateLineCommands(info[INFO_PARAMETER][0], Line.Type.conformal,
                                        info[INFO_PARAMETER][2], info[INFO_PARAMETER][3],
                                        info[INFO_PARAMETER][4], info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8], info[INFO_PARAMETER][9],
                                        info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18])

            # 线(Line_Oblique)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Line_Oblique:
                self.updateObliqueLineCommands(info[INFO_PARAMETER][0],info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2], info[INFO_PARAMETER][3],
                                        info[INFO_PARAMETER][4], info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8], info[INFO_PARAMETER][9],
                                        info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18])

            # 面(Area_Conformal)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Area_Conformal:
                self.updateConformalAreaCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][2], info[INFO_PARAMETER][3],
                                        info[INFO_PARAMETER][4], info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8], info[INFO_PARAMETER][9],
                                        info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18])

            # 面(Area_Rectangular)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Area_Rectangular:
                self.updateRectangularAreaCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][2], info[INFO_PARAMETER][3],
                                        info[INFO_PARAMETER][4], info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8], info[INFO_PARAMETER][9],
                                        info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18])

            # 面(Area_Polygonal)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Area_Polygonal:
                self.updatePolygonalAreaCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8],info[INFO_PARAMETER][9],
                                        info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16])

            # 体(Vol_Conformal 正投影体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Conformal:
                # FreeCAD.Console.PrintError('\n正投影体获取参数并进入判断语句\n')
                self.updateConformalVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9],
                                        info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18])

            # 体(Vol_SpecialCone 圆锥或圆台)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_SpecialCone:
                self.updateConeVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20])

            # 体(Vol_Cylinder 圆柱)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Cylinder:
                self.updateCylindricalVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11],info[INFO_PARAMETER][12],
                                        info[INFO_PARAMETER][13],info[INFO_PARAMETER][14],
                                        info[INFO_PARAMETER][15],info[INFO_PARAMETER][16],
                                        info[INFO_PARAMETER][17],info[INFO_PARAMETER][18],
                                        info[INFO_PARAMETER][19])

            # 体(Vol_Annular 环形体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Annular:
                self.updateAnnularVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20])

            # 体(Vol_Annular_Section 部分环形体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Annular_Section:
                self.updateAnnularSectionVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11], info[INFO_PARAMETER][12],
                                        info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20])

            # 体(Vol_Parallelepipedal 平行六面体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Parallelepipedal:
                self.updateParallelepipedalVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                                        info[INFO_PARAMETER][2],
                                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                                        info[INFO_PARAMETER][11],
                                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                                        info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                                        info[INFO_PARAMETER][20])

            # 体(Vol_Spherical 球体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Spherical:
                self.updateSphericalVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                                        info[INFO_PARAMETER][2],
                                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                                        info[INFO_PARAMETER][9],
                                                        info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                                        info[INFO_PARAMETER][18])

            # 体(Vol_Wedge 楔形体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Wedge:
                self.updateWedgeVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11], info[INFO_PARAMETER][12],
                                        info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20],info[INFO_PARAMETER][21],
                                        info[INFO_PARAMETER][22])

            # 体(Vol_Pyramid 棱锥体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Pyramid:
                self.updatePyramidVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11], info[INFO_PARAMETER][12],
                                        info[INFO_PARAMETER][13],info[INFO_PARAMETER][14],
                                        info[INFO_PARAMETER][15],info[INFO_PARAMETER][16],
                                        info[INFO_PARAMETER][17],info[INFO_PARAMETER][18],
                                        info[INFO_PARAMETER][19],info[INFO_PARAMETER][20],
                                        info[INFO_PARAMETER][21])

            # 体(Vol_Tetrahedron 四面体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Tetrahedron:
                self.updateTetrahedronVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20])

            # 体(Vol_Rhombus菱形体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Rhombus:
                self.updateRhombusVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                                         info[INFO_PARAMETER][2],
                                                         info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                                         info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                                         info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                                         info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                                         info[INFO_PARAMETER][11], info[INFO_PARAMETER][12],
                                                         info[INFO_PARAMETER][13], info[INFO_PARAMETER][14],
                                                         info[INFO_PARAMETER][15],
                                                         info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                                         info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                                         info[INFO_PARAMETER][20],info[INFO_PARAMETER][21],
                                                         info[INFO_PARAMETER][22],info[INFO_PARAMETER][23],
                                                         info[INFO_PARAMETER][24])

            # 体(Vol_Toroidal_Section部分圆环体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Toroidal_Section:
                self.updateToroidalSectionVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1], info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                        info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11], info[INFO_PARAMETER][12],
                                        info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18],info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20],info[INFO_PARAMETER][21],
                                        info[INFO_PARAMETER][22])

            # 体(Extruded挤出体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Extruded:
                self.updateExtrudedVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                                         info[INFO_PARAMETER][2],
                                                         info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                                         info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                                         info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                                         info[INFO_PARAMETER][9],
                                                         info[INFO_PARAMETER][10],info[INFO_PARAMETER][11],
                                                        info[INFO_PARAMETER][12],info[INFO_PARAMETER][13],
                                                        info[INFO_PARAMETER][14],info[INFO_PARAMETER][15],
                                                        info[INFO_PARAMETER][16],info[INFO_PARAMETER][17],
                                                        info[INFO_PARAMETER][18])

            # 体(Vol_Helical螺旋体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Helical:
                self.updateHelicalVolumeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                                         info[INFO_PARAMETER][2],
                                                         info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                                         info[INFO_PARAMETER][5], info[INFO_PARAMETER][6],
                                                         info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                                         info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                                         info[INFO_PARAMETER][11], info[INFO_PARAMETER][12],
                                                         info[INFO_PARAMETER][13], info[INFO_PARAMETER][14],
                                                         info[INFO_PARAMETER][15],info[INFO_PARAMETER][16],
                                                         info[INFO_PARAMETER][17],info[INFO_PARAMETER][18],
                                                         info[INFO_PARAMETER][19],info[INFO_PARAMETER][20],
                                                         info[INFO_PARAMETER][21],info[INFO_PARAMETER][22],
                                                         info[INFO_PARAMETER][23])
                
            # 体(阵列体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Array:
                self.updateArrayVolumeCommands(info[INFO_PARAMETER], info[2])
            # 体(Vol_ParamArray参数阵列体)
            if info[INFO_CLASSIFICATION] == Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_ParamArray:
                self.updateParamArrayVolumeCommands(info[INFO_PARAMETER][0], 
                                                         info[INFO_PARAMETER][1],
                                                         info[INFO_PARAMETER][2],info[INFO_PARAMETER][3], 
                                                         info[INFO_PARAMETER][4],
                                                         info[INFO_PARAMETER][5], 
                                                         info[INFO_PARAMETER][6],info[INFO_PARAMETER][7], info[INFO_PARAMETER][8],
                                                         info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],info[INFO_PARAMETER][11])
            #体（函数体）
            elif info[INFO_CLASSIFICATION]==Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Function:
                self.updateFunctionVolumeCommands(info[INFO_PARAMETER][0],
                                                    info[INFO_PARAMETER][1],
                                                    info[INFO_PARAMETER][2],
                                                    info[INFO_PARAMETER][3],
                                                    info[INFO_PARAMETER][4],
                                                    info[INFO_PARAMETER][5],
                                                    info[INFO_PARAMETER][6],
                                                    info[INFO_PARAMETER][7],
                                                    info[INFO_PARAMETER][8],
                                                    info[INFO_PARAMETER][9],
                                                    info[INFO_PARAMETER][10],
                                                    info[INFO_PARAMETER][11],info[INFO_PARAMETER][12],
                                                    info[INFO_PARAMETER][13],info[INFO_PARAMETER][14],
                                                    info[INFO_PARAMETER][15],info[INFO_PARAMETER][16],
                                                    info[INFO_PARAMETER][17],info[INFO_PARAMETER][18],
                                                    info[INFO_PARAMETER][19])
            elif info[INFO_CLASSIFICATION]==Modeling.Common.Tools.ObjectsTools.ObjectType.Vol_Revolution:
                self.updataRotateVolumeCommands((info[INFO_PARAMETER][0]),
                                                info[INFO_PARAMETER][1],
                                                info[INFO_PARAMETER][2],
                                                info[INFO_PARAMETER][3],
                                                info[INFO_PARAMETER][4],
                                                info[INFO_PARAMETER][5],
                                                info[INFO_PARAMETER][6],
                                                info[INFO_PARAMETER][7],
                                                info[INFO_PARAMETER][8],
                                                info[INFO_PARAMETER][9],
                                                info[INFO_PARAMETER][10])
        # 在体创建的最后面添加新的 MARK 命令@lzg 注意此mark非彼mark！！！
        from Physics.PhysicsCommand.DlgData import getDlgData
        infoList = getDlgData()

        INFO_CLASSIFICATION = 0
        INFO_PARAMETER = 1
        
        for info in infoList:
            if info[INFO_CLASSIFICATION] == "Mark_Type":
                self.updateNewMarkCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3],
                                        info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6])
            pass
    def refreshjson(self):
        '''
        bug：创建一根线，Ind使用这根线，修改线的坐标但是m3d不会更新坐标信息\n
        此函数是为了解决类似的bug\n
        直接修改json的坐标数据@lzg
        '''
        from Physics import PhysicsCommand
        from Modeling.Common.Tools import DocumentTools
        #json格式数据需要保持原有顺序输出
        from collections import OrderedDict
        REFRESH_JSON = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        # 这个list用来存储需要更新的json，有新的需要更新的部分添加在下面的for循环中
        list_need_refresh = []
        for i in REFRESH_JSON.keys():
            if REFRESH_JSON[i]['Dlg_Type'] == 'Ind_Type':
                list_need_refresh.append(i)
        for x in list_need_refresh:
            if REFRESH_JSON[x]['Orthogonal_projection_surface'] != '未指定':
                modelData = DocumentTools.getValueOfLineObjByLable(REFRESH_JSON[x]['Orthogonal_projection_surface'])
                REFRESH_JSON[x]['start_R'] = modelData[1]
                REFRESH_JSON[x]['start_Y'] = modelData[2]
                REFRESH_JSON[x]['start_Z'] = modelData[3]
                REFRESH_JSON[x]['end_R'] = modelData[4]
                REFRESH_JSON[x]['end_Y'] = modelData[5]
                REFRESH_JSON[x]['end_Z'] = modelData[6]
        FreeCAD.ActiveDocument.Begin = json.dumps(REFRESH_JSON)
        pass

    def __updatePhysicsInfo(self):
        try:
            self.refreshjson()
        except:
            FreeCAD.Console.PrintMessage("\n刷新json失败！！！")
            pass
        from Physics.PhysicsCommand.DlgData import getDlgData
        infoList = getDlgData()
        # print "PhysicsInfo"
        # print infoList
        INFO_CLASSIFICATION = 0
        INFO_PARAMETER = 1

        # FreeCAD.Console.PrintMessage("\ninfo里有什么？\n")
        for info in infoList:
            # FreeCAD.Console.PrintMessage("")
            # FreeCAD.Console.PrintMessage(info)
            # FreeCAD.Console.PrintMessage("\n")
            # port
            if info[INFO_CLASSIFICATION] == "Port_Type":
                # FreeCAD.Console.PrintError(str(info[INFO_PARAMETER]))
                # FreeCAD.Console.PrintError('\n'+str(info[INFO_PARAMETER][0])+'\n')
                self.updatePortCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11],
                                        info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                        info[INFO_PARAMETER][14],
                                        info[INFO_PARAMETER][15], info[INFO_PARAMETER][16],
                                        info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20],
                                        info[INFO_PARAMETER][21], info[INFO_PARAMETER][22],
                                        info[INFO_PARAMETER][23],
                                        info[INFO_PARAMETER][24], info[INFO_PARAMETER][25],
                                        info[INFO_PARAMETER][26],
                                        info[INFO_PARAMETER][27], info[INFO_PARAMETER][28],
                                        info[INFO_PARAMETER][29],
                                        info[INFO_PARAMETER][30], info[INFO_PARAMETER][31],
                                        info[INFO_PARAMETER][32],
                                        info[INFO_PARAMETER][33], info[INFO_PARAMETER][34],
                                        info[INFO_PARAMETER][35],
                                        info[INFO_PARAMETER][36], info[INFO_PARAMETER][37],
                                        info[INFO_PARAMETER][38],
                                        info[INFO_PARAMETER][39],info[INFO_PARAMETER][40],
                                        info[INFO_PARAMETER][41]
                                        )
            # EmSE
            if info[INFO_CLASSIFICATION] == "EmSE_Type":
                # FreeCAD.Console.PrintError("\n进入加载EmSE的数据过程")
                # FreeCAD.Console.PrintError("\n"+str(info[INFO_PARAMETER]))
                self.updateEmSECommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                        info[INFO_PARAMETER][11], info[INFO_PARAMETER][12],
                                        info[INFO_PARAMETER][13], info[INFO_PARAMETER][14],
                                        info[INFO_PARAMETER][15],
                                        info[INFO_PARAMETER][16], info[INFO_PARAMETER][17],
                                        info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                        info[INFO_PARAMETER][20])
                FreeCAD.Console.PrintError("\n执行完加载EmSE数据部分")
            # Merge
            if info[INFO_CLASSIFICATION] == "Merge_Type":
                # FreeCAD.Console.PrintError("\n进入加载Merge的数据过程")
                self.updateMergeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3])
                FreeCAD.Console.PrintError("\n执行完merge的数据过程")
            # Populate
            if info[INFO_CLASSIFICATION] == "Populate_Type":
                # FreeCAD.Console.PrintError("\n进入加载Populate的数据过程")
                self.updatePopulateCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                        info[INFO_PARAMETER][5],
                                        info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                        info[INFO_PARAMETER][8],
                                        info[INFO_PARAMETER][9], info[INFO_PARAMETER][10])
                FreeCAD.Console.PrintError("\n执行完加载Populate的数据过程")
            # Gasgas
            if info[INFO_CLASSIFICATION] == "Gasgas_Type":
                self.updataGasgasCommands(info[INFO_PARAMETER][0],info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3])
                FreeCAD.Console.PrintError("\n执行完加载Gasgas的数据过程")
            # Species
            if info[INFO_CLASSIFICATION] == "Species_Type":
                # FreeCAD.Console.PrintError("\n进入Species的数据过程")
                self.updataSpeciesCommands(info[INFO_PARAMETER][0],info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][3])
                # FreeCAD.Console.PrintError("\n执行完加载Species的数据过程")
            # free
            if info[INFO_CLASSIFICATION] == "Free_Type":
                if info[INFO_PARAMETER][1] == u"未指定":
                    isAppointArea = False
                else:
                    isAppointArea = True

                if info[INFO_PARAMETER][4] == u"R":
                    xType = "X1"
                elif info[INFO_PARAMETER][4] == u"theta":
                    xType = "X2"
                elif info[INFO_PARAMETER][4] == u"Z":
                    xType = "X3"
                else:
                    xType = "error"

                self.updateFreeSpaceCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][5],
                                             xType,
                                             info[INFO_PARAMETER][6],
                                             info[INFO_PARAMETER][7][0], info[INFO_PARAMETER][7][1],
                                             isAppointArea, info[INFO_PARAMETER][1],
                                             info[INFO_PARAMETER][2], info[INFO_PARAMETER][3],
                                             info[INFO_PARAMETER][8], info[INFO_PARAMETER][9],
                                             info[INFO_PARAMETER][10], info[INFO_PARAMETER][11],
                                             info[INFO_PARAMETER][12], info[INFO_PARAMETER][13])

            # sym
            if info[INFO_CLASSIFICATION] == "Sym_Type":
                if info[INFO_PARAMETER][6][0] == u"轴对称":
                    type = "AXIAL"
                elif info[INFO_PARAMETER][6][0] == u"镜像对称":
                    type = "MIRROR"
                elif info[INFO_PARAMETER][6][0] == u"周期对称":
                    type = "PERIODIC"
                else:
                    type = "error"

                trendType = "error"
                if info[INFO_PARAMETER][5][0] == True:
                    trendType = "NEGATIVE"
                if info[INFO_PARAMETER][5][1] == True:
                    trendType = "POSITIVE"

                if info[INFO_PARAMETER][1] == u"未指定":
                    isAppointArea = False
                else:
                    isAppointArea = True

                self.updateSymmetryCommands(info[INFO_PARAMETER][0], type, trendType,
                                            isAppointArea, info[INFO_PARAMETER][1],
                                            info[INFO_PARAMETER][2], info[INFO_PARAMETER][3],
                                            info[INFO_PARAMETER][4],
                                            info[INFO_PARAMETER][6][1],
                                            info[INFO_PARAMETER][7],
                                            info[INFO_PARAMETER][8][0],
                                            info[INFO_PARAMETER][8][1], info[INFO_PARAMETER][8][2],
                                            info[INFO_PARAMETER][9][0],
                                            info[INFO_PARAMETER][9][1], info[INFO_PARAMETER][9][2])

            # Exp
            if info[INFO_CLASSIFICATION] == "ExP_Type":
                self.updateDriverCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                [info[INFO_PARAMETER][2][0], info[INFO_PARAMETER][2][1], info[INFO_PARAMETER][2][2]],
                                [info[INFO_PARAMETER][2][3], info[INFO_PARAMETER][2][4], info[INFO_PARAMETER][2][5]],
                                            info[INFO_PARAMETER][3],
                                            info[INFO_PARAMETER][4],
                                            info[INFO_PARAMETER][5])

            # Foil
            if info[INFO_CLASSIFICATION] == "Foil_Type":
                self.updateFoilCommands(info[INFO_PARAMETER][0],
                                        info[INFO_PARAMETER][1],
                                        [info[INFO_PARAMETER][2][0], info[INFO_PARAMETER][2][1],
                                         info[INFO_PARAMETER][2][2]],
                                        [info[INFO_PARAMETER][2][3], info[INFO_PARAMETER][2][4],
                                         info[INFO_PARAMETER][2][5]],
                                        info[INFO_PARAMETER][3],
                                        info[INFO_PARAMETER][4][0],
                                        info[INFO_PARAMETER][4][1],
                                        info[INFO_PARAMETER][4][2],
                                        info[INFO_PARAMETER][4][3])

            # Inductor
            if info[INFO_CLASSIFICATION] == "Ind_Type":
                self.updateInductorCommands(info[INFO_PARAMETER][0],
                                        info[INFO_PARAMETER][1],
                                        [info[INFO_PARAMETER][2][0], info[INFO_PARAMETER][2][1],
                                         info[INFO_PARAMETER][2][2]],
                                        [info[INFO_PARAMETER][2][3], info[INFO_PARAMETER][2][4],
                                         info[INFO_PARAMETER][2][5]],
                                        info[INFO_PARAMETER][3],
                                        info[INFO_PARAMETER][4][0],
                                        info[INFO_PARAMETER][4][1])

            # EmB
            if info[INFO_CLASSIFICATION] == "EMB_Type":
                self.updateEmBCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                       info[INFO_PARAMETER][2],
                                       info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                       info[INFO_PARAMETER][5],
                                       info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                       info[INFO_PARAMETER][8],
                                       info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                       info[INFO_PARAMETER][11],
                                       info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                       info[INFO_PARAMETER][14],
                                       info[INFO_PARAMETER][15], info[INFO_PARAMETER][16],
                                       info[INFO_PARAMETER][17],
                                       info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                       info[INFO_PARAMETER][20],
                                       info[INFO_PARAMETER][21], info[INFO_PARAMETER][22],
                                       info[INFO_PARAMETER][23],
                                       info[INFO_PARAMETER][24])

            # EmE
            if info[INFO_CLASSIFICATION] == "EME_Type":
                self.updateEmECommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                       info[INFO_PARAMETER][2],
                                       info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                       info[INFO_PARAMETER][5],
                                       info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                       info[INFO_PARAMETER][8],
                                       info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                       info[INFO_PARAMETER][11],
                                       info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                       info[INFO_PARAMETER][14],
                                       info[INFO_PARAMETER][15], info[INFO_PARAMETER][16],
                                       info[INFO_PARAMETER][17],
                                       info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                       info[INFO_PARAMETER][20],
                                       info[INFO_PARAMETER][21], info[INFO_PARAMETER][22],
                                       info[INFO_PARAMETER][23],
                                       info[INFO_PARAMETER][24], info[INFO_PARAMETER][25],
                                       info[INFO_PARAMETER][26],
                                       info[INFO_PARAMETER][27], info[INFO_PARAMETER][28],
                                       info[INFO_PARAMETER][29],
                                       info[INFO_PARAMETER][30])

            # EmG
            if info[INFO_CLASSIFICATION] == "EMG_Type":
                self.updateEmGCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                       info[INFO_PARAMETER][2],
                                       info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                       info[INFO_PARAMETER][5],
                                       info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                       info[INFO_PARAMETER][8],
                                       info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                       info[INFO_PARAMETER][11],
                                       info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                       info[INFO_PARAMETER][14],
                                       info[INFO_PARAMETER][15], info[INFO_PARAMETER][16],
                                       info[INFO_PARAMETER][17],
                                       info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                       info[INFO_PARAMETER][20],
                                       info[INFO_PARAMETER][21], info[INFO_PARAMETER][22],
                                       info[INFO_PARAMETER][23],
                                       info[INFO_PARAMETER][24], info[INFO_PARAMETER][25],
                                       info[INFO_PARAMETER][26],
                                       info[INFO_PARAMETER][27], info[INFO_PARAMETER][28],
                                       info[INFO_PARAMETER][29],
                                       info[INFO_PARAMETER][30], info[INFO_PARAMETER][31])

            # EmH
            if info[INFO_CLASSIFICATION] == "EMH_Type":
                self.updateEmHCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                       info[INFO_PARAMETER][2],
                                       info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                       info[INFO_PARAMETER][5],
                                       info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                       info[INFO_PARAMETER][8],
                                       info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                       info[INFO_PARAMETER][11],
                                       info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                       info[INFO_PARAMETER][14],
                                       info[INFO_PARAMETER][15], info[INFO_PARAMETER][16],
                                       info[INFO_PARAMETER][17],
                                       info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                       info[INFO_PARAMETER][20],
                                       info[INFO_PARAMETER][21], info[INFO_PARAMETER][22],
                                       info[INFO_PARAMETER][23],
                                       info[INFO_PARAMETER][24], info[INFO_PARAMETER][25])

            # EmT
            if info[INFO_CLASSIFICATION] == "EMT_Type":
                self.updateEmTCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                       info[INFO_PARAMETER][2],
                                       info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                       info[INFO_PARAMETER][5],
                                       info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                       info[INFO_PARAMETER][8],
                                       info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                       info[INFO_PARAMETER][11],
                                       info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                       info[INFO_PARAMETER][14],
                                       info[INFO_PARAMETER][15], info[INFO_PARAMETER][16],
                                       info[INFO_PARAMETER][17],
                                       info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                       info[INFO_PARAMETER][20],
                                       info[INFO_PARAMETER][21], info[INFO_PARAMETER][22],
                                       info[INFO_PARAMETER][23],
                                       info[INFO_PARAMETER][24])

            # Cntr
            if info[INFO_CLASSIFICATION] == "Cntr_Type":
                self.updateContourCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                           info[INFO_PARAMETER][2],
                                           info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                           info[INFO_PARAMETER][5],
                                           info[INFO_PARAMETER][6], info[INFO_PARAMETER][7])

            # Vec
            if info[INFO_CLASSIFICATION] == "Vec_Type":
                self.updateVectorCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                          info[INFO_PARAMETER][2],
                                          info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                          info[INFO_PARAMETER][5],
                                          info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                          info[INFO_PARAMETER][8],
                                          info[INFO_PARAMETER][9], info[INFO_PARAMETER][10])

            # Pha
            if info[INFO_CLASSIFICATION] == "Pha_Type":
                self.updatePhasespaceCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                              info[INFO_PARAMETER][2],
                                              info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                              info[INFO_PARAMETER][5],
                                              info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                              info[INFO_PARAMETER][8],
                                              info[INFO_PARAMETER][9], info[INFO_PARAMETER][10])

            # Ran
            if info[INFO_CLASSIFICATION] == "Ran_Type":
                self.updateRangeCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                         info[INFO_PARAMETER][2],
                                         info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                         info[INFO_PARAMETER][5],
                                         info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                         info[INFO_PARAMETER][8],
                                         info[INFO_PARAMETER][9])

            # Obs
            if info[INFO_CLASSIFICATION] == "Obs_Type":
                # FreeCAD.Console.PrintError('\n\n\nobserve1111111\n')
                self.updateObserveCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1],
                                           info[INFO_PARAMETER][2],
                                           info[INFO_PARAMETER][3], info[INFO_PARAMETER][4],
                                           info[INFO_PARAMETER][5],
                                           info[INFO_PARAMETER][6], info[INFO_PARAMETER][7],
                                           info[INFO_PARAMETER][8],
                                           info[INFO_PARAMETER][9], info[INFO_PARAMETER][10],
                                           info[INFO_PARAMETER][11],
                                           info[INFO_PARAMETER][12], info[INFO_PARAMETER][13],
                                           info[INFO_PARAMETER][14],
                                           info[INFO_PARAMETER][15], info[INFO_PARAMETER][16],
                                           info[INFO_PARAMETER][17],
                                           info[INFO_PARAMETER][18], info[INFO_PARAMETER][19],
                                           info[INFO_PARAMETER][20],
                                           info[INFO_PARAMETER][21],
                                           info[INFO_PARAMETER][22],
                                           info[INFO_PARAMETER][23],
                                           info[INFO_PARAMETER][24],
                                           info[INFO_PARAMETER][25],
                                           info[INFO_PARAMETER][26],
                                           info[INFO_PARAMETER][27],
                                           info[INFO_PARAMETER][28],)
                # FreeCAD.Console.PrintError('\n\n\nobserve222222\n')
            # timerName, type, numType, stratTime="", stopTime="", timeIncrement="", triggerTimes=""
            # timer
            if info[INFO_CLASSIFICATION] == "Timer_Type" or info[INFO_CLASSIFICATION] == "DefTimer_Type":
                # 处理type
                if info[INFO_PARAMETER][1] == 0:
                    type = Timer.Type.periodic
                elif info[INFO_PARAMETER][1] == 1:
                    type = Timer.Type.discrete
                else:
                    type = "error"

                # 处理numType
                if info[INFO_PARAMETER][2][0] == True:
                    numType = Timer.NumType.integer
                else:
                    numType = Timer.NumType.real

                # triggerTimes
                triggerTimeList = info[INFO_PARAMETER][6].split(" ")
                for tmp in triggerTimeList:
                    if tmp == "":
                        triggerTimeList.remove(tmp)

                self.updateTimerCommands(info[INFO_PARAMETER][0], type, numType,
                                         info[INFO_PARAMETER][3],
                                         info[INFO_PARAMETER][4], info[INFO_PARAMETER][5],
                                         triggerTimeList)


    def __updateEngineeringInfo(self):
        from ProjectSetting.Commands.ProjectSettingsDlgData import getDlgData
        infoList = getDlgData()

        # print "EngineeringInfo"
        # print infoList

        INFO_CLASSIFICATION = 0
        INFO_PARAMETER = 1

        for info in infoList:
            # WorkSpaceSettings
            if info[INFO_CLASSIFICATION] == "WorkSpaceSettings":
                try:
                     flag=info[INFO_PARAMETER][4]
                except:
                    pass
                else:
                    # if flag == True:
                    self.updateWorkAreaCommands(info[INFO_PARAMETER][0],
                                                info[INFO_PARAMETER][1][0], info[INFO_PARAMETER][1][1],
                                                info[INFO_PARAMETER][1][2],
                                                info[INFO_PARAMETER][2][0], info[INFO_PARAMETER][2][1],
                                                info[INFO_PARAMETER][2][2],
                                                info[INFO_PARAMETER][3][0], info[INFO_PARAMETER][3][1],
                                                info[INFO_PARAMETER][3][2],flag)


            # NewMaterical
            if info[INFO_CLASSIFICATION] == "NewMaterical":
            # if "NewMaterical" in info[INFO_CLASSIFICATION]:
                # FreeCAD.Console.PrintError('\n'+str(info[INFO_PARAMETER][0])+'\n')
                self.updateMaterialCommands(info[INFO_PARAMETER][0],
                                            info[INFO_PARAMETER][1],
                                            info[INFO_PARAMETER][2],
                                            info[INFO_PARAMETER][3],
                                            info[INFO_PARAMETER][4][0], info[INFO_PARAMETER][4][1],
                                            info[INFO_PARAMETER][5][0], info[INFO_PARAMETER][5][1])

            # FiledSetting
            if info[INFO_CLASSIFICATION] == "FiledSetting":
                self.updatePresetCommands(info[INFO_PARAMETER][0][0], info[INFO_PARAMETER][0][1],
                                            info[INFO_PARAMETER][1][0], info[INFO_PARAMETER][1][1],
                                            info[INFO_PARAMETER][2][0], info[INFO_PARAMETER][2][1],
                                            info[INFO_PARAMETER][3][0], info[INFO_PARAMETER][3][1],
                                            info[INFO_PARAMETER][4][0], info[INFO_PARAMETER][4][1],
                                            info[INFO_PARAMETER][5][0], info[INFO_PARAMETER][5][1],
                                            info[INFO_PARAMETER][6])

            # TimeDomainComputing
            if info[INFO_CLASSIFICATION] == "TimeDomainComputing":

                # 格式化场算法参数
                if info[INFO_PARAMETER][1] == u"时偏FDTD":
                    algorithm = "BIASED"
                elif info[INFO_PARAMETER][1] == u"中心差分FDTD":
                    algorithm = "CENTERED"
                elif info[INFO_PARAMETER][1] == u"高Q值FDTD":
                    algorithm = "HIGH_Q"
                else:
                    algorithm = "error"

                # 格式化模式参数
                pattern = "error"
                if info[INFO_PARAMETER][2][1] == True:
                    pattern = "EM"
                if info[INFO_PARAMETER][2][2] == True:
                    pattern = "TE"
                if info[INFO_PARAMETER][2][3] == True:
                    pattern = "TM"

                self.updateTimeComputationCommands(info[INFO_PARAMETER][0],
                                                   algorithm,
                                                   info[INFO_PARAMETER][2][0], pattern,
                                                   info[INFO_PARAMETER][3][0],info[INFO_PARAMETER][3][1],
                                                   info[INFO_PARAMETER][4],
                                                   info[INFO_PARAMETER][5],info[INFO_PARAMETER][6],
                                                   info[INFO_PARAMETER][7],info[INFO_PARAMETER][8],
                                                   info[INFO_PARAMETER][9],info[INFO_PARAMETER][10],
                                                   info[INFO_PARAMETER][11],info[INFO_PARAMETER][12])

            # DataProcessingSetting
            if info[INFO_CLASSIFICATION] == "DataProcessingSetting":
                isASCII = True
                if info[INFO_PARAMETER][6][1] == True:
                    isASCII = False

                self.updateDataExportCommands(FreeCAD.ActiveDocument.Label + "_TIME",
                                              info[INFO_PARAMETER][0],
                                              info[INFO_PARAMETER][1],
                                              info[INFO_PARAMETER][2],
                                              info[INFO_PARAMETER][3],
                                              info[INFO_PARAMETER][4],
                                              info[INFO_PARAMETER][5][0],info[INFO_PARAMETER][5][1],
                                              info[INFO_PARAMETER][6][0],info[INFO_PARAMETER][6][1],
                                              isASCII)

            # ModelingInfo
            if info[INFO_CLASSIFICATION] == "ModelingInfo":
                self.updateHeaderCommands(info[INFO_PARAMETER][2],
                                        info[INFO_PARAMETER][1],
                                        info[INFO_PARAMETER][0],
                                        info[INFO_PARAMETER][3])

            # RunOptions
            if info[INFO_CLASSIFICATION] == "RunOptions":
                self.updateRunOptionCommands(info[INFO_PARAMETER][0], info[INFO_PARAMETER][1])


    ########################## 以下是根据几何建模或参数建模更新m3d文件的函数 v1##########################

    #######几何信息

    def updateParameter(self, name, val):
        '''
        更新参数命令组
        :param name: 参数名
        :param val: 参数值
        '''
        # 获得命令
        content = getParameterCommands(name, val)
        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.PARAMETER,
                                   content)


    def updatePonitCommands(self, ponitName, coordinates,
                            isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                            ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """
        添加或更新点命令组
        :param ponitName: 点名称
        :param coordinates: 点坐标列表
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得point命令
        content = getPointCommands(ponitName, coordinates)
        # 获得附加的mark命令
        extraContent = getMarkCommands(ponitName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                   ismin_1, ismid_1, ismax_1,
                   ismin_2, ismid_2, ismax_2,
                   ismin_3, ismid_3, ismax_3)
        # 更新manager
        self.__addOrUpdateCommands(ponitName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   [[self.__Classification.DEFINE_OBJECTS, extraContent]])


    def updateLineCommands(self, lineName, lineType, startPointCoordinates, stopPointCoordinates,
                           isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                           ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """
        添加或更新线命令组
        :param lineName: 线名称
        :param lineType: 线类型( CONFORMAL \ OBLIQUE )
        :param startPointCoordinates: 起点坐标列表
        :param stopPointCoordinates: 止点坐标列表
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得line命令
        content = getLineCommands(lineName, lineType, startPointCoordinates, stopPointCoordinates)
        # 获得附加的mark命令
        extraContent = getMarkCommands(lineName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                                        ismin_1, ismid_1, ismax_1,
                                        ismin_2, ismid_2, ismax_2,
                                        ismin_3, ismid_3, ismax_3)
        # FreeCAD.Console.PrintError('\nconent:   '+str(content))
        # FreeCAD.Console.PrintError('\nextraconent:   '+str(extraContent))
        # 更新manager
        self.__addOrUpdateCommands(lineName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   [[self.__Classification.DEFINE_OBJECTS, extraContent]])


    def updateObliqueLineCommands(self, lineName,lineType, startPointCoordinates, stopPointCoordinates,
                           isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                           ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """
        添加或更新线命令组
        :param lineName: 线名称
        :param lineType: 线类型( CONFORMAL \ OBLIQUE )
        :param startPointCoordinates: 起点坐标列表
        :param stopPointCoordinates: 止点坐标列表
        :param baseradius: 半径
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return:
        """
        # 获得line命令
        content = getObliqueLineCommands(lineName,startPointCoordinates, stopPointCoordinates)
        # 获得附加的mark命令
        extraContent = getMarkCommands(lineName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                   ismin_2, ismid_2, ismax_2,
                   ismin_3, ismid_3, ismax_3)
        # 更新manager
        self.__addOrUpdateCommands(lineName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   [[self.__Classification.DEFINE_OBJECTS, extraContent]])


    def updateConformalAreaCommands(self, areaName, startPointCoordinates, stopPointCoordinates,
                                    isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                    ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """
        :param areaName: 面名称
        :param startPointCoordinates: 起点坐标列表
        :param stopPointCoordinates: 止点坐标列表
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得area命令
        content = getAreaCommands(areaName, Area.Shape.conformal, startPointCoordinates, stopPointCoordinates)
        # 获得附加的mark命令
        extraContent = getMarkCommands(areaName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                                    ismin_1, ismid_1, ismax_1,
                                    ismin_2, ismid_2, ismax_2,
                                    ismin_3, ismid_3, ismax_3)
        # 更新manager
        self.__addOrUpdateCommands(areaName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   [[self.__Classification.DEFINE_OBJECTS, extraContent]])


    def updateRectangularAreaCommands(self, areaName, startPointCoordinates, stopPointCoordinates,
                                      isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                      ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param areaName: 面名称
        :param startPointCoordinates: 起点坐标列表
        :param stopPointCoordinates: 止点坐标列表
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得area命令
        content = getAreaCommands(areaName, Area.Shape.rectangular, startPointCoordinates, stopPointCoordinates)
        # 获得附加的mark命令
        extraContent = getMarkCommands(areaName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        # 更新manager
        self.__addOrUpdateCommands(areaName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   [[self.__Classification.DEFINE_OBJECTS, extraContent]])

    def updatePolygonalAreaCommands(self, areaName, pointCoordinatesList,
                                      isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                      ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param areaName: 面名称
        :param pointCoordinatesList: 点坐标列表
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return:
        """
        # 获得area命令
        content = getPolygonalAreaCommands(areaName, pointCoordinatesList)
        # 获得附加的mark命令
        extraContent = getMarkCommands(areaName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        # 更新manager
        self.__addOrUpdateCommands(areaName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   [[self.__Classification.DEFINE_OBJECTS, extraContent]])


    def updateConformalVolumeCommands(self, volumeName, nearPointCoordinates, farPointCoordinates,
                                      attributeResults,
                                      isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                      ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """
        
        :param volumeName: 投影体名称
        :param nearPointCoordinates: 近点坐标列表
        :param farPointCoordinates: 远点坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # FreeCAD.Console.PrintError('\n已经进入更新正投影体m3d的函数\n')
        # 获得volume命令
        content = getConformalVolumeCommands(volumeName, nearPointCoordinates, farPointCoordinates)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateConeVolumeCommands(self, volumeName, basePointCoordinates, topPointCoordinates, baseradius, topradius,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """
        
        :param volumeName: 圆锥或圆台名称
        :param basePointCoordinates: 底店坐标列表
        :param topPointCoordinates: 顶点坐标列表
        :param baseradius: 底半径
        :param topradius: 顶半径
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getConeVolumeCommands(volumeName, basePointCoordinates, topPointCoordinates, baseradius, topradius)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                                            isDielectric, isotropy, attributeResults[4],
                                                            attributeResults[5], attributeResults[6],
                                                            attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateCylindricalVolumeCommands(self, volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radius,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param centerPoint1Coordinates: 点1坐标列表
        :param centerPoint2Coordinates: 点2坐标列表
        :param radius: 底半径
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getCylindricalVolumeCommands(volumeName,centerPoint1Coordinates, centerPoint2Coordinates, radius)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                                            isDielectric, isotropy, attributeResults[4],
                                                            attributeResults[5], attributeResults[6],
                                                            attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateAnnularVolumeCommands(self, volumeName, centerPoint1Coordinates, centerPoint2Coordinates, radiusInner, radiusOuter,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param centerPoint1Coordinates: 点1坐标列表
        :param centerPoint2Coordinates: 点2坐标列表
        :param radiusInner: 内半径
        :param radiusOuter: 外半径
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getAnnularVolumeCommands(volumeName,centerPoint1Coordinates, centerPoint2Coordinates, radiusInner, radiusOuter)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateAnnularSectionVolumeCommands(self, volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,point3Coordinates, point4Coordinates,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 点1坐标列表
        :param point2Coordinates: 点2坐标列表
        :param radiusInner: 内半径
        :param radiusOuter: 外半径
        :param point3Coordinates: 点3坐标列表
        :param point4Coordinates: 点4坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getAnnularSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates,
                                                  radiusInner, radiusOuter, point3Coordinates, point4Coordinates)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateParallelepipedalVolumeCommands(self, volumeName, point1Coordinates, point2Coordinates, point3Coordinates, point4Coordinates,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 点1坐标列表
        :param point2Coordinates: 点2坐标列表
        :param point3Coordinates: 点3坐标列表
        :param point4Coordinates: 点4坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getParallelepipedalVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates,
                                                    point4Coordinates)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateSphericalVolumeCommands(self, volumeName, pointCoordinates, radius,
                                      attributeResults,
                                      isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                      ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 点1坐标列表
        :param point2Coordinates: 点2坐标列表
        :param point3Coordinates: 点3坐标列表
        :param point4Coordinates: 点4坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getSphericalVolumeCommands(volumeName, pointCoordinates, radius)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateWedgeVolumeCommands(self, volumeName,point1Coordinates, point2Coordinates,point3Coordinates,
                                             point4Coordinates, point5Coordinates, point6Coordinates,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 点1坐标列表
        :param point2Coordinates: 点2坐标列表
        :param point3Coordinates: 点3坐标列表
        :param point4Coordinates: 点4坐标列表
        :param point5Coordinates: 点5坐标列表
        :param point6Coordinates: 点6坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getWedgeVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates,
                                                    point4Coordinates, point5Coordinates, point6Coordinates)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updatePyramidVolumeCommands(self, volumeName,point1Coordinates, point2Coordinates,point3Coordinates,
                                             point4Coordinates, point5Coordinates,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 点1坐标列表
        :param point2Coordinates: 点2坐标列表
        :param point3Coordinates: 点3坐标列表
        :param point4Coordinates: 点4坐标列表
        :param point5Coordinates: 点5坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getPyramidVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates,
                                                    point4Coordinates, point5Coordinates)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateTetrahedronVolumeCommands(self, volumeName,point1Coordinates, point2Coordinates,point3Coordinates,
                                             point4Coordinates,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 点1坐标列表
        :param point2Coordinates: 点2坐标列表
        :param point3Coordinates: 点3坐标列表
        :param point4Coordinates: 点4坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getTetrahedronVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates,
                                                    point4Coordinates)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateRhombusVolumeCommands(self, volumeName, point1Coordinates, point2Coordinates, point3Coordinates,
                                        point4Coordinates,point5Coordinates, point6Coordinates, point7Coordinates,
                                        point8Coordinates,
                                        attributeResults,
                                        isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                        ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):

        # 获得volume命令
        content = getRhombusVolumeCommands(volumeName, point1Coordinates, point2Coordinates, point3Coordinates,
                                               point4Coordinates, point5Coordinates, point6Coordinates, point7Coordinates,
                                               point8Coordinates)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateToroidalSectionVolumeCommands(self, volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,point3Coordinates, point4Coordinates,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 点1坐标列表
        :param point2Coordinates: 点2坐标列表
        :param point3Coordinates: 点3坐标列表
        :param point4Coordinates: 点4坐标列表
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        # 获得volume命令
        content = getToroidalSectionVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,point3Coordinates, point4Coordinates,)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateExtrudedVolumeCommands(self, volumeName, areaLabel, lineLabel,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param areaLabel: 面名称
        :param lineLabel: 线名称
        :param attributeResults: 自定义属性
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return:
        """
        # 获得volume命令
        content = getExtrudedVolumeCommands(volumeName,areaLabel, lineLabel)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)


    def updateHelicalVolumeCommands(self, volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,point3Coordinates, pitch, width,
                                 attributeResults,
                                 isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                                 ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param point1Coordinates: 基点坐标列表
        :param point2Coordinates: 顶点坐标列表
        :param radiusInner: 内半径
        :param radiusOuter: 外半径
        :param point3Coordinates: 起点坐标列表
        :param pitch: 螺旋节距
        :param width: 螺旋线径向宽度
        :param isConductor: 是否为理想导体
        :param isVoid: 是否为真空区域
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return:
        """
        # 获得volume命令
        content = getHelicalVolumeCommands(volumeName, point1Coordinates, point2Coordinates, radiusInner, radiusOuter,point3Coordinates, pitch, width,)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)
            

    def updateArrayVolumeCommands(self,arrayParameterList, baseParameterList):
        """
        :param arrayParameterList: 阵列体的参数
        :param baseParameterList: 阵列体的基础物体参数
        :return:
        """
        arrayName = arrayParameterList[0]
        # 获得附加的mark命令
        volumeName = "Arr_"+baseParameterList[1][0]
        [isX1, isX2, isX3, X1Size, X2Size, X3Size, 
        ismin_1, ismid_1, ismax_1,
        ismin_2, ismid_2, ismax_2,
        ismin_3, ismid_3, ismax_3] = baseParameterList[1][-15:]
        extraContentMark = getMarkCommands(volumeName +'\'i\'', isX1, isX2, isX3, X1Size, X2Size, X3Size,
                                           ismin_1, ismid_1, ismax_1,
                                           ismin_2, ismid_2, ismax_2,
                                           ismin_3, ismid_3, ismax_3)
        extra=[]
        # extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        baseType = baseParameterList[0]

        if baseType.startswith("Vol"):
            # FreeCAD.Console.PrintError("\n执行到这里ifififif")
            # FreeCAD.Console.PrintError("\n执行到这里:   "+str(baseParameterList))
            # 此处可能出现问题，所以添加异常处理，待后续改进 @lzg
            try:
                content = getArrayVolumeCommands(self.coordinateSystem, arrayParameterList,baseType, baseParameterList[1][:-16],extraContentMark)
                attributeResults = baseParameterList[1][-16:-15]
            except:
                content = getArrayVolumeCommands(self.coordinateSystem, arrayParameterList,baseType, baseParameterList[1][:-7],extraContentMark)
                attributeResults = baseParameterList[1][-7:-6]
            # 获得附加的属性命令
            if attributeResults[0][0] == "Conductor":
                extraContentConductor = getConductorCommands(volumeName,thiscontent=content)
                extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
            elif attributeResults[0][0] == "Vacuo":
                extraContentVoid = getVoidCommands(volumeName,thiscontent=content)
                extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
            elif attributeResults[0][0] == "Custom":
                isotropy = False
                isDielectric = False
                if attributeResults[0][3] == "Isotropy":
                    isDielectric = True
                    isotropy = True
                if attributeResults[0][3] == "Anisotropy":
                    isDielectric = True
                    isotropy = False
                # 加上有一个默认参数不是阵列体的参数 @fubiao
                extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[0][1], attributeResults[0][2],
                                      isDielectric, isotropy, attributeResults[0][4], attributeResults[0][5], attributeResults[0][6],
                                      attributeResults[0][7],attributeResults[0][8],attributeResults[0][9],
                                      thiscontent=content)
                extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])
                        # 获得volume命令
            # content = getArrayVolumeCommands(self.coordinateSystem, arrayParameterList,baseType, baseParameterList[1][:-7],extraContentMark)
        else:
            # 获得volume命令
            content = getArrayVolumeCommands(self.coordinateSystem, arrayParameterList, baseType,baseParameterList[1][:-6])
        # 更新manager
        self.__addOrUpdateCommands(arrayName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)
    # @fubiao
    def updateParamArrayVolumeCommands(self,volumeName, 
                                        baseObjType,
                                        start,end, 
                                        baseObjData,
                                        attributeResults,
                                        isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size=""):
        
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName+"\'i\'", isX1, isX2, isX3, X1Size, X2Size, X3Size)

        content=getParamArrayVolumeCommands(volumeName,baseObjType,start,end,baseObjData,extraContentMark)
        
        # content=content+extraContentMark

        extra = [[self.__Classification.DEFINE_OBJECTS, ""]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName,thiscontent=content)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName,thiscontent=content)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9],thiscontent=content)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)
    #体（函数体）
    def updateFunctionVolumeCommands(self,volumeName,
                                    Point_1,Point_2,functionStr,attributeResults,
                                    isX1=False,isX2=False,isX3=False,X1Size="",X2Size="",X3Size="",
                                    ismin_1 = False, ismid_1 = False, ismax_1 = False,
                            ismin_2 = False, ismid_2 = False, ismax_2 = False,
                            ismin_3 = False, ismid_3 = False, ismax_3 = False):
        content = getFunctionVolumeCommands(volumeName,self.coordinateSystem, Point_1,Point_2,functionStr)
        # 获得附加的mark命令
        extraContentMark = getMarkCommands(volumeName, isX1, isX2, isX3, X1Size, X2Size, X3Size,
                    ismin_1, ismid_1, ismax_1,
                    ismin_2, ismid_2, ismax_2,
                    ismin_3, ismid_3, ismax_3)
        FreeCAD.Console.PrintError("extraContentMark: "+str(extraContentMark)+"\n")
        extra = [[self.__Classification.DEFINE_OBJECTS, extraContentMark]]
        # 获得附加的属性命令
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                  isDielectric, isotropy, attributeResults[4], attributeResults[5], attributeResults[6],
                                  attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])
        # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)

    def updataRotateVolumeCommands(self,volumeName,
                                   axis_base_point,axis_top_point,area,
                                   attributeResults,
                                   isX1=False,isX2=False,isX3=False,X1Size="",X2Size="",X3Size="",
                                   ismin_1 = False, ismid_1 = False, ismax_1 = False,
                                   ismin_2 = False, ismid_2 = False, ismax_2 = False,
                                   ismin_3 = False, ismid_3 = False, ismax_3 = False):
        """

        :param volumeName: 名称
        :param axis_base_point: 点1坐标列表
        :param axis_top_point: 点2坐标列表
        :param area: 面名
        :param attributeResults: 附加属性命令
        :param isX1:是否选择了X1对应的坐标轴
        :param isX2:是否选择了X2对应的坐标轴
        :param isX3:是否选择了X3对应的坐标轴
        :param X1Size:X1坐标轴上的值
        :param X2Size:X2坐标轴上的值
        :param X3Size:X3坐标轴上的值
        :return:
        """
        #获得volume命令
        content = getRotateVolumeCommands(volumeName,axis_base_point,axis_top_point,area)
        #获得附加的mark命令
        extraContenMark=getMarkCommands(volumeName,isX1,isX2,isX3,X1Size,X2Size,X3Size,
                                        ismin_1, ismid_1, ismax_1,
                                        ismin_2, ismid_2, ismax_2,
                                        ismin_3, ismid_3, ismax_3)
        extra=[[self.__Classification.DEFINE_OBJECTS,extraContenMark]]
        # 获得附加的属性命令,直接复制粘贴的
        if attributeResults[0] == "Conductor":
            extraContentConductor = getConductorCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentConductor])
        elif attributeResults[0] == "Vacuo":
            extraContentVoid = getVoidCommands(volumeName)
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentVoid])
        elif attributeResults[0] == "Custom":
            isotropy = False
            isDielectric = False
            if attributeResults[3] == "Isotropy":
                isDielectric = True
                isotropy = True
            if attributeResults[3] == "Anisotropy":
                isDielectric = True
                isotropy = False

            extraContentDIY = getVolumeDIYAttributeCommands(volumeName, attributeResults[1], attributeResults[2],
                                                            isDielectric, isotropy, attributeResults[4],
                                                            attributeResults[5], attributeResults[6],
                                                            attributeResults[7],attributeResults[8],attributeResults[9])
            extra.append([self.__Classification.PROPERTIES_AND_PROCESSES, extraContentDIY])

            # 更新manager
        self.__addOrUpdateCommands(volumeName,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content,
                                   extra)
    ########物理信息
    def updatePortCommands(self, name, direction,
                    isPhaseVelocity=False, phaseVelocity="",
                    isScale=False, scale="",
                    isFt=False, ftVal="",
                    isGeFirst=False, geFirstName="", geFirstVal="",
                    isGeSecond=False, geSecondName="", geSecondVal="",
                    isNormalization=False, isNewConformalLine=True,normalizationLine="",
                    isLaplacian=False, laplacianFirst="", laplacianSecond="",
                    isAppointArea=False, areaName="", startPointCoordinates=[], stopPointCoordinates=[],
                    isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size="",
                    laplacenumber1="",laplacenumber2="",
                    laplacianThird="", laplacianFourth="",laplacianFifth="",
                    laplacenumber3="",laplacenumber4="",laplacenumber5="",
                    laplace_num = "",
                    circuit_Checked = False,circuit = "",
                    observe_name = ""):
        """
        
        name为波导端口名称
        direction为波导端口的法向，POSITIVE 或 NEGATIVE
    
        以下为可选参数
        isPhaseVelocity、phaseVelocity对应于相对相速比
        isScale、scale相对于法向修正
        isFt、ftVal相对于输入场时间分布
        isGeFirst、geFirstName、geFirstVal相对于空间分布的第一个空,geFirstName请以 GE* 命名
        isGeSecond、geSecondName、geSecondVal相对于空间分布的第二个空，geSecondName请以 GE* 命名
        isNormalization、isNewConformalLine、normalizationLine相对于电压归一化，其中isNewConformalLine代表是否需要新建线
        isLaplacian、laplacianFirst、laplacianSecind相对于拉普拉斯的两个选项
        circuit_Checked 为归一化电压是否选择，circuit为归一化电压内容
        
        :param isAppointArea: 是否指定正交投影面
        :param areaName: 若指定，正交投影面名称
        :param startPointCoordinates: 若没有指定，起点坐标列表
        :param stopPointCoordinates: 若没有指定，止点坐标列表
        
        :param isX1: 是否选择了X1的坐标轴
        :param isX2: 是否选择了X2应的坐标轴
        :param isX3: 是否选择了X3应的坐标轴
        :param X1Size: X1坐标轴上的值
        :param X2Size: X2坐标轴上的值
        :param X3Size: X3坐标轴上的值
        :return: 
        """
        

        # 检查必要参数是否都填入
        if isAppointArea and areaName == "":
            sayz("Port命令生成，请检查areaName是否填入")
            return

        if not isAppointArea and startPointCoordinates == []:
            sayz("Port命令生成，请检查startPointCoordinates是否填入")
            return

        if not isAppointArea and stopPointCoordinates == []:
            sayz("Port命令生成，请检查stopPointCoordinates是否填入")
            return
        # 如果没有指定正交投影面
        if not isAppointArea:
            # 获得附加的line命令
            if isNormalization:
                # 获得port命令
                content = getPortCommands(name, self.coordinateSystem, name, direction,
                                          isPhaseVelocity, phaseVelocity,
                                          isScale, scale,
                                          isFt, ftVal,
                                          isGeFirst, geFirstName, geFirstVal,
                                          isGeSecond, geSecondName, geSecondVal,
                                          isNormalization, name+".LINE",
                                          isLaplacian, laplacianFirst, laplacianSecond,
                                          laplacenumber1,laplacenumber2,
                                          laplacianThird, laplacianFourth,laplacianFifth,
                                          laplacenumber3,laplacenumber4,laplacenumber5,
                                          laplace_num,
                                          circuit_Checked,circuit,
                                          observe_name)

                # 获得附加的area命令
                extraContentArea = getAreaCommands(name, Area.Shape.conformal, startPointCoordinates,
                                                   stopPointCoordinates)

                # 获得归一化线的止点坐标
                lineStarts = "error"
                lineStops = "error"
                # 直角坐标系下(x,y,z)
                if self.coordinateSystem == self.CoordinateSystem.rectangularSys:
                    # x坐标相同
                    if startPointCoordinates[0] == stopPointCoordinates[0]:
                        # 得到startpoint的值和单位组成的list
                        start_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[2])
                        stop_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[2])
                        pointCoordinates_z = str((float(start_z_data[0]) + float(stop_z_data[0])) / 2) + start_z_data[1]
                        lineStarts = [startPointCoordinates[0], startPointCoordinates[1], pointCoordinates_z]
                        lineStops = [startPointCoordinates[0], stopPointCoordinates[1], pointCoordinates_z]

                    # y坐标相同
                    elif startPointCoordinates[1] == stopPointCoordinates[1]:
                        # 得到startpoint的值和单位组成的list
                        start_x_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[0])
                        stop_x_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[0])
                        pointCoordinates_x = str((float(start_x_data[0]) + float(stop_x_data[0])) / 2) + start_x_data[1]
                        lineStarts = [pointCoordinates_x, startPointCoordinates[1], startPointCoordinates[2]]
                        lineStops = [pointCoordinates_x, stopPointCoordinates[1], stopPointCoordinates[2]]

                    # z坐标相同
                    else:
                        # 得到startpoint的值和单位组成的list
                        start_y_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[1])
                        stop_y_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[1])
                        pointCoordinates_y = str((float(start_y_data[0]) + float(stop_y_data[0])) / 2) + start_y_data[1]
                        lineStarts = [startPointCoordinates[0], pointCoordinates_y, startPointCoordinates[2]]
                        lineStops = [stopPointCoordinates[0], pointCoordinates_y, startPointCoordinates[2]]

                # 柱坐标系下(z,r,theta)
                if self.coordinateSystem == self.CoordinateSystem.cylindricalSys:
                    # z坐标相同或r坐标相同
                    if startPointCoordinates[0] == stopPointCoordinates[0] or startPointCoordinates[1] == \
                            stopPointCoordinates[1]:
                        # 得到startpoint的值和单位组成的list
                        start_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(
                            startPointCoordinates[2])
                        stop_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[2])
                        pointCoordinates_theta = str((float(start_theta_data[0]) + float(stop_theta_data[0])) / 2) + \
                                                 start_theta_data[1]
                        lineStarts = [startPointCoordinates[0], startPointCoordinates[1], pointCoordinates_theta]
                        lineStops = [stopPointCoordinates[0], stopPointCoordinates[1], pointCoordinates_theta]
                    else:
                        # 得到startpoint的值和单位组成的list
                        start_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[0])
                        stop_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[0])
                        pointCoordinates_z = str((float(start_z_data[0]) + float(stop_z_data[0])) / 2) + start_z_data[1]
                        lineStarts = [pointCoordinates_z, startPointCoordinates[1], startPointCoordinates[2]]
                        lineStops = [pointCoordinates_z, stopPointCoordinates[1], startPointCoordinates[2]]

                # 极坐标系下(r,theta,z)
                if self.coordinateSystem == self.CoordinateSystem.polarSys:
                    # z坐标相同或r坐标相同
                    if startPointCoordinates[0] == stopPointCoordinates[0] or startPointCoordinates[2] == \
                            stopPointCoordinates[2]:
                        # 得到startpoint的值和单位组成的list
                        start_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(
                            startPointCoordinates[1])
                        stop_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[1])
                        pointCoordinates_theta = str((float(start_theta_data[0]) + float(stop_theta_data[0])) / 2) + \
                                                 start_theta_data[1]
                        lineStarts = [startPointCoordinates[0], pointCoordinates_theta, startPointCoordinates[2]]
                        lineStops = [stopPointCoordinates[0], pointCoordinates_theta, stopPointCoordinates[2]]
                    else:
                        # 得到startpoint的值和单位组成的list
                        start_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[2])
                        stop_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[2])
                        pointCoordinates_z = str((float(start_z_data[0]) + float(stop_z_data[0])) / 2) + start_z_data[1]
                        lineStarts = [startPointCoordinates[0], startPointCoordinates[1], pointCoordinates_z]
                        lineStops = [stopPointCoordinates[0], startPointCoordinates[1], pointCoordinates_z]

                extraContentline = Point(name+".LNLO", lineStarts).getPonitStr() + NEWLINE + \
                                   Point(name + ".LNHI", lineStops).getPonitStr() + NEWLINE + \
                                   Line(name+".LINE", Line.Type.conformal, [name+".LNLO", name+".LNHI"]).getLineStr() + NEWLINE

                # 获得附加的mark命令
                extraContentMark = getMarkCommands(name, isX1, isX2, isX3, X1Size, X2Size, X3Size)

                # 更新manager
                self.__addOrUpdateCommands(name,
                                           self.__Classification.PROPERTIES_AND_PROCESSES,
                                           content,
                                           [[self.__Classification.PANEL_OBJECTS, extraContentArea],
                                            [self.__Classification.PANEL_OBJECTS, extraContentline],
                                            [self.__Classification.PANEL_OBJECTS, extraContentMark]])

            else:
                # 获得port命令
                content = getPortCommands(name, self.coordinateSystem, name, direction,
                                          isPhaseVelocity, phaseVelocity,
                                          isScale, scale,
                                          isFt, ftVal,
                                          isGeFirst, geFirstName, geFirstVal,
                                          isGeSecond, geSecondName, geSecondVal,
                                          isNormalization, normalizationLine,
                                          isLaplacian, laplacianFirst, laplacianSecond,
                                          laplacenumber1,laplacenumber2,
                                          laplacianThird, laplacianFourth,laplacianFifth,
                                          laplacenumber3,laplacenumber4,laplacenumber5,
                                          laplace_num,
                                          circuit_Checked,circuit,
                                          observe_name)

                # 获得附加的area命令
                extraContentArea = getAreaCommands(name, Area.Shape.conformal, startPointCoordinates,
                                                   stopPointCoordinates)

                # 获得附加的mark命令
                extraContentMark = getMarkCommands(name, isX1, isX2, isX3, X1Size, X2Size, X3Size)

                # 更新manager
                self.__addOrUpdateCommands(name,
                                           self.__Classification.PROPERTIES_AND_PROCESSES,
                                           content,
                                           [[self.__Classification.PANEL_OBJECTS, extraContentArea],
                                            [self.__Classification.PANEL_OBJECTS, extraContentMark]])


        # 如果指定了正交投影面
        else:
            # 获得附加的line命令
            # 如果可归一化且需新建线
            if isNormalization and isNewConformalLine:

                # 获得port命令
                content = getPortCommands(name, self.coordinateSystem, areaName, direction,
                                          isPhaseVelocity, phaseVelocity,
                                          isScale, scale,
                                          isFt, ftVal,
                                          isGeFirst, geFirstName, geFirstVal,
                                          isGeSecond, geSecondName, geSecondVal,
                                          isNormalization, areaName + ".LINE",
                                          isLaplacian, laplacianFirst, laplacianSecond,
                                          laplacenumber1,laplacenumber2,
                                          laplacianThird, laplacianFourth,laplacianFifth,
                                          laplacenumber3,laplacenumber4,laplacenumber5,
                                          laplace_num,
                                          circuit_Checked,circuit,
                                          observe_name)

                # 获得归一化线的止点坐标
                # todo::修改投影线的起止坐标
                lineStarts = "error"
                lineStops = "error"
                # 直角坐标系下(x,y,z)
                if self.coordinateSystem == self.CoordinateSystem.rectangularSys:
                    # x坐标相同
                    if startPointCoordinates[0] == stopPointCoordinates[0]:
                        # 得到startpoint的值和单位组成的list
                        start_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[2])
                        stop_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[2])
                        pointCoordinates_z = str((float(start_z_data[0])+float(stop_z_data[0]))/2) + start_z_data[1]
                        lineStarts = [startPointCoordinates[0], startPointCoordinates[1], pointCoordinates_z]
                        lineStops = [startPointCoordinates[0], stopPointCoordinates[1], pointCoordinates_z]

                    # y坐标相同
                    elif startPointCoordinates[1] == stopPointCoordinates[1]:
                        # 得到startpoint的值和单位组成的list
                        start_x_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[0])
                        stop_x_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[0])
                        pointCoordinates_x = str((float(start_x_data[0]) + float(stop_x_data[0])) / 2) + start_x_data[1]
                        lineStarts = [pointCoordinates_x, startPointCoordinates[1], startPointCoordinates[2]]
                        lineStops = [pointCoordinates_x, stopPointCoordinates[1], stopPointCoordinates[2]]

                    # z坐标相同
                    else:
                        # 得到startpoint的值和单位组成的list
                        start_y_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[1])
                        stop_y_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[1])
                        pointCoordinates_y = str((float(start_y_data[0]) + float(stop_y_data[0])) / 2) + start_y_data[1]
                        lineStarts = [startPointCoordinates[0], pointCoordinates_y, startPointCoordinates[2]]
                        lineStops = [stopPointCoordinates[0], pointCoordinates_y, startPointCoordinates[2]]

                # 柱坐标系下(z,r,theta)
                if self.coordinateSystem == self.CoordinateSystem.cylindricalSys:
                    # z坐标相同或r坐标相同
                    if startPointCoordinates[0] == stopPointCoordinates[0] or startPointCoordinates[1] == stopPointCoordinates[1]:
                        # 得到startpoint的值和单位组成的list
                        start_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[2])
                        stop_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[2])
                        pointCoordinates_theta = str((float(start_theta_data[0]) + float(stop_theta_data[0])) / 2) + start_theta_data[1]
                        lineStarts = [startPointCoordinates[0], startPointCoordinates[1], pointCoordinates_theta]
                        lineStops = [stopPointCoordinates[0], stopPointCoordinates[1], pointCoordinates_theta]
                    else:
                        # 得到startpoint的值和单位组成的list
                        start_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[0])
                        stop_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[0])
                        pointCoordinates_z = str((float(start_z_data[0]) + float(stop_z_data[0]))/ 2) + start_z_data[1]
                        lineStarts = [pointCoordinates_z, startPointCoordinates[1], startPointCoordinates[2]]
                        lineStops = [pointCoordinates_z, stopPointCoordinates[1], startPointCoordinates[2]]

                # 极坐标系下(r,theta,z)
                if self.coordinateSystem == self.CoordinateSystem.polarSys:
                    # z坐标相同或r坐标相同
                    if startPointCoordinates[0] == stopPointCoordinates[0] or startPointCoordinates[2] == \
                            stopPointCoordinates[2]:
                        
                        # 得到startpoint的值和单位组成的list
                        start_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[1])
                        stop_theta_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[1])
                        pointCoordinates_theta = str((float(start_theta_data[0]) + float(stop_theta_data[0]))/ 2) + start_theta_data[1]
                        lineStarts = [startPointCoordinates[0], pointCoordinates_theta, startPointCoordinates[2]]
                        lineStops = [stopPointCoordinates[0], pointCoordinates_theta, stopPointCoordinates[2]]
                    else:
                        # 得到startpoint的值和单位组成的list
                        start_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(startPointCoordinates[2])
                        stop_z_data = Modeling.Common.Tools.UnitTools.getValueAndUnitOfDataFromParamObj(stopPointCoordinates[2])
                        pointCoordinates_z = str((float(start_z_data[0]) + float(stop_z_data[0]))/ 2) + start_z_data[1]
                        lineStarts = [startPointCoordinates[0], startPointCoordinates[1], pointCoordinates_z]
                        lineStops = [stopPointCoordinates[0], startPointCoordinates[1], pointCoordinates_z]
                # 生成对应的注释
                lineCommandsStr = NEWLINE + "!!" + name + NEWLINE

                extraContentline = lineCommandsStr+Point(areaName + ".LNLO", lineStarts).getPonitStr() + NEWLINE + \
                                   Point(areaName + ".LNHI", lineStops).getPonitStr() + NEWLINE +\
                                   Line(areaName + ".LINE", Line.Type.conformal,
                                        [areaName + ".LNLO", areaName + ".LNHI"]).getLineStr() + NEWLINE

                # 更新manager
                self.__addOrUpdateCommands(name,
                                           self.__Classification.PROPERTIES_AND_PROCESSES,
                                           content,
                                           [[self.__Classification.PANEL_OBJECTS, extraContentline]])
            else:
                # 获得port命令
                content = getPortCommands(name, self.coordinateSystem, areaName, direction,
                    isPhaseVelocity, phaseVelocity,
                    isScale, scale,
                    isFt,ftVal,
                    isGeFirst, geFirstName, geFirstVal,
                    isGeSecond, geSecondName, geSecondVal,
                    isNormalization, normalizationLine,
                    isLaplacian, laplacianFirst, laplacianSecond,
                    laplacenumber1,laplacenumber2,
                    laplacianThird, laplacianFourth,laplacianFifth,
                                          laplacenumber3,laplacenumber4,laplacenumber5,
                                          laplace_num,
                                          circuit_Checked,circuit,
                                          observe_name)

                # 更新manager
                self.__addOrUpdateCommands(name,
                                           self.__Classification.PROPERTIES_AND_PROCESSES,
                                           content)
    def updateNewMarkCommands(self, name, mark_obj, direction, isChecked_min, isChecked_mid, isChecked_max, size):
        '''
        需要额外添加的MARK命令
        '''

        content = getNewMarkCommands(name, mark_obj, direction, isChecked_min, isChecked_mid, isChecked_max, size)

        # 写完再取消注释
        self.__addOrUpdateCommands(name,
                                   self.__Classification.DEFINE_OBJECTS,
                                   content)
    def updateEmSECommands(self,name,energySec,maxNum,WEIGHT_FACTOR,ENERGY_DISTRIBUTION,min_energy,
                            max_energy,ANGLE_DISTRIBUTION,isCheck_WF=False,isCheck_ED=False,isCheck_AD=False,
                            notInclude1="未指定",notInclude2="未指定",include1="未指定",include2="未指定",Emitter="未指定",
                            isEmit = False,isExclude1 = False,isExclude2 = False,isInclude1 = False,isInclude2 = False):
        '''
        更新二次发射M3D的函数
        '''
        # FreeCAD.Console.PrintError("\n进入updateEmSECommands")
        content = getEmSECommands(name,energySec,maxNum,WEIGHT_FACTOR,ENERGY_DISTRIBUTION,min_energy,
                            max_energy,ANGLE_DISTRIBUTION,isCheck_WF,isCheck_ED,isCheck_AD,
                            notInclude1,notInclude2,include1,include2,Emitter,
                            isEmit,isExclude1,isExclude2,isInclude1,isInclude2)
        # FreeCAD.Console.PrintError("\n生成concent")
        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)
    def updateMergeCommands(self,name,Types,everyNum,maxNum):
        '''
        更新Merge的M3D的函数
        '''
        FreeCAD.Console.PrintError("\n进入加载update的数据过程")
        content = getMergeCommands(name,Types,everyNum,maxNum)    

        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)   
    def updataGasgasCommands(self,name,Types,pressure,temperature):
        '''
        更新Gasgas的M3D函数
        '''
        content = getGasgasCommands(name,Types,pressure,temperature)
        
        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content) 

    def updataSpeciesCommands(self,name,powerUnitl,quality,massUnit):
        '''
        更新Species的M3D的函数
        '''
        content = getSpeciesCommands(name,powerUnitl,quality,massUnit)
        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.COMMON_PRESETS,
                                   content) 

    def updatePopulateCommands(self,name,types,volume,X1,Y1,Z1,X2,Y2,Z2,density,temp):
        '''
        更新Populate的函数
        '''        
        content = getPopulateCommands(name,types,volume,X1,Y1,Z1,X2,Y2,Z2,density,temp)
        # FreeCAD.Console.PrintError("\n生成Populate的content")
        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content) 

    def updateFreeSpaceCommands(self,freeSpaceName, trendType, xType, component, isConductivity, funExpression,
                                isAppointArea=False, areaName="", startPointCoordinates=[], stopPointCoordinates=[],
                                isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size=""):

        # 检查必要参数是否都填入
        if isAppointArea and areaName == "":
            sayz( "FreeSpace命令生成，请检查areaName是否填入")
            return

        if not isAppointArea and startPointCoordinates == []:
            sayz("FreeSpace命令生成，请检查startPointCoordinates是否填入")
            return

        if not isAppointArea and stopPointCoordinates == []:
            sayz("FreeSpace命令生成，请检查stopPointCoordinates是否填入")
            return

        # 如果没有指定正交投影面
        if not isAppointArea:
            # 获得FreeSpace命令
            content = getFreespaceCommands(freeSpaceName, freeSpaceName, trendType, xType, component, isConductivity, funExpression)

            # 获得附加的area命令
            extraContentVolume = getConformalVolumeCommands(freeSpaceName, startPointCoordinates, stopPointCoordinates)

            # 获得附加的mark命令
            extraContentMark = getMarkCommands(freeSpaceName, isX1, isX2, isX3, X1Size, X2Size, X3Size)

            # 更新manager
            self.__addOrUpdateCommands(freeSpaceName,
                                       self.__Classification.PROPERTIES_AND_PROCESSES,
                                       content,
                                       [[self.__Classification.PANEL_OBJECTS, extraContentVolume],
                                        [self.__Classification.PANEL_OBJECTS, extraContentMark]])

        # 如果指定了正交投影面
        else:
            # 获得FreeSpace命令
            content = getFreespaceCommands(freeSpaceName, areaName, trendType, xType, component, isConductivity, funExpression)

            # 更新manager
            self.__addOrUpdateCommands(freeSpaceName,
                                       self.__Classification.PROPERTIES_AND_PROCESSES,
                                       content)


    def updateSymmetryCommands(self, name, type, trendType,
                                    isAppointArea=False, areaName="", startPointCoordinates=[], stopPointCoordinates=[],normalList=[True,False,False],
                                    appointAreaInMid="",Normal_Period="" ,isX1=False, isX2=False, isX3=False, X1Size="", X2Size="", X3Size=""):
        """
        :param name:面板名称
        :param type:对称类型 AXIAL、MIRROR、PERIODIC   
        :param trendType: 方向 POSITIVE、NEGATIVE
        :param isAppointArea: 是否指定正交投影面
        :param areaName: 若指定，正交投影面名称
        :param startPointCoordinates: 若没有指定，起点坐标列表
        :param stopPointCoordinates: 若没有指定，止点坐标列表
        :param normalList:法向方向列表
        :param appointAreaInMid: 在界面中间指定的投影面名称
        :param Normal_Period:法向周期
        :return: 
        """

        # 检查必要参数是否都填入
        if isAppointArea and areaName == "":
            sayz("Symmetry命令生成，请检查areaName是否填入")
            return

        if not isAppointArea and startPointCoordinates == []:
            sayz("Symmetry命令生成，请检查startPointCoordinates是否填入")
            return

        if not isAppointArea and stopPointCoordinates == []:
            sayz("Symmetry命令生成，请检查stopPointCoordinates是否填入")
            return

        # 如果没有指定正交投影面
        if not isAppointArea:
            # 获得Symmetry命令
            content = getSymmetryCommands(name, type, trendType, name, name+"P")
            # 获得附加的area命令
            extraContentArea = getAreaCommands(name, Area.Shape.conformal, startPointCoordinates, stopPointCoordinates,explanatoryName=name+" "+str(Normal_Period))
            extraContentAreaExtra=""
            # 如果对称类型是轴对称的话，还得再加一个面
            if type==Symmetry.Type.periodic:
                UnitType1=Modeling.Common.Tools.UnitTools.SupportUnitType.Length
                UnitType2=Modeling.Common.Tools.UnitTools.SupportUnitType.Length
                UnitType3=Modeling.Common.Tools.UnitTools.SupportUnitType.Length
                if FreeCAD.ActiveDocument.CoordinateSystem==Modeling.Common.Tools.CoordinateSystemTools.CoordinateType.Rectangular:
                    pass
                elif FreeCAD.ActiveDocument.CoordinateSystem==Modeling.Common.Tools.CoordinateSystemTools.CoordinateType.Polar:
                    UnitType2=Modeling.Common.Tools.UnitTools.SupportUnitType.Angle
                else:
                    UnitType3=Modeling.Common.Tools.UnitTools.SupportUnitType.Angle

                if normalList[0]:
                    startPointCoordinates=[Modeling.Common.Tools.UnitTools.calculator(str(startPointCoordinates[0])+"+"+str(Normal_Period),UnitType1),startPointCoordinates[1],startPointCoordinates[2]]
                    stopPointCoordinates=[Modeling.Common.Tools.UnitTools.calculator(str(stopPointCoordinates[0])+"+"+str(Normal_Period),UnitType1),stopPointCoordinates[1],stopPointCoordinates[2]]
                elif normalList[1]:
                    startPointCoordinates=[startPointCoordinates[0],Modeling.Common.Tools.UnitTools.calculator(str(startPointCoordinates[1])+"+"+str(Normal_Period),UnitType2),startPointCoordinates[2]]
                    stopPointCoordinates=[stopPointCoordinates[0],Modeling.Common.Tools.UnitTools.calculator(str(stopPointCoordinates[1])+"+"+str(Normal_Period),UnitType2),stopPointCoordinates[2]]
                else:
                    startPointCoordinates=[startPointCoordinates[0],startPointCoordinates[1],Modeling.Common.Tools.UnitTools.calculator(str(startPointCoordinates[2])+"+"+str(Normal_Period),UnitType3)]
                    stopPointCoordinates=[stopPointCoordinates[0],stopPointCoordinates[1],Modeling.Common.Tools.UnitTools.calculator(str(stopPointCoordinates[2])+"+"+str(Normal_Period),UnitType3)]
                extraContentAreaExtra = getAreaCommands(name+"P", Area.Shape.conformal, startPointCoordinates, stopPointCoordinates)
            extraContentArea=extraContentArea+extraContentAreaExtra
            # 获得附加的mark命令
            extraContentMark = getMarkCommands(name, isX1, isX2, isX3, X1Size, X2Size, X3Size)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.PROPERTIES_AND_PROCESSES,
                                       content,
                                       [[self.__Classification.PANEL_OBJECTS, extraContentArea],
                                        [self.__Classification.PANEL_OBJECTS, extraContentMark]])

        # 如果指定了正交投影面
        else:
            # 获得Symmetry命令
            content = getSymmetryCommands(name, type, trendType, areaName, appointAreaInMid)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.PROPERTIES_AND_PROCESSES,
                                       content)


    def updateDriverCommands(self, name, type, startPoints, stopPonits, currentDensity, funExpression,source_type):
        """激励电流源m3d文本写入

        :param type: 电流源类型
        :param startPoints: 起点坐标列表
        :param stopPonits: 止点坐标列表
        :param name: 名称
        :param currentDensity: 指定电流密度 
        :param funExpression: 函数表达式
        :param source_type:电流源类型所指定的具体信息
        :return: 
        """

        # 基本命令
        content = getDriverCommands(self.coordinateSystem, name, currentDensity, funExpression,source_type)
        # FreeCAD.Console.PrintError('\nDriv的content：'+str(content))

        # 附加命令
        if type == u"点电流源":
            extra = getPointCommands(name, startPoints)

        elif type == u"线电流源":
            extra = getLineCommands(name, Line.Type.conformal, startPoints, stopPonits)

        elif type == u"面电流源":
            extra = getAreaCommands(name, Area.Shape.conformal, startPoints, stopPonits)

        elif type == u"体电流源":
            extra = getConformalVolumeCommands(name, startPoints, stopPonits)
            # FreeCAD.Console.PrintError('\nDriv的extra：'+str(extra))
        else:
            extra = "error"

        # 跟新manager
        # 如果指定了source_type就不生成extra @lzg
        if source_type == '未指定':
            self.__addOrUpdateCommands(name,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content,
                                   [[self.__Classification.PANEL_OBJECTS, extra]])
        else:
            self.__addOrUpdateCommands(name,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)


    def updateFoilCommands(self, name, type, startPoints, stopPoints, thick,
                           isDIY, DITMaterial, isDefault, defaultMaterial):
        # 基本命令
        content = getFoilCommands(name, thick, isDIY, DITMaterial, isDefault, defaultMaterial,type)

        # 附加命令
        if type == u"未指定":
            extra = getConformalVolumeCommands(name, startPoints, stopPoints)

            # 跟新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.PROPERTIES_AND_PROCESSES,
                                       content,
                                       [[self.__Classification.PANEL_OBJECTS, extra]])
        else:
            # 跟新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.PROPERTIES_AND_PROCESSES,
                                       content)


    def updateInductorCommands(self, name, type, startPoints, stopPoints, diameter, isInductance, inductance):
        # 基本命令
        content = getInductorCommands(name, diameter, isInductance, inductance)

        # 附加命令
        #if type == u"未指定":
        extra = getLineCommands(name, Line.Type.conformal, startPoints, stopPoints)

        # 跟新manager
        self.__addOrUpdateCommands(name,
                                    self.__Classification.PROPERTIES_AND_PROCESSES,
                                    content,
                                    [[self.__Classification.PANEL_OBJECTS, extra]])
        # else:
        #     # 跟新manager
        #     self.__addOrUpdateCommands(name,
        #                                self.__Classification.PROPERTIES_AND_PROCESSES,
        #                                content)


    def updateEmBCommands(self, emitName, BeamJ, BeamV,
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
            isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 UNIFORM

            以下为发射区域选项
            isEmit, mobject 为发射区域选项-发射体
            isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
            isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
        """
        # 获得EmE命令
        content = getEmBCommands(self.coordinateSystem, emitName, BeamJ, BeamV,
                                 isSpecies, species,
                                 isNumber, creationRate,
                                 isTiming, timingType, stepMultiple,
                                 isSurfaceSpacing, surfaceSpacing,
                                 isOutwardSpacing, outwardSpacing, dn,
                                 isEmit, mobject,
                                 isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                                 isInclude1, includeVolume1, isInclude2, includeVolume2)
        # 更新manager
        self.__addOrUpdateCommands(emitName,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)


    def updateEmECommands(self, emitName,
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
                         isInclude1=False, includeVolume1="", isInclude2=False, includeVolume2=""):
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
        isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 UNIFORM

        以下为发射区域选项
        isEmit, mobject 为发射区域选项-发射体
        isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
        isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
        """

        # 获得EmE命令
        content = getEmECommands(self.coordinateSystem, emitName,
                                  isTField, TField,
                                  isRField, RField,
                                  isCharg, Charg,
                                  isFRate, FRate,
                                  isSpecies, species,
                                  isNumber, creationRate,
                                  isTiming, timingType, stepMultiple,
                                  isSurfaceSpacing, surfaceSpacing,
                                  isOutwardSpacing, outwardSpacing, dn,
                                  isEmit, mobject,
                                  isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                                  isInclude1, includeVolume1, isInclude2, includeVolume2)
        # 更新manager
        self.__addOrUpdateCommands(emitName,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)


    def updateEmGCommands(self, emitName, It, Bg, Pl, Pt, Dgc, pointCoordinates, isX1=False, isX2=False, isX3=False,
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
            isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 UNIFORM

            以下为发射区域选项
            isEmit, mobject 为发射区域选项-发射体
            isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
            isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
        """
        # 获得EmG命令
        content = getEmGCommands(self.coordinateSystem, emitName, It, Bg, Pl, Pt, Dgc, pointCoordinates, isX1, isX2,
                                 isX3,
                                 isSpecies, species,
                                 isNumber, creationRate,
                                 isTiming, timingType, stepMultiple,
                                 isSurfaceSpacing, surfaceSpacing,
                                 isOutwardSpacing, outwardSpacing, dn,
                                 isEmit, mobject,
                                 isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                                 isInclude1, includeVolume1, isInclude2, includeVolume2)
        # 更新manager
        self.__addOrUpdateCommands(emitName,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)


    def updateEmHCommands(self, emitName, A, B, PHI,
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
        isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 UNIFORM

        以下为发射区域选项
        isEmit, mobject 为发射区域选项-发射体
        isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
        isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
        """
        # 获得EmH命令
        content = getEmHCommands(self.coordinateSystem, emitName, A, B, PHI,
                                 isSpecies, species,
                                 isNumber, creationRate,
                                 isTiming, timingType, stepMultiple,
                                 isSurfaceSpacing, surfaceSpacing,
                                 isOutwardSpacing, outwardSpacing, dn,
                                 isEmit, mobject,
                                 isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                                 isInclude1, includeVolume1, isInclude2, includeVolume2)
        # 更新manager
        self.__addOrUpdateCommands(emitName,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)


    def updateEmTCommands(self, emitName, WF, TP,
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
            isOutwardSpacing, outwardSpacing, dn 为发射选项-沿外表面分布，outwardSpacing为 RANDOM 或 UNIFORM

            以下为发射区域选项
            isEmit, mobject 为发射区域选项-发射体
            isExclude1, excludeVolume1, isExclude2, excludeVolume2 为发射区域选项-设置不包括的投影型区域
            isInclude1, includeVolume1, isInclude2, includeVolume2 为发射区域选项-设置包括的投影型区域
        """
        # 获得EmT命令
        content = getEmTCommands(self.coordinateSystem, emitName, WF, TP,
                                 isSpecies, species,
                                 isNumber, creationRate,
                                 isTiming, timingType, stepMultiple,
                                 isSurfaceSpacing, surfaceSpacing,
                                 isOutwardSpacing, outwardSpacing, dn,
                                 isEmit, mobject,
                                 isExclude1, excludeVolume1, isExclude2, excludeVolume2,
                                 isInclude1, includeVolume1, isInclude2, includeVolume2)
        # 更新manager
        self.__addOrUpdateCommands(emitName,
                                   self.__Classification.PROPERTIES_AND_PROCESSES,
                                   content)


    def updateContourCommands(self, name, field, timerName, isShade=False,
                                   isAppointArea=False, areaName="",startPointCoordinates=[], stopPointCoordinates=[]):
        """
        
        :param name: 对应面板名称
        :param field: 对应观测场
        :param timerName: 对应定时器，默认的有 DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
        :param isShade: 对应是否等值线填充显示
        :param isAppointArea: 是否指定正交投影面
        :param areaName: 若指定，正交投影面名称
        :param startPointCoordinates: 若没有指定，起点坐标列表
        :param stopPointCoordinates: 若没有指定，止点坐标列表
        :return: 
        """

        # 检查必要参数是否都填入
        if isAppointArea and areaName=="":
            sayz("Contour命令生成，请检查areaName是否填入")
            return

        if not isAppointArea and startPointCoordinates==[]:
            sayz("Contour命令生成，请检查startPointCoordinates是否填入")
            return

        if not isAppointArea and stopPointCoordinates==[]:
            sayz("Contour命令生成，请检查stopPointCoordinates是否填入")
            return

        # 如果没有指定正交投影面
        if not isAppointArea:
            # 获得Contour命令
            content = getContourCommands(name, name, field, timerName, isShade)

            # 获得附加的area命令
            extraContent = getAreaCommands(name, Area.Shape.conformal, startPointCoordinates, stopPointCoordinates)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_CONTOUR,
                                       content,
                                       [[self.__Classification.PANEL_OBJECTS, extraContent]])

        # 如果指定了正交投影面
        else:
            # 获得Contour命令
            content = getContourCommands(name, areaName, field, timerName, isShade)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_CONTOUR,
                                       content)



    def updateVectorCommands(self, field1, field2, name, timerName, isNumber=False, number1="", number2="",
                                  isAppointArea=False, areaName="", startPointCoordinates=[], stopPointCoordinates=[]):
        """
        
        :param field1: 观测场1
        :param field2: 观测场2
        :param name: 对应面板名称
        :param timerName: 定时器，默认的有DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
        :param isNumber: 是否指定矢量个数
        :param number1: 矢量个数第一个空
        :param number2: 矢量个数第二个空
        :param isAppointArea: 是否指定正交投影面
        :param areaName: 若指定，正交投影面名称
        :param startPointCoordinates: 若没有指定，起点坐标列表
        :param stopPointCoordinates: 若没有指定，止点坐标列表
        :return: 
        """

        # 检查必要参数是否都填入
        if isAppointArea and areaName == "":
            sayz("Vector命令生成，请检查areaName是否填入")
            return

        if not isAppointArea and startPointCoordinates == []:
            sayz("Vector命令生成，请检查startPointCoordinates是否填入")
            return

        if not isAppointArea and stopPointCoordinates == []:
            sayz("Vector命令生成，请检查stopPointCoordinates是否填入")
            return

        # 如果没有指定正交投影面
        if not isAppointArea:
            # 获得vector命令
            content = getVectorCommands(name, field1, field2, name, timerName, isNumber, number1, number2)

            # 获得附加的area命令
            extraContent = getAreaCommands(name, Area.Shape.conformal, startPointCoordinates, stopPointCoordinates)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_VECTOR,
                                       content,
                                       [[self.__Classification.PANEL_OBJECTS, extraContent]])

        # 如果指定了正交投影面
        else:
            # 获得vector命令
            content = getVectorCommands(name, field1, field2, areaName, timerName, isNumber, number1, number2)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_VECTOR,
                                       content)


    def updatePhasespaceCommands(self, name, horizontalAxis, verticalAxis,
                 timerName,
                 species,
                 isThickness=False, direction="", thickness1="", thickness2="",
                 isSuffix=False, suffix=""):
        """
        :param name 面板名称
        :param horizontalAxis: 横轴显示
        :param verticalAxis: 纵轴显示
        :param timerName: 定时器,默认的有DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
        :param species: 粒子类型，ELECTRON、PROTON、ALL 中的一种
        :param isThickness: 是否显示厚度
        :param direction: 显示厚度- 方向，X1、X2、X3中的一种
        :param thickness1: 显示厚度 - 数据1
        :param thickness2: 显示厚度 - 数据2
        :param isSuffix: 是否有后缀
        :param suffix: 后缀值
        :return: 
        """

        # 获得Phasespace命令
        content = getPhasespaceCommands(name, horizontalAxis, verticalAxis, timerName, species,
                 isThickness, direction, thickness1, thickness2,
                 isSuffix, suffix)

        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.ALL_PLOTS_PHASESPACE,
                                   content)


    def updateRangeCommands(self, name, field, timerName, isFFT=False, isMagnitude=False, isComplex=False,
                                 isAppointLine=False, lineName="", startPointCoordinates=[], stopPointCoordinates=[]):
        """
        
        :param name: 面板名称
        :param field: 分类子项的具体值
        :param timerName: 定时器，默认的有DefTimer、TSYS$FIRST、TSYS$LAST，其余的可以从定时器中获取
        :param isFFT: 是否进行快速傅里叶变化
        :param isMagnitude: 是否进行实分析
        :param isComplex: 是否进行复分析
        :param isAppointLine: 是否指定正交投影面
        :param lineName: 若指定，正交投影线名称
        :param startPointCoordinates: 若没有指定，起点坐标列表
        :param stopPointCoordinates: 若没有指定，止点坐标列表
        :return: 
        """

        # 检查必要参数是否都填入
        if isAppointLine and lineName == "":
            sayz("Range命令生成，请检查lineName是否填入")
            return

        if not isAppointLine and startPointCoordinates == []:
            sayz("Range命令生成，请检查startPointCoordinates是否填入")
            return

        if not isAppointLine and stopPointCoordinates == []:
            sayz("Range命令生成，请检查stopPointCoordinates是否填入")
            return

        # 如果没有指定正交投影面
        if not isAppointLine:
            # 获得range命令
            content = getRangeCommands(name, name, field, timerName, isFFT, isMagnitude, isComplex)

            # 获得附加的line命令
            extraContent = getLineCommands(name, Line.Type.conformal, startPointCoordinates, stopPointCoordinates)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_RANGE,
                                       content,
                                       [[self.__Classification.PANEL_OBJECTS, extraContent]])

        # 如果指定了正交投影面
        else:
            # 获得range命令
            content = getRangeCommands(name, lineName, field, timerName, isFFT, isMagnitude, isComplex)

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_RANGE,
                                       content)


    def updateObserveCommands(self, name="",
                                   isField=False, isFieldIntegral=False, isFieldPower=False, isFieldEnergy=False, isParticleStatistics=False,
                                   isParticleCollected=False,isParticleEmitted=False,isParticleDestroyed=False,field="",
                                   isFFT=False, fftType="", isfreq=False,freqFrom="", freqTo="",
                                   isTime=False, timeFrom="", timeTo="",
                                   isInterval=False, interval="",
                                   isFilter=False, filterType="", timePara="",
                                   observeType="", isAppoint=False, appointName="", startPointCoordinates=[], stopPointCoordinates=[],
                                   name2 = ''):

        """
        
        :param name: 面板名称
        :param name2: 面板别名
        :param isField: 是否选择了场分类项
        :param isFieldIntegral: 是否选择了场积分分类项
        :param isFieldPower: 是否选择了场功率分类项
        :param isFieldEnergy: 是否选择了场能量分类项
        :param isEmitEps: 是否选择了EMIT_EPS
        :param field: 观测项对应的分类子项
        
        :param observeType: 观测类型，POINT \ LINE \ AREA \ VOLUME  \ EMIT
        :param isAppoint: 是否指定正交投影面
        :param appointName: 若指定，正交投影面名称
        :param startPointCoordinates: 若没有指定，起点坐标列表
        :param stopPointCoordinates: 若没有指定，止点坐标列表
        
        以下是可选项
        :param isFFT: 是否进行快速傅里叶变换
        :param fftType: FFT类型，这里的值为 MAGNITUDE（实分析）、COMPLEX（复分析）
        :param freqFrom: 频率范围起点
        :param freqTo: 频率范围终点
        :param isTime: 是否选择时间范围
        :param timeFrom: 时间范围起点
        :param timeTo: 时间范围重点
        :param isFilter: 是否数据显示平滑处理
        :param filterType: 平滑处理类型，这里的值为 STEP（时间平均）、LO_PASS（RC分析）
        :param timePara: RC分析
        
        """
        
        # 检查必要参数是否都填入
        if isAppoint and appointName == "":
            sayz("Observe命令生成，请检查areaName是否填入")
            return

        if not isAppoint and startPointCoordinates == []:
            sayz("Observe命令生成，请检查startPointCoordinates是否填入")
            return

        if not isAppoint and stopPointCoordinates == []:
            sayz("Observe命令生成，请检查stopPointCoordinates是否填入")
            return

        # 如果没有指定
        if not isAppoint:
            # 获得observe命令
            content = getObserveCommands(name, isField, isFieldIntegral, isFieldPower, isFieldEnergy, isParticleStatistics,
                        isParticleCollected,isParticleEmitted,isParticleDestroyed,
                        field, name,
                        isFFT, fftType, isfreq, freqFrom, freqTo,
                        isTime, timeFrom, timeTo,
                        isInterval, interval,
                        isFilter, filterType, timePara,
                        name2)

            # 获得附加命令
            extraContent = ""
            if observeType == "POINT":
                extraContent = getPointCommands(name, startPointCoordinates)
            elif observeType == "LINE":
                extraContent = getLineCommands(name, Line.Type.conformal, startPointCoordinates, stopPointCoordinates)
            elif observeType == "AREA":
                extraContent = getAreaCommands(name, Line.Type.conformal, startPointCoordinates, stopPointCoordinates)
            elif observeType == "VOLUME":
                extraContent = getConformalVolumeCommands(name, startPointCoordinates, stopPointCoordinates)
            else:
                return "Observe命令生成，请检查observeType"

            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_OBSERVE,
                                       content,
                                       [[self.__Classification.PANEL_OBJECTS, extraContent]])

        # 如果指定了
        else:
            # 获得observe命令
            content = getObserveCommands(name, isField, isFieldIntegral, isFieldPower, isFieldEnergy, isParticleStatistics,
                        isParticleCollected,isParticleEmitted,isParticleDestroyed,
                        field, appointName,
                        isFFT, fftType,isfreq,freqFrom, freqTo,
                        isTime, timeFrom, timeTo,
                        isInterval, interval,
                        isFilter, filterType, timePara,name2)
            # 更新manager
            self.__addOrUpdateCommands(name,
                                       self.__Classification.ALL_PLOTS_OBSERVE,
                                       content)


    def updateTimerCommands(self, timerName, type, numType, stratTime="", stopTime="", timeIncrement="", triggerTimes=""):

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

        # 获得timer命令
        content = getTimerCommands(timerName, type, numType, stratTime, stopTime, timeIncrement, triggerTimes)

        # 更新manager
        self.__addOrUpdateCommands(timerName,
                                   self.__Classification.ALL_PLOTS_TIMER,
                                   content)


    ########工程信息
    def updateWorkAreaCommands(self, name, x1Start, x1Stop, x1Step, x2Start, x2Stop, x2Step, x3Start, x3Stop, x3Step,flag):
        """
        
        :param name: 
        :param name: 名称
        :param x1Start: 第一个坐标范围起
        :param x1Stop: 第一个坐标范围至
        :param x1Step: 第一个坐标步长
        :param x2Start: 第二个坐标范围起
        :param x2Stop: 第二个坐标范围至
        :param x2Step: 第二个坐标
        :param x3Start: 第三个坐标范围起
        :param x3Stop: 第三个坐标范围至
        :param x3Step: 第三个坐标步长
        :return: 
        """
        # FreeCAD.Console.PrintMessage("\n断点\n")
        # 获得主设置区域的命令
        content=""
        if flag == True:
            content = getWorkAreaCommands(name, x1Start, x1Stop, x2Start, x2Stop, x3Start, x3Stop)
        else:
            content = "\nAUTOGRID ;\n"
            # FreeCAD.Console.PrintMessage(type(content))

        # 获得附加命令
        extra = getParameterCommands("DX1", x1Step) + \
                getParameterCommands("DX2", x2Step) + \
                getParameterCommands("DX3", x3Step)

        # 更新manager
        self.__addOrUpdateCommands("workAreaUESTC",
                                   self.__Classification.GENERATE_GRID,
                                   content,
                                   [[self.__Classification.PARAMETER, extra]])


    def updateMaterialCommands(self, name="", atomicNumber="", atomicMass="", massDensity="",
                 isConductivity=False, conductivity="",
                 isPermittivity=False, permittivity=""):

        # 获得主设置区域的命令
        content = getMaterialCommands(name, atomicNumber, atomicMass, massDensity,
                            isConductivity, conductivity,
                            isPermittivity, permittivity)
        # FreeCAD.Console.PrintError("\n" +str(name)+'     '+str(content)+'\n')

        # 更新manager
        self.__addOrUpdateCommands(name,
                                   self.__Classification.COMMON_PRESETS,
                                   content)


    def updatePresetCommands(self,
                      isSetB1=False, setB1="", isSetB2=False, setB2="", isSetB3=False, setB3="",
                      isSetE1=False, setE1="", isSetE2=False, setE2="", isSetE3=False, setE3="",
                      diySet=""):

        # 获得主设置区域的命令
        content = getPresetCommands(self.coordinateSystem,
                      isSetB1, setB1, isSetB2, setB2, isSetB3, setB3,
                      isSetE1, setE1, isSetE2, setE2, isSetE3, setE3,
                      diySet)

        # 更新manager
        self.__addOrUpdateCommands("presetUESTC",
                                   self.__Classification.COMMON_PRESETS,
                                   content)


    def updateTimeComputationCommands(self, time="", algorithm="",
                       isPattern=False, pattern="",
                       isStep=False, step="",
                       isChargeAlgorithm=False,Types = "",
                       EveryNum = "",MaxNum = "",
                       isChecked_part = False,
                       checkBoxStep = False,
                       computeTimeInterval = "1",
                       is_re = False,
                       is_nonre = False):

        # 获得主设置区域的命令
        content = getTimeComputationCommands(time, algorithm,
                                    isPattern, pattern,
                                    isStep, step,
                                    isChargeAlgorithm,
                                    Types,
                                    EveryNum,MaxNum,
                                    isChecked_part,
                                    checkBoxStep,
                                    computeTimeInterval,
                                    is_re,
                                    is_nonre)
        #FreeCAD.Console.PrintError(str(content)+'     '+str(isChargeAlgorithm)+'     '+str(step)+str(time)+'   '+str(algorithm))

        # 更新manager
        self.__addOrUpdateCommands("timeComputationUESTC",
                                   self.__Classification.SIMULATION_SETTINGS,
                                   content)


    def updateDataExportCommands(self, fileName, isObs=True, isRan=True, isCntr=True, isVec=True, isPha=True,
                          isPrefix=False, prefix="",
                          isSuffix=False, suffix="",
                          isASCII=True):

        # 获得主设置区域的命令
        content = getDataExportCommands(fileName, isObs, isRan, isCntr, isVec, isPha,
                          isPrefix, prefix,
                          isSuffix, suffix,
                          isASCII)

        # 更新manager
        self.__addOrUpdateCommands("dataExportUESTC",
                                   self.__Classification.DUMP_OPTIONS,
                                   content)


    def updateHeaderCommands(self, organization, author, device, remarks):
        # 获得主设置区域的命令
        content = getHeaderCommands(organization, author, device, remarks)

        # 更新manager
        self.__addOrUpdateCommands("headerUESTC",
                                   self.__Classification.HEADER_SYSTEM,
                                   content)


    def updateRunOptionCommands(self, isDisplay, isPause):
        # 获得主设置区域的命令
        content = getRunOptionCommands(isDisplay, isPause)

        # 更新manager
        self.__addOrUpdateCommands("runOptionUESTC",
                                   self.__Classification.RUN_OPTIONS,
                                   content)
    
    # 在批处理部分需要访问__StrInit这个类
    def getStrInit(self):
        return self.__StrInit


def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")


#===============================以下为测试代码，为了输出简洁，注释了=================================================

# test = M3DFileUtil()
#
# test.addaddOrUpdateParameter("name", "val")
#
# test.addOrUpdatePonitCommands("defPoint", ["0mm","0mm","0mm"],
#                                 isX1=False, isX2=False, isX3=False, X1Size="DX1", X2Size="DX2", X3Size="")
#
# test.addOrUpdateLineCommands("defLine", "CONFORMAL", ["0mm","0mm","0mm"], ["0mm","0mm","10mm"],
#                              isX1=True, isX2=True, isX3=False, X1Size="DX1", X2Size="DX2", X3Size="")
#
# test.addOrUpdateAreaCommands("defArea", "CONFORMAL", ["0mm","0mm","0mm"], ["0mm","0mm","10mm"],
#                              isX1=True, isX2=True, isX3=False, X1Size="DX1", X2Size="DX2", X3Size="")
#
# test.addOrUpdateConformalVolumeCommands("volumeConfo", ["0mm","0mm","0mm"], ["12mm","0mm","0mm"],
#                                            isConductor=True, isVoid=False,
#                                         isX1=True, isX2=True, isX3=False, X1Size="DX1", X2Size="DX2", X3Size="")
#
#
# test.addOrUpdateConeVolumeCommands("volumeConfo2", ["0mm","0mm","0mm"], ["12mm","0mm","0mm"], "10mm", "10mm",
#                                   isConductor=False, isVoid=True,
#                                   isX1=True, isX2=True, isX3=False, X1Size="DX1", X2Size="DX2", X3Size="")
#
# test.addOrUpdatePortCommands("port","POSITIVE",
#                       isPhaseVelocity=True, phaseVelocity="1",
#                       isScale=True, scale="2",
#                       isFt=True, ftVal="5.e5*t",
#                       isGeFirst=True, geFirstName="GE1", geFirstVal="0",
#                       isGeSecond=True, geSecondName="GE3", geSecondVal="0.0",
#                       isNormalization=True, normalizationLine="line",
#                       isLaplacian=True, laplacianFirst="va", laplacianSecond="vb",
#                       isAppointArea=False, areaName="",
#                       startPointCoordinates = ["0mm", "0mm", "0mm"], stopPointCoordinates = ["0mm", "0mm","0mm"],
#                       isX1=True, isX2=True, isX3=False, X1Size="DX1", X2Size="DX2", X3Size="")
#
# test.addOrUpdateEmECommands("ExplosiveName",
#                          isTField=True, TField="0.2",
#                          isRField=True, RField="5.23",
#                          isCharg=True, Charg="12.3",
#                          isFRate=True, FRate="12.5",
#                          isSpecies=True, species="ELECTRON",
#                          isNumber=True, creationRate="3",
#                          isTiming=True, timingType="TIMING", stepMultiple="1",
#                          isSurfaceSpacing=True, surfaceSpacing="RANDOM",
#                          isOutwardSpacing=True, outwardSpacing="RANDOM", dn="0.25",
#                          isEmit=True, mobject="obj",
#                          isExclude1=True, excludeVolume1="exv1", isExclude2=False, excludeVolume2="",
#                          isInclude1=True, includeVolume1="inv2", isInclude2=True, includeVolume2="aa")
#
#
# test.addOrUpdateContourCommands("cntr", "E1", "DefTimer", isShade=False,
#                                   isAppointArea=False, areaName="",
#                                 startPointCoordinates=["0mm","0mm","0mm"], stopPointCoordinates=["0mm","0mm","0mm"])
#
#
# test.addOrUpdateVectorCommands("E1", "E3", "vector", "TSYS$FIRST", isNumber=True, number1="20", number2="20",
#                                   isAppointArea=False, areaName="",
#                                 startPointCoordinates=["0mm","0mm","0mm"], stopPointCoordinates=["0mm","0mm","0mm"])
#
#
# test.addOrUpdatePhasespaceCommands("phase","X1", "X3","timerName", "PROTON",
#                  isThickness=True, direction="X1", thickness1="2", thickness2="3",
#                  isSuffix=True, suffix="phase")
#
# test.addOrUpdateObserveCommands(name="observe",
#                         isField=True, isFieldIntegral=False, isFieldPower=False, isFieldEnergy=False, isEmitEps=False,field="E1",
#                         isFFT=True, fftType="MAGNITUDE", freqFrom="0", freqTo="10",
#                         isTime=True, timeFrom="0", timeTo="10",
#                         isFilter=True, filterType="STEP", timePara="0.05",
#                         observeType="LINE", isAppoint=False, appointName="areaName",
#                         startPointCoordinates=["0mm", "0mm", "0mm"], stopPointCoordinates=["0mm", "0mm", "0mm"])
#
#
# test.addOrUpdateRangeCommands("range", "B1", "timerName", isFFT=True, isMagnitude=True, isComplex=False,
#                               isAppointLine=False, lineName="",
#                               startPointCoordinates=["0mm", "0mm", "0mm"], stopPointCoordinates=["0mm", "0mm", "0mm"])
#
# test.addOrUpdateSymmetryCommands("symmetry", "PERIODIC", "NEGATIVE",
#                                     isAppointArea=True, areaName="areaName",
#                                     startPointCoordinates=["0mm", "0mm", "0mm"], stopPointCoordinates=["0mm", "0mm", "0mm"],
#                                     appointAreaInMid="areaName2")
#
# test.addOrUpdateTimerCommands("timer", "PERIODIC", "INTEGER", stratTime="11", stopTime="11", timeIncrement="100", triggerTimes="")

