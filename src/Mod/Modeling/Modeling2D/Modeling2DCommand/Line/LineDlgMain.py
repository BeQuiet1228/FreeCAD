# -*- coding: utf-8 -*-
import traceback

import LineDialog
from PySide import QtGui
import FreeCAD
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI, ExpressionTools
from Modeling.Modeling2D.Tools.Tools2D import sayz


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = LineDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.customAttribute = BaseDialog.CustomShowWidget()

        # 暂时写在这里
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
            self.ui.le_point1_x.setText(str(self.obj.user_point1_x).replace(' ',''))
            self.ui.le_point1_y.setText(str(self.obj.user_point1_y).replace(' ',''))
            self.ui.le_point2_x.setText(str(self.obj.user_point2_x).replace(' ',''))
            self.ui.le_point2_y.setText(str(self.obj.user_point2_y).replace(' ',''))
            # 隐藏点线的属性
            self.ui.groupBox_2.hide()

            # length = ExpressionTools.currentLengthUnits()
            # point1_x_value = str(self.obj.x1_helper.getValueAs(length)).replace(' ', '') + length
            # point1_y_value = str(self.obj.y1_helper.getValueAs(length)).replace(' ', '') + length
            # point2_x_value = str(self.obj.x2_helper.getValueAs(length)).replace(' ', '') + length
            # point2_y_value = str(self.obj.y2_helper.getValueAs(length)).replace(' ', '') + length
            # expression_list = self.obj.ExpressionEngine
            # for i in expression_list:
            #     if i[0] == "x1_helper":
            #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "y1_helper":
            #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "x2_helper":
            #         point2_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "y2_helper":
            #         point2_y_value = i[1].replace('Param.', '').replace(' ', '')
            # self.ui.le_point1_x.setText(point1_x_value)
            # self.ui.le_point1_y.setText(point1_y_value)
            # self.ui.le_point2_x.setText(point2_x_value)
            # self.ui.le_point2_y.setText(point2_y_value)
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
        self.close()
        try:
            ToolsUI.setCommonInfoToModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.setCustomAttributeToModelObj(self.obj, self.customAttribute.ui)
            # user_xxx辅助记录输入信息
            self.obj.user_point1_x = self.ui.le_point1_x.text().replace(" ", "")
            self.obj.user_point1_y = self.ui.le_point1_y.text().replace(" ", "")
            self.obj.user_point2_x = self.ui.le_point2_x.text().replace(" ", "")
            self.obj.user_point2_y = self.ui.le_point2_y.text().replace(" ", "")

            # 由于草图建模的线的坐标仅支持浮点型数据，所以使用x1_helper辅助记录表达式
            ToolsUI.setPlaceToObj(self.obj, "x1_helper", self.ui.le_point1_x.text())
            ToolsUI.setPlaceToObj(self.obj, "y1_helper", self.ui.le_point1_y.text())
            ToolsUI.setPlaceToObj(self.obj, "x2_helper", self.ui.le_point2_x.text())
            ToolsUI.setPlaceToObj(self.obj, "y2_helper", self.ui.le_point2_y.text())
            self.obj.Start.x = self.obj.x1_helper.Value
            self.obj.Start.y = self.obj.y1_helper.Value
            self.obj.End.x = self.obj.x2_helper.Value
            self.obj.End.y = self.obj.y2_helper.Value
            self.obj.recompute()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())


