# -*- coding: utf-8 -*-
from PySide import QtGui
import FreeCAD
import FreeCADGui
from Modeling.Modeling2D.Modeling2DCommand.MacroParticle import MacroParticleDialog
from Modeling.Modeling2D.Tools import ToolsUI, Tools2D


def getNewParticle():
    NewParticle_list = Tools2D.getSpecificTypePhyAndProObjects(u"ParticleDefine")
    NewParticleName_list = []
    for ele in NewParticle_list:
        NewParticleName_list.append(ele.Label)
    return NewParticleName_list


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = MacroParticleDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.obj = obj
        self.isNew = isNew
        self.isKeepData = False
        self.initDialog()
        self.loadData()

    def initDialog(self):
        # 刷新下拉框
        self.refrsehCombox()
        self.ui.checkBox.stateChanged.connect(self.comboBox_clicked)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)
        self.ui.pb_ok.clicked.connect(self.slotOK)
        ToolsUI.setResolution(self)

    def comboBox_clicked(self):
        self.ui.comboBox.setEnabled(self.ui.checkBox.isChecked())
        self.ui.lineEdit_every.setEnabled(self.ui.checkBox.isChecked())
        self.ui.lineEdit_max.setEnabled(self.ui.checkBox.isChecked())

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def slotOK(self):
        self.isKeepData = True
        self.close()

    def loadData(self):
        self.ui.checkBox.setChecked(self.obj.isMacroParticle)
        self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(self.obj.typeOfParticles))
        self.ui.lineEdit_every.setText(self.obj.particleNumber)
        self.ui.lineEdit_max.setText(self.obj.macroParticleNumber)

    def keepData(self):
        self.obj.isMacroParticle = self.ui.checkBox.isChecked()
        self.obj.typeOfParticles = self.ui.comboBox.currentText()
        self.obj.particleNumber = self.ui.lineEdit_every.text()
        self.obj.macroParticleNumber = self.ui.lineEdit_max.text()

    def refrsehCombox(self):
        comboBox_Particle_list = []
        for i in range(self.ui.comboBox.count()):
            comboBox_Particle_list.append(self.ui.comboBox.itemText(i))
        particleList = getNewParticle()
        for i in particleList:
            if i not in comboBox_Particle_list:
                self.ui.comboBox.addItem(i)

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
