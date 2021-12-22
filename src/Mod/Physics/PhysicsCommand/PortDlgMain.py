# -*- coding: utf-8 -*-
# 解决Port端口设置问题，方案1：修改DlgData数据，将Ft_checked设为true,Ft+设为Orthogonal_projection_surface的值
import FreeCAD
from PySide import QtGui
import Physics.PhysicsGui.PortDlg
import Simulation
from DlgData import DlgData, sayz,getDlgData
from Modeling.Common.Tools import DocumentTools,ObjectsTools,Completer
import BoundPalMain
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
import json
from PhysicsTools import CompleterTools,SetColorTools
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
from Modeling.Common.Tools.PhysicsDialog import *
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0

def show(type,className,itemUserName):
    FreeCAD.Console.PrintMessage("ClassNameshow:  "+str(className)+"\n") 
    FreeCAD.Console.PrintMessage("ClassNameshow:  "+str(className)+"\n") 

    global  ObjectDict  
    if type == "new":
        ObjectDict[className] = PortMain("new",className)
        ObjectDict[className].setModal(False)
        ObjectDict[className].setModal(False)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    #同样是点击修改面板，为什么这里直接进入1但是其他有些面板同样的操作进入的却是2？如emh
    elif type == "old":
        #1
        if className in ObjectDict.keys():
            # 增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
            JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
            oldData = DlgData(JSON_CADComment[itemUserName], itemUserName)
            ObjectDict[className].loadData(oldData)

            # FreeCAD.Console.PrintError('\n程序进入打开dialog\n')
            ObjectDict[className].refreshCombox()
            # FreeCAD.Console.PrintError('\n已经刷新好下拉框\n')
            ObjectDict[className].ComboBox_Shadow_clicked()
            # FreeCAD.Console.PrintError('\n下拉框点击完毕\n')
            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
        #2           
        else:
            ObjectDict[className] = PortMain(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  

class PortMain(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.PortDlg.Ui_Dialog_PortDlg()
        self.ui.setupUi(self)
        # CompleterTools.setLineEditsCompleter([self.ui.LineEdit_Name])
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        # FreeCAD.Console.PrintMessage("port")
        # FreeCAD.Console.PrintMessage(self.ui.LineEdit_start_x.parent())
        # self.ui.LineEdit_start_x=Completer.AutoCompleteEdit(self.ui.groupBox_Port)
        # self.ui.LineEdit_start_x.setcompleterlist(["DX1","DX2","DX3"])
        # FreeCAD.Console.PrintMessage(self.ui.LineEdit_start_x)
        self.defaultValue = ["OSYS$MIDPLANE1","OSYS$MIDPLANE2","OSYS$MIDPLANE3"]
        global flag
        flag = 0
        # FreeCAD.Console.PrintMessage(isinstance(getattr(self.ui,"LineEdit_Name"),QtGui.QLineEdit))
        self.ui.radioButton_forward.setChecked(True)
        # 再打开Dialog的时候就设置一次输入框的个数
        # self.setSpinBoxNum()

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
        self.ui.pushButton.clicked.connect(self.onCancel)
        self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)

        # 当portname被修改时触发函数修改归一化名字
        # 注意这里
        self.ui.LineEdit_Name.textChanged.connect(self.LineEdit_Name_textChanged)

        self.ui.LineEdit_start_x.textChanged.connect(self.LineEdit_start_x_textChanged)
        self.ui.LineEdit_start_y.textChanged.connect(self.LineEdit_start_y_textChanged)
        self.ui.LineEdit_start_z.textChanged.connect(self.LineEdit_start_z_textChanged)

        self.ui.radioButton_x.clicked.connect(self.radioButton_x_clicked)
        self.ui.radioButton_y.clicked.connect(self.radioButton_y_clicked)
        self.ui.radioButton_z.clicked.connect(self.radioButton_z_clicked)

        self.ui.checkBox_x.clicked.connect(self.checkBox_x_clicked)
        self.ui.checkBox_y.clicked.connect(self.checkBox_y_clicked)
        self.ui.checkBox_z.clicked.connect(self.checkBox_z_clicked)

        self.ui.checkBox_vport.clicked.connect(self.checkBox_vport_clicked)
        self.ui.checkBox_scale.clicked.connect(self.checkBox_scale_clicked)
        self.ui.checkBox_Ft.clicked.connect(self.checkBox_Ft_clicked)
        self.ui.checkBox_GE2.clicked.connect(self.checkBox_GE2_clicked)
        self.ui.checkBox_GE3.clicked.connect(self.checkBox_GE3_clicked)
        # 拉普拉斯设置数量出现变化时，相应的修改界面下拉框的数量 @lizhenguang
        self.ui.spinBox_num.valueChanged.connect(self.setSpinBoxNum)

        if self.ui.checkBox_Ft.isEnabled():
            self.ui.checkBox_FT.clicked.connect(self.checkBox_FT_clicked)

        self.ui.checkBox_circuit.clicked.connect(self.checkBox_circuit_clicked)
        self.ui.checkBox_lap.clicked.connect(self.checkBox_lap_clicked)

        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        # 添加一个报错指引功能 @ lizhenguang
        # self.ui.pushButton_ok.clicked.connect(self.reporterrors)
        # self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className))
        self.initDialog(JSON_CADComment,className)

        FreeCAD.Console.PrintMessage("DialogID: "+str(DialogID)+"\n")
        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            self.loadData(oldData)            
            flag = 1  
        #初始化
        self.ComboBox_Shadow_clicked()
        ######################################这里是在wzj学弟的基础上进行bug修复################################
        # 这里主要修改的bug是分支树上修改面板后，json数据不是修改而是叠加，并且点击取消按钮以后，再次打开应该是保持json里面的数据内容
        # 这里 self.userNameBefore是为了防止修改名称后，丢失原来的名称信息，所以记录下了修改之前的名称
        #      flagUpdateItemName是标志是否为修改数据的标志位，True表示是从“修改数据”进入到改编版的,反之亦反
        #      updateItemName 函数是更新当前选中的item的text变为ui的name,因为在选择“修改数据”后，该item肯定是被选中状态的。
        self.userNameBefore=self.ui.LineEdit_Name.text()  
        #用于判断是否进行名称更新
        self.flagUpdateItemName=False

        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(500, new_y)
    #  @lizhenguang
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
        # print "调试从这里开始\n"
        # print Orthogonal_list
        # print "调试到这里结束\n"
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
        # if self.flagUpdateItemName:
        #     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #     oldData = DlgData(JSON_CADComment[self.userNameBefore], self.userNameBefore)
        #     self.loadData(oldData)
        self.close()

    # 点击确定按钮
    def onConfirm(self,FreeCAD_Comment_Dict,className):
        FreeCAD.Console.PrintError('\n执行到此处111')
        objName = self.ui.ComboBox_Shadow.currentText()
        if objName in self.defaultValue:
            pass
        else:
            #设置颜色
            SetColorTools.setColor(self.ui.ComboBox_Shadow.currentText(),physicsType="Port")

        laplace_text1 = self.ui.ComboBox_lap1.currentText()
        laplace_text2 = self.ui.ComboBox_lap2.currentText()
        laplace_text3 = self.ui.ComboBox_lap3.currentText()
        laplace_text4 = self.ui.ComboBox_lap4.currentText()
        laplace_text5 = self.ui.ComboBox_lap5.currentText()
        laplace_num = int(self.ui.spinBox_num.value())
        if self.ui.checkBox_lap.isChecked():
            if laplace_num == 2:
                if laplace_text1 == '未指定' or laplace_text2 == '未指定':
                    report = QtGui.QMessageBox()
                    report.setText(u'拉普拉斯不可以未指定')
                    report.exec_()
                    return
            if laplace_num == 3:
                # FreeCAD.Console.PrintError(str(laplace_num)+'\n\n\n')
                if laplace_text1 == '未指定' or laplace_text2 == '未指定' or laplace_text3 == '未指定':
                    # FreeCAD.Console.PrintError(str(laplace_num)+'\n\n\n')
                    report = QtGui.QMessageBox()
                    report.setText(u'拉普拉斯不可以未指定')
                    report.exec_()
                    return
            if laplace_num == 4:
                if laplace_text1 == '未指定' or laplace_text2 == '未指定' or laplace_text3 == '未指定' or laplace_text4 == '未指定':
                    report = QtGui.QMessageBox()
                    report.setText(u'拉普拉斯不可以未指定')
                    report.exec_()
                    return
            if laplace_num == 5:
                if laplace_text1 == '未指定' or laplace_text2 == '未指定' or laplace_text3 == '未指定' \
                    or laplace_text4 == '未指定' or laplace_text5 == '未指定':
                    report = QtGui.QMessageBox()
                    report.setText(u'拉普拉斯不可以未指定')
                    report.exec_()
                    return
        oldJson = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        # 存储只修改数据而没有修改item名的情况
        oldData = ["modify", self.userNameBefore, className]
        itemData = ["modify", self.userNameBefore, className]
        FreeCAD.Console.PrintError('\n执行到此处222')
        global flag
        count = 1
        #这个name必须确保唯一性！！！
        #也就是他的窗口编辑框里面的值
        name = self.ui.LineEdit_Name.text() 
        self.close()
        if flag == 0:
            while name in FreeCAD_Comment_Dict.keys():
               name = self.ui.LineEdit_Name.text() + str(count)
               count+=1
            self.ui.LineEdit_Name.setText(name)
            itemData, oldData = BoundPalMain.addItem(u"波导端口", name, className)
            flag = 1
        #防止修改名称使得json重复
        if self.flagUpdateItemName:
            # FreeCAD.Console.PrintError('修改名称')
            if not name == self.userNameBefore:
                JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
                if self.userNameBefore in JSON_CADComment:
                    JSON_CADComment.pop(self.userNameBefore)
                    FreeCAD.ActiveDocument.Begin = json.dumps(JSON_CADComment)
                    # 判断更新的名称是否有重名
                    while name in FreeCAD_Comment_Dict.keys():
                        name = self.ui.LineEdit_Name.text() + str(count)
                        count += 1
                    #更新名称
                    # if self.flagUpdateItemName:
                    itemData, oldData = BoundPalMain.updateItemName(name)
                    self.flagUpdateItemName=False
        self.userNameBefore=name
        FreeCAD.Console.PrintError('\n执行到此处333')
        newData = DlgData({},name)
        isModify = self.keepData(newData)
        FreeCAD.Console.PrintError('\n执行到加载完数据')

        if isModify and itemData is not None:
            jsonData = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)

            # 更新两个栈
            record = [jsonData, itemData, oldJson, oldData]
            DoManager.newOperation(record)

        # 更新m3d文档 by mx
        # 获得m3d的util
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        # 获得最近的m3d字符串
        # FreeCAD.Console.PrintError('213123123123123123123123')
        FileStr = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)

    # 加载数据


    def loadData(self,DlgData):
        # 要找的似乎在DlgData中，对其进行遍历
        # print "\n"
        # for key, value in DlgData.data.items():
        #     print key , " corresponds to " , DlgData.data[key]
        #     print "\n"
        # FreeCAD.Console.PrintError('\n\n\n'+'port load data starting\n\n')
        try:               
            self.ui.LineEdit_Name.setText(DlgData.data['name'])
            # 设置标记的旧名字
            self.userNameBefore = DlgData.data['name']
            FreeCAD.Console.PrintError('\n'+str(DlgData.data['Orthogonal_projection_surface'])+'\n')
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(DlgData.data['Orthogonal_projection_surface']))
            self.ui.LineEdit_start_x.setText(DlgData.data['start_R'])
            self.ui.LineEdit_start_y.setText(DlgData.data['start_Y'])
            self.ui.LineEdit_start_z.setText(DlgData.data['start_Z'])
            self.ui.LineEdit_end_x.setText(DlgData.data['end_R'])
            self.ui.LineEdit_end_y.setText(DlgData.data['end_Y'])
            self.ui.LineEdit_end_z.setText(DlgData.data['end_Z'])
            # DX编辑框
            self.ui.checkBox_x.setChecked(DlgData.data['DX_R_Checked'])  
            self.checkBox_x_clicked()
            self.ui.checkBox_y.setChecked(DlgData.data['DX_Y_Checked'])
            self.checkBox_y_clicked()
            self.ui.checkBox_z.setChecked(DlgData.data['DX_Z_Checked'])
            self.checkBox_z_clicked()
            self.ui.LineEdit_DX1.setText(DlgData.data['DX_R'])
            self.ui.LineEdit_DX2.setText(DlgData.data['DX_Y'])
            self.ui.LineEdit_DX3.setText(DlgData.data['DX_Z'])            
            # 相对加速比
            self.ui.checkBox_vport.setChecked(DlgData.data['vport_Checked'])
            self.ui.LineEdit_vport.setEnabled(DlgData.data['vport_Checked'])
            self.ui.LineEdit_vport.setText(DlgData.data['vport'])            
            # 法向修正
            self.ui.checkBox_scale.setChecked(DlgData.data['scale_Checked'])
            self.ui.LineEdit_scale.setEnabled(DlgData.data['scale_Checked'])
            self.ui.LineEdit_scale.setText(DlgData.data['scale'])
            # 输入场时间分布
            sayz("DlgData.data['Ft_Checked']")
            sayz(DlgData.data['Ft_Checked'])
            self.ui.checkBox_Ft.setChecked(DlgData.data['Ft_Checked'])
            self.ui.LineEdit_Ft.setEnabled(DlgData.data['Ft_Checked'])             
            self.ui.LineEdit_Ft.setText(DlgData.data['Ft'])            
            # 空间分布2
            self.ui.checkBox_GE2.setChecked(DlgData.data['GE2_Checked'])
            self.ui.LineEdit_GE2.setEnabled(DlgData.data['GE2_Checked'])
            self.ui.LineEdit_GE2.setText(DlgData.data['GE2'])
            # 空间分布3
            self.ui.checkBox_GE3.setChecked(DlgData.data['GE3_Checked'])
            self.ui.LineEdit_GE3.setEnabled(DlgData.data['GE3_Checked'])
            self.ui.LineEdit_GE3.setText(DlgData.data['GE3'])
            # 线上电压归一化
            # print "调试从此开始\n"
            self.ui.checkBox_FT.setChecked(DlgData.data['FT_Checked'])
            # print self.ui.checkBox_FT.setChecked(DlgData.data['FT_Checked']),"\n"
            self.ui.checkBox_FT.setEnabled(DlgData.data['FT_Checked'])
            # print self.ui.checkBox_FT.setEnabled(DlgData.data['FT_Checked']),"\n"
            self.ui.checkBox_FT.setEnabled(DlgData.data['Ft_Checked'])
            # print self.ui.checkBox_FT.setEnabled(DlgData.data['Ft_Checked']),"\n"
            # print "调试到此结束\n"
            # 当端口面为未指定的时候，默认线是否也得是未指定
            if DlgData.data['Orthogonal_projection_surface'] == u"未指定":
                self.ui.ComboBox_FT.setCurrentIndex(0)
            else:
                # 修改这一部分代码，检查DlgData.data['FT+']是否是端口面名，如果是不是的话加入该项
                if DlgData.data['FT+']==DlgData.data['Orthogonal_projection_surface']+'.LINE':
                    self.ui.ComboBox_FT.setCurrentIndex(self.ui.ComboBox_FT.findText(DlgData.data['FT+']))
                else:
                    # 方案一如果二者不一致，则加入该项并设为当前项
                    # print "有执行\n"
                    # self.ui.ComboBox_FT.addItem(DlgData.data['Orthogonal_projection_surface']+'.LINE')
                    # self.ui.ComboBox_FT.setCurrentIndex(self.ui.ComboBox_FT.findText(DlgData.data['FT+']+'.LINE'))
                    # 方案二，将第0项设为端口面名+‘.LINE’
                    self.ui.ComboBox_FT.setItemText(0, DlgData.data['Orthogonal_projection_surface']+".LINE")
                    # self.ui.ComboBox_FT.setCurrentIndex(self.ui.ComboBox_FT.findText(DlgData.data['Orthogonal_projection_surface']+".LINE"))
                    FreeCAD.Console.PrintError("FT+"+str(DlgData.data['FT+'])+"\n")
                    self.ui.ComboBox_FT.setCurrentIndex(self.ui.ComboBox_FT.findText(DlgData.data['FT+']))


            # FreeCAD.Console.PrintError('\n\n\n'+'port load data done at circuit!!!\n\n')
            # ciucuit输入时间
            self.ui.checkBox_circuit.setEnabled(DlgData.data['circuit_Checked'])
            self.ui.checkBox_circuit.setChecked(DlgData.data['circuit_Checked'])
            self.ui.LineEdit_circuit.setEnabled(DlgData.data['circuit_Checked'])
            self.ui.lineEdit_obs.setEnabled(DlgData.data['circuit_Checked'])
            self.ui.label_obs.setEnabled(DlgData.data['circuit_Checked'])
            self.ui.LineEdit_circuit.setText(DlgData.data['circuit'])
            self.ui.lineEdit_obs.setText(DlgData.data['observe_name'])

            # 拉普拉斯
            self.ui.checkBox_lap.setChecked(DlgData.data['lap_Checked'])
            self.ui.ComboBox_lap1.setEnabled(DlgData.data['lap_Checked'])
            self.ui.ComboBox_lap2.setEnabled(DlgData.data['lap_Checked'])
            # 添加拉普拉斯的内容 @lizhenguang
            self.ui.spinBox.setEnabled(DlgData.data['lap_Checked'])
            self.ui.spinBox_2.setEnabled(DlgData.data['lap_Checked'])
            # @lizhenguang
            try:
                self.ui.spinBox_num.setValue(int(DlgData.data['Laplace_num']))
            except:
                # FreeCAD.Console.PrintError('\n\n\n'+'port laplace_num is wrong!!!\n\n')
                pass
            # FreeCAD.Console.PrintError('\n\n\n'+'port load data done at laplace!!!\n\n')

            self.ui.ComboBox_lap1.setCurrentIndex(self.ui.ComboBox_lap1.findText(DlgData.data['Laplace1']))  
            self.ui.ComboBox_lap2.setCurrentIndex(self.ui.ComboBox_lap2.findText(DlgData.data['Laplace2']))
            self.ui.ComboBox_lap3.setCurrentIndex(self.ui.ComboBox_lap3.findText(DlgData.data['Laplace3']))
            self.ui.ComboBox_lap4.setCurrentIndex(self.ui.ComboBox_lap4.findText(DlgData.data['Laplace4']))
            self.ui.ComboBox_lap5.setCurrentIndex(self.ui.ComboBox_lap5.findText(DlgData.data['Laplace5']))
            # FreeCAD.Console.PrintError('\n\n\n'+'port load data done at laplace num !!!\n\n')
            self.ui.spinBox.setValue(int(DlgData.data['Laplace1_number']))
            self.ui.spinBox_2.setValue(int(DlgData.data['Laplace2_number'])) 
            self.ui.spinBox_3.setValue(int(DlgData.data['Laplace3_number'])) 
            self.ui.spinBox_4.setValue(int(DlgData.data['Laplace4_number'])) 
            self.ui.spinBox_5.setValue(int(DlgData.data['Laplace5_number'])) 

            self.checkBox_lap_clicked()
            # FreeCAD.Console.PrintError('\n\n\n'+'port load data done at lzg!!!\n\n')
            # 法向选择
            if DlgData.data['normal'] == "R":
                self.ui.radioButton_x.setChecked(True)
                self.ui.checkBox_GE2.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")
                self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
            if DlgData.data['normal'] == "theta":
                self.ui.radioButton_y.setChecked(True)
                self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
                self.ui.checkBox_GE3.setText(u"空间分布.GE3(" + self.x + "," + self.y + "," + self.z + ") = ")
            if DlgData.data['normal'] == "Z":
                self.ui.radioButton_z.setChecked(True)
                self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
                self.ui.checkBox_GE3.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")

            # 正向反向选择
            if DlgData.data['direction'] == "NEGATIVE":
                self.ui.radioButton_opposite.setChecked(True)
            if DlgData.data['direction'] == "POSITIVE":
                self.ui.radioButton_forward.setChecked(True)
            # FreeCAD.Console.PrintError('\n\n\n'+'port load data done\n\n')

        except KeyError as reason:
            sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason))

    # 保存数据
    def keepData(self,DlgData): 
        DlgData.addData("name",DlgData.id)
        DlgData.addData("Orthogonal_projection_surface",self.ui.ComboBox_Shadow.currentText())
        if self.ui.ComboBox_Shadow.currentIndex() == 0: 
            DlgData.addData("isAppointArea",False)            
        else:
            # if ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_Shadow.currentText()):
            #     FreeCAD.Console.PrintMessage("OKEY\n")
            # else:
            #     FreeCAD.Console.PrintMessage("NO\n")
            DlgData.addData("isAppointArea",True)
        DlgData.addData("Dlg_Type","Port_Type")
        DlgData.addData("start_R",self.ui.LineEdit_start_x.text())
        DlgData.addData("start_Y",self.ui.LineEdit_start_y.text())
        DlgData.addData("start_Z",self.ui.LineEdit_start_z.text())        
        DlgData.addData("end_R",self.ui.LineEdit_end_x.text())
        DlgData.addData("end_Y",self.ui.LineEdit_end_y.text())
        DlgData.addData("end_Z",self.ui.LineEdit_end_z.text())

        # 法向选择
        if self.ui.radioButton_x.isChecked():             
            DlgData.addData("normal","R")
        if self.ui.radioButton_y.isChecked():             
            DlgData.addData("normal","theta")
        if self.ui.radioButton_z.isChecked():             
            DlgData.addData("normal","Z")

        # 正向反向选择
        if self.ui.radioButton_opposite.isChecked():            
            DlgData.addData("direction","NEGATIVE")
        if self.ui.radioButton_forward.isChecked():
            DlgData.addData("direction","POSITIVE")

        # DX编辑框
        DlgData.addData("DX_R_Checked",self.ui.checkBox_x.isChecked())
        DlgData.addData("DX_Y_Checked",self.ui.checkBox_y.isChecked())
        DlgData.addData("DX_Z_Checked",self.ui.checkBox_z.isChecked())

        DlgData.addData("DX_R",self.ui.LineEdit_DX1.text())
        DlgData.addData("DX_Y",self.ui.LineEdit_DX2.text())
        DlgData.addData("DX_Z",self.ui.LineEdit_DX3.text())

        # 相对加速比
        DlgData.addData("vport_Checked",self.ui.checkBox_vport.isChecked())        
        DlgData.addData("vport",self.ui.LineEdit_vport.text())        

        # 法向修正
        DlgData.addData("scale_Checked",self.ui.checkBox_scale.isChecked())        
        DlgData.addData("scale",self.ui.LineEdit_scale.text())        

        # 输入场时间分布
        DlgData.addData("Ft_Checked",self.ui.checkBox_Ft.isChecked())
        DlgData.addData("Ft",self.ui.LineEdit_Ft.toPlainText())

        # 空间分布
        DlgData.addData("GE2_Checked",self.ui.checkBox_GE2.isChecked())
        DlgData.addData("GE3_Checked",self.ui.checkBox_GE3.isChecked())
        if self.ui.radioButton_x.isChecked():
            DlgData.addData("geFirstName","GE2")
            DlgData.addData("geSecondName","GE3")
        if self.ui.radioButton_y.isChecked():   
            DlgData.addData("geFirstName","GE1")
            DlgData.addData("geSecondName","GE3")
        if self.ui.radioButton_z.isChecked():
            DlgData.addData("geFirstName","GE1")
            DlgData.addData("geSecondName","GE2")  
        DlgData.addData("geFirstVal",self.ui.LineEdit_GE2.toPlainText())
        DlgData.addData("geSecondVal",self.ui.LineEdit_GE3.toPlainText())
        DlgData.addData("GE2", self.ui.LineEdit_GE2.toPlainText())
        DlgData.addData("GE3", self.ui.LineEdit_GE3.toPlainText())

        # 线上电压归一化
        DlgData.addData("FT_Checked",self.ui.checkBox_FT.isChecked())
        # 如果线上归一化下拉框选择的是portName.Line,则设置为True，代表需要新建一个conformal线
        DlgData.addData("isNewConformalLine", self.ui.ComboBox_FT.currentIndex()==0)
        DlgData.addData("FT+", self.ui.ComboBox_FT.currentText())
        FreeCAD.Console.PrintMessage("ComboBox_FT:"+str(self.ui.ComboBox_FT.currentText())+"\n")
        ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_FT.currentText())
        # circuit输入时间
        DlgData.addData("circuit_Checked",self.ui.checkBox_circuit.isChecked())              
        DlgData.addData("circuit",self.ui.LineEdit_circuit.text())
        DlgData.addData("observe_name",self.ui.lineEdit_obs.text().replace(' ',''))

        # 拉普拉斯1
        DlgData.addData("lap_Checked",self.ui.checkBox_lap.isChecked())           
        DlgData.addData("Laplace1",self.ui.ComboBox_lap1.currentText())
        # 添加拉普拉斯的内容 @lizhenguang
        

        # 拉普拉斯2
        DlgData.addData("Laplace2",self.ui.ComboBox_lap2.currentText())
        DlgData.addData("Laplace3",self.ui.ComboBox_lap3.currentText())
        DlgData.addData("Laplace4",self.ui.ComboBox_lap4.currentText())
        DlgData.addData("Laplace5",self.ui.ComboBox_lap5.currentText())
        # 添加拉普拉斯的内容 @lizhenguang
        DlgData.addData("Laplace1_number",self.ui.spinBox.value())
        DlgData.addData("Laplace2_number",self.ui.spinBox_2.value())  
        DlgData.addData("Laplace3_number",self.ui.spinBox_3.value()) 
        DlgData.addData("Laplace4_number",self.ui.spinBox_4.value()) 
        DlgData.addData("Laplace5_number",self.ui.spinBox_5.value()) 
        DlgData.addData("Laplace_num",self.ui.spinBox_num.value()) 
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        # FreeCAD.Console.PrintError(Comment)
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0
        
    # 正交投影面下拉列表
    def ComboBox_Shadow_clicked(self):
        # FreeCAD.Console.PrintError('\n进入下拉框点击函数\n')
        ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentIndex())
        # FreeCAD.Console.PrintError('\n下拉框点击第一条命令\n')
        if self.ui.ComboBox_Shadow.currentIndex() == 0:
            # FreeCAD.Console.PrintError('\n下拉框当前值为0\n')
            # 即若投影面未指定则线上电压不可选
            # 线上电压归一化不可选
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
            #objName为现在的投影面名称
            # FreeCAD.Console.PrintError('\n推测此处出现问题111\n')
            objName = self.ui.ComboBox_Shadow.currentText()
            if objName in self.defaultValue:
                pass
            else:
                # 获得面的相关数据
                modelData = DocumentTools.getValueOfAreaObjByLable(objName)
            # 起点与止点坐标
            # self.ui.LineEdit_start_x.setText(str(modelData[1]) '''+ self.x_unit''')
            # self.ui.LineEdit_start_y.setText(str(modelData[2])''' + self.y_unit''')
            # self.ui.LineEdit_start_z.setText(str(modelData[3]) '''+ self.z_unit''')
            # self.ui.LineEdit_end_x.setText(str(modelData[4]) '''+ self.x_unit''')
            # self.ui.LineEdit_end_y.setText(str(modelData[5])''' + self.y_unit''')
            # self.ui.LineEdit_end_z.setText(str(modelData[6])''' + self.z_unit''')
                self.ui.LineEdit_start_x.setText(str(modelData[1]) )
                self.ui.LineEdit_start_y.setText(str(modelData[2]))
                self.ui.LineEdit_start_z.setText(str(modelData[3]))
                self.ui.LineEdit_end_x.setText(str(modelData[4]))
                self.ui.LineEdit_end_y.setText(str(modelData[5]))
                self.ui.LineEdit_end_z.setText(str(modelData[6]))
                # FreeCAD.Console.PrintError('\n推测此处出现问题222\n')
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
    #     print "有执行\n"
    #     Orthogonal_list = DocumentTools.getActiveDocTypes("Area_Conformal")
    #     print self.ui.checkBox_FT.
    #     print Orthogonal_list
    #     if Orthogonal_list[0] not in self.ui.ComboBox_FT.itemText():
    #         self.ui.ComboBox_FT.setItemText(0, Orthogonal_list[0] + ".LINE")
    #         print Orthogonal_list[0]

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

    # 点击法向z按钮
    def radioButton_z_clicked(self):
        self.ui.LineEdit_end_z.setEnabled(False)
        self.ui.LineEdit_end_z.setText(self.ui.LineEdit_start_z.text())
        self.ui.LineEdit_end_x.setEnabled(True)
        self.ui.LineEdit_end_y.setEnabled(True)
        self.ui.checkBox_GE2.setText(u"空间分布.GE1(" + self.x + "," + self.y + "," + self.z + ") = ")
        self.ui.checkBox_GE3.setText(u"空间分布.GE2(" + self.x + "," + self.y + "," + self.z + ") = ")

    # 非均匀网格x
    def checkBox_x_clicked(self): 
        self.ui.LineEdit_DX1.setEnabled(self.ui.checkBox_x.isChecked())

    # 非均匀网格y
    def checkBox_y_clicked(self):
        self.ui.LineEdit_DX2.setEnabled(self.ui.checkBox_y.isChecked())

    # 非均匀网格z
    def checkBox_z_clicked(self):
        self.ui.LineEdit_DX3.setEnabled(self.ui.checkBox_z.isChecked())

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
            # else:
            #     self.ui.checkBox_circuit.setChecked(False)
            #     self.ui.checkBox_circuit.setEnabled(False)
            #     self.ui.LineEdit_circuit.setEnabled(False)
            #     self.ui.label_obs.setEnabled(False)
            #     self.ui.lineEdit_obs.setEnabled(False)
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
        # self.ui.checkBox_circuit.setEnabled(self.ui.checkBox_FT.isChecked())
        # 当正投影面不是未指定时，才可选择正投影线
        if self.ui.ComboBox_Shadow.currentIndex() != 0:
            self.ui.ComboBox_FT.setEnabled(self.ui.checkBox_FT.isChecked())

        # self.ui.ComboBox_FT.setItemText(0, self.ui.ComboBox_Shadow.currentIndex()+".LINE")
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
        # self.ui.ComboBox_lap3.setEnabled(self.ui.checkBox_lap.isChecked())
        # self.ui.ComboBox_lap4.setEnabled(self.ui.checkBox_lap.isChecked())
        # self.ui.ComboBox_lap5.setEnabled(self.ui.checkBox_lap.isChecked())

        self.ui.spinBox.setEnabled(self.ui.checkBox_lap.isChecked())
        self.ui.spinBox_2.setEnabled(self.ui.checkBox_lap.isChecked())
        # self.ui.spinBox_3.setEnabled(self.ui.checkBox_lap.isChecked())
        # self.ui.spinBox_4.setEnabled(self.ui.checkBox_lap.isChecked())
        # self.ui.spinBox_5.setEnabled(self.ui.checkBox_lap.isChecked())

        self.ui.spinBox_num.setEnabled(self.ui.checkBox_lap.isChecked())
        # FreeCAD.Console.PrintError('\n\n\n'+'port load data done at 11111!!!\n\n')
        self.setSpinBoxNum()
        # FreeCAD.Console.PrintError('\n\n\n'+'port load data done at 222222!!!\n\n')
      
#我这里拥有数几个面板的数据--该怎么传给M呢？

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)

