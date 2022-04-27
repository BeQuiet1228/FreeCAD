# -*- coding: utf-8 -*-
import traceback
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import FieldSettingDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = FieldSettingDialog.Ui_Dialog_FieldSettingDlg()
        self.ui.setupUi(self)

    def initDialog(self):
        """
        重写初始按钮
        """
        self.ui.pushButton_ok.clicked.connect(self.slotOK)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            self.ischeck_magenetic_x()
            self.ischeck_magenetic_y()
            self.ischeck_magenetic_z()
            self.ischeck_electric_x()
            self.ischeck_electric_y()
            self.ischeck_electric_z()
            self.ui.checkBox_magenetic_x.clicked.connect(self.ischeck_magenetic_x)
            self.ui.checkBox_magenetic_y.clicked.connect(self.ischeck_magenetic_y)
            self.ui.checkBox_magenetic_z.clicked.connect(self.ischeck_magenetic_z)
            self.ui.checkBox_electric_x.clicked.connect(self.ischeck_electric_x)
            self.ui.checkBox_electric_y.clicked.connect(self.ischeck_electric_y)
            self.ui.checkBox_electric_z.clicked.connect(self.ischeck_electric_z)
            self.checkBox_lable()
        except:
            Tools3D.sayz("FieldSetting加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            # 电磁场按钮
            self.ui.checkBox_magenetic_x.setChecked(self.obj.isMagnetostaticFieldX)
            self.ui.checkBox_magenetic_y.setChecked(self.obj.isMagnetostaticFieldY)
            self.ui.checkBox_magenetic_z.setChecked(self.obj.isMagnetostaticFieldZ)
            self.ui.checkBox_electric_x.setChecked(self.obj.isElectrostaticFieldX)
            self.ui.checkBox_electric_y.setChecked(self.obj.isElectrostaticFieldY)
            self.ui.checkBox_electric_z.setChecked(self.obj.isElectrostaticFieldZ)
            self.ischeck_magenetic_x()
            self.ischeck_magenetic_y()
            self.ischeck_magenetic_z()
            # 静电磁场的值
            self.ui.LineEdit_magenetic_x.setText(self.obj.magnetostaticFieldX)
            self.ui.LineEdit_magenetic_y.setText(self.obj.magnetostaticFieldY)
            self.ui.LineEdit_magenetic_z.setText(self.obj.magnetostaticFieldZ)
            self.ui.LineEdit_electric_x.setText(self.obj.electrostaticFieldX)
            self.ui.LineEdit_electric_y.setText(self.obj.electrostaticFieldY)
            self.ui.LineEdit_electric_z.setText(self.obj.electrostaticFieldZ)
            self.ui.textEdit_filed_custom.setText(self.obj.self_definingFunction)
            self.ischeck_electric_x()
            self.ischeck_electric_y()
            self.ischeck_electric_z()
        except:
            Tools3D.sayz("FieldSetting加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            # 静电磁场按钮
            self.obj.isMagnetostaticFieldX = self.ui.checkBox_magenetic_x.isChecked()
            self.obj.isMagnetostaticFieldY = self.ui.checkBox_magenetic_y.isChecked()
            self.obj.isMagnetostaticFieldZ = self.ui.checkBox_magenetic_z.isChecked()
            self.obj.isElectrostaticFieldX = self.ui.checkBox_electric_x.isChecked()
            self.obj.isElectrostaticFieldY = self.ui.checkBox_electric_y.isChecked()
            self.obj.isElectrostaticFieldZ = self.ui.checkBox_electric_z.isChecked()
            # 静电磁场的值
            self.obj.magnetostaticFieldX = self.ui.LineEdit_magenetic_x.toPlainText()
            self.obj.magnetostaticFieldY = self.ui.LineEdit_magenetic_y.toPlainText()
            self.obj.magnetostaticFieldZ = self.ui.LineEdit_magenetic_z.toPlainText()
            self.obj.electrostaticFieldX = self.ui.LineEdit_electric_x.toPlainText()
            self.obj.electrostaticFieldY = self.ui.LineEdit_electric_y.toPlainText()
            self.obj.electrostaticFieldZ = self.ui.LineEdit_electric_z.toPlainText()
            self.obj.self_definingFunction = self.ui.textEdit_filed_custom.toPlainText()
        except:
            Tools3D.sayz("FieldSetting加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def ischeck_magenetic_x(self):
        self.ui.LineEdit_magenetic_x.setEnabled(self.ui.checkBox_magenetic_x.isChecked())

    def ischeck_magenetic_y(self):
        self.ui.LineEdit_magenetic_y.setEnabled(self.ui.checkBox_magenetic_y.isChecked())

    def ischeck_magenetic_z(self):
        self.ui.LineEdit_magenetic_z.setEnabled(self.ui.checkBox_magenetic_z.isChecked())

    def ischeck_electric_x(self):
        self.ui.LineEdit_electric_x.setEnabled(self.ui.checkBox_electric_x.isChecked())

    def ischeck_electric_y(self):
        self.ui.LineEdit_electric_y.setEnabled(self.ui.checkBox_electric_y.isChecked())

    def ischeck_electric_z(self):
        self.ui.LineEdit_electric_z.setEnabled(self.ui.checkBox_electric_z.isChecked())

    def checkBox_lable(self):
        coord = Tools3D.getCoordinate()
        x1 = coord[0] + "方向" + "FBSXT" + "(" + coord[0] + ", " + coord[1] +  ", " + coord[2] + ")" + "="
        y1 = coord[1] + "方向" + "FBSXT" + "(" + coord[0] + ", " + coord[1] +  ", " + coord[2] + ")" + "="
        z1 = coord[2] + "方向" + "FBSXT" + "(" + coord[0] + ", " + coord[1] +  ", " + coord[2] + ")" + "="
        self.ui.checkBox_magenetic_x.setText(x1)
        self.ui.checkBox_magenetic_y.setText(y1)
        self.ui.checkBox_magenetic_z.setText(z1)
        self.ui.checkBox_electric_x.setText(x1)
        self.ui.checkBox_electric_y.setText(y1)
        self.ui.checkBox_electric_z.setText(z1)
