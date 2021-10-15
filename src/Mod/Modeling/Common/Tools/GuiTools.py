# -*- coding: utf-8 -*-

# 关于GUI的一些功能


import FreeCAD as App
import FreeCADGui as Gui

def setObjToFitTheView (obj):
    '''
    obj:    被放到适合位置的物体
    return: none
    '''
    # TypeId:对象在C++中的TypeId,本程序所有的模型均为“Part::PartFeature”
    if obj.TypeId == "Part::FeaturePython":
        #清除所有的选择
        Gui.Selection.clearSelection()
        # 增加当前选择
        Gui.Selection.addSelection(obj)
        # 将当前选择的物体放在镜头前合适位置
        Gui.SendMsgToActiveView("ViewSelection")


