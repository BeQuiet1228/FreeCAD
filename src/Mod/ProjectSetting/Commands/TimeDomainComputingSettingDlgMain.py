#-*- coding: utf-8 -*-
import json

import FreeCAD
import PySide
from PySide import QtGui,QtCore
from ProjectSettingGui.TimeDomainComputingSettings import TimeDomainComputingSettingDlg
from Modeling.Common.CommonCommand.NewDocument import ObjectDict
import ProjectSettingCommand
from ProjectSettingsDlgData import ProjectSettingsDlgData as DlgData
import ProjectSettingsDlgData
import File.FileCommand.M3DFile.M3DFileUtil
import File.FileCommand.TextUI.FileTextView
from Tools import CompleterTools
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
class TimeDomainComputingSetting(QtGui.QDialog):
    def __init__(self,className,type):
        QtGui.QDialog.__init__(self)
        self.ui = TimeDomainComputingSettingDlg.Ui_Dialog_TimeDomainComputingSettingDlg()
        self.ui.setupUi(self)
        # global flag
        #代码补全
        CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
        # self.ui.pushButton.clicked.connect(self.pushBtn_Cancel)
        # self.ui.comboBox_filed_arithmetic.clicked.connect(self.onFiledAri)
        self.ui.checkBox_setting_mode.clicked.connect(self.onCheckBoxSettingMode)
        self.ui.checkBox_setting_stride.clicked.connect(self.onCheckBoxSettingStride)
        self.ui.checkBox_part.clicked.connect(self.setMacroParticleShow)
        self.ui.checkBox_setting_step.clicked.connect(self.onCheckBoxSettingStep)
        self.ui.radioButton_nonre.clicked.connect(self.onRadioButton)
        self.ui.radioButton_re.clicked.connect(self.onRadioButton)
        # self.ui.radioButton_EM.clicked.connect(self.onRadioBtnEM)
        # self.ui.radioButton_TE.clicked.connect(self.onRadioBtnTE)
        # self.ui.radioButton_TM.clicked.connect(self.onRadioBtnTM)
        # self.ui.checkBox_setting_chargeContinuity.clicked.connect(self.oncheckBocSettingChargerCon)
        # self.test_try()

        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict) 
        self.ui.pushButton_ok.clicked.connect(lambda: self.pushBtn_OK(JSON_CADComment,className))

        if className in JSON_CADComment:
            oldData=JSON_CADComment[className]
            self.loadData(oldData)

        self.onCheckBoxSettingMode()
        self.onCheckBoxSettingStride()
        self.setMacroParticleShow()
        self.onCheckBoxSettingStep()
        self.onRadioButton()
        # if self.ui.checkBox_conductivity.checkState==PySide.QtCore.Qt.CheckState.Checked:
        #     self.ui.lineEdit_conductivity.setReadOnly(False)
        # else:
        #     self.ui.lineEdit_conductivity.setReadOnly(True)
        # if self.ui.checkBox_dielectric_constant.checkState==PySide.QtCore.Qt.CheckState.Checked:
        #     self.ui.lineEdit_dielectric_constant.setReadOnly(False)
        # else:
        #     self.ui.lineEdit_dielectric_constant.setReadOnly(True)
        if type=="toolBar":
            self.hideUpPart()
            # 适配分辨率
            import Physics.PhysicsCommand.AdaptiveDPIUtil as AdaptiveDPIUtil
            new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
            self.resize(500, 200)
        else:
            self.hideBelowPart()
            # 适配分辨率
            import Physics.PhysicsCommand.AdaptiveDPIUtil as AdaptiveDPIUtil
            new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
            self.resize(500, 400)
        
    def hideUpPart(self):
        self.setWindowTitle(u"宏粒子合并")
        #隐藏上半部分
        self.ui.label.hide()
        self.ui.lineEdit_compute_time.hide()
        self.ui.label_3.hide()
        self.ui.groupBox_WorkSpace_X.hide()
        self.ui.groupBox_WorkSpace_Y.hide()
        #显示下半部分
        self.ui.checkBox_part.show()
        self.ui.lineEdit_max.show()
        self.ui.label_5.show()
        self.ui.label_4.show()
        self.ui.lineEdit_every.show()
        self.ui.comboBox.show()
        self.ui.label_6.show()
        self.ui.pushButton_ok.show()
    def hideBelowPart(self):
        self.setWindowTitle(u"时域计算设置")
        #显示上半部分
        self.ui.label.show()
        self.ui.lineEdit_compute_time.show()
        self.ui.label_3.show()
        self.ui.groupBox_WorkSpace_X.show()
        self.ui.groupBox_WorkSpace_Y.show()
        #隐藏下半部分
        self.ui.checkBox_part.hide()
        self.ui.lineEdit_max.hide()
        self.ui.label_5.hide()
        self.ui.label_4.hide()
        self.ui.lineEdit_every.hide()
        self.ui.comboBox.hide()
        self.ui.label_6.hide()
        self.ui.pushButton_ok.show()
        
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
        FreeCAD.Console.PrintMessage("Cancel")
        self.close()
        pass
    def loadData(self,DlgData):
        try:
            self.ui.lineEdit_compute_time.setText(DlgData["computeTime"])
            self.ui.comboBox_filed_arithmetic.setCurrentIndex(self.ui.comboBox_filed_arithmetic.findText(DlgData["filedAri"]))
            self.ui.checkBox_setting_mode.setChecked(DlgData["settingMode"])
            self.ui.radioButton_EM.setChecked(DlgData["radioEM"])
            self.ui.radioButton_TE.setChecked(DlgData["radioTE"])
            self.ui.radioButton_TM.setChecked(DlgData["radioTM"])
            self.ui.checkBox_setting_stride.setChecked(DlgData["checkBoxStride"])
            self.ui.lineEdit_setting_stride.setText(DlgData["lineEditStride"])
            self.ui.checkBox_setting_chargeContinuity.setChecked(DlgData["checkBoxCharCont"])
            try:
                self.ui.comboBox.setCurrentIndex(self.ui.comboBox.findText(DlgData["Types"]))
                self.ui.checkBox_part.setChecked(DlgData["isChecked_part"])
                self.ui.lineEdit_every.setText(DlgData["EveryNum"])
                self.ui.lineEdit_max.setText(DlgData["MaxNum"])
            except:
                FreeCAD.Console.PrintMessage("设置宏粒子出错！")
            try:
                self.ui.checkBox_setting_step.setChecked(DlgData["checkBoxStep"])
                self.ui.lineEdit_setting_step.setText(DlgData["computeTimeInterval"])
                self.ui.radioButton_re.setChecked(DlgData["is_re"])
                self.ui.radioButton_nonre.setChecked(DlgData["is_nonre"])
            except:
                FreeCAD.Console.PrintMessage("\n设置时间步长间隔出错!")
        except KeyError as reson:
            FreeCAD.Console.PrintMessage(str(reson))
    def keepData(self,DlgData,className): 
        DlgData.addData("computeTime",self.ui.lineEdit_compute_time.text())
        DlgData.addData("filedAri",self.ui.comboBox_filed_arithmetic.currentText())
        DlgData.addData("settingMode",self.ui.checkBox_setting_mode.isChecked())
        DlgData.addData("radioEM",self.ui.radioButton_EM.isChecked())
        DlgData.addData("radioTE",self.ui.radioButton_TE.isChecked())
        DlgData.addData("radioTM",self.ui.radioButton_TM.isChecked())
        DlgData.addData("checkBoxStride",self.ui.checkBox_setting_stride.isChecked())
        DlgData.addData("lineEditStride",self.ui.lineEdit_setting_stride.text())
        DlgData.addData("checkBoxCharCont",self.ui.checkBox_setting_chargeContinuity.isChecked())
        # 新添加的宏粒子合并 @lzg
        DlgData.addData("Types",self.ui.comboBox.currentText())
        DlgData.addData("EveryNum",self.ui.lineEdit_every.text())
        DlgData.addData("MaxNum",self.ui.lineEdit_max.text())
        DlgData.addData("isChecked_part",self.ui.checkBox_part.isChecked())
        # 新添加的粒子计算时间步长设置 @lzg
        DlgData.addData("checkBoxStep",self.ui.checkBox_setting_step.isChecked())
        DlgData.addData("computeTimeInterval",self.ui.lineEdit_setting_step.text())
        DlgData.addData("is_re",self.ui.radioButton_re.isChecked())
        DlgData.addData("is_nonre",self.ui.radioButton_nonre.isChecked())

        Comment = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)



        # print className
        Comment[className] = DlgData.data
        FreeCAD.ActiveDocument.Comment = json.dumps(Comment)

    def onCheckBoxSettingMode(self):
        self.ui.radioButton_EM.setEnabled(self.ui.checkBox_setting_mode.isChecked()) 
        self.ui.radioButton_TE.setEnabled(self.ui.checkBox_setting_mode.isChecked()) 
        self.ui.radioButton_TM.setEnabled(self.ui.checkBox_setting_mode.isChecked()) 
    def setMacroParticleShow(self):
        self.ui.comboBox.setEnabled(self.ui.checkBox_part.isChecked())
        self.ui.lineEdit_every.setEnabled(self.ui.checkBox_part.isChecked())
        self.ui.lineEdit_max.setEnabled(self.ui.checkBox_part.isChecked())

    def onCheckBoxSettingStride(self):
        self.ui.lineEdit_setting_stride.setEnabled(self.ui.checkBox_setting_stride.isChecked()) 
    def onCheckBoxSettingStep(self):
        self.ui.lineEdit_setting_step.setEnabled(self.ui.checkBox_setting_step.isChecked())
        self.ui.radioButton_re.setEnabled(self.ui.checkBox_setting_step.isChecked())
        self.ui.radioButton_nonre.setEnabled(self.ui.checkBox_setting_step.isChecked())
    def onRadioButton(self):
        flag_re = self.ui.radioButton_re.isChecked()
        if flag_re:
            self.ui.radioButton_re.setChecked(True)
            self.ui.radioButton_nonre.setChecked(False)
        else:
            self.ui.radioButton_re.setChecked(False)
            self.ui.radioButton_nonre.setChecked(True)
    def test_try(self):
        string_test = "runtime"
        result=True
        try:
            self.test_try2()
            # try:
            #     num=float(string_test)
            #     result = num == num
            # except :
            #     result=False
            #     FreeCAD.Console.PrintError("\n进入内层异常语句")
        except:
            FreeCAD.Console.PrintError("\n进入外层异常语句")
        return result
    def test_try2(self):
        string_test = "runtime"
        try:
            num=float(string_test)
            result = num == num
        except :
            result=False
            FreeCAD.Console.PrintError("\n进入内层异常语句")
