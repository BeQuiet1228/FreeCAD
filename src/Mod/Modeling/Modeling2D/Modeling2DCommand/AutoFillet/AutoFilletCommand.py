# encoding:utf-8
import math

import FreeCAD
import FreeCADGui


# import Modeling.Modeling2D.Modeling2DCommand.Fillet.FilletInstance as Fillet


# class AutoFilletCommand:
#     """
#     注册倒角命令
#     """
#     def IsActive(self):
#         if FreeCADGui.ActiveDocument:
#             return True
#         else:
#             return False
#
#     def Activated(self):
#         # createAutoFillet()
#
#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/foil.svg"
#         MenuText = Tools2D.QT_TRANSLATE_NOOP(
#             'CreateAutoFillet',
#             '倒角')
#         ToolTip = Tools2D.QT_TRANSLATE_NOOP(
#             'CreateAutoFillet',
#             '倒角')
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}
#
#
# FreeCADGui.addCommand('CreateAutoFillet', AutoFilletCommand())


# 应急之举
def createAutoFillet(obj, num, radius):
    """
    创建一个自动的倒角功能
    :param radius: 倒角的半径
    :param obj: 被倒角的体
    :param num: 第几个角，从最左下角开始顺时针计算
    :return: 被创建好的倒角，attribute为void
    """
    import Modeling.Modeling2D.Modeling2DCommand.Fillet.FilletInstance as Fillet
    from Modeling.Modeling2D.Tools import Tools2D, ToolsUI

    point_x_outside = None
    point_y_outside = None
    point_x_inside = None
    point_y_inside = None
    fillet_obj = Fillet.getObject()
    if num == 1:
        # 获取第num个角度对应的坐标值
        point_x_outside = min(obj.Point1X.Value, obj.Point2X.Value)
        point_y_outside = min(obj.Point1Y.Value, obj.Point2Y.Value)
        point_x_inside = point_x_outside + radius
        point_y_inside = point_y_outside + radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(180)
        fillet_obj.user_endAngle = str(270)

    elif num == 2:
        point_x_outside = min(obj.Point1X.Value, obj.Point2X.Value)
        point_y_outside = max(obj.Point1Y.Value, obj.Point2Y.Value)
        point_x_inside = point_x_outside + radius
        point_y_inside = point_y_outside - radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(90)
        fillet_obj.user_endAngle = str(180)

    elif num == 3:
        point_x_outside = max(obj.Point1X.Value, obj.Point2X.Value)
        point_y_outside = max(obj.Point1Y.Value, obj.Point2Y.Value)
        point_x_inside = point_x_outside - radius
        point_y_inside = point_y_outside - radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(0)
        fillet_obj.user_endAngle = str(90)

    elif num == 4:
        point_x_outside = max(obj.Point1X.Value, obj.Point2X.Value)
        point_y_outside = min(obj.Point1Y.Value, obj.Point2Y.Value)
        point_x_inside = point_x_outside - radius
        point_y_inside = point_y_outside + radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(270)
        fillet_obj.user_endAngle = str(360)

    else:
        return

    fillet_obj.Attribute = "Void"
    ToolsUI.setPlaceToObj(fillet_obj, "Point1X", fillet_obj.user_point1_x)
    ToolsUI.setPlaceToObj(fillet_obj, "Point1Y", fillet_obj.user_point1_y)
    ToolsUI.setPlaceToObj(fillet_obj, "Point2X", fillet_obj.user_point2_x)
    ToolsUI.setPlaceToObj(fillet_obj, "Point2Y", fillet_obj.user_point2_y)
    ToolsUI.setPlaceToObj(fillet_obj, "Radius", fillet_obj.user_radius)
    ToolsUI.setAngleToObj(fillet_obj, "StartAngle", fillet_obj.user_startAngle)
    ToolsUI.setAngleToObj(fillet_obj, "EndAngle", fillet_obj.user_endAngle)

    fillet_obj.recompute()


def createAutoFilletForPolygonal(obj, num, radius):
    """
    为多边形自动创建倒角
    :param obj: 多边形对象
    :param num: 第几个角，如果是第n个角，则对应第 n-1, n, n+1 个点对应的角
    :param radius: 倒角的半径
    :return:
    """
    import Modeling.Modeling2D.Modeling2DCommand.Fillet.FilletInstance as Fillet
    from Modeling.Modeling2D.Tools import Tools2D, ToolsUI

    points = obj.Points         # 点坐标的list
    points_len = len(points)    # 点坐标的数量，如果有 n 个点，则长度为 n+1，因为首尾需要相连

    if num > points_len:
        # 传入参数错误
        Tools2D.sayz("参数错误，不再自动添加倒角")
        return

    point_1 = None
    point_2 = None
    point_3 = None

    if num == 1:
        point_1 = points[-1]
        point_2 = points[num - 1]
        point_3 = points[num]
    elif num == points_len:
        point_1 = points[num - 2]
        point_2 = points[num - 1]
        point_3 = points[0]
    else:
        point_1 = points[num - 2]
        point_2 = points[num - 1]
        point_3 = points[num]

    fillet_obj = Fillet.getObject()
    different = 0.00000001      # 用于判断浮点数“相等”的精度
    # 为了保持与之前代码类似
    point_x_outside = None
    point_y_outside = None
    point_x_inside = None
    point_y_inside = None

    # 判断三个点是否构成直角，并且判断是否平行
    # 类似于正投影面的第一个角
    if ((abs(point_1[0] - point_2[0]) <= different) and (abs(point_2[1] - point_3[1]) <= different) and \
       (point_1[1] - point_2[1] > 0) and (point_2[0] - point_3[0] < 0)) or \
       ((abs(point_3[0] - point_2[0]) <= different) and (abs(point_2[1] - point_1[1]) <= different) and \
       (point_3[1] - point_2[1] > 0) and (point_2[0] - point_1[0] < 0)):

        Tools2D.sayz("daojiao 111")
        point_x_outside = point_2[0]
        point_y_outside = point_2[1]
        point_x_inside = point_x_outside + radius
        point_y_inside = point_y_outside + radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(180)
        fillet_obj.user_endAngle = str(270)
    # 类似于正投影面的第二个角
    elif ((abs(point_2[0] - point_1[0]) <= different) and (abs(point_2[1] - point_3[1]) <= different) and \
         (point_2[1] - point_1[1] > 0) and (point_2[0] - point_3[0] < 0)) or \
         ((abs(point_2[0] - point_3[0]) <= different) and (abs(point_2[1] - point_1[1]) <= different) and \
         (point_2[1] - point_3[1] > 0) and (point_2[0] - point_1[0] < 0)):

        Tools2D.sayz("daojiao 222")
        point_x_outside = point_2[0]
        point_y_outside = point_2[1]
        point_x_inside = point_x_outside + radius
        point_y_inside = point_y_outside - radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(90)
        fillet_obj.user_endAngle = str(180)
    # 类似于正投影面的第三个角
    elif ((abs(point_2[1] - point_1[1]) <= different) and (abs(point_2[0] - point_3[0]) <= different) and \
         (point_1[0] - point_2[0] < 0) and (point_2[1] - point_3[1] > 0)) or \
         ((abs(point_2[1] - point_3[1]) <= different) and (abs(point_2[0] - point_1[0]) <= different) and \
         (point_3[0] - point_2[0] < 0) and (point_2[1] - point_1[1] > 0)):

        Tools2D.sayz("daojiao 333")
        point_x_outside = point_2[0]
        point_y_outside = point_2[1]
        point_x_inside = point_x_outside - radius
        point_y_inside = point_y_outside - radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(0)
        fillet_obj.user_endAngle = str(90)
    # 类似于正投影面的第四个角
    elif ((abs(point_2[0] - point_1[0]) <= different) and (abs(point_2[1] - point_3[1]) <= different) and \
         (point_1[1] - point_2[1] > 0) and (point_3[0] - point_2[0] < 0)) or \
         ((abs(point_2[0] - point_3[0]) <= different) and (abs(point_2[1] - point_1[1]) <= different) and \
         (point_1[0] - point_2[0] < 0) and (point_3[1] - point_2[1] > 0)):

        Tools2D.sayz("daojiao 444")
        point_x_outside = point_2[0]
        point_y_outside = point_2[1]
        point_x_inside = point_x_outside - radius
        point_y_inside = point_y_outside + radius

        fillet_obj.user_point1_x = str(point_x_inside)
        fillet_obj.user_point1_y = str(point_y_inside)
        fillet_obj.user_point2_x = str(point_x_outside)
        fillet_obj.user_point2_y = str(point_y_outside)
        fillet_obj.user_radius = str(radius)
        fillet_obj.user_startAngle = str(270)
        fillet_obj.user_endAngle = str(360)

    else:
        Tools2D.sayz("错误的if语句导致结束")
        return

    fillet_obj.Attribute = "Void"
    ToolsUI.setPlaceToObj(fillet_obj, "Point1X", fillet_obj.user_point1_x)
    ToolsUI.setPlaceToObj(fillet_obj, "Point1Y", fillet_obj.user_point1_y)
    ToolsUI.setPlaceToObj(fillet_obj, "Point2X", fillet_obj.user_point2_x)
    ToolsUI.setPlaceToObj(fillet_obj, "Point2Y", fillet_obj.user_point2_y)
    ToolsUI.setPlaceToObj(fillet_obj, "Radius", fillet_obj.user_radius)
    ToolsUI.setAngleToObj(fillet_obj, "StartAngle", fillet_obj.user_startAngle)
    ToolsUI.setAngleToObj(fillet_obj, "EndAngle", fillet_obj.user_endAngle)

    fillet_obj.recompute()





