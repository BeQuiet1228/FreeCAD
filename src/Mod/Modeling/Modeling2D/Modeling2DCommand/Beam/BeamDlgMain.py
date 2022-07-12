# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import BeamDialog
import FreeCAD


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = BeamDialog.Ui_Dialog_EmbDlg()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.loadData()
        self.getInfoFromObj()

    def loadData(self):
        # 可以做个封装
        self.ui.checkBox_particleType.clicked.connect(self.checkBox_particleType_clicked)
        self.ui.checkBox_generationRate.clicked.connect(self.checkBox_generationRate_clicked)
        self.ui.checkBox_transmittingInterval.clicked.connect(self.checkBox_transmittingInterval_clicked)
        self.ui.checkBox_surface.clicked.connect(self.checkBox_surface_clicked)
        self.ui.checkBox_outSurface.clicked.connect(self.checkBox_outSurface_clicked)

        self.ui.pb_ok.clicked.connect(self.pb_ok_clicked)
        self.ui.pb_cancel.clicked.connect(self.pb_cancel_clicked)

    def getInfoFromObj(self):
        self.ui.LineEdit_Name.setText(self.obj.Label)
        # 动态的添加下拉框，做个标记回头改,发射体
        # self.ui.ComboBox_Shadow.addItems(self.obj.emitter)
        self.ui.textEdit_BeamJ.setText(self.obj.beamCurrentDensity)
        self.ui.textEdit_BeamV.setText(self.obj.beamVoltageDensity)
        self.ui.checkBox_particleType.setChecked(self.obj.isParticleType)
        # 下拉框动态显示,粒子类型
        # self.ui.ComboBox_particleType.addItems(self.obj.particleType)
        self.ui.checkBox_generationRate.setChecked(self.obj.isGenerationRate)
        self.ui.spinBox_generationRate.setValue(self.obj.generationRate)
        self.ui.checkBox_transmittingInterval.setChecked(self.obj.isFiringInterval)
        self.ui.radioButton_random.setChecked(self.obj.isRandomDistribution)
        self.ui.radioButton_strictTiming.setChecked(self.obj.isStrictTiming)
        self.ui.spinBox_timesStep.setValue(self.obj.firingInterval)
        self.ui.checkBox_surface.setChecked(self.obj.isSurfaceDistribution)
        self.ui.radioButton_randomm.setChecked(self.obj.isRandom1)
        self.ui.radioButton_uniform.setChecked(self.obj.isBalance1)
        self.ui.radioButton_fixed.setChecked(self.obj.isImmobilization1)
        self.ui.checkBox_outSurface.setChecked(self.obj.isOuterSurfaceDistribution)
        self.ui.radioButton_randommm.setChecked(self.obj.isRandom2)
        self.ui.radioButton_alongOutsideFixed.setChecked(self.obj.isImmobilization2)
        self.ui.LineEdit_Dn.setText(self.obj.excursion)
        # 动态刷新下拉框,发射区域选项
        # self.ui.ComboBox_included.addItems(self.obj.launchArea1)
        # self.ui.ComboBox_includedd.addItems(self.obj.launchArea2)
        # self.ui.ComboBox_notInclued.addItems(self.obj.launchOrthogonalProjectionRegin1)
        # self.ui.ComboBox_notIncludedd.addItems(self.obj.launchOrthogonalProjectionRegin2)


    def checkBox_particleType_clicked(self):
        self.ui.ComboBox_particleType.setEnabled(self.ui.checkBox_particleType.isChecked())

    def checkBox_generationRate_clicked(self):
        self.ui.spinBox_generationRate.setEnabled(self.ui.checkBox_generationRate.isChecked())

    def checkBox_transmittingInterval_clicked(self):
        self.ui.radioButton_random.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.radioButton_strictTiming.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.spinBox_timesStep.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())

    def checkBox_surface_clicked(self):
        self.ui.radioButton_randomm.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_uniform.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_fixed.setEnabled(self.ui.checkBox_surface.isChecked())

    def checkBox_outSurface_clicked(self):
        self.ui.radioButton_randommm.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.radioButton_alongOutsideFixed.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.LineEdit_Dn.setEnabled(self.ui.checkBox_outSurface.isChecked())

    def pb_ok_clicked(self):
        self.keepData()
        self.close()

    def pb_cancel_clicked(self):
        self.close()
        if self.isNew:
            FreeCAD.ActiveDocument.removeObject(self.obj.Label)

    def keepData(self):
        self.obj.Label = self.ui.LineEdit_Name.text()
        self.obj.emitter = self.ui.ComboBox_Shadow.currentText()
        self.obj.beamCurrentDensity = self.ui.textEdit_BeamJ.toPlainText()
        self.obj.beamVoltageDensity = self.ui.textEdit_BeamV.toPlainText()
        self.obj.isParticleType = self.ui.checkBox_particleType.isChecked()
        self.obj.particleType = self.ui.ComboBox_particleType.currentText()
        self.obj.isGenerationRate = self.ui.checkBox_generationRate.isChecked()
        self.obj.generationRate = self.ui.spinBox_generationRate.value()
        self.obj.isFiringInterval = self.ui.checkBox_transmittingInterval.isChecked()
        self.obj.isRandomDistribution = self.ui.radioButton_random.isChecked()
        self.obj.isStrictTiming = self.ui.radioButton_strictTiming.isChecked()
        self.obj.firingInterval = self.ui.spinBox_timesStep.value()
        self.obj.isSurfaceDistribution = self.ui.checkBox_surface.isChecked()
        self.obj.isRandom1 = self.ui.radioButton_randomm.isChecked()
        self.obj.isBalance1 = self.ui.radioButton_uniform.isChecked()
        self.obj.isImmobilization1 = self.ui.radioButton_fixed.isChecked()
        self.obj.isOuterSurfaceDistribution = self.ui.checkBox_outSurface.isChecked()
        self.obj.isRandom2 = self.ui.radioButton_randommm.isChecked()
        self.obj.isImmobilization2 = self.ui.radioButton_alongOutsideFixed.isChecked()
        self.obj.excursion = self.ui.LineEdit_Dn.text()
        self.obj.launchArea1 = self.ui.ComboBox_notInclued.currentText()
        self.obj.launchArea2 = self.ui.ComboBox_notIncludedd.currentText()
        self.obj.launchOrthogonalProjectionRegin1 = self.ui.ComboBox_included.currentText()
        self.obj.launchOrthogonalProjectionRegin2 = self.ui.ComboBox_includedd.currentText()






