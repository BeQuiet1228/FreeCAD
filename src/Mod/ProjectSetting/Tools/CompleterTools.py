# -*- coding: utf-8 -*-
from PySide import QtGui
from PySide.QtGui import QCompleter,QStringListModel
import FreeCAD
from Modeling.Common.Tools import ObjectsTools
import Modeling

def setLineEditsCompleter(lineEdits):
    '''
    @brief:为lineEdits列表里的LineEdit对象添加补全list
    '''
    for lineEdit in lineEdits:
        lineEdit.setcompleterlist(getParamsList())
        # completer=QCompleter()
        # lineEdit.setCompleter(completer)
        # model=QStringListModel()
        # model.setStringList(getParamsList())
        # completer.setModel(model)

def getParamsList():
    '''
    @brief:获得参数体的所有参数以及步长参数
    '''
    paramObj=ObjectsTools.getParamObj()
    paramsList=[]
    if  paramObj:
        params=paramObj.DynamicData
        paramsExtra=["DX1","DX2","DX3"]
        paramsList=params+paramsExtra
    return paramsList


def getAllLineEdits(ui):
    '''
    @brief:获得UI中的所有LineEdit控件对象list
    '''
    lineEdits=[]
    for attr in dir(ui):
        if isinstance(getattr(ui,attr),Modeling.Common.Tools.Completer.AutoCompleteEdit):
            lineEdits.append(getattr(ui,attr))
    return lineEdits