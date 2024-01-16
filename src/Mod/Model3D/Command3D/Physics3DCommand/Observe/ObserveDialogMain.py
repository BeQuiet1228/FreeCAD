# -*- coding: utf-8 -*-
import traceback
import ObserveDialog
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D, ObjectTools


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = ObserveDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        初始化界面，设置界面逻辑，绑定信号与槽
        """
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(self.ui))
        self.default_point_list = []
        self.default_line_list = []
        self.default_plane_list = ["OSYS$MIDPLANE1", "OSYS$MIDPLANE2", "OSYS$MIDPLANE3"]
        self.default_volume_list = ["OSYS$VOLUME"]
        # 列表的初始化
        self.initObservationField()
        self.initParticles()

        self.ui.cb_observationType.currentIndexChanged.connect(self.slotObservation)
        self.ui.cb_optionType.currentIndexChanged.connect(self.slotOption)
        self.ui.radioButton_x.toggled.connect(self.radioButton_clicked)
        self.ui.radioButton_y.toggled.connect(self.radioButton_clicked)
        self.ui.radioButton_z.toggled.connect(self.radioButton_clicked)
        self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
        self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
        self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

        self.ui.rb_isField.toggled.connect(self.observeSignals)
        self.ui.rb_isFieldIntegral.toggled.connect(self.observeSignals)
        self.ui.rb_isFieldPower.toggled.connect(self.observeSignals)
        self.ui.rb_isFieldEnergy.toggled.connect(self.observeSignals)

        self.ui.rb_isParticleStatistics.toggled.connect(self.observeSignals)
        self.ui.rb_isCollectedParticles.toggled.connect(self.observeSignals)
        self.ui.rb_isEmittedParticle.toggled.connect(self.observeSignals)
        self.ui.rb_isAnnihilatingParticle.toggled.connect(self.observeSignals)

        self.ui.cb_particles2.currentIndexChanged.connect(self.observeSignals)

        self.ui.cb_isFFT.stateChanged.connect(self.isFFTSignals)
        self.ui.cb_isFrequencyRange.stateChanged.connect(self.isFrequencyRangeSignals)
        self.ui.cb_isTimeRange.stateChanged.connect(self.isTimeRangeSignals)
        self.ui.cb_isObservationInterval.stateChanged.connect(self.isObservationIntervalSignals)
        self.ui.cb_isDataDisplay.stateChanged.connect(self.isDataDisplaySignals)

        # 获取当前坐标系及坐标系单位
        Tools3D.switchPointLabel(self.ui)
        Tools3D.switchRadioButtonLabel(self.ui)

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            self.ui.le_name.setText(self.obj.Label)
            Tools3D.setCoorToUI(self.ui, self.obj)
            Tools3D.setRadioButtonToUI(self.ui, self.obj)

            itemIndex = self.ui.cb_observationType.findText(str(self.obj.ObservationType))
            self.ui.cb_observationType.setCurrentIndex(itemIndex)
            self.slotObservation()
            self.ui.le_alias.setText(self.obj.alias)

            itemIndex = self.ui.cb_optionType.findText(str(self.obj.orthogonalProjectionPlane))
            self.ui.cb_optionType.setCurrentIndex(itemIndex)
            self.slotOption()

            itemIndex1 = self.ui.cb_point1_name.findText(str(self.obj.point1_name))
            self.ui.cb_point1_name.setCurrentIndex(itemIndex1)

            itemIndex2 = self.ui.cb_point2_name.findText(str(self.obj.point2_name))
            self.ui.cb_point2_name.setCurrentIndex(itemIndex2)

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

            if self.ui.cb_optionType.currentIndex() == 0:
                self.radioButton_clicked()

        except AttributeError:
            Tools3D.sayz("Observe--异常--在读取Object属性时出现异常")
            Tools3D.sayz(traceback.format_exc())
        except Exception as e:
            Tools3D.sayz("Observe--" + str(e))
        else:
            Tools3D.sayz("Observe--成功--读取Object信息")

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        try:
            # Tools3D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.Label = Tools3D.setLabel(self.ui.le_name.text())
            Tools3D.getUICoordinate(self.obj, self.ui)
            Tools3D.getUIRadioButton(self.obj, self.ui)

            self.obj.ObservationType = self.ui.cb_observationType.currentText()
            self.obj.alias = self.ui.le_alias.text()
            self.obj.orthogonalProjectionPlane = self.ui.cb_optionType.currentText()

            self.obj.point1_name = self.ui.cb_point1_name.currentText()
            self.obj.point2_name = self.ui.cb_point2_name.currentText()

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
            Tools3D.sayz("error:" + traceback.format_exc())
        pass

    def slotObservation(self):
        """
        根据cb_observationType的选项刷新cb_optionType中的内容，并更新界面信息
        """
        try:
            self.ui.cb_optionType.clear()
            self.ui.cb_optionType.addItem("未指定")
            Orthogonal_list = []
            ComboBox_list = []
            # 时间观测点
            if self.ui.cb_observationType.currentIndex() == 0:
                Orthogonal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Point)
                for i in self.default_point_list:
                    self.ui.cb_optionType.addItem(i)

                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Point)
                # 设置分类项
                self.ui.rb_isField.setEnabled(True)
                self.ui.rb_isFieldIntegral.setEnabled(False)
                self.ui.rb_isFieldPower.setEnabled(False)
                self.ui.rb_isFieldEnergy.setEnabled(False)

                self.ui.rb_isParticleStatistics.setEnabled(False)
                self.ui.rb_isCollectedParticles.setEnabled(False)
                self.ui.rb_isEmittedParticle.setEnabled(False)
                self.ui.rb_isAnnihilatingParticle.setEnabled(False)
                # 默认勾选场
                self.ui.rb_isField.setChecked(True)

            # 时间观测线
            elif self.ui.cb_observationType.currentIndex() == 1:
                Orthogonal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Line_Conformal)
                for i in self.default_line_list:
                    self.ui.cb_optionType.addItem(i)

                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Line_Conformal)
                # 设置分类项
                self.ui.rb_isField.setEnabled(True)
                self.ui.rb_isFieldIntegral.setEnabled(True)
                self.ui.rb_isFieldPower.setEnabled(False)
                self.ui.rb_isFieldEnergy.setEnabled(False)

                self.ui.rb_isParticleStatistics.setEnabled(False)
                self.ui.rb_isCollectedParticles.setEnabled(False)
                self.ui.rb_isEmittedParticle.setEnabled(False)
                self.ui.rb_isAnnihilatingParticle.setEnabled(False)
                # 默认以勾选场
                self.ui.rb_isField.setChecked(True)

            # 时间观测面
            elif self.ui.cb_observationType.currentIndex() == 2:
                Orthogonal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Area_Conformal)
                for i in self.default_plane_list:
                    self.ui.cb_optionType.addItem(i)

                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Area_Conformal)
                # 设置分类项
                self.ui.rb_isField.setEnabled(True)
                self.ui.rb_isFieldIntegral.setEnabled(True)
                self.ui.rb_isFieldPower.setEnabled(True)
                self.ui.rb_isFieldEnergy.setEnabled(False)

                self.ui.rb_isParticleStatistics.setEnabled(False)
                self.ui.rb_isCollectedParticles.setEnabled(True)
                self.ui.rb_isEmittedParticle.setEnabled(True)
                self.ui.rb_isAnnihilatingParticle.setEnabled(True)
                # 默认以勾选场
                self.ui.rb_isField.setChecked(True)

            # 时间观测体
            elif self.ui.cb_observationType.currentIndex() == 3:
                Orthogonal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
                for i in self.default_volume_list:
                    self.ui.cb_optionType.addItem(i)

                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Vol_Conformal)
                # 设置分类项
                self.ui.rb_isField.setEnabled(False)
                self.ui.rb_isFieldIntegral.setEnabled(False)
                self.ui.rb_isFieldPower.setEnabled(False)
                self.ui.rb_isFieldEnergy.setEnabled(True)

                self.ui.rb_isParticleStatistics.setEnabled(True)
                self.ui.rb_isCollectedParticles.setEnabled(True)
                self.ui.rb_isEmittedParticle.setEnabled(True)
                self.ui.rb_isAnnihilatingParticle.setEnabled(True)
                # 默认以勾选场能量
                self.ui.rb_isFieldEnergy.setChecked(True)

            for i in range(self.ui.cb_optionType.count()):
                ComboBox_list.append(self.ui.cb_optionType.itemText(i))
            for i in Orthogonal_list:
                if i not in ComboBox_list:
                    self.ui.cb_optionType.addItem(i)

        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def slotOption(self):
        """
        当Option的选项发生变化时触发的槽函数
        """
        try:
            # 时间观测点
            if self.ui.cb_observationType.currentIndex() == 0:
                curType = ObjectTools.ObjectType.Point
                typeObjList = self.default_point_list
            # 时间观测线
            elif self.ui.cb_observationType.currentIndex() == 1:
                curType = ObjectTools.ObjectType.Line_Conformal
                typeObjList = self.default_line_list
            # 时间观测面
            elif self.ui.cb_observationType.currentIndex() == 2:
                curType = ObjectTools.ObjectType.Area_Conformal
                typeObjList = self.default_plane_list
            # 时间观测体
            elif self.ui.cb_observationType.currentIndex() == 3:
                curType = ObjectTools.ObjectType.Vol_Conformal
                typeObjList = self.default_volume_list
            else:
                Tools3D.sayz("error")
                return

            if self.ui.cb_optionType.currentIndex() < 0:
                pass
            # 未选择
            elif self.ui.cb_optionType.currentIndex() == 0:
                Tools3D.setCoordEnabled(self.ui, curType)
            # 其它
            else:
                objName = self.ui.cb_optionType.currentText()
                if objName in typeObjList:
                    Tools3D.setIsEdit(self.ui, False)
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                    Tools3D.setIsEdit(self.ui, False)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())


    def initObservationField(self):
        field_list = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3", "Q0", "E1AV", "E2AV", "E3AV",
                      "B1AV", "B2AV", "B3AV", "E1ST", "E2ST", "E3ST", "B1ST", "B2ST", "B3ST", "PHST", "B", "E"]
        for i in field_list:
            self.ui.cb_field.addItem(i)

    # x法向修改时，修改起点即修改终点
    def LineEdit_start_x_textChanged(self):
        if not self.ui.LineEdit_end_x.isEnabled():
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # y法向修改时，修改起点即修改终点
    def LineEdit_start_y_textChanged(self):
        if not self.ui.LineEdit_end_y.isEnabled():
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # z法向修改时，修改起点即修改终点
    def LineEdit_start_z_textChanged(self):
        if not self.ui.LineEdit_end_z.isEnabled():
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    # 点击法向按钮
    def radioButton_clicked(self):
        if self.ui.cb_observationType.currentIndex() == 1:
            if self.ui.radioButton_x.isChecked():
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
                self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
                self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
            elif self.ui.radioButton_y.isChecked():
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
                self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
                self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
            elif self.ui.radioButton_z.isChecked():
                self.ui.LineEdit_end_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
                self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        elif self.ui.cb_observationType.currentIndex() == 2:
            if self.ui.radioButton_x.isChecked():
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
                self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            elif self.ui.radioButton_y.isChecked():
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
                self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
            elif self.ui.radioButton_z.isChecked():
                self.ui.LineEdit_end_z.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
        else:
            pass


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
        try:
            ParticlesList = ["ALL", "ELECTRON", "PROTON"]
            ParticlesTypeList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.NewParticle)
            for i in ParticlesTypeList:
                if i not in ParticlesList:
                    self.ui.cb_particles4.addItem(i)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())
