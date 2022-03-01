# -*- coding: utf-8 -*-
import traceback

import FreeCAD
import FreeCADGui
from PySide import QtGui
# 跟DefTimerDialog公用一个Dialog
from Modeling.Modeling2D.Modeling2DCommand.DefTimer import DefTimerDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = DefTimerDialog.Ui_CustomTimerDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.isKeepData = False

    def initDialog(self):
        self.loadData()
        self.slotTypeChanged()
        # self.ui.LineEdit_Name.setEnabled(False)
        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)
        self.ui.typeComboBox.currentIndexChanged.connect(self.slotTypeChanged)

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def slotOK(self):
        self.isKeepData = True
        self.close()

    def loadData(self):
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
            Tools2D.sayz("CustomTimer加载数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

    def keepData(self):
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())

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
            Tools2D.sayz("CustomTimer设置数据时出现异常")
            Tools2D.sayz(traceback.format_exc())

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

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)


