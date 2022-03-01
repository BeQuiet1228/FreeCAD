# -*- coding: utf-8 -*-
import PortDialog
from PySide import QtGui
import FreeCAD
import FreeCADGui
from Modeling.Common.Tools import DocumentTools
from Modeling.Modeling2D.Tools import Tools2D


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = PortDialog.Ui_Dialog_PortDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.initDialog()
        self.loadData()
        self.setModal(False)
        self.isNew = isNew
        self.isKeepData = False

    def initDialog(self):
        try:
            self.defaultValue = []

            self.ui.pb_cancel.clicked.connect(self.onCancel)
            self.ui.pb_ok.clicked.connect(self.onConfirm)

            self.ui.radioButton_forward.setChecked(True)
            # 获取当前坐标系及坐标系单位
            coord = Tools2D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[2]
            # 根据坐标系初始化面板
            self.ui.label_X.setText(self.x)
            self.ui.label_Y.setText(self.y)
            self.ui.radioButton_x.setText(self.x)
            self.ui.radioButton_y.setText(self.y)
            self.ui.checkBox_x.setText(self.x)
            self.ui.checkBox_y.setText(self.y)
            self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + ") = ")
            self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + ") = ")
            # self.ui.LineEdit_start_x.setText("0" + self.x_unit)
            # self.ui.LineEdit_start_y.setText("0" + self.y_unit)
            # self.ui.LineEdit_end_x.setText("0" + self.x_unit)
            # self.ui.LineEdit_end_y.setText("0" + self.y_unit)
            self.refreshCombox()
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked_1)

            # 当port name被修改时触发函数修改归一化名字
            self.ui.LineEdit_Name.textChanged.connect(self.LineEdit_Name_textChanged)

            self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
            self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)

            self.ui.radioButton_x.clicked.connect(self.radioButton_x_clicked)
            self.ui.radioButton_y.clicked.connect(self.radioButton_y_clicked)

            self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
            self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)

            self.ui.checkBox_vport.clicked.connect(self.checkBox_vport_clicked)
            self.ui.checkBox_scale.clicked.connect(self.checkBox_scale_clicked)
            self.ui.checkBox_Ft.clicked.connect(self.checkBox_Ft_clicked)
            self.ui.checkBox_GE2.clicked.connect(self.checkBox_GE2_clicked)
            self.ui.checkBox_GE3.clicked.connect(self.checkBox_GE3_clicked)

            if self.ui.checkBox_Ft.isEnabled():
                self.ui.checkBox_FT.clicked.connect(self.checkBox_FT_clicked)

            self.ui.checkBox_circuit.clicked.connect(self.checkBox_circuit_clicked)

            # 初始化
            self.ComboBox_Shadow_clicked()
            self.userNameBefore = self.ui.LineEdit_Name.text()
            # 用于判断是否进行名称更新
            self.flagUpdateItemName = False

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        ComboBox_Shadow_list = []
        ComboBox_FT_list = []
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_FT.count()):
            ComboBox_FT_list.append(self.ui.ComboBox_FT.itemText(i))
        Orthogonal_list = Tools2D.getAllConformalLineLabel()

        for i in Orthogonal_list:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
        # 拉普拉斯下拉框添加正投影体选项
        volumeList = DocumentTools.getConductorVols()
        # # 线上电压归一化添加线选项
        lineList = Orthogonal_list
        # 这里的就是下拉栏里的名称
        for i in lineList:
            if i not in ComboBox_FT_list:
                self.ui.ComboBox_FT.addItem(i)

    # 点击取消按钮关闭窗口
    def onCancel(self):
        self.isKeepData = False
        self.close()

    # 点击确定按钮
    def onConfirm(self):
        self.isKeepData = True
        self.close()

    def loadData(self):
        try:
            # 名字
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.ComboBox_Shadow.setCurrentIndex(
                self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionPlane)))
            self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
            self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
            # # 法向选择
            # self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
            # self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)
            # DX编辑框
            self.ui.checkBox_x.setChecked(self.obj.isMarkX)
            self.checkBox_x_clicked()
            self.ui.checkBox_y.setChecked(self.obj.isMarkY)
            self.checkBox_y_clicked()
            self.ui.LineEdit_DX1.setText(self.obj.MarkX)
            self.ui.LineEdit_DX2.setText(self.obj.MarkY)
            # 相对加速比
            self.ui.checkBox_vport.setChecked(self.obj.isCheckVPORT)
            self.ui.LineEdit_vport.setEnabled(self.obj.isCheckVPORT)
            self.ui.LineEdit_vport.setText(self.obj.VPORT)
            # 法向修正
            self.ui.checkBox_scale.setChecked(self.obj.isCheckSCALE)
            self.ui.LineEdit_scale.setEnabled(self.obj.isCheckSCALE)
            self.ui.LineEdit_scale.setText(self.obj.SCALE)
            # 输入场时间分布
            self.ui.checkBox_Ft.setChecked(self.obj.isCheckFT)
            self.ui.LineEdit_Ft.setEnabled(self.obj.isCheckFT)
            self.ui.LineEdit_Ft.setText(self.obj.FT)
            # 空间分布2
            self.ui.checkBox_GE2.setChecked(self.obj.isCheckGE2)
            self.ui.LineEdit_GE2.setEnabled(self.obj.isCheckGE2)
            self.ui.LineEdit_GE2.setText(self.obj.GE2)
            # 空间分布3
            self.ui.checkBox_GE3.setChecked(self.obj.isCheckGE3)
            self.ui.LineEdit_GE3.setEnabled(self.obj.isCheckGE3)
            self.ui.LineEdit_GE3.setText(self.obj.GE3)
            # 线上电压归一化
            self.ui.checkBox_FT.setChecked(self.obj.isCheckNormalization)
            self.ui.checkBox_FT.setEnabled(self.obj.isCheckNormalization)
            # 当端口面为未指定的时候，默认线是否也得是未指定
            if self.obj.orthogonalProjectionPlane == u"未指定":
                self.ui.ComboBox_FT.setCurrentIndex(0)
            else:
                self.ui.ComboBox_FT.setCurrentIndex(self.ui.ComboBox_FT.findText(str(self.obj.normalization)))
            # circuit输入时间
            self.ui.checkBox_circuit.setEnabled(self.obj.isCircuit)
            self.ui.checkBox_circuit.setChecked(self.obj.isCircuit)
            self.ui.LineEdit_circuit.setEnabled(self.obj.isCircuit)
            self.ui.lineEdit_obs.setEnabled(self.obj.isCircuit)
            self.ui.label_obs.setEnabled(self.obj.isCircuit)
            self.ui.LineEdit_circuit.setText(self.obj.circuit)
            self.ui.lineEdit_obs.setText(self.obj.observeName)
            # 法向选择
            if self.obj.isCheckNormal1:
                self.ui.radioButton_x.setChecked(True)
                Tools2D.sayz("设置法相x")
                self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + ") = ")
                self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + ") = ")
            if self.obj.isCheckNormal2:
                self.ui.radioButton_y.setChecked(True)
                self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + ") = ")
                self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + ") = ")
            self.checkBox_Ft_clicked()

            # 正向反向选择
            if self.obj.isNegative is True:
                self.ui.radioButton_opposite.setChecked(True)
            if self.obj.isPositive is True:
                self.ui.radioButton_forward.setChecked(True)
        except KeyError as reason:
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    # 保存数据
    def keepData(self):
        try:
            # 名字
            Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
            self.obj.orthogonalProjectionPlane = self.ui.ComboBox_Shadow.currentText()
            # if self.ui.ComboBox_Shadow.currentIndex() == 0:
            #     DlgData.addData("isAppointArea",False)
            # else:
            #     DlgData.addData("isAppointArea",True)
            # DlgData.addData("Dlg_Type","Port_Type")
            self.obj.point1_X = self.ui.LineEdit_start_x.text()
            self.obj.point1_Y = self.ui.LineEdit_start_y.text()
            self.obj.point2_X = self.ui.LineEdit_end_x.text()
            self.obj.point2_Y = self.ui.LineEdit_end_y.text()
            # 法向选择
            self.obj.isCheckNormal1 = self.ui.radioButton_x.isChecked()
            self.obj.isCheckNormal2 = not (self.obj.isCheckNormal1)

            # 正向反向选择
            self.obj.isNegative = self.ui.radioButton_opposite.isChecked()
            self.obj.isPositive = self.ui.radioButton_forward.isChecked()

            # DX编辑框
            self.obj.isMarkX = self.ui.checkBox_x.isChecked()
            self.obj.isMarkY = self.ui.checkBox_y.isChecked()

            self.obj.MarkX = self.ui.LineEdit_DX1.text()
            self.obj.MarkY = self.ui.LineEdit_DX2.text()
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
            # 如果线上归一化下拉框选择的是portName.Line,则设置为True，代表需要新建一个conformal线
            # DlgData.addData("isNewConformalLine", self.ui.ComboBox_FT.currentIndex()==0)
            self.obj.normalization = self.ui.ComboBox_FT.currentText()
            # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_FT.currentText())
            # circuit输入时间
            self.obj.isCircuit = self.ui.checkBox_circuit.isChecked()
            self.obj.circuit = self.ui.LineEdit_circuit.text()
            self.obj.observeName = self.ui.lineEdit_obs.text().replace(' ', '')

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())
        pass

    # 正交投影面下拉列表
    def ComboBox_Shadow_clicked(self):
        # FreeCAD.Console.PrintError('\n进入下拉框点击函数\n')
        # ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentIndex())
        # FreeCAD.Console.PrintError('\n下拉框点击第一条命令\n')
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setEnabled(False)
            # self.LineEdit_Name_textChanged()
            # 起点可编辑
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            if self.ui.radioButton_x.isChecked() is True:
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(True)
            if self.ui.radioButton_y.isChecked() is True:
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
        else:
            # 线上电压归一化可选
            self.ui.ComboBox_FT.setEnabled(True)
            # 如果选择了投影线，则线的名字跟随投影线
            # self.ui.ComboBox_FT.setItemText(0, self.ui.ComboBox_Shadow.currentText())

            # 正交投影面
            objName = self.ui.ComboBox_Shadow.currentText()
            if objName in self.defaultValue:
                pass
            else:
                # 获得面的相关数据
                modelData = Tools2D.getValueOfAreaObjByLabel(objName)
                self.ui.LineEdit_start_x.setText(modelData["point1.x"])
                self.ui.LineEdit_start_y.setText(modelData["point1.y"])
                self.ui.LineEdit_end_x.setText(modelData["point2.x"])
                self.ui.LineEdit_end_y.setText(modelData["point2.y"])
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                # 法向
                if modelData["normal"] == "X" or modelData["normal"] == "x":
                    self.ui.radioButton_x.setChecked(True)
                    self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + ") = ")
                    self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + ") = ")
                elif modelData["normal"] == "Y" or modelData["normal"] == "y":
                    self.ui.radioButton_y.setChecked(True)
                    self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + ") = ")
                    self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + ") = ")
                else:
                    FreeCAD.Console.PrintMessage("get Area_Conformal error")
            self.ui.LineEdit_start_x.setEnabled(False)
            self.ui.LineEdit_start_y.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)

    # 当portname修改时，如果没有选择投影面，对应修改线上电压归一化对应的线名
    # （如果选择了投影面则线名和面名一致）# 根据要求将线上电压归一化的线名改成面名
    def LineEdit_Name_textChanged(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setItemText(0, self.ui.LineEdit_Name.text())

    # x法向修改时，修改起点即修改终点
    def LineEdit_start_x_textChanged(self):
        if not self.ui.LineEdit_end_x.isEnabled():
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # y法向修改时，修改起点即修改终点
    def LineEdit_start_y_textChanged(self):
        if not self.ui.LineEdit_end_y.isEnabled():
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # 点击法向x按钮
    def radioButton_x_clicked(self):
        self.ui.LineEdit_end_x.setEnabled(False)
        self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
        self.ui.LineEdit_end_y.setEnabled(True)
        self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + ") = ")
        self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + ") = ")

    # 点击法向y按钮
    def radioButton_y_clicked(self):
        self.ui.LineEdit_end_y.setEnabled(False)
        self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        self.ui.LineEdit_end_x.setEnabled(True)
        self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + ") = ")
        self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + ") = ")

    # 非均匀网格x
    def checkBox_x_clicked(self):
        self.ui.LineEdit_DX1.setEnabled(self.ui.checkBox_x.isChecked())

    # 非均匀网格y
    def checkBox_y_clicked(self):
        self.ui.LineEdit_DX2.setEnabled(self.ui.checkBox_y.isChecked())

    # 相对加速比
    def checkBox_vport_clicked(self):
        self.ui.LineEdit_vport.setEnabled(self.ui.checkBox_vport.isChecked())

    # 法向修正
    def checkBox_scale_clicked(self):
        self.ui.LineEdit_scale.setEnabled(self.ui.checkBox_scale.isChecked())

    def ciucuit_function(self):
        '''
        关于circuit部分小部件的逻辑的函数
        '''
        if self.ui.checkBox_Ft.isChecked():
            self.ui.checkBox_circuit.setEnabled(True)
        else:
            self.ui.checkBox_circuit.setChecked(False)
            self.ui.checkBox_circuit.setEnabled(False)
            self.ui.LineEdit_circuit.setEnabled(False)
            self.ui.label_obs.setEnabled(False)
            self.ui.lineEdit_obs.setEnabled(False)

    # 时间分布
    def checkBox_Ft_clicked(self):
        self.ui.LineEdit_Ft.setEnabled(self.ui.checkBox_Ft.isChecked())
        self.ui.checkBox_FT.setEnabled(self.ui.checkBox_Ft.isChecked())
        self.ciucuit_function()

    # 空间分布1
    def checkBox_GE2_clicked(self):
        # self.ui.LineEdit_GE2.setEnabled(self.ui.checkBox_GE2.isChecked())
        self.ui.LineEdit_GE2.setEnabled(self.ui.checkBox_GE2.isChecked())
        # self.ciucuit_function()

    # 空间分布2
    def checkBox_GE3_clicked(self):
        # self.ui.LineEdit_GE3.setEnabled(self.ui.checkBox_GE3.isChecked())
        self.ui.LineEdit_GE3.setEnabled(self.ui.checkBox_GE3.isChecked())
        # self.ciucuit_function()

    # 线上归一电压
    def checkBox_FT_clicked(self):
        # 当正投影面不是未指定时，才可选择正投影线
        if self.ui.ComboBox_Shadow.currentIndex() != 0:
            self.ui.ComboBox_FT.setEnabled(self.ui.checkBox_FT.isChecked())

    # 输入时间
    def checkBox_circuit_clicked(self):
        if self.ui.checkBox_circuit.isChecked():
            self.ui.LineEdit_circuit.setEnabled(True)
            self.ui.label_obs.setEnabled(True)
            self.ui.lineEdit_obs.setEnabled(True)
        else:
            self.ui.LineEdit_circuit.setEnabled(False)
            self.ui.label_obs.setEnabled(False)
            self.ui.lineEdit_obs.setEnabled(False)

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

    def ComboBox_Shadow_clicked_1(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setEnabled(False)
            self.LineEdit_Name_textChanged()
            # 设置ui坐标的可编辑状态
            # Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Area_Conformal)
            # 如果选择未指定，则线的名字跟随波导的名字
            self.ui.ComboBox_FT.setItemText(0, self.ui.LineEdit_Name.text())
            self.ui.ComboBox_FT.setCurrentIndex(0)
        else:
            # 线上电压归一化可选
            self.ui.ComboBox_FT.setEnabled(True)
            # 如果选择了投影面，则线的名字跟随投影面
            tmp = self.ui.ComboBox_FT.findText(self.ui.ComboBox_Shadow.currentText())
            if tmp == -1:
                self.ui.ComboBox_FT.setItemText(0, self.ui.ComboBox_Shadow.currentText())
                self.ui.ComboBox_FT.setCurrentIndex(0)
            else:
                self.ui.ComboBox_FT.setItemText(0, self.ui.LineEdit_Name.text())
                self.ui.ComboBox_FT.setCurrentIndex(tmp)



