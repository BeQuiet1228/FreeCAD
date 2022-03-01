#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
import SphericalDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD
import ProjectSetting
import re

class showSphericalDialog(showObjDialog):
    def __init__(self, obj, parent=None):
        #手动调用父类构造函数。
        showObjDialog.__init__(self,obj,parent)
        #设置ui文件
        self.ui = SphericalDialog.Ui_Dialog()
        self.ui.setupUi(self)
        #初始化对话框
        self.initDialog()

        self.ui.lineEdit_4.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_5.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_6.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_7.setcompleterlist(getGlobalVar())

        self.obj = obj
        self.error = ''

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.move(screen.right()-self.size().width()-150, screen.bottom()*0.5-200)
        self.DisplayMode()

        self.setUI()
    def setDefaultValue(self):
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            if length =='mm':
                str_1 ='0'+length
                str_2 = '0'+length
                str_r = '0'+length
            elif length == 'cm':
                str_1 = '0'+length
                str_2 = '0'+length
                str_r = '0'+length
            elif length == 'm':
                str_1 = '0'+length
                str_2 = '0'+length
                str_r = '0'+length
            str_3 = '0'+length

            # self.ui.lineEdit.setText(str_1)
            # self.ui.lineEdit_2.setText(str_3)
            # self.ui.lineEdit_3.setText(str_3)
            self.ui.lineEdit_4.setText(str_2)
            self.ui.lineEdit_5.setText(str_3)
            self.ui.lineEdit_6.setText(str_3)
            self.ui.lineEdit_7.setText(str_r)
            # self.ui.lineEdit_8.setText(str_r)
        else:
            if length =='mm':
                str_z1 ='0'+length
                str_z2 = '0'+length
                str_r = '0'+length
            elif length == 'cm':
                str_z1 = '0'+length
                str_z2 = '0'+length
                str_r = '0'+length
            elif length == 'm':
                str_z1 = '0'+length
                str_z2 = '0'+length
                str_r = '0'+length
            str_3 = '0'+length
            if angle == 'deg':
                str_theta = '0'+angle
            else :
                str_theta = '0'+angle
            # self.ui.lineEdit.setText(str_z1)
            # self.ui.lineEdit_2.setText(str_theta)
            # self.ui.lineEdit_3.setText(str_3)
            self.ui.lineEdit_4.setText(str_z2)
            self.ui.lineEdit_5.setText(str_theta)
            self.ui.lineEdit_6.setText(str_3)
            self.ui.lineEdit_7.setText(str_r) 
            # self.ui.lineEdit_8.setText(str_r)
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6)

            pass
    def settheLocation(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('CenterPoint.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('CenterPoint.x',None)
                    self.obj.CenterPoint.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point.x'+'  '+str(point_2_x_before)+'\n'

            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.Stringfunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('CenterPoint.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('CenterPoint.y',None)
                    self.obj.CenterPoint.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point.y'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('CenterPoint.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('CenterPoint.z',None)
                    self.obj.CenterPoint.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point.z'+'  '+str(point_2_z_before)+'\n'
                
            point_r_before=self.ui.lineEdit_7.text()
            point_r_after=InputTools.Stringfunctions(point_r_before)
            try:
                if point_r_after[1]==2:
                    self.obj.setExpression('Radius',point_r_after[0])
                else:
                    self.obj.setExpression('Radius',None)
                    self.obj.Radius=point_r_after[0]
            except:
                self.error=self.error+'Radius'+'  '+str(point_r_before)+'\n'
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('CenterPoint.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('CenterPoint.x',None)
                    self.obj.CenterPoint.x=point_2_x_after[0]
            except:
                self.error=self.error+'CenterPoint.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('CenterPoint.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('CenterPoint.y',None)
                    self.obj.CenterPoint.y=point_2_y_after[0]
            except:
                self.error=self.error+'CenterPoint.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('CenterPoint.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('CenterPoint.z',None)
                    self.obj.CenterPoint.z=point_2_z_after[0]
            except:
                self.error=self.error+'CenterPoint.Z'+'  '+str(point_2_z_before)+'\n'

            point_r_before=self.ui.lineEdit_7.text()
            point_r_after=InputTools.Stringfunctions(point_r_before)
            try:
                if point_r_after[1]==2:
                    self.obj.setExpression('Radius',point_r_after[0])
                else:
                    self.obj.setExpression('Radius',None)
                    self.obj.Radius=point_r_after[0]
            except:
                self.error=self.error+'Radius'+'  '+str(point_r_before)+'\n'
        else:
            point_2_x_before=self.ui.lineEdit_5.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('CenterPoint.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('CenterPoint.x',None)
                    self.obj.CenterPoint.x=point_2_x_after[0]
            except:
                self.error=self.error+'CenterPoint.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_6.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('CenterPoint.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('CenterPoint.y',None)
                    self.obj.CenterPoint.y=point_2_y_after[0]
            except:
                self.error=self.error+'CenterPoint.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_4.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('CenterPoint.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('CenterPoint.z',None)
                    self.obj.CenterPoint.z=point_2_z_after[0]
            except:
                self.error=self.error+'CenterPoint.Z'+'  '+str(point_2_z_before)+'\n'

            point_r_before=self.ui.lineEdit_7.text()
            point_r_after=InputTools.Stringfunctions(point_r_before)
            try:
                if point_r_after[1]==2:
                    self.obj.setExpression('Radius',point_r_after[0])
                else:
                    self.obj.setExpression('Radius',None)
                    self.obj.Radius=point_r_after[0]
            except:
                self.error=self.error+'Radius'+'  '+str(point_r_before)+'\n'

            pass
class reshowSphericalDialog(showSphericalDialog):
    def deleteobj(self):
        pass
    def setDefaultValue(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            list1=self.obj.ExpressionEngine
            list2=['','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'CenterPoint.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'CenterPoint.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'CenterPoint.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'Radius':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
            
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.CenterPoint.x,length))+length
                    elif x==1:
                        list2[x]=str(ValueUnitslength(self.obj.CenterPoint.y,length))+length
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.CenterPoint.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(float(self.obj.Radius.Value),length))+length

            # self.ui.lineEdit.setText(list2[0])
            # self.ui.lineEdit_2.setText(list2[1])
            # self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[0])
            self.ui.lineEdit_5.setText(list2[1])
            self.ui.lineEdit_6.setText(list2[2])
            self.ui.lineEdit_7.setText(list2[3])
        else:
            list1=self.obj.ExpressionEngine
            list2=['','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'CenterPoint.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'CenterPoint.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'CenterPoint.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'Radius':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
                
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.CenterPoint.x,length))+length
                    elif x==1:
                        # list2[x]=str(self.obj.Point_1.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.CenterPoint.y,angle))+angle
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.CenterPoint.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(float(self.obj.Radius.Value),length))+length

            # self.ui.lineEdit.setText(list2[0])
            # self.ui.lineEdit_2.setText(list2[1])
            # self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[0])
            self.ui.lineEdit_5.setText(list2[1])
            self.ui.lineEdit_6.setText(list2[2])
            self.ui.lineEdit_7.setText(list2[3])
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6)
