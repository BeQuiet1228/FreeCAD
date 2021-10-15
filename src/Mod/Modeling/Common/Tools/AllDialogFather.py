# -*- coding: UTF-8 -*-
from PySide import QtGui,QtCore
from enum import Enum
import FreeCAD
import json
from Modeling.Common.Tools.ObjectsTools import *
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
#对话框类型
class DialogType(Enum):
    #空对话框
    NULL_DIALOG = 0
    #模型参数对话框
    MODEL_DIALOG = 1
    #物理参数对话框
    PHYSICS_DIALOG = 2
#所有对话框的父类
class AllDialogFather(QtGui.QDialog):
    def __init__(self,obj,parent = None):
        self.dialogType = DialogType.NULL_DIALOG
        #重写子类构造函数时需要手动调用父类构造函数
        QtGui.QDialog.__init__(self,parent)

    #去重名
    #防止模型名称与边界名称、观测名称重复
    def removeRepetitionName(self):
        # FreeCAD.Console.PrintError('\n类名：  '+str(self.__class__.__name__)+'\n')
        #获取源与边界、各种观测的的名字集合
        j_document = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict)
        names = j_document.keys()
        #获取当前文档名称
        docName = FreeCAD.ActiveDocument.Name
        #通过文档名称获取所有模型的对象
        objects = getAllObjectszofThisDoc(docName)
        # 判断模型对象是否为空
        if len(objects):
            #遍历所有的模型对象，获取所有模型的名称
            for obj in objects:
                names.append(getRealNameBySplitObjectLabel(obj))
        #获取名字编辑框
        lineEdit = None
        if self.dialogType == DialogType.MODEL_DIALOG:
            lineEdit = self.ui.Base_lineEdit_1
        if self.dialogType == DialogType.PHYSICS_DIALOG:
            try:
                lineEdit = self.ui.LineEdit_Name
            except:
                lineEdit = self.ui.lineEdit_name
        #获取当前名称
        currentName = lineEdit.text()
        #检查名字是否重复，如果重复则增加后缀
        count = 1
        try:
            if self.dialogType == DialogType.PHYSICS_DIALOG:
                if self.flagUpdateItemName:
                    if not currentName == self.userNameBefore:
                        while currentName in names:
                            currentName = lineEdit.text() + str(count)
                            count+=1
                else:
                    while currentName in names:
                        currentName = lineEdit.text() + str(count)
                        count+=1
            else:
                while currentName in names:
                    currentName = lineEdit.text() + str(count)
                    count+=1
        except:
            pass
        # count = 1
        # while currentName in names:
        #        currentName = lineEdit.text() + str(count)
        #        count+=1
        #重置编辑框中的文本
        lineEdit.setText(currentName)
        # FreeCAD.Console.PrintMessage(names)


