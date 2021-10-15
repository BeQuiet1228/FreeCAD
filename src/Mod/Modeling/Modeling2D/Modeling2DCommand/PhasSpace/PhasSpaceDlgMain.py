# -*- coding: utf-8 -*-
import traceback

import PhasSpaceDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui
from Modeling.Modeling2D.Tools import Tools2D, ToolsUI
from Modeling.Modeling2D.Tools.Tools2D import sayz


def getNewParticle():
    NewParticle_list = Tools2D.getSpecificTypePhyAndProObjects(u"ParticleDefine")
    NewParticleName_list = []
    for ele in NewParticle_list:
        NewParticleName_list.append(ele.Label)
    return NewParticleName_list


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = PhasSpaceDialog.Ui_Dialog()
        self.ui.setupUi(self)

        # 暂时写在这里
        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.getInfoFromObj()
        self.isKeepData = False

    def initDialog(self):
        """
        初始化界面，设置界面逻辑，绑定信号与槽
        """
        # 初始化粒子种类下拉框
        self.initParticles()
        # 列表的初始化
        self.initHorizon()
        self.initVertical()
        self.initThick()
        self.initTimer()
        # 此处按钮命名需要修改
        self.ui.checkBox_thick.stateChanged.connect(self.isThick)
        self.ui.checkBox_suffix.stateChanged.connect(self.isSuffix)
        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)
        self.ui.ComboBox_thick.setEnabled(False)
        # 观测粒子默认全部，其他不可选。
        # self.ui.ComboBox_Observation_particle.setEnabled(False)
        # order发生变化时所触发的函数

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
            itemIndex4 = self.ui.ComboBox_thick.findText(str(self.obj.showThick))
            self.ui.ComboBox_thick.setCurrentIndex(itemIndex4)
            self.ui.le_thick1.setText(self.obj.thickValue1)
            self.ui.le_thick2.setText(self.obj.thickValue2)

            self.ui.checkBox_suffix.setChecked(self.obj.isSuffix)
            self.ui.le_phase.setText(self.obj.suffix)

        except AttributeError:
            Tools2D.sayz("Circular--异常--在读取Object属性时出现异常")
            Tools2D.sayz(traceback.format_exc())
        except Exception as e:
            Tools2D.sayz("Circular--" + str(e))
        else:
            Tools2D.sayz("Circular--成功--读取Object信息")

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        try:
            Tools2D.setLabelToObj(self.obj, self.ui.le_name.text())
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

            pass
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def slotOK(self):
        """
        确定按钮绑定的槽函数
        """
        self.isKeepData = True
        self.close()

    def slotCancel(self):
        """
        取消按钮绑定的槽函数
        """
        self.isKeepData = False
        self.close()

    def initHorizon(self):
        list = ["X1",
                "X2",
                "P1",
                "P2",
                "P3",
                "KE",
                "FX",
                "XR",
                "YR",
                "EPSX",
                "EPSY",
                ]
        for i in range(0, len(list)):
            self.ui.ComboBox_Horizon.addItem(list[i])

    def initVertical(self):
        list = ["X1",
                "X2",
                "P1",
                "P2",
                "P3",
                "KE",
                "FX",
                "XR",
                "YR",
                "EPSX",
                "EPSY",
                ]
        for i in range(0, len(list)):
            self.ui.ComboBox_Vertical.addItem(list[i])

    def initThick(self):
        list=["X1", "X2"]
        for i in list:
            self.ui.ComboBox_thick.addItem(i)

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

    def isThick(self):
        self.ui.ComboBox_thick.setEnabled(self.ui.checkBox_thick.isChecked())
        self.ui.le_thick1.setEnabled(self.ui.checkBox_thick.isChecked())
        self.ui.le_thick2.setEnabled(self.ui.checkBox_thick.isChecked())
        pass

    def isSuffix(self):
        self.ui.le_phase.setEnabled(self.ui.checkBox_suffix.isChecked())
        pass

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            try:
                self.setInfoToObj()
                FreeCADGui.runCommand("CreateM2D")
            except AttributeError:
                Tools2D.sayz("PhasSpace--异常--在读取Object属性时出现异常")
                Tools2D.sayz(traceback.format_exc())
            except Exception as e:
                Tools2D.sayz("PhasSpace--" + str(e))
            else:
                Tools2D.sayz("PhasSpace--成功--设置Object信息")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

    def initParticles(self):
        ParticlesList = [u"全部", u"电子", u"质子"]
        ParticlesTypeList = getNewParticle()
        # for i in ParticlesList:
        #     self.ui.ComboBox_Observation_particle.addItem(i)
        for i in ParticlesTypeList:
            if i not in ParticlesList:
                self.ui.ComboBox_Observation_particle.addItem(i)
