# -*- coding: utf-8 -*-
import traceback
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import MacroParticleDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = MacroParticleDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        self.refrsehCombox()

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.typeComboBox.setCurrentIndex(self.ui.typeComboBox.findText(self.obj.particleType))
            self.ui.LineEdit_every.setText(self.obj.every)
            self.ui.LineEdit_max.setText(self.obj.max)
        except:
            Tools3D.sayz("MacroParticle加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.particleType = self.ui.typeComboBox.currentText()
            self.obj.every = self.ui.LineEdit_every.text().replace(" ", "")
            self.obj.max = self.ui.LineEdit_max.text().replace(" ", "")
        except:
            Tools3D.sayz("MacroParticle加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def refrsehCombox(self):
        """
        刷新下拉框
        """
        comboBox_Particle_list = []
        for i in range(self.ui.typeComboBox.count()):
            comboBox_Particle_list.append(self.ui.typeComboBox.itemText(i))
        ParticleList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.NewParticle)
        for i in ParticleList:
            if i not in comboBox_Particle_list:
                self.ui.typeComboBox.addItem(i)
