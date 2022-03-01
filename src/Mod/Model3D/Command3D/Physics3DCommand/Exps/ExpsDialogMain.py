# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import ExpsDialog
import traceback


class ShowDialog(BaseDialogMain.BaseEmitDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BaseEmitDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = ExpsDialog.Ui_Dialog_EmeDlg()
        self.ui.setupUi(self)

    def privateDialog(self):
        try:
            self.ui.checkBox_TField.clicked.connect(self.checkBox_TField_clicked)
            self.ui.checkBox_RField.clicked.connect(self.checkBox_RField_clicked)
            self.ui.checkBox_Charg.clicked.connect(self.checkBox_Charg_clicked)
            self.ui.checkBox_FRate.clicked.connect(self.checkBox_FRate_clicked)
            # 获取当前坐标系及坐标系单位
            coord = Tools3D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[2]
            # 根据坐标系初始化面板
            parameter = "(T," + self.x + "," + self.y + "," + self.z + ")= "
            self.ui.checkBox_TField.setText(u"极限场值.TField" + parameter)
            self.ui.checkBox_RField.setText(u"空间余场.RField" + parameter)
            self.ui.checkBox_Charg.setText(u"最小电荷.Charg" + parameter)
            self.ui.checkBox_FRate.setText(u"等离子体产生率.FRate" + parameter)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def checkBox_TField_clicked(self):
        self.ui.textEdit_TField.setEnabled(self.ui.checkBox_TField.isChecked())

    def checkBox_RField_clicked(self):
        self.ui.textEdit_RField.setEnabled(self.ui.checkBox_RField.isChecked())

    def checkBox_Charg_clicked(self):
        self.ui.textEdit_Charg.setEnabled(self.ui.checkBox_Charg.isChecked())

    def checkBox_FRate_clicked(self):
        self.ui.textEdit_FRate.setEnabled(self.ui.checkBox_FRate.isChecked())

    def loadPrivateData(self):
        try:
            self.ui.checkBox_TField.setChecked(self.obj.isLimitFieldValue)
            self.ui.textEdit_TField.setText(self.obj.limitFieldValue)
            self.ui.checkBox_RField.setChecked(self.obj.isMoreThanSpacemoreThanSpace)
            self.ui.textEdit_RField.setText(self.obj.moreThanSpace)
            self.ui.checkBox_Charg.setChecked(self.obj.isTheMinimumCharge)
            self.ui.textEdit_Charg.setText(self.obj.theMinimumCharge)
            self.ui.checkBox_FRate.setChecked(self.obj.isPlasmaProductionRate)
            self.ui.textEdit_FRate.setText(self.obj.plasmaProductionRate)
            # 设置槽的状态
            self.checkBox_TField_clicked()
            self.checkBox_RField_clicked()
            self.checkBox_Charg_clicked()
            self.checkBox_FRate_clicked()
        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setPrivateInfoToObj(self):
        self.obj.isLimitFieldValue = self.ui.checkBox_TField.isChecked()
        self.obj.limitFieldValue = self.ui.textEdit_TField.toPlainText()
        self.obj.isMoreThanSpacemoreThanSpace = self.ui.checkBox_RField.isChecked()
        self.obj.moreThanSpace = self.ui.textEdit_RField.toPlainText()
        self.obj.isTheMinimumCharge = self.ui.checkBox_Charg.isChecked()
        self.obj.theMinimumCharge = self.ui.textEdit_Charg.toPlainText()
        self.obj.isPlasmaProductionRate = self.ui.checkBox_FRate.isChecked()
        self.obj.plasmaProductionRate = self.ui.textEdit_FRate.toPlainText()