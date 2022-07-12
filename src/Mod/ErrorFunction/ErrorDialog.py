# -*- coding: utf-8 -*-
import FreeCAD
from PySide import QtGui,QtCore
import warning
import re

class WarningDialog(QtGui.QDialog):
    def __init__(self,parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.ui=warning.Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.ui.OK.clicked.connect(self.close)
    def daasd(self):
        pass
    def errormassageinput(self,str1):
        self.ui.textEdit.setText(str1)

# class showCylinderDialog(QtGui.QDialog):
#     def __init__(self,obj,parent=None):
#         QtGui.QDialog.__init__(self,parent)
#         self.ui=CylinderDialog.Ui_Dialog()
#         self.ui.setupUi(self)
# class ErrorChecking:
#     def __init__(self,str1):
#         pass
#     def strtolist(str1):
#         list1=re.split(r'([+-/*])',str1)

#报错功能的检索大致分为几类
#1.连续使用运算符号
#2.使用的变量不存在
#3.9m9

