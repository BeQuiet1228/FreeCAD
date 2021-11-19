# -*- coding: UTF-8 -*-
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import FreeCAD,FreeCADGui
from Modeling3DCommand.Vol_Revolution.UI import Vol_RevolutionDlg
from Modeling.Common.Tools import UnitTools,ObjectsTools,CoordinateSystemTools,DocumentTools,BaseObjDialog
import Modeling3DCommand as Model
import RevolutionInstance as Instance
import time
import re
from Modeling3D.Tools import  RebuildForUITools,ModelingByUITools
import CreateRevolution as createObj
# from Modeling.Common.CommonCommand.NewDocument import ObjectDict,NewDocument
class VolRevolotion(QtGui.QDialog):
    def __init__(self, obj=None):
        QtGui.QDialog.__init__(self)
        self.ui = Vol_RevolutionDlg.Ui_Dialog_VolRevolution()
        self.ui.setupUi(self)

        # 设置下拉选项
        self.ui.lineEdit_PointBaseX.setcompleterlist(BaseObjDialog.getGlobalVar())
        self.ui.lineEdit_PointBaseY.setcompleterlist(BaseObjDialog.getGlobalVar())
        self.ui.lineEdit_PointBaseZ.setcompleterlist(BaseObjDialog.getGlobalVar())
        self.ui.lineEdit_PointTopX.setcompleterlist(BaseObjDialog.getGlobalVar())
        self.ui.lineEdit_PointTopY.setcompleterlist(BaseObjDialog.getGlobalVar())
        self.ui.lineEdit_PointTopZ.setcompleterlist(BaseObjDialog.getGlobalVar())

        self.initCombox()
        # 消息绑定
        self.ui.pushButton_ok.clicked.connect(self.pushBtnOk)
        self.ui.pushButton_cancel.clicked.connect(self.pushButton_cancel)

        # 设置默认标签和单位
        units = FreeCAD.Units.getDefaultUnits()
        if units[0] == 0:
            self.ui.lineEdit_PointBaseX.setText("0mm")
            self.ui.lineEdit_PointBaseY.setText("0mm")
            self.ui.lineEdit_PointBaseZ.setText("0mm")

            self.ui.lineEdit_PointTopX.setText("0mm")
            self.ui.lineEdit_PointTopY.setText("1mm")
            self.ui.lineEdit_PointTopZ.setText("0mm")
        elif units[0] == 1:
            self.ui.lineEdit_PointBaseX.setText("0cm")
            self.ui.lineEdit_PointBaseY.setText("0cm")
            self.ui.lineEdit_PointBaseZ.setText("0cm")

            self.ui.lineEdit_PointTopX.setText("0cm")
            self.ui.lineEdit_PointTopY.setText("1cm")
            self.ui.lineEdit_PointTopZ.setText("0cm")
        else:
            self.ui.lineEdit_PointBaseX.setText("0m")
            self.ui.lineEdit_PointBaseY.setText("0m")
            self.ui.lineEdit_PointBaseZ.setText("0m")

            self.ui.lineEdit_PointTopX.setText("0m")
            self.ui.lineEdit_PointTopY.setText("1m")
            self.ui.lineEdit_PointTopZ.setText("0m")
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            pass
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            self.ui.label_5.setText("R")
            self.ui.label_6.setText("Theta")
            self.ui.label_7.setText("Z")
            if units[1]==0:
                self.ui.lineEdit_PointBaseY.setText("0deg")
                self.ui.lineEdit_PointTopY.setText("1deg")
            else:
                self.ui.lineEdit_PointBaseY.setText("0rad")
                self.ui.lineEdit_PointTopY.setText("0rad")
        else:
            self.ui.label_5.setText("Z")
            self.ui.label_6.setText("R")
            self.ui.label_7.setText("Theta")
            if units[1]==0:
                self.ui.lineEdit_PointBaseZ.setText("0deg")
                self.ui.lineEdit_PointTopZ.setText("1deg")
            else:
                self.ui.lineEdit_PointBaseZ.setText("0rad")
                self.ui.lineEdit_PointTopZ.setText("0rad")

        self.obj=obj
        #如果obj存在则，按照obj进行重建面板
        if obj:
            self.ui.comboBox_Areas.setCurrentIndex(self.ui.comboBox_Areas.findText(str(obj.Area)))
            self.ui.lineEdit_name.setText(obj.Label)
            self.ui.spinBox_Order.setValue(obj.Order)
            #重建非均匀网格属性
            RebuildForUITools.fillUniformGridByObj(self.ui,obj)
            #重建模型属性
            point_Base=ObjectsTools.turnPropertyToExpression(obj,"Point_Base")
            point_Top=ObjectsTools.turnPropertyToExpression(obj,"Point_Top")
            self.ui.lineEdit_PointBaseX.setText(str(point_Base[0]))
            self.ui.lineEdit_PointBaseY.setText(str(point_Base[1]))
            self.ui.lineEdit_PointBaseZ.setText(str(point_Base[2]))

            self.ui.lineEdit_PointTopX.setText(str(point_Top[0]))
            self.ui.lineEdit_PointTopY.setText(str(point_Top[1]))
            self.ui.lineEdit_PointTopZ.setText(str(point_Top[2]))
        else:
            # 如果没有物体就跟着默认来
            pass

    def initCombox(self):
        areas=ObjectsTools.getAreasByDoc(FreeCAD.ActiveDocument)
        for areaItem in areas:
            self.ui.comboBox_Areas.addItem(areaItem)

    def pushBtnOk(self):
        # sayz(self.obj)
        if not self.obj:
            self.obj=createObj.createRevolution()
        self.obj.Label=str(self.ui.lineEdit_name.text())
        self.obj.Order=int(self.ui.spinBox_Order.value())
        ModelingByUITools.setDX1DX2DX3Value(self.obj,self.ui)
        ModelingByUITools.setPointValue(self.obj,"Point_Base",str(self.ui.lineEdit_PointBaseX.text()),
                                                               str(self.ui.lineEdit_PointBaseY.text()),
                                                               str(self.ui.lineEdit_PointBaseZ.text()))
        ModelingByUITools.setPointValue(self.obj,"Point_Top",str(self.ui.lineEdit_PointTopX.text()),
                                                               str(self.ui.lineEdit_PointTopY.text()),
                                                               str(self.ui.lineEdit_PointTopZ.text()))
        self.obj.Area=str(self.ui.comboBox_Areas.currentText())
        self.obj.recompute()
        self.close()

    def pushButton_cancel(self):
        self.close()
        
def sayz(msg):
    FreeCAD.Console.PrintMessage("\n")   
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")        

        







