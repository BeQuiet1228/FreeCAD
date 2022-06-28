# -*- coding:utf-8 -*-
# @Time: 2020/11/2 09:15
# @Author: lilei
# @File: DataExportSettingInstance.py
import FreeCAD
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Modeling.Modeling2D.Tools import Tools2D


class DataExportSetting(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("dataProcess")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "dataProcess")
            self.__setProperty()

    def __setProperty(self):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectType.DataProcess
        self.obj.addProperty("App::PropertyBool", "isTimeObservation").isTimeObservation = False
        self.obj.addProperty("App::PropertyBool", "isSpaceObservation").isSpaceObservation = False
        self.obj.addProperty("App::PropertyBool", "isAllelicChartData").isAllelicChartData = False
        self.obj.addProperty("App::PropertyBool", "isVectorGraphData").isVectorGraphData = False
        self.obj.addProperty("App::PropertyBool", "isPhaseSpatialData").isPhaseSpatialData = False
        self.obj.addProperty("App::PropertyBool", "isSetFilePrefix").isSetFilePrefix = False
        self.obj.addProperty("App::PropertyString", "setFilePrefix").setFilePrefix = ""

        self.obj.addProperty("App::PropertyBool", "isFileSuffixes").isFileSuffixes = False
        self.obj.addProperty("App::PropertyString", "fileSuffixes").fileSuffixes = ""
        self.obj.addProperty("App::PropertyBool", "isTextFormat").isTextFormat = True
        self.obj.addProperty("App::PropertyBool", "isBinaryFormat").isBinaryFormat = False


def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    dataExportIns = DataExportSetting()
    return dataExportIns.obj

