# -*- coding: utf-8 -*-
import traceback
import AreaRanDialog
import AreaRanInstance
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D, ObjectTools


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = AreaRanDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        try:
            self.default_list = ["OSYS$MIDLINE1", "OSYS$MIDLINE2", "OSYS$MIDLINE3"]
            self.initChooseParticle()
            self.initParticleType()
            self.initParticleAxis()

            self.initTimer()
            self.refreshCombox()
            self.initObservationField()
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)

            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
            self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

            self.ui.radioButton_x.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_z.clicked.connect(self.radioButton_clicked)

            self.ui.radioButton_field.toggled.connect(self.sortingItem)
            self.ui.radioButton_integral.toggled.connect(self.sortingItem)
            self.ui.radioButton_power.toggled.connect(self.sortingItem)
            self.ui.radioButton_energy.toggled.connect(self.sortingItem)
            self.ui.radioButton_particles.toggled.connect(self.sortingItem)

            self.ui.checkBox_Fourier.stateChanged.connect(self.checkBoxFourier)

            # 根据坐标系初始化面板
            Tools3D.switchPointLabel(self.ui)
            Tools3D.switchRadioButtonLabel(self.ui)

        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            self.ui.le_name.setText(self.obj.Label)
            Tools3D.setCoorToUI(self.ui, self.obj)
            Tools3D.setRadioButtonToUI(self.ui, self.obj)

            itemIndex = self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionLine))
            self.ui.ComboBox_Shadow.setCurrentIndex(itemIndex)

            itemIndex1 = self.ui.ComboBox_start.findText(str(self.obj.point1_name))
            self.ui.ComboBox_start.setCurrentIndex(itemIndex1)

            itemIndex2 = self.ui.ComboBox_end.findText(str(self.obj.point2_name))
            self.ui.ComboBox_end.setCurrentIndex(itemIndex2)

            self.ui.radioButton_field.setChecked(self.obj.isField)
            self.ui.radioButton_integral.setChecked(self.obj.isFieldIntegral)
            self.ui.radioButton_power.setChecked(self.obj.isFieldPower)
            self.ui.radioButton_energy.setChecked(self.obj.isFieldEnergy)

            self.ui.radioButton_particles.setChecked(self.obj.isParticle)

            itemIndex3 = self.ui.ComboBox_E1.findText(str(self.obj.field))
            self.ui.ComboBox_E1.setCurrentIndex(itemIndex3)

            itemIndex4 = self.ui.ComboBox_EDL.findText(str(self.obj.fieldIntegral))
            self.ui.ComboBox_EDL.setCurrentIndex(itemIndex4)

            itemIndex5 = self.ui.ComboBox_SDA.findText(str(self.obj.fieldPower))
            self.ui.ComboBox_SDA.setCurrentIndex(itemIndex5)

            itemIndex6 = self.ui.ComboBox_EM.findText(str(self.obj.fieldEnergy))
            self.ui.ComboBox_EM.setCurrentIndex(itemIndex6)

            self.ui.comboBox_particle.setCurrentIndex(self.ui.comboBox_particle.findText(str(self.obj.chooseParticle)))
            self.ui.comboBox_particleType.setCurrentIndex(
                self.ui.comboBox_particleType.findText(str(self.obj.particleType)))
            self.ui.comboBox_axis.setCurrentIndex(self.ui.comboBox_axis.findText(str(self.obj.particleAxis)))

            self.ui.checkBox_Fourier.setChecked(self.obj.isFFT)
            self.ui.radioButton_real.setChecked(self.obj.isRealAnalysis)
            self.ui.radioButton_complex.setChecked(self.obj.isComplexAnalysis)

            itemIndex7 = self.ui.ComboBox_timer.findText(str(self.obj.timer))
            self.ui.ComboBox_timer.setCurrentIndex(itemIndex7)
            self.ComboBox_Shadow_clicked()
            # 仅当“未指定”时，初始化界面时，模拟一次点击，以开启或关闭对应point_end三个坐标的enabled状态
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.radioButton_clicked()

        except AttributeError:
            Tools3D.sayz("AreaRan--异常--在读取Object属性时出现异常")
            Tools3D.sayz(traceback.format_exc())
        except Exception as e:
            Tools3D.sayz("AreaRan--" + str(e))
        else:
            Tools3D.sayz("AreaRan--成功--读取Object信息")

    def setInfoToObj(self):
        try:
            # Tools3D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.Label = Tools3D.setLabel(self.ui.le_name.text())
            Tools3D.getUICoordinate(self.obj, self.ui)
            Tools3D.getUIRadioButton(self.obj, self.ui)

            self.obj.orthogonalProjectionLine = self.ui.ComboBox_Shadow.currentText()

            self.obj.point1_name = self.ui.ComboBox_start.currentText()
            self.obj.point2_name = self.ui.ComboBox_end.currentText()

            self.obj.isField = self.ui.radioButton_field.isChecked()
            self.obj.isFieldIntegral = self.ui.radioButton_integral.isChecked()
            self.obj.isFieldPower = self.ui.radioButton_power.isChecked()
            self.obj.isFieldEnergy = self.ui.radioButton_energy.isChecked()
            self.obj.isParticle = self.ui.radioButton_particles.isChecked()

            self.obj.field = self.ui.ComboBox_E1.currentText()
            self.obj.fieldIntegral = self.ui.ComboBox_EDL.currentText()
            self.obj.fieldPower = self.ui.ComboBox_SDA.currentText()
            self.obj.fieldEnergy = self.ui.ComboBox_EM.currentText()

            self.obj.chooseParticle = self.ui.comboBox_particle.currentText()
            self.obj.particleType = self.ui.comboBox_particleType.currentText()
            self.obj.particleAxis = self.ui.comboBox_axis.currentText()

            self.obj.isFFT = self.ui.checkBox_Fourier.isChecked()
            self.obj.isRealAnalysis = self.ui.radioButton_real.isChecked()
            self.obj.isComplexAnalysis = self.ui.radioButton_complex.isChecked()

            self.obj.timer = self.ui.ComboBox_timer.currentText()
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        """
        初始化空间观测线的下拉框
        """
        try:
            ComboBox_Shadow_list = []
            for i in self.default_list:
                self.ui.ComboBox_Shadow.addItem(i)
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
            lineList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Line_Conformal)
            for i in lineList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def initObservationField(self):
        list = ["E1", "E2", "E3", "B1", "B2", "B3", "J1", "J2", "J3", "Q0",
                "E1AV", "E2AV", "E3AV", "B1AV", "B2AV", "B3AV", "E1ST", "E2ST",
                "E3ST", "B1ST", "B2ST", "B3ST", "PHST", "B", "E"]
        for i in range(0, len(list)):
            self.ui.ComboBox_E1.addItem(list[i])

    def initTimer(self):
        try:
            Timer_list = []
            for i in range(self.ui.ComboBox_timer.count()):
                Timer_list.append(self.ui.ComboBox_timer.itemText(i))
            # defTimerList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.DefaultTimer)
            timerList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.CustomTimer)
            # allTimerList = defTimerList + timerList
            for i in timerList:
                if i not in Timer_list:
                    self.ui.ComboBox_timer.addItem(i)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def sortingItem(self):
        self.ui.ComboBox_E1.setEnabled(self.ui.radioButton_field.isChecked())
        self.ui.ComboBox_EDL.setEnabled(self.ui.radioButton_integral.isChecked())
        self.ui.ComboBox_SDA.setEnabled(self.ui.radioButton_power.isChecked())
        self.ui.ComboBox_EM.setEnabled(self.ui.radioButton_energy.isChecked())
        self.ui.comboBox_particle.setEnabled(self.ui.radioButton_particles.isChecked())
        self.ui.comboBox_particleType.setEnabled(self.ui.radioButton_particles.isChecked())
        self.ui.comboBox_axis.setEnabled(self.ui.radioButton_particles.isChecked())
        # self.ui.checkBox_Fourier.setEnabled(not self.ui.radioButton_particles.isChecked())

    def checkBoxFourier(self):
        self.ui.radioButton_real.setEnabled(self.ui.checkBox_Fourier.isChecked())
        self.ui.radioButton_complex.setEnabled(self.ui.checkBox_Fourier.isChecked())

    def initChooseParticle(self):
        chooseParticle_list = ["CURRENT", "POWER", "ENERGY"]
        for i in chooseParticle_list:
            self.ui.comboBox_particle.addItem(i)

    def initParticleType(self):
        particleType_list = ["ELECTRON", "PROTON"]
        for i in particleType_list:
            self.ui.comboBox_particleType.addItem(i)

    def initParticleAxis(self):
        particleAxis = ["X1", "X2"]
        for i in particleAxis:
            self.ui.comboBox_axis.addItem(i)

    def ComboBox_Shadow_clicked(self):
        try:
            # 未选择
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Line_Conformal)
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.default_list:
                    Tools3D.setIsEdit(self.ui, False)
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                    Tools3D.setIsEdit(self.ui, False)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

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
        else:
            pass
