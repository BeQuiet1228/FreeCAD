# -*- coding: utf-8 -*-
import traceback

import LineConformalDialog
from PySide import QtGui
import FreeCAD
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI, ExpressionTools
from Modeling.Modeling2D.Tools.Tools2D import sayz
import math


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = LineConformalDialog.Ui_dialog()
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
            # 由于initDialog在设置坐标之前，所以在此处额外添加一次设置坐标
            self.slotNormal()
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
            self.obj.normal = self.ui.cb_normal.currentText()
            self.obj.recompute()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def initDialog(self):
        BaseDialog.BaseModelDialog.initDialog(self)
        self.setNormal()
        self.ui.le_point1_x.textChanged.connect(self.slotLineEdit)
        self.ui.le_point1_y.textChanged.connect(self.slotLineEdit)
        # 隐藏点线的属性
        self.ui.groupBox_2.hide()
        # coodinate = FreeCAD.ActiveDocument.CoordinateSystem
        # if coodinate == u'Rectangular':
        #     coodinateList = ["X", "Y"]
        #     normalList = []
        #     for i in coodinateList:
        #         if i not in normalList:
        #             normalList.append(i)
        # elif coodinate == u'Cylindrical':
        #     coodinateList = ["Z", "R"]
        #     normalList = []
        #     for i in coodinateList:
        #         if i not in normalList:
        #             normalList.append(i)

    def setNormal(self):
        """
        界面初始化时设置normal选项的逻辑
        """
        # 初始化时normal为空字符
        if len(self.obj.normal) == 0:
            x_length = abs(self.obj.x2_helper.Value - self.obj.x1_helper.Value)
            y_length = abs(self.obj.y2_helper.Value - self.obj.y1_helper.Value)
            if x_length <= y_length:
                self.ui.cb_normal.setCurrentIndex(0)
            else:
                self.ui.cb_normal.setCurrentIndex(1)
        else:
            if self.obj.normal == "X" or self.obj.normal == "Z":
                self.ui.cb_normal.setCurrentIndex(0)
            elif self.obj.normal == "Y" or self.obj.normal == "R":
                self.ui.cb_normal.setCurrentIndex(1)
            else:
                Tools2D.sayz("致命错误，normal出现了意外的值")
                self.obj.normal = "X"
        self.slotNormal()
        self.ui.cb_normal.currentIndexChanged.connect(self.slotNormal)

    def slotNormal(self):
        """
        当normal的选项发生变化时，调整坐标输入框的状态
        """
        if self.ui.cb_normal.currentIndex() == 0:
            self.ui.le_point2_x.setEnabled(False)
            self.ui.le_point2_y.setEnabled(True)
            self.ui.le_point2_x.setText(self.ui.le_point1_x.text())
        else:
            self.ui.le_point2_x.setEnabled(True)
            self.ui.le_point2_y.setEnabled(False)
            self.ui.le_point2_y.setText(self.ui.le_point1_y.text())

    def slotLineEdit(self):
        """
        normal设定x时，le_point2_x不可以被编辑，但是值随le_point1_x变化
        """
        normal_text = self.ui.cb_normal.currentText()
        if normal_text == 'x' or normal_text == "X" or normal_text == "Z":
            point1_x_text = self.ui.le_point1_x.text()
            self.ui.le_point2_x.setText(point1_x_text)
        elif normal_text == "Y" or normal_text == "R":
            point1_y_text = self.ui.le_point1_y.text()
            self.ui.le_point2_y.setText(point1_y_text)
