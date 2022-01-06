# -*- coding: utf-8 -*-
import traceback

import PointDialog
from PySide import QtGui
import FreeCAD
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI, ExpressionTools
from Modeling.Modeling2D.Tools.Tools2D import sayz


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = PointDialog.Ui_Dialog()
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
            self.ui.groupBox_2.hide()

            # length = ExpressionTools.currentLengthUnits()
            # point1_x_value = str(self.obj.X.getValueAs(length)).replace(' ', '') + length
            # point1_y_value = str(self.obj.Y.getValueAs(length)).replace(' ', '') + length
            # expression_list = self.obj.ExpressionEngine
            # for i in expression_list:
            #     if i[0] == "X":
            #         point1_x_value = i[1].replace('Param.', '').replace(' ', '')
            #     elif i[0] == "Y":
            #         point1_y_value = i[1].replace('Param.', '').replace(' ', '')
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
        self.close()
        try:
            ToolsUI.setCommonInfoToModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.setCustomAttributeToModelObj(self.obj, self.customAttribute.ui)
            # 将输入框的内容直接记录到user_xxx
            self.obj.user_point1_x = self.ui.le_point1_x.text().replace(" ", "")
            self.obj.user_point1_y = self.ui.le_point1_y.text().replace(" ", "")
            # 由于草图建模的线的坐标仅支持浮点型数据，所以使用x1_helper辅助记录表达式
            ToolsUI.setPlaceToObj(self.obj, "X", self.ui.le_point1_x.text())
            ToolsUI.setPlaceToObj(self.obj, "Y", self.ui.le_point1_y.text())
            self.obj.recompute()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())


