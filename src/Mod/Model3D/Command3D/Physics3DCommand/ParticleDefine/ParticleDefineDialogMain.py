# -*- coding: utf-8 -*-
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import ParticleDefineDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = ParticleDefineDialog.Ui_Dialog()
        self.ui.setupUi(self)


    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            # 获取当前坐标系及坐标系单位
            coord = Tools3D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[2]
            self.x_unit = coord[3]
            self.y_unit = coord[4]
            self.z_unit = coord[5]

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.LineEdit_Unitl.setText(self.obj.powerUnit)
            self.ui.LineEdit_Quality.setText(self.obj.mass)
            self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(self.obj.protonMassUnit))
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
            self.obj.powerUnit = self.ui.LineEdit_Unitl.text().replace(" ", "")
            self.obj.mass = self.ui.LineEdit_Quality.text().replace(" ", "")
            self.obj.protonMassUnit = self.ui.comboBox.currentText()
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setPrivateInfoToObj(self):
        pass
