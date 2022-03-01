# -*- coding: utf-8 -*-
import FreeCADGui
import FreeCAD
from Model3D.Tools import Tools3D,ObjectTools
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
import MarkDialog


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = MarkDialog.Ui_Dialog()
        self.ui.setupUi(self)

    def loadDialog(self):
        """
        此处写对话框的逻辑,注意异常处理
        """
        try:
            # 获取当前坐标系及坐标系单位
            # coord = Tools3D.getCoordinate()
            # self.x = coord[0]
            # self.y = coord[1]
            # self.z = coord[2]
            # self.x_unit = coord[3]
            # self.y_unit = coord[4]
            # self.z_unit = coord[5]
            self.refreshCombox()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def getInfoFromObj(self):
        """
        从obj获取数据加载到对话框、注意异常处理
        """
        try:
            self.ui.comboBox_obj.setCurrentIndex(self.ui.comboBox_obj.findText(str(self.obj.markObject)))
            # Mark方向
            self.ui.comboBox_x.setCurrentIndex(self.ui.comboBox_x.findText(str(self.obj.direction)))
            # Mark位置
            self.ui.checkBox_min.setChecked(self.obj.isMINIMUM)
            self.ui.checkBox_mid.setChecked(self.obj.isMIDPOINT)
            self.ui.checkBox_max.setChecked(self.obj.isMAXIMUM)
            # Mark大小
            self.ui.lineEdit_size.setText(self.obj.size)

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        """
        从对话框读取数据，设置obj的属性值
        """
        try:
            # self.obj.orthogonalProjectionPlane = self.ui.ComboBox_uniformParam.currentText()

            # Mark对象
            self.obj.markObject = self.ui.comboBox_obj.currentText()
            # Mark方向
            self.obj.direction = self.ui.comboBox_x.currentText()
            # Mark位置
            self.obj.isMINIMUM = self.ui.checkBox_min.isChecked()
            self.obj.isMIDPOINT = self.ui.checkBox_mid.isChecked()
            self.obj.isMAXIMUM = self.ui.checkBox_max.isChecked()
            # Mark大小
            self.obj.size = self.ui.lineEdit_size.text()

        except:
            import traceback
            Tools3D.sayz("error:" + traceback.format_exc())

    def setPrivateInfoToObj(self):
        pass

    def refreshCombox(self):
        '''
        每次加载窗口时都要重新加载下拉列表，以实现动态加载
        一般来说就是ComboBox_Shadow_list需要动态刷新
        '''
        ComboBox_list=[]
        MarkObj = []
        for i in range(self.ui.comboBox_obj.count()):
            ComboBox_list.append(self.ui.comboBox_obj.itemText(i))
        MarkList = ObjectTools.getAllObjects()
        for i in MarkList:
            if hasattr(i, "Order"):
                MarkObj.append(i.Label)
        for i in MarkObj:
            if i not in ComboBox_list:
                self.ui.comboBox_obj.addItem(i)
