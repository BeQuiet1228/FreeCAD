# -*- coding: utf-8 -*-
import FilletDialog
from PySide import QtGui
import FreeCAD

from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import ToolsUI, Tools2D, ExpressionTools
from Modeling.Modeling2D.Tools.Tools2D import sayz


class ShowDialog(BaseDialog.BaseModelDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = FilletDialog.Ui_Sector()
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
            ToolsUI.getCommonInfoFromModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.getCustomAttributeFromModelObj(self.obj, self.customAttribute.ui)
            self.ui.le_point1_x.setText(str(self.obj.user_point1_x).replace(' ',''))
            self.ui.le_point1_y.setText(str(self.obj.user_point1_y).replace(' ',''))
            self.ui.le_point2_x.setText(str(self.obj.user_point2_x).replace(' ',''))
            self.ui.le_point2_y.setText(str(self.obj.user_point2_y).replace(' ',''))
            self.ui.le_radius.setText(str(self.obj.user_radius).replace(' ',''))
            self.ui.le_startAngle.setText(str(self.obj.user_startAngle).replace(' ',''))
            self.ui.le_endAngle.setText(str(self.obj.user_endAngle).replace(' ',''))

            # length = ExpressionTools.currentLengthUnits()
            # ExpressionEngine = dict(self.obj.ExpressionEngine)
            # Tools2D.sayz(str(ExpressionEngine))
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
            #
            # if ExpressionEngine.has_key("Point2Y"):
            #     self.ui.le_point2_y.setText(str(ExpressionEngine["Point2Y"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_point2_y.setText(str(self.obj.Point2Y.getValueAs(length)).replace(' ', '') + length)
            #
            # if ExpressionEngine.has_key("Radius"):
            #     self.ui.le_radius.setText(str(ExpressionEngine["Radius"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_radius.setText(str(self.obj.Radius.getValueAs(length)).replace(' ', '') + length)
            #
            # if ExpressionEngine.has_key("StartAngle"):
            #     self.ui.le_startAngle.setText(str(ExpressionEngine["StartAngle"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_startAngle.setText(str(self.obj.StartAngle).replace(' ', ''))
            #
            # if ExpressionEngine.has_key("EndAngle"):
            #     self.ui.le_endAngle.setText(str(ExpressionEngine["EndAngle"].replace('Param.', '').replace(' ', '')))
            # else:
            #     self.ui.le_endAngle.setText(str(self.obj.EndAngle).replace(' ', ''))
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        self.close()
        try:
            ToolsUI.setCommonInfoToModelObj(self.obj, self.ui)
            # 自定义属性
            ToolsUI.setCustomAttributeToModelObj(self.obj, self.customAttribute.ui)

            self.obj.user_point1_x = self.ui.le_point1_x.text().replace(" ", "")
            self.obj.user_point1_y = self.ui.le_point1_y.text().replace(" ", "")
            self.obj.user_point2_x = self.ui.le_point2_x.text().replace(" ", "")
            self.obj.user_point2_y = self.ui.le_point2_y.text().replace(" ", "")
            self.obj.user_radius = self.ui.le_radius.text().replace(" ", "")
            self.obj.user_startAngle = self.ui.le_startAngle.text().replace(" ", "")
            self.obj.user_endAngle = self.ui.le_endAngle.text().replace(" ", "")

            ToolsUI.setPlaceToObj(self.obj, "Point1X", self.ui.le_point1_x.text())
            ToolsUI.setPlaceToObj(self.obj, "Point1Y", self.ui.le_point1_y.text())
            ToolsUI.setPlaceToObj(self.obj, "Point2X", self.ui.le_point2_x.text())
            ToolsUI.setPlaceToObj(self.obj, "Point2Y", self.ui.le_point2_y.text())
            ToolsUI.setPlaceToObj(self.obj, "Radius", self.ui.le_radius.text())
            ToolsUI.setAngleToObj(self.obj, "StartAngle", self.ui.le_startAngle.text())
            ToolsUI.setAngleToObj(self.obj, "EndAngle", self.ui.le_endAngle.text())
            self.obj.recompute()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass
