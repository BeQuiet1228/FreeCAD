#-*- coding: utf-8 -*-
from Modeling.Common.Tools.BaseObjDialog import *
import PolygonalDialog
import ItemDialog
from PySide import QtGui
from Modeling import Common
import FreeCAD
import ProjectSetting
import re
import PySide
# 放在listWedgit里面的控件
class subForm(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.ui = ItemDialog.Ui_Form()
        self.ui.setupUi(self)

class showPolygonalDialog(showObjDialog):
    def __init__(self, obj, parent=None):
        #手动调用父类构造函数。
        showObjDialog.__init__(self,obj,parent)
        #设置ui文件
        self.ui = PolygonalDialog.Ui_Dialog()
        self.ui.setupUi(self)
        #初始化对话框
        self.initDialog()
        # 将obj设置为类成员
        self.obj = obj
        # 用来管理报错功能的字符串，只要字符串非空最后就会报错
        self.error = ''
        # 此变量用来存放已经有多少个subWidget
        self.subWidgetNumbers = 0
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        screen = QtGui.QDesktopWidget().screenGeometry()
        self.move(screen.right()-self.size().width()-150, screen.bottom()*0.5-200)
        self.DisplayMode()
        # 设置ui
        self.setUI()

    def setUI(self):
        # 添加mark的补充部分
        self.setMarkUi()
        self.ui.OK_pushButton.clicked.connect(self.setExtraMark)
        self.setDialog()

        # 设置初始化的label
        self.setDefaultLabel()
        # 设置Label
        self.ui.OK_pushButton.clicked.connect(self.setLabel)

        # 设置Order
        self.setOrder()
        # 设置物体order，以及排序
        self.ui.OK_pushButton.clicked.connect(self.OrderChanged)

        # 设置Mark真假
        self.setDefaultMark()
        self.ui.OK_pushButton.clicked.connect(self.setMark)
        # 设置Mark初始值，为工作区的步长
        self.settingMarkInitialValues()
        # 设置到物体的Mark的值
        self.ui.OK_pushButton.clicked.connect(self.setMarkValue)

        # 设置显示点个数的ui
        self.ui.listWidget.setViewMode(QtGui.QListView.ListMode)
        # 注意此处仅需要调用setDialogNumber即可，具体的设置界面有subwid的个数在此函数中已经被调用
        self.setDialogNumber()
        self.ui.spinBox_num.valueChanged.connect(self.setPointNum)
        # 设置点的初始坐标
        self.setDeafultLineeditDialog()
        # self.setDefaultValue()
        # 设置点的坐标
        self.ui.OK_pushButton.clicked.connect(self.setPointLocaToObj)
        
        # 显示错误信息
        self.ui.OK_pushButton.clicked.connect(self.closeDialog)
        self.ui.OK_pushButton.clicked.connect(self.showWarningDialog)

        # 点击取消删除该物体
        self.ui.Cancel_pushButton.clicked.connect(self.deleteobj)
        # 点击取消关闭对话框
        self.ui.Cancel_pushButton.clicked.connect(self.close)
    def setDeafultLineeditDialog(self):
        '''
        在子类中调用，在这里为纯虚函数
        '''
        pass
    def setDefaultMark(self): 
        self.ui.checkBox.setCheckState(QtCore.Qt.CheckState.Unchecked)    
        self.ui.checkBox_2.setCheckState(QtCore.Qt.CheckState.Unchecked)   
        self.ui.checkBox_3.setCheckState(QtCore.Qt.CheckState.Unchecked)
    def setDialogNumber(self):
        '''
        设置点的数量到Dialog
        '''
        num = int(self.obj.NumbersOfPoints)
        self.ui.spinBox_num.setValue(num)
        self.setPointNum()
    def setPointNum(self):
        '''
        该函数的作用设置点的数量，如果要修改点的个数调用该函数
        '''
        num = int(self.ui.spinBox_num.value())
        self.createSubWidget(num)
    def createSubWidget(self, subWidget_number):
        '''
        批量创建子控件并添加到listWidget,不应该直接调用该函数
        '''
        # 注意此处需要更新obj的点的个数，否则在设置坐标时会出现异常
        self.obj.NumbersOfPoints = subWidget_number
        # 当subWidget_number < self.subWidgetNumbers时
        # 删除self.subWidgetNumbers - subWidget_number次的最后一个小控件
        if subWidget_number < self.subWidgetNumbers:
            for i in range(self.subWidgetNumbers - subWidget_number):
                self.ui.listWidget.takeItem(self.ui.listWidget.count() - 1)
            # 更新小控件的个数
            self.subWidgetNumbers = subWidget_number
            return

        # 当subWidget_number = self.subWidgetNumbers时, 什么都不做直接退出
        if subWidget_number == self.subWidgetNumbers:
            return 

        # 当subWidget_number > self.subWidgetNumbers时
        if subWidget_number > self.subWidgetNumbers:
            for i in range(subWidget_number - self.subWidgetNumbers):
                # 创建subForm对象
                tempSub = subForm(self)
                tempSub.ui.label_10.setText('Point' + str(self.subWidgetNumbers + i + 1) + ':')
                # 为小控件的lineEdit设置默认值
                self.setDefaultNumberToSubWidget(tempSub)
                # 为小控件的lineEdit设置自动填充功能
                tempSub.ui.lineEdit.setcompleterlist(getGlobalVar())
                tempSub.ui.lineEdit_2.setcompleterlist(getGlobalVar())
                tempSub.ui.lineEdit_3.setcompleterlist(getGlobalVar())
                # 创建临时WidItem
                tempWidItem = PySide.QtGui.QListWidgetItem()
                # 在这里控制小控件每一行的长宽
                tempWidItem.setSizeHint(PySide.QtCore.QSize(200, 45))
                # 向listWidget添加item的固定调用方法为一下两行
                self.ui.listWidget.addItem(tempWidItem)
                self.ui.listWidget.setItemWidget(tempWidItem, tempSub)
            # 更新小控件的个数
            self.subWidgetNumbers = subWidget_number
            return
    # def dasdas(self):
    #     subWidget111 = self.ui.listWidget.itemWidget(itemFromIndex())
    def setDefaultNumberToSubWidget(self, subWid):
        '''
        向传进来的subWidget设置默认值，分三个坐标系设置
        '''
        from Modeling.Common.Tools import InputTools
        length=InputTools.currentLengthUnits()
        angle=InputTools.currentAngleUnits()
        if FreeCAD.ActiveDocument.CoordinateSystem=="Rectangular":
            if length =='mm':
                str_1 ='0'+length
            elif length == 'cm':
                str_1 = '0'+length
            elif length == 'm':
                str_1 = '0'+length
            subWid.ui.lineEdit.setText(str_1)
            subWid.ui.lineEdit_2.setText(str_1)
            subWid.ui.lineEdit_3.setText(str_1)
        elif FreeCAD.ActiveDocument.CoordinateSystem=="Polar":
            if length =='mm':
                str_z1 ='0'+length
            elif length == 'cm':
                str_z1 = '0'+length
            elif length == 'm':
                str_z1 = '0'+length
            if angle == 'deg':
                str_theta = '0'+angle
            else :
                str_theta = '0'+angle
            subWid.ui.lineEdit.setText(str_z1)
            subWid.ui.lineEdit_2.setText(str_theta)
            subWid.ui.lineEdit_3.setText(str_z1)
        else:
            if length =='mm':
                str_z1 ='0'+length
            elif length == 'cm':
                str_z1 = '0'+length
            elif length == 'm':
                str_z1 = '0'+length
            if angle == 'deg':
                str_theta = '0'+angle
            else :
                str_theta = '0'+angle
            subWid.ui.lineEdit.setText(str_z1)
            subWid.ui.lineEdit_2.setText(str_z1)
            subWid.ui.lineEdit_3.setText(str_theta)
    def setPointLocaToObj(self):
        '''
        将点坐标设置到obj里面去
        '''
        for i in range(self.subWidgetNumbers):
            self.setSinglePointToObj(i)
        pass
    def setSinglePointToObj(self, index):
        '''
        说明： index表示当前正在处理的point的索引-1
        obj本身是不用被传递进来的，仅需传递subWid的索引，以及当前想要传递哪个点的坐标到obj
        '''
        # 仅在小于小控件个数的时候才有效，不过一般都是有效的，添加判断防止出现异常
        if index < self.subWidgetNumbers:
            # FreeCAD.Console.PrintError("\n进入赋值判断语句")
            # 想获取Widget必须通过以下两行代码的方式来获取，注意区分Item和Widget的区别
            tempItem = self.ui.listWidget.item(index)
            tempSubWid = self.ui.listWidget.itemWidget(tempItem)
            from Modeling.Common.Tools import InputTools
            FreeCAD.Console.PrintError("\n坐标系:\t" + str(FreeCAD.ActiveDocument.CoordinateSystem))
            # 直角坐标系下的赋值
            if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
                # x
                point_index_x_before = tempSubWid.ui.lineEdit.text()
                point_index_x_after = InputTools.Stringfunctions(point_index_x_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".x", str(point_index_x_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t X error:\t" + point_index_x_before + "\n"
                # y
                point_index_y_before = tempSubWid.ui.lineEdit_2.text()
                point_index_y_after = InputTools.Stringfunctions(point_index_y_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".y", str(point_index_y_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t X error:\t" + point_index_y_before + "\n"
                # z
                point_index_z_before = tempSubWid.ui.lineEdit_3.text()
                point_index_z_after = InputTools.Stringfunctions(point_index_z_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".z", str(point_index_z_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t X error:\t" + point_index_z_before + "\n"
            elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
                # r
                point_index_x_before = tempSubWid.ui.lineEdit.text()
                point_index_x_after = InputTools.Stringfunctions(point_index_x_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".x", str(point_index_x_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t R error:\t" + point_index_x_before + "\n"
                # theta
                point_index_y_before = tempSubWid.ui.lineEdit_2.text()
                point_index_y_after = InputTools.anglefunctions(point_index_y_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".y", str(point_index_y_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t theta error:\t" + point_index_y_before + "\n"
                # z
                point_index_z_before = tempSubWid.ui.lineEdit_3.text()
                point_index_z_after = InputTools.Stringfunctions(point_index_z_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".z", str(point_index_z_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t Z error:\t" + point_index_z_before + "\n"
            else:
                # z
                point_index_x_before = tempSubWid.ui.lineEdit.text()
                point_index_x_after = InputTools.Stringfunctions(point_index_x_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".z", str(point_index_x_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t Z error:\t" + point_index_x_before + "\n"
                # r
                point_index_y_before = tempSubWid.ui.lineEdit_2.text()
                point_index_y_after = InputTools.Stringfunctions(point_index_y_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".x", str(point_index_y_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t R error:\t" + point_index_y_before + "\n"
                # theta
                point_index_z_before = tempSubWid.ui.lineEdit_3.text()
                point_index_z_after = InputTools.anglefunctions(point_index_z_before)
                try:
                    self.obj.setExpression("Point" + str(index + 1) + ".y", str(point_index_z_after[0]))
                except BaseException:
                    self.error = self.error + "Point" + str(index + 1) + "\t theta error:\t" + point_index_z_before + "\n"
            pass
class reshowPolygonalDialog(showPolygonalDialog):
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
    def deleteobj(self):
        pass
    def setDeafultLineeditDialog(self):
        '''
        设置打开Dialog时候的默认值
        '''
        # 首先获取obj的点坐标，并通过相关的list生成对应的字典结构，方便赋值调用
        list1 = self.obj.ExpressionEngine
        # 存放数据的字典
        data_dict = {}
        for i in list1:
            data_dict[i[0]] = i[1]
        # 依次获取小控件，并通过查询字典来赋值
        from Modeling.Common.Tools import InputTools
        length = InputTools.currentLengthUnits()
        angle = InputTools.currentAngleUnits()
        # 直角坐标系下设置默认值
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            for i in range(self.subWidgetNumbers):
                tempItem = self.ui.listWidget.item(i)
                tempSubWid = self.ui.listWidget.itemWidget(tempItem)
                # x------------------------------------------------------------
                # 如果在keys里面说明是一个变量
                if "Point" + str(i + 1) + ".x" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".x"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).x
                        tempStr = str(ValueUnitslength(tempStr, length)) + length
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).x
                    tempStr = str(ValueUnitslength(tempStr, length)) + length
                    tempSubWid.ui.lineEdit.setText(tempStr)
                # y---------------------------------------------------------
                if "Point" + str(i + 1) + ".y" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".y"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).y
                        tempStr = str(ValueUnitslength(tempStr, length)) + length
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit_2.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).y
                    tempStr = str(ValueUnitslength(tempStr, length)) + length
                    tempSubWid.ui.lineEdit_2.setText(tempStr)
                # z----------------------------------------------------------
                if "Point" + str(i + 1) + ".z" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".z"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).z
                        tempStr = str(ValueUnitslength(tempStr, length)) + length
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit_3.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).z
                    tempStr = str(ValueUnitslength(tempStr, length)) + length
                    tempSubWid.ui.lineEdit_3.setText(tempStr)
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            for i in range(self.subWidgetNumbers):
                tempItem = self.ui.listWidget.item(i)
                tempSubWid = self.ui.listWidget.itemWidget(tempItem)
                # r----------------------------------------------------------
                # 如果在keys里面说明是一个变量
                if "Point" + str(i + 1) + ".x" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".x"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).x
                        tempStr = str(ValueUnitslength(tempStr, length)) + length
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).x
                    tempStr = str(ValueUnitslength(tempStr, length)) + length
                    tempSubWid.ui.lineEdit.setText(tempStr)
                # theta---------------------------------------------------------
                if "Point" + str(i + 1) + ".y" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".y"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).y
                        tempStr = str(ValueUnitslength(tempStr, angle)) + angle
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit_2.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).y
                    tempStr = str(ValueUnitslength(tempStr, angle)) + angle
                    tempSubWid.ui.lineEdit_2.setText(tempStr)
                # z-----------------------------------------------------
                if "Point" + str(i + 1) + ".z" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".z"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).z
                        tempStr = str(ValueUnitslength(tempStr, length)) + length
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit_3.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).z
                    tempStr = str(ValueUnitslength(tempStr, length)) + length
                    tempSubWid.ui.lineEdit_3.setText(tempStr)
        else:
            for i in range(self.subWidgetNumbers):
                tempItem = self.ui.listWidget.item(i)
                tempSubWid = self.ui.listWidget.itemWidget(tempItem)
                # z----------------------------------------------------------
                # 如果在keys里面说明是一个变量
                if "Point" + str(i + 1) + ".z" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".z"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).z
                        tempStr = str(ValueUnitslength(tempStr, length)) + length
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).z
                    tempStr = str(ValueUnitslength(tempStr, length)) + length
                    tempSubWid.ui.lineEdit.setText(tempStr)
                # r---------------------------------------------------------
                if "Point" + str(i + 1) + ".x" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".x"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).x
                        tempStr = str(ValueUnitslength(tempStr, length)) + length
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit_2.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).x
                    tempStr = str(ValueUnitslength(tempStr, length)) + length
                    tempSubWid.ui.lineEdit_2.setText(tempStr)
                # theta-----------------------------------------------------
                if "Point" + str(i + 1) + ".y" in data_dict.keys():
                    tempStr = data_dict["Point" + str(i + 1) + ".y"]
                    if "Param." in tempStr:
                        tempStr = tempStr.replace('Param.','')
                    # 如果"Param."不在tempStr里面说明他是一个浮点型数据，为了避免出现浮点过长的情况，在这里做一定的处理
                    else:
                        tempStr = getattr(self.obj, "Point" + str(i + 1)).y
                        tempStr = str(ValueUnitslength(tempStr, angle)) + angle
                    # 将解析后的字符串添加到Dialog
                    tempSubWid.ui.lineEdit_3.setText(tempStr)
                # 如果不在说明是一个整型
                else:
                    tempStr = getattr(self.obj, "Point" + str(i + 1)).y
                    tempStr = str(ValueUnitslength(tempStr, angle)) + angle
                    tempSubWid.ui.lineEdit_3.setText(tempStr)

        