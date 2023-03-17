# -*- coding: utf-8 -*-
import IoniDialog
import traceback
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D, ObjectTools

def setGPreTimeFunction(Str):
    num = 0
    Str = Str[::-1]
    index = 0
    for i in Str:
        if i.isdigit():
            num = num + int(i) * pow(10, index)
            index += 1
        else:
            break
    return str(num)

class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = IoniDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(self.ui))
            #默认正投影体
            self.defaultValue = ["OSYS$VOLUME"]
            # 获取当前坐标系及坐标系单位
            Tools3D.switchPointLabel(self.ui)
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            # self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            self.ComboBox_Shadow_clicked()
            # 适配分辨率

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        try:
            self.ui.le_name.setText(self.obj.Label)
            self.ui.cb_type.setCurrentIndex(self.ui.cb_type.findText(self.obj.ionizationOfGas))
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.ioniType)))
            self.ui.le_pressure.setText(self.obj.gasPressure)
            self.ui.le_temperature.setText(self.obj.gasTemperature)
            Tools3D.setCoorToUI(self.ui, self.obj)
        except:
            Tools3D.sayz("Ioni加载数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        try:
            # Tools3D.setLabelToObj(self.obj, self.ui.le_name.text())
            self.obj.Label = Tools3D.setLabel(self.ui.le_name.text())
            self.obj.GPreTimeFunction = "GPreTime" + setGPreTimeFunction(self.obj.Label)
            self.obj.ioniType = self.ui.ComboBox_Shadow.currentText()
            self.obj.ionizationOfGas = self.ui.cb_type.currentText()
            self.obj.gasPressure = self.ui.le_pressure.toPlainText()
            self.obj.gasTemperature = self.ui.le_temperature.text()
            Tools3D.getUICoordinate(self.obj, self.ui)
        except:
            Tools3D.sayz("Ioni设置数据时出现异常")
            Tools3D.sayz("error:" + traceback.format_exc())

    def ComboBox_Shadow_clicked(self):
        try:
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Vol_Conformal)
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                Tools3D.setIsEdit(self.ui, False)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        try:
            ComboBox_Shadow_list = []
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
            volumeList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
            volumeList.append("OSYS$VOLUME")
            for i in volumeList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())
