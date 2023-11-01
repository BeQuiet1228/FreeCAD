# -*- coding: utf-8 -*-
import traceback
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import CustomTimerDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = CustomTimerDialog.Ui_CustomTimerDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            self.slotCustomTimer()
            self.ui.typeComboBox.currentIndexChanged.connect(self.slotCustomTimer)

        except:
            Tools3D.sayz("CustomTimer加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.typeComboBox.setCurrentIndex(self.ui.typeComboBox.findText(self.obj.CustomTimerType))
            self.ui.radioButton_step.setChecked(self.obj.isTimerStep)
            self.ui.radioButton_simulate.setChecked(self.obj.isTimerSimulate)
            self.ui.LineEdit_start.setText(self.obj.startTime)
            self.ui.LineEdit_end.setText(self.obj.endTime)
            self.ui.LineEdit_period.setText(self.obj.period)
            self.ui.LineEdit_Discrete_time.setText(self.obj.DiscreteTime)
        except:
            Tools3D.sayz("CustomTimer加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
            self.obj.CustomTimerType = self.ui.typeComboBox.currentText()
            self.obj.isTimerStep = self.ui.radioButton_step.isChecked()
            self.obj.isTimerSimulate = self.ui.radioButton_simulate.isChecked()
            self.obj.startTime = self.ui.LineEdit_start.text().replace(" ", "")
            self.obj.endTime = self.ui.LineEdit_end.text().replace(" ", "")
            self.obj.period = self.ui.LineEdit_period.text().replace(" ", "")
            self.obj.DiscreteTime = self.ui.LineEdit_Discrete_time.text()
        except:
            Tools3D.sayz("CustomTimer加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def slotCustomTimer(self):
        if self.ui.typeComboBox.currentIndex() == 0:
            self.ui.LineEdit_start.setEnabled(True)
            self.ui.LineEdit_end.setEnabled(True)
            self.ui.LineEdit_period.setEnabled(True)
            self.ui.LineEdit_Discrete_time.setEnabled(False)
        elif self.ui.typeComboBox.currentIndex() == 1:
            self.ui.LineEdit_start.setEnabled(False)
            self.ui.LineEdit_end.setEnabled(False)
            self.ui.LineEdit_period.setEnabled(False)
            self.ui.LineEdit_Discrete_time.setEnabled(True)
        else:
            pass




