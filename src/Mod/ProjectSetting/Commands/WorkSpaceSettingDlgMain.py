#-*- coding: utf-8 -*-
import json

import FreeCAD
from PySide import QtGui
from ProjectSettingGui.WorkSpaceSettings import WorkSpaceSettingsDlg
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import ProjectSettingCommand
from ProjectSettingsDlgData import ProjectSettingsDlgData as DlgData
import ProjectSettingsDlgData
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from Modeling.Common.Tools import ObjectsTools

#json格式数据需要保持原有顺序输出
from collections import OrderedDict

# class WorkSpaceSettings(QtGui.QDialog):
#     def __init__(self):
#         QtGui.QDialog.__init__(self)
#         self.ui=WorkSpaceSettingsDlg.Ui_Dialog_WorkSpaceDlg()
#         self.ui.setupUi(self)
#         # print self.data
        
#         self.ui.pushButton_ok.clicked.connect(self.pushBtn_OK)
#         self.ui.pushButton.clicked.connect(self.pushBtn_Cancel)
#         # self.ui.pushButton.clicked.connect(self.pushBtn_Cancel)
#         self.initData()

#     def initData(self):
#         # 获取当前坐标系及坐标系单位
#         coord = ProjectSettingCommand.getCooedinate()
#         self.x = coord[0]
#         self.y = coord[1]
#         self.z = coord[2]
#         self.x_unit = coord[3]
#         self.y_unit = coord[4]
#         self.z_unit = coord[5]

#         self.ui.groupBox_WorkSpace_X.setTitle(self.x)
#         self.ui.groupBox_WorkSpace_Y.setTitle(self.y)
#         self.ui.groupBox_WorkSpace_Z.setTitle(self.z)

#         self.ui.lineEdit_Name.setText(ProjectSettingsDlgData.data["name"])
#         self.ui.LineEdit_start_x.setText(ProjectSettingsDlgData.data["start_x"])
#         self.ui.LineEdit_end_x.setText(ProjectSettingsDlgData.data["end_x"])
#         self.ui.LineEdit_stride_x.setText(ProjectSettingsDlgData.data["stride_x"])
#         self.ui.LineEdit_start_y.setText(ProjectSettingsDlgData.data["start_y"])
#         self.ui.LineEdit_end_y.setText(ProjectSettingsDlgData.data["end_y"])
#         self.ui.LineEdit_stride_y.setText(ProjectSettingsDlgData.data["stride_y"])
#         self.ui.LineEdit_start_z.setText(ProjectSettingsDlgData.data["start_z"])
#         self.ui.LineEdit_end_z.setText(ProjectSettingsDlgData.data["end_z"])
#         self.ui.LineEdit_stride_z.setText(ProjectSettingsDlgData.data["stride_z"])
#         pass
#     def pushBtn_OK(self):
#         print "push"
#         self.updateUI()
#         self.close()
#         pass
#     def pushBtn_Cancel(self):
#         print "CLOSE"
#         self.close()
#         pass
#     def updateUI(self):
#         self.ProjectSettingsDlgData={"name":self.ui.lineEdit_Name.text(),
#             "start_x":self.ui.LineEdit_start_x.text(),
#             "end_x":self.ui.LineEdit_end_x.text(),
#             "stride_x":self.ui.LineEdit_stride_x.text(),
#             "start_y": self.ui.LineEdit_start_y.text(),
#             "end_y": self.ui.LineEdit_end_y.text(),
#             "stride_y": self.ui.LineEdit_stride_y.text(),
#             "start_z": self.ui.LineEdit_start_z.text(),
#             "end_z":self.ui.LineEdit_end_z.text(),
#             "stride_z": self.ui.LineEdit_stride_z.text()}
#         print self.ProjectSettingsDlgData
#         pass

# flag = 0 
# def show(className):
#     if className in ObjectDict.keys():
#         print "second"
#         # ObjectDict[className].refreshCombox()
#         ObjectDict[className]=WorkSpaceSettings("old",className)
#         ObjectDict[className].show()
#         ObjectDict[className].exec_()    
#     else:
#         print "first"
#         ObjectDict[className] = WorkSpaceSettings("new",className)
#         ObjectDict[className].show()
#         ObjectDict[className].exec_()

class WorkSpaceSettings(QtGui.QDialog):
    def __init__(self,className):
        # 这里有运行吗
        QtGui.QDialog.__init__(self)
        self.ui = WorkSpaceSettingsDlg.Ui_Dialog_WorkSpaceDlg()
        self.ui.setupUi(self)
        from ProjectSetting.Tools import CompleterTools
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        global flag
        # flag = 0
        # 设置DX改变的标志，为1时表示发生变化
        global DXChangeFlag
        DXChangeFlag = 0
        # 获取当前坐标系及坐标系单位
        coord = ProjectSettingCommand.getCooedinate()
        self.x = coord[0]
        self.y = coord[1]
        self.z = coord[2]
        self.x_unit = coord[3]
        self.y_unit = coord[4]
        self.z_unit = coord[5]

        self.ui.groupBox_WorkSpace_X.setTitle(self.x)
        self.ui.groupBox_WorkSpace_Y.setTitle(self.y)
        self.ui.groupBox_WorkSpace_Z.setTitle(self.z)
        # self.ui.pushButton_ok.clicked.connect(self.pushBtn_OK)
        self.ui.pushButton.clicked.connect(self.pushBtn_Cancel)

        self.ui.LineEdit_start_x.textChanged.connect(self.lineEditOnChange)
        self.ui.LineEdit_end_x.textChanged.connect(self.lineEditOnChange)
        self.ui.LineEdit_start_y.textChanged.connect(self.lineEditOnChange)
        self.ui.LineEdit_end_y.textChanged.connect(self.lineEditOnChange)
        self.ui.LineEdit_start_z.textChanged.connect(self.lineEditOnChange)
        self.ui.LineEdit_end_z.textChanged.connect(self.lineEditOnChange)

        self.ui.LineEdit_stride_x.textChanged.connect(self.LineEditStrideOnChange)
        self.ui.LineEdit_stride_y.textChanged.connect(self.LineEditStrideOnChange)
        self.ui.LineEdit_stride_z.textChanged.connect(self.LineEditStrideOnChange)

        self.ui.checkBox.setChecked(False)
        # self.ui.checkBox.setText("提交")
        # 防止json报错
        try:
            license = json.loads(FreeCAD.ActiveDocument.License)
        except:
            FreeCAD.ActiveDocument.License = json.dumps('True')
        # 只有模型发生变化才更新
        if (json.loads(FreeCAD.ActiveDocument.License) != 'False'):
            from ProjectSetting.Tools import ProjectSettingsTools
            ProjectSettingsTools.updateRangeOfWorkSpaceSettings()
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)

        self.ui.pushButton_ok.clicked.connect(lambda: self.pushBtn_OK(JSON_CADComment,className))

        if className in JSON_CADComment:
            # FreeCAD.Console.PrintError('\n进入加载json的工作区间设置部分')

            oldData=JSON_CADComment[className]
            # FreeCAD.Console.PrintError(oldData)
            self.loadData(oldData)
            # flag = 1 
        # if DialogID != "new":
        #     print JSON_CADComment
        #     print "\\"
        #     # print JSON_CADComment["SIMUVOLUME"]
        #     # oldData =ProjectSettingsDlgData(JSON_CADComment[className],DialogID)
        #     oldData=JSON_CADComment[className]
        #     self.loadData(oldData)            
        #     flag = 1   

    def pushBtn_OK(self,FreeCAD_Comment_Dict,className):
        # print "oke"
        # global flag 
        # count = 1
        # #这个name必须确保唯一性！！！
        # #也就是他的窗口编辑框里面的值  
        # if flag == 0:
        #     while name in FreeCAD_Comment_Dict.keys(): 
        #        name = self.ui.lineEdit_Name.text() + str(count) 
        #        count+=1             
        #     self.ui.lineEdit_Name.setText(name)       
        #     # addItem([0,0], name, className)
        #     flag = 1
        ProjectSettingsDlgData.getDlgData()
        newData = DlgData({},className)

        self.flag = self.ui.checkBox.isChecked()

        # if self.ui.checkBox.isChecked():
        #     self.keepData(newData,className)
        self.keepData(newData, className)
        # ObjectDict[className]=self
        self.close()
        # 设置paramObj的DX-3这三个属性
        global DXChangeFlag
        # 步长发生变化才更新
        if(DXChangeFlag):
            ObjectsTools.setDX1DX2DX3(str(self.ui.LineEdit_stride_x.text()),str(self.ui.LineEdit_stride_y.text()),str(self.ui.LineEdit_stride_z.text()))
            FreeCAD.Console.PrintMessage("testestest")
        # 标志更新为0
        DXChangeFlag = 0
        # 更新m3d文档 by mx
        # 获得m3d的util
        fileUtil = File.FileCommand.M3DFile.M3DFileUtil.M3DFileUtil()
        # 获得最近的m3d字符串
        FileStr = fileUtil.getLatestM3DFileStr()
        # 进行文本的更新
        File.FileCommand.TextUI.FileTextView.FileView().updateText(FileStr)
        FreeCAD.ActiveDocument.License = json.dumps('False')
        pass
    def pushBtn_Cancel(self):
        FreeCAD.ActiveDocument.License = json.dumps('False')
        self.close()
        pass
    def lineEditOnChange(self):
        FreeCAD.ActiveDocument.License = json.dumps('False')

    #步长发生变化的触发函数，将标志设为1
    def LineEditStrideOnChange(self):
        global DXChangeFlag
        DXChangeFlag = 1
    def loadData(self,DlgData):

        try:
            self.ui.lineEdit_Name.setText(DlgData["name"])
            self.ui.LineEdit_start_x.setText(DlgData["start_X"])
            self.ui.LineEdit_end_x.setText(DlgData["end_X"])
            self.ui.LineEdit_stride_x.setText(DlgData["stride_X"])
            self.ui.LineEdit_start_y.setText(DlgData["start_Y"])
            self.ui.LineEdit_end_y.setText(DlgData["end_Y"])
            self.ui.LineEdit_stride_y.setText(DlgData["stride_Y"])
            self.ui.LineEdit_start_z.setText(DlgData["start_Z"])
            self.ui.LineEdit_end_z.setText(DlgData["end_Z"])
            self.ui.LineEdit_stride_z.setText(DlgData["stride_Z"])
            self.ui.checkBox.setChecked(DlgData["commit"])
            # 加载触发的变化函数不管
            global DXChangeFlag
            DXChangeFlag = 0
        except KeyError as reson:
            FreeCAD.Console.PrintMessage(str(reson))
    def keepData(self,DlgData,className): 
        DlgData.addData("name",self.ui.lineEdit_Name.text())
        DlgData.addData("start_X",self.ui.LineEdit_start_x.text())
        DlgData.addData("end_X",self.ui.LineEdit_end_x.text())
        DlgData.addData("stride_X",self.ui.LineEdit_stride_x.text())
        DlgData.addData("start_Y",self.ui.LineEdit_start_y.text())
        DlgData.addData("end_Y",self.ui.LineEdit_end_y.text())
        DlgData.addData("stride_Y",self.ui.LineEdit_stride_y.text())
        DlgData.addData("start_Z",self.ui.LineEdit_start_z.text())
        DlgData.addData("end_Z",self.ui.LineEdit_end_z.text())
        DlgData.addData("stride_Z",self.ui.LineEdit_stride_z.text())
        # DlgData.addData("commit",self.ui.checkBox.isChecked())

        DlgData.addData("commit",self.flag)
        DlgData.addData("WhetherToHitOkOrNot",True)

        Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        Comment[className] = DlgData.data
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)

