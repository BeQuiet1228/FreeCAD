# encoding:utf-8
import FreeCAD
import FreeCADGui
import DataProcessingSettingInstance
import ChipicContinueUI
from Model3D.Tools import Tools3D
import DataProcessingSettingDialogMain
from PySide import QtGui
from Model3D.Tools import ObjectTools, InitDoc3D
import os


class CreateDataProcessingSettingCommand:
    """
    注册FreeSpace命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = DataProcessingSettingInstance.getObject()
        # 在这里打开Ui
        Form = DataProcessingSettingDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/DataProcessingSetting.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'DataProcessingSetting',
            '数据导出设置')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'DataProcessingSetting',
            'make DataProcessingSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateDataProcessingSetting', CreateDataProcessingSettingCommand())


class ChipicContinueDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = ChipicContinueUI.Ui_ChipicContinueUI()
        self.ui.setupUi(self)
        self.getInfo()
    def getInfo(self):
        self.info = FreeCAD.ActiveDocument.getObject("ChipicContinueInfo")
        if self.info is None:
            self.info = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "ChipicContinueInfo")
            self.info.addProperty("App::PropertyBool", "ContinueData").ContinueData = False
            self.info.addProperty("App::PropertyBool", "ContinueFile").ContinueFile = False
            self.info.addProperty("App::PropertyString", "cycle").cycle = "10"
            self.info.addProperty("App::PropertyString", "DataFileName").DataFileName = "RcdFile"
            self.info.addProperty("App::PropertyString", "ContinueFileName").ContinueFileName = "Data"
            self.info.addProperty("App::PropertyString", "m3d").m3d = ""
        self.initGUI()
        #InitDoc3D.addObjectToGroup_helper(self.info, "ChipicContinueInfo", "断点续算设置")
    def saveInfo(self):
        self.info.ContinueData =  self.ui.checkBoxData.isChecked()
        self.info.ContinueFile = self.ui.checkBoxContinue.isChecked()
        self.info.cycle = self.ui.lineEditCycel.text()
        self.info.DataFileName = self.ui.lineEditFileName.text()
        self.info.ContinueFileName =  self.ui.comboBoxFileName.currentText()
        m3d = ""
        if self.info.ContinueData:
            m3d += "TIMER RcdTimer PERIODIC REAL %.2e %.2e %.2e ;\n"\
                %(float(self.info.cycle)*1E-9,500*1E-9,float(self.info.cycle)*1E-9)
            m3d += "record RcdTimer "+self.info.DataFileName +";\n"
        if self.info.ContinueFile:
            m3d += "CONTINUE " +self.info.ContinueFileName +";\n"
        self.info.m3d = m3d
    def initGUI(self):
        # 获取当前文档的文件路径
        doc_path = os.path.dirname(FreeCADGui.ActiveDocument.Document.FileName)

        # 列出所有.data 文件
        data_files = [f for f in os.listdir(doc_path) if f.endswith('.rcf')]
        self.ui.comboBoxFileName.clear()
        for file_name in data_files:
            self.ui.comboBoxFileName.addItem(file_name)
        self.ui.checkBoxData.setChecked(self.info.ContinueData)
        self.ui.checkBoxContinue.setChecked(self.info.ContinueFile)
        self.ui.lineEditFileName.setText(self.info.DataFileName)
        self.ui.lineEditCycel.setText(self.info.cycle)
        index = self.ui.comboBoxFileName.findText(self.info.ContinueFileName)  # 查找文本，返回索引，如果未找到返回 -1
        if index == -1:
            index = 0  # 如果没有找到，设置为0
        self.ui.comboBoxFileName.setCurrentIndex(index)  # 设置选中项

        
    


class CreateChipicContinueCommand:
    """
    注册FreeSpace命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = DataProcessingSettingInstance.getObject()
        # 在这里打开Ui
        Form = ChipicContinueDialog()
        if Form.exec_():
            Form.saveInfo()
        FreeCADGui.runCommand('CreateM3D_new')

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/DataProcessingSetting.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'ChipicContinue',
            '断点续算设置')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'ChipicContinue',
            'make ChipicContinue')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateChipicContinue', CreateChipicContinueCommand())