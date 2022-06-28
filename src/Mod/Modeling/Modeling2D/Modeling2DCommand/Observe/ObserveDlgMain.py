# -*- coding: utf-8 -*-
import traceback

import ObserveDialog
from PySide import QtGui
import FreeCAD

from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI
from Modeling.Modeling2D.Tools.Tools2D import sayz


def getNewParticle():
    NewParticle_list = Tools2D.getSpecificTypePhyAndProObjects(u"ParticleDefine")
    NewParticleName_list = []
    for ele in NewParticle_list:
        NewParticleName_list.append(ele.Label)
    return NewParticleName_list


class ShowDialog(BaseDialog.BaseOtherDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialog.BaseOtherDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        """
        设置ui
        """
        self.ui = ObserveDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(False)

    def helperInitDialog(self):
        """
        初始化界面，设置界面逻辑，绑定信号与槽
        """
        self.defaultValue = []
        # 列表的初始化
        self.initObservationField()
        self.initParticles()
        # 此处按钮命名需要修改
        self.ui.cb_observationType.currentIndexChanged.connect(self.slotObservation)
        self.ui.cb_optionType.currentIndexChanged.connect(self.slotOption)
        self.ui.rb_isCheckNormal1.toggled.connect(self.slotRadioButton)
        self.ui.rb_isCheckNormal2.toggled.connect(self.slotRadioButton)
        self.ui.le_point1_X.textChanged.connect(self.lePointSignals)
        self.ui.le_point1_Y.textChanged.connect(self.lePointSignals)

        self.ui.rb_isField.toggled.connect(self.observeSignals)
        self.ui.rb_isFieldIntegral.toggled.connect(self.observeSignals)
        self.ui.rb_isFieldPower.toggled.connect(self.observeSignals)
        self.ui.rb_isFieldEnergy.toggled.connect(self.observeSignals)

        self.ui.rb_isParticleStatistics.toggled.connect(self.observeSignals)
        self.ui.rb_isCollectedParticles.toggled.connect(self.observeSignals)
        self.ui.rb_isEmittedParticle.toggled.connect(self.observeSignals)
        self.ui.rb_isAnnihilatingParticle.toggled.connect(self.observeSignals)

        self.ui.cb_particles2.currentIndexChanged.connect(self.observeSignals)
        # 隐藏粒子统计，收集粒子，发射粒子，湮灭粒子
        # self.ui.rb_isParticleStatistics.hide()
        # self.ui.rb_isCollectedParticles.hide()
        # self.ui.rb_isEmittedParticle.hide()
        # self.ui.rb_isAnnihilatingParticle.hide()
        # self.ui.le_particles1.hide()
        # self.ui.cb_particles2.hide()
        # self.ui.cb_particles3.hide()
        # self.ui.cb_particles4.hide()

        self.ui.cb_isFFT.stateChanged.connect(self.isFFTSignals)
        self.ui.cb_isFrequencyRange.stateChanged.connect(self.isFrequencyRangeSignals)
        self.ui.cb_isTimeRange.stateChanged.connect(self.isTimeRangeSignals)
        self.ui.cb_isObservationInterval.stateChanged.connect(self.isObservationIntervalSignals)
        self.ui.cb_isDataDisplay.stateChanged.connect(self.isDataDisplaySignals)

        # self.ui.pb_ok.clicked.connect(self.slotOK)
        #self.ui.pb_cancel.clicked.connect(self.slotCancel)

        self.getInfoFromObj()
        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        # 根据坐标系初始化面板
        self.ui.lb_x.setText(self.x)
        self.ui.lb_y.setText(self.y)
        self.ui.rb_isCheckNormal1.setText(self.x)
        self.ui.rb_isCheckNormal2.setText(self.y)

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            self.ui.le_name.setText(self.obj.Label)

            itemIndex = self.ui.cb_observationType.findText(str(self.obj.ObservationType))
            self.ui.cb_observationType.setCurrentIndex(itemIndex)
            self.slotObservation()

            self.ui.le_alias.setText(self.obj.alias)

            itemIndex = self.ui.cb_optionType.findText(str(self.obj.optionType))
            self.ui.cb_optionType.setCurrentIndex(itemIndex)
            self.slotOption()
            # self.ui.le_optionType.setText(self.obj.optionType)

            self.ui.le_point1_X.setText(self.obj.point1_X)
            self.ui.le_point1_Y.setText(self.obj.point1_Y)
            itemIndex1 = self.ui.cb_point1_name.findText(str(self.obj.point1_name))
            self.ui.cb_point1_name.setCurrentIndex(itemIndex1)

            self.ui.le_point2_X.setText(self.obj.point2_X)
            self.ui.le_point2_Y.setText(self.obj.point2_Y)
            itemIndex2 = self.ui.cb_point2_name.findText(str(self.obj.point2_name))
            self.ui.cb_point2_name.setCurrentIndex(itemIndex2)

            self.ui.rb_isCheckNormal1.setChecked(self.obj.isCheckNormal1)
            self.ui.rb_isCheckNormal2.setChecked(self.obj.isCheckNormal2)

            self.ui.rb_isField.setChecked(self.obj.isField)
            self.ui.rb_isFieldIntegral.setChecked(self.obj.isFieldIntegral)
            self.ui.rb_isFieldPower.setChecked(self.obj.isFieldPower)
            self.ui.rb_isFieldEnergy.setChecked(self.obj.isFieldEnergy)
            self.ui.rb_isParticleStatistics.setChecked(self.obj.isParticleStatistics)
            self.ui.rb_isCollectedParticles.setChecked(self.obj.isCollectedParticles)
            self.ui.rb_isEmittedParticle.setChecked(self.obj.isEmittedParticle)
            self.ui.rb_isAnnihilatingParticle.setChecked(self.obj.isAnnihilatingParticle)

            itemIndex3 = self.ui.cb_field.findText(str(self.obj.field))
            self.ui.cb_field.setCurrentIndex(itemIndex3)
            itemIndex4 = self.ui.cb_fieldIntegral.findText(str(self.obj.fieldIntegral))
            self.ui.cb_fieldIntegral.setCurrentIndex(itemIndex4)
            itemIndex5 = self.ui.cb_fieldPower.findText(str(self.obj.fieldPower))
            self.ui.cb_fieldPower.setCurrentIndex(itemIndex5)
            itemIndex6 = self.ui.cb_fieldEnergy.findText(str(self.obj.fieldEnergy))
            self.ui.cb_fieldEnergy.setCurrentIndex(itemIndex6)
            self.ui.le_particles1.setText(self.obj.particles1)
            itemIndex7 = self.ui.cb_particles2.findText(str(self.obj.particles2))
            self.ui.cb_particles2.setCurrentIndex(itemIndex7)
            itemIndex8 = self.ui.cb_particles3.findText(str(self.obj.particles3))
            self.ui.cb_particles3.setCurrentIndex(itemIndex8)
            itemIndex9 = self.ui.cb_particles4.findText(str(self.obj.particles4))
            self.ui.cb_particles4.setCurrentIndex(itemIndex9)

            self.ui.cb_isFFT.setChecked(self.obj.isFFT)
            self.ui.rb_isRealAnalysis.setChecked(self.obj.isRealAnalysis)
            self.ui.rb_isComplexAnalysis.setChecked(self.obj.isComplexAnalysis)

            self.ui.cb_isFrequencyRange.setChecked(self.obj.isFrequencyRange)
            self.ui.le_frequencyRange1.setText(self.obj.frequencyRange1)
            self.ui.le_frequencyRange2.setText(self.obj.frequencyRange2)

            self.ui.cb_isTimeRange.setChecked(self.obj.isTimeRange)
            self.ui.le_timeRange1.setText(self.obj.timeRange1)
            self.ui.le_timeRange2.setText(self.obj.timeRange2)

            self.ui.cb_isObservationInterval.setChecked(self.obj.isObservationInterval)
            self.ui.le_observationInterval.setText(self.obj.observationInterval)

            self.ui.cb_isDataDisplay.setChecked(self.obj.isDataDisplay)
            self.ui.rb_isTimeAverage.setChecked(self.obj.isTimeAverage)
            self.ui.rb_isRcAnalyze.setChecked(self.obj.isRcAnalyze)
            self.ui.le_filteringTimeParameter.setText(self.obj.filteringTimeParameter)

        except AttributeError:
            Tools2D.sayz("Observe--异常--在读取Object属性时出现异常")
            Tools2D.sayz(traceback.format_exc())
        except Exception as e:
            Tools2D.sayz("Observe--" + str(e))
        else:
            Tools2D.sayz("Observe--成功--读取Object信息")

    def keepData(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.ObservationType = self.ui.cb_observationType.currentText()
            self.obj.alias = self.ui.le_alias.text()
            self.obj.optionType = self.ui.cb_optionType.currentText()
            self.obj.point1_X = self.ui.le_point1_X.text()
            self.obj.point1_Y = self.ui.le_point1_Y.text()
            self.obj.point1_name = self.ui.cb_point1_name.currentText()
            self.obj.point2_X = self.ui.le_point2_X.text()
            self.obj.point2_Y = self.ui.le_point2_Y.text()
            self.obj.point2_name = self.ui.cb_point2_name.currentText()
            self.obj.isCheckNormal1 = self.ui.rb_isCheckNormal1.isChecked()
            self.obj.isCheckNormal2 = self.ui.rb_isCheckNormal2.isChecked()
            self.obj.isField = self.ui.rb_isField.isChecked()
            self.obj.isFieldIntegral = self.ui.rb_isFieldIntegral.isChecked()
            self.obj.isFieldPower = self.ui.rb_isFieldPower.isChecked()
            self.obj.isFieldEnergy = self.ui.rb_isFieldEnergy.isChecked()
            self.obj.isParticleStatistics = self.ui.rb_isParticleStatistics.isChecked()
            self.obj.isCollectedParticles = self.ui.rb_isCollectedParticles.isChecked()
            self.obj.isEmittedParticle = self.ui.rb_isEmittedParticle.isChecked()
            self.obj.isAnnihilatingParticle = self.ui.rb_isAnnihilatingParticle.isChecked()
            self.obj.field = self.ui.cb_field.currentText()
            self.obj.fieldIntegral = self.ui.cb_fieldIntegral.currentText()
            self.obj.fieldPower = self.ui.cb_fieldPower.currentText()
            self.obj.fieldEnergy = self.ui.cb_fieldEnergy.currentText()
            self.obj.particles1 = self.ui.le_particles1.text()
            self.obj.particles2 = self.ui.cb_particles2.currentText()
            self.obj.particles3 = self.ui.cb_particles3.currentText()
            self.obj.particles4 = self.ui.cb_particles4.currentText()

            self.obj.isFFT = self.ui.cb_isFFT.isChecked()
            self.obj.isRealAnalysis = self.ui.rb_isRealAnalysis.isChecked()
            self.obj.isComplexAnalysis = self.ui.rb_isComplexAnalysis.isChecked()

            self.obj.isFrequencyRange = self.ui.cb_isFrequencyRange.isChecked()
            self.obj.frequencyRange1 = self.ui.le_frequencyRange1.text()
            self.obj.frequencyRange2 = self.ui.le_frequencyRange2.text()

            self.obj.isTimeRange = self.ui.cb_isTimeRange.isChecked()
            self.obj.timeRange1 = self.ui.le_timeRange1.text()
            self.obj.timeRange2 = self.ui.le_timeRange2.text()

            self.obj.isObservationInterval = self.ui.cb_isObservationInterval.isChecked()
            self.obj.observationInterval = self.ui.le_observationInterval.text()

            self.obj.isDataDisplay = self.ui.cb_isDataDisplay.isChecked()
            self.obj.isTimeAverage = self.ui.rb_isTimeAverage.isChecked()
            self.obj.isRcAnalyze = self.ui.rb_isRcAnalyze.isChecked()
            self.obj.filteringTimeParameter = self.ui.le_filteringTimeParameter.text()

        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def slotObservation(self):
        """
        根据cb_observationType的选项刷新cb_optionType中的内容
        """
        # noinspection PyBroadException
        try:
            self.ui.cb_optionType.clear()
            self.ui.cb_optionType.addItem("未指定")
            self.ui.le_point1_X.setEnabled(True)
            self.ui.le_point1_Y.setEnabled(True)
            self.ui.le_point2_X.setEnabled(True)
            self.ui.le_point2_Y.setEnabled(True)
            self.ui.rb_isCheckNormal1.setEnabled(True)
            self.ui.rb_isCheckNormal2.setEnabled(True)
            Orthogonal_list = []
            if self.ui.cb_observationType.currentIndex() == 0:
                Orthogonal_list = Tools2D.getLabelsByType(Tools2D.ObjectType.Point)
                self.ui.le_point2_X.setEnabled(False)
                self.ui.le_point2_Y.setEnabled(False)
                self.ui.rb_isCheckNormal1.setEnabled(False)
                self.ui.rb_isCheckNormal2.setEnabled(False)
            elif self.ui.cb_observationType.currentIndex() == 1:
                Orthogonal_list = Tools2D.getLabelsByType(Tools2D.ObjectType.LineConformal)
                self.ui.le_point2_X.setEnabled(not self.ui.rb_isCheckNormal1.isChecked())
                self.ui.le_point2_Y.setEnabled(not self.ui.rb_isCheckNormal2.isChecked())
            elif self.ui.cb_observationType.currentIndex() == 2:
                self.ui.cb_optionType.addItem("OSYS$AREA")
                # Orthogonal_list = Tools2D.getLabelsByType(Tools2D.ObjectType.AreaConformal)
                Orthogonal_list = Tools2D.getAllAreaLabel()
                self.ui.rb_isCheckNormal1.setEnabled(False)
                self.ui.rb_isCheckNormal2.setEnabled(False)
            for i in Orthogonal_list:
                self.ui.cb_optionType.addItem(i)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def slotOption(self):
        """
        当Option的选项发生变化时触发的槽函数
        """
        if self.ui.cb_optionType.currentIndex() < 0:
            return
        self.ui.rb_isCheckNormal1.setEnabled(False)
        self.ui.rb_isCheckNormal2.setEnabled(False)
        objName = self.ui.cb_optionType.currentText()
        if self.ui.cb_observationType.currentIndex() == 0:
            if objName == '未指定':
                self.ui.le_point1_X.setEnabled(True)
                self.ui.le_point1_Y.setEnabled(True)
            else:
                modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                self.ui.le_point1_X.setText(modelData["point1.x"])
                self.ui.le_point1_Y.setText(modelData["point1.y"])
                self.ui.le_point1_X.setEnabled(False)
                self.ui.le_point1_Y.setEnabled(False)
            self.ui.le_point2_X.setEnabled(False)
            self.ui.le_point2_Y.setEnabled(False)
            # 法向不可选
            self.ui.rb_isCheckNormal1.setEnabled(False)
            self.ui.rb_isCheckNormal2.setEnabled(False)
            # 设置分类项
            self.ui.rb_isField.setEnabled(True)
            self.ui.rb_isFieldIntegral.setEnabled(False)
            self.ui.rb_isFieldPower.setEnabled(False)
            self.ui.rb_isFieldEnergy.setEnabled(False)

            self.ui.rb_isParticleStatistics.setEnabled(False)
            self.ui.rb_isCollectedParticles.setEnabled(False)
            self.ui.rb_isEmittedParticle.setEnabled(False)
            self.ui.rb_isAnnihilatingParticle.setEnabled(False)

        elif self.ui.cb_observationType.currentIndex() == 1:
            if objName == '未指定':
                self.ui.le_point1_X.setEnabled(True)
                self.ui.le_point1_Y.setEnabled(True)
                self.slotRadioButton()
                # 法向不可选
                self.ui.rb_isCheckNormal1.setEnabled(True)
                self.ui.rb_isCheckNormal2.setEnabled(True)
            else:
                modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                if objName in self.defaultValue:
                    pass
                else:
                    self.ui.le_point1_X.setText(modelData["point1.x"])
                    self.ui.le_point1_Y.setText(modelData["point1.y"])
                    self.ui.le_point2_X.setText(modelData["point2.x"])
                    self.ui.le_point2_Y.setText(modelData["point2.y"])
                    # 法向
                    if modelData["normal"] == "X" or modelData["normal"] == "x":
                        self.ui.rb_isCheckNormal1.setChecked(True)
                    elif modelData["normal"] == "Y" or modelData["normal"] == "y":
                        self.ui.rb_isCheckNormal2.setChecked(True)
                    else:
                        Tools2D.sayz("get Area_Conformal error")
                self.ui.le_point1_X.setEnabled(False)
                self.ui.le_point1_Y.setEnabled(False)
                self.ui.le_point2_X.setEnabled(False)
                self.ui.le_point2_Y.setEnabled(False)
            # 设置分类项
            self.ui.rb_isField.setEnabled(True)
            self.ui.rb_isFieldIntegral.setEnabled(True)
            self.ui.rb_isFieldPower.setEnabled(True)
            self.ui.rb_isFieldEnergy.setEnabled(False)

            self.ui.rb_isParticleStatistics.setEnabled(False)
            self.ui.rb_isCollectedParticles.setEnabled(True)
            self.ui.rb_isEmittedParticle.setEnabled(True)
            self.ui.rb_isAnnihilatingParticle.setEnabled(True)

        elif self.ui.cb_observationType.currentIndex() == 2:
            if objName == '未指定':
                self.ui.le_point1_X.setEnabled(True)
                self.ui.le_point1_Y.setEnabled(True)
                self.ui.le_point2_X.setEnabled(True)
                self.ui.le_point2_Y.setEnabled(True)
            elif objName == 'OSYS$AREA':
                self.ui.le_point1_X.setEnabled(False)
                self.ui.le_point1_Y.setEnabled(False)
                self.ui.le_point2_X.setEnabled(False)
                self.ui.le_point2_Y.setEnabled(False)
            else:
                if objName in self.defaultValue:
                    pass
                else:
                    area_conformal_list = Tools2D.getLabelsByType(Tools2D.ObjectType.AreaConformal)
                    # 当objName 不是正投影面时，不更新坐标信息
                    if objName in area_conformal_list:
                        modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                        self.ui.le_point1_X.setText(modelData["point1.x"])
                        self.ui.le_point1_Y.setText(modelData["point1.y"])
                        self.ui.le_point2_X.setText(modelData["point2.x"])
                        self.ui.le_point2_Y.setText(modelData["point2.y"])
                self.ui.le_point1_X.setEnabled(False)
                self.ui.le_point1_Y.setEnabled(False)
                self.ui.le_point2_X.setEnabled(False)
                self.ui.le_point2_Y.setEnabled(False)
            # 法向不可选
            self.ui.rb_isCheckNormal1.setEnabled(False)
            self.ui.rb_isCheckNormal2.setEnabled(False)
            # 设置分类项
            self.ui.rb_isField.setEnabled(True)
            self.ui.rb_isFieldIntegral.setEnabled(False)
            self.ui.rb_isFieldPower.setEnabled(True)
            self.ui.rb_isFieldEnergy.setEnabled(True)

            self.ui.rb_isParticleStatistics.setEnabled(True)
            self.ui.rb_isCollectedParticles.setEnabled(True)
            self.ui.rb_isEmittedParticle.setEnabled(True)
            self.ui.rb_isAnnihilatingParticle.setEnabled(True)

    def helperOK(self):
        self.isKeepData = True
        self.close()

    def helperCancel(self):
        self.isKeepData = False
        self.close()

    def initObservationField(self):
        field_list = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3", "Q0", "E1AV", "E2AV", "E3AV",
                      "B1AV", "B2AV", "B3AV", "E1ST", "E2ST", "E3ST", "B1ST", "B2ST", "B3ST", "PHST", "B", "E"]
        for i in field_list:
            self.ui.cb_field.addItem(i)

    def slotRadioButton(self):
        """
        radioButton相关的槽函数，主要设置lineEdit的编辑状态
        """
        if self.ui.cb_observationType.currentIndex() == 1:
            self.ui.le_point2_X.setEnabled(not self.ui.rb_isCheckNormal1.isChecked())
            self.ui.le_point2_Y.setEnabled(not self.ui.rb_isCheckNormal2.isChecked())
        self.lePointSignals()
        self.observeSignals()

    def lePointSignals(self):
        iscb_observationType = self.ui.cb_observationType.currentText()
        if str(iscb_observationType) != "时间观测点":
            if not self.ui.le_point2_Y.isEnabled():
                self.ui.le_point2_Y.setText(self.ui.le_point1_Y.text())
            if not self.ui.le_point2_X.isEnabled():
                self.ui.le_point2_X.setText(self.ui.le_point1_X.text())
        self.observeSignals()

    def observeSignals(self):
        self.ui.cb_field.setEnabled(self.ui.rb_isField.isChecked())
        self.ui.cb_fieldIntegral.setEnabled(self.ui.rb_isFieldIntegral.isChecked())
        self.ui.cb_fieldPower.setEnabled(self.ui.rb_isFieldPower.isChecked())
        self.ui.cb_fieldEnergy.setEnabled(self.ui.rb_isFieldEnergy.isChecked())

        self.ui.le_particles1.setEnabled(self.ui.rb_isParticleStatistics.isChecked())
        self.ui.cb_particles2.setEnabled(self.ui.rb_isParticleStatistics.isChecked())
        self.ui.cb_particles3.setEnabled(self.ui.rb_isCollectedParticles.isChecked() or
                                         self.ui.rb_isEmittedParticle.isChecked() or
                                         self.ui.rb_isAnnihilatingParticle.isChecked())
        self.ui.cb_particles4.setEnabled(self.ui.rb_isCollectedParticles.isChecked() or
                                         self.ui.rb_isEmittedParticle.isChecked() or
                                         self.ui.rb_isAnnihilatingParticle.isChecked())

        if self.ui.rb_isParticleStatistics.isChecked():
            if self.ui.cb_particles2.currentIndex() == 0:
                self.ui.le_particles1.setEnabled(True)
                self.ui.cb_particles4.setEnabled(False)
            else:
                self.ui.le_particles1.setEnabled(False)
                self.ui.cb_particles4.setEnabled(True)

    def isFFTSignals(self):
        self.ui.rb_isRealAnalysis.setEnabled(self.ui.cb_isFFT.isChecked())
        self.ui.rb_isComplexAnalysis.setEnabled(self.ui.cb_isFFT.isChecked())

    def isFrequencyRangeSignals(self):
        self.ui.le_frequencyRange1.setEnabled(self.ui.cb_isFrequencyRange.isChecked())
        self.ui.le_frequencyRange2.setEnabled(self.ui.cb_isFrequencyRange.isChecked())

    def isTimeRangeSignals(self):
        self.ui.le_timeRange1.setEnabled(self.ui.cb_isTimeRange.isChecked())
        self.ui.le_timeRange2.setEnabled(self.ui.cb_isTimeRange.isChecked())

    def isObservationIntervalSignals(self):
        self.ui.le_observationInterval.setEnabled(self.ui.cb_isObservationInterval.isChecked())

    def isDataDisplaySignals(self):
        self.ui.rb_isTimeAverage.setEnabled(self.ui.cb_isDataDisplay.isChecked())
        self.ui.rb_isRcAnalyze.setEnabled(self.ui.cb_isDataDisplay.isChecked())
        self.ui.le_filteringTimeParameter.setEnabled(self.ui.cb_isDataDisplay.isChecked())

    def initParticles(self):
        ParticlesList = ["ALL", "ELECTRON", "PROTON"]
        ParticlesTypeList = getNewParticle()
        # for i in ParticlesList:
        #     self.ui.ComboBox_Observation_particle.addItem(i)
        for i in ParticlesTypeList:
            if i not in ParticlesList:
                self.ui.cb_particles4.addItem(i)