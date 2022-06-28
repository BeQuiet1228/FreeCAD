# -*- coding: utf-8 -*-
from PySide import QtGui, QtCore
import ExpsDialog
from Modeling.Modeling2D.Tools import Tools2D
import FreeCAD
import FreeCADGui


class ShowDialog(QtGui.QDialog):
    def __init__(self, obj, isNew=False, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = ExpsDialog.Ui_Dialog_EmeDlg()
        self.ui.setupUi(self)

        self.setModal(False)
        self.obj = obj
        self.isNew = isNew
        self.initDialog()
        self.loadData()
        self.isKeepData = False

    def initDialog(self):
        try:
            self.ui.checkBox_TField.clicked.connect(self.checkBox_TField_clicked)
            self.ui.checkBox_RField.clicked.connect(self.checkBox_RField_clicked)
            self.ui.checkBox_Charg.clicked.connect(self.checkBox_Charg_clicked)
            self.ui.checkBox_FRate.clicked.connect(self.checkBox_FRate_clicked)

            self.ui.pb_ok.clicked.connect(self.pb_ok_clicked)
            self.ui.pb_cancel.clicked.connect(self.pb_cancel_clicked)

            self.ui.checkBox_particleType.clicked.connect(self.checkBox_particleType_clicked)
            self.ui.checkBox_generationRate.clicked.connect(self.checkBox_generationRate_clicked)
            self.ui.checkBox_transmittingInterval.clicked.connect(self.checkBox_transmittingInterval_clicked)
            self.ui.checkBox_surface.clicked.connect(self.checkBox_surface_clicked)
            self.ui.checkBox_outSurface.clicked.connect(self.checkBox_outSurface_clicked)
            # 刷新下拉框
            self.refreshCombox()
            # Tools2D.EmissionUiData(self.obj, self.ui)
            # 获取当前坐标系及坐标系单位
            coord = Tools2D.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            # 根据坐标系初始化面板
            parameter = "(T,"+self.x+","+self.y+")= "
            self.ui.checkBox_TField.setText(u"极限场值.TField"+parameter)
            self.ui.checkBox_RField.setText(u"空间余场.RField"+parameter)
            self.ui.checkBox_Charg.setText(u"最小电荷.Charg"+parameter)
            self.ui.checkBox_FRate.setText(u"等离子体产生率.FRate"+parameter)
            self.ui.label_5.setText(u"偏移Dn"+parameter)

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())

    def checkBox_TField_clicked(self):
        self.ui.textEdit_TField.setEnabled(self.ui.checkBox_TField.isChecked())

    def checkBox_RField_clicked(self):
        self.ui.textEdit_RField.setEnabled(self.ui.checkBox_RField.isChecked())

    def checkBox_Charg_clicked(self):
        self.ui.textEdit_Charg.setEnabled(self.ui.checkBox_Charg.isChecked())

    def checkBox_FRate_clicked(self):
        self.ui.textEdit_FRate.setEnabled(self.ui.checkBox_FRate.isChecked())

    def pb_ok_clicked(self):
        self.isKeepData = True
        self.close()

    def pb_cancel_clicked(self):
        self.isKeepData = False
        self.close()

    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_Shadow_list = []
        ComboBox_area_list = []
        default_list = ["OSYS$AREA"]
        for i in default_list:
            self.ui.ComboBox_Shadow.addItem(i)

        for i in range(self.ui.ComboBox_Shadow.count()):
            ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
        for i in range(self.ui.ComboBox_notInclued.count()):
            ComboBox_area_list.append(self.ui.ComboBox_notInclued.itemText(i))
        EmmiterList = Tools2D.getAllAreaLabel()
        VolumeListAll = Tools2D.getLabelsByType(Tools2D.ObjectType.AreaConformal)
        for i in EmmiterList:
            if i not in ComboBox_Shadow_list:
                self.ui.ComboBox_Shadow.addItem(i)
        for i in VolumeListAll:
            if i not in ComboBox_area_list:
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

    def loadData(self):
        try:
            self.ui.checkBox_TField.setChecked(self.obj.isLimitFieldValue)
            self.ui.textEdit_TField.setText(self.obj.limitFieldValue)
            self.ui.checkBox_RField.setChecked(self.obj.isMoreThanSpacemoreThanSpace)
            self.ui.textEdit_RField.setText(self.obj.moreThanSpace)
            self.ui.checkBox_Charg.setChecked(self.obj.isTheMinimumCharge)
            self.ui.textEdit_Charg.setText(self.obj.theMinimumCharge)
            self.ui.checkBox_FRate.setChecked(self.obj.isPlasmaProductionRate)
            self.ui.textEdit_FRate.setText(self.obj.plasmaProductionRate)
            # 设置槽的状态
            self.checkBox_TField_clicked()
            self.checkBox_RField_clicked()
            self.checkBox_Charg_clicked()
            self.checkBox_FRate_clicked()
            # Tools2D.EmissionUiData(self.obj, self.ui).loadDataFromObj()
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
            self.ui.ComboBox_notIncludedd.setCurrentIndex(
                self.ui.ComboBox_notIncludedd.findText(str(self.obj.launchArea2)))
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
            Tools2D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))

    def keepData(self):
        try:
            self.obj.isLimitFieldValue = self.ui.checkBox_TField.isChecked()
            self.obj.limitFieldValue = self.ui.textEdit_TField.toPlainText()
            self.obj.isMoreThanSpacemoreThanSpace = self.ui.checkBox_RField.isChecked()
            self.obj.moreThanSpace = self.ui.textEdit_RField.toPlainText()
            self.obj.isTheMinimumCharge = self.ui.checkBox_Charg.isChecked()
            self.obj.theMinimumCharge = self.ui.textEdit_Charg.toPlainText()
            self.obj.isPlasmaProductionRate = self.ui.checkBox_FRate.isChecked()
            self.obj.plasmaProductionRate = self.ui.textEdit_FRate.toPlainText()
            # Tools2D.EmissionUiData(self.obj, self.ui).getDataFromUi()

            # 名字
            Tools2D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
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

        except:
            import traceback
            Tools2D.sayz("error:" + traceback.format_exc())
        pass

    # 点击关闭对话框，删除创建的对象
    def closeEvent(self, event):
        if self.isKeepData:
            self.keepData()
            FreeCADGui.runCommand("CreateM2D")
        else:
            if self.isNew:
                FreeCAD.ActiveDocument.removeObject(self.obj.Label)
