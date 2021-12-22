# -*- coding: utf-8 -*-
# by wzn

from File.FileCommand.M3DFile.ParseM3DFile import ParseM3DFile
import Modeling.Common.Tools.ModelingByM3dFile as ModelingByM3dFile
import Physics.PhysicsCommand.BuildPanelsByM3dFile as BuildPhysicsByM3dFile
import ProjectSetting.Commands.BuildPanelsByM3dFile as BuildSettingsByM3dFile

def open(filename):
    # print(filename)
    # 获得一个解析文件的工具类对象
    parseM3DFile = ParseM3DFile()

    # 设置文件路径，并加载文件内容
    parseM3DFile.path = filename
    fileStrList =  parseM3DFile.getFileContent()
    m3dfileStrList = []
    # 去掉最后的换行符
    for i in range(len(fileStrList)):
        if fileStrList[i].startswith("##"):
            str = fileStrList[i][2:]
            m3dfileStrList.append(str)
    parseM3DFile.setfileStrList(m3dfileStrList)


    # 将字符串分类
    parseM3DFile.sortCommands()

    # 解析
    # 1.解析出坐标系
    coordinateSystem = parseM3DFile.getCoordinateSystem()
    # 2.解析自定义全局变量
    globalVariableList = parseM3DFile.getGlobalVariableList()
    # 3.解析模型
    modlelingParameterList = parseM3DFile.getModlelingParameterList()
    # 4.解析工程性质面板
    projectSettingList = parseM3DFile.getProjectSettingList()
    # 5.解析物理面板
    physicsParameterList = parseM3DFile.getPhysicsParameterList()

    # 重建
    # 1.新建文档
    ModelingByM3dFile.newDoc(coordinateSystem)
    # 2.重建自定义全局变量
    ModelingByM3dFile.setGlobalVariable(globalVariableList)
    # 3.重建模型
    ModelingByM3dFile.modelingByParameter(modlelingParameterList)
    # 4.重建工程性质面板
    BuildSettingsByM3dFile.setPanelsByParameter(projectSettingList)
    # 5.重建物理面板
    BuildPhysicsByM3dFile.setPanelsByParameter(physicsParameterList)