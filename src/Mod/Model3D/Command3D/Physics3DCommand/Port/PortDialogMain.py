# -*- coding: utf-8 -*-
import FreeCAD
from Model3D.Tools import Tools3D, ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import PortDialog
import traceback


# 坐标信息
def getCoordinate():
    """
    获取坐标系的标签
    """
    coordinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coordinate == u'Rectangular':
        unitList = ["X", "Y", "Z", "m", "m", "m"]
    elif coordinate == u"Polar":
        unitList = ["R", "P", "Z", "m", "deg", "m"]
    else:
        unitList = ["Z", "R", "P", "m", "m", "deg"]
    return unitList


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = PortDialog.Ui_Dialog_PortDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        try:
            self.defaultValue = ["OSYS$MIDPLANE1", "OSYS$MIDPLANE2", "OSYS$MIDPLANE3"]
            # 根据坐标系初始化面板
            Tools3D.switchPointLabel(self.ui)
            Tools3D.switchRadioButtonLabel(self.ui)
            Tools3D.switchCheckLabel(self.ui)

            # 获取当前坐标系及坐标系单位
            coord = getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[2]
            self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
            self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")

            # 动态刷新下拉框
            self.refreshCombox()
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked_1)

            # 当port name被修改时触发函数修改归一化名字
            self.ui.LineEdit_Name.textChanged.connect(self.LineEdit_Name_textChanged)
            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_textChanged)
            self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_textChanged)

            self.ui.radioButton_x.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_clicked)
            self.ui.radioButton_z.clicked.connect(self.radioButton_clicked)

            self.ui.checkBox_x.clicked.connect(self.checkBox_clicked)
            self.ui.checkBox_y.clicked.connect(self.checkBox_clicked)
            self.ui.checkBox_z.clicked.connect(self.checkBox_clicked)

            self.ui.checkBox_vport.clicked.connect(self.checkBox_vport_clicked)
            self.ui.checkBox_scale.clicked.connect(self.checkBox_scale_clicked)
            self.ui.checkBox_Ft.clicked.connect(self.checkBox_Ft_clicked)
            self.ui.checkBox_GE2.clicked.connect(self.checkBox_GE_clicked)
            self.ui.checkBox_GE3.clicked.connect(self.checkBox_GE_clicked)
            self.ui.checkBox_lap.clicked.connect(self.checkBox_lap_clicked)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        for i in self.defaultValue:
            self.ui.ComboBox_Shadow.addItem(i)
        ComboBox_Shadow_list = []
        ComboBox_FT_list = []
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))

        for i in range(self.ui.ComboBox_FT.count()):
            ComboBox_FT_list.append(self.ui.ComboBox_FT.itemText(i))

        AreaConforaml_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Area_Conformal)
        for i in AreaConforaml_list:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)

        #  归一化线
        LineConformal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Line_Conformal)
        for i in AreaConforaml_list:
            if i not in ComboBox_FT_list:
                self.ui.ComboBox_FT.addItem(i+".LINE")
        for i in LineConformal_list:
            if i not in ComboBox_FT_list:
                self.ui.ComboBox_FT.addItem(i)

        # 拉普拉斯只存放属性为Conductor的正投影体
        ComboBox_lap_list = []
        ConductorVolList = ObjectTools.getConductorVols()
        for i in ConductorVolList:
            if i not in ComboBox_lap_list:
                self.ui.ComboBox_lap1.addItem(i)
                self.ui.ComboBox_lap2.addItem(i)
                self.ui.ComboBox_lap3.addItem(i)
                self.ui.ComboBox_lap4.addItem(i)
                self.ui.ComboBox_lap5.addItem(i)

    def ComboBox_Shadow_clicked(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setEnabled(False)
            # 设置ui坐标的可编辑状态
            Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Area_Conformal)
        else:
            objName = self.ui.ComboBox_Shadow.currentText()
            # 正交投影面
            if objName in self.defaultValue:
                pass
            else:
                modelObj = ObjectTools.getObjByLabel(objName)
                self.ui.LineEdit_start_x.setText(str(modelObj.user_point1_x).replace(' ', ''))
                self.ui.LineEdit_start_y.setText(str(modelObj.user_point1_y).replace(' ', ''))
                self.ui.LineEdit_start_z.setText(str(modelObj.user_point1_z).replace(' ', ''))
                self.ui.LineEdit_end_x.setText(str(modelObj.user_point2_x).replace(' ', ''))
                self.ui.LineEdit_end_y.setText(str(modelObj.user_point2_y).replace(' ', ''))
                self.ui.LineEdit_end_z.setText(str(modelObj.user_point2_z).replace(' ', ''))
                # 法向
                # 获取当前坐标系及坐标系单位
                coord = Tools3D.getCoordinate()
                if hasattr(modelObj, "Normal"):
                    if modelObj.Normal == coord[0]:
                        self.ui.radioButton_x.setChecked(True)
                        self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
                        self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
                    elif modelObj.Normal == coord[1]:
                        self.ui.radioButton_y.setChecked(True)
                        self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
                        self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
                    else:
                        self.ui.radioButton_z.setChecked(True)
                        self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
                        self.ui.checkBox_GE3.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
            # 设置坐标，法向按钮不可编辑
            Tools3D.setIsEdit(self.ui, False)

    # 当portname修改时，如果没有选择投影面，对应修改线上电压归一化对应的线名
    # （如果选择了投影面则线名和面名一致）# 根据要求将线上电压归一化的线名改成面名
    def LineEdit_Name_textChanged(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setItemText(0, self.ui.LineEdit_Name.text()+".LINE")

    # 法向修改时，修改起点即修改终点
    def LineEdit_start_textChanged(self):
        if not self.ui.LineEdit_end_x.isEnabled():
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
        if not self.ui.LineEdit_end_y.isEnabled():
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        if not self.ui.LineEdit_end_z.isEnabled():
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    # 点击法向按钮
    def radioButton_clicked(self):
        if self.ui.radioButton_x.isChecked():
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
            self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
        elif self.ui.radioButton_y.isChecked():
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_z.setEnabled(True)
            self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z +  ") = ")
            self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z +  ") = ")
        elif self.ui.radioButton_z.isChecked():
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
            self.ui.LineEdit_end_x.setEnabled(True)
            self.ui.LineEdit_end_y.setEnabled(True)
            self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z +  ") = ")
            self.ui.checkBox_GE3.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z +  ") = ")

    # 非均匀网格
    def checkBox_clicked(self):
        self.ui.LineEdit_DX1.setEnabled(self.ui.checkBox_x.isChecked())
        self.ui.LineEdit_DX2.setEnabled(self.ui.checkBox_y.isChecked())
        self.ui.LineEdit_DX3.setEnabled(self.ui.checkBox_z.isChecked())

    # 时间分布
    def checkBox_Ft_clicked(self):
        self.ui.LineEdit_Ft.setEnabled(self.ui.checkBox_Ft.isChecked())
        self.ui.checkBox_FT.setEnabled(self.ui.checkBox_Ft.isChecked())
        self.ui.checkBox_circuit.setEnabled(self.ui.checkBox_Ft.isChecked())
        self.ui.checkBox_circuit.clicked.connect(self.ciucuit_function)

    # circuit 输入时间
    def ciucuit_function(self):
        self.ui.LineEdit_circuit.setEnabled(self.ui.checkBox_circuit.isChecked())
        self.ui.lineEdit_obs.setEnabled(self.ui.checkBox_circuit.isChecked())

    # 相对加速比
    def checkBox_vport_clicked(self):
        self.ui.LineEdit_vport.setEnabled(self.ui.checkBox_vport.isChecked())

    # 法向修正
    def checkBox_scale_clicked(self):
        self.ui.LineEdit_scale.setEnabled(self.ui.checkBox_scale.isChecked())

    def checkBox_GE_clicked(self):
        self.ui.LineEdit_GE2.setEnabled(self.ui.checkBox_GE2.isChecked())
        self.ui.LineEdit_GE3.setEnabled(self.ui.checkBox_GE3.isChecked())
        if self.ui.checkBox_GE2.isChecked() or self.ui.checkBox_GE3.isChecked():
            self.ui.checkBox_lap.setEnabled(False)
        else:
            self.ui.checkBox_lap.setEnabled(True)

    def checkBox_lap_clicked(self):
        self.ui.ComboBox_lap1.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.ComboBox_lap2.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.spinBox.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.spinBox_2.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.spinBox_num.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.spinBox_num.valueChanged.connect(self.setSpinBoxNum)
        self.ui.checkBox_GE2.setEnabled(not self.ui.checkBox_lap.isChecked())
        self.ui.checkBox_GE3.setEnabled(not self.ui.checkBox_lap.isChecked())

    def setSpinBoxNum(self):
        spin_num = self.ui.spinBox_num.value()
        if spin_num == 2:
            self.ui.ComboBox_lap3.setEnabled(False)
            self.ui.ComboBox_lap4.setEnabled(False)
            self.ui.ComboBox_lap5.setEnabled(False)
            self.ui.spinBox_3.setEnabled(False)
            self.ui.spinBox_4.setEnabled(False)
            self.ui.spinBox_5.setEnabled(False)
        elif spin_num == 3:
            self.ui.ComboBox_lap3.setEnabled(True)
            self.ui.ComboBox_lap4.setEnabled(False)
            self.ui.ComboBox_lap5.setEnabled(False)
            self.ui.spinBox_3.setEnabled(True)
            self.ui.spinBox_4.setEnabled(False)
            self.ui.spinBox_5.setEnabled(False)
        elif spin_num == 4:
            self.ui.ComboBox_lap3.setEnabled(True)
            self.ui.ComboBox_lap4.setEnabled(True)
            self.ui.ComboBox_lap5.setEnabled(False)
            self.ui.spinBox_3.setEnabled(True)
            self.ui.spinBox_4.setEnabled(True)
            self.ui.spinBox_5.setEnabled(False)
        elif spin_num == 5:
            self.ui.ComboBox_lap3.setEnabled(True)
            self.ui.ComboBox_lap4.setEnabled(True)
            self.ui.ComboBox_lap5.setEnabled(True)
            self.ui.spinBox_3.setEnabled(True)
            self.ui.spinBox_4.setEnabled(True)
            self.ui.spinBox_5.setEnabled(True)

    def getInfoFromObj(self):
        try:
            # 名字
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.ComboBox_Shadow.setCurrentIndex(
                self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionPlane)))
            # 坐标
            Tools3D.setCoorToUI(self.ui, self.obj)
            self.ComboBox_Shadow_clicked()
            # 法向
            Tools3D.setRadioButtonToUI(self.ui, self.obj)
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.radioButton_clicked()
            # 正向反向
            self.ui.radioButton_opposite.setChecked(self.obj.isNegative)
            self.ui.radioButton_forward.setChecked(self.obj.isPositive)
            # DX编辑框
            Tools3D.setGridToUI(self.ui, self.obj)
            self.checkBox_clicked()

            # 相对加速比
            self.ui.checkBox_vport.setChecked(self.obj.isCheckVPORT)
            self.ui.LineEdit_vport.setText(self.obj.VPORT)
            self.checkBox_vport_clicked()
            # 法向修正
            self.ui.checkBox_scale.setChecked(self.obj.isCheckSCALE)
            self.ui.LineEdit_scale.setText(self.obj.SCALE)
            self.checkBox_scale_clicked()
            # 输入场时间分布
            self.ui.checkBox_Ft.setChecked(self.obj.isCheckFT)
            self.ui.LineEdit_Ft.setText(self.obj.FT)
            self.checkBox_Ft_clicked()
            # 空间分布2
            self.ui.checkBox_GE2.setChecked(self.obj.isCheckGE2)
            self.ui.LineEdit_GE2.setText(self.obj.GE2)
            # 空间分布3
            self.ui.checkBox_GE3.setChecked(self.obj.isCheckGE3)
            self.ui.LineEdit_GE3.setText(self.obj.GE3)
            self.checkBox_GE_clicked()
            # 线上电压归一化
            self.ui.checkBox_FT.setChecked(self.obj.isCheckNormalization)
            if self.obj.orthogonalProjectionPlane == u"未指定":
                self.ui.ComboBox_FT.setCurrentIndex(0)
            else:
                self.ui.ComboBox_FT.setCurrentIndex(self.ui.ComboBox_FT.findText(str(self.obj.normalization)))

            # circuit输入时间
            self.ui.checkBox_circuit.setChecked(self.obj.isCircuit)
            self.ui.LineEdit_circuit.setText(self.obj.circuit)
            self.ui.lineEdit_obs.setText(self.obj.observeName)
            self.ciucuit_function()
            # 拉普拉斯
            self.ui.checkBox_lap.setChecked(self.obj.isCheckLapras)
            self.ui.spinBox_num.setValue(self.obj.laprasNumbers)
            self.ui.ComboBox_lap1.setCurrentIndex(self.ui.ComboBox_lap1.findText(str(self.obj.lapras1)))
            self.ui.spinBox.setValue(self.obj.lapras1Value)
            self.ui.ComboBox_lap2.setCurrentIndex(self.ui.ComboBox_lap2.findText(str(self.obj.lapras2)))
            self.ui.spinBox_2.setValue(self.obj.lapras2Value)
            self.ui.ComboBox_lap3.setCurrentIndex(self.ui.ComboBox_lap3.findText(str(self.obj.lapras3)))
            self.ui.spinBox_3.setValue(self.obj.lapras3Value)
            self.ui.ComboBox_lap4.setCurrentIndex(self.ui.ComboBox_lap4.findText(str(self.obj.lapras4)))
            self.ui.spinBox_4.setValue(self.obj.lapras4Value)
            self.ui.ComboBox_lap5.setCurrentIndex(self.ui.ComboBox_lap5.findText(str(self.obj.lapras5)))
            self.ui.spinBox_5.setValue(self.obj.lapras5Value)
            self.checkBox_lap_clicked()
            self.setSpinBoxNum()

        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def setInfoToObj(self):

        self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
        self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
        # 坐标
        Tools3D.getUICoordinate(self.obj, self.ui)
        # 法向选择
        Tools3D.getUIRadioButton(self.obj, self.ui)
        # 正向反向选择
        self.obj.isNegative = self.ui.radioButton_opposite.isChecked()
        self.obj.isPositive = self.ui.radioButton_forward.isChecked()
        # DX编辑框
        Tools3D.getUIGrid(self.obj, self.ui)
        # 相对加速比
        self.obj.isCheckVPORT = self.ui.checkBox_vport.isChecked()
        self.obj.VPORT = self.ui.LineEdit_vport.text()
        # 法向修正
        self.obj.isCheckSCALE = self.ui.checkBox_scale.isChecked()
        self.obj.SCALE = self.ui.LineEdit_scale.text()
        # 输入场时间分布
        self.obj.isCheckFT = self.ui.checkBox_Ft.isChecked()
        self.obj.FT = self.ui.LineEdit_Ft.toPlainText()
        # 空间分布
        self.obj.isCheckGE2 = self.ui.checkBox_GE2.isChecked()
        self.obj.isCheckGE3 = self.ui.checkBox_GE3.isChecked()
        self.obj.GE2 = self.ui.LineEdit_GE2.toPlainText()
        self.obj.GE3 = self.ui.LineEdit_GE3.toPlainText()
        # 线上电压归一化
        self.obj.isCheckNormalization = self.ui.checkBox_FT.isChecked()
        self.obj.normalization = self.ui.ComboBox_FT.currentText()
        # circuit输入时间
        self.obj.isCircuit = self.ui.checkBox_circuit.isChecked()
        self.obj.circuit = self.ui.LineEdit_circuit.text()
        self.obj.observeName = self.ui.lineEdit_obs.text()
        # 拉普拉斯
        self.obj.isCheckLapras = self.ui.checkBox_lap.isChecked()
        self.obj.laprasNumbers = self.ui.spinBox_num.value()
        self.obj.lapras1 = self.ui.ComboBox_lap1.currentText()
        self.obj.lapras1Value = self.ui.spinBox.value()
        self.obj.lapras2 = self.ui.ComboBox_lap2.currentText()
        self.obj.lapras2Value = self.ui.spinBox_2.value()
        self.obj.lapras3 = self.ui.ComboBox_lap3.currentText()
        self.obj.lapras3Value = self.ui.spinBox_3.value()
        self.obj.lapras4 = self.ui.ComboBox_lap4.currentText()
        self.obj.lapras4Value = self.ui.spinBox_4.value()
        self.obj.lapras5 = self.ui.ComboBox_lap5.currentText()
        self.obj.lapras5Value = self.ui.spinBox_5.value()

        if self.obj.isCheckNormalization:
            temp = ""
            coodinate = FreeCAD.ActiveDocument.CoordinateSystem
            if coodinate == u'Rectangular':
                if self.obj.isCheckNormal1:
                    temp = self.obj.point1_Z.replace(" ", "") + "+" + self.obj.point2_Z.replace(" ", "")
                elif self.obj.isCheckNormal2:
                    temp = self.obj.point1_X.replace(" ", "") + "+" + self.obj.point2_X.replace(" ", "")
                elif self.obj.isCheckNormal3:
                    temp = self.obj.point1_Y.replace(" ", "") + "+" + self.obj.point2_Y.replace(" ", "")
                self.obj.setExpression("helper", temp)
                # self.obj.helper = (self.obj.helper.Value) / 2
                # Tools3D.sayz(str((self.obj.helper) / 2) + "teeeeeeeeeer")
            elif coodinate == u"Polar":
                if self.obj.isCheckNormal1:
                    temp = self.obj.point1_Y.replace(" ", "") + "+" + self.obj.point2_Y.replace(" ", "")
                    self.obj.setExpression("helper0", temp)
                    # self.obj.helper0 = (self.obj.helper0.Value) / 2
                elif self.obj.isCheckNormal2:
                    temp = self.obj.point1_Z.replace(" ", "") + "+" + self.obj.point2_Z.replace(" ", "")
                    self.obj.setExpression("helper", temp)
                    # self.obj.helper = (self.obj.helper.Value) / 2
                elif self.obj.isCheckNormal3:
                    temp = self.obj.point1_Y.replace(" ", "") + "+" + self.obj.point2_Y.replace(" ", "")
                    self.obj.setExpression("helper0", temp)
                    # self.obj.helper0 = (self.obj.helper0.Value) / 2
            elif coodinate == u"Cylindrical":
                if self.obj.isCheckNormal1:
                    temp = self.obj.point1_Z.replace(" ", "") + "+" + self.obj.point2_Z.replace(" ", "")
                    self.obj.setExpression("helper0", temp)
                    # self.obj.helper0 = (self.obj.helper0.Value) / 2
                elif self.obj.isCheckNormal2:
                    temp = self.obj.point1_Z.replace(" ", "") + "+" + self.obj.point2_Z.replace(" ", "")
                    self.obj.setExpression("helper0", temp)
                    # self.obj.helper0 = (self.obj.helper0.Value) / 2
                elif self.obj.isCheckNormal3:
                    temp = self.obj.point1_X.replace(" ", "") + "+" + self.obj.point2_X.replace(" ", "")
                    self.obj.setExpression("helper", temp)
                    # self.obj.helper = (self.obj.helper.Value / 2)
            else:
                # temp = None
                Tools3D.sayz("错误")
            # self.obj.setExpression("helper", temp)
            # self.obj.helper = (self.obj.helper.Value) / 2

    def ComboBox_Shadow_clicked_1(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setEnabled(False)
            self.LineEdit_Name_textChanged()
            # 设置ui坐标的可编辑状态
            #Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Area_Conformal)
            # 如果选择未指定，则线的名字跟随波导的名字
            self.ui.ComboBox_FT.setItemText(0, self.ui.LineEdit_Name.text() + ".LINE")
            self.ui.ComboBox_FT.setCurrentIndex(0)
        else:
            # 线上电压归一化可选
            self.ui.ComboBox_FT.setEnabled(True)
            # 如果选择了投影面，则线的名字跟随投影面
            tmp = self.ui.ComboBox_FT.findText(self.ui.ComboBox_Shadow.currentText() + ".LINE")
            if tmp == -1:
                self.ui.ComboBox_FT.setItemText(0, self.ui.ComboBox_Shadow.currentText() + ".LINE")
                self.ui.ComboBox_FT.setCurrentIndex(0)
            else:
                self.ui.ComboBox_FT.setItemText(0, self.ui.LineEdit_Name.text() + ".LINE")
                self.ui.ComboBox_FT.setCurrentIndex(tmp)
