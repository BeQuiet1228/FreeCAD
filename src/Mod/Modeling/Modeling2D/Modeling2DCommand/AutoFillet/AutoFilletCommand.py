# encoding:utf-8
import math
import FreeCAD
import FreeCADGui
import Part
from Modeling.Modeling2D.Modeling2DCommand.testFillet import make_fiilet
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI
from Modeling.Modeling2D.Modeling2DCommand.Fillet import FilletInstance


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
    fillet_obj.IsAutoFillet = True
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


def radianToAngle(radian):
    return radian*180/math.pi%360


def getFillet(p4, p2, r, start_angle, end_angle):
    fillet_obj = FilletInstance.getObject()
    fillet_obj.user_point1_x = str(p4.x)
    fillet_obj.user_point1_y = str(p4.y)
    fillet_obj.user_point2_x = str(p2.x)
    fillet_obj.user_point2_y = str(p2.y)
    fillet_obj.user_radius = str(r)
    fillet_obj.user_startAngle = str(start_angle)
    fillet_obj.user_endAngle = str(end_angle)
    fillet_obj.Attribute = "Void"
    ToolsUI.setPlaceToObj(fillet_obj, "Point1X", fillet_obj.user_point1_x)
    ToolsUI.setPlaceToObj(fillet_obj, "Point1Y", fillet_obj.user_point1_y)
    ToolsUI.setPlaceToObj(fillet_obj, "Point2X", fillet_obj.user_point2_x)
    ToolsUI.setPlaceToObj(fillet_obj, "Point2Y", fillet_obj.user_point2_y)
    ToolsUI.setPlaceToObj(fillet_obj, "Radius", fillet_obj.user_radius)
    ToolsUI.setAngleToObj(fillet_obj, "StartAngle", fillet_obj.user_startAngle)
    ToolsUI.setAngleToObj(fillet_obj, "EndAngle", fillet_obj.user_endAngle)
    fillet_obj.recompute()


# 对多边形自动倒角做的处理 @wzg 2021.11.24
def setAutoFillet(obj, num, radius):
    n = len(obj.Points)
    # 多边形的三个点，围成一个角
    p1 = obj.Points[(num - 2) % n]
    p2 = obj.Points[(num - 1) % n]
    p3 = obj.Points[num % n]
    # 调用之前的函数，测试成功后，再优化函数
    line1 = Part.LineSegment(p1, p2)
    line2 = Part.LineSegment(p2, p3)
    line1 = line1.toShape()
    line2 = line2.toShape()
    # 返回4个点，弧上三个点，圆心一个点。顺序为左中右，圆心
    arc_list = make_fiilet.fillet([line1, line2], radius, False)
    arc_point1 = arc_list[0]
    arc_point2 = arc_list[1]
    arc_point3 = arc_list[2]
    arc_center = arc_list[3]
    # 假如是逆时针
    temp1_angle = arc_point1.sub(arc_center)
    temp2_angle = p2.sub(arc_center)
    temp3_angle = arc_point3.sub(arc_center)
    start_angle = radianToAngle(math.atan2(temp1_angle.y, temp1_angle.x))
    mid_angle = radianToAngle(math.atan2(temp2_angle.y, temp2_angle.x))
    end_angle = radianToAngle(math.atan2(temp3_angle.y, temp3_angle.x))
    mid_quadrant=1
    start_quadrant = 1
    end_quadrant = 1
    # 浮点数比较大小，需设置精度，测试成功后，再做处理
    if 0<=mid_angle<=90:
        mid_quadrant = 1
        mid_vec = FreeCAD.Vector(radius, radius, 0)
    elif 90<mid_angle<=180:
        mid_quadrant = 2
        mid_vec = FreeCAD.Vector(-radius, radius, 0)
    elif 180<mid_angle<=270:
        mid_quadrant = 3
        mid_vec = FreeCAD.Vector(-radius, -radius, 0)
    elif 270<mid_angle<=360:
        mid_quadrant = 4
        mid_vec = FreeCAD.Vector(radius, -radius, 0)
    else:
        Tools2D.sayz("中间角度计算错误")

    Tools2D.sayz("start_angle=" + str(start_angle))
    if 0<=start_angle<=90:
        start_quadrant = 1
    elif 90<start_angle<=180:
        start_quadrant = 2
    elif 180<start_angle<=270:
        start_quadrant = 3
    elif 270<start_angle<=360:
        start_quadrant = 4
    else:
        Tools2D.sayz("起始角度计算错误")
    Tools2D.sayz("end_angle="+str(end_angle))
    if 0<=end_angle<=90:
        end_quadrant = 1
    elif 90<end_angle<=180:
        end_quadrant = 2
    elif 180<end_angle<=270:
        end_quadrant = 3
    elif 270<end_angle<=360:
        end_quadrant = 4
    else:
        Tools2D.sayz("结束角度计算错误")
    Tools2D.sayz("end_quadrant=" + str(end_quadrant))
    Tools2D.sayz("start_quadrant="+str(start_quadrant))
    # 解决精度问题
    if abs(mid_angle-90)<0.00000001:
        mid_angle=90
        mid_quadrant=1
    if abs(mid_angle-180)<0.0000001:
        mid_angle=180
        mid_quadrant=2
    if abs(mid_angle-270)<0.0000001:
        mid_angle=270
        mid_quadrant=3

    if abs(start_angle-90)<0.00000001:
        start_angle=90
        start_quadrant=1
    if abs(start_angle-180)<0.0000001:
        start_angle=180
        start_quadrant=2
    if abs(start_angle-270)<0.0000001:
        start_angle=270
        start_quadrant=3

    if abs(end_angle-90)<0.00000001:
        end_angle=90
        end_quadrant=1
    if abs(end_angle-180)<0.0000001:
        end_angle=180
        end_quadrant=2
    if abs(end_angle-270)<0.0000001:
        end_angle=270
        end_quadrant=3

    # 解决顺时针建模，和逆时针建模，起始，结束角度相反的问题
    if mid_quadrant == 1:
        if (start_quadrant==1 and end_quadrant==1 and end_angle<start_angle) \
                or end_quadrant==4 or (start_quadrant==2 and end_quadrant==1):
            start_angle, end_angle = end_angle, start_angle
            start_quadrant, end_quadrant = end_quadrant, start_quadrant
    elif mid_quadrant == 2:
        if (end_quadrant==2 and end_angle<start_angle) or end_quadrant==1:
            start_angle, end_angle = end_angle, start_angle
            start_quadrant, end_quadrant = end_quadrant, start_quadrant
    elif mid_quadrant == 3:
        if (end_quadrant==3 and end_angle<start_angle) or end_quadrant==2:
            start_angle, end_angle = end_angle, start_angle
            start_quadrant, end_quadrant = end_quadrant, start_quadrant
    else:
        if (start_quadrant==4 and end_quadrant==4 and end_angle<start_angle) or \
                end_quadrant==3 or (end_quadrant==4 and start_quadrant==1):
            start_angle, end_angle = end_angle, start_angle
            start_quadrant, end_quadrant = end_quadrant, start_quadrant

    if mid_quadrant == 1:
        p2_mid = p2.add(mid_vec)
        # 中间象限是第1象限时，结束象限只能是第1，2象限
        if end_quadrant == 1:
            if start_quadrant == 4:
                p2_4 = FreeCAD.Vector(p2_mid.x, arc_center.y-radius, 0)
                getFillet(arc_center, p2_4, radius, start_angle, 360)
                getFillet(arc_center, p2_mid, radius, 0, end_angle)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, end_angle)
        else:
            if start_quadrant == 4:
                p2_4 = FreeCAD.Vector(p2_mid.x, arc_center.y - radius, 0)
                getFillet(arc_center, p2_4, radius, start_angle, 360)
                getFillet(arc_center, p2_mid, radius, 0, 90)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, 90)
            p2_2 = FreeCAD.Vector(arc_center.x-radius, p2_mid.y, 0)
            getFillet(arc_center, p2_2, radius, 90, end_angle)

    elif mid_quadrant == 2:
        p2_mid = p2.add(mid_vec)
        # 中间象限是第2象限，结束象限只能第2，3象限
        if end_quadrant == 2:
            if start_quadrant == 1:
                p2_1 = FreeCAD.Vector(arc_center.x+radius, p2_mid.y, 0)
                if start_angle!=90:
                    getFillet(arc_center, p2_1, radius, start_angle, 90)
                getFillet(arc_center, p2_mid, radius, 90, end_angle)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, end_angle)
        else:
            if start_quadrant == 1:
                p2_1 = FreeCAD.Vector(arc_center.x + radius, p2_mid.y, 0)
                if start_angle!=90:
                    getFillet(arc_center, p2_1, radius, start_angle, 90)
                getFillet(arc_center, p2_mid, radius, 90, 180)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, 180)
            p2_3 = FreeCAD.Vector(p2_mid.x, arc_center.y - radius, 0)
            getFillet(arc_center, p2_3, radius, 180, end_angle)

    elif mid_quadrant == 3:
        p2_mid = p2.add(mid_vec)
        # 中间象限是第3象限，结束象限只能第3，4象限
        if end_quadrant == 3:
            if start_quadrant == 2:
                p2_2 = FreeCAD.Vector(p2_mid.x, arc_center.y+radius, 0)
                if start_angle!=180:
                    getFillet(arc_center, p2_2, radius, start_angle, 180)
                getFillet(arc_center, p2_mid, radius, 180, end_angle)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, end_angle)
        else:
            if start_quadrant == 2:
                p2_2 = FreeCAD.Vector(p2_mid.x, arc_center.y+radius, 0)
                if start_angle!=180:
                    getFillet(arc_center, p2_2, radius, start_angle, 180)
                getFillet(arc_center, p2_mid, radius, 180, 270)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, 270)
            p2_4 = FreeCAD.Vector(arc_center.x+radius, p2_mid.y, 0)
            getFillet(arc_center, p2_4, radius, 270, end_angle)
    else:
        p2_mid = p2.add(mid_vec)
        # 中间象限是第4象限，结束象限只能第4，1象限
        if end_quadrant == 4:
            if start_quadrant == 3:
                p2_3 = FreeCAD.Vector(arc_center.x-radius, p2_mid.y, 0)
                if start_angle!=270:
                    getFillet(arc_center, p2_3, radius, start_angle, 270)
                getFillet(arc_center, p2_mid, radius, 270, end_angle)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, end_angle)
        else:
            if start_quadrant == 3:
                p2_3 = FreeCAD.Vector(arc_center.x-radius, p2_mid.y, 0)
                if start_angle!=270:
                    getFillet(arc_center, p2_3, radius, start_angle, 270)
                getFillet(arc_center, p2_mid, radius, 270, 360)
            else:
                getFillet(arc_center, p2_mid, radius, start_angle, 360)
            p2_4 = FreeCAD.Vector(p2_mid.x, arc_center.y+radius, 0)
            if end_angle!=0:
                getFillet(arc_center, p2_4, radius, 0, end_angle)














