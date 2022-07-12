# -*- coding: utf-8 -*-
from PySide import QtGui
import FreeCAD
import Part
import FreeCADGui
import ObjectArrayDialog
import linearWidget, orthoWidget, polarWidget, CustomWidget
from Model3D.Tools import ObjectTools, Tools3D


# 自定义属性
class CustomShowWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = CustomWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowLinearWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = linearWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowOrthoWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = orthoWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowPolarWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = polarWidget.Ui_Form()
        self.ui.setupUi(self)


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = ObjectArrayDialog.Ui_Dialog()
        self.ui.setupUi(self)

        self.customAttribute = CustomShowWidget()
        self.linearWidget = ShowLinearWidget()
        self.orthoWidget = ShowOrthoWidget()
        self.polarWidget = ShowPolarWidget()
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(self.linearWidget.ui))
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(self.orthoWidget.ui))
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(self.polarWidget.ui))
        self.setModal(False)
        self.obj = obj
        self.initDialog()

        self.loadData()
        self.getInfoFromObj()
        self.loadCustomData()
        self.isNew = isNew
        self.isKeepData = False

    def initDialog(self):
        self.ui.pb_ok.clicked.connect(self.slotOk)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)

        self.ui.gridLayout_array.addWidget(self.linearWidget)
        self.ui.gridLayout_array.addWidget(self.orthoWidget)
        self.ui.gridLayout_array.addWidget(self.polarWidget)

        self.initArrayType()
        self.initBaseObj()
        self.initLinear()
        self.initOrtho()
        self.initCenterAxis()

        self.refreshUIByArrayType()
        self.refreshOrthoUI()
        # 属性
        self.customAttribute.ui.lineEdit_sigma2.hide()
        self.customAttribute.ui.lineEdit_sigma3.hide()
        self.customAttribute.ui.lineEdit_setEps2.hide()
        self.customAttribute.ui.lineEdit_setEps3.hide()

    def loadData(self):
        # 初始化，绑定槽函数
        self.ui.comboBox_arrayType.currentIndexChanged.connect(self.refreshUIByArrayType)
        self.ui.comboBox_base.currentIndexChanged.connect(self.synchronizeAttributeOrder)
        self.orthoWidget.ui.comboBox_orthoFace.currentIndexChanged.connect(self.refreshOrthoUI)
        self.ui.comboBox_attribute.currentIndexChanged.connect(self.slotAttribute)

    def getInfoFromObj(self):
        try:
            self.ui.lineEdit_name.setText(self.obj.Label)
            Tools3D.getOrderFromObj(self.obj, self.ui)
            self.synchronizeAttributeOrder()

            itemIndex1 = self.ui.comboBox_arrayType.findText(str(self.obj.ArrayType))
            self.ui.comboBox_arrayType.setCurrentIndex(itemIndex1)
            # 第二次弹窗关闭下拉框
            if self.obj.isSetEnabled:
                # 经initBaseObj()初始化后，comboBox_base仅有一项，即obj.BaseType，CurrentIndex置为0即可
                self.ui.comboBox_base.setCurrentIndex(0)
                self.ui.comboBox_base.setEnabled(False)
            else:
                itemIndex2 = self.ui.comboBox_base.findText(str(self.obj.BaseType))
                self.ui.comboBox_base.setCurrentIndex(itemIndex2)
            # linear
            self.linearWidget.ui.lineEdit_number.setText(str(self.obj.user_linerNumber).replace(' ', ''))
            self.linearWidget.ui.lineEdit_intervalX.setText(str(self.obj.user_point_x).replace(' ', ''))
            self.linearWidget.ui.lineEdit_intervalY.setText(str(self.obj.user_point_y).replace(' ', ''))
            self.linearWidget.ui.lineEdit_intervalZ.setText(str(self.obj.user_point_z).replace(' ', ''))

            # ortho
            self.orthoWidget.ui.lineEdit_interval1.setText(str(self.obj.user_interval1).replace(' ', ''))
            self.orthoWidget.ui.lineEdit_interval2.setText(str(self.obj.user_interval2).replace(' ', ''))
            self.orthoWidget.ui.lineEdit_number1.setText(str(self.obj.user_number1).replace(' ', ''))
            self.orthoWidget.ui.lineEdit_number2.setText(str(self.obj.user_number2).replace(' ', ''))
            itemIndex3 = self.orthoWidget.ui.comboBox_orthoFace.findText(str(self.obj.orthoFace))
            self.orthoWidget.ui.comboBox_orthoFace.setCurrentIndex(itemIndex3)

            # polar
            self.polarWidget.ui.lineEdit_numberPolar.setText(str(self.obj.user_numberPolar).replace(' ', ''))
            itemIndex4 = self.polarWidget.ui.comboBox_centerAxis.findText(str(self.obj.centerAxis).replace(' ', ''))
            self.polarWidget.ui.comboBox_centerAxis.setCurrentIndex(itemIndex4)

        except:
            Tools3D.sayz("GetInfoFromObj error")

    def setInfoToObj(self):
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.lineEdit_name.text())
            Tools3D.setOrderToObj(self.obj, self.ui)
            self.obj.Attribute = self.ui.comboBox_attribute.currentText()
            self.obj.ArrayType = self.ui.comboBox_arrayType.currentText()
            self.obj.BaseType = self.ui.comboBox_base.currentText()
            # 第二次弹窗关闭下拉框
            self.obj.isSetEnabled = True
            # linear
            self.obj.user_linerNumber = self.linearWidget.ui.lineEdit_number.text().replace(' ', '')
            self.obj.user_point_x = self.linearWidget.ui.lineEdit_intervalX.text().replace(' ', '')
            self.obj.user_point_y = self.linearWidget.ui.lineEdit_intervalY.text().replace(' ', '')
            self.obj.user_point_z = self.linearWidget.ui.lineEdit_intervalZ.text().replace(' ', '')
            # ortho
            self.obj.user_interval1 = self.orthoWidget.ui.lineEdit_interval1.text().replace(' ', '')
            self.obj.user_interval2 = self.orthoWidget.ui.lineEdit_interval2.text().replace(' ', '')
            self.obj.user_number1 = self.orthoWidget.ui.lineEdit_number1.text().replace(' ', '')
            self.obj.user_number2 = self.orthoWidget.ui.lineEdit_number2.text().replace(' ', '')
            self.obj.orthoFace = self.orthoWidget.ui.comboBox_orthoFace.currentText()
            # polar
            self.obj.user_numberPolar = self.polarWidget.ui.lineEdit_numberPolar.text().replace(' ', '')
            self.obj.centerAxis = self.polarWidget.ui.comboBox_centerAxis.currentText()
            # liner
            Tools3D.setPlaceToObj(self.obj, "linerNumber", self.linearWidget.ui.lineEdit_number.text())
            Tools3D.setPlaceToObj(self.obj, "intervalX", self.linearWidget.ui.lineEdit_intervalX.text())
            Tools3D.setPlaceToObj(self.obj, "intervalY", self.linearWidget.ui.lineEdit_intervalY.text())
            Tools3D.setPlaceToObj(self.obj, "intervalZ", self.linearWidget.ui.lineEdit_intervalZ.text())
            # ortho
            Tools3D.setPlaceToObj(self.obj, "interval1", self.orthoWidget.ui.lineEdit_interval1.text())
            Tools3D.setPlaceToObj(self.obj, "interval2", self.orthoWidget.ui.lineEdit_interval2.text())
            Tools3D.setPlaceToObj(self.obj, "number1", self.orthoWidget.ui.lineEdit_number1.text())
            Tools3D.setPlaceToObj(self.obj, "number2", self.orthoWidget.ui.lineEdit_number2.text())
            # polar
            Tools3D.setPlaceToObj(self.obj, "numberPolar", self.polarWidget.ui.lineEdit_numberPolar.text())
            self.obj.recompute()
        except:
            Tools3D.sayz("SetInfoToObj error!")

    def refreshUIByArrayType(self):
        '''
            根据选择的ArrayType，展示对应的ui界面
        '''
        if self.ui.comboBox_arrayType.currentText() == "linear":
            self.linearWidget.show()
            self.orthoWidget.hide()
            self.polarWidget.hide()
        elif self.ui.comboBox_arrayType.currentText() == "ortho":
            self.linearWidget.hide()
            self.orthoWidget.show()
            self.polarWidget.hide()
        elif self.ui.comboBox_arrayType.currentText() == "polar":
            self.linearWidget.hide()
            self.orthoWidget.hide()
            self.polarWidget.show()
        else:
            Tools3D.sayz("Set Array Type wrong!")

    def refreshOrthoUI(self):
        '''
            根据选择的OrthoFace，展示对应Ortho的ui界面
        '''
        if self.orthoWidget.ui.comboBox_orthoFace.currentText() == "XY":
            self.orthoWidget.ui.label_interval1.setText(r"Interval X:")
            self.orthoWidget.ui.label_interval2.setText(r"Interval Y:")
            self.orthoWidget.ui.label_number1.setText(r"Number X:")
            self.orthoWidget.ui.label_number2.setText(r"Number Y:")
        elif self.orthoWidget.ui.comboBox_orthoFace.currentText() == "XZ":
            self.orthoWidget.ui.label_interval1.setText(r"Interval X:")
            self.orthoWidget.ui.label_interval2.setText(r"Interval Z:")
            self.orthoWidget.ui.label_number1.setText(r"Number X:")
            self.orthoWidget.ui.label_number2.setText(r"Number Z:")
        elif self.orthoWidget.ui.comboBox_orthoFace.currentText() == "YZ":
            self.orthoWidget.ui.label_interval1.setText(r"Interval Y:")
            self.orthoWidget.ui.label_interval2.setText(r"Interval Z:")
            self.orthoWidget.ui.label_number1.setText(r"Number Y:")
            self.orthoWidget.ui.label_number2.setText(r"Number Z:")
        elif self.orthoWidget.ui.comboBox_orthoFace.currentText() == "RZ":
            self.orthoWidget.ui.label_interval1.setText(r"Interval R:")
            self.orthoWidget.ui.label_interval2.setText(r"Interval Z:")
            self.orthoWidget.ui.label_number1.setText(r"Number R:")
            self.orthoWidget.ui.label_number2.setText(r"Number Z:")
        else:
            pass

    def synchronizeAttributeOrder(self):
        """
        同步Array和Base的Attribute和Order，使得Array的Attribute和Order等于Base的Attribute
        """
        baseObj = ObjectTools.getObjByLabel(self.ui.comboBox_base.currentText())
        tempIndex = self.ui.comboBox_attribute.findText(baseObj.Attribute)
        self.ui.comboBox_attribute.setCurrentIndex(tempIndex)

        if hasattr(baseObj, "Order"):
            self.ui.spinBox_order.setValue(baseObj.Order)

    def initArrayType(self):
        self.ui.comboBox_arrayType.clear()
        arrayType_list = ["linear", "ortho", "polar"]
        for i in arrayType_list:
            self.ui.comboBox_arrayType.addItem(i)

    def initBaseObj(self):
        if self.obj.isSetEnabled:
            self.ui.comboBox_base.clear()
            self.ui.comboBox_base.addItem(str(self.obj.BaseType))
        else:
            # baseObj_list = ObjectTools.getAllVolumes()
            # for i in baseObj_list:
            #     if i != self.obj.Label:
            #         self.ui.comboBox_base.addItem(i)

            # 可以阵列的体：正投影体、环形体、圆柱体、圆台体、球体、环形区域体
            conformal_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
            annular_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Annular)
            cylinder_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Cylinder)
            cone_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_SpecialCone)
            spherical_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Spherical)
            annular_section_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Annular_Section)
            baseObj_list = conformal_list + annular_list + cylinder_list + cone_list + spherical_list + annular_section_list
            for i in baseObj_list:
                self.ui.comboBox_base.addItem(i)

    def initLinear(self):
        """
            对不同的坐标系，更改LinearUI界面组件标签
        """
        curCoord = FreeCAD.ActiveDocument.CoordinateSystem
        if curCoord == u'Rectangular':
            self.linearWidget.ui.label_intervalX.setText(r"Interval X:")
            self.linearWidget.ui.label_intervalY.setText(r"Interval Y:")
            self.linearWidget.ui.label_intervalZ.setText(r"Interval Z:")
        elif curCoord == u"Polar":
            self.linearWidget.ui.label_intervalX.setText(r"Interval R:")
            self.linearWidget.ui.label_intervalY.setText(r"Interval Theta:")
            self.linearWidget.ui.label_intervalZ.setText(r"Interval Z:")
        else:
            self.linearWidget.ui.label_intervalX.setText(r"Interval Z:")
            self.linearWidget.ui.label_intervalY.setText(r"Interval R:")
            self.linearWidget.ui.label_intervalZ.setText(r"Interval Theta:")

    def initOrtho(self):
        self.orthoWidget.ui.comboBox_orthoFace.clear()
        curCoord = FreeCAD.ActiveDocument.CoordinateSystem
        if curCoord == u'Rectangular':
            orthoFace_list = ["XY", "XZ", "YZ"]
        else:
            orthoFace_list = ["RZ"]
        for i in orthoFace_list:
            self.orthoWidget.ui.comboBox_orthoFace.addItem(i)

    def initCenterAxis(self):
        self.polarWidget.ui.comboBox_centerAxis.clear()
        curCoord = FreeCAD.ActiveDocument.CoordinateSystem
        if curCoord == u'Rectangular':
            centerAxis_list = ["X", "Y", "Z"]
        else:
            centerAxis_list = ["Z"]
        for i in centerAxis_list:
            self.polarWidget.ui.comboBox_centerAxis.addItem(i)

    def slotOk(self):
        self.isKeepData = True
        self.close()

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def closeEvent(self, *args, **kwargs):
        if self.isKeepData:
            baseObj = ObjectTools.getObjByLabel(self.ui.comboBox_base.currentText())
            if hasattr(baseObj, "Order"):
                baseObj.removeProperty("Order")

            self.setInfoToObj()
            self.keepCustomData()
            self.obj.recompute()
            FreeCADGui.runCommand("CreateM3D_new")
            FreeCADGui.runCommand("UpdateBooleanCommand_3D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

    def loadCustomData(self):
        self.customAttribute.ui.comboBox_sigma.setCurrentIndex(self.customAttribute.ui.comboBox_sigma.findText(str(self.obj.C_SIGMA)))
        self.customAttribute.ui.comboBox_setEps.setCurrentIndex(self.customAttribute.ui.comboBox_setEps.findText(str(self.obj.RDC)))
        self.customAttribute.ui.lineEdit_sigma1.setText(str(self.obj.SIGMA1))
        self.customAttribute.ui.lineEdit_sigma2.setText(str(self.obj.SIGMA2))
        self.customAttribute.ui.lineEdit_sigma3.setText(str(self.obj.SIGMA3))
        self.customAttribute.ui.lineEdit_setEps1.setText(str(self.obj.EPS1))
        self.customAttribute.ui.lineEdit_setEps2.setText(str(self.obj.EPS2))
        self.customAttribute.ui.lineEdit_setEps3.setText(str(self.obj.EPS3))

    def keepCustomData(self):
        self.obj.C_SIGMA = self.customAttribute.ui.comboBox_sigma.currentText()
        self.obj.SIGMA1 = self.customAttribute.ui.lineEdit_sigma1.text()
        self.obj.SIGMA2 = self.customAttribute.ui.lineEdit_sigma2.text()
        self.obj.SIGMA3 = self.customAttribute.ui.lineEdit_sigma3.text()
        self.obj.RDC = self.customAttribute.ui.comboBox_setEps.currentText()
        self.obj.EPS1 = self.customAttribute.ui.lineEdit_setEps1.text()
        self.obj.EPS2 = self.customAttribute.ui.lineEdit_setEps2.text()
        self.obj.EPS3 = self.customAttribute.ui.lineEdit_setEps3.text()

    def slotAttribute(self):
        if self.ui.comboBox_attribute.currentIndex() == 2:
            self.ui.horizontalLayout_3.addWidget(self.customAttribute)
            self.customAttribute.show()
            self.customAttribute.ui.comboBox_sigma.currentIndexChanged.connect(self.sigmaOption)
            self.customAttribute.ui.comboBox_setEps.currentIndexChanged.connect(self.setEpsOption)
        else:
            self.customAttribute.hide()

    def sigmaOption(self):
        if self.customAttribute.ui.comboBox_sigma.currentIndex() == 0:
            self.customAttribute.ui.lineEdit_sigma1.show()
            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()
        elif self.customAttribute.ui.comboBox_sigma.currentIndex() == 1:
            self.customAttribute.ui.lineEdit_sigma1.show()
            self.customAttribute.ui.lineEdit_sigma2.show()
            self.customAttribute.ui.lineEdit_sigma3.show()
        else:
            self.customAttribute.ui.lineEdit_sigma1.hide()
            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()

    def setEpsOption(self):
        if self.customAttribute.ui.comboBox_setEps.currentIndex() == 0:
            self.customAttribute.ui.lineEdit_setEps1.show()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()
        elif self.customAttribute.ui.comboBox_setEps.currentIndex() == 1:
            self.customAttribute.ui.lineEdit_setEps1.show()
            self.customAttribute.ui.lineEdit_setEps2.show()
            self.customAttribute.ui.lineEdit_setEps3.show()
        else:
            self.customAttribute.ui.lineEdit_setEps1.hide()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()
