# -*- coding: UTF-8 -*-
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import FreeCAD,FreeCADGui
from Modeling3DCommand.Vol_Array.UI import Vol_Array_Dlg
from Modeling.Common.Tools import UnitTools,ObjectsTools,CoordinateSystemTools,DocumentTools
import Modeling3DCommand as Model
import ArrayInstance as Instance
import time
import re
from Modeling3D.Tools import  RebuildForUITools,ModelingByUITools

import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate
# from Modeling.Common.CommonCommand.NewDocument import ObjectDict,NewDocument
class VolArray(QtGui.QDialog):
    def __init__(self, obj=None):
        QtGui.QDialog.__init__(self)
        self.ui = Vol_Array_Dlg.Ui_Dialog_Vol_Array()
        self.ui.setupUi(self)
        # 连接信号与槽 @lizhenguang
        self.ui.comboBox_type.currentIndexChanged.connect(self.dafultsetting)
        self.ui.comboBox_type.currentIndexChanged.connect(self.ComboBox_type_clicked)
        # 连接信号与槽 @lizhenguang
        self.dafultsetting()
        self.ui.comboBox_type.currentIndexChanged.connect(self.dafultsetting)
        self.ui.ComboBox_Shadow_Attribute.currentIndexChanged.connect(self.ComboBox_Attribute_clicked)
        self.ui.pushButton_ok.clicked.connect(self.pushBtnOk)
        self.ui.pushButton_cancel.clicked.connect(self.cancelBtnClick)

        self.currentCoordinate=FreeCAD.ActiveDocument.CoordinateSystem
        self.initFialog()
                # 类型
        self.beforeType=-1
        self.obj=obj
        self.attribute=ObjectsTools.Attribute.NotDefine

        # 设置一下相关坐标
        Coordi_Name = RebuildForUITools.getCoordinateName(self.currentCoordinate)
        self.ui.label_X3.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[0], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Y3.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[1], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Z3.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[2], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_X2.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[0], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Y2.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[1], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Z2.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[2], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_X1.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[0], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Y1.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[1], None, QtGui.QApplication.UnicodeUTF8))
        self.ui.label_Z1.setText(QtGui.QApplication.translate("Dialog_Vol_Array", Coordi_Name[2], None, QtGui.QApplication.UnicodeUTF8))

        if obj:
            #名称：
            self.ui.LineEdit_Name.setText(ObjectsTools.getLabelWithoutOrder(obj))
            # self.beforeType=obj.BaseObjType
            self.ui.comboBox_type.setCurrentIndex(self.ui.comboBox_type.findText(obj.BaseObjType))
            attributeText=""
            if obj.Attribute==ObjectsTools.Attribute.NotDefine:
                attributeText=u"未定义"
            elif obj.Attribute==ObjectsTools.Attribute.Conductor:
                attributeText=u"理想导体"
            elif obj.Attribute==ObjectsTools.Attribute.Custom:
                attributeText=u"自定义"
            elif obj.Attribute==ObjectsTools.Attribute.Vacuo:
                attributeText=u"真空"
            self.ui.ComboBox_Shadow_Attribute.setCurrentIndex(self.ui.ComboBox_Shadow_Attribute.findText(attributeText))
            # 设置起始
            self.ui.lineEdit_start_i.setText(ObjectsTools.turnPropertyToExpression(obj,"IFrom"))
            self.ui.lineEdit_end_i.setText(ObjectsTools.turnPropertyToExpression(obj,"ITo"))
            # 填入体数据
            # 正投影体
            if self.ui.comboBox_type.currentIndex()==0:
                dataList=obj.BaseObjData.split(" ")
                if len(dataList)==2:
                    #Point_1
                    point=dataList[0].split(",")
                    if len(point)==3:
                        self.ui.lineEdit_Conformal_Ptn1X.setText(point[0])
                        self.ui.lineEdit_Conformal_Ptn1Y.setText(point[1])
                        self.ui.lineEdit_Conformal_Ptn1Z.setText(point[2])
                    point=dataList[1].split(",")
                    if len(point)==3:
                        self.ui.lineEdit_Conformal_Ptn2X.setText(point[0])
                        self.ui.lineEdit_Conformal_Ptn2Y.setText(point[1])
                        self.ui.lineEdit_Conformal_Ptn2Z.setText(point[2])
            #环形体
            elif self.ui.comboBox_type.currentIndex()==1:
                dataList=obj.BaseObjData.split(" ")
                if len(dataList)==4:
                    #Point_1
                    point=dataList[0].split(",")
                    if len(point)==3:
                        self.ui.lineEdit_Annular_Ptn1X.setText(point[0])
                        self.ui.lineEdit_Annular_Ptn1Y.setText(point[1])
                        self.ui.lineEdit_Annular_Ptn1Z.setText(point[2])
                    point=dataList[1].split(",")
                    if len(point)==3:
                        self.ui.lineEdit_Annular_Ptn2X.setText(point[0])
                        self.ui.lineEdit_Annular_Ptn2Y.setText(point[1])
                        self.ui.lineEdit_Annular_Ptn2Z.setText(point[2])
                    
                    self.ui.lineEdit_Annular_RadInner.setText(dataList[2])
                    self.ui.lineEdit_Annular_RadOuter.setText(dataList[3])
            #圆柱体
            elif self.ui.comboBox_type.currentIndex()==2:
                dataList=obj.BaseObjData.split(" ")
                if len(dataList)==3:
                    point=dataList[0].split(",")
                    if len(point)==3:
                        # FreeCAD.Console.PrintMessage("\n将点依次输出: "+point[0]+" "+point)
                        self.ui.lineEdit_Cylinder_Ptn1X.setText(point[0])
                        self.ui.lineEdit_Cylinder_Ptn1Y.setText(point[1])
                        self.ui.lineEdit_Cylinder_Ptn1Z.setText(point[2])
                    point=dataList[1].split(",")
                    if len(point)==3:
                        self.ui.lineEdit_Cylinder_Ptn2X.setText(point[0])
                        self.ui.lineEdit_Cylinder_Ptn2Y.setText(point[1])
                        self.ui.lineEdit_Cylinder_Ptn2Z.setText(point[2])
                    
                    self.ui.lineEdit_Cylinder_Rad.setText(dataList[2])
            #圆台体
            elif self.ui.comboBox_type.currentIndex()==3:

                dataList=obj.BaseObjData.split(" ")
                if len(dataList)==4:
                    #Point_1
                    point=dataList[0].split(",")
                    if len(point)==3:
                        self.ui.lineEdit_Cone_Ptn1X.setText(point[0])
                        self.ui.lineEdit_Cone_Ptn1Y.setText(point[1])
                        self.ui.lineEdit_Cone_Ptn1Z.setText(point[2])
                    point=dataList[1].split(",")
                    if len(point)==3:
                        self.ui.lineEdit_Cone_Ptn2X.setText(point[0])
                        self.ui.lineEdit_Cone_Ptn2Y.setText(point[1])
                        self.ui.lineEdit_Cone_Ptn2Z.setText(point[2])
                    
                    self.ui.lineEdit_Cone_RadBott.setText(dataList[2])
                    self.ui.lineEdit_Cone_RadUp.setText(dataList[3])
                pass
            else:
                pass
            
            if self.currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular:
                #填入非均匀网格属性
                self.ui.checkBox_UniformX.setChecked(obj.X)
                self.ui.checkBox_UniformY.setChecked(obj.Y)
                self.ui.checkBox_UniformZ.setChecked(obj.Z)

                self.ui.lineEdit_UniformX.setText(ObjectsTools.turnPropertyToExpression(obj,"X_Value"))
                self.ui.lineEdit_UniformY.setText(ObjectsTools.turnPropertyToExpression(obj,"Y_Value"))
                self.ui.lineEdit_UniformZ.setText(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))
            elif self.currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:
                #填入非均匀网格属性
                self.ui.checkBox_UniformX.setChecked(obj.R)
                self.ui.checkBox_UniformY.setChecked(obj.Theta)
                self.ui.checkBox_UniformZ.setChecked(obj.Z)

                self.ui.lineEdit_UniformX.setText(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))
                self.ui.lineEdit_UniformY.setText(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))
                self.ui.lineEdit_UniformZ.setText(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))                
            elif self.currentCoordinate==CoordinateSystemTools.CoordinateType.Cylindrical:
                #填入非均匀网格属性
                self.ui.checkBox_UniformX.setChecked(obj.Z)
                self.ui.checkBox_UniformY.setChecked(obj.R)
                self.ui.checkBox_UniformZ.setChecked(obj.Theta)

                self.ui.lineEdit_UniformX.setText(ObjectsTools.turnPropertyToExpression(obj,"Z_Value"))
                self.ui.lineEdit_UniformY.setText(ObjectsTools.turnPropertyToExpression(obj,"R_Value"))
                self.ui.lineEdit_UniformZ.setText(ObjectsTools.turnPropertyToExpression(obj,"Theta_Value"))                 
            pass
        else:
            # 设置一下不同坐标系下的变量名
            self.ui.lineEdit_Cylinder_Rad.setText("radius'i'")
            if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
                self.ui.lineEdit_Conformal_Ptn1X.setText("Ptn1X'i'")
                self.ui.lineEdit_Conformal_Ptn1Y.setText("Ptn1Y'i'")
                self.ui.lineEdit_Conformal_Ptn1Z.setText("Ptn1Z'i'")
                self.ui.lineEdit_Conformal_Ptn2X.setText("Ptn2X'i'")
                self.ui.lineEdit_Conformal_Ptn2Y.setText("Ptn2Y'i'")
                self.ui.lineEdit_Conformal_Ptn2Z.setText("Ptn2Z'i'")

                self.ui.lineEdit_Annular_Ptn2Y.setText("Ptn2Y'i'")
                self.ui.lineEdit_Annular_Ptn2Z.setText("Ptn2Z'i'")

                self.ui.lineEdit_Cylinder_Ptn1X.setText("Ptn1X'i'")
                self.ui.lineEdit_Cylinder_Ptn1Y.setText("Ptn1Y'i'")
                self.ui.lineEdit_Cylinder_Ptn1Z.setText("Ptn1Z'i'")
                self.ui.lineEdit_Cylinder_Ptn2X.setText("Ptn2X'i'")
                self.ui.lineEdit_Cylinder_Ptn2Y.setText("Ptn2Y'i'")
                self.ui.lineEdit_Cylinder_Ptn2Z.setText("Ptn2Z'i'")
            elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
                self.ui.lineEdit_Conformal_Ptn1X.setText("radius1'i'")
                self.ui.lineEdit_Conformal_Ptn1Y.setText("theta1'i'")
                self.ui.lineEdit_Conformal_Ptn1Z.setText("Ptn1Z'i'")
                self.ui.lineEdit_Conformal_Ptn2X.setText("radius2'i'")
                self.ui.lineEdit_Conformal_Ptn2Y.setText("theta2'i'")
                self.ui.lineEdit_Conformal_Ptn2Z.setText("Ptn2Z'i'")

                self.ui.lineEdit_Annular_Ptn1X.setText("radius1'i'")
                self.ui.lineEdit_Annular_Ptn1Y.setText("theta1'i'")
                self.ui.lineEdit_Annular_Ptn1Z.setText("Ptn1Z'i'")
                self.ui.lineEdit_Annular_Ptn2X.setText("radius2'i'")
                self.ui.lineEdit_Annular_Ptn2Y.setText("theta2'i'")
                self.ui.lineEdit_Annular_Ptn2Z.setText("Ptn2Z'i'")

                self.ui.lineEdit_Cylinder_Ptn1X.setText("radius1'i'")
                self.ui.lineEdit_Cylinder_Ptn1Y.setText("theta1'i'")
                self.ui.lineEdit_Cylinder_Ptn1Z.setText("Ptn1Z'i'")
                self.ui.lineEdit_Cylinder_Ptn2X.setText("radius2'i'")
                self.ui.lineEdit_Cylinder_Ptn2Y.setText("theta2'i'")
                self.ui.lineEdit_Cylinder_Ptn2Z.setText("Ptn2Z'i'")
            else:
                self.ui.lineEdit_Conformal_Ptn1X.setText("Ptn1Z'i'")
                self.ui.lineEdit_Conformal_Ptn1Y.setText("radius1'i'")
                self.ui.lineEdit_Conformal_Ptn1Z.setText("theta1'i'")
                self.ui.lineEdit_Conformal_Ptn2X.setText("Ptn2Z'i'")
                self.ui.lineEdit_Conformal_Ptn2Y.setText("radius2'i'")
                self.ui.lineEdit_Conformal_Ptn2Z.setText("theta2'i'")

                self.ui.lineEdit_Annular_Ptn1X.setText("Ptn1Z'i'")
                self.ui.lineEdit_Annular_Ptn1Y.setText("radius1'i'")
                self.ui.lineEdit_Annular_Ptn1Z.setText("theta1'i'")
                self.ui.lineEdit_Annular_Ptn2X.setText("Ptn2Z'i'")
                self.ui.lineEdit_Annular_Ptn2Y.setText("radius2'i'")
                self.ui.lineEdit_Annular_Ptn2Z.setText("theta2'i'")

                self.ui.lineEdit_Cylinder_Ptn1X.setText("Ptn1Z'i'")
                self.ui.lineEdit_Cylinder_Ptn1Y.setText("radius1'i'")
                self.ui.lineEdit_Cylinder_Ptn1Z.setText("theta1'i'")
                self.ui.lineEdit_Cylinder_Ptn2X.setText("Ptn2Z'i'")
                self.ui.lineEdit_Cylinder_Ptn2Y.setText("radius2'i'")
                self.ui.lineEdit_Cylinder_Ptn2Z.setText("theta2'i'")


            self.iStart=""
            self.iEnd=""
            self.baseObjType=""
            self.baseObjData=""

        self.ComboBox_type_clicked()
        self.ui.tabWidget.tabBar().hide()
    # 设置默认值 @lizhenguang
    def dafultsetting(self):
        if self.ui.comboBox_type.currentIndex()==0:
            if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
                self.ui.lineEdit_Conformal_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Conformal_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Conformal_Ptn2X.setText('xlf\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Y.setText('ylf\'i\'')
                self.ui.lineEdit_Conformal_Ptn2Z.setText('zlf\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
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

        elif self.ui.comboBox_type.currentIndex()==1:
            if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
                self.ui.lineEdit_Annular_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Annular_Ptn2X.setText('xlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y.setText('ylf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z.setText('zlf\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
                self.ui.lineEdit_Annular_Ptn1X.setText('rli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y.setText('theta_i\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Annular_Ptn2X.setText('rlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y.setText('theta_f\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z.setText('zlf\'i\'')
            else:
                self.ui.lineEdit_Annular_Ptn1X.setText('zli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Y.setText('rli\'i\'')
                self.ui.lineEdit_Annular_Ptn1Z.setText('theta_i\'i\'')

                self.ui.lineEdit_Annular_Ptn2X.setText('zlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Y.setText('rlf\'i\'')
                self.ui.lineEdit_Annular_Ptn2Z.setText('theta_f\'i\'')
            self.ui.lineEdit_Annular_RadInner.setText('radius_i\'i\'')
            self.ui.lineEdit_Annular_RadOuter.setText('radius_o\'i\'')
        elif self.ui.comboBox_type.currentIndex()==2:
            if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
                self.ui.lineEdit_Cylinder_Ptn1X.setText('xli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Y.setText('yli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Cylinder_Ptn2X.setText('xlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Y.setText('ylf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Z.setText('zlf\'i\'')
            elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
                self.ui.lineEdit_Cylinder_Ptn1X.setText('rli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Y.setText('theta_i\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Z.setText('zli\'i\'')

                self.ui.lineEdit_Cylinder_Ptn2X.setText('rlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Y.setText('theta_f\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Z.setText('zlf\'i\'')
            else:
                self.ui.lineEdit_Cylinder_Ptn1X.setText('zli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Y.setText('rli\'i\'')
                self.ui.lineEdit_Cylinder_Ptn1Z.setText('theta_i\'i\'')

                self.ui.lineEdit_Cylinder_Ptn2X.setText('zlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Y.setText('rlf\'i\'')
                self.ui.lineEdit_Cylinder_Ptn2Z.setText('theta_f\'i\'')
            self.ui.lineEdit_Cylinder_Rad.setText('radius\'i\'')
    def setTabEnable(self,index):
        for i in range(0,int(self.ui.tabWidget.count())):
            if i==index:
                self.ui.tabWidget.setTabEnabled(index,True)
                self.ui.tabWidget.setCurrentIndex(index)
            else:
                self.ui.tabWidget.setTabEnabled(i,False)
    def ComboBox_Attribute_clicked(self):
        currentIndex=self.ui.ComboBox_Shadow_Attribute.currentIndex()
        if currentIndex==0:
            self.attribute=ObjectsTools.Attribute.NotDefine
        elif currentIndex==1:
            self.attribute=ObjectsTools.Attribute.Conductor
        elif currentIndex==2:
            self.attribute=ObjectsTools.Attribute.Vacuo
        elif currentIndex==3:
            self.attribute=ObjectsTools.Attribute.Vacuo
    def ComboBox_type_clicked(self):
        currentIndex=self.ui.comboBox_type.currentIndex()
        self.baseObjType=self.ui.comboBox_type.currentText()
        self.setTabEnable(currentIndex)
        # if currentIndex<=4:
        #     self.ui.ComboBox_Shadow_Attribute.setEditable(False)
    #测试时间
    def time_me(fn):
        def _wrapper(*args, **kwargs):
            start = time.clock()
            fn(*args, **kwargs)
            FreeCAD.Console.PrintError("Array time: "+str(time.clock()-start)+"\n")
            # print "%s cost %s second"%(fn.__name__, time.clock() - start)
        return _wrapper
    
    @time_me
    def pushBtnOk(self):
        doc=FreeCAD.ActiveDocument
        # 删除基础体
        if self.obj:
            for shapeItem in self.obj.Shapes:
                doc.removeObject(shapeItem.Name)
        #
        
        grp=doc.Array
        paramObj=ObjectsTools.getParamObj()
        currentIndex=int(self.ui.tabWidget.currentIndex())
        objName=str(self.ui.LineEdit_Name.text())
        # 删除掉名字里多余的空格 @lizhenguang
        objName = objName.replace(' ','')
        self.iStart= str(self.ui.lineEdit_start_i.text())
        self.iEnd=str(self.ui.lineEdit_end_i.text())

        i_start=UnitTools.getValueByStr(str(self.ui.lineEdit_start_i.text()).replace(" ",""))
        i_end=UnitTools.getValueByStr(str(self.ui.lineEdit_end_i.text()).replace(" ",""))
        objsList=[]
        
        IRe=re.compile(r"\bi\b")

        FreeCAD.ActiveDocument.openTransaction("Array")
        # 正投影体
        if currentIndex==0:
            self.baseObjData=str(self.ui.lineEdit_Conformal_Ptn1X.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Conformal_Ptn1Y.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Conformal_Ptn1Z.text()).replace(" ","")+" "+\
                             str(self.ui.lineEdit_Conformal_Ptn2X.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Conformal_Ptn2Y.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Conformal_Ptn2Z.text()).replace(" ","")
                            
            for i in range(i_start,i_end+1):
                if self.currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular or  self.currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:                   
                    ptn1X=str(self.ui.lineEdit_Conformal_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Conformal_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Conformal_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")                    
                    ptn2X=str(self.ui.lineEdit_Conformal_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")                
                    ptn2Y=str(self.ui.lineEdit_Conformal_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")                 
                    ptn2Z=str(self.ui.lineEdit_Conformal_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")                  
                else:
                    # 问题应该是这里
                    ptn1X=str(self.ui.lineEdit_Conformal_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Conformal_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Conformal_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2X=str(self.ui.lineEdit_Conformal_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Y=str(self.ui.lineEdit_Conformal_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Z=str(self.ui.lineEdit_Conformal_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")
                
                objItem=doc.addObject("Part::FeaturePython", objName+str(i))
                objInstance=Model.Vol_Conformal.ConformalInstance.Conformal(objItem,needOrder=False,thistype=ObjectsTools.ObjectType.none)
                Model.Vol_Conformal.ConformalInstance.ViewProviderConformal(objItem.ViewObject)
                objItem.removeProperty("Type")
                # 赋值
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Conformal.Point1+".x",ptn1X)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Conformal.Point1+".y",ptn1Y)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Conformal.Point1+".z",ptn1Z)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Conformal.Point2+".x",ptn2X)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Conformal.Point2+".y",ptn2Y)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Conformal.Point2+".z",ptn2Z)

                objItem.recompute()
                objsList.append(objItem)
            pass
        # 环形体
        elif currentIndex==1:
            # # 删除之前的类型的属性
            # if self.beforeType!=1:
            #     self.changeTypePros()
            self.baseObjData=str(self.ui.lineEdit_Annular_Ptn1X.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Annular_Ptn1Y.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Annular_Ptn1Z.text()).replace(" ","")+" "+\
                             str(self.ui.lineEdit_Annular_Ptn2X.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Annular_Ptn2Y.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Annular_Ptn2Z.text()).replace(" ","")+" "+\
                             str(self.ui.lineEdit_Annular_RadInner.text()).replace(" ","")+" "+\
                             str(self.ui.lineEdit_Annular_RadOuter.text()).replace(" ","")
            for i in range(i_start,i_end+1):
                if self.currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular or  self.currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:                   
                    
                    ptn1X=str(self.ui.lineEdit_Annular_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Annular_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Annular_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")                    
                    ptn2X=str(self.ui.lineEdit_Annular_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")                
                    ptn2Y=str(self.ui.lineEdit_Annular_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")                 
                    ptn2Z=str(self.ui.lineEdit_Annular_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")                  
                else:
                    ptn1X=str(self.ui.lineEdit_Annular_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Annular_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Annular_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2X=str(self.ui.lineEdit_Annular_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Y=str(self.ui.lineEdit_Annular_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Z=str(self.ui.lineEdit_Annular_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")
                radInner=str(self.ui.lineEdit_Annular_RadInner.text()).replace("\'i\'",str(i)).replace(" ","")
                radOutter=str(self.ui.lineEdit_Annular_RadOuter.text()).replace("\'i\'",str(i)).replace(" ","")
                # # 处理输入中的i而不是'i'
                # ptn1X=IRe.sub(str(i),ptn1X)
                # ptn1Y=IRe.sub(str(i),ptn1Y)
                # ptn1Z=IRe.sub(str(i),ptn1Z)
                # ptn2X=IRe.sub(str(i),ptn2X)
                # ptn2Y=IRe.sub(str(i),ptn2Y)
                # ptn2Z=IRe.sub(str(i),ptn2Z)
                # radInner.sub(str(i),radInner)
                # radOutter.sub(str(i),radOutter)

                objItem=doc.addObject("Part::FeaturePython", objName+str(i))
                objInstance=Model.Vol_Annular.AnnularInstance.Annular(objItem,needOrder=False,thistype=ObjectsTools.ObjectType.none)
                Model.Vol_Annular.AnnularInstance.ViewProviderAnnular(objItem.ViewObject)
                objItem.removeProperty("Type")
                # 赋值
                self.setValue(objItem,"Point_1.x",ptn1X)
                self.setValue(objItem,"Point_1.y",ptn1Y)
                self.setValue(objItem,"Point_1.z",ptn1Z)
                self.setValue(objItem,"Point_2.x",ptn2X)
                self.setValue(objItem,"Point_2.y",ptn2Y)
                self.setValue(objItem,"Point_2.z",ptn2Z)

                self.setValue(objItem,"RadiusInside",radInner)
                self.setValue(objItem,"RadiusOutside",radOutter)

                objItem.recompute()
                objsList.append(objItem)
            pass
        # 圆柱体
        elif currentIndex==2:
            self.baseObjData=str(self.ui.lineEdit_Cylinder_Ptn1X.text())+","+\
                             str(self.ui.lineEdit_Cylinder_Ptn1Y.text())+","+\
                             str(self.ui.lineEdit_Cylinder_Ptn1Z.text())+" "+\
                             str(self.ui.lineEdit_Cylinder_Ptn2X.text())+","+\
                             str(self.ui.lineEdit_Cylinder_Ptn2Y.text())+","+\
                             str(self.ui.lineEdit_Cylinder_Ptn2Z.text())+" "+\
                             str(self.ui.lineEdit_Cylinder_Rad.text())
            for i in range(i_start,i_end+1):
                if self.currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular or  self.currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:                   
                    ptn1X=str(self.ui.lineEdit_Cylinder_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Cylinder_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Cylinder_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2X=str(self.ui.lineEdit_Cylinder_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Y=str(self.ui.lineEdit_Cylinder_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Z=str(self.ui.lineEdit_Cylinder_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")
                else:
                    ptn1X=str(self.ui.lineEdit_Cylinder_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Cylinder_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Cylinder_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2X=str(self.ui.lineEdit_Cylinder_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Y=str(self.ui.lineEdit_Cylinder_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Z=str(self.ui.lineEdit_Cylinder_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")

                rad=str(self.ui.lineEdit_Cylinder_Rad.text()).replace("\'i\'",str(i)).replace(" ","")
                # # 处理输入中的i而不是'i'
                # ptn1X=IRe.sub(str(i),ptn1X)
                # ptn1Y=IRe.sub(str(i),ptn1Y)
                # ptn1Z=IRe.sub(str(i),ptn1Z)
                # ptn2X=IRe.sub(str(i),ptn2X)
                # ptn2Y=IRe.sub(str(i),ptn2Y)
                # ptn2Z=IRe.sub(str(i),ptn2Z)
                # rad=IRe.sub(str(i),rad)

                objItem=doc.addObject("Part::FeaturePython", objName+str(i))
                objInstance=Model.Vol_Cylinder.CylinderInstance.Cylinder(objItem,needOrder=False,thistype=ObjectsTools.ObjectType.none)
                Model.Vol_Cylinder.CylinderInstance.ViewProviderCylinder(objItem.ViewObject)
                objItem.removeProperty("Type")
                # 赋值
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Cylinder.Point_1+".x",ptn1X)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Cylinder.Point_1+".y",ptn1Y)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Cylinder.Point_1+".z",ptn1Z)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Cylinder.Point_2+".x",ptn2X)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Cylinder.Point_2+".y",ptn2Y)
                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Cylinder.Point_2+".z",ptn2Z)

                self.setValue(objItem,ObjectsTools.PropertiesOfObj.Cylinder.Radius,rad)

                objItem.recompute()
                objsList.append(objItem)
            pass
        # 圆台体
        elif currentIndex==3:
            self.baseObjData=str(self.ui.lineEdit_Cone_Ptn1X.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Cone_Ptn1Y.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Cone_Ptn1Z.text()).replace(" ","")+" "+\
                             str(self.ui.lineEdit_Cone_Ptn2X.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Cone_Ptn2Y.text()).replace(" ","")+","+\
                             str(self.ui.lineEdit_Cone_Ptn2Z.text()).replace(" ","")+" "+\
                             str(self.ui.lineEdit_Cone_RadBott.text()).replace(" ","")+" "+\
                             str(self.ui.lineEdit_Cone_RadUp.text()).replace(" ","")
            for i in range(i_start,i_end+1):
                if self.currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular or  self.currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:                   
                    
                    ptn1X=str(self.ui.lineEdit_Cone_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Cone_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Cone_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")                    
                    ptn2X=str(self.ui.lineEdit_Cone_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")                
                    ptn2Y=str(self.ui.lineEdit_Cone_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")                 
                    ptn2Z=str(self.ui.lineEdit_Cone_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")                  
                else:
                    ptn1X=str(self.ui.lineEdit_Cone_Ptn1Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Y=str(self.ui.lineEdit_Cone_Ptn1Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn1Z=str(self.ui.lineEdit_Cone_Ptn1X.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2X=str(self.ui.lineEdit_Cone_Ptn2Y.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Y=str(self.ui.lineEdit_Cone_Ptn2Z.text()).replace("\'i\'",str(i)).replace(" ","")
                    ptn2Z=str(self.ui.lineEdit_Cone_Ptn2X.text()).replace("\'i\'",str(i)).replace(" ","")
                radBott=str(self.ui.lineEdit_Cone_RadBott.text()).replace("\'i\'",str(i)).replace(" ","")
                radUp=str(self.ui.lineEdit_Cone_RadUp.text()).replace("\'i\'",str(i)).replace(" ","")


                objItem=doc.addObject("Part::FeaturePython", objName+str(i))
                # objInstance=Model.Vol_Annular.AnnularInstance.Annular(objItem,needOrder=False,thistype=ObjectsTools.ObjectType.none)
                # Model.Vol_Annular.AnnularInstance.ViewProviderAnnular(objItem.ViewObject)
                objInstance=Model.Vol_SpecialCone.SpecialConeInstance.SpecialCone(objItem,needOrder=False,thistype=ObjectsTools.ObjectType.none)
                Model.Vol_SpecialCone.SpecialConeInstance.ViewProviderSpecialCone(objItem.ViewObject)
                objItem.removeProperty("Type")
                # 赋值
                self.setValue(objItem,"PointBottom.x",ptn1X)
                self.setValue(objItem,"PointBottom.y",ptn1Y)
                self.setValue(objItem,"PointBottom.z",ptn1Z)
                self.setValue(objItem,"PointTop.x",ptn2X)
                self.setValue(objItem,"PointTop.y",ptn2Y)
                self.setValue(objItem,"PointTop.z",ptn2Z)

                self.setValue(objItem,"RadiusBottom",radBott)
                self.setValue(objItem,"RadiusTop",radUp)

                objItem.recompute()
                objsList.append(objItem)
        # 最后
        if len(objsList)!=0:
            # FreeCAD.ActiveDocument.openTransaction("Array")
            obj=self.obj
            if not obj:
                obj = FreeCAD.ActiveDocument.addObject("Part::CustomFeaturePython",objName)            
                obj.Shapes=objsList
                objInstance=Instance.Array(obj)
            else:
                obj.Shapes=objsList 
                obj.Proxy.redraw(obj)
            obj.BaseObjType=self.baseObjType
            obj.BaseObjData=self.baseObjData
            obj.Attribute=self.attribute
            self.setValue(obj,"IFrom",self.iStart)
            self.setValue(obj,"ITo",self.iEnd)
            obj.Label=objName
            # obj.IFrom=self.iStart
            # obj.ITo=self.iEnd
            FreeCAD.ActiveDocument.commitTransaction()
            #设置非均匀网格属性
            if self.currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular:
                obj.X=self.ui.checkBox_UniformX.isChecked()
                obj.Y=self.ui.checkBox_UniformY.isChecked()
                obj.Z=self.ui.checkBox_UniformZ.isChecked()

                uniforX=str(self.ui.lineEdit_UniformX.text()).replace(" ","")
                uniforY=str(self.ui.lineEdit_UniformY.text()).replace(" ","")
                uniforZ=str(self.ui.lineEdit_UniformZ.text()).replace(" ","")
                
                self.setValue(obj,"X_Value",uniforX)
                self.setValue(obj,"Y_Value",uniforY)
                self.setValue(obj,"Z_Value",uniforZ)
            elif self.currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:
                obj.R=self.ui.checkBox_UniformX.isChecked()
                obj.Theta=self.ui.checkBox_UniformY.isChecked()
                obj.Z=self.ui.checkBox_UniformZ.isChecked()

                uniforX=str(self.ui.lineEdit_UniformX.text()).replace(" ","")
                uniforY=str(self.ui.lineEdit_UniformY.text()).replace(" ","")
                uniforZ=str(self.ui.lineEdit_UniformZ.text()).replace(" ","")
                
                self.setValue(obj,"R_Value",uniforX)
                self.setValue(obj,"Theta_Value",uniforY)
                self.setValue(obj,"Z_Value",uniforZ)
            else:
                obj.Z=self.ui.checkBox_UniformX.isChecked()
                obj.R=self.ui.checkBox_UniformY.isChecked()
                obj.Theta=self.ui.checkBox_UniformZ.isChecked()

                uniforZ=str(self.ui.lineEdit_UniformX.text()).replace(" ","")
                uniforR=str(self.ui.lineEdit_UniformY.text()).replace(" ","")
                uniforTheta=str(self.ui.lineEdit_UniformZ.text()).replace(" ","")

                self.setValue(obj,"Z_Value",uniforZ)
                self.setValue(obj,"R_Value",uniforR)
                self.setValue(obj,"Theta_Value",uniforTheta)
            
        doc.recompute()

        #更新布尔运算
        DocumentTools.updateBoolean()
        self.close()
    def cancelBtnClick(self):
        self.close()
    # 删除之前type的属性
    def changeTypePros(self):
        dictPros={}
        if self.obj:
            # 先删除之前的体属性
            if self.beforeType==0:
                dictPros=ObjectsTools.PropertiesOfObj.Vol_Conformal
                for proItemKey in dictPros:
                    obj.removeProperty(proItemKey)
        if self.baseObjType==0:
            dictPros=ObjectsTools.PropertiesOfObj.Vol_Conformal
            for proItemKey in dictPros:
                obj.addProperty("App::PropertyString",proItemKey)
    # 根据字符串（常量或者参数）赋值
    def setValue(self,obj,paramName,paramValue):
        paramObj=ObjectsTools.getParamObj()
        result=UnitTools.getTypeOfPossiblePropertyName(paramObj,"",paramValue,isParamObjSelf=False)
        FreeCAD.Console.PrintMessage("value: "+str(result)+"\n")
        if result[0]!=""and result[1]!=UnitTools.SupportUnitType.STRING:
            obj.setExpression(paramName,result[0])
    #初始化面板显示
    def initFialog(self):
        if self.currentCoordinate==CoordinateSystemTools.CoordinateType.Rectangular:
            for i in range(self.ui.tabWidget.count()):
                try:
                    getattr(self.ui,"label_X"+str(i)).setText("X")
                    getattr(self.ui,"label_Y"+str(i)).setText("Y")
                    getattr(self.ui,"label_Z"+str(i)).setText("Z")
                except:
                    FreeCAD.Console.PrintError("label_"+str(i)+" Wrong\n")
                    
            self.ui.checkBox_UniformX.setText("X")
            self.ui.checkBox_UniformY.setText("Y")
            self.ui.checkBox_UniformZ.setText("Z")
        elif self.currentCoordinate==CoordinateSystemTools.CoordinateType.Polar:
            for i in range(self.ui.tabWidget.count()):
                try:
                    getattr(self.ui,"label_X"+str(i)).setText("R")
                    getattr(self.ui,"label_Y"+str(i)).setText("Theta")
                    getattr(self.ui,"label_Z"+str(i)).setText("Z")
                except:
                    FreeCAD.Console.PrintError("label_"+str(i)+" Wrong\n")                    
            # self.ui.label_X.setText("R")
            # self.ui.label_Y.setText("Theta")
            # self.ui.label_Z.setText("Z")

            self.ui.checkBox_UniformX.setText("R")
            self.ui.checkBox_UniformY.setText("Theta")
            self.ui.checkBox_UniformZ.setText("Z")
        else:
            for i in range(self.ui.tabWidget.count()):
                try:
                    getattr(self.ui,"label_X"+str(i)).setText("Z")
                    getattr(self.ui,"label_Y"+str(i)).setText("R")
                    getattr(self.ui,"label_Z"+str(i)).setText("Theta")
                except:
                    FreeCAD.Console.PrintError("label_"+str(i)+" Wrong\n")                     
            # self.ui.label_X.setText("Z")
            # self.ui.label_Y.setText("R")
            # self.ui.label_Z.setText("Theta")

            self.ui.checkBox_UniformX.setText("Z")
            self.ui.checkBox_UniformY.setText("R")
            self.ui.checkBox_UniformZ.setText("Theta")  


def syna(msg):
    FreeCAD.Console.PrintMessage("\n")
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")

        

class CreateNewVolArrayCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        dlg=VolArray()
        dlg.show()
        # dlg.exec_()
        dlg.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_ParamArray.svg"
        MenuText = QT_TRANSLATE_NOOP(
            'CreateNewVolArrayCommand',
            'Create Param Array')
        ToolTip = QT_TRANSLATE_NOOP(
            'CreateNewVolArrayCommand',
            'Create Param Array')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateNewVolArrayCommand',CreateNewVolArrayCommand())