# -*- coding: utf-8 -*-
import FreeCAD

from Modeling.Modeling2D.Tools import Tools2D
# 定义obj类型
from Modeling.Modeling2D.Tools import ExpressionTools

# 在此处添加的helper是为了辅助模型使用表达式，草图建模出来的模型的坐标一般只能使用浮点型
def processObject(obj, type_str):
    """
    根据type_str判断obj的种类, type_str -> str
    为obj添加所需的属性，并打开ui
    """

    if type_str == "Circular":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.AreaCircular
        obj.addProperty("App::PropertyDistance", "x_helper", "NonUniformGrid", "").x_helper = obj.Placement.Base.x
        obj.addProperty("App::PropertyDistance", "y_helper", "NonUniformGrid", "").y_helper = obj.Placement.Base.y
        length = ExpressionTools.currentLengthUnits()
        obj.addProperty("App::PropertyString", "user_radius").user_radius = str(obj.Radius.getValueAs(length)) + length
        Tools2D.addUserProperty(obj, 1)
        Tools2D.defaultSettingForCircle(obj)
    elif type_str == "Line":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.Line
        obj.addProperty("App::PropertyDistance", "x1_helper", "NonUniformGrid", "").x1_helper = obj.Start.x
        obj.addProperty("App::PropertyDistance", "y1_helper", "NonUniformGrid", "").y1_helper = obj.Start.y
        obj.addProperty("App::PropertyDistance", "x2_helper", "NonUniformGrid", "").x2_helper = obj.End.x
        obj.addProperty("App::PropertyDistance", "y2_helper", "NonUniformGrid", "").y2_helper = obj.End.y
        changeLineStyle(obj)
        Tools2D.addUserProperty(obj, 2)
        Tools2D.defaultSettingForLine(obj)
    elif type_str == "LineConformal":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.LineConformal
        obj.addProperty("App::PropertyDistance", "x1_helper", "NonUniformGrid", "").x1_helper = obj.Start.x
        obj.addProperty("App::PropertyDistance", "y1_helper", "NonUniformGrid", "").y1_helper = obj.Start.y
        obj.addProperty("App::PropertyDistance", "x2_helper", "NonUniformGrid", "").x2_helper = obj.End.x
        obj.addProperty("App::PropertyDistance", "y2_helper", "NonUniformGrid", "").y2_helper = obj.End.y
        obj.addProperty("App::PropertyString", "normal", "NonUniformGrid", "")
        changeLineStyle(obj)
        Tools2D.addUserProperty(obj, 2)
        Tools2D.defaultSettingForLine(obj)
    elif type_str == "AreaPolygonal":
        # 注意helper的命名是从0开始的！！！
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.AreaPolygonal
        for i in range(len(obj.Points)):
            obj.addProperty("App::PropertyVectorDistance", "helper_" + str(i), "NonUniformGrid", "")
            setattr(obj, "helper_" + str(i), obj.Points[i])
        Tools2D.addUserProperty(obj, len(obj.Points))
        Tools2D.defaultSettingForPolygonal(obj)
    elif type_str == "Rectangle":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.Rectangle
        Tools2D.addUserProperty(obj, 2)
        Tools2D.defaultSettingForArea(obj)
    elif type_str == "AreaConformal":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.AreaConformal
        Tools2D.addUserProperty(obj, 2)
        Tools2D.defaultSettingForArea(obj)
    elif type_str == "RegularPolygon":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.RegularPolygon
    elif type_str == "Sector":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.Sector
        length = ExpressionTools.currentLengthUnits()
        obj.addProperty("App::PropertyString", "user_radius").user_radius = str(obj.Radius.getValueAs(length)) + length
        Tools2D.addUserProperty(obj, 1)
        Tools2D.defaultSettingForPoint(obj)
    elif type_str == "Point":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.Point
        Tools2D.addUserProperty(obj, 1)
        Tools2D.defaultSettingForPoint(obj)
    elif type_str == "Fillet":
        obj.addProperty("App::PropertyString", "Type").Type = Tools2D.ObjectType.Fillet
        length = ExpressionTools.currentLengthUnits()
        obj.addProperty("App::PropertyString", "user_radius").user_radius = str(obj.Radius.getValueAs(length)) + length
        obj.addProperty("App::PropertyString", "user_startAngle").user_startAngle = "0"
        obj.addProperty("App::PropertyString", "user_endAngle").user_endAngle = "90"
        Tools2D.addUserProperty(obj, 2)
        Tools2D.defaultSettingForArea(obj)

    Tools2D.addAttributeToObject(obj)
    Tools2D.addCommonPropertyToObject(obj)


# 改变线的风格样式
def changeLineStyle(obj):
    obj.ViewObject.Deviation = 0.2
    obj.ViewObject.DrawStyle = "Dotted"
    obj.ViewObject.LineWidth = 5

