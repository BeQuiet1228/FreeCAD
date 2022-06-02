# -*- coding: utf-8 -*-
from Model3D.Tools import Tools3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import SolendDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = SolendDialog.Ui_Dialog_SolDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            #代码补全
            self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3"]
            # 获取当前坐标系及坐标系单位
            coord = Tools3D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[2]
            self.x_unit = coord[3]
            self.y_unit = coord[4]
            self.z_unit = coord[5]

            self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
            self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)
            self.ui.checkBox_z.clicked.connect(self.checkBox_z_clicked)
            Tools3D.switchCheckLabel(self.ui)
            # # 刷新下拉框
            # self.refreshCombox()
            # # 正投影面下拉框选择事件
            self.ui.ComboBox_uniformParam.currentIndexChanged.connect(self.ComboBox_uniformParam_clicked)
            self.ComboBox_uniformParam_clicked()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def ComboBox_uniformParam_clicked(self):
        if self.ui.ComboBox_uniformParam.currentIndex() == 0:
            self.ui.LineEdit_Rparam.setEnabled(False)
            self.ui.LineEdit_Zparam.setEnabled(False)
            self.ui.LineEdit_RadiusOut.setEnabled(False)
            self.ui.LineEdit_duty.setEnabled(False)
            self.ui.LineEdit_RadiusIn.setEnabled(False)
            self.ui.LineEdit_Permeability.setEnabled(False)
            self.ui.LineEdit_current.setEnabled(True)
            self.ui.LineEdit_theta.setEnabled(True)
            self.ui.LineEdit_phi.setEnabled(True)
        elif self.ui.ComboBox_uniformParam.currentIndex() == 1:
            self.ui.LineEdit_Rparam.setEnabled(True)
            self.ui.LineEdit_Zparam.setEnabled(True)
            self.ui.LineEdit_RadiusOut.setEnabled(False)
            self.ui.LineEdit_duty.setEnabled(False)
            self.ui.LineEdit_RadiusIn.setEnabled(False)
            self.ui.LineEdit_Permeability.setEnabled(False)
            self.ui.LineEdit_current.setEnabled(True)
            self.ui.LineEdit_theta.setEnabled(True)
            self.ui.LineEdit_phi.setEnabled(True)
        elif self.ui.ComboBox_uniformParam.currentIndex() == 2:
            self.ui.LineEdit_Rparam.setEnabled(False)
            self.ui.LineEdit_Zparam.setEnabled(False)
            self.ui.LineEdit_RadiusOut.setEnabled(True)
            self.ui.LineEdit_duty.setEnabled(True)
            self.ui.LineEdit_RadiusIn.setEnabled(True)
            self.ui.LineEdit_Permeability.setEnabled(True)
            self.ui.LineEdit_current.setEnabled(True)
            self.ui.LineEdit_theta.setEnabled(True)
            self.ui.LineEdit_phi.setEnabled(True)

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.LineEdit_CenterR.setText(self.obj.coreR)
            self.ui.LineEdit_CenterZ.setText(self.obj.coreZ)
            self.ui.ComboBox_uniformParam.setCurrentIndex(self.ui.ComboBox_uniformParam.findText(str(self.obj.uniformParam)))
            self.ui.LineEdit_halfRadius.setText(str(self.obj.coilHalf).replace(' ', ''))
            self.ui.LineEdit_radiusIn.setText(str(self.obj.innerRadius).replace(' ', ''))
            self.ui.LineEdit_radiusOut.setText(str(self.obj.outerRadius).replace(' ', ''))
            self.ui.LineEdit_num.setText(self.obj.turnRatio)
            self.ui.LineEdit_Rparam.setText(self.obj.factorR)
            self.ui.LineEdit_Zparam.setText(self.obj.factorZ)
            self.ui.LineEdit_duty.setText(self.obj.dutyCycle)
            self.ui.LineEdit_RadiusIn.setText(self.obj.radiusInner)
            self.ui.LineEdit_RadiusOut.setText(self.obj.radiusOuter)
            self.ui.LineEdit_Permeability.setText(self.obj.permeability)
            self.ui.LineEdit_current.setText(self.obj.coilCurrent)
            self.ui.LineEdit_theta.setText(self.obj.angleTheta)
            self.ui.LineEdit_phi.setText(self.obj.anglePhi)
            Tools3D.setGridToUI(self.ui, self.obj)
            self.checkBox_x_clicked()
            self.checkBox_y_clicked()
            self.checkBox_z_clicked()


        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            self.obj.coreR = self.ui.LineEdit_CenterR.text()
            self.obj.coreZ = self.ui.LineEdit_CenterZ.text()
            self.obj.uniformParam = self.ui.ComboBox_uniformParam.currentText()
            self.obj.coilHalf = self.ui.LineEdit_halfRadius.text()
            self.obj.innerRadius = self.ui.LineEdit_radiusIn.text()
            self.obj.outerRadius = self.ui.LineEdit_radiusOut.text()
            self.obj.turnRatio = self.ui.LineEdit_num.text()
            self.obj.factorR = self.ui.LineEdit_Rparam.text()
            self.obj.factorZ = self.ui.LineEdit_Zparam.text()
            self.obj.dutyCycle = self.ui.LineEdit_duty.text()
            self.obj.radiusInner = self.ui.LineEdit_RadiusIn.text()
            self.obj.radiusOuter = self.ui.LineEdit_RadiusOut.text()
            self.obj.permeability = self.ui.LineEdit_Permeability.text()
            self.obj.coilCurrent = self.ui.LineEdit_current.text()
            self.obj.angleTheta = self.ui.LineEdit_theta.text()
            self.obj.anglePhi = self.ui.LineEdit_phi.text()

            # DX编辑框
            Tools3D.getUIGrid(self.obj, self.ui)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setPrivateInfoToObj(self):
        pass

    def checkBox_x_clicked(self):
        if self.ui.checkBox_x.isChecked():
            self.ui.LineEdit_DX1.setEnabled(True)
        else:
            self.ui.LineEdit_DX1.setEnabled(False)

    def checkBox_y_clicked(self):
        if self.ui.checkBox_y.isChecked():
            self.ui.LineEdit_DX2.setEnabled(True)
        else:
            self.ui.LineEdit_DX2.setEnabled(False)

    def checkBox_z_clicked(self):
        if self.ui.checkBox_z.isChecked():
            self.ui.LineEdit_DX3.setEnabled(True)
        else:
            self.ui.LineEdit_DX3.setEnabled(False)

    def initDialog(self):
        self.ui.pushButton_ok.clicked.connect(self.slotOK)
        self.ui.pushButton.clicked.connect(self.slotCancel)