# -*- coding: utf-8 -*-
import traceback
import FreeCAD
import FreeCADGui
import PySide
from PySide import QtGui
from Model3D.Command3D.Physics3DCommand.TimeDomainSetting import TimeDomainSettingDialog
from Model3D.Tools import Tools3D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = TimeDomainSettingDialog.Ui_Dialog_TimeDomainComputingSettingDlg()
        self.ui.setupUi(self)
        self.obj = obj

        self.initDialog()
        self.setModal(True)
        self.ui.groupBox_WorkSpace_Y_2.hide()

    def initDialog(self):
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
            self.loadData()

        except Exception as reason:
            Tools3D.sayz("初始化Dialog时出现错误，错误如下：")
            Tools3D.sayz(traceback.format_exc())
        else:
            Tools3D.sayz("正确初始化对话框")

    def pushBtn_OK(self):
        self.keepData()
        self.close()
        FreeCADGui.runCommand("CreateM3D_new")

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
                Tools3D.sayz("\n设置时间步长间隔出错!")
        except KeyError as reason:
            Tools3D.sayz("error:" + str(reason))

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
            Tools3D.sayz("KeyError:" + str(reason))
        else:
            Tools3D.sayz("成功设置信息到Object")

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
