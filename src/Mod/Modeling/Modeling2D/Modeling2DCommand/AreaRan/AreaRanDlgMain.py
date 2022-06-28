# -*- coding: utf-8 -*-
import traceback

import AreaRanDialog
import AreaRanInstance
from PySide import QtGui
import FreeCAD

from Modeling.Modeling2D.Modeling2DCommand.BaseUI import BaseDialog
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI
from Modeling.Modeling2D.Tools.Tools2D import sayz


class ShowDialog(BaseDialog.BaseOtherDialog):
    def __init__(self, obj, isNew=False, parent=None):
        self.obj = obj
        if not hasattr(self.obj, "isParticle"):
            AreaRanInstance.completionProperties(self.obj)
        BaseDialog.BaseOtherDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        """
        设置ui
        """
        self.ui = AreaRanDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(False)

    def helperInitDialog(self):
        """
        初始化界面，设置界面逻辑，绑定信号与槽
        """
        # if not hasattr(self.obj, "isParticle"):
        #     AreaRanInstance.completionProperties(self.obj)
        self.defaultValue = ["OSYS$MIDLINE1", "OSYS$MIDLINE2", "OSYS$MIDLINE3"]
        # 列表的初始化
        self.initObservationField()
        self.initChooseParticle()
        self.initParticleType()
        self.initParticleAxis()
        self.initTimer()
        # 此处按钮命名需要修改
        self.ui.radioButton_x.toggled.connect(self.setRadioButton)
        self.ui.radioButton_y.toggled.connect(self.setRadioButton)

        self.ui.radioButton_field.toggled.connect(self.sortingItem)
        self.ui.radioButton_integral.toggled.connect(self.sortingItem)
        self.ui.radioButton_power.toggled.connect(self.sortingItem)
        self.ui.radioButton_energy.toggled.connect(self.sortingItem)
        self.ui.radioButton_particles.toggled.connect(self.sortingItem)

        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.slotComboBoxShadow)

        self.ui.checkBox_Fourier.stateChanged.connect(self.checkBoxFourier)

        self.ui.le_start_x.textChanged.connect(self.leStart)
        self.ui.le_start_y.textChanged.connect(self.leStart)

        self.initOrthogonalProjectionLine()

        self.loadData()
        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        # 根据坐标系初始化面板
        self.ui.label_X.setText(self.x)
        self.ui.label_Y.setText(self.y)
        self.ui.radioButton_x.setText(self.x)
        self.ui.radioButton_y.setText(self.y)

    def helperOK(self):
        self.isKeepData = True
        self.close()

    def helperCancel(self):
        self.isKeepData = False
        self.close()

    def loadData(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        self.ui.le_name.setText(self.obj.Label)
        itemIndex = self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionLine))
        self.ui.ComboBox_Shadow.setCurrentIndex(itemIndex)

        self.ui.le_start_x.setText(self.obj.point1_X)
        self.ui.le_start_y.setText(self.obj.point1_Y)
        itemIndex1 = self.ui.ComboBox_start.findText(str(self.obj.point1_name))
        self.ui.ComboBox_start.setCurrentIndex(itemIndex1)

        self.ui.le_end_x.setText(self.obj.point2_X)
        self.ui.le_end_y.setText(self.obj.point2_Y)
        itemIndex2 = self.ui.ComboBox_end.findText(str(self.obj.point2_name))
        self.ui.ComboBox_end.setCurrentIndex(itemIndex2)

        self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
        self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)

        self.ui.radioButton_field.setChecked(self.obj.isField)
        self.ui.radioButton_integral.setChecked(self.obj.isFieldIntegral)
        self.ui.radioButton_power.setChecked(self.obj.isFieldPower)
        self.ui.radioButton_energy.setChecked(self.obj.isFieldEnergy)
        self.ui.radioButton_particles.setChecked(self.obj.isParticle)

        itemIndex3 = self.ui.ComboBox_E1.findText(str(self.obj.field))
        self.ui.ComboBox_E1.setCurrentIndex(itemIndex3)

        itemIndex4 = self.ui.ComboBox_EDL.findText(str(self.obj.fieldIntegral))
        self.ui.ComboBox_E1.setCurrentIndex(itemIndex4)

        itemIndex5 = self.ui.ComboBox_SDA.findText(str(self.obj.fieldPower))
        self.ui.ComboBox_SDA.setCurrentIndex(itemIndex5)

        itemIndex6 = self.ui.ComboBox_EM.findText(str(self.obj.fieldEnergy))
        self.ui.ComboBox_EM.setCurrentIndex(itemIndex6)

        self.ui.comboBox_particle.setCurrentIndex(self.ui.comboBox_particle.findText(str(self.obj.chooseParticle)))
        self.ui.comboBox_particleType.setCurrentIndex(self.ui.comboBox_particleType.findText(str(self.obj.particleType)))
        self.ui.comboBox_axis.setCurrentIndex(self.ui.comboBox_axis.findText(str(self.obj.particleAxis)))

        self.ui.checkBox_Fourier.setChecked(self.obj.isFFT)
        self.ui.radioButton_real.setChecked(self.obj.isRealAnalysis)
        self.ui.radioButton_complex.setChecked(self.obj.isComplexAnalysis)

        itemIndex7 = self.ui.ComboBox_timer.findText(str(self.obj.timer))
        self.ui.ComboBox_timer.setCurrentIndex(itemIndex7)

    def keepData(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        # noinspection PyBroadException
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.orthogonalProjectionLine = self.ui.ComboBox_Shadow.currentText()
            # 坐标
            self.obj.point1_name = self.ui.ComboBox_start.currentText()
            self.obj.point1_X = self.ui.le_start_x.text()
            self.obj.point1_Y = self.ui.le_start_y.text()

            self.obj.point2_name = self.ui.ComboBox_end.currentText()
            self.obj.point2_X = self.ui.le_end_x.text()
            self.obj.point2_Y = self.ui.le_end_y.text()

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
            import traceback
            sayz("error:" + traceback.format_exc())

    def initOrthogonalProjectionLine(self):
        """
        初始化空间观测线的下拉框
        """
        line_list = self.defaultValue
        line_list = line_list + Tools2D.getLabelsByType(Tools2D.ObjectType.LineConformal)
        for i in line_list:
            self.ui.ComboBox_Shadow.addItem(i)

    def slotComboBoxShadow(self):
        # noinspection PyBroadException
        try:
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.ui.le_start_x.setEnabled(True)
                self.ui.le_start_y.setEnabled(True)
                self.ui.le_end_x.setEnabled(True)
                self.ui.le_end_y.setEnabled(True)
                self.ui.radioButton_x.setEnabled(True)
                self.ui.radioButton_y.setEnabled(True)
                self.setRadioButton()
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                    self.ui.le_start_x.setText(modelData["point1.x"])
                    self.ui.le_start_y.setText(modelData["point1.y"])
                    self.ui.le_end_x.setText(modelData["point2.x"])
                    self.ui.le_end_y.setText(modelData["point2.y"])
                    # 法向
                    if modelData["normal"] == "X" or modelData["normal"] == "x":
                        self.ui.radioButton_x.setChecked(True)
                    elif modelData["normal"] == "Y" or modelData["normal"] == "y":
                        self.ui.radioButton_y.setChecked(True)
                    else:
                        Tools2D.sayz("设置AreaRan法向时出现错误")
                self.ui.le_start_x.setEnabled(False)
                self.ui.le_start_y.setEnabled(False)
                self.ui.le_end_x.setEnabled(False)
                self.ui.le_end_y.setEnabled(False)
                self.ui.radioButton_x.setEnabled(False)
                self.ui.radioButton_y.setEnabled(False)
        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def initObservationField(self):
        field_list = ["E1",
                      "E2",
                      "E3",
                      "B1",
                      "B2",
                      "B3",
                      "J1",
                      "J2",
                      "J3",
                      "Q0",
                      "E1AV",
                      "E2AV",
                      "E3AV",
                      "B1AV",
                      "B2AV",
                      "B3AV",
                      "E1ST",
                      "E2ST",
                      "E3ST",
                      "B1ST",
                      "B2ST",
                      "B3ST",
                      "PHST",
                      "B",
                      "E",
                      ]
        for i in range(0, len(field_list)):
            self.ui.ComboBox_E1.addItem(field_list[i])

    def initTimer(self):
        try:
            Timer_list = []
            for i in range(self.ui.ComboBox_timer.count()):
                Timer_list.append(self.ui.ComboBox_timer.itemText(i))
            volumeList = Tools2D.getLabelsByType(Tools2D.ObjectType.Timer)
            for i in volumeList:
                if i not in Timer_list:
                    self.ui.ComboBox_timer.addItem(i)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def setRadioButton(self):
        if self.ui.radioButton_x.isChecked():
            self.ui.le_end_x.setEnabled(False)
            self.ui.le_end_y.setEnabled(True)
            self.ui.le_end_x.setText(self.ui.le_start_x.text())
        else:
            self.ui.le_end_x.setEnabled(True)
            self.ui.le_end_y.setEnabled(False)
            self.ui.le_end_y.setText(self.ui.le_start_y.text())

    def leStart(self):
        if self.ui.radioButton_x.isChecked():
            self.ui.le_end_x.setText(self.ui.le_start_x.text())
        else:
            self.ui.le_end_y.setText(self.ui.le_start_y.text())

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
