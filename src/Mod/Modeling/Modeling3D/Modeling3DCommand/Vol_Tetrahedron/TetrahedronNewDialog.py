#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
import TetrahedronDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD
import ProjectSetting
import re

class showTetrahedronDialog(showObjDialog):
    def __init__(self, obj, parent=None):
        #手动调用父类构造函数。
        showObjDialog.__init__(self,obj,parent)
        #设置ui文件
        self.ui = TetrahedronDialog.Ui_Dialog()
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
        self.ui.lineEdit_9.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_10.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_11.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_12.setcompleterlist(getGlobalVar())

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
            self.ui.lineEdit_7.setText(str_1)
            self.ui.lineEdit_8.setText(str_3)
            self.ui.lineEdit_9.setText(str_3)
            self.ui.lineEdit_10.setText(str_2)
            self.ui.lineEdit_11.setText(str_3)
            self.ui.lineEdit_12.setText(str_3)
            
            
            
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
            self.ui.lineEdit_7.setText(str_z1)
            self.ui.lineEdit_8.setText(str_theta)
            self.ui.lineEdit_9.setText(str_3)
            self.ui.lineEdit_10.setText(str_z2)
            self.ui.lineEdit_11.setText(str_theta)
            self.ui.lineEdit_12.setText(str_3)
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6)
            InputTools.textChangedbefore(self.ui.lineEdit_7,self.ui.lineEdit_8,self.ui.lineEdit_9)
            InputTools.textChangedbefore(self.ui.lineEdit_10,self.ui.lineEdit_11,self.ui.lineEdit_12)
            
            
            
            pass
    def settheLocation(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point_1.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point_1.x',None)
                    self.obj.Point_1.x = point_1_x_after[0]
            except:
                self.error=self.error+'Point_1.x'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.Stringfunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point_1.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point_1.y',None)
                    self.obj.Point_1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point_1.y'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point_1.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point_1.z',None)
                    self.obj.Point_1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point_1.z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point_2.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('Point_2.x',None)
                    self.obj.Point_2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point_2.x'+'  '+str(point_2_x_before)+'\n'

            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.Stringfunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point_2.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('Point_2.y',None)
                    self.obj.Point_2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point_2.y'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point_2.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('Point_2.z',None)
                    self.obj.Point_2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point_2.z'+'  '+str(point_2_z_before)+'\n'

            point_3_x_before=self.ui.lineEdit_7.text()
            point_3_x_after=InputTools.Stringfunctions(point_3_x_before)
            try:
                if point_3_x_after[1]==2:
                    self.obj.setExpression('Point_3.x',point_3_x_after[0])
                else:
                    self.obj.setExpression('Point_3.x',None)
                    self.obj.Point_3.x=point_3_x_after[0]
            except:
                self.error=self.error+'Point_3.x'+'  '+str(point_3_x_before)+'\n'

            point_3_y_before=self.ui.lineEdit_8.text()
            point_3_y_after=InputTools.Stringfunctions(point_3_y_before)
            try:
                if point_3_y_after[1]==2:
                    self.obj.setExpression('Point_3.y',point_3_y_after[0])
                else:
                    self.obj.setExpression('Point_3.y',None)
                    self.obj.Point_3.y=point_3_y_after[0]
            except:
                self.error=self.error+'Point_3.y'+'  '+str(point_3_y_before)+'\n'

            point_3_z_before=self.ui.lineEdit_9.text()
            point_3_z_after=InputTools.Stringfunctions(point_3_z_before)
            try:
                if point_3_z_after[1]==2:
                    self.obj.setExpression('Point_3.z',point_3_z_after[0])
                else:
                    self.obj.setExpression('Point_3.z',None)
                    self.obj.Point_3.z=point_3_z_after[0]
            except:
                self.error=self.error+'Point_3.z'+'  '+str(point_3_z_before)+'\n'

            point_4_x_before=self.ui.lineEdit_10.text()
            point_4_x_after=InputTools.Stringfunctions(point_4_x_before)
            try:
                if point_4_x_after[1]==2:
                    self.obj.setExpression('Point_4.x',point_4_x_after[0])
                else:
                    self.obj.setExpression('Point_4.x',None)
                    self.obj.Point_4.x=point_4_x_after[0]
            except:
                self.error=self.error+'Point_4.x'+'  '+str(point_4_x_before)+'\n'

            point_4_y_before=self.ui.lineEdit_11.text()
            point_4_y_after=InputTools.Stringfunctions(point_4_y_before)
            try:
                if point_4_y_after[1]==2:
                    self.obj.setExpression('Point_4.y',point_4_y_after[0])
                else:
                    self.obj.setExpression('Point_4.y',None)
                    self.obj.Point_4.y=point_4_y_after[0]
            except:
                self.error=self.error+'Point_4.y'+'  '+str(point_4_y_before)+'\n'

            point_4_z_before=self.ui.lineEdit_12.text()
            point_4_z_after=InputTools.Stringfunctions(point_4_z_before)
            try:
                if point_4_z_after[1]==2:
                    self.obj.setExpression('Point_4.z',point_4_z_after[0])
                else:
                    self.obj.setExpression('Point_4.z',None)
                    self.obj.Point_4.z=point_4_z_after[0]
            except:
                self.error=self.error+'Point_4.z'+'  '+str(point_4_z_before)+'\n'


            

                
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point_1.x',point_1_x_after[0])
                else:
                    self.obj.Point_1.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point_1.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point_1.y',point_1_y_after[0])
                else:
                    self.obj.Point_1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point_1.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point_1.z',point_1_z_after[0])
                else:
                    self.obj.Point_1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point_1.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point_2.x',point_2_x_after[0])
                else:
                    self.obj.Point_2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point_2.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point_2.y',point_2_y_after[0])
                else:
                    self.obj.Point_2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point_2.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point_2.z',point_2_z_after[0])
                else:
                    self.obj.Point_2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point_2.Z'+'  '+str(point_2_z_before)+'\n'

            point_3_x_before=self.ui.lineEdit_7.text()
            point_3_x_after=InputTools.Stringfunctions(point_3_x_before)
            try:
                if point_3_x_after[1]==2:
                    self.obj.setExpression('Point_3.x',point_3_x_after[0])
                else:
                    self.obj.Point_3.x=point_3_x_after[0]
            except:
                self.error=self.error+'Point_3.R'+'  '+str(point_3_x_before)+'\n'
            
            point_3_y_before=self.ui.lineEdit_8.text()
            point_3_y_after=InputTools.anglefunctions(point_3_y_before)
            try:
                if point_3_y_after[1]==2:
                    self.obj.setExpression('Point_3.y',point_3_y_after[0])
                else:
                    self.obj.Point_3.y=point_3_y_after[0]
            except:
                self.error=self.error+'Point_3.theta'+'  '+str(point_3_y_before)+'\n'

            point_3_z_before=self.ui.lineEdit_9.text()
            point_3_z_after=InputTools.Stringfunctions(point_3_z_before)
            try:
                if point_3_z_after[1]==2:
                    self.obj.setExpression('Point_3.z',point_3_z_after[0])
                else:
                    self.obj.Point_3.z=point_3_z_after[0]
            except:
                self.error=self.error+'Point_3.Z'+'  '+str(point_3_z_before)+'\n'


            point_4_x_before=self.ui.lineEdit_10.text()
            point_4_x_after=InputTools.Stringfunctions(point_4_x_before)
            try:
                if point_4_x_after[1]==2:
                    self.obj.setExpression('Point_4.x',point_4_x_after[0])
                else:
                    self.obj.Point_4.x=point_4_x_after[0]
            except:
                self.error=self.error+'Point_4.R'+'  '+str(point_4_x_before)+'\n'
            
            point_4_y_before=self.ui.lineEdit_11.text()
            point_4_y_after=InputTools.anglefunctions(point_4_y_before)
            try:
                if point_4_y_after[1]==2:
                    self.obj.setExpression('Point_4.y',point_4_y_after[0])
                else:
                    self.obj.Point_4.y=point_4_y_after[0]
            except:
                self.error=self.error+'Point_4.theta'+'  '+str(point_4_y_before)+'\n'

            point_4_z_before=self.ui.lineEdit_12.text()
            point_4_z_after=InputTools.Stringfunctions(point_4_z_before)
            try:
                if point_4_z_after[1]==2:
                    self.obj.setExpression('Point_4.z',point_4_z_after[0])
                else:
                    self.obj.Point_4.z=point_4_z_after[0]
            except:
                self.error=self.error+'Point_4.Z'+'  '+str(point_4_z_before)+'\n'
        else:
            point_1_x_before=self.ui.lineEdit_2.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point_1.x',point_1_x_after[0])
                else:
                    self.obj.Point_1.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point_1.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_3.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point_1.y',point_1_y_after[0])
                else:
                    self.obj.Point_1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point_1.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point_1.z',point_1_z_after[0])
                else:
                    self.obj.Point_1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point_1.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_5.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point_2.x',point_2_x_after[0])
                else:
                    self.obj.Point_2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point_2.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_6.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point_2.y',point_2_y_after[0])
                else:
                    self.obj.Point_2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point_2.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_4.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point_2.z',point_2_z_after[0])
                else:
                    self.obj.Point_2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point_2.Z'+'  '+str(point_2_z_before)+'\n'

            point_3_x_before=self.ui.lineEdit_8.text()
            point_3_x_after=InputTools.Stringfunctions(point_3_x_before)
            try:
                if point_3_x_after[1]==2:
                    self.obj.setExpression('Point_3.x',point_3_x_after[0])
                else:
                    self.obj.Point_3.x=point_3_x_after[0]
            except:
                self.error=self.error+'Point_3.R'+'  '+str(point_3_x_before)+'\n'
            
            point_3_y_before=self.ui.lineEdit_9.text()
            point_3_y_after=InputTools.anglefunctions(point_3_y_before)
            try:
                if point_3_y_after[1]==2:
                    self.obj.setExpression('Point_3.y',point_3_y_after[0])
                else:
                    self.obj.Point_3.y=point_3_y_after[0]
            except:
                self.error=self.error+'Point_3.theta'+'  '+str(point_3_y_before)+'\n'

            point_3_z_before=self.ui.lineEdit_7.text()
            point_3_z_after=InputTools.Stringfunctions(point_3_z_before)
            try:
                if point_3_z_after[1]==2:
                    self.obj.setExpression('Point_3.z',point_3_z_after[0])
                else:
                    self.obj.Point_3.z=point_3_z_after[0]
            except:
                self.error=self.error+'Point_3.Z'+'  '+str(point_3_z_before)+'\n'


            point_4_x_before=self.ui.lineEdit_11.text()
            point_4_x_after=InputTools.Stringfunctions(point_4_x_before)
            try:
                if point_4_x_after[1]==2:
                    self.obj.setExpression('Point_4.x',point_4_x_after[0])
                else:
                    self.obj.Point_4.x=point_4_x_after[0]
            except:
                self.error=self.error+'Point_4.R'+'  '+str(point_4_x_before)+'\n'
            
            point_4_y_before=self.ui.lineEdit_12.text()
            point_4_y_after=InputTools.anglefunctions(point_4_y_before)
            try:
                if point_4_y_after[1]==2:
                    self.obj.setExpression('Point_4.y',point_4_y_after[0])
                else:
                    self.obj.Point_4.y=point_4_y_after[0]
            except:
                self.error=self.error+'Point_4.theta'+'  '+str(point_4_y_before)+'\n'

            point_4_z_before=self.ui.lineEdit_10.text()
            point_4_z_after=InputTools.Stringfunctions(point_4_z_before)
            try:
                if point_4_z_after[1]==2:
                    self.obj.setExpression('Point_4.z',point_4_z_after[0])
                else:
                    self.obj.Point_4.z=point_4_z_after[0]
            except:
                self.error=self.error+'Point_4.Z'+'  '+str(point_4_z_before)+'\n'

            


            pass

class reshowTetrahedronDialog(showTetrahedronDialog):
    def deleteobj(self):
        pass

    def setDefaultValue(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','','','','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'Point_1.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'Point_1.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'Point_1.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'Point_2.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
                elif list1[i][0] == 'Point_2.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[4]=str1
                elif list1[i][0] == 'Point_2.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[5]=str1
                elif list1[i][0] == 'Point_3.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[6]=str1
                elif list1[i][0] == 'Point_3.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[7]=str1
                elif list1[i][0] == 'Point_3.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[8]=str1
                elif list1[i][0] == 'Point_4.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[9]=str1
                elif list1[i][0] == 'Point_4.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[10]=str1
                elif list1[i][0] == 'Point_4.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[11]=str1
                
            
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.Point_1.x,length))+length
                    elif x==1:
                        list2[x]=str(ValueUnitslength(self.obj.Point_1.y,length))+length
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.Point_1.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(self.obj.Point_2.x,length))+length
                    elif x==4:
                        list2[x]=str(ValueUnitslength(self.obj.Point_2.y,length))+length
                    elif x==5:
                        list2[x]=str(ValueUnitslength(self.obj.Point_2.z,length))+length
                    elif x==6:
                        list2[x]=str(ValueUnitslength(self.obj.Point_3.x,length))+length
                    elif x==7:
                        list2[x]=str(ValueUnitslength(self.obj.Point_3.y,length))+length
                    elif x==8:
                        list2[x]=str(ValueUnitslength(self.obj.Point_3.z,length))+length
                    elif x==9:
                        list2[x]=str(ValueUnitslength(self.obj.Point_4.x,length))+length
                    elif x==10:
                        list2[x]=str(ValueUnitslength(self.obj.Point_4.y,length))+length
                    elif x==11:
                        list2[x]=str(ValueUnitslength(self.obj.Point_4.z,length))+length
                    

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
            self.ui.lineEdit_7.setText(list2[6])
            self.ui.lineEdit_8.setText(list2[7])
            self.ui.lineEdit_9.setText(list2[8])
            self.ui.lineEdit_10.setText(list2[9])
            self.ui.lineEdit_11.setText(list2[10])
            self.ui.lineEdit_12.setText(list2[11])
           
            

        else:
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','','','','','','','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'Point_1.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'Point_1.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'Point_1.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'Point_2.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
                elif list1[i][0] == 'Point_2.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[4]=str1
                elif list1[i][0] == 'Point_2.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[5]=str1
                elif list1[i][0] == 'Point_3.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[6]=str1
                elif list1[i][0] == 'Point_3.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[7]=str1
                elif list1[i][0] == 'Point_3.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[8]=str1
                elif list1[i][0] == 'Point_4.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[9]=str1
                elif list1[i][0] == 'Point_4.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[10]=str1
                elif list1[i][0] == 'Point_4.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[11]=str1
                
                
                
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.Point_1.x,length))+length
                    elif x==1:
                        # list2[x]=str(self.obj.Point_1.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_1.y,angle))+angle
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.Point_1.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(self.obj.Point_2.x,length))+length
                    elif x==4:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_2.y,angle))+angle
                    elif x==5:
                        list2[x]=str(ValueUnitslength(self.obj.Point_2.z,length))+length
                    elif x==6:
                        list2[x]=str(ValueUnitslength(self.obj.Point_3.x,length))+length
                    elif x==7:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_3.y,angle))+angle
                    elif x==8:
                        list2[x]=str(ValueUnitslength(self.obj.Point_3.z,length))+length
                    elif x==9:
                        list2[x]=str(ValueUnitslength(self.obj.Point_4.x,length))+length
                    elif x==10:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_4.y,angle))+angle
                    elif x==11:
                        list2[x]=str(ValueUnitslength(self.obj.Point_4.z,length))+length
                    
                    

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
            self.ui.lineEdit_7.setText(list2[6])
            self.ui.lineEdit_8.setText(list2[7])
            self.ui.lineEdit_9.setText(list2[8])
            self.ui.lineEdit_10.setText(list2[9])
            self.ui.lineEdit_11.setText(list2[10])
            self.ui.lineEdit_12.setText(list2[11])
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6)
            InputTools.textChangedbefore(self.ui.lineEdit_7,self.ui.lineEdit_8,self.ui.lineEdit_9)
            InputTools.textChangedbefore(self.ui.lineEdit_10,self.ui.lineEdit_11,self.ui.lineEdit_12)
            
            