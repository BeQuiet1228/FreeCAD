# -*- coding: UTF-8 -*-
import traceback

from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import FreeCAD,FreeCADGui
from Modeling3DCommand.DraftModeling_Revolution.UI import DraftModeling_RevolutionDlg
from Modeling.Common.Tools import UnitTools,ObjectsTools,CoordinateSystemTools,DocumentTools
import Modeling3DCommand as Model
import DraftModeling_RevolutionInstance as Instance
import CreateDraftModeling_Revolution as createObj
import time
import re
from Modeling3D.Tools import  RebuildForUITools,ModelingByUITools

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
# from Modeling.Common.CommonCommand.NewDocument import ObjectDict,NewDocument
class DraftModeling_Revolution(QtGui.QDialog):
    def __init__(self,baseArea=None, obj=None):
        QtGui.QDialog.__init__(self)
        self.ui = DraftModeling_RevolutionDlg.Ui_Dialog_DraftModeling_Revolution()
        self.ui.setupUi(self)
        self.obj=obj
        self.baseArea=baseArea
        self.baseAreaLabel=""
        self.initCombox()
        #判断是否需要刷新图形
        self.flagRefresh=True
        # 用于判断ui是否是第一次打开
        self.isKeepData=False

        # 改变坐标系标签
        if FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            self.ui.label_4.setText("R")
            self.ui.label_5.setText("Theta")
            self.ui.label_6.setText("Z")
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Cylindrical":
            self.ui.label_4.setText("Z")
            self.ui.label_5.setText("R")
            self.ui.label_6.setText("Theta")
        else:
            pass




        # 初始化面
        if self.baseArea:
            self.ui.comboBox_Areas.setCurrentIndex(self.ui.comboBox_Areas.findText(str(self.baseArea.Label)))

        if not self.obj:
            self.obj=createObj.createDraftModeling_Revolution(area=str(self.ui.comboBox_Areas.currentText()))
            self.baseAreaLabel=str(self.ui.comboBox_Areas.currentText())
        #刷新
        self.refreshDlg()
      
        self.ui.pushButton_ok.clicked.connect(self.pushBtnOk)
        self.ui.pushButton_cancel.clicked.connect(self.pushBtnCancel)

        # self.ui.comboBox_Areas.currentIndexChanged.connect(self.refreshShape)
        # self.ui.lineEdit_PointBaseX.textChanged.connect(self.refreshShape)
        # self.ui.lineEdit_PointBaseY.textChanged.connect(self.refreshShape)
        # self.ui.lineEdit_PointBaseZ.textChanged.connect(self.refreshShape)
        # self.ui.lineEdit_PointTopX.textChanged.connect(self.refreshShape)
        # self.ui.lineEdit_PointTopY.textChanged.connect(self.refreshShape)
        # self.ui.lineEdit_PointTopZ.textChanged.connect(self.refreshShape)
        # self.ui.ComboBox_Shadow_Attribute.currentIndexChanged.connect(self.refreshShape)

    def refreshDlg(self):
        # self.initCombox()
        #刷新面板
        FreeCAD.Console.PrintMessage("self.baseArea: "+str(self.baseAreaLabel)+"\n")
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

        #重建非均匀网格属性
        RebuildForUITools.fillUniformGridByObj(self.ui,self.obj)
        #重建模型属性
        point_Base=ObjectsTools.turnPropertyToExpression(self.obj,"Point_Base")
        point_Top=ObjectsTools.turnPropertyToExpression(self.obj,"Point_Top")
        FreeCAD.Console.PrintError("\n设置草图——旋转体")
        # 在柱坐标系下点的坐标位置可能不太一样
        if FreeCAD.ActiveDocument.CoordinateSystem == u'Cylindrical':
            self.ui.lineEdit_PointBaseX.setText(str(point_Base[2]))
            self.ui.lineEdit_PointBaseY.setText(str(point_Base[0]))
            self.ui.lineEdit_PointBaseZ.setText(str(point_Base[1]))

            self.ui.lineEdit_PointTopX.setText(str(point_Top[2]))
            self.ui.lineEdit_PointTopY.setText(str(point_Top[0]))
            self.ui.lineEdit_PointTopZ.setText(str(point_Top[1]))
        else:
            self.ui.lineEdit_PointBaseX.setText(str(point_Base[0]))
            self.ui.lineEdit_PointBaseY.setText(str(point_Base[1]))
            self.ui.lineEdit_PointBaseZ.setText(str(point_Base[2]))

            self.ui.lineEdit_PointTopX.setText(str(point_Top[0]))
            self.ui.lineEdit_PointTopY.setText(str(point_Top[1]))
            self.ui.lineEdit_PointTopZ.setText(str(point_Top[2]))

        # self.ui.lineEdit_UniformX.setText(self.obj.)
        #填充非均匀网格数据
        RebuildForUITools.fillUniformGridByObj(self.ui,self.obj)

    def initCombox(self):
        # self.flagRefresh=False
        if self.obj:
            self.baseAreaLabel=self.obj.Area
            # self.baseArea=str(self.obj.Area)
        #现将下拉项置空
        self.ui.comboBox_Areas.clear()
        areas=ObjectsTools.getAreasByDoc(FreeCAD.ActiveDocument)
        FreeCAD.Console.PrintMessage(areas)
        self.ui.comboBox_Areas.addItems(areas)
        # self.flagRefresh=True

        # for areaItem in areas:
        #     self.ui.comboBox_Areas.addItem(areaItem)
    def getAddStride(self):
        addStrideStr= str(self.ui.lineEdit_addStride.text())
        return UnitTools.getValueByStr(addStrideStr)
    def closeEvent(self,event):
        self.draftLine.finish()
        # 关闭网格
        if hasattr(FreeCADGui,"Snapper"):
            FreeCADGui.Snapper.hide()
        closeGrid()
        FreeCAD.ActiveDocument.recompute()
        sayzError("close")

    def refreshShape(self):
        # if not self.flagRefresh:
        #     return
        closeGrid()
        areaLabel=str(self.ui.comboBox_Areas.currentText())
        self.obj.Area=areaLabel
        ModelingByUITools.setPointValue(self.obj,"Point_Base",str(self.ui.lineEdit_PointBaseX.text()),\
                                                               str(self.ui.lineEdit_PointBaseY.text()),\
                                                               str(self.ui.lineEdit_PointBaseZ.text()))
        
        ModelingByUITools.setPointValue(self.obj,"Point_Top",str(self.ui.lineEdit_PointTopX.text()),\
                                                               str(self.ui.lineEdit_PointTopY.text()),\
                                                               str(self.ui.lineEdit_PointTopZ.text()))
        # self.obj.recompute()
        self.obj.Proxy.redraw(self.obj)
        FreeCADGui.ActiveDocument.getObject(self.obj.Name).Visibility=True

        if hasattr(FreeCADGui,"Snapper"):
            FreeCADGui.Snapper.hide()
        ModelingByUITools.setAttributeValue(self.obj,self.ui.ComboBox_Shadow_Attribute.currentIndex())
        # FreeCAD.ActiveDocument.recompute()
        # self.obj.recompute()
        # FreeCAD.ActiveDocument.recompute()
        # FreeCADGui.SendMsgToActiveView("ViewSelection")

    def pushBtnOk(self):
        # 更新Label
        self.obj.Label = self.ui.LineEdit_Name.text()
        self.refreshShape()
        try:
            # DocumentTools.updateBoolean()
            import PartChipic
            PartChipic.updateBoolean(self.obj.Order, 1)
        except:
            FreeCAD.Console.PrintError(traceback.format_exc())
        # try:
        RebuildForUITools.fillUniformGridToObj(self.ui, self.obj)
        # except:
        #     FreeCAD.Console.PrintMessage('\n 设置mark 失败 \n')
        # ModelingByUITools.setAttributeValue(self.obj,self.ui.ComboBox_Shadow_Attribute.currentIndex())
        self.isKeepData=True

        self.close()

    def pushBtnCancel(self):
        self.close()
        # 当体是首次打开时，即通过按钮打开时，点击取消会删除当前的体，当在树结构打开，点击取消不会删除当前体
        if not self.isKeepData:
            doc = FreeCAD.ActiveDocument
            doc.removeObject(self.obj.Name)
        # 当体是首次打开时，即通过按钮打开时，点击取消会删除当前的体 @ lzg
        # if not self.baseArea == None:
        #     doc = FreeCAD.ActiveDocument
        #     doc.removeObject(self.obj.Name)
        #     sayz("这里调用了吗")
        pass
# 关闭选点的网格
def closeGrid():
    if hasattr(FreeCADGui,"Snapper"):
        if FreeCADGui.Snapper.grid:
            FreeCADGui.Snapper.respawnGrid()
            if FreeCADGui.Snapper.grid.Visible:
                FreeCADGui.Snapper.grid.off()
                FreeCADGui.Snapper.forceGridOff=True

class CreateNewDraftModeling_RevolutionCommand:
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
        # Line().Activated()

        selectObjs=FreeCADGui.Selection.getCompleteSelection()
        if len(selectObjs)==0:
            DocumentTools.errorMessage(u"请先选择一个面!\n")
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
                if objSele.Type in [ObjectsTools.ObjectType.Area_Conformal,\
                                    ObjectsTools.ObjectType.Area_Rectangular,\
                                        ObjectsTools.ObjectType.Area_Function,\
                                            ObjectsTools.ObjectType.Area_Polygonal]:

                    dlg=DraftModeling_Revolution(baseArea=objSele)

                    if not hasattr(dlg.obj.Proxy,"dialog"):
                        setattr(dlg.obj.Proxy,"dialog",dlg)
                    dlg.obj.Proxy.dialog=dlg

                    #将当前选择的模型选为拉伸体
                    FreeCADGui.Selection.clearSelection()
                    FreeCADGui.Selection.addSelection(dlg.obj)
                    #设置现在的旋转体不可见
                    FreeCADGui.ActiveDocument.getObject(dlg.obj.Name).Visibility=False
                
                    dlg.setModal(False)
                    dlg.show()
                    # 操作提示
                    DocumentTools.errorMessage(u"选中该旋转体后，再次点击旋转按钮或者按下‘R’，在场景中选取两个点，旋转轴以这两个点的连线作为旋转轴\n")

                #选择的是草图旋转体
                elif objSele.Type == ObjectsTools.ObjectType.Vol_Draft_Revolution:
                    # global dialogAndObj
                    if not hasattr(objSele.Proxy,"dialog"):
                        dlg=DraftModeling_Revolution(obj=objSele)
                        setattr(objSele.Proxy,"dialog",dlg)

                    dlg=objSele.Proxy.dialog
                    # 模型的dialog是否可见？
                    if not objSele.Proxy.dialog.isVisible():
                        dlg.setModal(False)
                        dlg.initCombox()
                        dlg.refreshDlg()
                        dlg.show()
                        # dlg.exec_()
                        # dlg.exec_()
                    else:
                        #每次点击选择线
                        # 将面置为可见，体置为不可见
                        FreeCADGui.ActiveDocument.getObject(dlg.baseArea.Name).Visibility=True
                        FreeCADGui.ActiveDocument.getObject(dlg.obj.Name).Visibility=False
                        
                        self.setTheCameraToArea(dlg.baseArea)

                        from Draft import DraftTools
                        draftLine=DraftTools.Line(dlg=dlg)
                        #
                        if not hasattr(dlg,"draftLine"):
                            setattr(dlg,"draftLine",draftLine)
                        setattr(dlg,"draftLine",draftLine)
                        draftLine.Activated()
                        # Line().Activated()
                        # line=Line().Activated()
                        # self.call = self.view.addEventCallback("SoEvent",self.action)
                        # ModelingByUITools.setValue(objSele,"Length",str(objSele.Length.Value+dlg.getAddStride()))
                        # objSele.recompute()
                        # dlg.refreshDlg()
                        pass
                else:
                    DocumentTools.errorMessage(u"请选择正确的模型对象\n")
    def setTheCameraToArea(self,faceObj):
        #将摄像机对准面的法向

        ##面的法向
        face=faceObj.Shape.Faces[0]
        normalFace=face.normalAt(1,1)
        # FreeCADGui.ActiveDocument.ActiveView.setCameraOrientation(faceObj.Placement.Rotation)
        cam = FreeCADGui.ActiveDocument.ActiveView.getCameraNode()
        from pivy import coin
        cam.pointAt( coin.SbVec3f(normalFace), coin.SbVec3f(0.0,0.0,1.0))
        FreeCADGui.Selection.addSelection(faceObj)
        FreeCADGui.SendMsgToActiveView("ViewSelection")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/DraftRevolution.svg"

        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'CreateNewDraftModeling_RevolutionCommand',
            'Create Revolution Draft Model')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'CreateNewDraftModeling_RevolutionCommand',
            'Create Revolution Draft Model')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip,
                'Accel':"R"}
FreeCADGui.addCommand('CreateNewDraftModeling_RevolutionCommand',CreateNewDraftModeling_RevolutionCommand())

def sayz(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")

def sayzError(msg):
    FreeCAD.Console.PrintError(msg)
    FreeCAD.Console.PrintError("\n")
