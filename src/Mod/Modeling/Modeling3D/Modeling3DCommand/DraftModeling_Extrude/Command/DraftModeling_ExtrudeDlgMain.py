# -*- coding: UTF-8 -*-
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import FreeCAD,FreeCADGui
from Modeling3DCommand.DraftModeling_Extrude.UI import DraftModeling_ExtrudeDlg
from Modeling.Common.Tools import UnitTools,ObjectsTools,CoordinateSystemTools,DocumentTools
import Modeling3DCommand as Model
import DraftModeling_ExtrudeInstance as Instance
import CreateDraftModeling_Extrude as createObj
import time
import re
from Modeling3D.Tools import  RebuildForUITools,ModelingByUITools

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
# from Modeling.Common.CommonCommand.NewDocument import ObjectDict,NewDocument
class DraftModeling_Extrude(QtGui.QDialog):
    def __init__(self,baseArea=None, obj=None):
        QtGui.QDialog.__init__(self)
        self.ui = DraftModeling_ExtrudeDlg.Ui_Dialog_DraftModeling_Extrude()
        self.ui.setupUi(self)
        self.obj=obj
        self.baseArea=baseArea
        #这里用一个标志位来控制refreshShape函数是否执行，在双击打开的面板的时候不需要执行
        self.flagRefresh=True
        self.baseAreaLabel=""
        self.initCombox()

        # 根据默认单位初始化填充
        units=FreeCAD.Units.getDefaultUnits()
        if units[0]==0:
            self.ui.lineEdit_length.setText("2mm")
            self.ui.lineEdit_addStride.setText("2mm")
        elif units[0]==1:
            self.ui.lineEdit_length.setText("2cm")
            self.ui.lineEdit_addStride.setText("2cm")
        else:
            self.ui.lineEdit_length.setText("2m")
            self.ui.lineEdit_addStride.setText("2m")
        FreeCAD.Console.PrintMessage(str(baseArea.Label)+"\n")
        # 初始化面
        if self.baseArea:
            self.ui.comboBox_Areas.setCurrentIndex(self.ui.comboBox_Areas.findText(str(baseArea.Label)))
            self.baseAreaLabel=self.baseArea.Label

        # sayz("0",str(self.ui.comboBox_Areas.findText(str(baseArea.Label))))
        # sayzError("0",str(self.ui.comboBox_Areas.currentIndex()))


        if not self.obj:
            self.obj=createObj.createDraftModeling_Extrude(area=str(self.ui.comboBox_Areas.currentText()),length="2mm")
            self.baseAreaLabel=str(self.ui.comboBox_Areas.currentText())

        #刷新
        self.refreshDlg()

        self.ui.pushButton_ok.clicked.connect(self.pushBtnOk)
        self.ui.pushButton_cancel.clicked.connect(self.pushBtnCancel)

        # self.ui.comboBox_Areas.currentIndexChanged.connect(self.refreshShape)
        # self.ui.lineEdit_length.textChanged.connect(self.refreshShape)
        # self.ui.ComboBox_Shadow_Attribute.currentIndexChanged.connect(self.refreshShape)

    def setFalgRefresh(self,flag=True):
        self.flagRefresh=flag

    def refreshDlg(self):
        # self.initCombox()
        FreeCAD.Console.PrintMessage("self.obj.Area "+str(self.baseAreaLabel)+"\n")
        self.baseAreaLabel=str(self.ui.comboBox_Areas.currentText())
        #刷新面板
        self.ui.comboBox_Areas.setCurrentIndex(self.ui.comboBox_Areas.findText(self.baseAreaLabel))
        self.ui.LineEdit_Name.setText(self.obj.Label)
        # self.ui.ComboBox_Shadow_Attribute.setCurrentIndex(self.obj.Attribute)
        attributeText=""
        if self.obj.Attribute==ObjectsTools.Attribute.NotDefine:
            attributeText=u"未定义"
        elif self.obj.Attribute==ObjectsTools.Attribute.Conductor:
            attributeText=u"理想导体"
        elif self.obj.Attribute==ObjectsTools.Attribute.Custom:
            attributeText=u"自定义"
        elif self.obj.Attribute==ObjectsTools.Attribute.Vacuo:
            attributeText=u"真空"
        self.ui.ComboBox_Shadow_Attribute.setCurrentIndex(self.ui.ComboBox_Shadow_Attribute.findText(attributeText))

        self.ui.lineEdit_length.setText(ObjectsTools.turnPropertyToExpression(self.obj,"Length"))
        RebuildForUITools.fillUniformGridByObj(self.ui,self.obj)
        # if FreeCAD.ActiveDocument.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
        #     self.ui.checkBox_UniformX.setChecked(self.obj.X)
        #     self.ui.checkBox_UniformY.setChecked(self.obj.Y)
        #     self.ui.checkBox_UniformZ.setChecked(self.obj.Z)
        # elif FreeCAD.ActiveDocument.CoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:

        # self.ui.lineEdit_UniformX.setText(self.obj.)
        #填充非均匀网格数据
        RebuildForUITools.fillUniformGridByObj(self.ui,self.obj)

    def initCombox(self):
        if self.obj:
            self.baseAreaLabel=str(self.obj.Area)
        #现将下拉项置空
        self.ui.comboBox_Areas.clear()
        areas=ObjectsTools.getAreasByDoc(FreeCAD.ActiveDocument)
        self.ui.comboBox_Areas.addItems(areas)
        FreeCAD.Console.PrintMessage("self.baseArea "+str(self.baseArea)+"\n")
        self.ui.comboBox_Areas.setCurrentIndex(self.ui.comboBox_Areas.findText(self.baseAreaLabel))
        # for areaItem in areas:
        #     self.ui.comboBox_Areas.addItem(areaItem)
    def getAddStride(self):
        addStrideStr= str(self.ui.lineEdit_addStride.text())
        return addStrideStr

    def refreshShape(self):
        if not self.flagRefresh:
            return
        areaLabel=str(self.ui.comboBox_Areas.currentText())
        length=str(self.ui.lineEdit_length.text().replace(" ",""))
        if not self.obj:
            #创建对应的体
            self.obj=createObj.createDraftModeling_Extrude(obj=None,area=areaLabel,length=length)
        else:
            self.obj.Area=areaLabel
            ModelingByUITools.setValue(self.obj,"Length",str(length))

        ModelingByUITools.setAttributeValue(self.obj,self.ui.ComboBox_Shadow_Attribute.currentIndex())
        # FreeCAD.ActiveDocument.recompute()

    def pushBtnOk(self):
        self.refreshShape()
        DocumentTools.updateBoolean()
        self.close()
        pass
    def pushBtnCancel(self):
        self.close()
        pass

dialogAndObj={}

class CreateNewDraftModeling_ExtrudeCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        '''
        1、 如果没有选择任何模型：弹出对话框提示先选择面
        2、 如果选择的模型大于1个：弹出对话框提示只能选择一个模型
        3、 如果只选择了一个模型：
            a、如果选择的模型是面属性，开始拉伸操作
            b、如果选择的模型不是面属性，提示
        
        '''
        selectObjs=FreeCADGui.Selection.getCompleteSelection()
        if len(selectObjs)==0:
            DocumentTools.errorMessage(u"请先选择一个面或者拉伸草图模型!\n")
            return
        elif len(selectObjs)>1:
            DocumentTools.errorMessage(u"不能选择多个对象！\n")
            return
        else:
            objSele=selectObjs[0]
            if not hasattr(objSele,"Type"):
                DocumentTools.errorMessage(u"请选择正确的模型对象\n")
                return
            else:
                #选择的是面
                if objSele.Type in [ObjectsTools.ObjectType.Area_Conformal,ObjectsTools.ObjectType.Area_Rectangular]:
                    dlg=DraftModeling_Extrude(baseArea=objSele)

                    if not hasattr(dlg.obj.Proxy,"dialog"):
                        setattr(dlg.obj.Proxy,"dialog",dlg)
                    dlg.obj.Proxy.dialog=dlg
                    #将当前选择的模型选为拉伸体
                    FreeCADGui.Selection.clearSelection()
                    FreeCADGui.Selection.addSelection(dlg.obj)

                    dlg.setModal(False)
                    dlg.show()
                    
                    # dlg.exec_()
                    # dlg.exec_()
                    # global dialogAndObj

                    # dialogAndObj[dlg.obj,dlg]
                #选择的是草图拉伸体
                elif objSele.Type == ObjectsTools.ObjectType.Vol_Draft_Extrude:
                    # global dialogAndObj
                    if not hasattr(objSele.Proxy,"dialog"):
                        dlg=DraftModeling_Extrude(obj=objSele)
                        setattr(objSele.Proxy,"dialog",dlg)

                    dlg=objSele.Proxy.dialog
                    # 模型的dialog是否可见？
                    if not objSele.Proxy.dialog.isVisible():
                        dlg.setModal(False)
                        dlg.setFalgRefresh(flag=False)
                        #刷新下拉项
                        dlg.initCombox()
                        dlg.refreshDlg()
                        dlg.setFalgRefresh(flag=True)
                        #
                        dlg.show()
                        # dlg.exec_()
                        # dlg.exec_()
                    else:
                        #每次length+2mm
                        # ModelingByUITools.setValue(objSele,"Length",str(objSele.Length.Value+dlg.getAddStride()))
                        # FreeCAD.Console.PrintError(str(UnitTools.turnNormalUnitToShowUnit(UnitTools.SupportUnitType.Length,str(objSele.Length.Value))+"+("+str(dlg.getAddStride())+")"))

                        ModelingByUITools.setValueNew(objSele,"Length",str(UnitTools.turnNormalUnitToShowUnit(UnitTools.SupportUnitType.Length,str(objSele.Length.Value))+"+("+str(dlg.getAddStride())+")"))
                        objSele.recompute()
                        dlg.refreshDlg()
                        pass

        # dlg=DraftModeling_Extrude()
        # FreeCAD.Console.PrintError(dlg.isVisible())
        # dlg.show()
        # # dlg.exec_()
        # dlg.exec_()
        # FreeCAD.Console.PrintError(dlg.isVisible())

    def GetResources(self):
        # IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_ParamArray.svg"
        IconPath =  FreeCAD.ConfigGet("AppHomePath") +"Mod/Modeling/Modeling3D/Modeling3DResources/DraftExtrusion.svg"

        MenuText = QT_TRANSLATE_NOOP(
            'CreateNewDraftModeling_ExtrudeCommand',
            'Create Extrude Draft Model')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateNewDraftModeling_ExtrudeCommand',
            'Create Extrude Draft Model')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip,
                'Accel':"E"}


FreeCADGui.addCommand('CreateNewDraftModeling_ExtrudeCommand',CreateNewDraftModeling_ExtrudeCommand())

def sayz(flag,msg):
    FreeCAD.Console.PrintMessage("\n"+str(flag)+" ")
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")
def sayzError(flag,msg):
    FreeCAD.Console.PrintError("\n"+str(flag)+" ")
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintMessage("\n")
