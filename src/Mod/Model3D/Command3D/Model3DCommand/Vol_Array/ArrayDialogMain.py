# -*- coding: utf-8 -*-
import PySide
import re
import ArrayDialog
from PySide import QtGui, QtCore
import FreeCAD, FreeCADGui
from Model3D.Tools import Tools3D
import traceback
import ArrayInstance
from Model3D.Tools import ExpressionTools3D

class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = ArrayDialog.Ui_Dialog_Vol_Array()
        self.ui.setupUi(self)
        self.end = 0
        self.setModal(False)
        self.obj = obj
        self.initDialog()
        self.currentCoordinate = FreeCAD.ActiveDocument.CoordinateSystem
        self.initFialog()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False


    def initDialog(self):
        """
        初始化界面，设置界面逻辑
        """
        self.ui.pushButton_ok.clicked.connect(self.slotOK)
        self.ui.pushButton_cancel.clicked.connect(self.slotCancel)
        try:
            self.ui.comboBox_type.currentIndexChanged.connect(self.ComboBox_type_clicked)
            # 连接信号与槽 @lizhenguang
            self.dafultsetting()
            self.ui.comboBox_type.currentIndexChanged.connect(self.dafultsetting)
            self.setFirst()
            # 设置模型初始默认值
            # self.ui.ComboBox_Shadow_Attribute.currentIndexChanged.connect(self.ComboBox_Attribute_clicked)
        except:
            Tools3D.sayz("错误：阵列体设置控件时出现错误")

    def initFialog(self):
        if self.currentCoordinate == u'Rectangular':
            for i in range(self.ui.tabWidget.count()):
                try:
                    getattr(self.ui, "label_X" + str(i)).setText("X")
                    getattr(self.ui, "label_Y" + str(i)).setText("Y")
                    getattr(self.ui, "label_Z" + str(i)).setText("Z")
                except:
                    FreeCAD.Console.PrintError("label_" + str(i) + " Wrong\n")

            self.ui.checkBox_UniformX.setText("X")
            self.ui.checkBox_UniformY.setText("Y")
            self.ui.checkBox_UniformZ.setText("Z")
        elif self.currentCoordinate == u"Polar":
            for i in range(self.ui.tabWidget.count()):
                try:
                    getattr(self.ui, "label_X" + str(i)).setText("R")
                    getattr(self.ui, "label_Y" + str(i)).setText("Theta")
                    getattr(self.ui, "label_Z" + str(i)).setText("Z")
                except:
                    FreeCAD.Console.PrintError("label_" + str(i) + " Wrong\n")

            self.ui.checkBox_UniformX.setText("R")
            self.ui.checkBox_UniformY.setText("Theta")
            self.ui.checkBox_UniformZ.setText("Z")
        else:
            for i in range(self.ui.tabWidget.count()):
                try:
                    getattr(self.ui, "label_X" + str(i)).setText("Z")
                    getattr(self.ui, "label_Y" + str(i)).setText("R")
                    getattr(self.ui, "label_Z" + str(i)).setText("Theta")
                except:
                    FreeCAD.Console.PrintError("label_" + str(i) + " Wrong\n")
                    # self.ui.label_X.setText("Z")
            # self.ui.label_Y.setText("R")
            # self.ui.label_Z.setText("Theta")

            self.ui.checkBox_UniformX.setText("Z")
            self.ui.checkBox_UniformY.setText("R")
            self.ui.checkBox_UniformZ.setText("Theta")

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        self.ui.LineEdit_Name.setText(self.obj.Label)
        Tools3D.getOrderFromObj(self.obj, self.ui)
        self.ui.ComboBox_Shadow_Attribute.setCurrentIndex(self.ui.ComboBox_Shadow_Attribute.findText(str(self.obj.Attribute)))
        self.ui.comboBox_type.setCurrentIndex(self.ui.comboBox_type.findText(str(self.obj.BaseObjType)))
        # self.ui.lineEdit_start_i.setText(ObjectsTools.turnPropertyToExpression(obj, "IFrom"))
        # self.ui.lineEdit_end_i.setText(ObjectsTools.turnPropertyToExpression(obj, "ITo"))
        # 参数处理部分后续补充 现在先用一个替代方案测试
        self.ui.lineEdit_start_i.setText(str(self.obj.IFrom))
        self.ui.lineEdit_end_i.setText(str(self.obj.ITo))
        # self.setFirst()
        self.ui.lineEdit_UniformX.setText(str(self.obj.MarkX).replace(' ', ''))
        self.ui.lineEdit_UniformY.setText(str(self.obj.MarkY).replace(' ', ''))
        self.ui.lineEdit_UniformZ.setText(str(self.obj.MarkZ).replace(' ', ''))
        self.ui.checkBox_UniformX.setChecked(self.obj.isMarkX)
        self.ui.checkBox_UniformY.setChecked(self.obj.isMarkY)
        self.ui.checkBox_UniformZ.setChecked(self.obj.isMarkZ)
        # self.dafultsetting()
        self.ComboBox_type_clicked()
        self.slotComboBox()


    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        self.baseObjData = []
        self.end = 0
        self.obj.Label = str(self.ui.LineEdit_Name.text()).replace(' ','')
        Tools3D.setOrderToObj(self.obj, self.ui)
        objName = str(self.ui.LineEdit_Name.text().replace(' ',''))
        self.obj.IFrom = int(self.ui.lineEdit_start_i.text())
        self.obj.ITo = int(self.ui.lineEdit_end_i.text())
        param = FreeCAD.ActiveDocument.getObject("Param")
        i_start = self.obj.IFrom
        i_end = self.obj.ITo
        self.obj.Attribute = self.ui.ComboBox_Shadow_Attribute.currentText()
        # 暂时这样处理测试整个结构 参数处理处理后此处要重新处理
        objsList = []
        doc = FreeCAD.ActiveDocument
        # 正投影体

        if self.ui.comboBox_type.currentIndex() == 0:
            self.baseObjData.append(str(self.ui.lineEdit_Conformal_Ptn1X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Conformal_Ptn1Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Conformal_Ptn1Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Conformal_Ptn2X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Conformal_Ptn2Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Conformal_Ptn2Z.text()).replace(" ", ""))

            for i in range(i_start, i_end + 1):
                ptn1X = str(self.ui.lineEdit_Conformal_Ptn1X.text())
                ptn1Y = str(self.ui.lineEdit_Conformal_Ptn1Y.text())
                ptn1Z = str(self.ui.lineEdit_Conformal_Ptn1Z.text())
                ptn2X = str(self.ui.lineEdit_Conformal_Ptn2X.text())
                ptn2Y = str(self.ui.lineEdit_Conformal_Ptn2Y.text())
                ptn2Z = str(self.ui.lineEdit_Conformal_Ptn2Z.text())
                try:
                    if self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                        temp_shape = ArrayInstance.drawComformal(getTheValue(self, ptn1X, i),
                                                                 getTheValue(self, ptn1Y, i),
                                                                 getTheValue(self, ptn1Z, i),
                                                                 getTheValue(self, ptn2X, i),
                                                                 getTheValue(self, ptn2Y, i),
                                                                 getTheValue(self, ptn2Z, i))
                        objsList.append(temp_shape)
                    elif self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                        temp_shape = ArrayInstance.drawComformal(getTheValue(self, ptn1X, i),
                                                                 getOtherValue(self, ptn1Y, i),
                                                                 getTheValue(self, ptn1Z, i),
                                                                 getTheValue(self, ptn2X, i),
                                                                 getOtherValue(self, ptn2Y, i),
                                                                 getTheValue(self, ptn2Z, i))
                        objsList.append(temp_shape)
                    else:
                        temp_shape = ArrayInstance.drawComformal(getTheValue(self, ptn1X, i),
                                                                 getTheValue(self, ptn1Y, i),
                                                                 getOtherValue(self, ptn1Z, i),
                                                                 getTheValue(self, ptn2X, i),
                                                                 getTheValue(self, ptn2Y, i),
                                                                 getOtherValue(self, ptn2Z, i))
                        objsList.append(temp_shape)
                except:
                    self.end = 1
                    Tools3D.sayz("参数读取错误")


        # 环形体
        elif self.ui.comboBox_type.currentIndex() == 1:
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn1X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn1Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn1Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn2X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn2Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn2Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_RadInner.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_RadOuter.text()).replace(" ", ""))

            for i in range(i_start, i_end + 1):
                ptn1X = str(self.ui.lineEdit_Annular_Ptn1X.text())
                ptn1Y = str(self.ui.lineEdit_Annular_Ptn1Y.text())
                ptn1Z = str(self.ui.lineEdit_Annular_Ptn1Z.text())
                ptn2X = str(self.ui.lineEdit_Annular_Ptn2X.text())
                ptn2Y = str(self.ui.lineEdit_Annular_Ptn2Y.text())
                ptn2Z = str(self.ui.lineEdit_Annular_Ptn2Z.text())
                radI = str(self.ui.lineEdit_Annular_RadInner.text())
                radO = str(self.ui.lineEdit_Annular_RadOuter.text())
                try:
                    if self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                        temp_shape = ArrayInstance.drawAnnular(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)
                    elif self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                        temp_shape = ArrayInstance.drawAnnular(getTheValue(self, ptn1X, i),
                                                               getOtherValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getOtherValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)
                    else:
                        temp_shape = ArrayInstance.drawAnnular(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getOtherValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getOtherValue(self, ptn2Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)

                except:
                    self.end = 1
                    Tools3D.sayz("参数读取错误")

        #圆柱体
        elif self.ui.comboBox_type.currentIndex() == 2:
            self.baseObjData.append(str(self.ui.lineEdit_Cylinder_Ptn1X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cylinder_Ptn1Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cylinder_Ptn1Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cylinder_Ptn2X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cylinder_Ptn2Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cylinder_Ptn2Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cylinder_Rad.text()).replace(" ", ""))

            for i in range(i_start, i_end + 1):
                ptn1X = str(self.ui.lineEdit_Cylinder_Ptn1X.text())
                ptn1Y = str(self.ui.lineEdit_Cylinder_Ptn1Y.text())
                ptn1Z = str(self.ui.lineEdit_Cylinder_Ptn1Z.text())
                ptn2X = str(self.ui.lineEdit_Cylinder_Ptn2X.text())
                ptn2Y = str(self.ui.lineEdit_Cylinder_Ptn2Y.text())
                ptn2Z = str(self.ui.lineEdit_Cylinder_Ptn2Z.text())
                rad = str(self.ui.lineEdit_Cylinder_Rad.text())
                try:
                    if self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                        temp_shape = ArrayInstance.drawCylinder(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, rad, i),
                                                               )
                        objsList.append(temp_shape)
                    elif self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                        temp_shape = ArrayInstance.drawCylinder(getTheValue(self, ptn1X, i),
                                                               getOtherValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getOtherValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, rad, i),
                                                               )
                        objsList.append(temp_shape)
                    else:
                        temp_shape = ArrayInstance.drawCylinder(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getOtherValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getOtherValue(self, ptn2Z, i),
                                                               getTheValue(self, rad, i),
                                                               )
                        objsList.append(temp_shape)

                except:
                    self.end = 1
                    Tools3D.sayz("参数读取错误")


        #圆台体
        elif self.ui.comboBox_type.currentIndex() == 3:
            self.baseObjData.append(str(self.ui.lineEdit_Cone_Ptn1X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cone_Ptn1Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cone_Ptn1Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cone_Ptn2X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cone_Ptn2Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cone_Ptn2Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cone_RadBott.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Cone_RadUp.text()).replace(" ", ""))

            for i in range(i_start, i_end + 1):
                ptn1X = str(self.ui.lineEdit_Cone_Ptn1X.text())
                ptn1Y = str(self.ui.lineEdit_Cone_Ptn1Y.text())
                ptn1Z = str(self.ui.lineEdit_Cone_Ptn1Z.text())
                ptn2X = str(self.ui.lineEdit_Cone_Ptn2X.text())
                ptn2Y = str(self.ui.lineEdit_Cone_Ptn2Y.text())
                ptn2Z = str(self.ui.lineEdit_Cone_Ptn2Z.text())
                radI = str(self.ui.lineEdit_Cone_RadBott.text())
                radO = str(self.ui.lineEdit_Cone_RadUp.text())
                try:
                    if self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                        temp_shape = ArrayInstance.drawSpecialCone(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)
                    elif self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                        temp_shape = ArrayInstance.drawSpecialCone(getTheValue(self, ptn1X, i),
                                                               getOtherValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getOtherValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)
                    else:
                        temp_shape = ArrayInstance.drawSpecialCone(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getOtherValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getOtherValue(self, ptn2Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)

                except:
                    self.end = 1
                    Tools3D.sayz("参数读取错误")


        elif self.ui.comboBox_type.currentIndex() == 4:
            self.baseObjData.append(str(self.ui.lineEdit_Spherical_Ptn1X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Spherical_Ptn1Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Spherical_Ptn1Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Spherical_Radius_3.text()).replace(" ", ""))

            for i in range(i_start, i_end + 1):
                ptn1X = str(self.ui.lineEdit_Spherical_Ptn1X.text())
                ptn1Y = str(self.ui.lineEdit_Spherical_Ptn1Y.text())
                ptn1Z = str(self.ui.lineEdit_Spherical_Ptn1Z.text())
                ptnR = str(self.ui.lineEdit_Spherical_Radius_3.text())
                try:
                    if self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                        temp_shape = ArrayInstance.drawSpherical(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptnR, i))
                        objsList.append(temp_shape)
                    elif self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                        temp_shape = ArrayInstance.drawSpherical(getTheValue(self, ptn1X, i),
                                                                 getOtherValue(self, ptn1Y, i),
                                                                 getTheValue(self, ptn1Z, i),
                                                                 getTheValue(self, ptnR, i))
                        objsList.append(temp_shape)
                    else:
                        temp_shape = ArrayInstance.drawSpherical(getTheValue(self, ptn1X, i),
                                                                 getTheValue(self, ptn1Y, i),
                                                                 getOtherValue(self, ptn1Z, i),
                                                                 getTheValue(self, ptnR, i))
                        objsList.append(temp_shape)

                except:
                    self.end = 1
                    Tools3D.sayz("参数读取错误")

        elif self.ui.comboBox_type.currentIndex() == 5:
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn1X_2.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn1Y_2.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn1Z_2.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn2X_2.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn2Y_2.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn2Z_2.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn3X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn3Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn3Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn4X.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn4Y.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_Ptn4Z.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_RadInner1.text()).replace(" ", ""))
            self.baseObjData.append(str(self.ui.lineEdit_Annular_RadOuter1.text()).replace(" ", ""))

            for i in range(i_start, i_end + 1):
                ptn1X = str(self.ui.lineEdit_Annular_Ptn1X_2.text())
                ptn1Y = str(self.ui.lineEdit_Annular_Ptn1Y_2.text())
                ptn1Z = str(self.ui.lineEdit_Annular_Ptn1Z_2.text())
                ptn2X = str(self.ui.lineEdit_Annular_Ptn2X_2.text())
                ptn2Y = str(self.ui.lineEdit_Annular_Ptn2Y_2.text())
                ptn2Z = str(self.ui.lineEdit_Annular_Ptn2Z_2.text())
                ptn3X = str(self.ui.lineEdit_Annular_Ptn3X.text())
                ptn3Y = str(self.ui.lineEdit_Annular_Ptn3Y.text())
                ptn3Z = str(self.ui.lineEdit_Annular_Ptn3Z.text())
                ptn4X = str(self.ui.lineEdit_Annular_Ptn4X.text())
                ptn4Y = str(self.ui.lineEdit_Annular_Ptn4Y.text())
                ptn4Z = str(self.ui.lineEdit_Annular_Ptn4Z.text())
                radI = str(self.ui.lineEdit_Annular_RadInner1.text())
                radO = str(self.ui.lineEdit_Annular_RadOuter1.text())
                try:
                    if self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                        temp_shape = ArrayInstance.drawAnnularSection(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, ptn3X, i),
                                                               getTheValue(self, ptn3Y, i),
                                                               getTheValue(self, ptn3Z, i),
                                                               getTheValue(self, ptn4X, i),
                                                               getTheValue(self, ptn4Y, i),
                                                               getTheValue(self, ptn4Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)
                    elif self.currentCoordinate == FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                        temp_shape = ArrayInstance.drawAnnularSection(getTheValue(self, ptn1X, i),
                                                               getOtherValue(self, ptn1Y, i),
                                                               getTheValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getOtherValue(self, ptn2Y, i),
                                                               getTheValue(self, ptn2Z, i),
                                                               getTheValue(self, ptn3X, i),
                                                               getOtherValue(self, ptn3Y, i),
                                                               getTheValue(self, ptn3Z, i),
                                                               getTheValue(self, ptn4X, i),
                                                               getOtherValue(self, ptn4Y, i),
                                                               getTheValue(self, ptn4Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)
                    else:
                        temp_shape = ArrayInstance.drawAnnularSection(getTheValue(self, ptn1X, i),
                                                               getTheValue(self, ptn1Y, i),
                                                               getOtherValue(self, ptn1Z, i),
                                                               getTheValue(self, ptn2X, i),
                                                               getTheValue(self, ptn2Y, i),
                                                               getOtherValue(self, ptn2Z, i),
                                                                      getTheValue(self, ptn3X, i),
                                                                      getTheValue(self, ptn3Y, i),
                                                                      getOtherValue(self, ptn3Z, i),
                                                                      getTheValue(self, ptn4X, i),
                                                                      getTheValue(self, ptn4Y, i),
                                                                      getOtherValue(self, ptn4Z, i),
                                                               getTheValue(self, radI, i),
                                                               getTheValue(self, radO, i),
                                                               )
                        objsList.append(temp_shape)

                except:
                    self.end = 1
                    Tools3D.sayz("参数读取错误")

        if len(objsList) != 0:
            self.obj.BaseObjType = self.baseObjType
            self.obj.BaseObjData = self.baseObjData
            objs = objsList
            theFirstShape = None
            otherShapes = []
            if len(objsList) <= 0:
                self.obj.Shape = None
            elif len(objsList) == 1:
                self.obj.Shape = objs[0]
            else:
                theFirstShape = objs[0]
                otherShapes = objs[1:]
                self.obj.Shape = theFirstShape.multiFuse(otherShapes)
        self.obj.MarkX = self.ui.lineEdit_UniformX.text()
        self.obj.MarkY = self.ui.lineEdit_UniformY.text()
        self.obj.MarkZ = self.ui.lineEdit_UniformZ.text()
        self.obj.isMarkX = self.ui.checkBox_UniformX.isChecked()
        self.obj.isMarkY = self.ui.checkBox_UniformY.isChecked()
        self.obj.isMarkZ = self.ui.checkBox_UniformZ.isChecked()
        self.obj.recompute()

    def slotComboBox(self):
        # 正投影体
        if self.ui.comboBox_type.currentIndex() == 0:
            dataList = self.obj.BaseObjData
            self.ui.lineEdit_Conformal_Ptn1X.setText(dataList[0])
            self.ui.lineEdit_Conformal_Ptn1Y.setText(dataList[1])
            self.ui.lineEdit_Conformal_Ptn1Z.setText(dataList[2])
            self.ui.lineEdit_Conformal_Ptn2X.setText(dataList[3])
            self.ui.lineEdit_Conformal_Ptn2Y.setText(dataList[4])
            self.ui.lineEdit_Conformal_Ptn2Z.setText(dataList[5])
        elif self.ui.comboBox_type.currentIndex() == 1:
            dataList = self.obj.BaseObjData
            self.ui.lineEdit_Annular_Ptn1X.setText(dataList[0])
            self.ui.lineEdit_Annular_Ptn1Y.setText(dataList[1])
            self.ui.lineEdit_Annular_Ptn1Z.setText(dataList[2])
            self.ui.lineEdit_Annular_Ptn2X.setText(dataList[3])
            self.ui.lineEdit_Annular_Ptn2Y.setText(dataList[4])
            self.ui.lineEdit_Annular_Ptn2Z.setText(dataList[5])
            self.ui.lineEdit_Annular_RadInner.setText(dataList[6])
            self.ui.lineEdit_Annular_RadOuter.setText(dataList[7])
        #     圆柱体
        elif self.ui.comboBox_type.currentIndex() == 2:
            dataList = self.obj.BaseObjData
            self.ui.lineEdit_Cylinder_Ptn1X.setText(dataList[0])
            self.ui.lineEdit_Cylinder_Ptn1Y.setText(dataList[1])
            self.ui.lineEdit_Cylinder_Ptn1Z.setText(dataList[2])
            self.ui.lineEdit_Cylinder_Ptn2X.setText(dataList[3])
            self.ui.lineEdit_Cylinder_Ptn2Y.setText(dataList[4])
            self.ui.lineEdit_Cylinder_Ptn2Z.setText(dataList[5])
            self.ui.lineEdit_Cylinder_Rad.setText(dataList[6])
        # 圆台
        elif self.ui.comboBox_type.currentIndex() == 3:
            dataList = self.obj.BaseObjData
            self.ui.lineEdit_Cone_Ptn1X.setText(dataList[0])
            self.ui.lineEdit_Cone_Ptn1Y.setText(dataList[1])
            self.ui.lineEdit_Cone_Ptn1Z.setText(dataList[2])
            self.ui.lineEdit_Cone_Ptn2X.setText(dataList[3])
            self.ui.lineEdit_Cone_Ptn2Y.setText(dataList[4])
            self.ui.lineEdit_Cone_Ptn2Z.setText(dataList[5])
            self.ui.lineEdit_Cone_RadBott.setText(dataList[6])
            self.ui.lineEdit_Cone_RadUp.setText(dataList[7])
        # 球体
        elif self.ui.comboBox_type.currentIndex() == 4:
            dataList = self.obj.BaseObjData
            self.ui.lineEdit_Spherical_Ptn1X.setText(dataList[0])
            self.ui.lineEdit_Spherical_Ptn1Y.setText(dataList[1])
            self.ui.lineEdit_Spherical_Ptn1Z.setText(dataList[2])
            self.ui.lineEdit_Spherical_Radius_3.setText(dataList[3])
        #  圆环区域体
        elif self.ui.comboBox_type.currentIndex() == 5:
            dataList = self.obj.BaseObjData
            self.ui.lineEdit_Annular_Ptn1X_2.setText(dataList[0])
            self.ui.lineEdit_Annular_Ptn1Y_2.setText(dataList[1])
            self.ui.lineEdit_Annular_Ptn1Z_2.setText(dataList[2])
            self.ui.lineEdit_Annular_Ptn2X_2.setText(dataList[3])
            self.ui.lineEdit_Annular_Ptn2Y_2.setText(dataList[4])
            self.ui.lineEdit_Annular_Ptn2Z_2.setText(dataList[5])
            self.ui.lineEdit_Annular_Ptn3X.setText(dataList[6])
            self.ui.lineEdit_Annular_Ptn3Y.setText(dataList[7])
            self.ui.lineEdit_Annular_Ptn3Z.setText(dataList[8])
            self.ui.lineEdit_Annular_Ptn4X.setText(dataList[9])
            self.ui.lineEdit_Annular_Ptn4Y.setText(dataList[10])
            self.ui.lineEdit_Annular_Ptn4Z.setText(dataList[11])
            self.ui.lineEdit_Annular_RadInner1.setText(dataList[12])
            self.ui.lineEdit_Annular_RadOuter1.setText(dataList[13])
        # 其余体后续补充


    def setFirst(self):
        self.iStart = ""
        self.iEnd = ""
        self.baseObjType = ""
        self.baseObjData = []
        # self.baseObjData = self.obj.BaseObjData
        self.ComboBox_type_clicked()
        self.ui.tabWidget.tabBar().hide()

    def ComboBox_type_clicked(self):
        currentIndex=self.ui.comboBox_type.currentIndex()
        self.baseObjType=self.ui.comboBox_type.currentText()
        self.setTabEnable(currentIndex)
        # if currentIndex<=4:
        #     self.ui.ComboBox_Shadow_Attribute.setEditable(False)

    def dafultsetting(self):
        if self.ui.comboBox_type.currentIndex() == 0:
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                self.ui.lineEdit_Conformal_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Conformal_Ptn2X.setText('xlf\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Y.setText('ylf\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Z.setText('zlf\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                self.ui.lineEdit_Conformal_Ptn1X.setText('rli\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Y.setText('theta_i\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Conformal_Ptn2X.setText('rlf\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Y.setText('theta_f\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Z.setText('zlf\'i\'')
            else:
                self.ui.lineEdit_Conformal_Ptn1X.setText('zli\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Y.setText('rli\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Z.setText('theta_i\'i\'')

                self.ui.lineEdit_Conformal_Ptn2X.setText('zlf\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Y.setText('rlf\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Z.setText('theta_f\'i\'')
        #         环形体
        elif self.ui.comboBox_type.currentIndex() == 1:
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                self.ui.lineEdit_Annular_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Annular_Ptn2X.setText('xlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y.setText('ylf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z.setText('zlf\'i\'')
                self.ui.lineEdit_Annular_RadInner.setText('radius_inner\'i\'')
                self.ui.lineEdit_Annular_RadOuter.setText('radius_outer\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                self.ui.lineEdit_Annular_Ptn1X.setText('rli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y.setText('theta_i\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Annular_Ptn2X.setText('rlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y.setText('theta_f\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z.setText('zlf\'i\'')
                self.ui.lineEdit_Annular_RadInner.setText('radius_inner\'i\'')
                self.ui.lineEdit_Annular_RadOuter.setText('radius_outer\'i\'')
            else:
                self.ui.lineEdit_Annular_Ptn1X.setText('zli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y.setText('rli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z.setText('theta_i\'i\'')

                self.ui.lineEdit_Annular_Ptn2X.setText('zlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y.setText('rlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z.setText('theta_f\'i\'')
                self.ui.lineEdit_Annular_RadInner.setText('radius_inner\'i\'')
                self.ui.lineEdit_Annular_RadOuter.setText('radius_outer\'i\'')
        #     圆柱体
        elif self.ui.comboBox_type.currentIndex() == 2:
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                self.ui.lineEdit_Cylinder_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Cylinder_Ptn2X.setText('xlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Y.setText('ylf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Z.setText('zlf\'i\'')
                self.ui.lineEdit_Cylinder_Rad.setText('radius\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                self.ui.lineEdit_Cylinder_Ptn1X.setText('rli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Y.setText('theta_i\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Cylinder_Ptn2X.setText('rlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Y.setText('theta_f\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Z.setText('zlf\'i\'')
                self.ui.lineEdit_Cylinder_Rad.setText('radius\'i\'')
            else:
                self.ui.lineEdit_Cylinder_Ptn1X.setText('zli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Y.setText('rli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Z.setText('theta_i\'i\'')

                self.ui.lineEdit_Cylinder_Ptn2X.setText('zlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Y.setText('rlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Z.setText('theta_f\'i\'')
                self.ui.lineEdit_Cylinder_Rad.setText('radius\'i\'')
        elif self.ui.comboBox_type.currentIndex() == 3:
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                self.ui.lineEdit_Cone_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Cone_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Cone_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Cone_Ptn2X.setText('xlf\'i\'')
                self.ui.lineEdit_Cone_Ptn2Y.setText('ylf\'i\'')
                self.ui.lineEdit_Cone_Ptn2Z.setText('zlf\'i\'')
                self.ui.lineEdit_Cone_RadBott.setText('radius_inner\'i\'')
                self.ui.lineEdit_Cone_RadUp.setText('radius_outer\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                self.ui.lineEdit_Cone_Ptn1X.setText('rli\'i\'')
                self.ui.lineEdit_Cone_Ptn1Y.setText('theta_i\'i\'')
                self.ui.lineEdit_Cone_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Cone_Ptn2X.setText('rlf\'i\'')
                self.ui.lineEdit_Cone_Ptn2Y.setText('theta_f\'i\'')
                self.ui.lineEdit_Cone_Ptn2Z.setText('zlf\'i\'')
                self.ui.lineEdit_Cone_RadBott.setText('radius_inner\'i\'')
                self.ui.lineEdit_Cone_RadUp.setText('radius_outer\'i\'')
            else:
                self.ui.lineEdit_Cone_Ptn1X.setText('zli\'i\'')
                self.ui.lineEdit_Cone_Ptn1Y.setText('rli\'i\'')
                self.ui.lineEdit_Cone_Ptn1Z.setText('theta_i\'i\'')
                self.ui.lineEdit_Cone_Ptn2X.setText('zlf\'i\'')
                self.ui.lineEdit_Cone_Ptn2Y.setText('rlf\'i\'')
                self.ui.lineEdit_Cone_Ptn2Z.setText('theta_f\'i\'')
                self.ui.lineEdit_Cone_RadBott.setText('radius_inner\'i\'')
                self.ui.lineEdit_Cone_RadUp.setText('radius_outer\'i\'')
        elif self.ui.comboBox_type.currentIndex() == 4:
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                self.ui.lineEdit_Spherical_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Spherical_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Spherical_Ptn1Z.setText('zli\'i\'')
                self.ui.lineEdit_Spherical_Radius_3.setText('radius\'i\'')

            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                self.ui.lineEdit_Spherical_Ptn1X.setText('rli\'i\'')
                self.ui.lineEdit_Spherical_Ptn1Y.setText('theta_i\'i\'')
                self.ui.lineEdit_Spherical_Ptn1Z.setText('zli\'i\'')
                self.ui.lineEdit_Spherical_Radius_3.setText('radius\'i\'')

            else:
                self.ui.lineEdit_Spherical_Ptn1X.setText('zli\'i\'')
                self.ui.lineEdit_Spherical_Ptn1Y.setText('rli\'i\'')
                self.ui.lineEdit_Spherical_Ptn1Z.setText('theta_i\'i\'')
                self.ui.lineEdit_Spherical_Radius_3.setText('radius\'i\'')
        elif self.ui.comboBox_type.currentIndex() == 5:
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                self.ui.lineEdit_Annular_Ptn1X_2.setText('xli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y_2.setText('yli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z_2.setText('zli\'i\'')

                self.ui.lineEdit_Annular_Ptn2X_2.setText('xlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y_2.setText('ylf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z_2.setText('zlf\'i\'')
                self.ui.lineEdit_Annular_Ptn3X.setText('xlt\'i\'')
                self.ui.lineEdit_Annular_Ptn3Y.setText('ylt\'i\'')
                self.ui.lineEdit_Annular_Ptn3Z.setText('zlt\'i\'')
                self.ui.lineEdit_Annular_Ptn4X.setText('xle\'i\'')
                self.ui.lineEdit_Annular_Ptn4Y.setText('yle\'i\'')
                self.ui.lineEdit_Annular_Ptn4Z.setText('zle\'i\'')

                self.ui.lineEdit_Annular_RadInner1.setText('radius_inner\'i\'')
                self.ui.lineEdit_Annular_RadOuter1.setText('radius_outer\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                self.ui.lineEdit_Annular_Ptn1X_2.setText('rli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y_2.setText('theta_i\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z_2.setText('zli\'i\'')

                self.ui.lineEdit_Annular_Ptn2X_2.setText('rlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y_2.setText('theta_f\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z_2.setText('zlf\'i\'')

                self.ui.lineEdit_Annular_Ptn3X.setText('rlt\'i\'')
                self.ui.lineEdit_Annular_Ptn3Y.setText('theta_t\'i\'')
                self.ui.lineEdit_Annular_Ptn3Z.setText('zlt\'i\'')
                self.ui.lineEdit_Annular_Ptn4X.setText('rle\'i\'')
                self.ui.lineEdit_Annular_Ptn4Y.setText('theta_e\'i\'')
                self.ui.lineEdit_Annular_Ptn4Z.setText('zle\'i\'')

                self.ui.lineEdit_Annular_RadInner1.setText('radius_inner\'i\'')
                self.ui.lineEdit_Annular_RadOuter1.setText('radius_outer\'i\'')
            else:
                self.ui.lineEdit_Annular_Ptn1X_2.setText('zli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y_2.setText('rli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z_2.setText('theta_i\'i\'')

                self.ui.lineEdit_Annular_Ptn2X_2.setText('zlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y_2.setText('rlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z_2.setText('theta_f\'i\'')

                self.ui.lineEdit_Annular_Ptn3X.setText('zlt\'i\'')
                self.ui.lineEdit_Annular_Ptn3Y.setText('rlt\'i\'')
                self.ui.lineEdit_Annular_Ptn3Z.setText('theta_t\'i\'')
                self.ui.lineEdit_Annular_Ptn4X.setText('zle\'i\'')
                self.ui.lineEdit_Annular_Ptn4Y.setText('rle\'i\'')
                self.ui.lineEdit_Annular_Ptn4Z.setText('theta_e\'i\'')
                self.ui.lineEdit_Annular_RadInner1.setText('radius_inner\'i\'')
                self.ui.lineEdit_Annular_RadOuter1.setText('radius_outer\'i\'')
        else:
            pass

    def setTabEnable(self, index):
        for i in range(0, int(self.ui.tabWidget.count())):
            if i==index:
                self.ui.tabWidget.setTabEnabled(index, True)
                self.ui.tabWidget.setCurrentIndex(index)
            else:
                self.ui.tabWidget.setTabEnabled(i, False)

    def slotOK(self):
        # self.keepData()
        self.setInfoToObj()
        if self.end==0:
            self.isKeepData = True
            self.close()
        else:
            QtGui.QMessageBox.information(None, "", "参数设置错误,无法绘制模型，请检查参数正确性。")

    def slotCancel(self):
        self.isKeepData = False
        self.close()


    def closeEvent(self, event):
        if self.isKeepData:
            try:
                # self.setInfoToObj()
                FreeCADGui.runCommand("CreateM3D_new")
                FreeCADGui.runCommand("UpdateBooleanCommand_3D")
            except AttributeError:
                Tools3D.sayz("--异常--在读取Object属性时出现异常")
                Tools3D.sayz(traceback.format_exc())
            except Exception as e:
                Tools3D.sayz("--" + str(e))
            else:
                FreeCAD.Console.PrintMessage("设置Object信息\n")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)


def getPropertyValue(name):
    try:
        param = FreeCAD.ActiveDocument.getObject("Param")
        t = param.getTypeIdOfProperty(name)
        if t == "App::PropertyFloat":
            return getattr(param, name)
        elif t == "App::PropertyDistance":
            return getattr(getattr(param, name), "Value")
        elif t == "App::PropertyAngle":
            return getattr(getattr(param, name), "Value")
        else:
            raise Exception("error with param type")
    except:
        Tools3D.sayz("value获取错误")


def getTheValue(self, name, i):
    if "'i'" in name:
        a=name.replace("\'i\'", str(i)).replace(" ", "")
        FreeCAD.Console.PrintMessage("Change property: " + str(a) + "\n")
        return getPropertyValue(a)
    else:
        Tools3D.setPlaceToObj(self.obj, "Helper1", name)
        FreeCAD.Console.PrintMessage("Change property: " + str(self.obj.Helper1.Value) + "\n")
        return self.obj.Helper1.Value


def getOtherValue(self, name, i):
    if "'i'" in name:
        a=name.replace("\'i\'", str(i)).replace(" ", "")
        FreeCAD.Console.PrintMessage("Change property: " + str(a) + "\n")
        return getPropertyValue(a)
    else:
        Tools3D.setPlaceToObj(self.obj, "Helper2", name)
        FreeCAD.Console.PrintMessage("Change property: " + str(self.obj.Helper2) + "\n")
        return self.obj.Helper2.Value