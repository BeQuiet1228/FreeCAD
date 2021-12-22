#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
# import ConformalDialog
import ConformalDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD
import ProjectSetting
import re


class showConformalDialog(showObjDialog):
    def __init__(self, obj, parent=None):
        #手动调用父类构造函数。
        showObjDialog.__init__(self,obj,parent)
        #设置ui文件
        self.ui = ConformalDialog.Ui_Dialog()
        self.ui.setupUi(self)
        #初始化对话框
        self.initDialog()

        self.ui.lineEdit.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_2.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_3.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_4.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_5.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_6.setcompleterlist(getGlobalVar())

        self.obj = obj
        self.error = ''

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.move(screen.right()-self.size().width()-150, screen.bottom()*0.5-200)
        self.DisplayMode()
        FreeCAD.Console.PrintError("这是正投影体\n")

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
                str_theta1 = '360'+angle
            else :
                str_theta = '0'+angle
                str_theta1 = '2*pi'+angle
            self.ui.lineEdit.setText(str_z1)
            self.ui.lineEdit_2.setText(str_theta)
            self.ui.lineEdit_3.setText(str_3)
            self.ui.lineEdit_4.setText(str_z2)
            self.ui.lineEdit_5.setText(str_theta1)
            self.ui.lineEdit_6.setText(str_3)
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
                    self.obj.setExpression('Point1.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point1.x',None)
                    self.obj.Point1.x = point_1_x_after[0]
            except:
                self.error=self.error+'Point1.x'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.Stringfunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point1.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point1.y',None)
                    self.obj.Point1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point1.y'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point1.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point1.z',None)
                    self.obj.Point1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point1.z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point2.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('Point2.x',None)
                    self.obj.Point2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point2.x'+'  '+str(point_2_x_before)+'\n'

            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.Stringfunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point2.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('Point2.y',None)
                    self.obj.Point2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point2.y'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point2.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('Point2.z',None)
                    self.obj.Point2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point2.z'+'  '+str(point_2_z_before)+'\n'
                
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point1.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point1.x',None)
                    self.obj.Point1.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point1.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point1.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point1.y',None)
                    self.obj.Point1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point1.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point1.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point1.z',None)
                    self.obj.Point1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point1.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point2.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('Point2.x',None)
                    self.obj.Point2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point2.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point2.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('Point2.y',None)
                    self.obj.Point2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point2.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point2.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('Point2.z',None)
                    self.obj.Point2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point2.Z'+'  '+str(point_2_z_before)+'\n'
        else:
            point_1_x_before=self.ui.lineEdit_2.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point1.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point1.x',None)
                    self.obj.Point1.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point1.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_3.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point1.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point1.y',None)
                    self.obj.Point1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point1.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point1.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point1.z',None)
                    self.obj.Point1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point1.Z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_5.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point2.x',point_2_x_after[0])
                else:
                    self.obj.setExpression('Point2.x',None)
                    self.obj.Point2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point2.R'+'  '+str(point_2_x_before)+'\n'
            
            point_2_y_before=self.ui.lineEdit_6.text()
            point_2_y_after=InputTools.anglefunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point2.y',point_2_y_after[0])
                else:
                    self.obj.setExpression('Point2.y',None)
                    self.obj.Point2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point2.theta'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_4.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point2.z',point_2_z_after[0])
                else:
                    self.obj.setExpression('Point2.z',None)
                    self.obj.Point2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point2.Z'+'  '+str(point_2_z_before)+'\n'

    def closeDialog(self):
        """
        为了判断体是否被成功创建，在这里重写父类的方法
        :return:
        """
        # 获取正投影体的坐标，判断坐标是否能有效绘制当前模型
        p1_x = self.obj.Point1.x
        p1_y = self.obj.Point1.y
        p1_z = self.obj.Point1.z

        p2_x = self.obj.Point2.x
        p2_y = self.obj.Point2.y
        p2_z = self.obj.Point2.z

        difference_value = min(abs(p1_x - p2_x), abs(p1_y - p2_y), abs(p1_z - p2_z))    # 差值
        
        # 以0.01微米为衡量标准
        if difference_value < 0.00000001:
            reply = QtGui.QMessageBox.information(None, "", "无法有效绘制正投影体，请检查坐标。")
            return

        # 此种判断方法并不会有效
        # if self.obj.Shape.isNull():
        #     reply = QtGui.QMessageBox.information(None, "", "无法有效绘制正投影体，请检查坐标。")
        #     return
        #
        # if not self.obj.Shape.isValid():
        #     reply = QtGui.QMessageBox.information(None, "", "无法有效绘制正投影体，请检查坐标。")
        #     return

        t1 = time.time()
        try:
            self.fin_Order = int(self.ui.Base_lineEdit_2.value())
        except:
            pass
        if len(self.error) == 0:
            self.hide()
            t2 = time.time()
            self.recompute_flag = self.WhethertoRecompute()
            # is_show 用来判断是否是建立体，而不是从树结构打开对话框，新建立体都需要重新计算
            if hasattr(self,'function_expression_before'):
                try:
                    if self.function_expression_before != self.ui.lineEdit_7.toPlainText():
                        self.recompute_flag = True
                        FreeCAD.Console.PrintError('\n函数表达式进行了修改，所以进行计算')
                except:
                    pass
            is_show = 1

            if "reshow" not in self.__class__.__name__:
                is_show = 0
            if self.recompute_flag or is_show == 0:
                FreeCAD.ActiveDocument.recompute()
                FreeCAD.Console.PrintError('\n此时重新计算了一次模型')
            else:
                FreeCAD.Console.PrintError('\n没有重新计算模型')

            t3 = time.time()

            if hasattr(self.obj, 'Attribute'):
                self.controlboolupdate(is_show)
            else:
                FreeCAD.Console.PrintError('\n由于没有attribute的原因跳过布尔运算')

            self.obj_resultshape.ViewObject.Transparency = 0
            self.obj.ViewObject.Visibility = False
            self.obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
            Common.Tools.ObjectsTools.setFitViewOfObject(self.obj)
            self.obj_resultshape.ViewObject.Transparency = 85
            self.obj.ViewObject.Visibility = True
            t4 = time.time()
            self.close()
            t5 = time.time()
            # @fubiao
            import ObjectsTools as objTools
            objTools.checkVolShape(self.obj)
            self.obj.recompute()

class reshowConformalDialog(showConformalDialog):
    def deleteobj(self):
        pass

    def setDefaultValue(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            list1=self.obj.ExpressionEngine
            list2=['','','','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'Point1.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'Point1.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'Point1.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'Point2.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
                elif list1[i][0] == 'Point2.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[4]=str1
                elif list1[i][0] == 'Point2.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[5]=str1
            
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.Point1.x,length))+length
                    elif x==1:
                        list2[x]=str(ValueUnitslength(self.obj.Point1.y,length))+length
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.Point1.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(self.obj.Point2.x,length))+length
                    elif x==4:
                        list2[x]=str(ValueUnitslength(self.obj.Point2.y,length))+length
                    elif x==5:
                        list2[x]=str(ValueUnitslength(self.obj.Point2.z,length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
        else:
            list1=self.obj.ExpressionEngine
            list2=['','','','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'Point1.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'Point1.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'Point1.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                elif list1[i][0] == 'Point2.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[3]=str1
                elif list1[i][0] == 'Point2.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[4]=str1
                elif list1[i][0] == 'Point2.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[5]=str1
                
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.Point1.x,length))+length
                    elif x==1:
                        # list2[x]=str(self.obj.Point_1.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point1.y,angle))+angle
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.Point1.z,length))+length
                    elif x==3:
                        list2[x]=str(ValueUnitslength(self.obj.Point2.x,length))+length
                    elif x==4:
                        # list2[x]=str(self.obj.Point_2.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point2.y,angle))+angle
                    elif x==5:
                        list2[x]=str(ValueUnitslength(self.obj.Point2.z,length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            InputTools.textChangedbefore(self.ui.lineEdit_4,self.ui.lineEdit_5,self.ui.lineEdit_6) 