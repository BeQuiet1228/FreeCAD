# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D,ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import PopuDialog


def getNewParticle():
    NewParticle_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.NewParticle)
    NewParticleName_list = []
    for ele in NewParticle_list:
        NewParticleName_list.append(ele)
    return NewParticleName_list


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = PopuDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            #代码补全
            self.defaultValue = ["OSYS$VOLUME"]
            # 获取当前坐标系及坐标系单位

            coord = Tools3D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[2]
            self.x_unit = coord[3]
            self.y_unit = coord[4]
            self.z_unit = coord[5]

            # 根据坐标系初始化面板
            self.ui.label_X.setText(self.x)
            self.ui.label_Y.setText(self.y)
            self.ui.label_Z.setText(self.z)
            self.initParticles()
            # 初始化正交投影面列表
            self.refreshCombox()
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

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
            volumeList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
            for i in volumeList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            index1 = self.ui.ComboBox_typesOfParticles.findText(str(self.obj.typesOfParticles))
            self.ui.ComboBox_typesOfParticles.setCurrentIndex(index1)
            index2 = self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionArea))
            self.ui.ComboBox_Shadow.setCurrentIndex(index2)
            self.ui.lineEdit_X1.setText(self.obj.gridMacroParticleNumberX)
            self.ui.lineEdit_Y1.setText(self.obj.gridMacroParticleNumberY)
            self.ui.lineEdit.setText(self.obj.gridMacroParticleNumberZ)
            self.ui.lineEdit_X2.setText(self.obj.averagelectronVelocityX)
            self.ui.lineEdit_Y2.setText(self.obj.averagelectronVelocityY)
            self.ui.lineEdit_2.setText(self.obj.averagelectronVelocityZ)
            self.ui.lineEdit_density.setText(self.obj.electricDensity)
            self.ui.lineEdit_temp.setText(self.obj.temperature)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())
        # except KeyError as reason:
        #     Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.typesOfParticles = self.ui.ComboBox_typesOfParticles.currentText()
            self.obj.orthogonalProjectionArea = self.ui.ComboBox_Shadow.currentText()
            self.obj.gridMacroParticleNumberX = self.ui.lineEdit_X1.text()
            self.obj.gridMacroParticleNumberY = self.ui.lineEdit_Y1.text()
            self.obj.gridMacroParticleNumberZ = self.ui.lineEdit.text()
            self.obj.averagelectronVelocityX = self.ui.lineEdit_X2.text()
            self.obj.averagelectronVelocityY = self.ui.lineEdit_Y2.text()
            self.obj.averagelectronVelocityZ = self.ui.lineEdit_2.text()
            self.obj.electricDensity = self.ui.lineEdit_density.text()
            self.obj.temperature = self.ui.lineEdit_temp.text()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())
        pass

    def setPrivateInfoToObj(self):
        pass

