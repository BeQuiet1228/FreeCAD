# -*- coding: utf-8 -*-
import traceback
from PySide import QtGui
from Model3D.Tools import Tools3D, ObjectTools
import FreeCADGui
import FreeCAD
import CustomWidget
import BaseDialog


class CustomShowWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = CustomWidget.Ui_Form()
        self.ui.setupUi(self)


# 该类是所有模型相关类的父类，子类需要重写__init__、getInfoFromObj、setInfoToObj
class BaseModelDialog(QtGui.QDialog):
    """
    模型对话框的父类
    """
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = BaseDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.gridLayout_object.addWidget(self.pointWidget)
        self.customAttribute = CustomShowWidget()
        self.setModal(False)
        self.obj = obj

        self.setCompleter(None)
        self.initDialog()

        self.loadCommonData()
        self.loadCustomData()
        self.getInfoFromObj()
        self.isNew = isNew
        self.isKeepData = False

    def initDialog(self):
        try:
            Tools3D.switchPointLabel_BaseModel(self.ui)

            self.ui.pushButton_ok.clicked.connect(self.slotOk)
            self.ui.pushButton_cancel.clicked.connect(self.slotCancel)

            # 点线面隐藏属性框
            line_list = ObjectTools.getAllLines()
            area_list = ObjectTools.getAllAreas()
            if hasattr(self.obj, "Type"):
                if self.obj.Type == ObjectTools.ObjectType.Point:
                    self.ui.groupBox_2.hide()
            if self.obj.Label in line_list or self.obj.Label in area_list:
                self.ui.groupBox_2.hide()

            self.ui.comboBox_attribute.currentIndexChanged.connect(self.slotAttribute)
            self.customAttribute.ui.lineEdit_sigma2.hide()
            self.customAttribute.ui.lineEdit_sigma3.hide()
            self.customAttribute.ui.lineEdit_setEps2.hide()
            self.customAttribute.ui.lineEdit_setEps3.hide()
        except:
            Tools3D.sayz(traceback.format_exc())

    def setCompleter(self, widget):
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(widget))

    def loadCommonData(self):
        self.ui.lineEdit_name.setText(self.obj.Label)
        # self.ui.spinBox_order.setValue(self.obj.Order)
        Tools3D.getOrderFromObj(self.obj, self.ui)
        self.ui.comboBox_attribute.setCurrentIndex(self.ui.comboBox_attribute.findText(str(self.obj.Attribute)))
        self.ui.lineEdit_dx1.setText(str(self.obj.MarkX).replace(' ', ''))
        self.ui.lineEdit_dx2.setText(str(self.obj.MarkY).replace(' ', ''))
        self.ui.lineEdit_dx3.setText(str(self.obj.MarkZ).replace(' ', ''))
        self.ui.checkBox_X.setChecked(self.obj.isMarkX)
        self.ui.checkBox_Y.setChecked(self.obj.isMarkY)
        self.ui.checkBox_Z.setChecked(self.obj.isMarkZ)
        self.ui.checkBox_minX.setChecked(self.obj.isCheckMinX)
        self.ui.checkBox_minY.setChecked(self.obj.isCheckMinX)
        self.ui.checkBox_minZ.setChecked(self.obj.isCheckMinZ)
        self.ui.checkBox_midX.setChecked(self.obj.isCheckMidX)
        self.ui.checkBox_midY.setChecked(self.obj.isCheckMidY)
        self.ui.checkBox_midZ.setChecked(self.obj.isCheckMidZ)
        self.ui.checkBox_maxX.setChecked(self.obj.isCheckMaxX)
        self.ui.checkBox_maxY.setChecked(self.obj.isCheckMaxY)
        self.ui.checkBox_maxZ.setChecked(self.obj.isCheckMaxZ)

    def loadCustomData(self):
        self.customAttribute.ui.comboBox_sigma.setCurrentIndex(self.customAttribute.ui.comboBox_sigma.findText(str(self.obj.C_SIGMA)))
        self.customAttribute.ui.comboBox_setEps.setCurrentIndex(self.customAttribute.ui.comboBox_setEps.findText(str(self.obj.RDC)))
        self.customAttribute.ui.lineEdit_sigma1.setText(str(self.obj.SIGMA1))
        self.customAttribute.ui.lineEdit_sigma2.setText(str(self.obj.SIGMA2))
        self.customAttribute.ui.lineEdit_sigma3.setText(str(self.obj.SIGMA3))
        self.customAttribute.ui.lineEdit_setEps1.setText(str(self.obj.EPS1))
        self.customAttribute.ui.lineEdit_setEps2.setText(str(self.obj.EPS2))
        self.customAttribute.ui.lineEdit_setEps3.setText(str(self.obj.EPS3))

    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        子类需要重写该方法，注意异常处理，不要因为输出异常而打不开对话框
        """
        pass

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        子类需要重写该方法，注意异常处理，不要因为输出异常而关不掉对话框
        """
        pass

    def keepCommomData(self):
        self.obj.Label = Tools3D.setLabel(self.ui.lineEdit_name.text())
        Tools3D.setOrderToObj(self.obj, self.ui)
        self.obj.Attribute = self.ui.comboBox_attribute.currentText()
        self.obj.MarkX = self.ui.lineEdit_dx1.text()
        self.obj.MarkY = self.ui.lineEdit_dx2.text()
        self.obj.MarkZ = self.ui.lineEdit_dx3.text()
        self.obj.isMarkX = self.ui.checkBox_X.isChecked()
        self.obj.isMarkY = self.ui.checkBox_Y.isChecked()
        self.obj.isMarkZ = self.ui.checkBox_Z.isChecked()
        self.obj.isCheckMinX = self.ui.checkBox_minX.isChecked()
        self.obj.isCheckMinY = self.ui.checkBox_minY.isChecked()
        self.obj.isCheckMinZ = self.ui.checkBox_minZ.isChecked()
        self.obj.isCheckMidX = self.ui.checkBox_midX.isChecked()
        self.obj.isCheckMidY = self.ui.checkBox_midY.isChecked()
        self.obj.isCheckMidZ = self.ui.checkBox_midZ.isChecked()
        self.obj.isCheckMaxX = self.ui.checkBox_maxX.isChecked()
        self.obj.isCheckMaxY = self.ui.checkBox_maxY.isChecked()
        self.obj.isCheckMaxZ = self.ui.checkBox_maxZ.isChecked()

    def keepCustomData(self):
        self.obj.C_SIGMA = self.customAttribute.ui.comboBox_sigma.currentText()
        self.obj.SIGMA1 = self.customAttribute.ui.lineEdit_sigma1.text()
        self.obj.SIGMA2 = self.customAttribute.ui.lineEdit_sigma2.text()
        self.obj.SIGMA3 = self.customAttribute.ui.lineEdit_sigma3.text()
        self.obj.RDC = self.customAttribute.ui.comboBox_setEps.currentText()
        self.obj.EPS1 = self.customAttribute.ui.lineEdit_setEps1.text()
        self.obj.EPS2 = self.customAttribute.ui.lineEdit_setEps2.text()
        self.obj.EPS3 = self.customAttribute.ui.lineEdit_setEps3.text()

    def slotOk(self):
        self.isKeepData = True
        self.setInfoToObj()
        self.close()

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def closeEvent(self, event):
        if self.isKeepData:
            try:
                # self.setInfoToObj()
                self.keepCommomData()
                self.keepCustomData()
                FreeCADGui.runCommand("CreateM3D_new")
                FreeCADGui.runCommand("UpdateBooleanCommand_3D")
            except AttributeError:
                Tools3D.sayz("--异常--在读取Object属性时出现异常")
                Tools3D.sayz(traceback.format_exc())
            except Exception as e:
                Tools3D.sayz("--" + str(e))
            else:
                FreeCAD.Console.PrintMessage("设置Object信息\n")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)

    def slotAttribute(self):
        if self.ui.comboBox_attribute.currentIndex() == 2:
            self.ui.verticalLayout_attribute.addWidget(self.customAttribute)
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


# 该类是物理设置相关类的父类，子类需要重写setUI、loadDialog、getInfoFromObj、setInfoToObj
class BasePhysicsDialog(QtGui.QDialog):
    """
    物理设置对话框的基类
    """
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = None
        self.setUI()
        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.isKeepData = False

        self.initDialog()
        self.loadDialog()
        self.getInfoFromObj()

    def setUI(self):
        # self.ui = NewMaterialDialog.Ui_Dialog_NewMaterialDlg()
        # self.ui.setupUi(self)
        pass

    def initDialog(self):
        self.ui.pb_ok.clicked.connect(self.slotOK)
        self.ui.pb_cancel.clicked.connect(self.slotCancel)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        pass

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        pass

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        pass

    def setPrivateInfoToObj(self):
        """
        多重继承可能会用到该函数
        """
        pass

    def slotOK(self):
        self.isKeepData = True
        self.close()

    def slotCancel(self):
        self.isKeepData = False
        self.close()

    def closeEvent(self, event):
        if self.isKeepData:
            try:
                self.setInfoToObj()
                self.setPrivateInfoToObj()
                FreeCADGui.runCommand("CreateM3D_new")
            except AttributeError:
                Tools3D.sayz("--异常--在读取Object属性时出现异常")
                Tools3D.sayz(traceback.format_exc())
            except Exception as e:
                Tools3D.sayz("--" + str(e))
            else:
                FreeCAD.Console.PrintMessage("设置Object信息\n")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)


# 发射处理的基类,子类需重写__init__,setUI,privateDialog,loadPrivateData,setPrivateInfoToObj
class BaseEmitDialog(BasePhysicsDialog):
    """
    发射处理对话框的基类
    """
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        # 此处要把对话框的ui实例化
        self.ui = None
        self.setUI()
        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.isKeepData = False

        self.initDialog()
        self.loadDialog()
        self.privateDialog()
        self.getInfoFromObj()
        self.loadPrivateData()

    def setUI(self):
        # self.ui = NewMaterialDialog.Ui_Dialog_NewMaterialDlg()
        # self.ui.setupUi(self)
        pass

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            self.ui.checkBox_particleType.clicked.connect(self.checkBox_particleType_clicked)
            self.ui.checkBox_generationRate.clicked.connect(self.checkBox_generationRate_clicked)
            self.ui.checkBox_transmittingInterval.clicked.connect(self.checkBox_transmittingInterval_clicked)
            self.ui.checkBox_surface.clicked.connect(self.checkBox_surface_clicked)
            self.ui.checkBox_outSurface.clicked.connect(self.checkBox_outSurface_clicked)
            # 刷新下拉框
            self.refreshCombox()
            # 获取当前坐标系及坐标系单位
            coord = Tools3D.getCoordinate()
            # 根据坐标系初始化面板
            self.ui.label_5.setText(u"偏移Dn(T," + coord[0] + "," + coord[1] + "," + coord[2] + ")= ")
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        """
        每次加载窗口时都要重新刷新下拉框，以实现动态加载
        一般来说就是ComboBox_Shodow_list需要动态刷新
        """
        ComboBox_Shadow_list = []
        ComboBox_volume_list = []
        default_list = ["OSYS$VOLUME"]
        for i in default_list:
            self.ui.ComboBox_Shadow.addItem(i)
        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_notInclued.count()):
            ComboBox_volume_list.append(self.ui.ComboBox_notInclued.itemText(i))

        EmmiterList = ObjectTools.getAllVolumes()
        VolumeListAll = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
        for i in EmmiterList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
        for i in VolumeListAll:
            if i not in ComboBox_volume_list:
                self.ui.ComboBox_notInclued.addItem(i)
                self.ui.ComboBox_notIncludedd.addItem(i)
                self.ui.ComboBox_included.addItem(i)
                self.ui.ComboBox_includedd.addItem(i)

    def checkBox_particleType_clicked(self):
        self.ui.ComboBox_particleType.setEnabled(self.ui.checkBox_particleType.isChecked())

    def checkBox_generationRate_clicked(self):
        self.ui.spinBox_generationRate.setEnabled(self.ui.checkBox_generationRate.isChecked())

    def checkBox_transmittingInterval_clicked(self):
        self.ui.radioButton_random.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.radioButton_strictTiming.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())
        self.ui.spinBox_timesStep.setEnabled(self.ui.checkBox_transmittingInterval.isChecked())

    def checkBox_surface_clicked(self):
        self.ui.radioButton_randomm.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_uniform.setEnabled(self.ui.checkBox_surface.isChecked())
        self.ui.radioButton_fixed.setEnabled(self.ui.checkBox_surface.isChecked())

    def checkBox_outSurface_clicked(self):
        self.ui.radioButton_randommm.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.radioButton_alongOutsideFixed.setEnabled(self.ui.checkBox_outSurface.isChecked())
        self.ui.LineEdit_Dn.setEnabled(self.ui.checkBox_outSurface.isChecked())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.LineEdit_Name.setText(self.obj.Label)
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.emitter)))
            self.ui.checkBox_particleType.setChecked(self.obj.isParticleType)
            self.ui.checkBox_generationRate.setChecked(self.obj.isGenerationRate)
            self.ui.spinBox_generationRate.setValue(self.obj.generationRate)
            self.ui.checkBox_transmittingInterval.setChecked(self.obj.isFiringInterval)
            self.ui.radioButton_random.setChecked(self.obj.isRandomDistribution)
            self.ui.radioButton_strictTiming.setChecked(self.obj.isStrictTiming)
            self.ui.spinBox_timesStep.setValue(self.obj.firingInterval)
            self.ui.checkBox_surface.setChecked(self.obj.isSurfaceDistribution)
            self.ui.radioButton_randomm.setChecked(self.obj.isRandom1)
            self.ui.radioButton_uniform.setChecked(self.obj.isBalance1)
            self.ui.radioButton_fixed.setChecked(self.obj.isImmobilization1)
            self.ui.checkBox_outSurface.setChecked(self.obj.isOuterSurfaceDistribution)
            self.ui.radioButton_randommm.setChecked(self.obj.isRandom2)
            self.ui.radioButton_alongOutsideFixed.setChecked(self.obj.isImmobilization2)
            self.ui.LineEdit_Dn.setText(self.obj.excursion)
            self.ui.ComboBox_notInclued.setCurrentIndex(self.ui.ComboBox_notInclued.findText(str(self.obj.launchArea1)))
            self.ui.ComboBox_notIncludedd.setCurrentIndex(self.ui.ComboBox_notIncludedd.findText(str(self.obj.launchArea2)))
            self.ui.ComboBox_included.setCurrentIndex(
                self.ui.ComboBox_included.findText(str(self.obj.launchOrthogonalProjectionRegin1)))
            self.ui.ComboBox_includedd.setCurrentIndex(
                self.ui.ComboBox_includedd.findText(str(self.obj.launchOrthogonalProjectionRegin2)))
            # 加载信号与槽的响应
            self.checkBox_particleType_clicked()
            self.checkBox_generationRate_clicked()
            self.checkBox_transmittingInterval_clicked()
            self.checkBox_surface_clicked()
            self.checkBox_outSurface_clicked()
        except KeyError as reason:
            Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def privateDialog(self):
        """
        独有的对话框逻辑
        """
        pass

    def loadPrivateData(self):
        """
        从obj中加载发射部分的独有数据到对话框中、注意异常处理
        """
        pass

    def setPrivateInfoToObj(self):
        """
        设置各个发射部分独有的数据到obj中
        """
        pass

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        # 名字
        # Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
        self.obj.Label = Tools3D.setLabel(self.ui.LineEdit_Name.text())
        self.obj.emitter = self.ui.ComboBox_Shadow.currentText()
        self.obj.isParticleType = self.ui.checkBox_particleType.isChecked()
        self.obj.particleType = self.ui.ComboBox_particleType.currentText()
        self.obj.isGenerationRate = self.ui.checkBox_generationRate.isChecked()
        self.obj.generationRate = self.ui.spinBox_generationRate.value()
        self.obj.isFiringInterval = self.ui.checkBox_transmittingInterval.isChecked()
        self.obj.isRandomDistribution = self.ui.radioButton_random.isChecked()
        self.obj.isStrictTiming = self.ui.radioButton_strictTiming.isChecked()
        self.obj.firingInterval = self.ui.spinBox_timesStep.value()
        self.obj.isSurfaceDistribution = self.ui.checkBox_surface.isChecked()
        self.obj.isRandom1 = self.ui.radioButton_randomm.isChecked()
        self.obj.isBalance1 = self.ui.radioButton_uniform.isChecked()
        self.obj.isImmobilization1 = self.ui.radioButton_fixed.isChecked()
        self.obj.isOuterSurfaceDistribution = self.ui.checkBox_outSurface.isChecked()
        self.obj.isRandom2 = self.ui.radioButton_randommm.isChecked()
        self.obj.isImmobilization2 = self.ui.radioButton_alongOutsideFixed.isChecked()
        self.obj.excursion = self.ui.LineEdit_Dn.text()
        self.obj.launchArea1 = self.ui.ComboBox_notInclued.currentText()
        self.obj.launchArea2 = self.ui.ComboBox_notIncludedd.currentText()
        self.obj.launchOrthogonalProjectionRegin1 = self.ui.ComboBox_included.currentText()
        self.obj.launchOrthogonalProjectionRegin2 = self.ui.ComboBox_includedd.currentText()
