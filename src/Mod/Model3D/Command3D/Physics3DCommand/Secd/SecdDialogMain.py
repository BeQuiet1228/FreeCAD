# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import SecdDialog
import traceback


class ShowDialog(BaseDialogMain.BaseEmitDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BaseEmitDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = SecdDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def privateDialog(self):
        try:
            self.ui.checkBox_weightCoefficient.clicked.connect(self.checkBox_weightCoefficient_clicked)
            self.ui.checkBox_energyDistribution.clicked.connect(self.checkBox_energyDistribution_clicked)
            self.ui.checkBox_angularDistribution.clicked.connect(self.checkBox_angularDistribution_clicked)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def checkBox_weightCoefficient_clicked(self):
        self.ui.lineEdit_WF.setEnabled(self.ui.checkBox_weightCoefficient.isChecked())

    def checkBox_energyDistribution_clicked(self):
        self.ui.lineEdit_ED.setEnabled(self.ui.checkBox_energyDistribution.isChecked())
        self.ui.lineEdit_energyMin.setEnabled(self.ui.checkBox_energyDistribution.isChecked())
        self.ui.lineEdit_energyMax.setEnabled(self.ui.checkBox_energyDistribution.isChecked())

    def checkBox_angularDistribution_clicked(self):
        self.ui.lineEdit_AD.setEnabled(self.ui.checkBox_energyDistribution.isChecked())

    def loadPrivateData(self):
        try:
            self.ui.lineEdit_maxNum.setText(self.obj.maximumEmissionFactor)
            self.ui.lineEdit_energy.setText(self.obj.maximumEmissionFactorEnergy)
            self.ui.checkBox_weightCoefficient.setChecked(self.obj.isWeightCoefficient)
            self.ui.lineEdit_WF.setText(self.obj.weightCoefficient)
            self.ui.checkBox_energyDistribution.setChecked(self.obj.isEnergyDistribution)
            self.ui.lineEdit_ED.setText(self.obj.energyDistribution)
            self.ui.lineEdit_energyMin.setText(self.obj.minimumEnergy)
            self.ui.lineEdit_energyMax.setText(self.obj.maximumEnergy)
            self.ui.checkBox_angularDistribution.setChecked(self.obj.isAngularDistribution)
            self.ui.lineEdit_AD.setText(self.obj.angularDistribution)
            # 设置文本框状态
            self.checkBox_weightCoefficient_clicked()
            self.checkBox_energyDistribution_clicked()
            self.checkBox_angularDistribution_clicked()
        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setPrivateInfoToObj(self):
        self.obj.maximumEmissionFactor = self.ui.lineEdit_maxNum.text()
        self.obj.maximumEmissionFactorEnergy = self.ui.lineEdit_energy.text()
        self.obj.isWeightCoefficient = self.ui.checkBox_weightCoefficient.isChecked()
        self.obj.weightCoefficient = self.ui.lineEdit_WF.text()
        self.obj.isEnergyDistribution = self.ui.checkBox_energyDistribution.isChecked()
        self.obj.energyDistribution = self.ui.lineEdit_ED.text()
        self.obj.minimumEnergy = self.ui.lineEdit_energyMin.text()
        self.obj.maximumEnergy = self.ui.lineEdit_energyMax.text()
        self.obj.isAngularDistribution = self.ui.checkBox_angularDistribution.isChecked()
        self.obj.angularDistribution = self.ui.lineEdit_AD.text()