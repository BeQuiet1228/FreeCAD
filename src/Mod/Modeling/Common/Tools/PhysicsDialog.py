# -*- coding: UTF-8 -*-
from Modeling.Common.Tools.AllDialogFather import *
import FreeCAD

class PhysicsDialog(AllDialogFather):
    def __init__(self,parent = None):
        AllDialogFather.__init__(self,parent)
        
    def initDialog(self,FreeCAD_Comment_Dict,className):
        #初始化对话框类型
        self.dialogType = DialogType.PHYSICS_DIALOG
        #链接okButton信号
        self.ui.pushButton_ok.clicked.connect( lambda: self.okButtonClincked(FreeCAD_Comment_Dict,className))
        # FreeCAD.Console.PrintError("\n执行完链接ok信号的函数")
    
    def okButtonClincked(self,FreeCAD_Comment_Dict,className):
        # FreeCAD.Console.PrintError("\n执行完onConfirm函数1111")
        self.removeRepetitionName()
        # FreeCAD.Console.PrintError("\n执行完onConfirm函数2222")
        self.onConfirm(FreeCAD_Comment_Dict,className)
        # FreeCAD.Console.PrintError("\n执行完onConfirm函数")