#-*- coding: utf-8 -*-
import json

import FreeCAD
import PySide
from PySide import QtGui,QtCore
from ProjectSettingGui.NewMaterial import NewMaterialDlg
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import ProjectSettingCommand
from ProjectSettingsDlgData import ProjectSettingsDlgData as DlgData
import ProjectSettingsDlgData

import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from Physics.PhysicsCommand import BoundPalMain
from Physics.PhysicsCommand import DoManager
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
flag = 0

def show(type,className,itemUserName):
    # 被树结构的双击事件调用
    FreeCAD.Console.PrintMessage("ClassNameshow:  "+str(className)+"\n") 
    FreeCAD.Console.PrintMessage("ClassNameshow:  "+str(itemUserName)+"\n") 

    if type == "new":
        ObjectDict[className] = NewMaterial("new",className)
        ObjectDict[className].setModal(False)
        ObjectDict[className].show()
        ObjectDict[className].exec_()
    elif type == "old":
        if className in ObjectDict.keys():
            # 增加了撤销操作后，数据可能发生变化，所以每次需要重新加载数据，
            JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
            oldData = DlgData(JSON_CADComment[itemUserName], itemUserName)
            # oldData=JSON_CADComment[itemUserName]
            ObjectDict[className].loadData(oldData)

            ObjectDict[className].flagUpdateItemName=True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()             
        else:
            ObjectDict[className] = NewMaterial(itemUserName,className)
            ObjectDict[className].flagUpdateItemName = True
            ObjectDict[className].setNameUnable()
            ObjectDict[className].setModal(False)
            ObjectDict[className].show()
            ObjectDict[className].exec_()
    

class NewMaterial(QtGui.QDialog):
    def __init__(self,DialogID,className):
        QtGui.QDialog.__init__(self)
        self.ui = NewMaterialDlg.Ui_Dialog_NewMaterialDlg()
        self.ui.setupUi(self)
        global flag
        flag = 0
        from ProjectSetting.Tools import CompleterTools
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        self.ui.pushButton.clicked.connect(self.pushBtn_Cancel)
        self.ui.checkBox_conductivity.clicked.connect(self.onCheckBox_conductivityClicked)
        self.ui.checkBox_dielectric_constant.clicked.connect(self.onCheckBox_dielectric_constantClicked)
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        self.ui.pushButton_ok.clicked.connect(lambda: self.pushBtn_OK(JSON_CADComment,className))
        # if className in JSON_CADComment:
        #     oldData=JSON_CADComment[className]
        #     self.loadData(oldData)
        if DialogID != "new":
            # oldData = DlgData(JSON_CADComment[className])
            oldData = DlgData(JSON_CADComment[DialogID],DialogID)
            self.loadData(oldData)
            flag = 1
        self.onCheckBox_conductivityClicked()
        self.onCheckBox_dielectric_constantClicked()
        self.userNameBefore=self.ui.lineEdit_Name.text()
        self.flagUpdateItemName = False
        # if self.ui.checkBox_conductivity.checkState==PySide.QtCore.Qt.CheckState.Checked:
        #     self.ui.lineEdit_conductivity.setReadOnly(False)
        # else:
        #     self.ui.lineEdit_conductivity.setReadOnly(True)
        # if self.ui.checkBox_dielectric_constant.checkState==PySide.QtCore.Qt.CheckState.Checked:
        #     self.ui.lineEdit_dielectric_constant.setReadOnly(False)
        # else:
        #     self.ui.lineEdit_dielectric_constant.setReadOnly(True)

    def pushBtn_OK(self,FreeCAD_Comment_Dict,className):
        self.close()
        # ProjectSettingsDlgData.getDlgData()
        oldJson = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        # 存储只修改数据而没有修改item名的情况
        oldData = ["modify", self.userNameBefore, className]
        itemData = ["modify", self.userNameBefore, className]
        # 将新材料添加到边界设置的树里面去，因为新材料需要设置很多个 @lizhenguang
        count = 1
        global flag
        name = self.ui.lineEdit_Name.text()
        if flag == 0:
            # name_list = []
            # for i in range(len(FreeCAD_Comment_Dict.keys())):
            #     try:
            #         name_list.append(FreeCAD_Comment_Dict["NewMaterical"+str(i)]['name'])
            #     except:
            #         pass
            #     while name in name_list:
            #         name = self.ui.lineEdit_Name.text() + str(count)
            #         count+=1
            # self.ui.lineEdit_Name.setText(name)
            # itemData, oldData=BoundPalMain.addItem(u"新材料", name, className)
            # flag = 1
            while name in FreeCAD_Comment_Dict.keys(): 
               name = self.ui.lineEdit_Name.text() + str(count) 
               count+=1       
            self.ui.lineEdit_Name.setText(name)
            itemData, oldData = BoundPalMain.addItem(u"新材料", name, className)
            flag = 1
        # BoundPalMain.updateItemName(name)
        #防止修改名称使得json重复
        if self.flagUpdateItemName:
            FreeCAD.Console.PrintError('修改名称')
            if not name == self.userNameBefore:
                JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
                if self.userNameBefore in JSON_CADComment:
                    JSON_CADComment.pop(self.userNameBefore)
                    FreeCAD.ActiveDocument.Comment = json.dumps(JSON_CADComment)
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
        isModify = self.keepData(newData,name)
        if isModify and itemData is not None:
            jsonData = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)

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
        pass
    def pushBtn_Cancel(self):
        self.close()
        pass
    def loadData(self,DlgData):
        try:
            self.userNameBefore = DlgData.data['name']
            self.ui.lineEdit_Name.setText(DlgData.data["name"])
            self.ui.lineEdit_atomic_number.setText(DlgData.data["ato_num"])
            self.ui.lineEdit_atomic_mass_number.setText(DlgData.data["ato_mass_num"])
            self.ui.lineEdit_atomic_desity.setText(DlgData.data["ato_desity"])
            self.ui.lineEdit_conductivity.setText(DlgData.data["conductivity"])
            self.ui.lineEdit_dielectric_constant.setText(DlgData.data["dielectric_constant"])
            if DlgData.data["checkBox_conductivity"]:
                self.ui.checkBox_conductivity.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_conductivity.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
            if DlgData.data["checkBox_dielectric_constant"]:
                self.ui.checkBox_dielectric_constant.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_dielectric_constant.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
        except KeyError as reson:
            FreeCAD.Console.PrintMessage(str(reson))
    def keepData(self,DlgData,className): 
        DlgData.addData("Dlg_Type", "NewMaterical")
        DlgData.addData("name",self.ui.lineEdit_Name.text())
        DlgData.addData("ato_num",self.ui.lineEdit_atomic_number.text())
        DlgData.addData("ato_mass_num",self.ui.lineEdit_atomic_mass_number.text())
        DlgData.addData("ato_desity",self.ui.lineEdit_atomic_desity.text())
        DlgData.addData("conductivity",self.ui.lineEdit_conductivity.text())
        DlgData.addData("dielectric_constant",self.ui.lineEdit_dielectric_constant.text())
        FreeCAD.Console.PrintMessage( self.ui.checkBox_conductivity.checkState())
        if self.ui.checkBox_conductivity.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("checkBox_conductivity",True)
        else:
            DlgData.addData("checkBox_conductivity",False)
        if self.ui.checkBox_dielectric_constant.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("checkBox_dielectric_constant",True)
        else:
            DlgData.addData("checkBox_dielectric_constant",False)
        Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        old = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        Comment[className] = DlgData.data
        # Comment["NewMaterical"] = DlgData.data
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)
        # 返回面板中的内容是否改变
        return cmp(old, Comment) != 0
    
    def onCheckBox_conductivityClicked(self):
        self.ui.lineEdit_conductivity.setEnabled(self.ui.checkBox_conductivity.isChecked()) 
    def onCheckBox_dielectric_constantClicked(self):
        self.ui.lineEdit_dielectric_constant.setEnabled(self.ui.checkBox_dielectric_constant.isChecked()) 

    def setNameUnable(self):
        self.ui.lineEdit_Name.setEnabled(False)