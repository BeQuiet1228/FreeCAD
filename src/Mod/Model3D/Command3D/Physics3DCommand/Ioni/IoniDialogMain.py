# -*- coding: utf-8 -*-
import IoniDialog
import traceback
import FreeCAD
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = IoniDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def getInfoFromObj(self):
        try:
            self.ui.le_name.setText(self.obj.Label)
            self.ui.cb_type.setCurrentIndex(self.ui.cb_type.findText(self.obj.ionizationOfGas))
            self.ui.le_pressure.setText(self.obj.gasPressure)
            self.ui.le_temperature.setText(self.obj.gasTemperature)
        except:
            Tools3D.sayz("Ioni加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        try:
            # Tools3D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.Label = Tools3D.setLabel(self.ui.le_name.text())
            self.obj.ionizationOfGas = self.ui.cb_type.currentText()
            self.obj.gasPressure = self.ui.le_pressure.text()
            self.obj.gasTemperature = self.ui.le_temperature.text()
        except:
            Tools3D.sayz("Ioni设置数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())
