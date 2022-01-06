# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import SecdDialog
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = SecdDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj
        self.initDialog()
        self.loadData()

    def initDialog(self):
        try:
            self.ui.checkBox_weightCoefficient.clicked.connect(self.checkBox_weightCoefficient_clicked)
            self.ui.checkBox_energyDistribution.clicked.connect(self.checkBox_energyDistribution_clicked)
            self.ui.checkBox_angularDistribution.clicked.connect(self.checkBox_angularDistribution_clicked)
            self.ui.pb_ok.clicked.connect(self.pb_ok_clicked)
            self.ui.pb_cancel.clicked.connect(self.pb_cancel_clicked)
            Tools2D.EmissionUiData(self.obj, self.ui)

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def checkBox_weightCoefficient_clicked(self):
        self.ui.lineEdit_WF.setEnabled(self.ui.checkBox_weightCoefficient.isChecked())

    def checkBox_energyDistribution_clicked(self):
        self.ui.lineEdit_ED.setEnabled(self.ui.checkBox_energyDistribution.isChecked())
        self.ui.lineEdit_energyMin.setEnabled(self.ui.checkBox_energyDistribution.isChecked())
        self.ui.lineEdit_energyMax.setEnabled(self.ui.checkBox_energyDistribution.isChecked())

    def checkBox_angularDistribution_clicked(self):
        self.ui.lineEdit_AD.setEnabled(self.ui.checkBox_energyDistribution.isChecked())

    def pb_ok_clicked(self):
        self.keepData()
        self.close()

    def pb_cancel_clicked(self):
        self.close()

    def loadData(self):
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
            Tools2D.EmissionUiData(self.obj, self.ui).loadDataFromObj()

        except KeyError as reason:
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def keepData(self):
        try:
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
            Tools2D.EmissionUiData(self.obj, self.ui).getDataFromUi()

        except KeyError as reason:
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))
        pass
