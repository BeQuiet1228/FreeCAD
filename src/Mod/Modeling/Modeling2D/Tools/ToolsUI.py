# -*- coding: utf-8 -*-
import traceback

import Tools2D
from Modeling.Modeling2D.Tools import ExpressionTools
 


# 该文件主要服务UI部分


def getAttributeList():
    """
    获取Attribute的str_list，用于生成下拉框
    """
    attribute_list = [Tools2D.Attribute.NotDefine,
                      Tools2D.Attribute.Conductor,
                      Tools2D.Attribute.Custom,
                      Tools2D.Attribute.Void]
    return attribute_list


def setCommonInfoToModelObj(obj, ui):
    """
    体相关的属性赋值！！！
    获取ui信息，并将通用属性设置到obj
    注意该函数被调用时应该放在异常处理里面
    """
    # 赋值时注意变量类型
    if hasattr(obj, "Attribute") and hasattr(ui, "cb_attribute"):
        obj.Attribute = ui.cb_attribute.currentText()
    # obj.Label = ui.le_name.text()
    Tools2D.setLabelToObj(obj, ui.le_name.text())
    # 设置order到obj
    setOrderToObj(obj, ui)
    obj.isMarkX = ui.checkBox_isMarkX.isChecked()
    obj.isMarkY = ui.checkBox_isMarkY.isChecked()
    obj.MarkX = ui.le_markx.text()
    obj.MarkY = ui.le_marky.text()

def setCustomAttributeToModelObj(obj, ui):
    """
    @wangzhenguo
    点线面相关的自定义属性赋值！！！
    获取ui信息，并将通用属性设置到obj
    注意该函数被调用时应该放在异常处理里面
    """
    obj.C_SIGMA = ui.comboBox_sigma.currentText()
    obj.SIGMA1 = ui.lineEdit_sigma1.text()
    obj.SIGMA2 = ui.lineEdit_sigma2.text()
    obj.SIGMA3 = ui.lineEdit_sigma3.text()
    obj.RDC = ui.comboBox_setEps.currentText()
    obj.EPS1 = ui.lineEdit_setEps1.text()
    obj.EPS2 = ui.lineEdit_setEps2.text()
    obj.EPS3 = ui.lineEdit_setEps3.text()

def setOrderToObj(obj, ui):
    """
    将order设置到obj，如果order的顺序是不正确的，则会根据规则自动修正
    """
    curNumOfObjects = len(Tools2D.getAllValidModelObj())
    curOrder = int(ui.le_order.text())

    Tools2D.updateWhenOrderChanged(obj, obj.Order, curOrder)


def getCommonInfoFromModelObj(obj, ui):
    """
    体相关的属性赋值！！！
    获取obj信息，并将通用属性设置到ui
    注意该函数被调用时应该放在异常处理里面
    """
    ui.le_name.setText(str(obj.Label))
    getOrderFromObj(obj, ui)
    ui.le_markx.setText(str(obj.MarkX))
    ui.le_marky.setText(str(obj.MarkY))
    ui.checkBox_isMarkX.setChecked(obj.isMarkX)
    ui.checkBox_isMarkY.setChecked(obj.isMarkY)


def getCustomAttributeFromModelObj(obj, ui):
    """
    @wangzhenguo
    点线面相关的属性赋值！！！
    获取obj信息，并将通用属性设置到ui
    注意该函数被调用时应该放在异常处理里面
    """
    ui.comboBox_sigma.setCurrentIndex(ui.comboBox_sigma.findText(str(obj.C_SIGMA)))
    ui.comboBox_setEps.setCurrentIndex(ui.comboBox_setEps.findText(str(obj.RDC)))
    ui.lineEdit_sigma1.setText(str(obj.SIGMA1))
    ui.lineEdit_sigma2.setText(str(obj.SIGMA2))
    ui.lineEdit_sigma3.setText(str(obj.SIGMA3))
    ui.lineEdit_setEps1.setText(str(obj.EPS1))
    ui.lineEdit_setEps2.setText(str(obj.EPS2))
    ui.lineEdit_setEps3.setText(str(obj.EPS3))


def getOrderFromObj(obj, ui):
    """
    从obj获取order属性，并将属性设置到ui上，如果obj的order远大于当前所有obj数量，则自动调整
    """
    objNumbers = len(Tools2D.getAllModelObjects())
    if obj.Order > objNumbers - 1:
        ui.le_order.setText(str(objNumbers - 1))
    else:
        ui.le_order.setText(str(obj.Order))


# def setPlaceToObj(obj, attr, place_str="0"):
#     """
#     获取UI信息，然后对字符串处理，并将处理后的值添加到obj
#     """
#     from Modeling.Common.Tools import InputTools
#     place = InputTools.Stringfunctions(place_str)
#     try:
#         if place[1] == 2:
#             obj.setExpression(attr, place[0])
#         else:
#             # 像”Point.x“这样的attr并不可以被setattr()直接赋值，需要attr拆分赋值
#             obj.setExpression(attr, None)
#             if '.' not in attr:
#                 setattr(obj, attr, place[0])
#             else:
#                 attr_list = attr.split('.')
#                 # 这里暂时仅处理长度为2的情况
#                 if len(attr_list) == 2:
#                     setattr(getattr(obj, attr_list[0]), attr_list[1], place[0])
#                 else:
#                     raise Exception("赋值出现异常，异常位置:ToolsUI.py")
#     except:
#         Tools2D.sayz("读取ui信息并设置坐标信息到obj失败")
#         Tools2D.sayz(obj.Label + "--属性：  " + attr + "   坐标:   " + str(place))
#         return "error:" + attr + "\t" + place_str + "\n"
#     else:
#         return None


def setPlaceToObj(obj, attr, place_str="0"):
    """
    获取UI信息，然后对字符串处理，并将处理后的值添加到obj
    """
    place = ExpressionTools.processingLengthExpression(place_str)
    try:
        if True:
            obj.setExpression(attr, place)
        else:
            # 像”Point.x“这样的attr并不可以被setattr()直接赋值，需要attr拆分赋值
            obj.setExpression(attr, None)
            if '.' not in attr:
                setattr(obj, attr, place)
            else:
                attr_list = attr.split('.')
                # 这里暂时仅处理长度为2的情况
                if len(attr_list) == 2:
                    setattr(getattr(obj, attr_list[0]), attr_list[1], place)
                else:
                    raise Exception("赋值出现异常，异常位置:ToolsUI.py")
    except:
        Tools2D.sayz(obj.Label + "--属性：  " + attr + "   坐标:   " + str(place))
        Tools2D.sayz(traceback.format_exc())
        return "error"
    else:
        return None


def setAngleToObj(obj, attr, angle_str="0"):
    from Modeling.Common.Tools import InputTools
    angle = InputTools.anglefunctions(angle_str)
    try:
        if angle[1] == 2:
            obj.setExpression(attr, angle[0])
        else:
            obj.setExpression(attr, None)
            # obj.Point.y = angle[0]
            setattr(obj, attr, angle[0])
    except:
        Tools2D.sayz("读取ui信息并设置坐标信息到obj失败")
        Tools2D.sayz(obj.Label + "--属性：  " + attr + "   坐标:   " + str(angle))
        return "error:" + attr + "\t" + angle_str + "\n"
    else:
        return None


def setResolution(ui_class):
    """
    适配分辨率
    """
    new_x, new_y = AdaptiveDPIUtil.get_new_dpi(ui_class.width(), ui_class.height())
    ui_class.resize(new_x, new_y)


