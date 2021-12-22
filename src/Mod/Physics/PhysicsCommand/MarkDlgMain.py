#-*- coding: utf-8 -*-
import Physics.PhysicsGui.MarkDlg
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
        ObjectDict[className] = MarkShow("new",className)
        ObjectDict[className].setModal(False)
        
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    #同样是点击修改面板，为什么这里直接进入1但是其他有些面板同样的操作进入的却是2？如emh
    elif type == "old":
        FreeCAD.Console.PrintError('\n进入到old')
        #1
        if className in ObjectDict.keys():
            FreeCAD.Console.PrintError('\n进入到 1111')
            # 增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
            JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
            oldData = DlgData(JSON_CADComment[itemUserName], itemUserName)
            ObjectDict[className].loadData(oldData)
            FreeCAD.Console.PrintError('\n加载完数据')

            # FreeCAD.Console.PrintError('\n程序进入打开dialog\n')
            ObjectDict[className].refreshCombox()
            # FreeCAD.Console.PrintError('\n已经刷新好下拉框\n')
            # ObjectDict[className].ComboBox_Shadow_clicked()
            # FreeCAD.Console.PrintError('\n下拉框点击完毕\n')
            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
        #2           
        else:
            ObjectDict[className] = MarkShow(className,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
    pass
class MarkShow(PhysicsDialog):
    def __init__(self,DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.MarkDlg.Ui_Dialog()
        self.ui.setupUi(self)
        #代码补全  调整ui文件后再取消注释
        # self.defaultValue = ["OSYS$VOLUME"]
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        global flag
        flag = 0
        # 链接信号与槽
        self.ui.pushButton_cancel.clicked.connect(self.onCancel)
        # 加载json ok键绑定的槽在initDialog里面
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className))
        # self.initDialog(JSON_CADComment,className)
        self.refreshCombox()
        
        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            # Em_loadData(self.ui,oldData,"EMH_TYPE")    
            self.loadData(oldData)      
            flag = 1 
        # Merge对话框没有名称
        self.userNameBefore=className
        #用于判断是否进行名称更新
        self.flagUpdateItemName=False
        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(500, new_y)

    def onCancel(self):
        self.close()

    # 点击确定按钮
    def onConfirm(self,FreeCAD_Comment_Dict,className):
        FreeCAD.Console.PrintError("\n进入Merge的确定函数")
        oldJson = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        # 存储只修改数据而没有修改item名的情况
        oldData = ["modify", self.userNameBefore, className]
        itemData = ["modify", self.userNameBefore, className]
        global flag 
        count = 1
        name = className    
        self.close() 
        # FreeCAD.Console.PrintError("\n执行完merge的关闭部分")
        if flag == 0:              
            while name in FreeCAD_Comment_Dict.keys(): 
               name = name + str(count) 
               count+=1       
            # self.ui.lineEdit_name.setText(name)
            itemData, oldData = BoundPalMain.addItem(u"MARK", name, className)
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

    def keepData(self, DlgData):
        DlgData.addData("name", DlgData.id)
        DlgData.addData("Dlg_Type", "Mark_Type")
        DlgData.addData("mark_obj",self.ui.comboBox_obj.currentText())
        DlgData.addData("direction", self.ui.comboBox_x.currentText())
        DlgData.addData("isChecked_min", self.ui.checkBox_min.isChecked())
        DlgData.addData("isChecked_mid", self.ui.checkBox_mid.isChecked())
        DlgData.addData("isChecked_max", self.ui.checkBox_max.isChecked())
        DlgData.addData("size", self.ui.lineEdit_size.text())
        # 此处添加className是为了解决className混乱的问题，于Simlation的相关类的Activated调用 @lzg
        DlgData.addData("className", DlgData.id)

        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[DlgData.id] = DlgData.data
        # FreeCAD.Console.PrintError(Comment)
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0
    def loadData(self, DlgData):
        try:
            self.userNameBefore = DlgData.data['name']
            self.ui.comboBox_obj.setCurrentIndex(self.ui.comboBox_obj.findText(DlgData.data["mark_obj"]))
            self.ui.comboBox_x.setCurrentIndex(self.ui.comboBox_x.findText(DlgData.data['direction']))
            self.ui.checkBox_min.setChecked(DlgData.data["isChecked_min"])
            self.ui.checkBox_mid.setChecked(DlgData.data["isChecked_mid"])
            self.ui.checkBox_max.setChecked(DlgData.data["isChecked_max"])
            self.ui.lineEdit_size.setText(DlgData.data["size"])
        except:
            pass

    def refreshCombox(self):  
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_list=[]
        for i in range(self.ui.comboBox_obj.count()):
            ComboBox_list.append(self.ui.comboBox_obj.itemText(i))
        MarkList = DocumentTools.getAllObjs()
        for i in MarkList:
            if i not in ComboBox_list:
                self.ui.comboBox_obj.addItem(i)

