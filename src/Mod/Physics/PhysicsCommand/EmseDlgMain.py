#-*- coding: utf-8 -*-
import Physics.PhysicsGui.EmseDlg
from PySide import QtGui
import json
import FreeCAD
from DlgData import DlgData, sayz, getDlgData
from Modeling.Common.Tools import DocumentTools,ObjectsTools
import BoundPalMain
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from PhysicsTools import CompleterTools
from Modeling.Common.Tools.PhysicsDialog import *
import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0

def show(type,className,itemUserName):
    #具体内容需要再添加
    FreeCAD.Console.PrintMessage("ClassNameshow:  "+str(className)+"\n") 
    FreeCAD.Console.PrintMessage("ClassNameshow:  "+str(className)+"\n") 

    global  ObjectDict  
    if type == "new":
        ObjectDict[className] = EmseShow("new",className)
        ObjectDict[className].setModal(False)
        ObjectDict[className].setModal(False)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    #同样是点击修改面板，为什么这里直接进入1但是其他有些面板同样的操作进入的却是2？如emh
    elif type == "old":
        FreeCAD.Console.PrintError('\n进入到old')
        #1
        if className in ObjectDict.keys():
            # 增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
            FreeCAD.Console.PrintError('\n进入old  1\n')
            JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
            oldData = DlgData(JSON_CADComment[itemUserName], itemUserName)
            ObjectDict[className].loadData(oldData)

            FreeCAD.Console.PrintError('\nclassName:  '+str(className)+'\nitemUserName:  '+ str(itemUserName))
            ObjectDict[className].refreshCombox()
            ObjectDict[className].setEnable()
            # FreeCAD.Console.PrintError('\n已经刷新好下拉框\n')
            # ObjectDict[className].ComboBox_Shadow_clicked()
            # FreeCAD.Console.PrintError('\n下拉框点击完毕\n')
            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
        #2           
        else:
            FreeCAD.Console.PrintError('\nclassName:  '+str(className)+'\nitemUserName:  '+ str(itemUserName))
            ObjectDict[className] = EmseShow(itemUserName,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
    pass

class EmseShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.EmseDlg.Ui_Dialog()
        self.ui.setupUi(self)
        #代码补全  调整ui文件后再取消注释
        # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        global flag
        flag = 0
        
        # 链接信号与槽
        self.ui.pushButton_cancel.clicked.connect(self.onCancel)
        self.ui.checkBox_4.clicked.connect(self.setEnable)
        self.ui.checkBox_5.clicked.connect(self.setEnable)
        self.ui.checkBox_6.clicked.connect(self.setEnable)
        # 加载json ok键绑定的槽在initDialog里面
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        self.initDialog(JSON_CADComment,className)
        # 刷新下拉框
        self.refreshCombox()
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)  
        self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)) 
        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            # Em_loadData(self.ui,oldData,"EMH_TYPE") 
            # FreeCAD.Console.PrintError('\noldData'+str(JSON_CADComment[DialogID]))   
            self.loadData(oldData)      
            flag = 1 
        
        self.setEnable()
        self.userNameBefore=self.ui.lineEdit_name.text()
        # 用于判断是否进行名称更新
        self.flagUpdateItemName=False
        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(500, new_y)
    def setEnable(self):
        if self.ui.checkBox_6.isChecked():
            self.ui.lineEdit_WF.setEnabled(True)
        else:
            self.ui.lineEdit_WF.setEnabled(False)
        if self.ui.checkBox_5.isChecked():
            self.ui.lineEdit_ED.setEnabled(True)
            self.ui.lineEdit_energyMax.setEnabled(True)
            self.ui.lineEdit_energyMin.setEnabled(True)
        else:
            self.ui.lineEdit_ED.setEnabled(False)
            self.ui.lineEdit_energyMax.setEnabled(False)
            self.ui.lineEdit_energyMin.setEnabled(False)
        if self.ui.checkBox_4.isChecked():
            self.ui.lineEdit_AD.setEnabled(True)
        else:
            self.ui.lineEdit_AD.setEnabled(False)


    def onCancel(self):
        # if self.flagUpdateItemName:
        #     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #     oldData = DlgData(JSON_CADComment[self.userNameBefore],self.userNameBefore)
        #     Em_loadData(self.ui,oldData,"EMH_TYPE")
        self.close()

    # 点击确定按钮
    def onConfirm(self,FreeCAD_Comment_Dict,className):
        FreeCAD.Console.PrintError("\n进入EmSE的确定函数")
        oldJson = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        # 存储只修改数据而没有修改item名的情况
        oldData = ["modify", self.userNameBefore, className]
        itemData = ["modify", self.userNameBefore, className]
        global flag 
        count = 1
        name = self.ui.lineEdit_name.text()    
        self.close() 
        FreeCAD.Console.PrintError("\n执行完EmSE的关闭部分")
        if flag == 0:              
            while name in FreeCAD_Comment_Dict.keys(): 
               name = self.ui.lineEdit_name.text() + str(count) 
               count+=1       
            self.ui.lineEdit_name.setText(name)
            itemData, oldData = BoundPalMain.addItem(u"发射处理", name, className)
            flag = 1
        #防止修改名称使得json重复
        if self.flagUpdateItemName:
            if not name == self.userNameBefore:
                JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
                if self.userNameBefore in JSON_CADComment:
                    JSON_CADComment.pop(self.userNameBefore)
                    FreeCAD.ActiveDocument.Begin = json.dumps(JSON_CADComment)
                    # 判断更新的名称是否有重名
                    while name in FreeCAD_Comment_Dict.keys():
                        name = self.ui.lineEdit_name.text() + str(count)
                        count += 1
                    #更新名称
                    # if self.flagUpdateItemName:
                    itemData, oldData = BoundPalMain.updateItemName(name)
                    self.flagUpdateItemName=False
        FreeCAD.Console.PrintError("\n执行完防止名称重复部分")
        # FreeCAD.Console.PrintError(name)
        self.userNameBefore=name
        newData = DlgData({},name)
        isModify = self.keepData(newData)
        FreeCAD.Console.PrintError("\n执行完加载数据部分")
        if isModify and itemData is not None:
            jsonData = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)

            # 更新两个栈
            record = [jsonData, itemData, oldJson, oldData]
            DoManager.newOperation(record)

        # 更新m3d文档 by mx
        # 获得m3d的util
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        # 获得最近的m3d字符串
        FileStr = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)
        FreeCAD.Console.PrintError("\n执行完整个确定部分")
    
    def keepData(self,DlgData):
        DlgData.addData("name",DlgData.id)
        DlgData.addData("Dlg_Type","EmSE_Type")
        DlgData.addData("energy_sec",self.ui.lineEdit_energy.text())
        DlgData.addData("max_num_sec",self.ui.lineEdit_maxNum.text())
        DlgData.addData("WEIGHT_FACTOR",self.ui.lineEdit_WF.text())
        DlgData.addData("ENERGY_DISTRIBUTION",self.ui.lineEdit_ED.text())
        DlgData.addData("min_energy",self.ui.lineEdit_energyMin.text())
        DlgData.addData("max_energy",self.ui.lineEdit_energyMax.text())
        DlgData.addData("ANGLE_DISTRIBUTION",self.ui.lineEdit_AD.text())
        DlgData.addData("isCheck_WF",self.ui.checkBox_6.isChecked())
        DlgData.addData("isCheck_ED",self.ui.checkBox_5.isChecked())
        DlgData.addData("isCheck_AD",self.ui.checkBox_4.isChecked())
        # 有新添加了五个变量
        DlgData.addData("notInclude1",self.ui.ComboBox_notInclued.currentText())
        DlgData.addData("notInclude2",self.ui.ComboBox_notIncludedd.currentText())
        DlgData.addData("include1",self.ui.ComboBox_included.currentText())
        DlgData.addData("include2",self.ui.ComboBox_includedd.currentText())
        DlgData.addData("Emitter",self.ui.ComboBox_Shadow.currentText())

        if self.ui.ComboBox_Shadow.currentText() == u'未指定':
            DlgData.addData("isEmit",False)
        else:
            ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_Shadow.currentText())
            DlgData.addData("isEmit",True)

        if self.ui.ComboBox_notInclued.currentText() == u'不指定':
            DlgData.addData("isExclude1",False)
        else:
            DlgData.addData("isExclude1",True)
            ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_notInclued.currentText())

        if self.ui.ComboBox_notIncludedd.currentText() == u'不指定':
            DlgData.addData("isExclude2",False)
        else:
            DlgData.addData("isExclude2",True)
            ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_notIncludedd.currentText())

        if self.ui.ComboBox_included.currentText() == u'不指定':
            DlgData.addData("isInclude1",False)
        else:
            DlgData.addData("isInclude1",True)
            ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_included.currentText())

        if self.ui.ComboBox_includedd.currentText() == u'不指定':
            DlgData.addData("isInclude2",False)
        else:
            DlgData.addData("isInclude2",True)
            ObjectsTools.findObjByLabelWithoutOrderAndInvisible(self.ui.ComboBox_includedd.currentText())

        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        # FreeCAD.Console.PrintError(Comment)
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0

    def loadData(self,DlgData):
        try:
            self.ui.lineEdit_name.setText(DlgData.data["name"])
            self.ui.lineEdit_energy.setText(DlgData.data["energy_sec"])
            self.ui.lineEdit_maxNum.setText(DlgData.data["max_num_sec"])
            self.ui.lineEdit_WF.setText(DlgData.data["WEIGHT_FACTOR"])
            self.ui.lineEdit_ED.setText(DlgData.data["ENERGY_DISTRIBUTION"])
            self.ui.lineEdit_energyMin.setText(DlgData.data["min_energy"])
            self.ui.lineEdit_energyMax.setText(DlgData.data["max_energy"])
            self.ui.lineEdit_AD.setText(DlgData.data["ANGLE_DISTRIBUTION"])
            self.ui.checkBox_6.setChecked(DlgData.data["isCheck_WF"])
            self.ui.checkBox_5.setChecked(DlgData.data["isCheck_ED"])
            self.ui.checkBox_4.setChecked(DlgData.data["isCheck_AD"])
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(DlgData.data['Emitter']))
            # FreeCAD.Console.PrintError('\n设置ComboBox_Shadow\n'+str(self.ui.ComboBox_Shadow.findText(DlgData.data['Emitter'])))
            # FreeCAD.Console.PrintError(DlgData.data['Emitter'])
            # 发射区域选项
            self.ui.ComboBox_notInclued.setCurrentIndex(self.ui.ComboBox_notInclued.findText(DlgData.data['notInclude1']))
            self.ui.ComboBox_notIncludedd.setCurrentIndex(self.ui.ComboBox_notIncludedd.findText(DlgData.data['notInclude2']))
            self.ui.ComboBox_included.setCurrentIndex(self.ui.ComboBox_included.findText(DlgData.data['include1']))
            self.ui.ComboBox_includedd.setCurrentIndex(self.ui.ComboBox_includedd.findText(DlgData.data['include2']))
        except :
            FreeCAD.Console.PrintError('\n加载数据失败')
            # sayz("!!!Error:KeyError,Maybe lack of key:%s"%str(reason)
            pass
        pass
    def refreshCombox(self):  
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list=[]
        ComboBox_area_list=[]
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_notInclued.count()):
            ComboBox_area_list.append(self.ui.ComboBox_notInclued.itemText(i))
        EmmiterList = DocumentTools.getAllVols()
        EmmiterList.append("OSYS$VOLUME")
        VolumeListAll = DocumentTools.getActiveDocTypes("Vol_Conformal",False)
        for i in EmmiterList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
        for i in VolumeListAll:
            if i not in ComboBox_area_list:
                self.ui.ComboBox_notInclued.addItem(i)  
                self.ui.ComboBox_notIncludedd.addItem(i) 
                self.ui.ComboBox_included.addItem(i) 
                self.ui.ComboBox_includedd.addItem(i)

    def setNameUnable(self):
        self.ui.lineEdit_name.setEnabled(False)
