# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, Tools3D, InitDoc3D


class NetStepSetting(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("SIMUVOLUME")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "SIMUVOLUME")
            self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Simu", "工作区间设置")

    def __setProperty(self, obj):
        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.Simu
        # stringList是一个列表，类型箔片会有很多指定类型
        if FreeCAD.ActiveDocument.CoordinateSystem == 'Rectangular':
            self.obj.addProperty("App::PropertyString", "stepSizeX").stepSizeX = "1mm"
            self.obj.addProperty("App::PropertyString", "stepSizeY").stepSizeY = "1mm"
            self.obj.addProperty("App::PropertyString", "stepSizeZ").stepSizeZ = "1mm"
        elif FreeCAD.ActiveDocument.CoordinateSystem == 'Polar':
            self.obj.addProperty("App::PropertyString", "stepSizeX").stepSizeX = "1mm"
            self.obj.addProperty("App::PropertyString", "stepSizeY").stepSizeY = "1deg"
            self.obj.addProperty("App::PropertyString", "stepSizeZ").stepSizeZ = "1mm"
        else:
            self.obj.addProperty("App::PropertyString", "stepSizeX").stepSizeX = "1mm"
            self.obj.addProperty("App::PropertyString", "stepSizeY").stepSizeY = "1mm"
            self.obj.addProperty("App::PropertyString", "stepSizeZ").stepSizeZ = "1deg"
        self.obj.addProperty("App::PropertyBool", "isStartUsing").isStartUsing = False
        Tools3D.addCommonStartEndCoordinate(obj)
        if not hasattr(obj, "Project"):
            self.obj.addProperty("App::PropertyString", "Project")


def getObject():
    netStepSettingIns = NetStepSetting()
    return netStepSettingIns.obj
