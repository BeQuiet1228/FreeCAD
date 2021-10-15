#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
import SpecialConeDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD
import ProjectSetting
import re

class showSpecialConeDialog(showObjDialog):
    def __init__(self, obj, parent=None):
        #手动调用父类构造函数。
        showObjDialog.__init__(self,obj,parent)
        #设置ui文件
        self.ui = SpecialConeDialog.Ui_Dialog()
        self.ui.setupUi(self)
        #初始化对话框
        self.initDialog()

        self.ui.lineEdit.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_2.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_3.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_4.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_5.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_6.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_7.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_8.setcompleterlist(getGlobalVar())

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

            self.ui.lineEdit.setText(str_1)
            self.ui.lineEdit_2.setText(str_3)
            self.ui.lineEdit_3.setText(str_3)
            self.ui.lineEdit_4.setText(str_2)
            self.ui.lineEdit_5.setText(str_3)
            self.ui.lineEdit_6.setText(str_3)
            self.ui.lineEdit_7.setText(str_r)
            self.ui.lineEdit_8.setText(str_r)
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
            self.ui.lineEdit.setText(str_z1)
            self.ui.lineEdit_2.setText(str_theta)
            self.ui.lineEdit_3.setText(str_3)
            self.ui.lineEdit_4.setText(str_z2)
            self.ui.lineEdit_5.setText(str_theta)
            self.ui.lineEdit_6.setText(str_3)
            self.ui.lineEdit_7.setText(str_r)
            self.ui.lineEdit_8.setText(str_r) 
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6) 

            pass
    def settheLocation(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('PointBottom.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('PointBottom.x',None)
                    self.obj.PointBottom.x=point_1_x_after[0]
            except:
                self.error=self.error+'PointBottom.x'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.Stringfunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('PointBottom.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('PointBottom.y',None)
                    self.obj.PointBottom.y=point_1_y_after[0]
            except:
                self.error=self.error+'PointBottom.y'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('PointBottom.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('PointBottom.z',None)
                    self.obj.PointBottom.z=point_1_z_after[0]
            except:
                self.error=self.error+'PointBottom.z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('PointTop.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('PointTop.x',None)
                    self.obj.PointTop.x=point_2_x_after[0]
            except:
                self.error=self.error+'PointTop.x'+'  '+str(point_2_x_before)+'\n'

            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.Stringfunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('PointTop.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('PointTop.y',None)
                    self.obj.PointTop.y=point_2_y_after[0]
            except:
                self.error=self.error+'PointTop.y'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('PointTop.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('PointTop.z',None)
                    self.obj.PointTop.z=point_2_z_after[0]
            except:
                self.error=self.error+'PointTop.z'+'  '+str(point_2_z_before)+'\n'
                
            point_rb_before=self.ui.lineEdit_7.text()
            point_rb_after=InputTools.Stringfunctions(point_rb_before)
            try:
                if point_rb_after[1]==2:
                    self.obj.setExpression('RadiusBottom',point_rb_after[0])
                else:
                    self.obj.setExpression('RadiusBottom',None)
                    self.obj.RadiusBottom=point_rb_after[0]
            except:
                self.error=self.error+'RadiusBottom'+'  '+str(point_rb_before)+'\n'

            point_rt_before=self.ui.lineEdit_8.text()
            point_rt_after=InputTools.Stringfunctions(point_rt_before)
            try:
                if point_rt_after[1]==2:
                    self.obj.setExpression('RadiusTop',point_rt_after[0])
                else:
                    self.obj.setExpression('RadiusTop',None)
                    self.obj.RadiusTop=point_rt_after[0]
            except:
                self.error=self.error+'RadiusTop'+'  '+str(point_rt_before)+'\n'
                
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('PointBottom.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('PointBottom.x',None)
                    self.obj.PointBottom.x=point_1_x_after[0]
            except:
                self.error=self.error+'PointBottom.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('PointBottom.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('PointBottom.y',None)
                    self.obj.PointBottom.y=point_1_y_after[0]
            except:
                self.error=self.error+'PointBottom.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('PointBottom.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('PointBottom.z',None)
                    self.obj.PointBottom.z=point_1_z_after[0]
            except:
                self.error=self.error+'PointBottom.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('PointTop.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('PointTop.x',None)
                    self.obj.PointTop.x=point_2_x_after[0]
            except:
                self.error=self.error+'PointTop.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('PointTop.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('PointTop.y',None)
                    self.obj.PointTop.y=point_2_y_after[0]
            except:
                self.error=self.error+'PointTop.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('PointTop.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('PointTop.z',None)
                    self.obj.PointTop.z=point_2_z_after[0]
            except:
                self.error=self.error+'PointTop.Z'+'  '+str(point_2_z_before)+'\n'

            point_rb_before=self.ui.lineEdit_7.text()
            point_rb_after=InputTools.Stringfunctions(point_rb_before)
            try:
                if point_rb_after[1]==2:
                    self.obj.setExpression('RadiusBottom',point_rb_after[0])
                else:
                    self.obj.setExpression('RadiusBottom',None)
                    self.obj.RadiusBottom=point_rb_after[0]
            except:
                self.error=self.error+'RadiusBottom'+'  '+str(point_rb_before)+'\n'

            point_rt_before=self.ui.lineEdit_8.text()
            point_rt_after=InputTools.Stringfunctions(point_rt_before)
            try:
                if point_rt_after[1]==2:
                    self.obj.setExpression('RadiusTop',point_rt_after[0])
                else:
                    self.obj.setExpression('RadiusTop',None)
                    self.obj.RadiusTop=point_rt_after[0]
            except:
                self.error=self.error+'RadiusTop'+'  '+str(point_rt_before)+'\n'
        else:
            point_1_x_before=self.ui.lineEdit_2.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('PointBottom.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('PointBottom.x',None)
                    self.obj.PointBottom.x=point_1_x_after[0]
            except:
                self.error=self.error+'PointBottom.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_3.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('PointBottom.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('PointBottom.y',None)
                    self.obj.PointBottom.y=point_1_y_after[0]
            except:
                self.error=self.error+'PointBottom.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('PointBottom.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('PointBottom.z',None)
                    self.obj.PointBottom.z=point_1_z_after[0]
            except:
                self.error=self.error+'PointBottom.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_5.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('PointTop.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('PointTop.x',None)
                    self.obj.PointTop.x=point_2_x_after[0]
            except:
                self.error=self.error+'PointTop.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_6.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('PointTop.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('PointTop.y',None)
                    self.obj.PointTop.y=point_2_y_after[0]
            except:
                self.error=self.error+'PointTop.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_4.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('PointTop.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('PointTop.z',None)
                    self.obj.PointTop.z=point_2_z_after[0]
            except:
                self.error=self.error+'PointTop.Z'+'  '+str(point_2_z_before)+'\n'

            point_rb_before=self.ui.lineEdit_7.text()
            point_rb_after=InputTools.Stringfunctions(point_rb_before)
            try:
                if point_rb_after[1]==2:
                    self.obj.setExpression('RadiusBottom',point_rb_after[0])
                else:
                    self.obj.setExpression('RadiusBottom',None)
                    self.obj.RadiusBottom=point_rb_after[0]
            except:
                self.error=self.error+'RadiusBottom'+'  '+str(point_rb_before)+'\n'

            point_rt_before=self.ui.lineEdit_8.text()
            point_rt_after=InputTools.Stringfunctions(point_rt_before)
            try:
                if point_rt_after[1]==2:
                    self.obj.setExpression('RadiusTop',point_rt_after[0])
                else:
                    self.obj.setExpression('RadiusTop',None)
                    self.obj.RadiusTop=point_rt_after[0]
            except:
                self.error=self.error+'RadiusTop'+'  '+str(point_rt_before)+'\n'


            pass
class reshowSpecialConeDialog(showSpecialConeDialog):
    def deleteobj(self):
        pass

    def setDefaultValue(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'PointBottom.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'PointBottom.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'PointBottom.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'PointTop.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
                elif list1[i][0] == 'PointTop.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[4]=str1
                elif list1[i][0] == 'PointTop.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[5]=str1
                elif list1[i][0] == 'RadiusBottom':
                    str1=list1[i][1].replace('Param.','')
                    list2[6]=str1
                elif list1[i][0] == 'RadiusTop':
                    str1=list1[i][1].replace('Param.','')
                    list2[7]=str1
            
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.PointBottom.x,length))+length
                    elif x==1:
                        list2[x]=str(ValueUnitslength(self.obj.PointBottom.y,length))+length
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.PointBottom.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(self.obj.PointTop.x,length))+length
                    elif x==4:
                        list2[x]=str(ValueUnitslength(self.obj.PointTop.y,length))+length
                    elif x==5:
                        list2[x]=str(ValueUnitslength(self.obj.PointTop.z,length))+length
                    elif x==6:
                        # number = filter(str.isdigit,  str(self.obj.Radius))
                        list2[x]=str(ValueUnitslength(float(self.obj.RadiusBottom.Value),length))+length
                    elif x==7:
                        # number = filter(str.isdigit,  str(self.obj.Radius))
                        list2[x]=str(ValueUnitslength(float(self.obj.RadiusTop.Value),length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
            self.ui.lineEdit_7.setText(list2[6])
            self.ui.lineEdit_8.setText(list2[7])
        else:
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'PointBottom.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'PointBottom.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'PointBottom.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'PointTop.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
                elif list1[i][0] == 'PointTop.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[4]=str1
                elif list1[i][0] == 'PointTop.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[5]=str1
                elif list1[i][0] == 'RadiusBottom':
                    str1=list1[i][1].replace('Param.','')
                    list2[6]=str1
                elif list1[i][0] == 'RadiusTop':
                    str1=list1[i][1].replace('Param.','')
                    list2[7]=str1
                
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.PointBottom.x,length))+length
                    elif x==1:
                        # list2[x]=str(self.obj.Point_1.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.PointBottom.y,angle))+angle
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.PointBottom.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(self.obj.PointTop.x,length))+length
                    elif x==4:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.PointTop.y,angle))+angle
                    elif x==5:
                        list2[x]=str(ValueUnitslength(self.obj.PointTop.z,length))+length
                    elif x==6:
                        # number = filter(str.isdigit,  str(self.obj.Radius))
                        list2[x]=str(ValueUnitslength(float(self.obj.RadiusBottom.Value),length))+length
                    elif x==7:
                        # number = filter(str.isdigit,  str(self.obj.Radius))
                        list2[x]=str(ValueUnitslength(float(self.obj.RadiusTop.Value),length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
            self.ui.lineEdit_7.setText(list2[6])
            self.ui.lineEdit_8.setText(list2[7])
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6) 