# -*- coding: utf-8 -*-
import NetStepSettingDialog
from PySide import QtGui
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog

class ShowDialog(BaseDialog.BaseOtherDialog):
    def __init__(self, obj, parent=None):
        BaseDialog.BaseOtherDialog.__init__(self, obj, parent)

    def setUI(self):
        """
        设置ui
        """
        self.ui = NetStepSettingDialog.Ui_Dialog_WorkSpaceDlg()
        self.ui.setupUi(self)
        self.setModal(True)

    def helperInitDialog(self):
        # # 获取当前坐标系及坐标系单位
        # coord = Tools2D.getCoordinate()
        # self.x = coord[0]
        # self.y = coord[1]
        # # 根据坐标系初始化面板
        # self.ui.groupBox_WorkSpace_X.setText(self.x)
        # self.ui.groupBox_WorkSpace_Y.setText(self.y)
        self.loadData()
        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        # 根据坐标系初始化面板
        self.ui.groupBox_WorkSpace_X.setTitle(self.x)
        self.ui.groupBox_WorkSpace_Y.setTitle(self.y)

    def helperOK(self):
        self.keepData()
        self.close()

    def helperCancel(self):
        self.close()

    def loadData(self):
        self.ui.lineEdit_Name.setText(self.obj.Label)
        # 范围X
        self.ui.LineEdit_start_x.setText(self.obj.point1_X)
        self.ui.LineEdit_end_x.setText(self.obj.point2_X)
        # 范围Y
        self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
        self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
        # 步长
        self.ui.LineEdit_stride_x.setText(self.obj.stepSizeX)
        self.ui.LineEdit_stride_y.setText(self.obj.stepSizeY)
        # 启用按钮
        self.ui.checkBox.setChecked(self.obj.isStartUsing)

    def keepData(self):
        # 名字
        self.obj.Label = self.ui.lineEdit_Name.text()
        # 范围X
        self.obj.point1_X = self.ui.LineEdit_start_x.text()
        self.obj.point2_X = self.ui.LineEdit_end_x.text()
        # 范围Y
        self.obj.point1_Y = self.ui.LineEdit_start_y.text()
        self.obj.point2_Y = self.ui.LineEdit_end_y.text()
        # 步长
        self.obj.stepSizeX = self.ui.LineEdit_stride_x.text()
        self.obj.stepSizeY = self.ui.LineEdit_stride_y.text()
        self.obj.isStartUsing = self.ui.checkBox.isChecked()




