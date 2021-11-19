#-*- coding: utf-8 -*-
from PySide import QtGui,QtCore
from Modeling import Common
import FreeCAD
import ProjectSetting
import re
import PartGui,PartChipic
import time
from Modeling.Common.Tools.AllDialogFather import *
class showObjDialog(AllDialogFather):
    def __init__(self, obj, parent=None):
        '''
        #此处写明继承的那个ui文件
        # self.ui = CylinderDialog.Ui_Dialog()
        # self.ui.setupUi(self)

        # self.ui.lineEdit.setcompleterlist(getGlobalVar())
        # 此处为行编辑器添加自动补全的变量列表
        '''
        AllDialogFather.__init__(self,parent)
        self.lineedit_text_before = []
        self.lineedit_text_after = []
        self.auto_lineedit = [] 
        try:
            self.attribute_before = obj.Attribute
        except:
            pass
    def initDialog(self):
        #设置对话框类型
        self.dialogType = DialogType.MODEL_DIALOG
        #链接okButton信号
        self.ui.OK_pushButton.clicked.connect(self.modelOkButtonClincked)
    #ok按钮点击槽
    def modelOkButtonClincked(self):
        #如果是模型对话框，则执行模型对话框的保存函数
        if self.dialogType == DialogType.MODEL_DIALOG:
            self.removeRepetitionName()
            self.modelDialogOkButtonClincked()
    def setUI(self):
        # 添加mark的补充部分
        self.setMarkUi()
        # 获取所有的AutoLineEdit
        self.auto_lineedit = self.getAllAutoLineEdits()

        # 设置Frame隐藏
        self.ui.frame.hide()
        # 根据坐标系设置面板信息
        self.setDialog()

        # 设置初始化的label
        self.setDefaultLabel()
        # 设置Order
        self.setOrder()
        # 设置属性
        self.setAttributeText()
        # 设置初始化Custom界面
        self.ui.comboBox.activated.connect(self.setAttribute)
        self.ui.comboBox_2.activated.connect(self.setline_00read)
        self.ui.comboBox_3.activated.connect(self.setEPS)
        
        # 设置Mark真假
        self.setDefaultMark()
        # 设置Mark初始值，为工作区的步长
        self.settingMarkInitialValues()
        
        # 设置点的初始坐标
        self.setDefaultValue()
        self.lineedit_text_before = self.getTextofAutoLineEdit(self.auto_lineedit)
        # 点击取消删除该物体
        self.ui.Cancel_pushButton.clicked.connect(self.deleteobj)
        # 点击取消关闭对话框
        self.ui.Cancel_pushButton.clicked.connect(self.close)
    def modelDialogOkButtonClincked(self):
        # FreeCAD.Console.PrintError('\n进入ok键所链接的函数\n')
        # 设置Label
        self.setLabel()
        # 设置order改变
        self.OrderChanged()
        # 设置点的坐标
        self.settheLocation()
        # FreeCAD.Console.PrintError('\n进入ok键所链接的函数，设置坐标之后\n')
        # 设置到物体的Mark的值
        self.setMarkValue()
        self.setMark()
        self.setExtraMark()
        # FreeCAD.Console.PrintError('\n进入ok键所链接的函数，设置mark之后\n')
        self.setAttributetoObj()
        # FreeCAD.Console.PrintError('\n进入ok键所链接的函数，设置属性之后\n')
        # 显示错误信息
        self.closeDialog()
        self.showWarningDialog()
        # FreeCAD.Console.PrintError('\n退出ok键所链接的函数\n')
    def setFieView(self):
        ObjectsTools.setFitViewOfObject(self.obj)

    def closeEvent(self,event):
        # self.obj_resultshape.ViewObject.Visibility = True
        self.obj_resultshape.ViewObject.Transparency = 0
        self.obj.ViewObject.Visibility = False
        from Physics.PhysicsTools import SetVisibilityOfModels
        SetVisibilityOfModels.setVisibility()
        QtGui.QDialog.closeEvent(self, event)
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
    def DisplayMode(self):
        try:
            self.obj_resultshape = FreeCAD.ActiveDocument.ResultShape
            self.obj_resultshape.ViewObject.DisplayMode = u'Flat Lines'
            # self.obj_resultshape.ViewObject.ShapeColor = (0.58, 0.58, 0.58)
            self.obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
            self.obj_resultshape.ViewObject.Transparency = 85
            #@fubiao 这里修改resultShape的参数，使她变为“金属化”材质
            diffuseColor=self.obj_resultshape.ViewObject.DiffuseColor
            self.obj_resultshape.ViewObject.ShapeMaterial.AmbientColor=(0.18,0.18,0.18)
            self.obj_resultshape.ViewObject.ShapeMaterial.SpecularColor=(0.45,0.45,0.45)
            self.obj_resultshape.ViewObject.ShapeMaterial.Shininess=0.13
            self.obj_resultshape.ViewObject.DiffuseColor=diffuseColor
            FreeCAD.Console.PrintError("\n")
            #@fubiao end
            # self.obj.ViewObject.ShapeColor = (0.00, 1.00, 0.00)
            self.obj.ViewObject.DisplayMode = u'Flat Lines'
            self.obj.ViewObject.Transparency = 0
            self.obj.ViewObject.Visibility = True
        except:
            pass
    def getAllAutoLineEdits(self):
        '''
        @brief:获得UI中的所有AutoLineEdit控件对象list，
        '''
        lineEdits=[]
        for attr in dir(self.ui):
            if isinstance(getattr(self.ui, attr), Common.Tools.Completer.AutoCompleteEdit):
                lineEdits.append(getattr(self.ui, attr))
        return lineEdits
    def getTextofAutoLineEdit(self,lineedit_list):
        '''
        这个函数是为了获取对话框所有AutoLineEdit的内容
        '''
        lineedit_text = []
        for lineedit in lineedit_list:
            lineedit_text.append(lineedit.text())
        # 如果想看到对话框打开和结束的坐标信息就将下面这句话取消注释
        # FreeCAD.Console.PrintError('\n'+str(lineedit_text)+'\n')
        return lineedit_text
        pass
    def WhethertoRecompute(self):
        '''
        为了程序更加流畅，需要在没修改坐标信息的时候就不去重新计算体，
        这个函数就是为了满足这个功能，
        showDialog不需要不需要调用此函数，仅在reshow里面来调用，
        通过检查类名是否有reshow关键词来判断时候进入此函数\n
        简而言之，如果信息一样则返回假，信息不一样，或者执行有异常则返回真
        '''
        # FreeCAD.Console.PrintError('\n进入比对函数\n')
        self.lineedit_text_after = self.getTextofAutoLineEdit(self.auto_lineedit)
        need_recompute = False
        for i in range(len(self.lineedit_text_before)):
            # FreeCAD.Console.PrintError('\n进入for循环\n')
            try:
                if self.lineedit_text_before[i] == self.lineedit_text_after[i]:
                    # FreeCAD.Console.PrintError('\n进入if判断语句\n')
                    need_recompute = False
                else:
                    return True
            except BaseException:
                # FreeCAD.Console.PrintError('\n对比异常，直接返回真\n')
                return True
        # FreeCAD.Console.PrintError('\n退出比对函数\n')
        return need_recompute

##############################  设置与Dialog面板相关的函数 ######################################
    def setDialog(self):
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            pass
        elif FreeCAD.ActiveDocument.CoordinateSystem == 'Polar':
            self.ui.C_label_1.setText('        R    ')
            self.ui.C_label_2.setText('       Theta ')
            self.ui.C_label_3.setText('        Z    ')

            self.ui.NUG_label_1.setText('         R    ')
            self.ui.NUG_label_2.setText('       Theta ')
            self.ui.NUG_label_3.setText('         Z    ')
        else:
            self.ui.C_label_1.setText('        Z    ')
            self.ui.C_label_2.setText('        R    ')
            self.ui.C_label_3.setText('       Theta ')

            self.ui.NUG_label_1.setText('         Z    ')
            self.ui.NUG_label_2.setText('         R    ')
            self.ui.NUG_label_3.setText('        Theta  ')

##############################  设置与Label相关的函数 ###########################################
    def setDefaultLabel(self):
        obj_label=self.obj.Label
        self.ui.Base_lineEdit_1.setText(obj_label)

    def setLabel(self):
        Obj_Label = self.ui.Base_lineEdit_1.text()
        Obj_Label = Obj_Label.replace(' ','')
        self.obj.Label = Obj_Label
###############################  设置与Order相关的函数 ##########################################
    def setOrder(self):
        self.ui.Base_lineEdit_2.setMaximum(int(999))
        num = self.obj.Order
        self.order_before = self.obj.Order
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
                for i in range(int(self.obj.Order) - lastOrder):
                    self.obj.Order = self.obj.Order-1
            elif lastOrder > self.obj.Order:
                for i in range(lastOrder-self.obj.Order):
                    self.obj.Order = self.obj.Order+1
        pass
###############################  设置与Attribute相关的函数 ##########################################
    def setAttributeText(self):
        '''
        添加索引项，
        设置初始的值（读取obj的属性来设置）
        根据是否是custom编辑属性框的进一步的属性
        '''
        self.ui.comboBox.addItem(Common.Tools.ObjectsTools.Attribute.NotDefine)
        self.ui.comboBox.addItem(Common.Tools.ObjectsTools.Attribute.Conductor)
        self.ui.comboBox.addItem(Common.Tools.ObjectsTools.Attribute.Custom)
        self.ui.comboBox.addItem('Void')
        if self.obj.Attribute == 'NotDefine':
            self.ui.comboBox.setCurrentIndex(0)
        elif self.obj.Attribute == 'Conductor':
            self.ui.comboBox.setCurrentIndex(1)
        elif self.obj.Attribute == 'Custom':
            self.ui.comboBox.setCurrentIndex(2)
            self.ui.frame.show()
            self.setCustom()
        elif self.obj.Attribute == 'Vacuo':
            self.ui.comboBox.setCurrentIndex(3)
        pass
    def setCustom(self):
        '''
        设置custom的显示信息，前提是obj的属性随着索引项的修改而修改
        '''
        # 只是初始化，初始化之后的修改需要另写函数
        CS = self.obj.ConductivitySIGMA
        value_CS = self.obj.ConductivitySIGMAValue
        CS_EPS = self.obj.CS_SetEPS
        CS_EPS2 = self.obj.CS_SetEPS2
        CS_EPS3 = self.obj.CS_SetEPS3
        # self.ui.lineEdit_00.setText(str(value_CS))

        if CS == 'Anisotropy':
            self.ui.lineEdit_00.show()
            self.ui.lineEdit_04.show()
            self.ui.lineEdit_05.show()
            self.ui.lineEdit_00.setText(str(CS_EPS))
            self.ui.lineEdit_04.setText(str(CS_EPS2))
            self.ui.lineEdit_05.setText(str(CS_EPS3))
            self.ui.comboBox_2.setCurrentIndex(1)
        elif CS == 'Isotropy' :
            self.ui.lineEdit_00.show()
            self.ui.lineEdit_04.hide()
            self.ui.lineEdit_05.hide()
            self.ui.lineEdit_00.setText(str(CS_EPS))
            # self.ui.lineEdit_04.setText(str(CS_EPS))
            # self.ui.lineEdit_05.setText(str(CS_EPS))
            self.ui.comboBox_2.setCurrentIndex(0)
        else:
            self.ui.comboBox_2.setCurrentIndex(2)
            self.ui.lineEdit_00.hide()
            self.ui.lineEdit_04.hide()
            self.ui.lineEdit_05.hide()
            

        RDC = self.obj.RelativeDielectricConstant
        EPS = self.obj.SetEPS
        EPS2 = self.obj.SetEPS2
        EPS3 = self.obj.SetEPS3
        if RDC == 'Anisotropy':
            self.ui.comboBox_3.setCurrentIndex(1)
            self.ui.lineEdit_01.show()
            self.ui.lineEdit_02.show()
            self.ui.lineEdit_03.show()
            self.ui.lineEdit_01.setText(str(EPS))
            self.ui.lineEdit_02.setText(str(EPS2))
            self.ui.lineEdit_03.setText(str(EPS3))
        elif RDC == 'Isotropy':
            self.ui.comboBox_3.setCurrentIndex(0)
            self.ui.lineEdit_01.show()
            self.ui.lineEdit_01.setText(str(EPS))
            self.ui.lineEdit_02.hide()
            self.ui.lineEdit_03.hide()
        else:
            self.ui.comboBox_3.setCurrentIndex(2)
            self.ui.lineEdit_01.hide()
            self.ui.lineEdit_02.hide()
            self.ui.lineEdit_03.hide()
    def setAttribute(self):
        '''
        根据索引项的切换，实时修改obj的attribute
        '''
        text1=self.ui.comboBox.currentText()
        a1 = self.size()
        w1 = a1.width()
        if text1=='NotDefine':
            # self.ui.resize(520,380)
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.NotDefine
            self.ui.frame.hide()
            self.resize(w1,380)
            # FreeCAD.Console.PrintMessage('1111111111\n')
        elif text1=='Conductor':
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.Conductor
            self.ui.frame.hide()
            self.resize(w1,380)
            # FreeCAD.Console.PrintMessage('2222222222\n')
        elif text1=='Custom':
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.Custom
            self.ui.frame.show()
            self.setCustom()
        elif text1=='Void':
            self.obj.Attribute=Common.Tools.ObjectsTools.Attribute.Vacuo
            self.ui.frame.hide()
            # FreeCAD.Console.PrintMessage('hide\n')
            self.resize(w1,380)
            # FreeCAD.Console.PrintMessage('33333333333\n')
            pass
        pass
    def setEPS(self):
        text1=self.ui.comboBox_3.currentText()
        EPS = self.obj.SetEPS
        EPS2 = self.obj.SetEPS2
        EPS3 = self.obj.SetEPS3
        if text1 == 'Anisotropy':
            FreeCAD.Console.PrintMessage('\nindex suscess')
            self.ui.lineEdit_01.show()
            self.ui.lineEdit_02.show()
            self.ui.lineEdit_03.show()
            self.ui.lineEdit_01.setText(str(EPS))
            self.ui.lineEdit_02.setText(str(EPS2))
            self.ui.lineEdit_03.setText(str(EPS3))
        elif text1 == 'Isotropy':
            FreeCAD.Console.PrintMessage('\nisotropy suscess')
            self.ui.lineEdit_01.show()
            self.ui.lineEdit_01.setText(str(EPS))
            self.ui.lineEdit_02.hide()
            self.ui.lineEdit_03.hide()
        else:
            self.ui.lineEdit_01.hide()
            self.ui.lineEdit_02.hide()
            self.ui.lineEdit_03.hide()
        pass
    def setline_00read(self):
        CS=self.ui.comboBox_2.currentText()
        CS_EPS = self.obj.CS_SetEPS
        CS_EPS2 = self.obj.CS_SetEPS2
        CS_EPS3 = self.obj.CS_SetEPS3
        # self.ui.lineEdit_00.setText(str(value_CS))

        if CS == 'Anisotropy':
            self.ui.lineEdit_00.show()
            self.ui.lineEdit_04.show()
            self.ui.lineEdit_05.show()
            self.ui.lineEdit_00.setText(str(CS_EPS))
            self.ui.lineEdit_04.setText(str(CS_EPS2))
            self.ui.lineEdit_05.setText(str(CS_EPS3))
            # self.ui.comboBox_2.setCurrentIndex(1)
        elif CS == 'Isotropy' :
            self.ui.lineEdit_00.show()
            self.ui.lineEdit_04.hide()
            self.ui.lineEdit_05.hide()
            self.ui.lineEdit_00.setText(str(CS_EPS))
            # self.ui.lineEdit_04.setText(str(CS_EPS))
            # self.ui.lineEdit_05.setText(str(CS_EPS))
            # self.ui.comboBox_2.setCurrentIndex(0)
        else:
            # self.ui.comboBox_2.setCurrentIndex(2)
            self.ui.lineEdit_00.hide()
            self.ui.lineEdit_04.hide()
            self.ui.lineEdit_05.hide()
        # value_CS=self.ui.comboBox_2.currentText()
        # if value_CS == 'true':
        #     self.ui.lineEdit_00.setEnabled(True)
        # else :
        #     self.ui.lineEdit_00.setEnabled(False)
    def setAttributetoObj(self):
        CS = self.ui.comboBox_2.currentText()
        if CS == 'Anisotropy':
            # self.obj.ConductivitySIGMA = 'Anisotropy'
            try:
                self.obj.ConductivitySIGMA = 'Anisotropy'
                CS_Value = self.ui.lineEdit_00.text()
                CS_Value2 = self.ui.lineEdit_04.text()
                CS_Value3 = self.ui.lineEdit_05.text()
                self.obj.CS_SetEPS = float(CS_Value)
                self.obj.CS_SetEPS2 = float(CS_Value2)
                self.obj.CS_SetEPS3 = float(CS_Value3)
            except:
                pass
        elif CS == 'Isotropy':
            # self.obj.ConductivitySIGMA = 'Isotropy'
            try:
                self.obj.ConductivitySIGMA = 'Isotropy'
                CS_Value = self.ui.lineEdit_00.text()
                self.obj.CS_SetEPS = float(CS_Value)
            except:
                pass
        else :
            try:
                self.obj.ConductivitySIGMA = 'NotDefine'
            except:
                pass

        RDC = self.ui.comboBox_3.currentText()
        if RDC == 'Anisotropy':
            self.obj.RelativeDielectricConstant = 'Anisotropy'
            EPS = self.ui.lineEdit_01.text()
            EPS2 = self.ui.lineEdit_02.text()
            EPS3 = self.ui.lineEdit_03.text()
            try:
                self.obj.SetEPS = float(EPS)
                self.obj.SetEPS2 = float(EPS2)
                self.obj.SetEPS3 = float(EPS3)
            except:
                pass
        elif RDC == 'Isotropy':
            self.obj.RelativeDielectricConstant = 'Isotropy'
            EPS = self.ui.lineEdit_01.text()
            try:
                self.obj.SetEPS = float(EPS)
            except:
                pass
        else :
            self.obj.RelativeDielectricConstant = 'NotDefine'
        pass
###############################  设置与Mark相关的函数 ##########################################
 #添加新的mark
    def setMarkUi(self):
        #第一排
        self.ui.checkBoxMark_1 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_1.setChecked(False)
        self.ui.checkBoxMark_1.setObjectName("checkBoxMark_1")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_1, 3, 1, 1, 1)
        self.ui.checkBoxMark_1.setText(QtGui.QApplication.translate("Dialog", "MINMUM", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.checkBoxMark_2 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_2.setChecked(False)
        self.ui.checkBoxMark_2.setObjectName("checkBoxMark_2")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_2, 3, 2, 1, 1)
        self.ui.checkBoxMark_2.setText(QtGui.QApplication.translate("Dialog", "MINMUM", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.checkBoxMark_3 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_3.setChecked(False)
        self.ui.checkBoxMark_3.setObjectName("checkBoxMark_3")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_3, 3, 3, 1, 1)
        self.ui.checkBoxMark_3.setText(QtGui.QApplication.translate("Dialog", "MINMUM", None, QtGui.QApplication.UnicodeUTF8))

        #第二排
        self.ui.checkBoxMark_4 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_4.setChecked(False)
        self.ui.checkBoxMark_4.setObjectName("checkBoxMark_4")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_4, 4, 1, 1, 1)
        self.ui.checkBoxMark_4.setText(QtGui.QApplication.translate("Dialog", "MIDMUM", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.checkBoxMark_5 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_5.setChecked(False)
        self.ui.checkBoxMark_5.setObjectName("checkBoxMark_5")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_5, 4, 2, 1, 1)
        self.ui.checkBoxMark_5.setText(QtGui.QApplication.translate("Dialog", "MIDMUM", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.checkBoxMark_6 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_6.setChecked(False)
        self.ui.checkBoxMark_6.setObjectName("checkBoxMark_6")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_6, 4, 3, 1, 1)
        self.ui.checkBoxMark_6.setText(QtGui.QApplication.translate("Dialog", "MIDMUM", None, QtGui.QApplication.UnicodeUTF8))

        #第三排
        self.ui.checkBoxMark_7 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_7.setChecked(False)
        self.ui.checkBoxMark_7.setObjectName("checkBoxMark_7")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_7, 5, 1, 1, 1)
        self.ui.checkBoxMark_7.setText(QtGui.QApplication.translate("Dialog", "MAXMUM", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.checkBoxMark_8 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_8.setChecked(False)
        self.ui.checkBoxMark_8.setObjectName("checkBoxMark_8")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_8, 5, 2, 1, 1)
        self.ui.checkBoxMark_8.setText(QtGui.QApplication.translate("Dialog", "MAXMUM", None, QtGui.QApplication.UnicodeUTF8))

        self.ui.checkBoxMark_9 = QtGui.QCheckBox(self.ui.groupBox_3)
        self.ui.checkBoxMark_9.setChecked(False)
        self.ui.checkBoxMark_9.setObjectName("checkBoxMark_9")
        self.ui.gridLayout.addWidget(self.ui.checkBoxMark_9, 5, 3, 1, 1)
        self.ui.checkBoxMark_9.setText(QtGui.QApplication.translate("Dialog", "MAXMUM", None, QtGui.QApplication.UnicodeUTF8))
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
        
    def setMark(self):
        '''
        设置Mark的状态到obj
        '''
        mark_x_bool = self.ui.checkBox.isChecked()
        mark_y_bool = self.ui.checkBox_2.isChecked()
        mark_z_bool = self.ui.checkBox_3.isChecked()
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            if mark_x_bool:
                self.obj.X=True
            else:
                self.obj.X=False
            if mark_y_bool:
                self.obj.Y=True
            else:
                self.obj.Y=False
            if mark_z_bool:
                self.obj.Z=True
            else:
                self.obj.Z=False
        else:
            if mark_x_bool:
                self.obj.R=True
            else:
                self.obj.R=False
            if mark_y_bool:
                self.obj.Theta=True
            else:
                self.obj.Theta=False
            if mark_z_bool:
                self.obj.Z=True
            else:
                self.obj.Z=False
    def setExtraMark(self):
        '''
        为mark的添加额外的控制部分，主要用来操作min，mid，max
        '''
        try:
            # if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            if True:
                # FreeCAD.Console.PrintError("\n进入执行set mark 的操作")
                self.obj.min_1 = self.ui.checkBoxMark_1.isChecked()
                self.obj.mid_1 = self.ui.checkBoxMark_4.isChecked()
                self.obj.max_1 = self.ui.checkBoxMark_7.isChecked()
                self.obj.min_2 = self.ui.checkBoxMark_2.isChecked()
                self.obj.mid_2 = self.ui.checkBoxMark_5.isChecked()
                self.obj.max_2 = self.ui.checkBoxMark_8.isChecked()
                self.obj.min_3 = self.ui.checkBoxMark_3.isChecked()
                self.obj.mid_3 = self.ui.checkBoxMark_6.isChecked()
                self.obj.max_3 = self.ui.checkBoxMark_9.isChecked()
                # FreeCAD.Console.PrintError("\n执行完set mark 的操作")
        except:
            pass



    def settingMarkInitialValues(self):
        '''
        设置Mark_Value的初始值
        '''
        # 新添加识别数字的功能
        # self.step_value = GetWorkSpaceStepList()
        list1 = self.obj.ExpressionEngine
        list2 = ['', '', '']
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            for x in range(len(list1)):
                if list1[x][0] == 'X_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[0] = list1[x][1].replace('Param.', '')
                    else:
                        list2[0] = self.obj.X_Value.UserString
                elif list1[x][0] == 'Y_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[1] = list1[x][1].replace('Param.', '')
                    else:
                        list2[1] = self.obj.Y_Value.UserString
                elif list1[x][0] == 'Z_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[2] = list1[x][1].replace('Param.', '')
                    else:
                        list2[2] = self.obj.Z_Value.UserString
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            for x in range(len(list1)):
                if list1[x][0] == 'R_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[0] = list1[x][1].replace('Param.', '')
                    else:
                        list2[0] = self.obj.R_Value.UserString
                elif list1[x][0] == 'Theta_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[1] = list1[x][1].replace('Param.', '')
                    else:
                        list2[1] = self.obj.Theta_Value.UserString
                elif list1[x][0] == 'Z_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[2] = list1[x][1].replace('Param.', '')
                    else:
                        list2[2] = self.obj.Z_Value.UserString
        else :
            for x in range(len(list1)):
                if list1[x][0] == 'Z_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[0] = list1[x][1].replace('Param.','')
                    else:
                        list2[0] = self.obj.Z_Value.UserString
                elif list1[x][0] == 'R_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[1] = list1[x][1].replace('Param.','')
                    else:
                        list2[1] = self.obj.R_Value.UserString
                elif list1[x][0] == 'Theta_Value':
                    if re.search(r'Param.',list1[x][1]):
                        list2[2] = list1[x][1].replace('Param.','')
                    else:
                        list2[2] = self.obj.Theta_Value.UserString


        self.ui.NUG_lineEdit.setText(list2[0])
        self.ui.NUG_lineEdit_2.setText(list2[1])
        self.ui.NUG_lineEdit_3.setText(list2[2])


    def setMarkValue(self):
        '''
        设置Mark的Value的值
        '''
        from Modeling.Common.Tools import InputTools
        mark_x_bool = self.ui.checkBox.isChecked()
        mark_y_bool = self.ui.checkBox_2.isChecked()
        mark_z_bool = self.ui.checkBox_3.isChecked()

        Fx = self.ui.NUG_lineEdit.text()
        Fy = self.ui.NUG_lineEdit_2.text()
        Fz = self.ui.NUG_lineEdit_3.text()

        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            if mark_x_bool:
                Fx_1 = InputTools.Stringfunctions(Fx)
                try:
                    self.obj.setExpression('X_Value',None)
                    self.obj.setExpression('X_Value', str(Fx_1[0]))
                except:
                     self.error=self.error+'Mark.X'+'  '+str(Fx)+'\n'
            if mark_y_bool:
                Fy_1 = InputTools.Stringfunctions(Fy)
                try:
                    self.obj.setExpression('Y_Value', None)
                    self.obj.setExpression('Y_Value', str(Fy_1[0]))
                except:
                     self.error=self.error+'Mark.Y'+'  '+str(Fy)+'\n'
            if mark_z_bool:
                Fz_1 = InputTools.Stringfunctions(Fz)
                try:
                    self.obj.setExpression('Z_Value', None)
                    self.obj.setExpression('Z_Value', str(Fz_1[0]))
                except:
                    self.error=self.error+'Mark.Z'+'  '+str(Fz)+'\n'
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            if mark_x_bool:
                Fx_1 = InputTools.Stringfunctions(Fx)
                try:
                    self.obj.setExpression('R_Value', None)
                    self.obj.setExpression('R_Value', str(Fx_1[0]))
                except:
                    self.error=self.error+'Mark.R'+'  '+str(Fx)+'\n'
            if mark_y_bool:
                Fy_1 = InputTools.anglefunctions(Fy)
                try:
                    self.obj.setExpression('Theta_Value', None)
                    self.obj.setExpression('Theta_Value', str(Fy_1[0]))
                except:
                    self.error=self.error+'Mark.Theta'+'  '+str(Fy)+'\n'
            if mark_z_bool:
                Fz_1 = InputTools.Stringfunctions(Fz)
                try:
                    self.obj.setExpression('Z_Value', None)
                    self.obj.setExpression('Z_Value', str(Fz_1[0]))
                except:
                    self.error=self.error+'Mark.Z'+'  '+str(Fz)+'\n'
        else:
            if mark_x_bool:
                Fx_1 = InputTools.Stringfunctions(Fx)
                try:
                    self.obj.setExpression('Z_Value', None)
                    self.obj.setExpression('Z_Value', str(Fx_1[0]))
                except:
                    self.error=self.error+'Mark.Z'+'  '+str(Fx)+'\n'
            if mark_y_bool:
                Fy_1 = InputTools.Stringfunctions(Fy)
                try:
                    self.obj.setExpression('R_Value', None)
                    self.obj.setExpression('R_Value', str(Fy_1[0]))
                except:
                    self.error=self.error+'Mark.R'+'  '+str(Fy)+'\n'
            if mark_z_bool:
                Fz_1 = InputTools.anglefunctions(Fz)
                try:
                    self.obj.setExpression('Theta_Value', None)
                    self.obj.setExpression('Theta_Value', str(Fz_1[0]))
                except:
                    self.error=self.error+'Mark.Theta'+'  '+str(Fz)+'\n'
###############################  设置与Position相关的函数 ##########################################            
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

            pass
    def settheLocation(self):
        # import InputTools
        # FreeCAD.Console.PrintMessage('setlocation')
        from Modeling.Common.Tools import InputTools
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            point_1_x_before=self.ui.lineEdit.text()
            point_1_x_after=InputTools.Stringfunctions(point_1_x_before)
            try:
                if point_1_x_after[1]==2:
                    self.obj.setExpression('Point_1.x',point_1_x_after[0])
                    
                else:
                    self.obj.Point_1.x=point_1_x_after[0]
            except:

                self.error=self.error+'Point_1.x'+'  '+str(point_1_x_before)+'\n'

            point_1_y_before=self.ui.lineEdit_2.text()
            point_1_y_after=InputTools.Stringfunctions(point_1_y_before)
            try:
                if point_1_y_after[1]==2:
                    self.obj.setExpression('Point_1.y',point_1_y_after[0])
                else:
                    self.obj.Point_1.y=point_1_y_after[0]
            except:
                self.error=self.error+'Point_1.y'+'  '+str(point_1_y_before)+'\n'

            point_1_z_before=self.ui.lineEdit_3.text()
            point_1_z_after=InputTools.Stringfunctions(point_1_z_before)
            try:
                if point_1_z_after[1]==2:
                    self.obj.setExpression('Point_1.z',point_1_z_after[0])
                else:
                    self.obj.Point_1.z=point_1_z_after[0]
            except:
                self.error=self.error+'Point_1.z'+'  '+str(point_1_z_before)+'\n'
        
            point_2_x_before=self.ui.lineEdit_4.text()
            point_2_x_after=InputTools.Stringfunctions(point_2_x_before)
            try:
                if point_2_x_after[1]==2:
                    self.obj.setExpression('Point_2.x',point_2_x_after[0])
                else:
                    self.obj.Point_2.x=point_2_x_after[0]
            except:
                self.error=self.error+'Point_2.x'+'  '+str(point_2_x_before)+'\n'

            point_2_y_before=self.ui.lineEdit_5.text()
            point_2_y_after=InputTools.Stringfunctions(point_2_y_before)
            try:
                if point_2_y_after[1]==2:
                    self.obj.setExpression('Point_2.y',point_2_y_after[0])
                else:
                    self.obj.Point_2.y=point_2_y_after[0]
            except:
                self.error=self.error+'Point_2.y'+'  '+str(point_2_y_before)+'\n'

            point_2_z_before=self.ui.lineEdit_6.text()
            point_2_z_after=InputTools.Stringfunctions(point_2_z_before)
            try:
                if point_2_z_after[1]==2:
                    self.obj.setExpression('Point_2.z',point_2_z_after[0])
                else:
                    self.obj.Point_2.z=point_2_z_after[0]
            except:
                self.error=self.error+'Point_2.z'+'  '+str(point_2_z_before)+'\n'
                
            point_r_before=self.ui.lineEdit_7.text()
            point_r_after=InputTools.Stringfunctions(point_r_before)
            try:
                if point_r_after[1]==2:
                    self.obj.setExpression('Radius',point_r_after[0])
                else:
                    self.obj.Radius=point_r_after[0]
            except:
                self.error=self.error+'Radius'+'  '+str(point_r_before)+'\n'
        else:
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

            point_r_before=self.ui.lineEdit_7.text()
            point_r_after=InputTools.Stringfunctions(point_r_before)
            try:
                if point_r_after[1]==2:
                    self.obj.setExpression('Radius',point_r_after[0])
                else:
                    self.obj.Radius=point_r_after[0]
            except:
                self.error=self.error+'Radius'+'  '+str(point_r_before)+'\n'

            pass
###############################  设置与Error相关的函数 ##########################################         
    def controlboolupdate(self,is_show):
        '''
        该函数用来控制是否进行布尔运算，当满足以下条件时进行布尔运算：\n
        1.order发生改变
        2.attribute发生改变
        3.坐标发生变化，并且attribute不是NotDefine
        '''
        if self.fin_Order != self.order_before:
            #PartGui.updateBoolean(self.fin_Order)
            PartGui.updateBoolean(self.fin_Order, is_show)
            return
        if self.obj.Attribute != self.attribute_before :
            #PartGui.updateBoolean(self.fin_Order)
            PartGui.updateBoolean(self.fin_Order, is_show)
            return
        if self.recompute_flag and self.obj.Attribute != 'NotDefine':
            #PartGui.updateBoolean(self.fin_Order)
            PartGui.updateBoolean(self.fin_Order, is_show)
            return
        FreeCAD.Console.PrintError('\n没有进行布尔运算')

    def closeDialog(self):
        FreeCAD.Console.PrintError('\nclose\n')
        t1 = time.time()
        try:
            self.fin_Order = int(self.ui.Base_lineEdit_2.value())
        except:
            pass
        if len(self.error)==0:
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
            # FreeCAD.ActiveDocument.recompute()
            t3 = time.time()
            FreeCAD.Console.PrintMessage('test1######\n')
            if hasattr(self.obj,'Attribute'):
                self.controlboolupdate(is_show)
            else:
                FreeCAD.Console.PrintError('\n由于没有attribute的原因跳过布尔运算')
            # PartGui.updateBoolean(self.fin_Order)
            self.obj_resultshape.ViewObject.Transparency = 0
            self.obj.ViewObject.Visibility = False
            # self.obj_resultshape.ViewObject.ShapeColor = (0.58, 0.58, 0.58)
            self.obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
            Common.Tools.ObjectsTools.setFitViewOfObject(self.obj)
            self.obj_resultshape.ViewObject.Transparency = 85
            self.obj.ViewObject.Visibility = True
            FreeCAD.Console.PrintMessage('test1!!!!!\n'+str(self.obj_resultshape.ViewObject.Transparency))
            t4 = time.time()
            # self.ui.lineEdit._completer.popup().hide()
            self.close()
            FreeCAD.Console.PrintMessage('test1@@@@@@@\n')
            t5 = time.time()
            FreeCAD.Console.PrintMessage('hide time'+str(t2-t1)+'\n')
            FreeCAD.Console.PrintMessage('recompute time'+str(t3-t2)+'\n')
            FreeCAD.Console.PrintMessage('updateboolean time'+str(t4-t3)+'\n')
            FreeCAD.Console.PrintMessage('close time'+str(t5-t4)+'\n')
            FreeCAD.Console.PrintMessage('all time'+str(t5-t1)+'\n')
            # @fubiao
            import ObjectsTools as objTools
            objTools.checkVolShape(self.obj)
            FreeCAD.Console.PrintError('\n执行完close语句\n')
            
    def showWarningDialog(self):
        if len(self.error)!=0:
            import ErrorFunction
            err_dia=ErrorFunction.ErrorDialog.WarningDialog()
            err_dia.errormassageinput(self.error)
            err_dia.show()
            err_dia.exec_()
            self.error=''
        pass
###############################  设置与OK,Cancel相关的函数 ########################################## 
    def deleteobj(self):
        doc = FreeCAD.ActiveDocument
        doc.removeObject(self.obj.Name)
        pass
###############################  设置与ReShowDialog相关的类 ##########################################
class reshowObjDialog(showObjDialog):

    def setDefaultValue(self):
        # import InputTools
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','']
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
                elif list1[i][0] == 'Radius':
                    str1=list1[i][1].replace('Param.','')
                    list2[6]=str1
            
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
                        # number = filter(str.isdigit,  str(self.obj.Radius))
                        list2[x]=str(ValueUnitslength(float(self.obj.Radius.Value),length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
            self.ui.lineEdit_7.setText(list2[6])
        else:
            list1=self.obj.ExpressionEngine
            list2=['','','','','','','']
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
                elif list1[i][0] == 'Radius':
                    str1=list1[i][1].replace('Param.','')
                    list2[6]=str1
                
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
                        # number = filter(str.isdigit,  str(self.obj.Radius))
                        list2[x]=str(ValueUnitslength(float(self.obj.Radius.Value),length))+length

            self.ui.lineEdit.setText(list2[0])
            self.ui.lineEdit_2.setText(list2[1])
            self.ui.lineEdit_3.setText(list2[2])
            self.ui.lineEdit_4.setText(list2[3])
            self.ui.lineEdit_5.setText(list2[4])
            self.ui.lineEdit_6.setText(list2[5])
            self.ui.lineEdit_7.setText(list2[6])
###############################  工具类函数相关的函数 ##########################################           
#重新获取obj时做单位的转换
def ValueUnitslength(num1,units):
    if units == 'mm':
        num1=num1*1000
    elif units == 'cm':
        num1=num1*100
    elif units == 'm':
        num1=num1
    # FreeCAD.Console.PrintMessage(str(num1)+'\n')
    return num1
def ValueUnitsangle(num1,units):
    if units == 'deg':
        num1=num1
    elif units == 'rad':
        num1=num1*180/pi
    return num1 

#获取工作区的步长   
def GetWorkSpaceStepList():
    # step_list=ProjectSettingDlgData.getDlgData()
    step_list=ProjectSetting.Commands.ProjectSettingsDlgData.getDlgData()
    if not FreeCAD.ActiveDocument.CoordinateSystem =='Cylindrical':
        step_x_u=step_list[0][1][1][2]
        step_y_u=step_list[0][1][2][2]
        step_z_u=step_list[0][1][3][2]
        step_x_n=getNumberfromUnicode(step_x_u)
        step_y_n=getNumberfromUnicode(step_y_u)
        step_z_n=getNumberfromUnicode(step_z_u)

        x_n=step_x_n[0].encode('utf-8')
        y_n=step_y_n[0].encode('utf-8')
        z_n=step_z_n[0].encode('utf-8')
        result=[x_n,y_n,z_n]
        return result
    else:
        step_x_u=step_list[4][1][1][2]
        step_y_u=step_list[4][1][2][2]
        step_z_u=step_list[4][1][3][2]
        step_x_n=getNumberfromUnicode(step_x_u)
        step_y_n=getNumberfromUnicode(step_y_u)
        step_z_n=getNumberfromUnicode(step_z_u)

        x_n=step_x_n[0].encode('utf-8')
        y_n=step_y_n[0].encode('utf-8')
        z_n=step_z_n[0].encode('utf-8')
        result=[x_n,y_n,z_n]
        return result
def getNumberfromUnicode(string):
    # string="A1.45，b5，6.45，8.82"
    result=re.findall(r"\d+\.?\d*",string)
    return result
def isNumber(n):
    result=True
    try:
        num=float(n)
        result = num == num
    except :
        result=False
    return result
def getGlobalVar():
    import Modeling
    GlobalVariablelist=Modeling.Common.Tools.ModelingCommandForM3dFile.getGlobalVariable()
    list1=[]
    for x in GlobalVariablelist:
        list1.append(x[0])
    list1.append('DX1')
    list1.append('DX2')
    list1.append('DX3')
    return list1