#-*- coding: utf-8 -*-
import json

import FreeCAD
import PySide
from PySide import QtGui,QtCore
from ProjectSettingGui.FieldSetting import FiledSettingDlg
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import ProjectSettingCommand
from ProjectSettingsDlgData import ProjectSettingsDlgData as DlgData
import ProjectSettingsDlgData
from Modeling.Common.Tools import CoordinateSystemTools
from Tools import CompleterTools
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
#json格式数据需要保持原有顺序输出
from collections import OrderedDict

class FieldSetting(QtGui.QDialog):
    def __init__(self,className):
        QtGui.QDialog.__init__(self)
        self.ui = FiledSettingDlg.Ui_Dialog_FieldSettingDlg()
        self.ui.setupUi(self)
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        if FreeCAD.ActiveDocument.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            self.ui.checkBox_magenetic_x.setText(u"X方向FBXST(X,Y,Z)=")
            self.ui.checkBox_magenetic_y.setText(u"Y方向FBXST(X,Y,Z)=")
            self.ui.checkBox_magenetic_z.setText(u"Z方向FBXST(X,Y,Z)=")
            self.ui.checkBox_electric_x.setText(u"X方向FBXST(X,Y,Z)=")
            self.ui.checkBox_electric_y.setText(u"Y方向FBXST(X,Y,Z)=")
            self.ui.checkBox_electric_z.setText(u"Z方向FBXST(X,Y,Z)=")
        elif  FreeCAD.ActiveDocument.CoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            self.ui.checkBox_magenetic_x.setText(u"R方向FBXST(R,θ,Z)=")
            self.ui.checkBox_magenetic_y.setText(u"θ方向FBXST(R,θ,Z)=")
            self.ui.checkBox_magenetic_z.setText(u"Z方向FBXST(R,θ,Z)=")
            self.ui.checkBox_electric_x.setText(u"R方向FBXST(R,θ,Z)=")
            self.ui.checkBox_electric_y.setText(u"θ方向FBXST(R,θ,Z)=")
            self.ui.checkBox_electric_z.setText(u"Z方向FBXST(R,θ,Z)=")
        else:
            self.ui.checkBox_magenetic_x.setText(u"Z方向FBXST(Z,θ,R)=")
            self.ui.checkBox_magenetic_y.setText(u"R方向FBXST(Z,θ,R)=")
            self.ui.checkBox_magenetic_z.setText(u"θ方向FBXST(Z,θ,R)=")
            self.ui.checkBox_electric_x.setText(u"Z方向FBXST(Z,θ,R)=")
            self.ui.checkBox_electric_y.setText(u"R方向FBXST(Z,θ,R)=")
            self.ui.checkBox_electric_z.setText(u"θ方向FBXST(Z,θ,R)=")           
        self.ui.checkBox_magenetic_x.clicked.connect(self.onCheckBox_magenetic_xClicked)
        self.ui.checkBox_magenetic_y.clicked.connect(self.onCheckBox_magenetic_yClicked)
        self.ui.checkBox_magenetic_z.clicked.connect(self.onCheckBox_magenetic_zClicked)
        self.ui.checkBox_electric_x.clicked.connect(self.onCheckBox_electric_xClicked)
        self.ui.checkBox_electric_y.clicked.connect(self.onCheckBox_electric_yClicked)
        self.ui.checkBox_electric_z.clicked.connect(self.onCheckBox_electric_zClicked)

        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict) 
        self.ui.pushButton_ok.clicked.connect(lambda: self.pushBtn_OK(JSON_CADComment,className))

        if className in JSON_CADComment:
            oldData=JSON_CADComment[className]
            self.loadData(oldData)

        self.onCheckBox_electric_xClicked()
        self.onCheckBox_electric_yClicked()
        self.onCheckBox_electric_zClicked()
        self.onCheckBox_magenetic_xClicked()
        self.onCheckBox_magenetic_yClicked()
        self.onCheckBox_magenetic_zClicked()

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
            self.ui.LineEdit_magenetic_x.setText(DlgData["mag_x"])
            self.ui.LineEdit_magenetic_y.setText(DlgData["mag_y"])
            self.ui.LineEdit_magenetic_z.setText(DlgData["mag_z"])
            self.ui.LineEdit_electric_x.setText(DlgData["ele_x"])
            self.ui.LineEdit_electric_y.setText(DlgData["ele_y"])
            self.ui.LineEdit_electric_z.setText(DlgData["ele_z"])
            self.ui.textEdit_filed_custom.setPlainText(DlgData["filedCustom"])
            if DlgData["check_mag_x"]:
                self.ui.checkBox_magenetic_x.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_magenetic_x.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
            if DlgData["check_mag_y"]:
                self.ui.checkBox_magenetic_y.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_magenetic_y.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
            if DlgData["check_mag_z"]:
                self.ui.checkBox_magenetic_z.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_magenetic_z.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
            if DlgData["check_ele_x"]:
                self.ui.checkBox_electric_x.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_electric_x.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
            if DlgData["check_ele_y"]:
                self.ui.checkBox_electric_y.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_electric_y.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
            if DlgData["check_ele_z"]:
                self.ui.checkBox_electric_z.setCheckState(PySide.QtCore.Qt.CheckState.Checked)
            else:
                self.ui.checkBox_electric_z.setCheckState(PySide.QtCore.Qt.CheckState.Unchecked)
        except KeyError as reson:
            FreeCAD.Console.PrintMessage(str(reson)) 
    def keepData(self,DlgData,className): 
        DlgData.addData("mag_x",self.ui.LineEdit_magenetic_x.toPlainText())
        DlgData.addData("mag_y",self.ui.LineEdit_magenetic_y.toPlainText())
        DlgData.addData("mag_z",self.ui.LineEdit_magenetic_z.toPlainText())
        DlgData.addData("ele_x",self.ui.LineEdit_electric_x.toPlainText())
        DlgData.addData("ele_y",self.ui.LineEdit_electric_y.toPlainText())
        DlgData.addData("ele_z",self.ui.LineEdit_electric_z.toPlainText())
        DlgData.addData("filedCustom",self.ui.textEdit_filed_custom.toPlainText())

        if self.ui.checkBox_magenetic_x.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("check_mag_x",True)
        else:
            DlgData.addData("check_mag_x",False)
        if self.ui.checkBox_magenetic_y.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("check_mag_y",True)
        else:
            DlgData.addData("check_mag_y",False)
        if self.ui.checkBox_magenetic_z.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("check_mag_z",True)
        else:
            DlgData.addData("check_mag_z",False)
        if self.ui.checkBox_electric_x.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("check_ele_x",True)
        else:
            DlgData.addData("check_ele_x",False)
        if self.ui.checkBox_electric_y.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("check_ele_y",True)
        else:
            DlgData.addData("check_ele_y",False)
        if self.ui.checkBox_electric_z.checkState()==PySide.QtCore.Qt.CheckState.Checked:
            DlgData.addData("check_ele_z",True)
        else:
            DlgData.addData("check_ele_z",False)
        Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        Comment[className] = DlgData.data
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)

    def onCheckBox_magenetic_xClicked(self):
        self.ui.LineEdit_magenetic_x.setEnabled(self.ui.checkBox_magenetic_x.isChecked()) 
    def onCheckBox_magenetic_yClicked(self):
        self.ui.LineEdit_magenetic_y.setEnabled(self.ui.checkBox_magenetic_y.isChecked()) 
    def onCheckBox_magenetic_zClicked(self):
        self.ui.LineEdit_magenetic_z.setEnabled(self.ui.checkBox_magenetic_z.isChecked()) 
    def onCheckBox_electric_xClicked(self):
        self.ui.LineEdit_electric_x.setEnabled(self.ui.checkBox_electric_x.isChecked()) 
    def onCheckBox_electric_yClicked(self):
        self.ui.LineEdit_electric_y.setEnabled(self.ui.checkBox_electric_y.isChecked())     
    def onCheckBox_electric_zClicked(self):
        self.ui.LineEdit_electric_z.setEnabled(self.ui.checkBox_electric_z.isChecked()) 