#-*- coding: utf-8 -*-
import PortDialog
from PySide import QtGui
import FreeCAD
from Physics.PhysicsCommand import Simulation
from Physics.PhysicsCommand.DlgData import sayz
from Modeling.Common.Tools import DocumentTools,ObjectsTools
from Physics.PhysicsTools import CompleterTools
from Modeling.Modeling2D.Tools import Tools2D

class ShowDialog(QtGui.QDialog):
    def __init__(self,obj,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = PortDialog.Ui_Dialog_PortDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.initDialog()
        self.loadData()

    def initDialog(self):
        try:
            #代码补全
            self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3"]
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            self.ui.pb_cancel.clicked.connect(self.onCancel)
            self.ui.pb_ok.clicked.connect(self.onConfirm)
            self.ui.radioButton_forward.setChecked(True)
            # 获取当前坐标系及坐标系单位
            coord = Simulation.getCoordinate()
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
            self.ui.radioButton_x.setText(self.x)
            self.ui.radioButton_y.setText(self.y)
            self.ui.radioButton_z.setText(self.z)
            self.ui.checkBox_x.setText(self.x)
            self.ui.checkBox_y.setText(self.y)
            self.ui.checkBox_z.setText(self.z)
            self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
            self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
            self.ui.LineEdit_start_x.setText("0" + self.x_unit)
            self.ui.LineEdit_start_y.setText("0" + self.y_unit)
            self.ui.LineEdit_start_z.setText("0" + self.z_unit)
            self.ui.LineEdit_end_x.setText("0" + self.x_unit)
            self.ui.LineEdit_end_y.setText("0" + self.y_unit)
            self.ui.LineEdit_end_z.setText("0" + self.z_unit)
            self.refreshCombox() 
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)

            # 关闭Z轴设置
            self.ui.label_Z.hide()
            self.ui.radioButton_z.hide()
            self.ui.checkBox_z.hide()
            self.ui.LineEdit_start_z.hide()
            self.ui.LineEdit_end_z.hide()
            self.ui.LineEdit_DX3.hide()

            # 当portname被修改时触发函数修改归一化名字
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
            # 拉普拉斯设置数量出现变化时，相应的修改界面下拉框的数量 
            self.ui.spinBox_num.valueChanged.connect(self.setSpinBoxNum)

            if self.ui.checkBox_Ft.isEnabled():
                self.ui.checkBox_FT.clicked.connect(self.checkBox_FT_clicked)

            self.ui.checkBox_circuit.clicked.connect(self.checkBox_circuit_clicked)
            self.ui.checkBox_lap.clicked.connect(self.checkBox_lap_clicked)

            #初始化
            self.ComboBox_Shadow_clicked()
            self.userNameBefore=self.ui.LineEdit_Name.text()  
            #用于判断是否进行名称更新
            self.flagUpdateItemName=False

            # 适配分辨率
            from Physics.PhysicsCommand import AdaptiveDPIUtil
            new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
            self.resize(500, new_y)

        except:
            import traceback
            sayz("error:" + traceback.format_exc())
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
        pass

    def reporterrors(self):
        laplace_text1 = self.ui.ComboBox_lap1.currentText()
        laplace_text2 = self.ui.ComboBox_lap2.currentText()
        if laplace_text1 == '未指定' or laplace_text2 == '未指定':
            report = QtGui.QMessageBox()
            report.setText(u'拉普拉斯不可以未指定')
            report.exec_()
         
    def refreshCombox(self):
        # 这里存储的应该就是下拉的表格
        ComboBox_Shadow_list=[]
        ComboBox_lap1_list=[]
        ComboBox_lap2_list=[]
        ComboBox_lap3_list=[]
        ComboBox_lap4_list=[]
        ComboBox_lap5_list=[]
        ComboBox_FT_list=[]
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_lap1.count()):
            ComboBox_lap1_list.append(self.ui.ComboBox_lap1.itemText(i))
        for i in range(self.ui.ComboBox_lap2.count()):
            ComboBox_lap2_list.append(self.ui.ComboBox_lap2.itemText(i))
        for i in range(self.ui.ComboBox_lap3.count()):
            ComboBox_lap3_list.append(self.ui.ComboBox_lap3.itemText(i))
        for i in range(self.ui.ComboBox_lap4.count()):
            ComboBox_lap4_list.append(self.ui.ComboBox_lap4.itemText(i))
        for i in range(self.ui.ComboBox_lap5.count()):
            ComboBox_lap5_list.append(self.ui.ComboBox_lap5.itemText(i))
        for i in range(self.ui.ComboBox_FT.count()):
            ComboBox_FT_list.append(self.ui.ComboBox_FT.itemText(i))
        Orthogonal_list = DocumentTools.getActiveDocTypes("Area_Conformal")
        Orthogonal_list.append("OSYS$MIDPLANE1")
        Orthogonal_list.append("OSYS$MIDPLANE2")
        Orthogonal_list.append("OSYS$MIDPLANE3")

        for i in Orthogonal_list:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
        # 拉普拉斯下拉框添加正投影体选项
        volumeList = DocumentTools.getConductorVols()
        for i in volumeList:
            if i not in ComboBox_lap1_list:
                self.ui.ComboBox_lap1.addItem(i)   
            if i not in ComboBox_lap2_list:
                self.ui.ComboBox_lap2.addItem(i)    
            if i not in ComboBox_lap3_list:
                self.ui.ComboBox_lap3.addItem(i)  
            if i not in ComboBox_lap4_list:
                self.ui.ComboBox_lap4.addItem(i)  
            if i not in ComboBox_lap5_list:
                self.ui.ComboBox_lap5.addItem(i)                        
        # # 线上电压归一化添加线选项
        # lineList 是端口面里的内容
        lineList = DocumentTools.getActiveDocTypes("Line_Conformal")
        #这里的就是下拉栏里的名称
        for i in lineList:
            if i not in ComboBox_FT_list:
                self.ui.ComboBox_FT.addItem(i)

    # 点击取消按钮关闭窗口
    def onCancel(self):
        self.close()

    # 点击确定按钮
    def onConfirm(self):
        self.keepData()
        self.close()


    def loadData(self):
        try:             
            self.ui.LineEdit_Name.setText(self.obj.Name)
            # 设置标记的旧名字
            self.userNameBefore = self.obj.Name
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.orthogonalProjectionPlane)))
            self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            self.ui.LineEdit_start_y.setText(self.obj.point1_Y)
            self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
            # 法向选择
            self.ui.radioButton_x.setChecked(self.obj.isCheckNormal1)
            self.ui.radioButton_y.setChecked(self.obj.isCheckNormal2)
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
            # ciucuit输入时间
            self.ui.checkBox_circuit.setEnabled(self.obj.isCircuit)
            self.ui.checkBox_circuit.setChecked(self.obj.isCircuit)
            self.ui.LineEdit_circuit.setEnabled(self.obj.isCircuit)
            self.ui.lineEdit_obs.setEnabled(self.obj.isCircuit)
            self.ui.label_obs.setEnabled(self.obj.isCircuit)
            self.ui.LineEdit_circuit.setText(self.obj.circuit)
            self.ui.lineEdit_obs.setText(self.obj.observeName)

            # 拉普拉斯
            self.ui.checkBox_lap.setChecked(self.obj.isCheckLapras)
            self.ui.ComboBox_lap1.setEnabled(self.obj.isCheckLapras)
            self.ui.ComboBox_lap2.setEnabled(self.obj.isCheckLapras)
            # 添加拉普拉斯的内容 
            self.ui.spinBox.setEnabled(self.obj.isCheckLapras)
            self.ui.spinBox_2.setEnabled(self.obj.isCheckLapras)
            try:
                self.ui.spinBox_num.setValue(int(self.obj.laprasNumbers))
            except:
                # FreeCAD.Console.PrintError('\n\n\n'+'port laplace_num is wrong!!!\n\n')
                pass

            self.ui.ComboBox_lap1.setCurrentIndex(self.ui.ComboBox_lap1.findText(str(self.obj.lapras1)))
            self.ui.ComboBox_lap2.setCurrentIndex(self.ui.ComboBox_lap2.findText(str(self.obj.lapras2)))
            self.ui.ComboBox_lap3.setCurrentIndex(self.ui.ComboBox_lap3.findText(str(self.obj.lapras3)))
            self.ui.ComboBox_lap4.setCurrentIndex(self.ui.ComboBox_lap4.findText(str(self.obj.lapras4)))
            self.ui.ComboBox_lap5.setCurrentIndex(self.ui.ComboBox_lap5.findText(str(self.obj.lapras5)))
            self.ui.spinBox.setValue(int(self.obj.lapras1Value))
            self.ui.spinBox_2.setValue(int(self.obj.lapras2Value)) 
            self.ui.spinBox_3.setValue(int(self.obj.lapras3Value)) 
            self.ui.spinBox_4.setValue(int(self.obj.lapras4Value)) 
            self.ui.spinBox_5.setValue(int(self.obj.lapras5Value))

            self.checkBox_lap_clicked()
            # 法向选择
            if self.obj.isCheckNormal1:
                self.ui.radioButton_x.setChecked(True)
                self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
                self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
            if self.obj.isCheckNormal2:
                self.ui.radioButton_y.setChecked(True)
                self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
                self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")

            # 正向反向选择
            if self.obj.isNegative == True:
                self.ui.radioButton_opposite.setChecked(True)
            if self.obj.isPositive == True:
                self.ui.radioButton_forward.setChecked(True)

        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))

    # 保存数据
    def keepData(self): 
        try:
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
            self.obj.isCheckNormal2 = not(self.obj.isCheckNormal1)     

            # 正向反向选择
            self.obj.isNegative = self.ui.radioButton_opposite.isChecked()           
            self.obj.isPositive = self.ui.radioButton_forward.isChecked()

            # DX编辑框
            self.obj.isMarkX = self.ui.checkBox_x.isChecked()
            self.obj.isMarkY = self.ui.checkBox_y.isChecked()

            self.obj.MarkX = self.ui.LineEdit_DX1.text()
            self.obj.MarkX = self.ui.LineEdit_DX2.text()
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
            # if self.ui.radioButton_x.isChecked():
            #     DlgData.addData("geFirstName","GE2")
            #     DlgData.addData("geSecondName","GE3")
            # if self.ui.radioButton_y.isChecked():   
            #     DlgData.addData("geFirstName","GE1")
            #     DlgData.addData("geSecondName","GE3")
            # if self.ui.radioButton_z.isChecked():
            #     DlgData.addData("geFirstName","GE1")
            #     DlgData.addData("geSecondName","GE2")  
            # DlgData.addData("geFirstVal",self.ui.LineEdit_GE2.toPlainText())
            # DlgData.addData("geSecondVal",self.ui.LineEdit_GE3.toPlainText())
            # DlgData.addData("GE2", self.ui.LineEdit_GE2.toPlainText())
            # DlgData.addData("GE3", self.ui.LineEdit_GE3.toPlainText())

            # 线上电压归一化
            self.obj.isCheckNormalization = self.ui.checkBox_FT.isChecked()
            # 如果线上归一化下拉框选择的是portName.Line,则设置为True，代表需要新建一个conformal线
            # DlgData.addData("isNewConformalLine", self.ui.ComboBox_FT.currentIndex()==0)
            self.obj.normalization = self.ui.ComboBox_FT.currentText()
            # ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_FT.currentText())
            # circuit输入时间
            self.obj.isCircuit = self.ui.checkBox_circuit.isChecked()             
            self.obj.circuit = self.ui.LineEdit_circuit.text()
            self.obj.observeName = self.ui.lineEdit_obs.text().replace(' ','')
            # 拉普拉斯1
            self.obj.isCheckLapras = self.ui.checkBox_lap.isChecked()    
            # 拉普拉斯2
            self.obj.lapras1 = self.ui.ComboBox_lap1.currentText() 
            self.obj.lapras2 = self.ui.ComboBox_lap2.currentText()
            self.obj.lapras3 = self.ui.ComboBox_lap3.currentText()
            self.obj.lapras4 = self.ui.ComboBox_lap4.currentText()
            self.obj.lapras5 = self.ui.ComboBox_lap5.currentText()
            # 添加拉普拉斯的内容 
            self.obj.lapras1Value = self.ui.spinBox.value()
            self.obj.lapras2Value = self.ui.spinBox_2.value()  
            self.obj.lapras3Value = self.ui.spinBox_3.value() 
            self.obj.lapras4Value = self.ui.spinBox_4.value() 
            self.obj.lapras5Value = self.ui.spinBox_5.value() 
            self.obj.laprasNumbers = self.ui.spinBox_num.value() 
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass


    # 正交投影面下拉列表
    def ComboBox_Shadow_clicked(self):
        # FreeCAD.Console.PrintError('\n进入下拉框点击函数\n')
        ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentIndex())
        # FreeCAD.Console.PrintError('\n下拉框点击第一条命令\n')
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setEnabled(False)
            self.LineEdit_Name_textChanged()
            # 起点可编辑
            self.ui.LineEdit_start_x.setEnabled(True)
            self.ui.LineEdit_start_y.setEnabled(True)
            self.ui.LineEdit_start_z.setEnabled(True)
            if self.ui.radioButton_x.isChecked() == True:
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
            if self.ui.radioButton_y.isChecked() == True:
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(True)
            if self.ui.radioButton_z.isChecked() == True:
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.radioButton_x.setEnabled(True)
            self.ui.radioButton_y.setEnabled(True)
            self.ui.radioButton_z.setEnabled(True)
        else:
            # FreeCAD.Console.PrintError('\n下拉框当前值不为0！！！\n')
            # 线上电压归一化可选
            
            self.ui.ComboBox_FT.setEnabled(True)
            # 如果选择了投影面，则线的名字跟随投影面
            self.ui.ComboBox_FT.setItemText(0, self.ui.ComboBox_Shadow.currentText() + ".LINE")
            
            # 正交投影面
            objName = self.ui.ComboBox_Shadow.currentText()
            if objName in self.defaultValue:
                pass
            else:
                # 获得面的相关数据
                modelData = DocumentTools.getValueOfAreaObjByLable(objName)
                self.ui.LineEdit_start_x.setText(str(modelData[1]) )
                self.ui.LineEdit_start_y.setText(str(modelData[2]))
                self.ui.LineEdit_start_z.setText(str(modelData[3]))
                self.ui.LineEdit_end_x.setText(str(modelData[4]))
                self.ui.LineEdit_end_y.setText(str(modelData[5]))
                self.ui.LineEdit_end_z.setText(str(modelData[6]))
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_start_z.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
                # 法向
                if modelData[7] == 1:
                    self.ui.radioButton_x.setChecked(True)
                    self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
                    self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
                elif modelData[7] == 2:
                    self.ui.radioButton_y.setChecked(True)
                    self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
                    self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
                elif modelData[7] == 3:
                    self.ui.radioButton_z.setChecked(True)
                    self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
                    self.ui.checkBox_GE3.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
                elif modelData[7] == 0:
                    FreeCAD.Console.PrintMessage("get Area_Conformal error")
            self.ui.LineEdit_start_x.setEnabled(False)
            self.ui.LineEdit_start_y.setEnabled(False)
            self.ui.LineEdit_start_z.setEnabled(False)
            self.ui.LineEdit_end_x.setEnabled(False)
            self.ui.LineEdit_end_y.setEnabled(False)
            self.ui.LineEdit_end_z.setEnabled(False)
            self.ui.radioButton_x.setEnabled(False)
            self.ui.radioButton_y.setEnabled(False)
            self.ui.radioButton_z.setEnabled(False)

    # 当portname修改时，如果没有选择投影面，对应修改线上电压归一化对应的线名
    # （如果选择了投影面则线名和面名一致）# 根据要求将线上电压归一化的线名改成面名
    def LineEdit_Name_textChanged(self):
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            self.ui.ComboBox_FT.setItemText(0, self.ui.LineEdit_Name.text() + ".LINE")

    # x法向修改时，修改起点即修改终点
    def LineEdit_start_x_textChanged(self):
        if not self.ui.LineEdit_end_x.isEnabled():
            self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())

    # y法向修改时，修改起点即修改终点
    def LineEdit_start_y_textChanged(self):
        if not self.ui.LineEdit_end_y.isEnabled():
            self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())

    # z法向修改时，修改起点即修改终点
    def LineEdit_start_z_textChanged(self):
        if not self.ui.LineEdit_end_z.isEnabled():
            self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())

    # 点击法向x按钮
    def radioButton_x_clicked(self):
        self.ui.LineEdit_end_x.setEnabled(False)
        self.ui.LineEdit_end_x.setText(self.ui.LineEdit_start_x.text())
        self.ui.LineEdit_end_y.setEnabled(True)
        self.ui.LineEdit_end_z.setEnabled(True)
        self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
        self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")

    # 点击法向y按钮
    def radioButton_y_clicked(self):
        self.ui.LineEdit_end_y.setEnabled(False)
        self.ui.LineEdit_end_y.setText(self.ui.LineEdit_start_y.text())
        self.ui.LineEdit_end_x.setEnabled(True)
        self.ui.LineEdit_end_z.setEnabled(True)
        self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
        self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")

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
        self.ui.LineEdit_GE2.setEnabled(self.ui.checkBox_GE2.isChecked())
        self.ui.LineEdit_GE2.setEnabled(self.ui.checkBox_GE2.isChecked())
        self.ciucuit_function()
        

    # 空间分布2
    def checkBox_GE3_clicked(self):
        self.ui.LineEdit_GE3.setEnabled(self.ui.checkBox_GE3.isChecked())
        self.ui.LineEdit_GE3.setEnabled(self.ui.checkBox_GE3.isChecked())
        self.ciucuit_function()

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

    # 拉普拉斯
    def checkBox_lap_clicked(self):
        self.ui.ComboBox_lap1.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.ComboBox_lap2.setEnabled(self.ui.checkBox_lap.isChecked())

        self.ui.spinBox.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.spinBox_2.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.spinBox_num.setEnabled(self.ui.checkBox_lap.isChecked())
        self.setSpinBoxNum()


   

