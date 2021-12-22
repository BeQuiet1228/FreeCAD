# -*- coding: utf-8 -*-
# by maxin
import FreeCAD
from File.FileCommand.M3DFile.ParseM3DFile import ParseM3DFile
from File.FileCommand.M3DFile.M3DFileUtil import M3DFileUtil
import Modeling.Common.Tools.ModelingByM3dFile as ModelingByM3dFile
import Physics.PhysicsCommand.BuildPanelsByM3dFile as BuildPhysicsByM3dFile
import ProjectSetting.Commands.BuildPanelsByM3dFile as BuildSettingsByM3dFile

import Modeling.Common.Tools.DocumentTools as DocumentTools
def clientSetWorkpath(workpath):
    FreeCAD.clientSetWorkpath(workpath)
def open(filename):
    # print(filename)
    # 获得一个解析文件的工具类对象
    parseM3DFile = ParseM3DFile()
    
    # 设置文件路径，并加载文件内容
    parseM3DFile.path = filename
    parseM3DFile.getFileContent()
    
    # 将字符串分类
    parseM3DFile.sortCommands()
    
    # 解析
    # 1.解析出坐标系
    coordinateSystem = parseM3DFile.getCoordinateSystem()

    # 2.解析自定义全局变量
    globalVariableList = parseM3DFile.getGlobalVariableList()
    # FreeCAD.Console.PrintMessage("\nglobalVariablieList:\n")
    # FreeCAD.Console.PrintMessage(globalVariableList)
    # 3.解析模型
    modlelingParameterList = parseM3DFile.getModlelingParameterList()
    FreeCAD.Console.PrintMessage("\nmodelingParameterList:\n")
    FreeCAD.Console.PrintMessage(modlelingParameterList)
    # 4.解析工程性质面板
    projectSettingList = parseM3DFile.getProjectSettingList()
    # FreeCAD.Console.PrintMessage("\nprojectSettingList:\n")
    # FreeCAD.Console.PrintMessage(projectSettingList)
    # 5.解析物理面板
    physicsParameterList = parseM3DFile.getPhysicsParameterList()
    # FreeCAD.Console.PrintMessage("\nphysicsParameterList:\n")
    # FreeCAD.Console.PrintMessage(physicsParameterList)
    # 重建
    # 1.新建文档
    ModelingByM3dFile.newDoc(coordinateSystem)
    # 2.重建自定义全局变量
    ModelingByM3dFile.setGlobalVariable(globalVariableList)
    # 3.重建模型
    # FreeCAD.Console.PrintMessage(modlelingParameterList)
    # 在这里我需要知道阵列体是如何构建的，它的‘i’是如何发挥作用的
    # 然后完成参数阵列体的构建，我认为这里我可能会重写modelingByParameter函数
    ModelingByM3dFile.modelingByParameter(modlelingParameterList)
    # 4.重建工程性质面板
    BuildSettingsByM3dFile.setPanelsByParameter(projectSettingList)
    # 5.重建物理面板
    BuildPhysicsByM3dFile.setPanelsByParameter(physicsParameterList)
    
    # 为工程添加最后的设置
    DocumentTools.finalSettingByRebuildByM3d()

def export(objectslist, filename):
    # 获得一个m3d util
    m3DFileUtil = M3DFileUtil()

    # 重新设置m3d文件路径
    m3DFileUtil.path = filename

    # 保存m3d文件
    m3DFileUtil.writeToFile()