# -*- coding: utf-8 -*-
import CircularDialog
from PySide import QtGui, QtCore
import traceback
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI, ExpressionTools


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = CircularDialog.Ui_Circular()
        self.ui.setupUi(self)

        self.customAttribute = BaseDialog.CustomShowWidget()

        self.setModal(False)
        self.obj = obj
        # 为老工程做适配，如果没有属性则添加属性
        if not hasattr(self.obj, "C_SIGMA"):
            Tools2D.completionProperties(self.obj)

        self.initDialog()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            # 共有数据
            ToolsUI.getCommonInfoFromModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.getCustomAttributeFromModelObj(self.obj, self.customAttribute.ui)
            # 独有数据
            self.ui.le_radius.setText(str(self.obj.user_radius).replace(' ',''))
            self.ui.le_point1_x.setText(str(self.obj.user_point1_x).replace(' ',''))
            self.ui.le_point1_y.setText(str(self.obj.user_point1_y).replace(' ',''))
            # length = ExpressionTools.currentLengthUnits()
            # # 为了处理表达式相关信息，我们总是看看表达式引擎中是否含有与坐标相关信息
            # radius_value = str(self.obj.Radius.getValueAs(length)).replace(' ', '') + length
            # point1_x_value = str(self.obj.x_helper.getValueAs(length)).replace(' ', '') + length
            # point1_y_value = str(self.obj.y_helper.getValueAs(length)).replace(' ', '') + length
            # expression_list = self.obj.ExpressionEngine
            # # 如果表达式引擎中存在对应数据，则使用表达式引擎中的数据
            # for i in expression_list:
            #     if i[0] == "Radius":
            #         radius_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "x_helper":
            #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "y_helper":
            #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
            # self.ui.le_radius.setText(radius_value)
            # self.ui.le_point1_x.setText(point1_x_value)
            # self.ui.le_point1_y.setText(point1_y_value)
        except AttributeError:
            Tools2D.sayz("Circular--异常--在读取Object属性时出现异常")
            Tools2D.sayz(traceback.format_exc())
        except Exception as e:
            Tools2D.sayz("Circular--" + str(e))
        else:
            Tools2D.sayz("Circular--成功--读取Object信息")
        # 加载Mark对应文本框的状态
        self.setIsMarkXState()
        self.setIsMarkYState()

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        try:
            ToolsUI.setCommonInfoToModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.setCustomAttributeToModelObj(self.obj, self.customAttribute.ui)
            # user_xxx辅助记录输入信息
            self.obj.user_point1_x = self.ui.le_point1_x.text().replace(" ", "")
            self.obj.user_point1_y = self.ui.le_point1_y.text().replace(" ", "")
            self.obj.user_radius = self.ui.le_radius.text().replace(" ", "")

            # 坐标相关赋值
            ToolsUI.setPlaceToObj(self.obj, "Radius", self.ui.le_radius.text())
            # 由于草图圆的圆心只能设置浮点值，所以为圆添加两个属性辅助纪录圆心的值
            ToolsUI.setPlaceToObj(self.obj, "x_helper", self.ui.le_point1_x.text())
            ToolsUI.setPlaceToObj(self.obj, "y_helper", self.ui.le_point1_y.text())
            self.obj.Placement.Base.x = self.obj.x_helper.Value
            self.obj.Placement.Base.y = self.obj.y_helper.Value

            self.obj.recompute()
        except:
            Tools2D.sayz(traceback.format_exc())




