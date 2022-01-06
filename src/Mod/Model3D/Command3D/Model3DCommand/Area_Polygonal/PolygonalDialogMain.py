# -*- coding: utf-8 -*-
import PySide
import re
import PolygonalDialog
from PySide import QtGui, QtCore
import ItemWidget3D
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D, ObjectTools


class SubForm(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        self.ui = ItemWidget3D.Ui_Form()
        self.ui.setupUi(self)


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = PolygonalDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(False)
        self.obj = obj
        self.initDialog()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False
        Tools3D.switchPointLabel_BaseModel(self.ui)
        Tools3D.switchPointLabel_Model(self.ui)

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        self.ui.le_name.setText(str(self.obj.Label))
        Tools3D.getOrderFromObj(self.obj, self.ui)
        self.ui.le_markx.setText(str(self.obj.MarkX).replace(' ', ''))
        self.ui.le_marky.setText(str(self.obj.MarkY).replace(' ', ''))
        self.ui.le_markz.setText(str(self.obj.MarkZ).replace(' ', ''))
        self.ui.checkBox_isMarkX.setChecked(self.obj.isMarkX)
        self.ui.checkBox_isMarkY.setChecked(self.obj.isMarkY)
        self.ui.checkBox_isMarkZ.setChecked(self.obj.isMarkZ)
        self.ui.checkBox_minX.setChecked(self.obj.isCheckMinX)
        self.ui.checkBox_minY.setChecked(self.obj.isCheckMinX)
        self.ui.checkBox_minZ.setChecked(self.obj.isCheckMinZ)
        self.ui.checkBox_midX.setChecked(self.obj.isCheckMidX)
        self.ui.checkBox_midY.setChecked(self.obj.isCheckMidY)
        self.ui.checkBox_midZ.setChecked(self.obj.isCheckMidZ)
        self.ui.checkBox_maxX.setChecked(self.obj.isCheckMaxX)
        self.ui.checkBox_maxY.setChecked(self.obj.isCheckMaxY)
        self.ui.checkBox_maxZ.setChecked(self.obj.isCheckMaxZ)
        self.ui.spinBox_num.setValue(self.obj.NumbersOfPoints)
        self.slotSpinBox_num()

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        self.obj.Label = self.ui.le_name.text()
        Tools3D.setOrderToObj(self.obj, self.ui)
        self.obj.MarkX = self.ui.le_markx.text()
        self.obj.MarkY = self.ui.le_marky.text()
        self.obj.MarkZ = self.ui.le_markz.text()
        self.obj.isMarkX = self.ui.checkBox_isMarkX.isChecked()
        self.obj.isMarkY = self.ui.checkBox_isMarkY.isChecked()
        self.obj.isMarkZ = self.ui.checkBox_isMarkZ.isChecked()
        self.obj.isCheckMinX = self.ui.checkBox_minX.isChecked()
        self.obj.isCheckMinY = self.ui.checkBox_minY.isChecked()
        self.obj.isCheckMinZ = self.ui.checkBox_minZ.isChecked()
        self.obj.isCheckMidX = self.ui.checkBox_midX.isChecked()
        self.obj.isCheckMidY = self.ui.checkBox_midY.isChecked()
        self.obj.isCheckMidZ = self.ui.checkBox_midZ.isChecked()
        self.obj.isCheckMaxX = self.ui.checkBox_maxX.isChecked()
        self.obj.isCheckMaxY = self.ui.checkBox_maxY.isChecked()
        self.obj.isCheckMaxZ = self.ui.checkBox_maxZ.isChecked()
        self.getItemValue()
        self.obj.recompute()

    def getItemValue(self):
        """
        获取界面坐标信息并设置到helper中，再读取helper中的浮点值设置到Points中
        """
        for index in range(self.ui.spinBox_num.value()):
            tempItem = self.ui.listWidget.item(index)
            tempSubWid = self.ui.listWidget.itemWidget(tempItem)
            setattr(self.obj, "user_point" + str(index + 1) + "_x", tempSubWid.ui.lineEdit_pointx.text().replace(' ', ''))
            setattr(self.obj, "user_point" + str(index + 1) + "_y", tempSubWid.ui.lineEdit_pointy.text().replace(' ', ''))
            setattr(self.obj, "user_point" + str(index + 1) + "_z", tempSubWid.ui.lineEdit_pointz.text().replace(' ', ''))
            Tools3D.setPlaceToObj(self.obj, "Point" + str(index + 1) + ".y", tempSubWid.ui.lineEdit_pointy.text())
            Tools3D.setPlaceToObj(self.obj, "Point" + str(index + 1) + ".x", tempSubWid.ui.lineEdit_pointx.text())
            Tools3D.setPlaceToObj(self.obj, "Point" + str(index + 1) + ".z", tempSubWid.ui.lineEdit_pointz.text())

    def initDialog(self):
        """
        初始化界面，设置界面逻辑
        """
        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)
        try:
            self.ui.spinBox_num.valueChanged.connect(self.slotSpinBox_num)
        except:
            Tools3D.sayz("错误：多边形设置点控件时出现错误")

    def slotSpinBox_num(self):
        """
        点的数量控件数值变化时，修改obj点个数以及Dialog控件个数
        :return: None
        """
        # 先切换Model，在切换View
        cur_num = self.ui.listWidget.count()    # 获取当前listWidget中item数量，即当前点的数量
        input_num = self.ui.spinBox_num.value()

        if input_num == cur_num:
            pass
        elif input_num > cur_num:
            self.addModelPoints(input_num)
            self.addViewPoints(input_num)
        else:
            self.deleteViewPoints(input_num)

    def addModelPoints(self, num):
        """
        添加obj点的数量
        :param num: 输入的点的数量
        :return: None
        """
        num_points = self.getNumOfObjPoints()
        if num_points < num:
            # 注意边界条件，range(a,b) 意味着 [a, b)
            for i in range(num_points + 1, num + 1):
                self.obj.addProperty("App::PropertyVectorDistance", "Point" + str(i),
                                     "Object of a PolygonalArea", "")
                self.obj.addProperty("App::PropertyString", "user_point" + str(i) + "_x")
                self.obj.addProperty("App::PropertyString", "user_point" + str(i) + "_y")
                self.obj.addProperty("App::PropertyString", "user_point" + str(i) + "_z")
                if FreeCAD.ActiveDocument.CoordinateSystem == 'Rectangular':
                    setattr(self.obj, "user_point" + str(i) + "_x", "0mm")
                    setattr(self.obj, "user_point" + str(i) + "_y", "0mm")
                    setattr(self.obj, "user_point" + str(i) + "_z", "0mm")
                elif FreeCAD.ActiveDocument.CoordinateSystem == 'Polar':
                    setattr(self.obj, "user_point" + str(i) + "_x", "0mm")
                    setattr(self.obj, "user_point" + str(i) + "_y", "0deg")
                    setattr(self.obj, "user_point" + str(i) + "_z", "0mm")
                else:
                    setattr(self.obj, "user_point" + str(i) + "_x", "0mm")
                    setattr(self.obj, "user_point" + str(i) + "_y", "0mm")
                    setattr(self.obj, "user_point" + str(i) + "_z", "0deg")
        self.obj.NumbersOfPoints = num

    def addViewPoints(self, num):
        """
        向ListWidget（View）添加控件
        :param num: 输入的点的数量
        :return: None
        """
        cur_count = self.ui.listWidget.count()
        if cur_count < num:
            for i in range(cur_count + 1, num + 1):
                self.addItem(i)

    def deleteViewPoints(self, num):
        """
        删除ListWidget(View)控件
        :param num: 输入的点的数量
        :return: None
        """
        cur_count = self.ui.listWidget.count()
        if 3 <= num < cur_count:
            for i in range(cur_count - num):
                self.ui.listWidget.takeItem(self.ui.listWidget.count() - 1)
        self.obj.NumbersOfPoints=num

    def getNumOfObjPoints(self):
        """
        获取当前Obj点的个数
        :return: int
        """
        temp_list = self.obj.PropertiesList
        num = 0
        for i in temp_list:
            if re.match(r'^Point\d+$', i, re.I):
                num = num + 1
        return num

    def addItem(self, pointOrder):
        tempSub = SubForm(self)
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(tempSub.ui))
        tempSub.ui.label_name.setText('Point' + str(pointOrder) + ':')
        tempSub.ui.lineEdit_pointx.setText(str(getattr(self.obj, "user_point" + str(pointOrder) + "_x")))
        tempSub.ui.lineEdit_pointy.setText(str(getattr(self.obj, "user_point" + str(pointOrder) + "_y")))
        tempSub.ui.lineEdit_pointz.setText(str(getattr(self.obj, "user_point" + str(pointOrder) + "_z")))

        tempWidItem = PySide.QtGui.QListWidgetItem()
        tempWidItem.setSizeHint(PySide.QtCore.QSize(200, 45))
        # 向listWidget添加item的固定调用方法为一下两行
        self.ui.listWidget.addItem(tempWidItem)
        self.ui.listWidget.setItemWidget(tempWidItem, tempSub)

    def slotOK(self):
        try:
            self.setInfoToObj()
        except:
            Tools3D.sayz("--异常--在读取Object属性时出现异常")
        judge = self.judgePoint()
        if judge:
            QtGui.QMessageBox.information(None, "", "无法有效绘制多边形，请检查坐标。")
        else:
            self.isKeepData = True
            self.close()

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def closeEvent(self, event):
        if self.isKeepData:
            FreeCADGui.runCommand("CreateM3D_new")
            FreeCADGui.runCommand("RefreshVolume_3D")
            FreeCADGui.runCommand("UpdateBooleanCommand_3D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

    def judgePoint(self):
        temp_list = self.obj.PropertiesList
        drawPoints = []
        for i in temp_list:
            if re.match(r'Point\d+', i, re.I):
                ve = getattr(self.obj, i)
                curpoint = Tools3D.pointToRecVec(ve)
                drawPoints.append(curpoint)
        if not ObjectTools.isFourPointsOnTheSamePlane(drawPoints):
            return True
        else:
            return False
