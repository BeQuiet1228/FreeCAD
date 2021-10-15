# -*- coding: utf-8 -*-
import traceback
import PhasSpaceDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D, ObjectTools


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = PhasSpaceDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        try:
            self.default_timer_list = ["TSYS$FIRST", "TSYS$LAST", "TSYS$EIGEN", "TSYS$EDGEMODE", "TSYS$ENERGY"]
            self.initParticles()
            self.initHorizon()
            self.initVertical()
            self.initThick()
            self.initTimer()
            self.ui.checkBox_thick.stateChanged.connect(self.isThick)
            self.ui.checkBox_suffix.stateChanged.connect(self.isSuffix)
            self.ui.ComboBox_thick.setEnabled(False)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            self.ui.le_name.setText(self.obj.Label)

            itemIndex1 = self.ui.ComboBox_Observation_particle.findText(str(self.obj.observationParticle))
            self.ui.ComboBox_Observation_particle.setCurrentIndex(itemIndex1)

            itemIndex2 = self.ui.ComboBox_timer.findText(str(self.obj.timer))
            self.ui.ComboBox_timer.setCurrentIndex(itemIndex2)

            itemIndex3 = self.ui.ComboBox_Horizon.findText(str(self.obj.horizontalAxisShow))
            self.ui.ComboBox_Horizon.setCurrentIndex(itemIndex3)

            itemIndex4 = self.ui.ComboBox_Vertical.findText(str(self.obj.verticalAxisShow))
            self.ui.ComboBox_Vertical.setCurrentIndex(itemIndex4)

            self.ui.checkBox_thick.setChecked(self.obj.isShowThickness)
            itemIndex5 = self.ui.ComboBox_thick.findText(str(self.obj.showThick))
            self.ui.ComboBox_thick.setCurrentIndex(itemIndex5)
            self.ui.le_thick1.setText(self.obj.thickValue1)
            self.ui.le_thick2.setText(self.obj.thickValue2)

            self.ui.checkBox_suffix.setChecked(self.obj.isSuffix)
            self.ui.le_phase.setText(self.obj.suffix)

        except AttributeError:
            Tools3D.sayz("PhasSpace--异常--在读取Object属性时出现异常")
            Tools3D.sayz(traceback.format_exc())
        except Exception as e:
            Tools3D.sayz("PhasSpace--" + str(e))
        else:
            Tools3D.sayz("PhasSpace--成功--读取Object信息")

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        try:
            # Tools3D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.Label = Tools3D.setLabel(self.ui.le_name.text())
            self.obj.observationParticle = self.ui.ComboBox_Observation_particle.currentText()
            self.obj.timer = self.ui.ComboBox_timer.currentText()
            self.obj.horizontalAxisShow = self.ui.ComboBox_Horizon.currentText()
            self.obj.verticalAxisShow = self.ui.ComboBox_Vertical.currentText()
            self.obj.isShowThickness = self.ui.checkBox_thick.isChecked()
            self.obj.showThick = self.ui.ComboBox_thick.currentText()
            self.obj.thickValue1 = self.ui.le_thick1.text()
            self.obj.thickValue2 = self.ui.le_thick2.text()
            self.obj.isSuffix = self.ui.checkBox_suffix.isChecked()
            self.obj.suffix = self.ui.le_phase.text()

        except:
            Tools3D.sayz("error:" + traceback.format_exc())
        pass

    def initHorizon(self):
        horizon_list = ["X1", "X2", "X3", "P1", "P2", "P3", "KE", "FX", "XR", "YR", "EPSX", "EPSY"]
        for i in range(0, len(horizon_list)):
            self.ui.ComboBox_Horizon.addItem(horizon_list[i])

    def initVertical(self):
        vertical_list = ["X1", "X2", "X3", "P1", "P2", "P3", "KE", "FX", "XR", "YR", "EPSX", "EPSY"]
        for i in range(0, len(vertical_list)):
            self.ui.ComboBox_Vertical.addItem(vertical_list[i])

    def initThick(self):
        thick_list = ["X1", "X2", "X3"]
        for i in range(0, len(thick_list)):
            self.ui.ComboBox_thick.addItem(thick_list[i])

    def initTimer(self):
        try:
            Timer_list = []
            for i in self.default_timer_list:
                self.ui.ComboBox_timer.addItem(i)
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

    def isThick(self):
        self.ui.ComboBox_thick.setEnabled(self.ui.checkBox_thick.isChecked())
        self.ui.le_thick1.setEnabled(self.ui.checkBox_thick.isChecked())
        self.ui.le_thick2.setEnabled(self.ui.checkBox_thick.isChecked())

    def isSuffix(self):
        self.ui.le_phase.setEnabled(self.ui.checkBox_suffix.isChecked())

    def initParticles(self):
        try:
            ParticlesList = [u"全部", u"电子", u"质子"]
            ParticlesTypeList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.NewParticle)
            for i in ParticlesTypeList:
                if i not in ParticlesList:
                    self.ui.ComboBox_Observation_particle.addItem(i)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())
