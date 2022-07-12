# -*- coding: utf-8 -*-
import traceback

import PopuDialog
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
        self.ui = PopuDialog.Ui_Dialog()
        self.ui.setupUi(self)

        # self.setModel(False)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.loadData()
        self.isKeepData = False

    def initDialog(self):
        """
        设置对话框的逻辑
        """
        # 初始化粒子种类下拉框
        self.initParticles()
        # 初始化正交投影面列表
        self.refreshCombox()
        self.ui.pb_ok.clicked.connect(self.pb_ok_clicked)
        self.ui.pb_cancel.clicked.connect(self.pb_cancel_clicked)
        # 获取当前坐标系及坐标系单位
        coord = Tools2D.getCoordinate()
        self.x = coord[0]
        self.y = coord[1]
        # 根据坐标系初始化面板
        self.ui.label_5.setText(self.x)
        self.ui.label_6.setText(self.y)

    def initParticles(self):
        ParticlesList = ["ALL", "ELECTRON", "PROTON"]
        ParticlesTypeList = getNewParticle()
        for i in ParticlesList:
            self.ui.ComboBox_typesOfParticles.addItem(i)
        for i in ParticlesTypeList:
            if i not in ParticlesList:
                self.ui.ComboBox_typesOfParticles.addItem(i)

    def refreshCombox(self):
        """
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        """
        try:
            ComboBox_Shadow_list = []
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
            volumeList = Tools2D.getLabelsByType(Tools2D.ObjectType.AreaConformal)
            for i in volumeList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def pb_ok_clicked(self):
        self.isKeepData = True
        self.close()

    def pb_cancel_clicked(self):
        self.isKeepData = False
        self.close()

    def loadData(self):
        self.ui.ComboBox_typesOfParticles.setCurrentIndex(self.ui.ComboBox_typesOfParticles.findText(str(self.obj.typesOfParticles)))
        self.ui.lineEdit_X1.setText(self.obj.gridMacroParticleNumberX)
        self.ui.lineEdit_Y1.setText(self.obj.gridMacroParticleNumberY)
        self.ui.lineEdit_X2.setText(self.obj.averagelectronVelocityX)
        self.ui.lineEdit_Y2.setText(self.obj.averagelectronVelocityY)
        self.ui.lineEdit_density.setText(self.obj.electricDensity)
        self.ui.lineEdit_temp.setText(self.obj.temperature)

    def keepData(self):
        self.obj.typesOfParticles = self.ui.ComboBox_typesOfParticles.currentText()
        self.obj.orthogonalProjectionArea = self.ui.ComboBox_Shadow.currentText()
        self.obj.gridMacroParticleNumberX = self.ui.lineEdit_X1.text()
        self.obj.gridMacroParticleNumberY = self.ui.lineEdit_Y1.text()
        self.obj.averagelectronVelocityX = self.ui.lineEdit_X2.text()
        self.obj.averagelectronVelocityY = self.ui.lineEdit_Y2.text()
        self.obj.electricDensity = self.ui.lineEdit_density.text()
        self.obj.temperature = self.ui.lineEdit_temp.text()

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)