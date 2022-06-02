# -*- coding: utf-8 -*-
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import TherDialog
import traceback


class ShowDialog(BaseDialogMain.BaseEmitDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BaseEmitDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = TherDialog.Ui_Dialog_EmtDlg()
        self.ui.setupUi(self)

    def privateDialog(self):
        # 获取当前坐标系及坐标系单位
        coord = Tools3D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        # 根据坐标系初始化面板
        parameter = "(T," + self.x + "," + self.y + "," + self.z + ")= "
        self.ui.label.setText(u"工作函数.WF" + parameter)
        self.ui.label_3.setText(u"工作温度.TP" + parameter)

    def loadPrivateData(self):
        try:
            self.ui.LineEdit_WF.setText(self.obj.workingFunctionWF)
            self.ui.LineEdit_TP.setText(self.obj.workingTemperatureTP)
        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setPrivateInfoToObj(self):
        self.obj.workingFunctionWF = self.ui.LineEdit_WF.text()
        self.obj.workingTemperatureTP = self.ui.LineEdit_TP.text()