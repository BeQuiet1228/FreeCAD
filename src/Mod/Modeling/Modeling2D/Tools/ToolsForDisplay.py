# -*- coding: utf-8 -*-
from Modeling.Modeling2D.Tools import Tools2D
import FreeCAD


def setColors(obj):
    """
    根据obj的Attribute设置颜色
    """
    # noinspection PyBroadException
    try:
        if not hasattr(obj, "Attribute") or not hasattr(obj, "ViewObject"):
            return
        if obj.Attribute == Tools2D.Attribute.NotDefine:
            obj.ViewObject.ShapeColor = (0.047059, 0.047059, 0.800000)  # 蓝色
        elif obj.Attribute == Tools2D.Attribute.Conductor:
            obj.ViewObject.ShapeColor = (0.803922, 0.803922, 0.803922)  # 金属色
        elif obj.Attribute == Tools2D.Attribute.Custom:
            obj.ViewObject.ShapeColor = (0.047059, 0.800000, 0.047059)  # 绿色
        elif obj.Attribute == Tools2D.Attribute.Vacuo or obj.Attribute == Tools2D.Attribute.Void:
            obj.ViewObject.ShapeColor = (1.000000, 1.000000, 1.000000)  # 白色
    except:
        FreeCAD.Console.PrintError("设置颜色时出现错误")
