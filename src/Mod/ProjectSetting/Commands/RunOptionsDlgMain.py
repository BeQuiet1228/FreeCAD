# -*- coding: UTF-8 -*-
import json

import FreeCAD
from PySide import QtGui
from ProjectSettingGui.RunOptions import RunOptionsDlg
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import ProjectSettingCommand
from ProjectSettingsDlgData import ProjectSettingsDlgData as DlgData
import ProjectSettingsDlgData
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
class RunOptions(QtGui.QDialog):
    def __init__(self,className):
        QtGui.QDialog.__init__(self)
        self.ui = RunOptionsDlg.Ui_Dialog_RunOptionsDlg()
        self.ui.setupUi(self)
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        self.ui.pushButton_ok.clicked.connect(lambda: self.pushBtn_OK(JSON_CADComment,className))

        if className in JSON_CADComment:
            oldData=JSON_CADComment[className]
            self.loadData(oldData)
    def pushBtn_OK(self,FreeCAD_Comment_Dict,className):

        ProjectSettingsDlgData.getDlgData()
        newData = DlgData({},className)           
        self.keepData(newData,className)
        # ObjectDict[className]=self
        self.close()

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
            self.ui.checkBox_show_structureChart.setChecked(DlgData["checkBoxShowStructChart"])
            self.ui.checkBox_paused_when_start.setChecked(DlgData["CheckBoxPausedWhenStart"])          
        except KeyError as reson:
            FreeCAD.Console.PrintMessage(str(reson))
    def keepData(self,DlgData,className): 
        DlgData.addData("CheckBoxPausedWhenStart",self.ui.checkBox_paused_when_start.isChecked())
        DlgData.addData("checkBoxShowStructChart",self.ui.checkBox_show_structureChart.isChecked())
        
        Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        Comment[className] = DlgData.data
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)
