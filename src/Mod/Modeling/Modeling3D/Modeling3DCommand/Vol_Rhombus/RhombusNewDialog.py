#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
import RhombusDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD
import ProjectSetting
import re

class showRhombusDialog(showObjDialog):
    def __init__(self, obj, parent=None):
        #手动调用父类构造函数。
        showObjDialog.__init__(self,obj,parent)
        #设置ui文件
        self.ui = RhombusDialog.Ui_Dialog()
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
        self.ui.lineEdit_13.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_14.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_15.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_16.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_17.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_18.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_19.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_20.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_21.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_22.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_23.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_24.setcompleterlist(getGlobalVar())

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
            self.ui.lineEdit_13.setText(str_2)
            self.ui.lineEdit_14.setText(str_3)
            self.ui.lineEdit_15.setText(str_3)
            self.ui.lineEdit_16.setText(str_2)
            self.ui.lineEdit_17.setText(str_3)
            self.ui.lineEdit_18.setText(str_3)
            self.ui.lineEdit_19.setText(str_2)
            self.ui.lineEdit_20.setText(str_3)
            self.ui.lineEdit_21.setText(str_3)
            self.ui.lineEdit_22.setText(str_2)
            self.ui.lineEdit_23.setText(str_3)
            self.ui.lineEdit_24.setText(str_3)
        
            
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
            self.ui.lineEdit_13.setText(str_z2)
            self.ui.lineEdit_14.setText(str_theta)
            self.ui.lineEdit_15.setText(str_3)
            self.ui.lineEdit_16.setText(str_z2)
            self.ui.lineEdit_17.setText(str_theta)
            self.ui.lineEdit_18.setText(str_3)
            self.ui.lineEdit_19.setText(str_z2)
            self.ui.lineEdit_20.setText(str_theta)
            self.ui.lineEdit_21.setText(str_3)
            self.ui.lineEdit_22.setText(str_z2)
            self.ui.lineEdit_23.setText(str_theta)
            self.ui.lineEdit_24.setText(str_3)
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6)
            InputTools.textChangedbefore(self.ui.lineEdit_7,self.ui.lineEdit_8,self.ui.lineEdit_9)
            InputTools.textChangedbefore(self.ui.lineEdit_10,self.ui.lineEdit_11,self.ui.lineEdit_12)
            InputTools.textChangedbefore(self.ui.lineEdit_13,self.ui.lineEdit_14,self.ui.lineEdit_15)
            InputTools.textChangedbefore(self.ui.lineEdit_16,self.ui.lineEdit_17,self.ui.lineEdit_18)
            InputTools.textChangedbefore(self.ui.lineEdit_19,self.ui.lineEdit_20,self.ui.lineEdit_21)
            InputTools.textChangedbefore(self.ui.lineEdit_22,self.ui.lineEdit_23,self.ui.lineEdit_24)
            
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


            point_5_x_before=self.ui.lineEdit_13.text()
            point_5_x_after=InputTools.Stringfunctions(point_5_x_before)
            try:
                if point_5_x_after[1]==2:
                    self.obj.setExpression('Point_5.x',point_5_x_after[0])
                else:
                    self.obj.setExpression('Point_5.x',None)
                    self.obj.Point_5.x=point_5_x_after[0]
            except:
                self.error=self.error+'Point_5.x'+'  '+str(point_5_x_before)+'\n'

            point_5_y_before=self.ui.lineEdit_14.text()
            point_5_y_after=InputTools.Stringfunctions(point_5_y_before)
            try:
                if point_5_y_after[1]==2:
                    self.obj.setExpression('Point_5.y',point_5_y_after[0])
                else:
                    self.obj.setExpression('Point_5.y',None)
                    self.obj.Point_5.y=point_5_y_after[0]
            except:
                self.error=self.error+'Point_5.y'+'  '+str(point_5_y_before)+'\n'

            Point_5_z_before=self.ui.lineEdit_15.text()
            Point_5_z_after=InputTools.Stringfunctions(Point_5_z_before)
            try:
                if Point_5_z_after[1]==2:
                    self.obj.setExpression('Point_5.z',Point_5_z_after[0])
                else:
                    self.obj.setExpression('Point_5.z',None)
                    self.obj.Point_5.z=Point_5_z_after[0]
            except:
                self.error=self.error+'Point_5.z'+'  '+str(Point_5_z_before)+'\n'

            Point_6_x_before=self.ui.lineEdit_16.text()
            Point_6_x_after=InputTools.Stringfunctions(Point_6_x_before)
            try:
                if Point_6_x_after[1]==2:
                    self.obj.setExpression('Point_6.x',Point_6_x_after[0])
                else:
                    self.obj.setExpression('Point_6.x',None)
                    self.obj.Point_6.x=Point_6_x_after[0]
            except:
                self.error=self.error+'Point_6.x'+'  '+str(Point_6_x_before)+'\n'

            Point_6_y_before=self.ui.lineEdit_17.text()
            Point_6_y_after=InputTools.Stringfunctions(Point_6_y_before)
            try:
                if Point_6_y_after[1]==2:
                    self.obj.setExpression('Point_6.y',Point_6_y_after[0])
                else:
                    self.obj.setExpression('Point_6.y',None)
                    self.obj.Point_6.y=Point_6_y_after[0]
            except:
                self.error=self.error+'Point_6.y'+'  '+str(Point_6_y_before)+'\n'

            Point_6_z_before=self.ui.lineEdit_18.text()
            Point_6_z_after=InputTools.Stringfunctions(Point_6_z_before)
            try:
                if Point_6_z_after[1]==2:
                    self.obj.setExpression('Point_6.z',Point_6_z_after[0])
                else:
                    self.obj.setExpression('Point_6.z',None)
                    self.obj.Point_6.z=Point_6_z_after[0]
            except:
                self.error=self.error+'Point_6.z'+'  '+str(Point_6_z_before)+'\n'

            point_7_x_before=self.ui.lineEdit_19.text()
            point_7_x_after=InputTools.Stringfunctions(point_7_x_before)
            try:
                if point_7_x_after[1]==2:
                    self.obj.setExpression('Point_7.x',point_7_x_after[0])
                else:
                    self.obj.setExpression('Point_7.x',None)
                    self.obj.Point_7.x=point_7_x_after[0]
            except:
                self.error=self.error+'Point_7.x'+'  '+str(point_7_x_before)+'\n'

            point_7_y_before=self.ui.lineEdit_20.text()
            point_7_y_after=InputTools.Stringfunctions(point_7_y_before)
            try:
                if point_7_y_after[1]==2:
                    self.obj.setExpression('Point_7.y',point_7_y_after[0])
                else:
                    self.obj.setExpression('Point_7.y',None)
                    self.obj.Point_7.y=point_7_y_after[0]
            except:
                self.error=self.error+'Point_7.y'+'  '+str(point_7_y_before)+'\n'

            point_7_z_before=self.ui.lineEdit_21.text()
            point_7_z_after=InputTools.Stringfunctions(point_7_z_before)
            try:
                if point_7_z_after[1]==2:
                    self.obj.setExpression('Point_7.z',point_7_z_after[0])
                else:
                    self.obj.setExpression('Point_7.z',None)
                    self.obj.Point_7.z=point_7_z_after[0]
            except:
                self.error=self.error+'Point_7.z'+'  '+str(point_7_z_before)+'\n'


            point_8_x_before=self.ui.lineEdit_22.text()
            point_8_x_after=InputTools.Stringfunctions(point_8_x_before)
            try:
                if point_8_x_after[1]==2:
                    self.obj.setExpression('Point_8.x',point_8_x_after[0])
                else:
                    self.obj.setExpression('Point_8.x',None)
                    self.obj.Point_8.x=point_8_x_after[0]
            except:
                self.error=self.error+'Point_8.x'+'  '+str(point_8_x_before)+'\n'

            point_8_y_before=self.ui.lineEdit_23.text()
            point_8_y_after=InputTools.Stringfunctions(point_8_y_before)
            try:
                if point_8_y_after[1]==2:
                    self.obj.setExpression('Point_8.y',point_8_y_after[0])
                else:
                    self.obj.setExpression('Point_8.y',None)
                    self.obj.Point_8.y=point_8_y_after[0]
            except:
                self.error=self.error+'Point_8.y'+'  '+str(point_8_y_before)+'\n'

            point_8_z_before=self.ui.lineEdit_24.text()
            point_8_z_after=InputTools.Stringfunctions(point_8_z_before)
            try:
                if point_8_z_after[1]==2:
                    self.obj.setExpression('Point_8.z',point_8_z_after[0])
                else:
                    self.obj.setExpression('Point_8.z',None)
                    self.obj.Point_8.z=point_8_z_after[0]
            except:
                self.error=self.error+'Point_8.z'+'  '+str(point_8_z_before)+'\n'
                
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point_1.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point_1.x',None)
                    self.obj.Point_1.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point_1.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point_1.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point_1.y',None)
                    self.obj.Point_1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point_1.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point_1.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point_1.z',None)
                    self.obj.Point_1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point_1.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point_2.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('Point_2.x',None)
                    self.obj.Point_2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point_2.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point_2.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('Point_2.y',None)
                    self.obj.Point_2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point_2.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point_2.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('Point_2.z',None)
                    self.obj.Point_2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point_2.Z'+'  '+str(point_2_z_before)+'\n'

            point_3_x_before=self.ui.lineEdit_7.text()
            point_3_x_after=InputTools.Stringfunctions(point_3_x_before)
            try:
                if point_3_x_after[1]==2:
                    self.obj.setExpression('Point_3.x',point_3_x_after[0])
                else:
                    self.obj.setExpression('Point_3.x',None)
                    self.obj.Point_3.x=point_3_x_after[0]
            except:
                self.error=self.error+'Point_3.R'+'  '+str(point_3_x_before)+'\n'
            
            point_3_y_before=self.ui.lineEdit_8.text()
            point_3_y_after=InputTools.anglefunctions(point_3_y_before)
            try:
                if point_3_y_after[1]==2:
                    self.obj.setExpression('Point_3.y',point_3_y_after[0])
                else:
                    self.obj.setExpression('Point_3.y',None)
                    self.obj.Point_3.y=point_3_y_after[0]
            except:
                self.error=self.error+'Point_3.theta'+'  '+str(point_3_y_before)+'\n'

            point_3_z_before=self.ui.lineEdit_9.text()
            point_3_z_after=InputTools.Stringfunctions(point_3_z_before)
            try:
                if point_3_z_after[1]==2:
                    self.obj.setExpression('Point_3.z',point_3_z_after[0])
                else:
                    self.obj.setExpression('Point_3.z',None)
                    self.obj.Point_3.z=point_3_z_after[0]
            except:
                self.error=self.error+'Point_3.Z'+'  '+str(point_3_z_before)+'\n'


            point_4_x_before=self.ui.lineEdit_10.text()
            point_4_x_after=InputTools.Stringfunctions(point_4_x_before)
            try:
                if point_4_x_after[1]==2:
                    self.obj.setExpression('Point_4.x',point_4_x_after[0])
                else:
                    self.obj.setExpression('Point_4.x',None)
                    self.obj.Point_4.x=point_4_x_after[0]
            except:
                self.error=self.error+'Point_4.R'+'  '+str(point_4_x_before)+'\n'
            
            point_4_y_before=self.ui.lineEdit_11.text()
            point_4_y_after=InputTools.anglefunctions(point_4_y_before)
            try:
                if point_4_y_after[1]==2:
                    self.obj.setExpression('Point_4.y',point_4_y_after[0])
                else:
                    self.obj.setExpression('Point_4.y',None)
                    self.obj.Point_4.y=point_4_y_after[0]
            except:
                self.error=self.error+'Point_4.theta'+'  '+str(point_4_y_before)+'\n'

            point_4_z_before=self.ui.lineEdit_12.text()
            point_4_z_after=InputTools.Stringfunctions(point_4_z_before)
            try:
                if point_4_z_after[1]==2:
                    self.obj.setExpression('Point_4.z',point_4_z_after[0])
                else:
                    self.obj.setExpression('Point_4.z',None)
                    self.obj.Point_4.z=point_4_z_after[0]
            except:
                self.error=self.error+'Point_4.Z'+'  '+str(point_4_z_before)+'\n'

            point_5_x_before=self.ui.lineEdit_13.text()
            point_5_x_after=InputTools.Stringfunctions(point_5_x_before)
            try:
                if point_5_x_after[1]==2:
                    self.obj.setExpression('Point_5.x',point_5_x_after[0])
                else:
                    self.obj.setExpression('Point_5.x',None)
                    self.obj.Point_5.x=point_5_x_after[0]
            except:
                self.error=self.error+'Point_5.R'+'  '+str(point_5_x_before)+'\n'
            
            point_5_y_before=self.ui.lineEdit_14.text()
            point_5_y_after=InputTools.anglefunctions(point_5_y_before)
            try:
                if point_5_y_after[1]==2:
                    self.obj.setExpression('Point_5.y',point_5_y_after[0])
                else:
                    self.obj.setExpression('Point_5.y',None)
                    self.obj.Point_5.y=point_5_y_after[0]
            except:
                self.error=self.error+'Point_5.theta'+'  '+str(point_5_y_before)+'\n'

            point_5_z_before=self.ui.lineEdit_15.text()
            point_5_z_after=InputTools.Stringfunctions(point_5_z_before)
            try:
                if point_5_z_after[1]==2:
                    self.obj.setExpression('Point_5.z',point_5_z_after[0])
                else:
                    self.obj.setExpression('Point_5.z',None)
                    self.obj.Point_5.z=point_5_z_after[0]
            except:
                self.error=self.error+'Point_5.Z'+'  '+str(point_5_z_before)+'\n'

            point_6_x_before=self.ui.lineEdit_16.text()
            point_6_x_after=InputTools.Stringfunctions(point_6_x_before)
            try:
                if point_6_x_after[1]==2:
                    self.obj.setExpression('Point_6.x',point_6_x_after[0])
                else:
                    self.obj.setExpression('Point_6.x',None)
                    self.obj.Point_6.x=point_6_x_after[0]
            except:
                self.error=self.error+'Point_6.R'+'  '+str(point_6_x_before)+'\n'
            
            point_6_y_before=self.ui.lineEdit_17.text()
            point_6_y_after=InputTools.anglefunctions(point_6_y_before)
            try:
                if point_6_y_after[1]==2:
                    self.obj.setExpression('Point_6.y',point_6_y_after[0])
                else:
                    self.obj.setExpression('Point_6.y',None)
                    self.obj.Point_6.y=point_6_y_after[0]
            except:
                self.error=self.error+'Point_6.theta'+'  '+str(point_6_y_before)+'\n'

            point_6_z_before=self.ui.lineEdit_18.text()
            point_6_z_after=InputTools.Stringfunctions(point_6_z_before)
            try:
                if point_6_z_after[1]==2:
                    self.obj.setExpression('Point_6.z',point_6_z_after[0])
                else:
                    self.obj.setExpression('Point_6.z',None)
                    self.obj.Point_6.z=point_6_z_after[0]
            except:
                self.error=self.error+'Point_6.Z'+'  '+str(point_6_z_before)+'\n'

            point_7_x_before=self.ui.lineEdit_19.text()
            point_7_x_after=InputTools.Stringfunctions(point_7_x_before)
            try:
                if point_7_x_after[1]==2:
                    self.obj.setExpression('Point_7.x',point_7_x_after[0])
                else:
                    self.obj.setExpression('Point_7.x',None)
                    self.obj.Point_7.x=point_7_x_after[0]
            except:
                self.error=self.error+'Point_7.R'+'  '+str(point_7_x_before)+'\n'
            
            point_7_y_before=self.ui.lineEdit_20.text()
            point_7_y_after=InputTools.anglefunctions(point_7_y_before)
            try:
                if point_7_y_after[1]==2:
                    self.obj.setExpression('Point_7.y',point_7_y_after[0])
                else:
                    self.obj.setExpression('Point_7.y',None)
                    self.obj.Point_7.y=point_7_y_after[0]
            except:
                self.error=self.error+'Point_7.theta'+'  '+str(point_7_y_before)+'\n'

            point_7_z_before=self.ui.lineEdit_21.text()
            point_7_z_after=InputTools.Stringfunctions(point_7_z_before)
            try:
                if point_7_z_after[1]==2:
                    self.obj.setExpression('Point_7.z',point_7_z_after[0])
                else:
                    self.obj.setExpression('Point_7.z',None)
                    self.obj.Point_7.z=point_7_z_after[0]
            except:
                self.error=self.error+'Point_7.Z'+'  '+str(point_7_z_before)+'\n'

            point_8_x_before=self.ui.lineEdit_22.text()
            point_8_x_after=InputTools.Stringfunctions(point_8_x_before)
            try:
                if point_8_x_after[1]==2:
                    self.obj.setExpression('Point_8.x',point_8_x_after[0])
                else:
                    self.obj.setExpression('Point_8.x',None)
                    self.obj.Point_8.x=point_8_x_after[0]
            except:
                self.error=self.error+'Point_8.R'+'  '+str(point_8_x_before)+'\n'
            
            point_8_y_before=self.ui.lineEdit_23.text()
            point_8_y_after=InputTools.anglefunctions(point_8_y_before)
            try:
                if point_8_y_after[1]==2:
                    self.obj.setExpression('Point_8.y',point_8_y_after[0])
                else:
                    self.obj.setExpression('Point_8.y',None)
                    self.obj.Point_8.y=point_8_y_after[0]
            except:
                self.error=self.error+'Point_8.theta'+'  '+str(point_8_y_before)+'\n'

            point_8_z_before=self.ui.lineEdit_24.text()
            point_8_z_after=InputTools.Stringfunctions(point_8_z_before)
            try:
                if point_8_z_after[1]==2:
                    self.obj.setExpression('Point_8.z',point_8_z_after[0])
                else:
                    self.obj.setExpression('Point_8.z',None)
                    self.obj.Point_8.z=point_8_z_after[0]
            except:
                self.error=self.error+'Point_8.Z'+'  '+str(point_8_z_before)+'\n'
        else:
            point_1_x_before=self.ui.lineEdit_2.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point_1.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point_1.x',None)
                    self.obj.Point_1.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point_1.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_3.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point_1.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point_1.y',None)
                    self.obj.Point_1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point_1.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point_1.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point_1.z',None)
                    self.obj.Point_1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point_1.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_5.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point_2.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('Point_2.x',None)
                    self.obj.Point_2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point_2.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_6.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point_2.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('Point_2.y',None)
                    self.obj.Point_2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point_2.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_4.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point_2.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('Point_2.z',None)
                    self.obj.Point_2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point_2.Z'+'  '+str(point_2_z_before)+'\n'

            point_3_x_before=self.ui.lineEdit_8.text()
            point_3_x_after=InputTools.Stringfunctions(point_3_x_before)
            try:
                if point_3_x_after[1]==2:
                    self.obj.setExpression('Point_3.x',point_3_x_after[0])
                else:
                    self.obj.setExpression('Point_3.x',None)
                    self.obj.Point_3.x=point_3_x_after[0]
            except:
                self.error=self.error+'Point_3.R'+'  '+str(point_3_x_before)+'\n'
            
            point_3_y_before=self.ui.lineEdit_9.text()
            point_3_y_after=InputTools.anglefunctions(point_3_y_before)
            try:
                if point_3_y_after[1]==2:
                    self.obj.setExpression('Point_3.y',point_3_y_after[0])
                else:
                    self.obj.setExpression('Point_3.y',None)
                    self.obj.Point_3.y=point_3_y_after[0]
            except:
                self.error=self.error+'Point_3.theta'+'  '+str(point_3_y_before)+'\n'

            point_3_z_before=self.ui.lineEdit_7.text()
            point_3_z_after=InputTools.Stringfunctions(point_3_z_before)
            try:
                if point_3_z_after[1]==2:
                    self.obj.setExpression('Point_3.z',point_3_z_after[0])
                else:
                    self.obj.setExpression('Point_3.z',None)
                    self.obj.Point_3.z=point_3_z_after[0]
            except:
                self.error=self.error+'Point_3.Z'+'  '+str(point_3_z_before)+'\n'


            point_4_x_before=self.ui.lineEdit_11.text()
            point_4_x_after=InputTools.Stringfunctions(point_4_x_before)
            try:
                if point_4_x_after[1]==2:
                    self.obj.setExpression('Point_4.x',point_4_x_after[0])
                else:
                    self.obj.setExpression('Point_4.x',None)
                    self.obj.Point_4.x=point_4_x_after[0]
            except:
                self.error=self.error+'Point_4.R'+'  '+str(point_4_x_before)+'\n'
            
            point_4_y_before=self.ui.lineEdit_12.text()
            point_4_y_after=InputTools.anglefunctions(point_4_y_before)
            try:
                if point_4_y_after[1]==2:
                    self.obj.setExpression('Point_4.y',point_4_y_after[0])
                else:
                    self.obj.setExpression('Point_4.y',None)
                    self.obj.Point_4.y=point_4_y_after[0]
            except:
                self.error=self.error+'Point_4.theta'+'  '+str(point_4_y_before)+'\n'

            point_4_z_before=self.ui.lineEdit_10.text()
            point_4_z_after=InputTools.Stringfunctions(point_4_z_before)
            try:
                if point_4_z_after[1]==2:
                    self.obj.setExpression('Point_4.z',point_4_z_after[0])
                else:
                    self.obj.setExpression('Point_4.z',None)
                    self.obj.Point_4.z=point_4_z_after[0]
            except:
                self.error=self.error+'Point_4.Z'+'  '+str(point_4_z_before)+'\n'

            point_5_x_before=self.ui.lineEdit_14.text()
            point_5_x_after=InputTools.Stringfunctions(point_5_x_before)
            try:
                if point_5_x_after[1]==2:
                    self.obj.setExpression('Point_5.x',point_5_x_after[0])
                else:
                    self.obj.setExpression('Point_5.x',None)
                    self.obj.Point_5.x=point_5_x_after[0]
            except:
                self.error=self.error+'Point_5.R'+'  '+str(point_5_x_before)+'\n'
            
            point_5_y_before=self.ui.lineEdit_15.text()
            point_5_y_after=InputTools.anglefunctions(point_5_y_before)
            try:
                if point_5_y_after[1]==2:
                    self.obj.setExpression('Point_5.y',point_5_y_after[0])
                else:
                    self.obj.setExpression('Point_5.y',None)
                    self.obj.Point_5.y=point_5_y_after[0]
            except:
                self.error=self.error+'Point_5.theta'+'  '+str(point_5_y_before)+'\n'

            point_5_z_before=self.ui.lineEdit_13.text()
            point_5_z_after=InputTools.Stringfunctions(point_5_z_before)
            try:
                if point_5_z_after[1]==2:
                    self.obj.setExpression('Point_5.z',point_5_z_after[0])
                else:
                    self.obj.setExpression('Point_5.z',None)
                    self.obj.Point_5.z=point_5_z_after[0]
            except:
                self.error=self.error+'Point_5.Z'+'  '+str(point_5_z_before)+'\n'

            point_6_x_before=self.ui.lineEdit_17.text()
            point_6_x_after=InputTools.Stringfunctions(point_6_x_before)
            try:
                if point_6_x_after[1]==2:
                    self.obj.setExpression('Point_6.x',point_6_x_after[0])
                else:
                    self.obj.setExpression('Point_6.x',None)
                    self.obj.Point_6.x=point_6_x_after[0]
            except:
                self.error=self.error+'Point_6.R'+'  '+str(point_6_x_before)+'\n'
            
            point_6_y_before=self.ui.lineEdit_18.text()
            point_6_y_after=InputTools.anglefunctions(point_6_y_before)
            try:
                if point_6_y_after[1]==2:
                    self.obj.setExpression('Point_6.y',point_6_y_after[0])
                else:
                    self.obj.setExpression('Point_6.y',None)
                    self.obj.Point_6.y=point_6_y_after[0]
            except:
                self.error=self.error+'Point_6.theta'+'  '+str(point_6_y_before)+'\n'

            point_6_z_before=self.ui.lineEdit_16.text()
            point_6_z_after=InputTools.Stringfunctions(point_6_z_before)
            try:
                if point_6_z_after[1]==2:
                    self.obj.setExpression('Point_6.z',point_6_z_after[0])
                else:
                    self.obj.setExpression('Point_6.z',None)
                    self.obj.Point_6.z=point_6_z_after[0]
            except:
                self.error=self.error+'Point_6.Z'+'  '+str(point_6_z_before)+'\n'

            point_7_x_before=self.ui.lineEdit_20.text()
            point_7_x_after=InputTools.Stringfunctions(point_7_x_before)
            try:
                if point_7_x_after[1]==2:
                    self.obj.setExpression('Point_7.x',point_7_x_after[0])
                else:
                    self.obj.setExpression('Point_7.x',None)
                    self.obj.Point_7.x=point_7_x_after[0]
            except:
                self.error=self.error+'Point_7.R'+'  '+str(point_7_x_before)+'\n'
            
            point_7_y_before=self.ui.lineEdit_21.text()
            point_7_y_after=InputTools.anglefunctions(point_7_y_before)
            try:
                if point_7_y_after[1]==2:
                    self.obj.setExpression('Point_7.y',point_7_y_after[0])
                else:
                    self.obj.setExpression('Point_7.y',None)
                    self.obj.Point_7.y=point_7_y_after[0]
            except:
                self.error=self.error+'Point_7.theta'+'  '+str(point_7_y_before)+'\n'

            point_7_z_before=self.ui.lineEdit_19.text()
            point_7_z_after=InputTools.Stringfunctions(point_7_z_before)
            try:
                if point_7_z_after[1]==2:
                    self.obj.setExpression('Point_7.z',point_7_z_after[0])
                else:
                    self.obj.setExpression('Point_7.z',None)
                    self.obj.Point_7.z=point_7_z_after[0]
            except:
                self.error=self.error+'Point_7.Z'+'  '+str(point_7_z_before)+'\n'

            point_8_x_before=self.ui.lineEdit_23.text()
            point_8_x_after=InputTools.Stringfunctions(point_8_x_before)
            try:
                if point_8_x_after[1]==2:
                    self.obj.setExpression('Point_8.x',point_8_x_after[0])
                else:
                    self.obj.setExpression('Point_8.x',None)
                    self.obj.Point_8.x=point_8_x_after[0]
            except:
                self.error=self.error+'Point_8.R'+'  '+str(point_8_x_before)+'\n'
            
            point_8_y_before=self.ui.lineEdit_24.text()
            point_8_y_after=InputTools.anglefunctions(point_8_y_before)
            try:
                if point_8_y_after[1]==2:
                    self.obj.setExpression('Point_8.y',point_8_y_after[0])
                else:
                    self.obj.setExpression('Point_8.y',None)
                    self.obj.Point_8.y=point_8_y_after[0]
            except:
                self.error=self.error+'Point_8.theta'+'  '+str(point_8_y_before)+'\n'

            point_8_z_before=self.ui.lineEdit_22.text()
            point_8_z_after=InputTools.Stringfunctions(point_8_z_before)
            try:
                if point_8_z_after[1]==2:
                    self.obj.setExpression('Point_8.z',point_8_z_after[0])
                else:
                    self.obj.setExpression('Point_8.z',None)
                    self.obj.Point_8.z=point_8_z_after[0]
            except:
                self.error=self.error+'Point_8.Z'+'  '+str(point_8_z_before)+'\n'


            pass

class reshowRhombusDialog(showRhombusDialog):
    def deleteobj(self):
        pass

    def setDefaultValue(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','','','','','','','','','','','','','','','','','','']
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
                elif list1[i][0] == 'Point_5.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[12]=str1
                elif list1[i][0] == 'Point_5.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[13]=str1
                elif list1[i][0] == 'Point_5.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[14]=str1
                elif list1[i][0] == 'Point_6.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[15]=str1
                elif list1[i][0] == 'Point_6.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[16]=str1
                elif list1[i][0] == 'Point_6.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[17]=str1
                elif list1[i][0] == 'Point_7.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[18]=str1
                elif list1[i][0] == 'Point_7.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[19]=str1
                elif list1[i][0] == 'Point_7.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[20]=str1
                elif list1[i][0] == 'Point_8.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[21]=str1
                elif list1[i][0] == 'Point_8.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[22]=str1
                elif list1[i][0] == 'Point_8.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[23]=str1
            
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
                    elif x==12:
                        list2[x]=str(ValueUnitslength(self.obj.Point_5.x,length))+length
                    elif x==13:
                        list2[x]=str(ValueUnitslength(self.obj.Point_5.y,length))+length
                    elif x==14:
                        list2[x]=str(ValueUnitslength(self.obj.Point_5.z,length))+length
                    elif x==15:
                        list2[x]=str(ValueUnitslength(self.obj.Point_6.x,length))+length
                    elif x==16:
                        list2[x]=str(ValueUnitslength(self.obj.Point_6.y,length))+length
                    elif x==17:
                        list2[x]=str(ValueUnitslength(self.obj.Point_6.z,length))+length
                    elif x==18:
                        list2[x]=str(ValueUnitslength(self.obj.Point_7.x,length))+length
                    elif x==19:
                        list2[x]=str(ValueUnitslength(self.obj.Point_7.y,length))+length
                    elif x==20:
                        list2[x]=str(ValueUnitslength(self.obj.Point_7.z,length))+length
                    elif x==21:
                        list2[x]=str(ValueUnitslength(self.obj.Point_8.x,length))+length
                    elif x==22:
                        list2[x]=str(ValueUnitslength(self.obj.Point_8.y,length))+length
                    elif x==23:
                        list2[x]=str(ValueUnitslength(self.obj.Point_8.z,length))+length

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
            self.ui.lineEdit_13.setText(list2[12])
            self.ui.lineEdit_14.setText(list2[13])
            self.ui.lineEdit_15.setText(list2[14])
            self.ui.lineEdit_16.setText(list2[15])
            self.ui.lineEdit_17.setText(list2[16])
            self.ui.lineEdit_18.setText(list2[17])
            self.ui.lineEdit_19.setText(list2[18])
            self.ui.lineEdit_20.setText(list2[19])
            self.ui.lineEdit_21.setText(list2[20])
            self.ui.lineEdit_22.setText(list2[21])
            self.ui.lineEdit_23.setText(list2[22])
            self.ui.lineEdit_24.setText(list2[23])

        else:
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','','','','','','','','','','','','','','','','','','','','']
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
                elif list1[i][0] == 'Point_5.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[12]=str1
                elif list1[i][0] == 'Point_5.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[13]=str1
                elif list1[i][0] == 'Point_5.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[14]=str1
                elif list1[i][0] == 'Point_6.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[15]=str1
                elif list1[i][0] == 'Point_6.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[16]=str1
                elif list1[i][0] == 'Point_6.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[17]=str1
                elif list1[i][0] == 'Point_7.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[18]=str1
                elif list1[i][0] == 'Point_7.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[19]=str1
                elif list1[i][0] == 'Point_7.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[20]=str1
                elif list1[i][0] == 'Point_8.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[21]=str1
                elif list1[i][0] == 'Point_8.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[22]=str1
                elif list1[i][0] == 'Point_8.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[23]=str1
                
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
                    elif x==12:
                        list2[x]=str(ValueUnitslength(self.obj.Point_5.x,length))+length
                    elif x==13:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_5.y,angle))+angle
                    elif x==14:
                        list2[x]=str(ValueUnitslength(self.obj.Point_5.z,length))+length
                    elif x==15:
                        list2[x]=str(ValueUnitslength(self.obj.Point_6.x,length))+length
                    elif x==16:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_6.y,angle))+angle
                    elif x==17:
                        list2[x]=str(ValueUnitslength(self.obj.Point_6.z,length))+length
                    elif x==18:
                        list2[x]=str(ValueUnitslength(self.obj.Point_7.x,length))+length
                    elif x==19:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_7.y,angle))+angle
                    elif x==20:
                        list2[x]=str(ValueUnitslength(self.obj.Point_7.z,length))+length
                    elif x==21:
                        list2[x]=str(ValueUnitslength(self.obj.Point_8.x,length))+length
                    elif x==22:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point_8.y,angle))+angle
                    elif x==23:
                        list2[x]=str(ValueUnitslength(self.obj.Point_8.z,length))+length

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
            self.ui.lineEdit_13.setText(list2[12])
            self.ui.lineEdit_14.setText(list2[13])
            self.ui.lineEdit_15.setText(list2[14])
            self.ui.lineEdit_16.setText(list2[15])
            self.ui.lineEdit_17.setText(list2[16])
            self.ui.lineEdit_18.setText(list2[17])
            self.ui.lineEdit_19.setText(list2[18])
            self.ui.lineEdit_20.setText(list2[19])
            self.ui.lineEdit_21.setText(list2[20])
            self.ui.lineEdit_22.setText(list2[21])
            self.ui.lineEdit_23.setText(list2[22])
            self.ui.lineEdit_24.setText(list2[23])
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6)
            InputTools.textChangedbefore(self.ui.lineEdit_7,self.ui.lineEdit_8,self.ui.lineEdit_9)
            InputTools.textChangedbefore(self.ui.lineEdit_10,self.ui.lineEdit_11,self.ui.lineEdit_12)
            InputTools.textChangedbefore(self.ui.lineEdit_13,self.ui.lineEdit_14,self.ui.lineEdit_15)
            InputTools.textChangedbefore(self.ui.lineEdit_16,self.ui.lineEdit_17,self.ui.lineEdit_18)
            InputTools.textChangedbefore(self.ui.lineEdit_19,self.ui.lineEdit_20,self.ui.lineEdit_21)
            InputTools.textChangedbefore(self.ui.lineEdit_22,self.ui.lineEdit_23,self.ui.lineEdit_24)