# -*- coding: UTF-8 -*-
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import FreeCAD,FreeCADGui
from Modeling3DCommand.Area_Function.UI import Area_FunctionDlg
from Modeling.Common.Tools import UnitTools,ObjectsTools,CoordinateSystemTools,DocumentTools
import Modeling3DCommand as Model
import AreaFunctionInstance as Instance
import CreateAreaFunction as createObj
import time
import re
import FreeCAD
from Modeling3D.Tools import  RebuildForUITools,ModelingByUITools
# from Modeling.Common.CommonCommand.NewDocument import ObjectDict,NewDocument
class AreaFunctionDlgMain(QtGui.QDialog):
    def __init__(self, obj=None):
        QtGui.QDialog.__init__(self)
        self.ui = Area_FunctionDlg.Ui_Dialog_AreaFunction()
        self.ui.setupUi(self)
        self.obj=obj

        self.currentCoordinate=FreeCAD.ActiveDocument.CoordinateSystem

        # 设置相关坐标
        Coordi_Name = RebuildForUITools.getCoordinateName(self.currentCoordinate)
        self.ui.label_12.setText(
            QtGui.QApplication.translate("Dialog_AreaFunction", Coordi_Name[0], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_13.setText(QtGui.QApplication.translate("Dialog_AreaFunction", Coordi_Name[1], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_14.setText(QtGui.QApplication.translate("Dialog_AreaFunction", Coordi_Name[2], None, QtGui.QApplication.UnicodeUTF8))

        # 单位问题
        units =  FreeCAD.Units.getDefaultUnits()
        if units[0]==0:
            unit_len="mm"
        elif units[0]==1:
            unit_len="cm"
        elif units[0]==2:
            unit_len="m"

        if units[1]==0:
            unit_ang="rad"
        elif units[1]==1:
            unit_ang="deg"

        self.ui.lineEdit_Point_1X.setText(str(-1)+unit_len)
        self.ui.lineEdit_Point_1Y.setText(str(-1) + unit_len)
        self.ui.lineEdit_Point_1Z.setText(str(-1) + unit_len)

        self.ui.lineEdit_Point_2X.setText(str(-1) + unit_len)
        self.ui.lineEdit_Point_2Y.setText(str(-1) + unit_len)
        self.ui.lineEdit_Point_2Z.setText(str(-1) + unit_len)

        if FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            self.ui.lineEdit_Point_1Y.setText(str(-1) + unit_ang)
            self.ui.lineEdit_Point_2Y.setText(str(-1) + unit_ang)
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Cylindrical":
            self.ui.lineEdit_Point_1Z.setText(str(-1) + unit_ang)
            self.ui.lineEdit_Point_2Z.setText(str(-1) + unit_ang)


        # 如果obj！=None
        if obj:
            self.ui.lineEdit_Name.setText(obj.Label)
            self.ui.spinBox_Order.setValue(obj.Order)
            # 重建非均匀网格属性
            RebuildForUITools.fillUniformGridByObj(self.ui,obj)
            # 重建模型属性
            self.ui.lineEdit_Point_1X.setText(str(ObjectsTools.turnPropertyToExpression(obj,"Point_1")[0]))
            self.ui.lineEdit_Point_1Y.setText(str(ObjectsTools.turnPropertyToExpression(obj,"Point_1")[1]))
            self.ui.lineEdit_Point_1Z.setText(str(ObjectsTools.turnPropertyToExpression(obj,"Point_1")[2]))
            self.ui.lineEdit_Point_2X.setText(str(ObjectsTools.turnPropertyToExpression(obj,"Point_2")[0]))
            self.ui.lineEdit_Point_2Y.setText(str(ObjectsTools.turnPropertyToExpression(obj,"Point_2")[1]))
            self.ui.lineEdit_Point_2Z.setText(str(ObjectsTools.turnPropertyToExpression(obj,"Point_2")[2]))

            self.ui.lineEdit_ExpressionStr.setText(obj.Expression)
            self.ui.spinBox_Precision.setValue(obj.Precision)
            pass
        else:
            pass

        self.ui.pushButton_ok.clicked.connect(self.onPushOkBtn)
        self.ui.pushButton_cancel.clicked.connect(self.onPushCancelBtn)

    def onPushOkBtn(self):
        if not self.obj:
            self.obj=createObj.createFunctionArea()

        self.obj.Label=str(self.ui.lineEdit_Name.text())
        self.obj.Order=int(self.ui.spinBox_Order.value())

        ModelingByUITools.setDX1DX2DX3Value(self.obj,self.ui)

        ModelingByUITools.setValue(self.obj,"Point_1.x",str(self.ui.lineEdit_Point_1X.text()))
        ModelingByUITools.setValue(self.obj,"Point_1.y",str(self.ui.lineEdit_Point_1Y.text()))
        ModelingByUITools.setValue(self.obj,"Point_1.z",str(self.ui.lineEdit_Point_1Z.text()))

        ModelingByUITools.setValue(self.obj,"Point_2.x",str(self.ui.lineEdit_Point_2X.text()))
        ModelingByUITools.setValue(self.obj,"Point_2.y",str(self.ui.lineEdit_Point_2Y.text()))
        ModelingByUITools.setValue(self.obj,"Point_2.z",str(self.ui.lineEdit_Point_2Z.text()))

        self.obj.Expression=str(self.ui.lineEdit_ExpressionStr.text())

        self.obj.Precision=int(self.ui.spinBox_Precision.value())

        self.obj.recompute()
        self.close()
        pass
    def onPushCancelBtn(self):
        self.close()
        pass