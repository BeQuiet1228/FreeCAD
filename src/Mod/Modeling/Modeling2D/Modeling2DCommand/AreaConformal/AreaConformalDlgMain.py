# -*- coding: utf-8 -*-
import traceback

import AreaConformalDialog
from PySide import QtGui
import FreeCAD
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI, ExpressionTools
from Modeling.Modeling2D.Tools.Tools2D import sayz


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = AreaConformalDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.customAttribute = BaseDialog.CustomShowWidget()

        # 暂时写在这里
        self.setModal(False)
        self.obj = obj
        # 为老工程做适配，如果没有属性则添加属性
        if not hasattr(self.obj, "C_SIGMA"):
            Tools2D.completionProperties(self.obj)
        self.initDialog()

        self.slotFillet()
        self.ui.isFillet.stateChanged.connect(self.slotFillet)

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
            # ExpressionEngine = dict(self.obj.ExpressionEngine)
            # if ExpressionEngine.has_key("Point1X"):
            #     self.ui.le_point1_x.setText(str(ExpressionEngine["Point1X"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_point1_x.setText(str(self.obj.Point1X.getValueAs(length)).replace(' ', '') + length)
            #
            # if ExpressionEngine.has_key("Point1Y"):
            #     self.ui.le_point1_y.setText(str(ExpressionEngine["Point1Y"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_point1_y.setText(str(self.obj.Point1Y.getValueAs(length)).replace(' ', '') + length)
            #
            # if ExpressionEngine.has_key("Point2X"):
            #     self.ui.le_point2_x.setText(str(ExpressionEngine["Point2X"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_point2_x.setText(str(self.obj.Point2X.getValueAs(length)).replace(' ', '') + length)
            # if ExpressionEngine.has_key("Point2Y"):
            #     self.ui.le_point2_y.setText(str(ExpressionEngine["Point2Y"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_point2_y.setText(str(self.obj.Point2Y.getValueAs(length)).replace(' ', '') + length)
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
            self.obj.user_point2_x = self.ui.le_point2_x.text().replace(" ", "")
            self.obj.user_point2_y = self.ui.le_point2_y.text().replace(" ", "")

            ToolsUI.setPlaceToObj(self.obj, "Point1X", self.ui.le_point1_x.text())
            ToolsUI.setPlaceToObj(self.obj, "Point1Y", self.ui.le_point1_y.text())
            ToolsUI.setPlaceToObj(self.obj, "Point2X", self.ui.le_point2_x.text())
            ToolsUI.setPlaceToObj(self.obj, "Point2Y", self.ui.le_point2_y.text())
            self.obj.recompute()
            self.addFillet()
            self.obj.IsAutoFillet = self.ui.isFillet.isChecked()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def slotFillet(self):
        if self.ui.isFillet.isChecked():
            self.ui.cb_fillet_num.setEnabled(True)
            self.ui.dsp_radius.setEnabled(True)
        else:
            self.ui.cb_fillet_num.setEnabled(False)
            self.ui.dsp_radius.setEnabled(False)

    def addFillet(self):
        if self.ui.isFillet.isChecked():
            num = self.ui.cb_fillet_num.currentText()

            if num.isdigit():
                num = int(num)
            else:
                return

            radius = self.ui.dsp_radius.value() * 0.001

            import Modeling.Modeling2D.Modeling2DCommand.AutoFillet.AutoFilletCommand as Fillet

            Fillet.createAutoFillet(self.obj, num, radius)