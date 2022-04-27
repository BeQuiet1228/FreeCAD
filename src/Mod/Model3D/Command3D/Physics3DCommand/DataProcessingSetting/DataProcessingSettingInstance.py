#-*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import ObjectTools, InitDoc3D


class DataProcessingSetting(object):
    def __init__(self):
        self.obj = FreeCAD.ActiveDocument.getObject("dataProcess")
        if self.obj is None:
            self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "dataProcess")
            self.__setProperty()
        InitDoc3D.addObjectToGroup_helper(self.obj, "DataProcess", "数据导出设定")

    def __setProperty(self):

        # 此处type通过一个枚举类来进行赋值
        self.obj.addProperty("App::PropertyString", "Type").Type = ObjectTools.ObjectType.DataProcess
        # stringList是一个列表，类型箔片会有很多指定类型
        self.obj.addProperty("App::PropertyBool", "isCheckBox_Time_obser").isCheckBox_Time_obser = False
        self.obj.addProperty("App::PropertyBool", "isCheckBox_space_obser").isCheckBox_space_obser = False
        self.obj.addProperty("App::PropertyBool", "isCheckBox_contor_plot").isCheckBox_contor_plot = False
        self.obj.addProperty("App::PropertyBool", "isCheckBox_vector_data").isCheckBox_vector_data = False
        self.obj.addProperty("App::PropertyBool", "isCheckBox_phase_space").isCheckBox_phase_space = False
        self.obj.addProperty("App::PropertyBool", "isCheckBox_set_prefix").isCheckBox_set_prefix = False
        self.obj.addProperty("App::PropertyBool", "isCheckBox_set_suffix").isCheckBox_set_suffix = False
        self.obj.addProperty("App::PropertyString", "prefiX").prefiX = ""
        self.obj.addProperty("App::PropertyString", "suffiX").suffiX = ""
        self.obj.addProperty("App::PropertyBool", "isCheckBox_text").isCheckBox_text = True
        self.obj.addProperty("App::PropertyBool", "isCheckBox_binary").isCheckBox_binary = False
        if not hasattr(self.obj, "Project"):
            self.obj.addProperty("App::PropertyString", "Project")

def getObject():
    """
    创建obj并添加与Foil相关的属性，然后返回obj
    """
    DataProcessingSettingIns = DataProcessingSetting()
    return DataProcessingSettingIns.obj
