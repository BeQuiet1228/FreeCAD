#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
import PointDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD
import ProjectSetting
import re

class showPointDialog(showObjDialog):
    def __init__(self, obj, parent=None):
        #手动调用父类构造函数。
        showObjDialog.__init__(self,obj,parent)
        #设置ui文件
        self.ui = PointDialog.Ui_Dialog()
        self.ui.setupUi(self)
        #初始化对话框
        self.initDialog()

        self.ui.lineEdit.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_2.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_3.setcompleterlist(getGlobalVar())

        self.obj = obj
        self.error = ''

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.move(screen.right()-self.size().width()-150, screen.bottom()*0.5-200)
        self.DisplayMode()

        self.setUI()
    def setUI(self):
        # 添加mark的补充部分
        self.setMarkUi()
        self.ui.OK_pushButton.clicked.connect(self.setExtraMark)
        # 获取所有的AutoLineEdit
        self.auto_lineedit = self.getAllAutoLineEdits()

        # 设置Frame隐藏
        # self.ui.frame.hide()
        # 根据坐标系设置面板信息
        self.setDialog()

        # 设置初始化的label
        self.setDefaultLabel()
        # 设置Label
        self.ui.OK_pushButton.clicked.connect(self.setLabel)

        # 设置Order
        self.setOrder()
        # 设置物体order，以及排序
        self.ui.OK_pushButton.clicked.connect(self.OrderChanged)


        # # 设置属性
        # self.setAttributeText()
        # # 设置初始化Custom界面
        # self.ui.comboBox.activated.connect(self.setAttribute)
        # self.ui.comboBox_2.activated.connect(self.setline_00read)
        # self.ui.comboBox_3.activated.connect(self.setEPS)
        # self.ui.OK_pushButton.clicked.connect(self.setAttributetoObj)


        # 设置Mark真假
        self.setDefaultMark()
        self.ui.OK_pushButton.clicked.connect(self.setMark)
        # 设置Mark初始值，为工作区的步长
        self.settingMarkInitialValues()
        # 设置到物体的Mark的值
        self.ui.OK_pushButton.clicked.connect(self.setMarkValue)

        # 设置点的初始坐标
        self.setDefaultValue()
        self.lineedit_text_before = self.getTextofAutoLineEdit(self.auto_lineedit)
        # 设置点的坐标
        self.ui.OK_pushButton.clicked.connect(self.settheLocation)
        
        # 显示错误信息
        self.ui.OK_pushButton.clicked.connect(self.closeDialog)
        self.ui.OK_pushButton.clicked.connect(self.showWarningDialog)


        # 点击取消删除该物体
        self.ui.Cancel_pushButton.clicked.connect(self.deleteobj)
        # 点击取消关闭对话框
        self.ui.Cancel_pushButton.clicked.connect(self.close)
    def setDefaultMark(self):
        self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.ui.checkBox_2.setCheckState(QtCore.Qt.CheckState.Unchecked)
        self.ui.checkBox_3.setCheckState(QtCore.Qt.CheckState.Unchecked)
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
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)
            pass
    def settheLocation(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point.x',point_1_x_after[0])  
                else:
                    self.obj.setExpression('Point.x',None)
                    self.obj.Point.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point.x'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.Stringfunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point.y',None)
                    self.obj.Point.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point.y'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point.z',None)
                    self.obj.Point.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point.z'+'  '+str(point_1_z_before)+'\n'
        
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point.x',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point.x',None)
                    self.obj.Point.x=point_1_x_after[0]
            except:
                self.error=self.error+'Point.R'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.anglefunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point.y',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point.y',None)
                    self.obj.Point.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point.theta'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point.z',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point.z',None)
                    self.obj.Point.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point.Z'+'  '+str(point_1_z_before)+'\n'
            pass
        else:
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point.z',point_1_x_after[0])
                else:
                    self.obj.setExpression('Point.z',None)
                    self.obj.Point.z=point_1_x_after[0]
            except:
                self.error=self.error+'Point.Z'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.Stringfunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point.x',point_1_y_after[0])
                else:
                    self.obj.setExpression('Point.x',None)
                    self.obj.Point.x=point_1_y_after[0]
            except:
                self.error=self.error+'Point.R'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.anglefunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point.y',point_1_z_after[0])
                else:
                    self.obj.setExpression('Point.y',None)
                    self.obj.Point.y=point_1_z_after[0]
            except:
                self.error=self.error+'Point.theta'+'  '+str(point_1_z_before)+'\n'
class reshowPointDialog(showPointDialog):
    def deleteobj(self):
        pass
    def setDefaultMark(self):
        mark_x = True
        mark_y = True
        mark_z = True
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            mark_x = self.obj.X
            mark_y = self.obj.Y
            mark_z = self.obj.Z
        else:
            mark_x = self.obj.R
            mark_y = self.obj.Theta
            mark_z = self.obj.Z
        if mark_x:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Unchecked)
        if mark_y:
            self.ui.checkBox_2.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.ui.checkBox_2.setCheckState(QtCore.Qt.CheckState.Unchecked)
        if mark_z:
            self.ui.checkBox_3.setCheckState(QtCore.Qt.CheckState.Checked)
        else:
            self.ui.checkBox_3.setCheckState(QtCore.Qt.CheckState.Unchecked)
        # 为mark添加补充部分，由于老工程不存在相关属性所以放在异常处理部分 @lzg
        try:
            # if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            if True:
                mark_min_1 = self.obj.min_1
                mark_mid_1 = self.obj.mid_1
                mark_max_1 = self.obj.max_1
                mark_min_2 = self.obj.min_2
                mark_mid_2 = self.obj.mid_2
                mark_max_2 = self.obj.max_2
                mark_min_3 = self.obj.min_3
                mark_mid_3 = self.obj.mid_3
                mark_max_3 = self.obj.max_3
                if mark_min_1:
                    self.ui.checkBoxMark_1.setChecked(True)
                if mark_mid_1:
                    self.ui.checkBoxMark_4.setChecked(True)
                if mark_max_1:
                    self.ui.checkBoxMark_7.setChecked(True)
                if mark_min_2:
                    self.ui.checkBoxMark_2.setChecked(True)
                if mark_mid_2:
                    self.ui.checkBoxMark_5.setChecked(True)
                if mark_max_2:
                    self.ui.checkBoxMark_8.setChecked(True)
                if mark_min_3:
                    self.ui.checkBoxMark_3.setChecked(True)
                if mark_mid_3:
                    self.ui.checkBoxMark_6.setChecked(True)
                if mark_max_3:
                    self.ui.checkBoxMark_9.setChecked(True)
            pass
        except:
            pass

    def setDefaultValue(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            list1=self.obj.ExpressionEngine
            list2=['','','']
            for i in range(len(list1)):
                if list1[i][0] == 'Point.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'Point.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'Point.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
            
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.Point.x,length))+length
                    elif x==1:
                        list2[x]=str(ValueUnitslength(self.obj.Point.y,length))+length
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.Point.z,length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
        else:
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','','']
            for i in range(len(list1)):
                if list1[i][0] == 'Point.x':
                    str1=list1[i][1].replace('Param.','')
                    list2[0]=str1
                elif list1[i][0] == 'Point.y':
                    str1=list1[i][1].replace('Param.','')
                    list2[1]=str1
                elif list1[i][0] == 'Point.z':
                    str1=list1[i][1].replace('Param.','')
                    list2[2]=str1
                
                
            for x in range(len(list2)):
                if len(list2[x]) == 0:
                    if x == 0:
                        list2[x]=str(ValueUnitslength(self.obj.Point.x,length))+length
                    elif x==1:
                        # list2[x]=str(self.obj.Point_1.y)+angle
                        list2[x]=str(ValueUnitsangle(self.obj.Point.y,angle))+angle
                    elif x==2:
                        list2[x]=str(ValueUnitslength(self.obj.Point.z,length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
        if FreeCAD.ActiveDocument.CoordinateSystem=='Cylindrical':
            InputTools.textChangedbefore(self.ui.lineEdit,self.ui.lineEdit_2,self.ui.lineEdit_3)