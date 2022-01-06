# -*- coding: utf-8 -*-
import traceback
import FreeCAD
import FreeCADGui
from PySide import QtGui
import DefTimerDialog
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = DefTimerDialog.Ui_CustomTimerDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        self.slotTypeChanged()
        self.ui.typeComboBox.currentIndexChanged.connect(self.slotTypeChanged)

        # DefTimer的名字是固定的，不允许修改
        self.ui.LineEdit_Name.setEnabled(False)

    def getInfoFromObj(self):
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)

            self.ui.typeComboBox.setCurrentIndex(self.ui.typeComboBox.findText(self.obj.defTimerType))
            # 定时基准
            self.ui.radioButton_step.setChecked(self.obj.isTimeSteps)
            self.ui.radioButton_simulate.setChecked(self.obj.isSimulationSteps)
            # 起始时刻
            self.ui.LineEdit_start.setText(self.obj.startTime)
            # 结束时刻
            self.ui.LineEdit_end.setText(self.obj.endTime)
            # 定时周期
            self.ui.LineEdit_period.setText(self.obj.timeCycle)
            # 离散时刻
            self.ui.LineEdit_Discrete_time.setText(self.obj.discreteTime)
        except:
            Tools3D.sayz("DefTimer加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
            # DefTimer的名字是固定的，不允许修改
            self.obj.defTimerType = self.ui.typeComboBox.currentText()
            # 定时基准
            if self.ui.radioButton_step.isChecked():
                self.obj.isTimeSteps = True
            else:
                self.obj.isTimeSteps = False

            if self.ui.radioButton_simulate.isChecked():
                self.obj.isSimulationSteps = True
            else:
                self.obj.isSimulationSteps = False
            # 起始时刻
            self.obj.startTime = self.ui.LineEdit_start.text().replace(" ", "")
            # 结束时刻
            self.obj.endTime = self.ui.LineEdit_end.text().replace(" ", "")
            # 定时周期
            self.obj.timeCycle = self.ui.LineEdit_period.text().replace(" ", "")
            # 离散时刻
            self.obj.discreteTime = self.ui.LineEdit_Discrete_time.text()
        except:
            Tools3D.sayz("DefTimer加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def slotTypeChanged(self):
        if self.ui.typeComboBox.currentIndex() == 0:
            self.ui.LineEdit_Discrete_time.setEnabled(False)
            self.ui.LineEdit_end.setEnabled(True)
            self.ui.LineEdit_period.setEnabled(True)
            self.ui.LineEdit_start.setEnabled(True)
        if self.ui.typeComboBox.currentIndex() == 1:
            self.ui.LineEdit_Discrete_time.setEnabled(True)
            self.ui.LineEdit_end.setEnabled(False)
            self.ui.LineEdit_period.setEnabled(False)
            self.ui.LineEdit_start.setEnabled(False)


