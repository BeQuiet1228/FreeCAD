# -*- coding: utf-8 -*-
import json
import traceback

import FreeCAD
import FreeCADGui
import PySide
from PySide import QtGui, QtCore

from Modeling.Modeling2D.Modeling2DCommand.TimeDomainSetting import TimeDomainSettingDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = TimeDomainSettingDialog.Ui_Dialog_TimeDomainComputingSettingDlg()
        self.ui.setupUi(self)
        self.obj = obj

        self.initDialog()
        self.setModal(True)

    def initDialog(self):
        # noinspection PyBroadException
        try:
            self.ui.checkBox_setting_mode.clicked.connect(self.onCheckBoxSettingMode)
            self.ui.checkBox_setting_stride.clicked.connect(self.onCheckBoxSettingStride)
            self.ui.checkBox_part.clicked.connect(self.setMacroParticleShow)
            self.ui.checkBox_setting_step.clicked.connect(self.onCheckBoxSettingStep)
            self.ui.radioButton_nonre.clicked.connect(self.onRadioButton)
            self.ui.radioButton_re.clicked.connect(self.onRadioButton)
            self.ui.pushButton_ok.clicked.connect(self.pushBtn_OK)

            self.onCheckBoxSettingMode()
            self.onCheckBoxSettingStride()
            self.setMacroParticleShow()
            self.onCheckBoxSettingStep()
            self.onRadioButton()
            # 隐藏下半部分
            self.hideBelowPart()

            self.loadData()
        except Exception as reason:
            Tools2D.sayz("初始化Dialog时出现错误，错误如下：")
            Tools2D.sayz(traceback.format_exc())
        else:
            Tools2D.sayz("正确初始化对话框")

    def hideUpPart(self):
        self.setWindowTitle(u"宏粒子合并")
        # 隐藏上半部分
        self.ui.label.hide()
        self.ui.lineEdit_compute_time.hide()
        self.ui.label_3.hide()
        self.ui.groupBox_WorkSpace_X.hide()
        self.ui.groupBox_WorkSpace_Y.hide()
        # 显示下半部分
        self.ui.checkBox_part.show()
        self.ui.lineEdit_max.show()
        self.ui.label_5.show()
        self.ui.label_4.show()
        self.ui.lineEdit_every.show()
        self.ui.comboBox.show()
        self.ui.label_6.show()
        self.ui.pushButton_ok.show()

    def hideBelowPart(self):
        self.setWindowTitle(u"时域计算设置")
        # 显示上半部分
        self.ui.label.show()
        self.ui.lineEdit_compute_time.show()
        self.ui.label_3.show()
        self.ui.groupBox_WorkSpace_X.show()
        self.ui.groupBox_WorkSpace_Y.show()
        # 隐藏下半部分
        self.ui.groupBox_WorkSpace_Y_2.hide()
        self.ui.checkBox_part.hide()
        self.ui.lineEdit_max.hide()
        self.ui.label_5.hide()
        self.ui.label_4.hide()
        self.ui.lineEdit_every.hide()
        self.ui.comboBox.hide()
        self.ui.label_6.hide()
        self.ui.pushButton_ok.show()

    def pushBtn_OK(self):
        self.keepData()
        FreeCADGui.runCommand("CreateM2D")
        self.close()

    def pushBtn_Cancel(self):
        self.close()

    def loadData(self):
        try:
            # 计算时间
            self.ui.lineEdit_compute_time.setText(self.obj.computationTime)
            # 场计算设置
            self.ui.comboBox_filed_arithmetic.setCurrentIndex(
                self.ui.comboBox_filed_arithmetic.findText(self.obj.fieldAlgorithm))
            # 设置模式
            self.ui.checkBox_setting_mode.setChecked(self.obj.isSettingPattern)
            self.ui.radioButton_EM.setChecked(self.obj.isEM)
            self.ui.radioButton_TE.setChecked(self.obj.isTE)
            self.ui.radioButton_TM.setChecked(self.obj.isTM)
            # 设置步长
            self.ui.checkBox_setting_stride.setChecked(self.obj.isSetStep)
            self.ui.lineEdit_setting_stride.setText(self.obj.setStep)
            # 粒子计算设置
            self.ui.checkBox_setting_chargeContinuity.setChecked(self.obj.isSetAlgorithm)
            try:
                # self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(DlgData["Types"]))
                # self.ui.checkBox_part.setChecked(DlgData["isChecked_part"])
                # self.ui.lineEdit_every.setText(DlgData["EveryNum"])
                # self.ui.lineEdit_max.setText(DlgData["MaxNum"])
                pass
            except:
                FreeCAD.Console.PrintMessage("设置宏粒子出错！")
            try:
                # 粒子计算时间步间隔
                self.ui.checkBox_setting_step.setChecked(self.obj.isParticleCalculatesTimeStepInterval)
                self.ui.lineEdit_setting_step.setText(self.obj.particleCalculatesTimeStepInterval)
                self.ui.radioButton_re.setChecked(self.obj.isRelativistic)
                self.ui.radioButton_nonre.setChecked(self.obj.isNonrelativistic)
                self.onCheckBoxSettingMode()
                self.onCheckBoxSettingStep()
                self.onCheckBoxSettingStride()
                self.setMacroParticleShow()
            except:
                FreeCAD.Console.PrintMessage("\n设置时间步长间隔出错!")
        except KeyError as reason:
            FreeCAD.Console.PrintMessage(str(reason))

    def keepData(self):
        try:
            # 计算时间
            self.obj.computationTime = self.ui.lineEdit_compute_time.text().replace(" ", "")
            # 场计算设置
            self.obj.fieldAlgorithm = self.ui.comboBox_filed_arithmetic.currentText()
            # 设置模式
            self.obj.isSettingPattern = self.ui.checkBox_setting_mode.isChecked()
            self.obj.isEM = self.ui.radioButton_EM.isChecked()
            self.obj.isTE = self.ui.radioButton_TE.isChecked()
            self.obj.isTM = self.ui.radioButton_TM.isChecked()
            # 设置步长
            self.obj.isSetStep = self.ui.checkBox_setting_stride.isChecked()
            self.obj.setStep = self.ui.lineEdit_setting_stride.text().replace(" ", "")
            # 粒子计算设置
            self.obj.isSetAlgorithm = self.ui.checkBox_setting_chargeContinuity.isChecked()
            self.obj.isParticleCalculatesTimeStepInterval = self.ui.checkBox_setting_step.isChecked()
            self.obj.particleCalculatesTimeStepInterval = self.ui.lineEdit_setting_step.text().replace(" ", "")
            self.obj.isRelativistic = self.ui.radioButton_re.isChecked()
            self.obj.isNonrelativistic = self.ui.radioButton_nonre.isChecked()
        except KeyError as reason:
            FreeCAD.Console.PrintMessage(str(reason))
        else:
            Tools2D.sayz("成功设置信息到Object")

    def onCheckBoxSettingMode(self):
        self.ui.radioButton_EM.setEnabled(self.ui.checkBox_setting_mode.isChecked())
        self.ui.radioButton_TE.setEnabled(self.ui.checkBox_setting_mode.isChecked())
        self.ui.radioButton_TM.setEnabled(self.ui.checkBox_setting_mode.isChecked())

    def setMacroParticleShow(self):
        self.ui.comboBox.setEnabled(self.ui.checkBox_part.isChecked())
        self.ui.lineEdit_every.setEnabled(self.ui.checkBox_part.isChecked())
        self.ui.lineEdit_max.setEnabled(self.ui.checkBox_part.isChecked())

    def onCheckBoxSettingStride(self):
        self.ui.lineEdit_setting_stride.setEnabled(self.ui.checkBox_setting_stride.isChecked())

    def onCheckBoxSettingStep(self):
        self.ui.lineEdit_setting_step.setEnabled(self.ui.checkBox_setting_step.isChecked())
        self.ui.radioButton_re.setEnabled(self.ui.checkBox_setting_step.isChecked())
        self.ui.radioButton_nonre.setEnabled(self.ui.checkBox_setting_step.isChecked())

    def onRadioButton(self):
        flag_re = self.ui.radioButton_re.isChecked()
        if flag_re:
            self.ui.radioButton_re.setChecked(True)
            self.ui.radioButton_nonre.setChecked(False)
        else:
            self.ui.radioButton_re.setChecked(False)
            self.ui.radioButton_nonre.setChecked(True)

