#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
import ArrayDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD,PartChipic
import ProjectSetting
import re

class showArrayDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = ArrayDialog.Ui_Dialog()
        self.ui.setupUi(self)

        # self.setModal(True)
        self.obj = obj
        self.error = ''
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.move(screen.right()-self.size().width()-150, screen.bottom()*0.5-200)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.ui.lineEdit.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_2.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_3.setcompleterlist(getGlobalVar())
        self.ui.lineEdit_4.setcompleterlist(getGlobalVar())

        self.obj_resultshape = FreeCAD.ActiveDocument.ResultShape
        # self.obj_resultshape.ViewObject.Visibility = False
        self.obj_resultshape.ViewObject.DisplayMode = u'Flat Lines'
        # self.obj_resultshape.ViewObject.ShapeColor = (0.58, 0.58, 0.58)
        self.obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
        self.obj_resultshape.ViewObject.Transparency = 85
        # self.obj.ViewObject.ShapeColor = (0.00, 1.00, 0.00)
        self.obj.ViewObject.DisplayMode = u'Flat Lines'
        self.obj.ViewObject.Transparency = 0
        self.obj.ViewObject.Visibility = True

        # 根据坐标系设置面板信息
        # self.addcomboboxitem()
        self.setDialog()

        # 设置初始化的label
        self.setDefaultLabel()
        # 设置Label
        self.ui.OK_pushButton.clicked.connect(self.setLabel)
        # 设置Order
        self.setOrder()
        # 设置物体order，以及排序
        self.ui.OK_pushButton.clicked.connect(self.OrderChanged)
        # 设置属性
        self.setAttributeText()
        self.ui.comboBox.activated.connect(self.setAttribute)
        #设置array type
        self.setBaseType()
        self.setArrayType()
        self.ui.comboBox_2.activated.connect(self.setArrayTypetoObj)
        self.setDialog()
        self.ui.comboBox_2.activated.connect(self.setDialog)
        # self.ui.comboBox_3.activated.connect(self.setDialog)

        #设置position信息到obj
        self.ui.OK_pushButton.clicked.connect(self.settheLocation)

        # 显示错误信息
        self.ui.OK_pushButton.clicked.connect(self.closeDialog)
        self.ui.OK_pushButton.clicked.connect(self.showWarningDialog)

        # 点击取消删除该物体
        self.ui.Cancel_pushButton.clicked.connect(self.deleteobj)
        # 点击取消关闭对话框
        self.ui.Cancel_pushButton.clicked.connect(self.close)

###############################  设置与OK,Cancel相关的函数 ########################################## 
    def deleteobj(self):
        doc = FreeCAD.ActiveDocument
        doc.removeObject(self.obj.Name)
        # self.obj_resultshape.ViewObject.Visibility = True
        # self.obj.ViewObject.Visibility = False
        pass
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
    def closeEvent(self,event):
        # self.obj_resultshape.ViewObject.Visibility = True
        self.obj_resultshape.ViewObject.Transparency = 0
        self.obj.ViewObject.Visibility = False
        QtGui.QDialog.closeEvent(self, event)
        
##############################  设置与Dialog面板相关的函数 ######################################
    def additem1(self):
        self.ui.comboBox_3.clear()
        self.ui.comboBox_3.addItem('XY')
        self.ui.comboBox_3.addItem('XZ')
        self.ui.comboBox_3.addItem('YZ')
    def additem2(self):
        self.ui.comboBox_3.clear()
        self.ui.comboBox_3.addItem('X')
        self.ui.comboBox_3.addItem('Y')
        self.ui.comboBox_3.addItem('Z')
    def additem3(self):
        self.ui.comboBox_3.clear()
        self.ui.comboBox_3.addItem('RZ')
    def additem4(self):
        self.ui.comboBox_3.clear()
        self.ui.comboBox_3.addItem('Z')

    def allshow(self):
        self.ui.label_01.show()
        self.ui.label_02.show()
        self.ui.label_03.show()
        self.ui.label_04.show()
        self.ui.label_05.show()
        self.ui.lineEdit.show()
        self.ui.lineEdit_2.show()
        self.ui.lineEdit_3.show()
        self.ui.lineEdit_4.show()
        self.ui.comboBox_3.show()
    def setDialog(self):
        arraytype = self.ui.comboBox_2.currentText()
        # ortho_face = self.ui.comboBox_3.currentText()
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            if arraytype == 'linear':
                self.allshow()
                self.ui.label_01.setText('Interval X:')
                self.ui.label_02.setText('Interval Y:')
                self.ui.label_03.setText('Interval Z:')
                self.ui.label_04.setText('Number:')
                self.ui.label_05.hide()
                self.ui.comboBox_3.hide()
                self.setlinearDialog()
            elif arraytype == 'ortho':
                self.allshow()
                self.additem1()
                obj_ortho_face = self.obj.OrthoFace
                if obj_ortho_face == 'XY':
                    self.ui.comboBox_3.setCurrentIndex(0)
                elif obj_ortho_face == 'XZ':
                    self.ui.comboBox_3.setCurrentIndex(1)
                elif obj_ortho_face == 'YZ':
                    self.ui.comboBox_3.setCurrentIndex(2)
                self.setortho()
                self.ui.comboBox_3.activated.connect(self.setortho)
                self.ui.label_05.setText('Ortho Face:')
                self.setorthoDialog()
            else:
                self.allshow()
                self.additem2()
                center_axis = self.obj.CenterAxis
                if center_axis == 'X':
                    self.ui.comboBox_3.setCurrentIndex(0)
                elif center_axis == 'Y':
                    self.ui.comboBox_3.setCurrentIndex(1)
                else :
                    self.ui.comboBox_3.setCurrentIndex(2)
                self.ui.label_01.setText('Number Polar:')
                self.ui.label_02.hide()
                self.ui.label_03.hide()
                self.ui.label_04.hide()
                self.ui.lineEdit_2.hide()
                self.ui.lineEdit_3.hide()
                self.ui.lineEdit_4.hide()
                self.ui.label_05.setText('Center Axis:')
                
                self.setpolarDialog()

        elif FreeCAD.ActiveDocument.CoordinateSystem == 'Polar':
            if arraytype == 'linear':
                self.allshow()
                self.ui.label_01.setText('Interval R:')
                self.ui.label_02.setText('Interval Theta:')
                self.ui.label_03.setText('Interval Z:')
                self.ui.label_04.setText('Number:')
                self.ui.label_05.hide()
                self.ui.comboBox_3.hide()
                self.setlinearDialog()
            elif arraytype == 'ortho':
                self.allshow()
                self.additem3()
                self.ui.label_01.setText('Interval R:')
                self.ui.label_02.setText('Interval Z:')
                self.ui.label_03.setText('Number R:')
                self.ui.label_04.setText('Number Z:')
                self.ui.label_05.setText('Ortho Face:')
                self.setorthoDialog()
            else:
                self.allshow()
                self.ui.label_01.setText('Number Polar:')
                self.ui.label_02.hide()
                self.ui.label_03.hide()
                self.ui.label_04.hide()
                self.ui.lineEdit_2.hide()
                self.ui.lineEdit_3.hide()
                self.ui.lineEdit_4.hide()
                self.ui.label_05.setText('Center Axis:')
                self.additem4()
                self.setpolarDialog()
        else:
            if arraytype == 'linear':
                self.allshow()
                self.ui.label_01.setText('Interval Z:')
                self.ui.label_02.setText('Interval R:')
                self.ui.label_03.setText('Interval Theta:')
                self.ui.label_04.setText('Number:')
                self.ui.label_05.hide()
                self.ui.comboBox_3.hide()
                self.setlinearDialog()
            elif arraytype == 'ortho':
                self.allshow()
                self.additem3()
                self.ui.label_01.setText('Interval R:')
                self.ui.label_02.setText('Interval Z:')
                self.ui.label_03.setText('Number R:')
                self.ui.label_04.setText('Number Z:')
                self.ui.label_05.setText('Ortho Face:')
                self.setorthoDialog()
            else:
                self.allshow()
                self.ui.label_01.setText('Number Polar:')
                self.ui.label_02.hide()
                self.ui.label_03.hide()
                self.ui.label_04.hide()
                self.ui.lineEdit_2.hide()
                self.ui.lineEdit_3.hide()
                self.ui.lineEdit_4.hide()
                self.ui.label_05.setText('Center Axis:')
                self.additem4()
                self.setpolarDialog()
        pass
    def setortho(self):
        ortho_face = self.ui.comboBox_3.currentText()
        if ortho_face == 'XY':
            self.ui.label_01.setText('Interval X:')
            self.ui.label_02.setText('Interval Y:')
            self.ui.label_03.setText('Number X:')
            self.ui.label_04.setText('Number Y:')
        elif ortho_face == 'XZ':
            self.ui.label_01.setText('Interval X:')
            self.ui.label_02.setText('Interval Z:')
            self.ui.label_03.setText('Number X:')
            self.ui.label_04.setText('Number Z:')
        elif ortho_face == 'YZ' :
            self.ui.label_01.setText('Interval Y:')
            self.ui.label_02.setText('Interval Z:')
            self.ui.label_03.setText('Number Y:')
            self.ui.label_04.setText('Number Z:')
##############################  设置与Label相关的函数 ###########################################
    def setDefaultLabel(self):
        obj_label=self.obj.Label
        self.ui.Base_lineEdit_1.setText(obj_label)

    def setLabel(self):
        Obj_Label = self.ui.Base_lineEdit_1.text()
        self.obj.Label = Obj_Label
###############################  设置与Order相关的函数 ##########################################
    def setOrder(self):
        num = self.obj.Order
        self.ui.Base_lineEdit_2.setValue(int(num))

    def OrderChanged(self):
        '''
        根据修改的Order进行插入排序
        '''
        docName = self.obj.Document.Name
        curNumOfObjects = Common.Tools.ObjectsTools.getNumOfObjects(docName)
        lastOrder = self.ui.Base_lineEdit_2.value()
        lastOrder = int(lastOrder)
        FreeCAD.Console.PrintMessage(str(lastOrder)+'  '+str(curNumOfObjects-1))
        
        if lastOrder <= curNumOfObjects-1:
            if lastOrder < self.obj.Order:
                for i in range(curNumOfObjects-lastOrder-1):
                    self.obj.Order = self.obj.Order-1
            elif lastOrder > self.obj.Order:
                for i in range(lastOrder-self.obj.Order):
                    self.obj.Order = self.obj.Order+1
        pass
    def setAttributeText(self):
        '''
        添加索引项，
        设置初始的值（读取obj的属性来设置）
        根据是否是custom编辑属性框的进一步的属性
        '''
        self.ui.comboBox.addItem(Common.Tools.ObjectsTools.Attribute.NotDefine)
        self.ui.comboBox.addItem(Common.Tools.ObjectsTools.Attribute.Conductor)
        self.ui.comboBox.addItem(Common.Tools.ObjectsTools.Attribute.Custom)
        self.ui.comboBox.addItem("Void")
        if self.obj.Attribute == 'NotDefine':
            self.ui.comboBox.setCurrentIndex(0)
        elif self.obj.Attribute == 'Conductor':
            self.ui.comboBox.setCurrentIndex(1)
        elif self.obj.Attribute == 'Custom':
            self.ui.comboBox.setCurrentIndex(2)
        elif self.obj.Attribute == 'Vacuo':
            self.ui.comboBox.setCurrentIndex(3)
        pass
    def setAttribute(self):
        '''
        根据索引项的切换，实时修改obj的attribute
        '''
        text1=self.ui.comboBox.currentText()
        if text1=='NotDefine':
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.NotDefine
            self.ui.frame.hide()
        elif text1=='Conductor':
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.Conductor
        elif text1=='Custom':
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.Custom
        elif text1=='Void':
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.Vacuo
        pass
    def setBaseType(self):
        '''
        根据arraytype的信息设置Dialog
        '''
        base_type = self.obj.BaseType
        self.ui.label_type.setText(base_type)
    def setArrayType(self):
        array_type = self.obj.ArrayType
        # FreeCAD.Console.PrintMessage(array_type)
        if array_type == 'linear':
            self.ui.comboBox_2.setCurrentIndex(0)
        elif array_type == 'ortho':
            # FreeCAD.Console.PrintMessage('test!!!!!!!!!!!!!\n')
            self.ui.comboBox_2.setCurrentIndex(1)
            # FreeCAD.Console.PrintMessage('test@@@@@@@@@@@@\n')
        elif array_type == 'polar':
            self.ui.comboBox_2.setCurrentIndex(2)
    def setArrayTypetoObj(self):
        at = self.ui.comboBox_2.currentText()
        if at == 'linear':
            self.obj.ArrayType = 'linear'
        elif at == 'ortho':
            self.obj.ArrayType = 'ortho'
        else:
            self.obj.ArrayType = 'polar'
    def setlinearDialog(self):
        # 这里需要根据当前坐标系进行设置
        units = FreeCAD.Units.getDefaultUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem =="Rectangular":
            if units[0]==0:
                self.ui.lineEdit.setText('0mm')
                self.ui.lineEdit_2.setText('0mm')
                self.ui.lineEdit_3.setText('0mm')
            elif units[0]==1:
                self.ui.lineEdit.setText('0cm')
                self.ui.lineEdit_2.setText('0cm')
                self.ui.lineEdit_3.setText('0cm')
            else:
                self.ui.lineEdit.setText('0m')
                self.ui.lineEdit_2.setText('0m')
                self.ui.lineEdit_3.setText('0m')
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            if units[0]==0:
                self.ui.lineEdit.setText('0mm')
                self.ui.lineEdit_3.setText("0mm")
            elif units[0]==1:
                self.ui.lineEdit.setText('0cm')
                self.ui.lineEdit_3.setText("0cm")
            else:
                self.ui.lineEdit.setText('0m')
                self.ui.lineEdit_3.setText("0m")
            if units[1]==1:
                self.ui.lineEdit_2.setText("0rad")
            else:
                self.ui.lineEdit_2.setText("0deg")
        else:
            if units[0]==0:
                self.ui.lineEdit.setText("0mm")
                self.ui.lineEdit_2.setText("0mm")
            elif units[0]==1:
                self.ui.lineEdit.setText("0cm")
                self.ui.lineEdit_2.setText("0cm")
            else :
                self.ui.lineEdit.setText("0m")
                self.ui.lineEdit_2.setText("0m")
            if units[1]==1:
                self.ui.lineEdit_3.setText("0rad")
            else:
                self.ui.lineEdit_3.setText("0deg")
        self.ui.lineEdit_4.setText('2')
    def setorthoDialog(self):
        self.ui.lineEdit.setText('0mm')
        self.ui.lineEdit_2.setText('0mm')
        self.ui.lineEdit_3.setText('1')
        self.ui.lineEdit_4.setText('1')
    def setpolarDialog(self):
        self.ui.lineEdit.setText('1')
    
    def settheLocation(self):
        from Modeling.Common.Tools import InputTools
        arraytype = self.ui.comboBox_2.currentText()
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            if arraytype == 'linear':
                point_1_x_before = self.ui.lineEdit.text()
                point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                try:
                    if point_1_x_after[1] == 2:
                        self.obj.setExpression('IntervalX',point_1_x_after[0])    
                    else:
                        self.obj.IntervalX = point_1_x_after[0]
                except:
                    self.error = self.error+'IntervalX'+'  '+str(point_1_x_before)+'\n'
                
                point_1_y_before = self.ui.lineEdit_2.text()
                point_1_y_after = InputTools.Stringfunctions(point_1_y_before)
                try:
                    if point_1_y_after[1] == 2:
                        self.obj.setExpression('IntervalY',point_1_y_after[0])    
                    else:
                        self.obj.IntervalY = point_1_y_after[0]
                except:
                    self.error = self.error+'IntervalY'+'  '+str(point_1_y_before)+'\n'
                
                point_1_z_before = self.ui.lineEdit_3.text()
                point_1_z_after = InputTools.Stringfunctions(point_1_z_before)
                try:
                    if point_1_z_after[1] == 2:
                        self.obj.setExpression('IntervalZ',point_1_z_after[0])    
                    else:
                        self.obj.IntervalZ = point_1_z_after[0]
                except:
                    self.error = self.error+'IntervalZ'+'  '+str(point_1_z_before)+'\n'

                num_linear = self.ui.lineEdit_4.text()
                try:
                    self.obj.Number = int(num_linear)
                except:
                    self.error = self.error+'Number  '+str(num_linear)+'\n'
                
            elif arraytype == 'ortho':
                ortho_face = self.ui.comboBox_3.currentText()
                if ortho_face == 'XY':
                    point_1_x_before = self.ui.lineEdit.text()
                    point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                    try:
                        if point_1_x_after[1] == 2:
                            self.obj.setExpression('IntervalX',point_1_x_after[0])    
                        else:
                            self.obj.IntervalX = point_1_x_after[0]
                    except:
                        self.error = self.error+'IntervalX'+'  '+str(point_1_x_before)+'\n'
                
                    point_1_y_before = self.ui.lineEdit_2.text()
                    point_1_y_after = InputTools.Stringfunctions(point_1_y_before)
                    try:
                        if point_1_y_after[1] == 2:
                            self.obj.setExpression('IntervalY',point_1_y_after[0])    
                        else:
                            self.obj.IntervalY = point_1_y_after[0]
                    except:
                        self.error = self.error+'IntervalY'+'  '+str(point_1_y_before)+'\n'
                
                    num_x = self.ui.lineEdit_3.text()
                    try:
                        self.obj.NumberX = int(num_x)
                    except:
                        self.error = self.error+'NumberX  '+str(num_x)+'\n'

                    num_y = self.ui.lineEdit_4.text()
                    try:
                        self.obj.NumberY = int(num_y)
                    except:
                        self.error = self.error+'NumberY  '+str(num_y)+'\n'
                elif ortho_face == 'XZ':
                    point_1_x_before = self.ui.lineEdit.text()
                    point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                    try:
                        if point_1_x_after[1] == 2:
                            self.obj.setExpression('IntervalX',point_1_x_after[0])    
                        else:
                            self.obj.IntervalX = point_1_x_after[0]
                    except:
                        self.error = self.error+'IntervalX'+'  '+str(point_1_x_before)+'\n'

                    point_1_y_before = self.ui.lineEdit_2.text()
                    point_1_y_after = InputTools.Stringfunctions(point_1_y_before)
                    try:
                        if point_1_y_after[1] == 2:
                            self.obj.setExpression('IntervalZ',point_1_y_after[0])    
                        else:
                            self.obj.IntervalZ = point_1_y_after[0]
                    except:
                        self.error = self.error+'IntervalZ'+'  '+str(point_1_y_before)+'\n'
                    
                    num_x = self.ui.lineEdit_3.text()
                    try:
                        self.obj.NumberX = int(num_x)
                    except:
                        self.error = self.error+'NumberX  '+str(num_x)+'\n'
                    
                    num_z = self.ui.lineEdit_4.text()
                    try:
                        self.obj.NumberZ = int(num_z)
                    except:
                        self.error = self.error+'NumberZ  '+str(num_z)+'\n'
                elif ortho_face == 'YZ':
                    point_1_x_before = self.ui.lineEdit.text()
                    point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                    try:
                        if point_1_x_after[1] == 2:
                            self.obj.setExpression('IntervalY',point_1_x_after[0])    
                        else:
                            self.obj.IntervalY = point_1_x_after[0]
                    except:
                        self.error = self.error+'IntervalY'+'  '+str(point_1_x_before)+'\n'

                    point_1_y_before = self.ui.lineEdit_2.text()
                    point_1_y_after = InputTools.Stringfunctions(point_1_y_before)
                    try:
                        if point_1_y_after[1] == 2:
                            self.obj.setExpression('IntervalZ',point_1_y_after[0])    
                        else:
                            self.obj.IntervalZ = point_1_y_after[0]
                    except:
                        self.error = self.error+'IntervalZ'+'  '+str(point_1_y_before)+'\n'
                    
                    num_y = self.ui.lineEdit_3.text()
                    try:
                        self.obj.NumberY = int(num_y)
                    except:
                        self.error = self.error+'NumberY  '+str(num_y)+'\n'
                    
                    num_z = self.ui.lineEdit_4.text()
                    try:
                        self.obj.NumberZ = int(num_z)
                    except:
                        self.error = self.error+'NumberZ  '+str(num_z)+'\n'
                
                of = self.ui.comboBox_3.currentText()
                if of == 'XY':
                    self.obj.OrthoFace = 'XY'
                elif of == 'XZ':
                    self.obj.OrthoFace = 'XZ'
                else:
                    self.obj.OrthoFace = 'YZ' 
            
            else:
                num_polar = self.ui.lineEdit.text()
                try:
                    self.obj.NumberPolar = int(num_polar)
                except:
                    self.error = self.error+'Number Polar  '+str(num_polar)+'\n'

                ca = self.ui.comboBox_3.currentText()
                if ca == 'X':
                    self.obj.CenterAxis = 'X'
                elif ca == 'Y':
                    self.obj.CenterAxis = 'Y'
                else:
                    self.obj.CenterAxis = 'Z'
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            if arraytype == 'linear':
                point_1_x_before = self.ui.lineEdit.text()
                point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                try:
                    if point_1_x_after[1] == 2:
                        self.obj.setExpression('IntervalR',point_1_x_after[0])    
                    else:
                        self.obj.IntervalR = point_1_x_after[0]
                except:
                    self.error = self.error+'IntervalR'+'  '+str(point_1_x_before)+'\n'
                
                point_1_y_before = self.ui.lineEdit_2.text()
                point_1_y_after = InputTools.anglefunctions(point_1_y_before)
                try:
                    if point_1_y_after[1] == 2:
                        self.obj.setExpression('IntervalTheta',point_1_y_after[0])    
                    else:
                        self.obj.IntervalTheta = point_1_y_after[0]
                except:
                    self.error = self.error+'IntervalTheta'+'  '+str(point_1_y_before)+'\n'
                
                point_1_z_before = self.ui.lineEdit_3.text()
                point_1_z_after = InputTools.Stringfunctions(point_1_z_before)
                try:
                    if point_1_z_after[1] == 2:
                        self.obj.setExpression('IntervalZ',point_1_z_after[0])    
                    else:
                        self.obj.IntervalZ = point_1_z_after[0]
                except:
                    self.error = self.error+'IntervalZ'+'  '+str(point_1_z_before)+'\n'

                num_linear = self.ui.lineEdit_4.text()
                try:
                    self.obj.Number = int(num_linear)
                except:
                    self.error = self.error+'Number  '+str(num_linear)+'\n'
            elif arraytype == 'ortho':
                point_1_x_before = self.ui.lineEdit.text()
                point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                try:
                    if point_1_x_after[1] == 2:
                        self.obj.setExpression('IntervalR',point_1_x_after[0])    
                    else:
                        self.obj.IntervalR = point_1_x_after[0]
                except:
                    self.error = self.error+'IntervalR'+'  '+str(point_1_x_before)+'\n'
                
                point_1_y_before = self.ui.lineEdit_2.text()
                point_1_y_after = InputTools.Stringfunctions(point_1_y_before)
                try:
                    if point_1_y_after[1] == 2:
                        self.obj.setExpression('IntervalZ',point_1_y_after[0])    
                    else:
                        self.obj.IntervalZ = point_1_y_after[0]
                except:
                    self.error = self.error+'IntervalZ'+'  '+str(point_1_y_before)+'\n'
                
                num_x = self.ui.lineEdit_3.text()
                try:
                    self.obj.NumberR = int(num_x)
                except:
                    self.error = self.error+'NumberR  '+str(num_x)+'\n'

                num_y = self.ui.lineEdit_4.text()
                try:
                    self.obj.NumberZ = int(num_y)
                except:
                    self.error = self.error+'NumberZ  '+str(num_y)+'\n'
            else:
                num_polar = self.ui.lineEdit.text()
                try:
                    self.obj.NumberPolar = int(num_polar)
                except:
                    self.error = self.error+'Number Polar  '+str(num_polar)+'\n'

                # ca = self.ui.comboBox_3.currentText()
                # if ca == 'X':
                #     self.obj.CenterAxis = 'X'
                # elif ca == 'Y':
                #     self.obj.CenterAxis = 'Y'
                # else:
                #     self.obj.CenterAxis = 'Z'
        else:
            if arraytype == 'linear':
                point_1_x_before = self.ui.lineEdit_2.text()
                point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                try:
                    if point_1_x_after[1] == 2:
                        self.obj.setExpression('IntervalR',point_1_x_after[0])    
                    else:
                        self.obj.IntervalR = point_1_x_after[0]
                except:
                    self.error = self.error+'IntervalR'+'  '+str(point_1_x_before)+'\n'
                
                point_1_y_before = self.ui.lineEdit_3.text()
                point_1_y_after = InputTools.anglefunctions(point_1_y_before)
                try:
                    if point_1_y_after[1] == 2:
                        self.obj.setExpression('IntervalTheta',point_1_y_after[0])    
                    else:
                        self.obj.IntervalTheta = point_1_y_after[0]
                except:
                    self.error = self.error+'IntervalTheta'+'  '+str(point_1_y_before)+'\n'
                
                point_1_z_before = self.ui.lineEdit.text()
                point_1_z_after = InputTools.Stringfunctions(point_1_z_before)
                try:
                    if point_1_z_after[1] == 2:
                        self.obj.setExpression('IntervalZ',point_1_z_after[0])    
                    else:
                        self.obj.IntervalZ = point_1_z_after[0]
                except:
                    self.error = self.error+'IntervalZ'+'  '+str(point_1_z_before)+'\n'

                num_linear = self.ui.lineEdit_4.text()
                try:
                    self.obj.Number = int(num_linear)
                except:
                    self.error = self.error+'Number  '+str(num_linear)+'\n'
            elif arraytype == 'ortho':
                point_1_x_before = self.ui.lineEdit.text()
                point_1_x_after = InputTools.Stringfunctions(point_1_x_before)
                try:
                    if point_1_x_after[1] == 2:
                        self.obj.setExpression('IntervalR',point_1_x_after[0])    
                    else:
                        self.obj.IntervalR = point_1_x_after[0]
                except:
                    self.error = self.error+'IntervalR'+'  '+str(point_1_x_before)+'\n'
                
                point_1_y_before = self.ui.lineEdit_2.text()
                point_1_y_after = InputTools.Stringfunctions(point_1_y_before)
                try:
                    if point_1_y_after[1] == 2:
                        self.obj.setExpression('IntervalZ',point_1_y_after[0])    
                    else:
                        self.obj.IntervalZ = point_1_y_after[0]
                except:
                    self.error = self.error+'IntervalZ'+'  '+str(point_1_y_before)+'\n'
                
                num_x = self.ui.lineEdit_3.text()
                try:
                    self.obj.NumberR = int(num_x)
                except:
                    self.error = self.error+'NumberR  '+str(num_x)+'\n'

                num_y = self.ui.lineEdit_4.text()
                try:
                    self.obj.NumberZ = int(num_y)
                except:
                    self.error = self.error+'NumberZ  '+str(num_y)+'\n'
            else:
                num_polar = self.ui.lineEdit.text()
                try:
                    self.obj.NumberPolar = int(num_polar)
                except:
                    self.error = self.error+'Number Polar  '+str(num_polar)+'\n'


#######################################设置error#################################
    def closeDialog(self):
        # FreeCAD.Console.PrintMessage('close\n')
        lastOrder = int(self.ui.Base_lineEdit_2.value())
        if len(self.error)==0:
            self.hide()
            FreeCAD.ActiveDocument.recompute()
            #PartGui.updateBoolean(lastOrder) #ZD
            PartChipic.updateBoolean(lastOrder, 1)
            self.obj_resultshape.ViewObject.Transparency = 0
            self.obj.ViewObject.Visibility = False
            # self.obj_resultshape.ViewObject.ShapeColor = (0.58, 0.58, 0.58)
            self.obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
            # self.ui.lineEdit._completer.popup().hide()
            self.close()
    def showWarningDialog(self):
        if len(self.error)!=0:
            import ErrorFunction
            err_dia=ErrorFunction.ErrorDialog.WarningDialog()
            err_dia.errormassageinput(self.error)
            err_dia.show()
            err_dia.exec_()
            self.error=''
        pass

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
class reshowArrayDialog(showArrayDialog):
    def deleteobj(self):
        pass

    def setlinearDialog(self):
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        Expression_list = self.obj.ExpressionEngine
        list1 = ['','','','']
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            for x in range(len(Expression_list)):
                if Expression_list[x][0] == 'IntervalX':
                    str1 = Expression_list[x][1].replace('Param.','')
                    list1[0] = str1
                elif Expression_list[x][0] == 'IntervalY':
                    str2 = Expression_list[x][1].replace('Param.','')
                    list1[1] = str2
                elif Expression_list[x][0] == 'IntervalZ':
                    str3 = Expression_list[x][1].replace('Param.','')
                    list1[2] = str3
                elif Expression_list[x][0] == 'Number':
                    str4 = Expression_list[x][1].replace('Param.','')
                    list1[3] = str4

            for x in range(len(list1)):
                if len(list1[x]) == 0:
                    if x == 0:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalX.Value, length))+length
                    elif x == 1:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalY.Value, length))+length
                    elif x == 2:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalZ.Value, length))+length
                    elif x == 3:
                        list1[x] = self.obj.Number
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            for x in range(len(Expression_list)):
                if Expression_list[x][0] == 'IntervalR':
                    str1 = Expression_list[x][1].replace('Param.','')
                    list1[0] = str1
                elif Expression_list[x][0] == 'IntervalTheta':
                    str2 = Expression_list[x][1].replace('Param.','')
                    list1[1] = str2
                elif Expression_list[x][0] == 'IntervalZ':
                    str3 = Expression_list[x][1].replace('Param.','')
                    list1[2] = str3
                elif Expression_list[x][0] == 'Number':
                    str4 = Expression_list[x][1].replace('Param.','')
                    list1[3] = str4
            for x in range(len(list1)):
                if len(list1[x]) == 0:
                    if x == 0:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalR.Value, length))+length
                    elif x == 1:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalTheta.Value, angle))+angle
                    elif x == 2:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalZ.Value, length))+length
                    elif x == 3:
                        list1[x] = self.obj.Number
        else:
            for x in range(len(Expression_list)):
                if Expression_list[x][0] == 'IntervalZ':
                    str1 = Expression_list[x][1].replace('Param.','')
                    list1[0] = str1
                elif Expression_list[x][0] == 'IntervalR':
                    str2 = Expression_list[x][1].replace('Param.','')
                    list1[1] = str2
                elif Expression_list[x][0] == 'IntervalTheta':
                    str3 = Expression_list[x][1].replace('Param.','')
                    list1[2] = str3
                elif Expression_list[x][0] == 'Number':
                    str4 = Expression_list[x][1].replace('Param.','')
                    list1[3] = str4
            for x in range(len(list1)):
                if len(list1[x]) == 0:
                    if x == 0:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalZ.Value, length))+length
                    elif x == 1:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalR.Value, length))+length
                    elif x == 2:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalTheta.Value, angle))+angle
                    elif x == 3:
                        list1[x] = self.obj.Number


        self.ui.lineEdit.setText(list1[0])
        self.ui.lineEdit_2.setText(list1[1])
        self.ui.lineEdit_3.setText(list1[2])
        self.ui.lineEdit_4.setText(str(list1[3]))
    def setorthoDialog(self):
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            Expression_list = self.obj.ExpressionEngine
            list1 = ['','','','','','']
            for x in range(len(Expression_list)):
                if Expression_list[x][0] == 'IntervalX':
                    str1 = Expression_list[x][1].replace('Param.','')
                    list1[0] = str1
                elif Expression_list[x][0] == 'IntervalY':
                    str2 = Expression_list[x][1].replace('Param.','')
                    list1[1] = str2
                elif Expression_list[x][0] == 'IntervalZ':
                    str3 = Expression_list[x][1].replace('Param.','')
                    list1[2] = str3
                elif Expression_list[x][0] == 'NumberX':
                    str4 = Expression_list[x][1].replace('Param.','')
                    list1[3] = str4
                elif Expression_list[x][0] == 'NumberY':
                    str5 = Expression_list[x][1].replace('Param.','')
                    list1[4] = str5
                elif Expression_list[x][0] == 'NumberZ':
                    str6 = Expression_list[x][1].replace('Param.','')
                    list1[5] = str6

            for x in range(len(list1)):
                if len(list1[x]) == 0:
                    if x == 0:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalX.Value, length))+length
                    elif x == 1:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalY.Value, length))+length
                    elif x == 2:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalZ.Value, length))+length
                    elif x == 3:
                        list1[x] = self.obj.NumberX
                    elif x == 4:
                        list1[x] = self.obj.NumberY
                    elif x == 5:
                        list1[x] = self.obj.NumberZ
            ortho_face = self.ui.comboBox_3.currentText()
            # FreeCAD.Console.PrintMessage('test!!!!!!!!!!!\n')
            if ortho_face == 'XY':
                self.ui.lineEdit.setText(list1[0])
                self.ui.lineEdit_2.setText(list1[1])
                self.ui.lineEdit_3.setText(str(list1[3]))
                self.ui.lineEdit_4.setText(str(list1[4]))
            elif ortho_face == 'XZ':
            # FreeCAD.Console.PrintMessage('test@@@@@@@@@@@@\n')
                self.ui.lineEdit.setText(list1[0])
                self.ui.lineEdit_2.setText(list1[2])
                self.ui.lineEdit_3.setText(str(list1[3]))
                self.ui.lineEdit_4.setText(str(list1[5]))
            elif ortho_face == 'YZ':
                self.ui.lineEdit.setText(list1[1])
                self.ui.lineEdit_2.setText(list1[2])
                self.ui.lineEdit_3.setText(str(list1[4]))
                self.ui.lineEdit_4.setText(str(list1[5]))
        else :
            Expression_list = self.obj.ExpressionEngine
            list1 = ['','','','']
            for x in range(len(Expression_list)):
                if Expression_list[x][0] == 'IntervalR':
                    str1 = Expression_list[x][1].replace('Param.','')
                    list1[0] = str1
                elif Expression_list[x][0] == 'IntervalZ':
                    str2 = Expression_list[x][1].replace('Param.','')
                    list1[1] = str2
                elif Expression_list[x][0] == 'NumberR':
                    str4 = Expression_list[x][1].replace('Param.','')
                    list1[2] = str4
                elif Expression_list[x][0] == 'NumberZ':
                    str5 = Expression_list[x][1].replace('Param.','')
                    list1[3] = str5
            for x in range(len(list1)):
                if len(list1[x]) == 0:
                    if x == 0:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalR.Value, length))+length
                    elif x == 1:
                        list1[x] = str(ValueUnitslength(self.obj.IntervalZ.Value, length))+length
                    elif x == 2:
                        list1[x] = self.obj.NumberR
                    elif x == 3:
                        list1[x] = self.obj.NumberZ
            self.ui.lineEdit.setText(list1[0])
            self.ui.lineEdit_2.setText(list1[1])
            self.ui.lineEdit_3.setText(str(list1[2]))
            self.ui.lineEdit_4.setText(str(list1[3]))
                


    def setpolarDialog(self):
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        Expression_list = self.obj.ExpressionEngine
        str1 = ''
        for x in range(len(Expression_list)):
            if Expression_list[x][0] == 'NumberPolar':
                str1 = Expression_list[x][1].replace('Param.','')
        if len(str1) == 0:
            str1 = self.obj.NumberPolar
        self.ui.lineEdit.setText(str(str1))
