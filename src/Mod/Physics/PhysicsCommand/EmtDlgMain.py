#-*- coding: utf-8 -*-
import Physics.PhysicsGui.EmtDlg
from PySide import QtGui
import json
import FreeCAD
from DlgData import DlgData, sayz, Em_keepData, Em_loadData,getDlgData

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
    if type == "new":
        ObjectDict[className] = EmtShow("new",className)
        ObjectDict[className].setModal(False)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    elif type == "old":
        if className in ObjectDict.keys():
            # 增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
            JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
            oldData = DlgData(JSON_CADComment[itemUserName], itemUserName)
            Em_loadData(ObjectDict[className].ui, oldData, "EMT_TYPE")
            # 设置标记的旧名字
            ObjectDict[className].userNameBefore = oldData.data['name']

            ObjectDict[className].refreshCombox()
            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()             
        else:
            ObjectDict[className] = EmtShow(itemUserName,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()  
        
class EmtShow(PhysicsDialog):
    def __init__(self, DialogID,className,parent=None):
        PhysicsDialog.__init__(self, parent)
        self.ui = Physics.PhysicsGui.EmtDlg.Ui_Dialog_EmtDlg()
        self.ui.setupUi(self)
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        global flag
        flag = 0
        self.ui.pushButton.clicked.connect(self.onCancel)
        self.ui.checkBox_particleType.clicked.connect(self.checkBox_particleType_clicked)
        self.ui.checkBox_generationRate.clicked.connect(self.checkBox_generationRate_clicked)
        self.ui.checkBox_transmittingInterval.clicked.connect(self.checkBox_transmittingInterval_clicked)
        self.ui.checkBox_surface.clicked.connect(self.checkBox_surface_clicked)
        self.ui.checkBox_outSurface.clicked.connect(self.checkBox_outSurface_clicked)

        self.ui.ComboBox_Shadow.currentIndexChanged.connect(lambda:self.ComboBox_changed("ComboBox_Shadow"))
        self.ui.ComboBox_included.currentIndexChanged.connect(lambda:self.ComboBox_changed("ComboBox_included"))
        self.ui.ComboBox_includedd.currentIndexChanged.connect(lambda:self.ComboBox_changed("ComboBox_includedd"))
        self.ui.ComboBox_notIncludedd.currentIndexChanged.connect(lambda:self.ComboBox_changed("ComboBox_notIncludedd"))
        self.ui.ComboBox_notInclued.currentIndexChanged.connect(lambda:self.ComboBox_changed("ComboBox_notInclued"))
        # 刷新下拉框
        self.refreshCombox()
        # 加载每个Project都具有的Comment【里面存储着对话框的所有数据】----》JSON对象----》应用于加载窗口
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)  

        # self.ui.pushButton_ok.clicked.connect(lambda: self.onConfirm(JSON_CADComment,className)) 
        self.initDialog(JSON_CADComment,className)

        if DialogID != "new":
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            Em_loadData(self.ui,oldData,"EMT_TYPE")          
            flag = 1 
        self.userNameBefore=self.ui.LineEdit_Name.text()
                #用于判断是否进行名称更新
        self.flagUpdateItemName=False

        # 适配分辨率
        import AdaptiveDPIUtil
        new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
        self.resize(500, new_y)
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

    # 点击ok按钮确认
    def onConfirm(self,FreeCAD_Comment_Dict,className):
        oldJson = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        # 存储只修改数据而没有修改item名的情况
        oldData = ["modify", self.userNameBefore, className]
        itemData = ["modify", self.userNameBefore, className]
        global flag 
        count = 1
        name = self.ui.LineEdit_Name.text()    
        self.close() 
        if flag == 0:              
            while name in FreeCAD_Comment_Dict.keys(): 
               name = self.ui.LineEdit_Name.text() + str(count) 
               count+=1       
            self.ui.LineEdit_Name.setText(name)
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
                        name = self.ui.LineEdit_Name.text() + str(count)
                        count += 1
                    #更新名称
                    # if self.flagUpdateItemName:
                    itemData, oldData = BoundPalMain.updateItemName(name)
                    self.flagUpdateItemName=False
        self.userNameBefore=name
        newData = DlgData({},name)
        isModify = Em_keepData(self.ui,newData,"EMT_TYPE")
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


    # 点击取消按钮关闭窗口 
            # 点击取消按钮关闭窗口
    def onCancel(self):
        # if self.flagUpdateItemName:
        #     JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        #     oldData = DlgData(JSON_CADComment[self.userNameBefore],self.userNameBefore)
        #     Em_loadData(self.ui,oldData,"EME_TYPE")
        self.close()

    def checkBox_particleType_clicked(self):
        self.ui.ComboBox_particleType.setEnabled(self.ui.checkBox_particleType.isChecked())
    def checkBox_generationRate_clicked(self):
        self.ui.spinBox_generationRate.setEnabled(self.ui.checkBox_generationRate.isChecked())
    def checkBox_transmittingInterval_clicked(self):
        self.ui.radioButton_random.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.radioButton_strictTiming.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.spinBox_timesStep.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
    def checkBox_surface_clicked(self):
        self.ui.radioButton_randomm.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_uniform.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_fixed.setEnabled(self.ui.checkBox_surface.isChecked())
    def checkBox_outSurface_clicked(self):
        self.ui.radioButton_randommm.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.radioButton_alongOutsideFixed.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.LineEdit_Dn.setEnabled(self.ui.checkBox_outSurface.isChecked())

    def ComboBox_changed(self,which):
        if which=="ComboBox_Shadow":
            ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
        elif which=="ComboBox_included":
            ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_included.currentText())
            pass
        elif which=="ComboBox_includedd":
            ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_includedd.currentText())
            pass
        elif which=="ComboBox_notIncludedd":
            ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_notIncludedd.currentText())
            pass
        elif which=="ComboBox_notInclued":
            ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_notInclued.currentText())
            pass

    def setNameUnable(self):
        self.ui.LineEdit_Name.setEnabled(False)