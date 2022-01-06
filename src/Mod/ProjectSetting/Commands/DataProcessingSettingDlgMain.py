#-*- coding: utf-8 -*-
import json

import FreeCAD
import PySide
from PySide import QtGui,QtCore
from ProjectSettingGui.DataProcessingSetting import DataProcessingSettingDlg
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import ProjectSettingCommand
from ProjectSettingsDlgData import ProjectSettingsDlgData  as DlgData
import ProjectSettingsDlgData
from Modeling.Common.Tools import CoordinateSystemTools



import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
#json格式数据需要保持原有顺序输出
from collections import OrderedDict

class DataProcessingSetting(QtGui.QDialog):
    def __init__(self,className):
        QtGui.QDialog.__init__(self)
        self.ui = DataProcessingSettingDlg.Ui_Dialog_DataProcessingSettingDlg()
        self.ui.setupUi(self)
        from ProjectSetting.Tools import CompleterTools
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        self.ui.checkBox_set_prefix.clicked.connect(self.onCheckBox_set_prefix)
        self.ui.checkBox_set_suffix.clicked.connect(self.onCheckBox_set_suffix)
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        self.ui.pushButton_ok.clicked.connect(lambda: self.pushBtn_OK(JSON_CADComment,className))

        if className in JSON_CADComment:
            oldData=JSON_CADComment[className]
            self.loadData(oldData)

        self.onCheckBox_set_prefix()
        self.onCheckBox_set_suffix()

    def pushBtn_OK(self,FreeCAD_Comment_Dict,className):
        ProjectSettingsDlgData.getDlgData()
        newData = DlgData({},className)           
        self.keepData(newData,className)
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
            self.ui.checkBox_Time_obser.setChecked(DlgData["time_obser"])
            self.ui.checkBox_space_obser.setChecked(DlgData["space_obser"])
            self.ui.checkBox_contor_plot.setChecked(DlgData["contor_plot"])
            self.ui.checkBox_vector_data.setChecked(DlgData["vector_data"])
            self.ui.checkBox_phase_space.setChecked(DlgData["phase_space"])
            self.ui.checkBox_set_prefix.setChecked(DlgData["checkBox_prefix"])
            self.ui.checkBox_set_suffix.setChecked(DlgData["checkBox_suffix"])
            self.ui.lineEdit_prefix.setText(DlgData["lineEdit_prefix"])
            self.ui.lineEdit_suffix.setText(DlgData["lineEdit_suffix"])
            self.ui.radioButton_text_format.setChecked(DlgData["text_form"])
            self.ui.radioButton_binary_format.setChecked(DlgData["binary_form"])
        except KeyError as reson:
            FreeCAD.Console.PrintMessage(str(reson))
    def keepData(self,DlgData,className): 
        DlgData.addData("time_obser",self.ui.checkBox_Time_obser.isChecked())
        DlgData.addData("space_obser",self.ui.checkBox_space_obser.isChecked())
        DlgData.addData("contor_plot",self.ui.checkBox_contor_plot.isChecked())
        DlgData.addData("vector_data",self.ui.checkBox_vector_data.isChecked())
        DlgData.addData("phase_space",self.ui.checkBox_phase_space.isChecked())
        DlgData.addData("checkBox_prefix",self.ui.checkBox_set_prefix.isChecked())
        DlgData.addData("checkBox_suffix",self.ui.checkBox_set_suffix.isChecked())
        DlgData.addData("lineEdit_prefix",self.ui.lineEdit_prefix.text())
        DlgData.addData("lineEdit_suffix",self.ui.lineEdit_suffix.text())
        DlgData.addData("text_form",self.ui.radioButton_text_format.isChecked())
        DlgData.addData("binary_form",self.ui.radioButton_binary_format.isChecked())

        Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        Comment[className] = DlgData.data
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)

    def onCheckBox_set_prefix(self):
        self.ui.lineEdit_prefix.setEnabled(self.ui.checkBox_set_prefix.isChecked()) 
    def onCheckBox_set_suffix(self):
        self.ui.lineEdit_suffix.setEnabled(self.ui.checkBox_set_suffix.isChecked()) 