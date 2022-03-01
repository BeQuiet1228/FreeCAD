#-*- coding: utf-8 -*-
import FoilDialog
from PySide import QtGui
import FreeCAD
from Physics.PhysicsCommand import Simulation
from Physics.PhysicsCommand.DlgData import sayz
from Modeling.Common.Tools import DocumentTools,ObjectsTools
from Physics.PhysicsTools import CompleterTools
from Modeling.Modeling2D.Tools import Tools2D

def getNewMaterical():
    NewMaterical_list = Tools2D.getSpecificTypePhyAndProObjects(u"NewMaterial")
    NewMatericalName_list = []
    for ele in NewMaterical_list:
        NewMatericalName_list.append(ele.Name)
    return NewMatericalName_list

         
class ShowDialog(QtGui.QDialog):
    def __init__(self,obj,parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = FoilDialog.Ui_Dialog_FoilDlg()
        self.ui.setupUi(self)
        self.obj = obj
        self.initDialog()
        self.loadData()

    def initDialog(self):
        try:
            #代码补全
            self.defaultValue = ["OSYS$VOLUME"]
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            self.ui.pb_cancel.clicked.connect(self.onCancel)
            self.ui.pb_ok.clicked.connect(self.onConfirm)
            self.ui.DefaultMaterial.clicked.connect(self.DefaultMaterial_clicked)
            self.ui.CustomMaterial.clicked.connect(self.CustomMaterial_clicked)
            # 获取当前坐标系及坐标系单位
            coord = Simulation.getCoordinate()
            self.x = coord[0]
            self.y = coord[1]
            self.z = coord[2]
            self.x_unit = coord[3]
            self.y_unit = coord[4]
            self.z_unit = coord[5]
            # 箔片厚度是不受坐标系单位影响的量，如果不需要修改请删除下列代码块
            unit = FreeCAD.Units.getDefaultUnits()
            if unit[0]==0:
                self.ui.LineEdit_thick.setText("1mm")
            elif unit[0]==1:
                self.ui.LineEdit_thick.setText("0.1cm")
            else:
                self.ui.LineEdit_thick.setText("0.001m")


            # 根据坐标系初始化面板
            self.ui.label_X.setText(self.x)
            self.ui.label_Y.setText(self.y)
            self.ui.label_Z.setText(self.z)

            self.ui.LineEdit_start_x.setText("0" + self.x_unit)
            self.ui.LineEdit_start_y.setText("0" + self.y_unit)
            self.ui.LineEdit_start_z.setText("0" + self.z_unit)
            self.ui.LineEdit_end_x.setText("0" + self.x_unit)
            self.ui.LineEdit_end_y.setText("0" + self.y_unit)
            self.ui.LineEdit_end_z.setText("0" + self.z_unit)

            # 关闭Z轴设置
            self.ui.label_Z.hide()
            self.ui.LineEdit_start_z.hide()
            self.ui.LineEdit_end_z.hide()
            
            self.ui.CustomMaterial.setChecked(True)
            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)

            self.userNameBefore=self.ui.LineEdit_Name.text()
            # 用于判断是否进行名称更新
            self.flagUpdateItemName=False

            self.ComboBox_Shadow_clicked()
            # 适配分辨率
            from Physics.PhysicsCommand import AdaptiveDPIUtil
            new_x, new_y = AdaptiveDPIUtil.get_new_dpi(self.width(), self.height())
            self.resize(new_x, new_y)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())


    def refreshCombox(self):  
        try:
            '''
            每次加载窗口时都要重新加载下拉列表，以实现动态加载
            一般来说就是ComboBox_Shadow_list需要动态刷新
            '''
            ComboBox_Shadow_list=[]
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
            volumeList = DocumentTools.getActiveDocTypes("Area_Conformal")
            volumeList.append("OSYS$VOLUME")
            for i in volumeList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)     

            ComboBox_Material_list = []
            for i in range(self.ui.ComboBox_Material.count()):
                ComboBox_Material_list.append(self.ui.ComboBox_Material.itemText(i))
            Custom_Material_list = getNewMaterical()
            for i in Custom_Material_list:
                if i not in ComboBox_Material_list:
                    self.ui.ComboBox_Material.addItem(i)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())


    def ComboBox_Shadow_clicked(self):
        try:
            ObjectsTools.findObjByLabelWithoutOrderAndVisible(self.ui.ComboBox_Shadow.currentText())
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                self.ui.LineEdit_start_x.setEnabled(True)
                self.ui.LineEdit_start_y.setEnabled(True)
                self.ui.LineEdit_start_z.setEnabled(True)
                self.ui.LineEdit_end_x.setEnabled(True)
                self.ui.LineEdit_end_y.setEnabled(True)
                self.ui.LineEdit_end_z.setEnabled(True)
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    modelData = DocumentTools.getValueOfVolComformalObjByLable(objName)
                    self.ui.LineEdit_start_x.setText(str(modelData[1]))
                    self.ui.LineEdit_start_y.setText(str(modelData[2]))
                    self.ui.LineEdit_start_z.setText(str(modelData[3]))
                    self.ui.LineEdit_end_x.setText(str(modelData[4]))
                    self.ui.LineEdit_end_y.setText(str(modelData[5]))
                    self.ui.LineEdit_end_z.setText(str(modelData[6]))
                self.ui.LineEdit_start_x.setEnabled(False)
                self.ui.LineEdit_start_y.setEnabled(False)
                self.ui.LineEdit_start_z.setEnabled(False)
                self.ui.LineEdit_end_x.setEnabled(False)
                self.ui.LineEdit_end_y.setEnabled(False)
                self.ui.LineEdit_end_z.setEnabled(False)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())

    def onCancel(self):
        self.close()

    def onConfirm(self):
        self.keepData()
        self.close()
        
    def loadData(self): 
        try:    
            self.refreshCombox()
            # 获取对象 modefied
            self.ui.LineEdit_Name.setText(self.obj.Name) 
            # 设置标记的旧名字
            self.userNameBefore = self.obj.Name
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.foilType)))
            
            self.ui.LineEdit_start_x.setText(self.obj.point1_X)
            self.ui.LineEdit_start_y.setText(self.obj.point1_Y)

            self.ui.LineEdit_end_x.setText(self.obj.point2_X)
            self.ui.LineEdit_end_y.setText(self.obj.point2_Y)
            # 铂片厚度
            self.ui.LineEdit_thick.setText(self.obj.foilThickness)
            # 材料名称
            self.ui.CustomMaterial.setChecked(self.obj.isCheckCustom)
            self.ui.ComboBox_Material.setCurrentIndex(self.ui.ComboBox_Material.findText(str(self.obj.customMaterial)))
            # else:
            self.ui.DefaultMaterial.setChecked(not self.obj.isCheckCustom) 
            self.ui.Gold.setText(self.obj.defaultMaterial)               
        except:
            import traceback
            sayz("error:" + traceback.format_exc())   
        pass        

    def keepData(self):
        try:
            self.obj.foilType = self.ui.ComboBox_Shadow.currentText()
            self.obj.point1_X = self.ui.LineEdit_start_x.text()
            self.obj.point1_Y = self.ui.LineEdit_start_y.text()

            self.obj.point2_X = self.ui.LineEdit_end_x.text()
            self.obj.point2_Y = self.ui.LineEdit_end_y.text()

            # 铂片厚度
            self.obj.foilThickness = self.ui.LineEdit_thick.text()
            # 材料名称
            self.obj.isCheckCustom = self.ui.CustomMaterial.isChecked()
            self.obj.customMaterial = self.ui.ComboBox_Material.currentText()
            # else:
            self.obj.isCheckDefault = not(self.obj.isCheckCustom)
            self.obj.defaultMaterial = self.ui.Gold.text()
            self.refreshCombox()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def CustomMaterial_clicked(self):
        if self.ui.CustomMaterial.isChecked():
            self.ui.ComboBox_Material.setEnabled(self.ui.CustomMaterial.isChecked())
            self.ui.Gold.setEnabled(self.ui.CustomMaterial.isChecked())
        else:
            self.ui.ComboBox_Material.setEnabled(False)

    def DefaultMaterial_clicked(self):
        if self.ui.DefaultMaterial.isChecked():
            self.ui.Gold.setEnabled(True)
            self.ui.ComboBox_Material.setEnabled(False)
        else:
            self.ui.Gold.setEnabled(False)
