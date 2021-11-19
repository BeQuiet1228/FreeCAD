# -*- coding: UTF-8 -*-
from PySide import QtGui, QtCore
import FreeCAD,FreeCADGui
import re
import json
import FreeCAD
from Modeling.Modeling3D.Modeling3DCommand.ShowAllFunction import ShowAllFunctionDialog
from Modeling.Common.Tools import DocumentTools
from Modeling import Common
from Physics.PhysicsCommand import DlgData
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
class ShowAllFunctionDlgMain(QtGui.QDialog):
    def __init__(self, obj=None):
        QtGui.QDialog.__init__(self)
        self.ui = ShowAllFunctionDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.function_list = DocumentTools.getAllFunctions()
        self.NumberOfPages = 0 #用来管理页数的变量 0表示第一页
        self.setLabel()
        self.setComboBox()
        self.ui.checkBox_all.setChecked(self.setcheckBox_all_State())

        self.ui.pushButton_up.clicked.connect(self.PreviousPages)
        self.ui.pushButton_down.clicked.connect(self.NextPages)
        self.ui.pushButton_ok.clicked.connect(self.closeDialog)
        # self.ui.checkBox_all.clicked.connect(self.setAllFunctionNotDefine)
         

    def setLabel(self):
        len_function = len(self.function_list) - self.NumberOfPages*5
        if len_function >= 5:
            len_function = 5
        FreeCAD.Console.PrintError('\n函数体列表的长度:'+str(len_function))
        if len_function == 0:
            self.ui.label_1.setText("NULL")
            self.ui.label_2.setText("NULL")
            self.ui.label_3.setText("NULL")
            self.ui.label_4.setText("NULL")
            self.ui.label_5.setText("NULL")
        elif len_function == 1:
            self.ui.label_1.setText(self.function_list[int(self.NumberOfPages*5)].Label)
            self.ui.label_2.setText("NULL")
            self.ui.label_3.setText("NULL")
            self.ui.label_4.setText("NULL")
            self.ui.label_5.setText("NULL")
        elif len_function == 2:
            self.ui.label_1.setText(self.function_list[self.NumberOfPages*5].Label)
            self.ui.label_2.setText(self.function_list[self.NumberOfPages*5+1].Label)
            self.ui.label_3.setText("NULL")
            self.ui.label_4.setText("NULL")
            self.ui.label_5.setText("NULL")
        elif len_function == 3:
            self.ui.label_1.setText(self.function_list[self.NumberOfPages*5].Label)
            self.ui.label_2.setText(self.function_list[self.NumberOfPages*5+1].Label)
            self.ui.label_3.setText(self.function_list[self.NumberOfPages*5+2].Label)
            self.ui.label_4.setText("NULL")
            self.ui.label_5.setText("NULL")
        elif len_function == 4:
            self.ui.label_1.setText(self.function_list[self.NumberOfPages*5].Label)
            self.ui.label_2.setText(self.function_list[self.NumberOfPages*5+1].Label)
            self.ui.label_3.setText(self.function_list[self.NumberOfPages*5+2].Label)
            self.ui.label_4.setText(self.function_list[self.NumberOfPages*5+3].Label)
            self.ui.label_5.setText("NULL")
        elif len_function == 5:
            self.ui.label_1.setText(self.function_list[self.NumberOfPages*5].Label)
            self.ui.label_2.setText(self.function_list[self.NumberOfPages*5+1].Label)
            self.ui.label_3.setText(self.function_list[self.NumberOfPages*5+2].Label)
            self.ui.label_4.setText(self.function_list[self.NumberOfPages*5+3].Label)
            self.ui.label_5.setText(self.function_list[self.NumberOfPages*5+4].Label)
    def PreviousPages(self):
        '''
        上一页按钮所链接的函数
        '''
        if self.NumberOfPages == 0:
            return
        self.NumberOfPages = self.NumberOfPages - 1
        self.setLabel()
        self.setComboBox()
    def NextPages(self):
        '''
        下一页按钮所链接的函数\n
        除第一页外，不允许再出现全部为NULL的情况
        '''
        MaxPages = int(len(self.function_list)/5)
        if self.NumberOfPages >= MaxPages:
            return
        self.NumberOfPages = self.NumberOfPages + 1
        self.setLabel()
        self.setComboBox()
    def setComboBox(self):
        '''
        用来设置下拉框选项的函数
        '''
        self.setAllComboBoxNULL()
        len_function = len(self.function_list) - self.NumberOfPages*5
        if len_function >= 5:
            len_function = 5
        if len_function >= 1:
            if self.function_list[self.NumberOfPages*5].Attribute == "NotDefine":
                pass
            elif self.function_list[self.NumberOfPages*5].Attribute == "Conductor":
                self.ui.comboBox_1.setCurrentIndex(1)
            elif self.function_list[self.NumberOfPages*5].Attribute == "Vacuo":
                self.ui.comboBox_1.setCurrentIndex(2)
        if len_function >= 2:
            if self.function_list[self.NumberOfPages*5+1].Attribute == "NotDefine":
                pass
            elif self.function_list[self.NumberOfPages*5+1].Attribute == "Conductor":
                self.ui.comboBox_2.setCurrentIndex(1)
            elif self.function_list[self.NumberOfPages*5+1].Attribute == "Vacuo":
                self.ui.comboBox_2.setCurrentIndex(2)
        if len_function >= 3:
            if self.function_list[self.NumberOfPages*5+2].Attribute == "NotDefine":
                pass
            elif self.function_list[self.NumberOfPages*5+2].Attribute == "Conductor":
                self.ui.comboBox_3.setCurrentIndex(1)
            elif self.function_list[self.NumberOfPages*5+2].Attribute == "Vacuo":
                self.ui.comboBox_3.setCurrentIndex(2)
        if len_function >= 4:
            if self.function_list[self.NumberOfPages*5+3].Attribute == "NotDefine":
                pass
            elif self.function_list[self.NumberOfPages*5+3].Attribute == "Conductor":
                self.ui.comboBox_4.setCurrentIndex(1)
            elif self.function_list[self.NumberOfPages*5+3].Attribute == "Vacuo":
                self.ui.comboBox_4.setCurrentIndex(2)
        if len_function >= 5:
            if self.function_list[self.NumberOfPages*5+4].Attribute == "NotDefine":
                pass
            elif self.function_list[self.NumberOfPages*5+4].Attribute == "Conductor":
                self.ui.comboBox_5.setCurrentIndex(1)
            elif self.function_list[self.NumberOfPages*5+4].Attribute == "Vacuo":
                self.ui.comboBox_5.setCurrentIndex(2)

    def setAllComboBoxNULL(self):
        '''
        把所有ComboBox设置为未定义
        '''
        self.ui.comboBox_1.setCurrentIndex(0)
        self.ui.comboBox_2.setCurrentIndex(0)
        self.ui.comboBox_3.setCurrentIndex(0)
        self.ui.comboBox_4.setCurrentIndex(0)
        self.ui.comboBox_5.setCurrentIndex(0)
    def setAllFunctionNotDefine(self):
        '''
        如果勾选框被选中\n
        那么把所有的函数体都把属性改为未定义
        '''
        notdefine_flag = self.ui.checkBox_all.isChecked()
        FreeCAD.Console.PrintError('\n是否选择了全部不参与布尔运算:'+str(notdefine_flag))
        newdata = DlgData.DlgData({},"setAllFunction")
        if notdefine_flag:
            for objItem in self.function_list:
                FreeCAD.Console.PrintError('\n函数体名称:'+str(objItem.Label))
                objItem.Attribute = "NotDefine"
                FreeCAD.Console.PrintError('      该函数体的属性:'+str(objItem.Attribute))
            Common.Tools.DocumentTools.updateBoolean()
    def closeDialog(self):
        '''
        确定按钮所链接的函数
        '''
        self.setAllFunctionNotDefine()
        self.close()
    def setcheckBox_all_State(self):
        '''
        如果所有的函数体都是未定义，返回True，checkBox设为勾选
        '''
        # flag_checkBox_all = False
        for objItem in self.function_list:
            if objItem.Attribute != "NotDefine":
                return False
        return True
    def keepData(self,dlgdata):
        '''
        用来保存函数体的属性，在设置未定义后所有函数体属性都变为未定义\n
        但是需要在取消所有函数体都变为未定义之后恢复所有函数体的属性\n
        将数据保存在json里面
        '''
        for objItem in self.function_list:
            dlgdata.addData(objItem.Name,objItem.Attribute)
        Comment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        Comment[dlgdata.id] = dlgdata.data
        FreeCAD.ActiveDocument.Begin = json.dumps(Comment)
        pass





