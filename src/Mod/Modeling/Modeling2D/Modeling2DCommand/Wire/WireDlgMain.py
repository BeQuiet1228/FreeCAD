# -*- coding: utf-8 -*-
import PySide

import WireDialog
from PySide import QtGui, QtCore
import ItemWidget2D
import FreeCAD

from Modeling.Common.Tools.BaseObjDialog import ValueUnitslength
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI, CompleterTools, ExpressionTools
from Modeling.Modeling2D.Tools.Tools2D import sayz


class SubForm(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.ui = ItemWidget2D.Ui_Form()
        self.ui.setupUi(self)


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = WireDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.customAttribute = BaseDialog.CustomShowWidget()

        # 暂时写在这里
        self.setModal(False)
        self.obj = obj
        self.oldPointNum = len(self.obj.Points)
        # 为老工程做适配，如果没有属性则添加属性
        if not hasattr(self.obj, "C_SIGMA"):
            Tools2D.completionProperties(self.obj)

        self.ui.sb_fillet_num.setMinimum(1)
        self.slotFillet()
        self.ui.isFillet.stateChanged.connect(self.slotFillet)

        # 储存点数
        self.subWidgetNumbers = len(self.obj.Points)
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
            self.initItem()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass
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
            self.getItemValue()
            self.obj.recompute()

            self.addFillet()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass
        if not self.obj.Shape.isValid():
            QtGui.QMessageBox.information(None, "",
                                          "坐标数据错误，无法成功绘制模型。")

    def getItemValue(self):
        """
        获取界面坐标信息并设置到helper中，再读取helper中的浮点值设置到Points中
        """
        points = []
        for index in range(self.ui.spinBox_num.value()):
            tempItem = self.ui.listWidget.item(index)
            tempSubWid = self.ui.listWidget.itemWidget(tempItem)
            x = tempSubWid.ui.le_x.text()
            y = tempSubWid.ui.le_y.text()
            # 用user_xxx记录用户输入数据
            setattr(self.obj, "user_point" + str(index + 1) + "_x", x)
            setattr(self.obj, "user_point" + str(index + 1) + "_y", y)
            ToolsUI.setPlaceToObj(self.obj, "helper_" + str(index) + ".x", tempSubWid.ui.le_x.text())
            ToolsUI.setPlaceToObj(self.obj, "helper_" + str(index) + ".y", tempSubWid.ui.le_y.text())
            temp_x = getattr(self.obj, "helper_" + str(index)).x
            temp_y = getattr(self.obj, "helper_" + str(index)).y
            Vector = FreeCAD.Vector(temp_x, temp_y, 0)
            points.append(Vector)
        self.obj.Points = points

    def initDialog(self):
        """
        初始化界面，设置界面逻辑
        """
        BaseDialog.BaseModelDialog.initDialog(self)
        # 设置SubForm
        try:
            self.ui.spinBox_num.valueChanged.connect(self.createSubWidget)
        except:
            Tools2D.sayz("错误：多边形设置点控件时出现错误")

    def initItem(self):
        # 设置点的个数
        self.ui.spinBox_num.setValue(self.subWidgetNumbers)
        # 添加小控件
        for i in range(self.subWidgetNumbers):
            self.addItem(i)
        # 设置坐标
        self.getPlaceFromObj()

    def createSubWidget(self):
        """
        批量创建子控件并添加到listWidget,不应该直接调用该函数
        """
        # 注意此处需要更新obj的点的个数，否则在设置坐标时会出现异常
        # self.obj.NumbersOfPoints = subWidget_number
        # 当subWidget_number < self.subWidgetNumbers时
        # 删除self.subWidgetNumbers - subWidget_number次的最后一个小控件
        subWidget_number = self.ui.spinBox_num.value()
        # 首先根据控件中显示的数值设置多边形点的数量
        self.setTheNumberOfHelper(subWidget_number)
        if 3 <= subWidget_number < self.subWidgetNumbers:
            for i in range(self.subWidgetNumbers - subWidget_number):
                self.ui.listWidget.takeItem(self.ui.listWidget.count() - 1)
            # 更新小控件的个数
            self.subWidgetNumbers = subWidget_number
            return

        # 当subWidget_number = self.subWidgetNumbers时, 什么都不做直接退出
        if subWidget_number == self.subWidgetNumbers:
            return

        # 当subWidget_number > self.subWidgetNumbers时
        if subWidget_number > self.subWidgetNumbers:
            for i in range(self.subWidgetNumbers, subWidget_number):
                # 创建SubForm对象
                self.addItem(i)
            # 更新小控件的个数
            self.subWidgetNumbers = subWidget_number
            return

    def addItem(self, PointOrder):
        tempSub = SubForm(self)
        tempSub.ui.lb_name.setText('Point' + str(PointOrder + 1) + ':')
        if len(self.obj.Points) > PointOrder:
            # tempSub.ui.le_x.setText(str(self.obj.Points[PointOrder].x))
            # tempSub.ui.le_y.setText(str(self.obj.Points[PointOrder].y))
            self.getHelperFromObj(PointOrder, tempSub)
        tempWidItem = PySide.QtGui.QListWidgetItem()
        # 在这里控制小控件每一行的长宽
        tempWidItem.setSizeHint(PySide.QtCore.QSize(200, 45))
        # 向listWidget添加item的固定调用方法为一下两行
        self.ui.listWidget.addItem(tempWidItem)
        self.ui.listWidget.setItemWidget(tempWidItem, tempSub)
        tempSub.ui.le_x.setcompleterlist(CompleterTools.getParamsList())
        tempSub.ui.le_y.setcompleterlist(CompleterTools.getParamsList())

    def getPlaceFromObj(self):
        """
        读取obj坐标信息并设置到UI
        """
        for i in range(self.subWidgetNumbers):
            tempItem = self.ui.listWidget.item(i)
            tempSubWid = self.ui.listWidget.itemWidget(tempItem)
            tempSubWid.ui.le_x.setText(str(getattr(self.obj, "user_point" + str(i + 1) + "_x")).replace(' ', ''))
            tempSubWid.ui.le_y.setText(str(getattr(self.obj, "user_point" + str(i + 1) + "_y")).replace(' ', ''))
        # # 首先获取obj的点坐标，并通过相关的list生成对应的字典结构，方便赋值调用
        # points_list = self.obj.ExpressionEngine
        # points_dict = {}
        # for i in points_list:
        #     points_dict[i[0]] = i[1]
        # # 依次获取小控件，并通过查询字典来赋值
        # from Modeling.Common.Tools import InputTools
        # length = InputTools.currentLengthUnits()
        # # angle = InputTools.currentAngleUnits()
        # # 直角坐标系下设置默认值
        # if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular" \
        #         or FreeCAD.ActiveDocument.CoordinateSystem == "Cylindrical":
        #     for i in range(self.subWidgetNumbers):
        #         tempItem = self.ui.listWidget.item(i)
        #         tempSubWid = self.ui.listWidget.itemWidget(tempItem)
        #         # x------------------------------------------------------------
        #         # 如果在keys里面说明是一个变量
        #         if "helper_" + str(i) + ".x" in points_dict.keys():
        #             Tools2D.sayz("设置表达式")
        #             tempStr = points_dict["helper_" + str(i) + ".x"]
        #             Tools2D.sayz(str(tempStr))
        #             if "Param." in tempStr:
        #                 tempStr = tempStr.replace('Param.', '')
        #             # # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
        #             # else:
        #             #     tempStr = getattr(self.obj, "helper_" + str(i)).x
        #             #     tempStr = str(ValueUnitslength(tempStr, length)) + length
        #             tempStr = tempStr.replace(" ", "")
        #             tempSubWid.ui.le_x.setText(tempStr)
        #         # 如果不在说明是一个整型
        #         else:
        #             tempStr = getattr(self.obj, "helper_" + str(i)).x
        #             tempStr = str(ValueUnitslength(tempStr, length)) + length
        #             tempStr = tempStr.replace(" ", "")
        #             tempSubWid.ui.le_x.setText(tempStr)
        #         # y---------------------------------------------------------
        #         if "helper_" + str(i) + ".y" in points_dict.keys():
        #             tempStr = points_dict["helper_" + str(i) + ".y"]
        #             if "Param." in tempStr:
        #                 tempStr = tempStr.replace('Param.', '')
        #             # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
        #             # else:
        #             #     tempStr = getattr(self.obj, "helper_" + str(i)).y
        #             #     tempStr = str(ValueUnitslength(tempStr, length)) + length
        #             # 将解析后的字符串添加到Dialog
        #             tempStr = tempStr.replace(" ", "")
        #             tempSubWid.ui.le_y.setText(tempStr)
        #         # 如果不在说明是一个整型
        #         else:
        #             tempStr = getattr(self.obj, "helper_" + str(i)).y
        #             tempStr = str(ValueUnitslength(tempStr, length)) + length
        #             tempStr = tempStr.replace(" ", "")
        #             tempSubWid.ui.le_y.setText(tempStr)

    def getHelperFromObj(self, num, tempSubWid):
        """
        从helper中读取数据，该函数主要应对点的数量先减少后增加时的情况
        """
        from Modeling.Common.Tools import InputTools
        length = InputTools.currentLengthUnits()

        points_list = self.obj.ExpressionEngine
        points_dict = {}
        for i in points_list:
            points_dict[i[0]] = i[1]
        tempStr_x = str(getattr(self.obj, "helper_" + str(num)).x)
        tempStr_y = str(getattr(self.obj, "helper_" + str(num)).y)
        # 如果helper不在表达式引擎中，那么他一定是一个浮点型
        if "helper_" + str(num) + ".x" in points_dict:
            tempStr_x = points_dict["helper_" + str(num) + ".x"]
        else:
            tempStr_x = str(ValueUnitslength(float(tempStr_x), length)) + length
            tempStr_x = tempStr_x.replace(" ", "")

        if "helper_" + str(num) + ".y" in points_dict:
            tempStr_y = points_dict["helper_" + str(num) + ".y"]
        else:
            tempStr_y = str(ValueUnitslength(float(tempStr_y), length)) + length
            tempStr_y = tempStr_y.replace(" ", "")

        tempStr_x = tempStr_x.replace("Param.", "").replace(" ", "")
        tempSubWid.ui.le_x.setText(tempStr_x)
        tempStr_y = tempStr_y.replace("Param.", "").replace(" ", "")
        tempSubWid.ui.le_y.setText(tempStr_y)

    def setTheNumberOfHelper(self, expected_num):
        """
        设置helper的数量，注意helper的命名时从0开始的
        """
        cur_num = len(self.obj.Points)
        if expected_num < cur_num:
            pass
        elif expected_num == cur_num:
            return
        else:
            for i in range(cur_num, expected_num):
                if hasattr(self.obj, "helper_" + str(i)):
                    continue
                self.obj.addProperty("App::PropertyVectorDistance", "helper_" + str(i), "NonUniformGrid", "")
                setattr(self.obj, "helper_" + str(i), FreeCAD.Vector(0, 0, 0))
                # 添加user_xxx   user_point1_x 对应 helper_0.x
                self.obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_x")
                self.obj.addProperty("App::PropertyString", "user_point" + str(i + 1) + "_y")
                setattr(self.obj, "user_point" + str(i + 1) + "_x", "0")
                setattr(self.obj, "user_point" + str(i + 1) + "_y", "0")

    def slotFillet(self):
        if self.ui.isFillet.isChecked():
            self.ui.sb_fillet_num.setEnabled(True)
            self.ui.dsp_radius.setEnabled(True)
        else:
            self.ui.sb_fillet_num.setEnabled(False)
            self.ui.dsp_radius.setEnabled(False)

    def addFillet(self):
        if self.ui.isFillet.isChecked():
            num = self.ui.sb_fillet_num.value()

            radius = self.ui.dsp_radius.value() * 0.001

            import Modeling.Modeling2D.Modeling2DCommand.AutoFillet.AutoFilletCommand as Fillet

            Fillet.createAutoFilletForPolygonal(self.obj, num, radius)


