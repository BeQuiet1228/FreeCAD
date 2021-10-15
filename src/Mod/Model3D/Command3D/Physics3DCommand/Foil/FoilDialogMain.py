# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D,ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import FoilDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = FoilDialog.Ui_Dialog_FoilDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            #代码补全
            self.defaultValue = ["OSYS$VOLUME"]
            # 这段代码暂时注释
            # CompleterTools.setLineEditsCompleter(CompleterTools.getAllLineEdits(self.ui))
            # 获取当前坐标系及坐标系单位
            self.ui.DefaultMaterial.clicked.connect(self.DefaultMaterial_clicked)
            self.ui.CustomMaterial.clicked.connect(self.CustomMaterial_clicked)
            Tools3D.switchPointLabel(self.ui)
            self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            # 刷新下拉框
            self.refreshCombox()
            # 正投影面下拉框选择事件
            # self.ui.ComboBox_Shadow.currentIndexChanged.connect(self.ComboBox_Shadow_clicked)
            self.ComboBox_Shadow_clicked()
            # 适配分辨率

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        try:
            ComboBox_Shadow_list = []
            for i in range(self.ui.ComboBox_Shadow.count()):
                ComboBox_Shadow_list.append(self.ui.ComboBox_Shadow.itemText(i))
            volumeList = ObjectTools.getLabelsByType(ObjectTools.ObjectType.Vol_Conformal)
            volumeList.append("OSYS$VOLUME")
            for i in volumeList:
                if i not in ComboBox_Shadow_list:
                    self.ui.ComboBox_Shadow.addItem(i)
            ComboBox_Material_list = []
            for i in range(self.ui.ComboBox_Material.count()):
                ComboBox_Material_list.append(self.ui.ComboBox_Material.itemText(i))
            Custom_Material_list = ObjectTools.getLabelsByType(ObjectTools.ObjectType.NewMaterial)
            for i in Custom_Material_list:
                if i not in ComboBox_Material_list:
                    self.ui.ComboBox_Material.addItem(i)

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def ComboBox_Shadow_clicked(self):
        try:
            if self.ui.ComboBox_Shadow.currentIndex() == 0:
                Tools3D.setCoordEnabled(self.ui, ObjectTools.ObjectType.Vol_Conformal)
            else:
                objName = self.ui.ComboBox_Shadow.currentText()
                if objName in self.defaultValue:
                    pass
                else:
                    Tools3D.setModelCoordinate(self.ui, objName)
                Tools3D.setIsEdit(self.ui, False)
        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.refreshCombox()
            # 名称
            self.ui.LineEdit_Name.setText(self.obj.Label)
            # 下拉框
            self.ui.ComboBox_Shadow.setCurrentIndex(self.ui.ComboBox_Shadow.findText(str(self.obj.foilType)))
            # 坐标
            Tools3D.setCoorToUI(self.ui, self.obj)
            # 铂片厚度
            self.ui.LineEdit_thick.setText(self.obj.foilThickness)
            # 材料名称
            self.ui.CustomMaterial.setChecked(self.obj.isCheckCustom)
            self.ui.ComboBox_Material.setCurrentIndex(self.ui.ComboBox_Material.findText(str(self.obj.customMaterial)))
            self.ui.DefaultMaterial.setChecked(not self.obj.isCheckCustom)
            self.ui.Gold.setText(self.obj.defaultMaterial)
            # 如果选中了物体，那么重新读取一次物体的数据
            self.ComboBox_Shadow_clicked()
            self.ui.ComboBox_Material.setEnabled(self.ui.CustomMaterial.isChecked())
            self.ui.Gold.setEnabled(self.ui.DefaultMaterial.isChecked())

        except:
            import traceback
            # Tools3D.sayz("!!!Error:KeyError,Maybe lack of key:%s" % str(reason))
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            # Tools3D.setLabelToObj(self.obj, self.ui.LineEdit_Name.text())
            # 泊片类型
            self.obj.foilType = self.ui.ComboBox_Shadow.currentText()
            # 坐标
            Tools3D.getUICoordinate(self.obj, self.ui)
            self.obj.foilThickness = self.ui.LineEdit_thick.text()
            # 材料名称
            self.obj.isCheckCustom = self.ui.CustomMaterial.isChecked()
            self.obj.customMaterial = self.ui.ComboBox_Material.currentText()
            self.obj.isCheckDefault = not self.obj.isCheckCustom
            self.obj.defaultMaterial = self.ui.Gold.text()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())
        pass

    def setPrivateInfoToObj(self):
        pass

    def CustomMaterial_clicked(self):
        if self.ui.CustomMaterial.isChecked():
            self.ui.ComboBox_Material.setEnabled(self.ui.CustomMaterial.isChecked())
            self.ui.Gold.setEnabled(self.ui.DefaultMaterial.isChecked())
        else:
            self.ui.ComboBox_Material.setEnabled(False)

    def DefaultMaterial_clicked(self):
        if self.ui.DefaultMaterial.isChecked():
            self.ui.Gold.setEnabled(True)
            self.ui.ComboBox_Material.setEnabled(False)
        else:
            self.ui.Gold.setEnabled(False)




