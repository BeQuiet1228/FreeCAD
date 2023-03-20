# -*- coding: utf-8 -*-
import NetStepSettingDialog
import traceback
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D
import FreeCAD


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = NetStepSettingDialog.Ui_Dialog_WorkSpaceDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        self.setModal(True)
        # 根据坐标系初始化面板
        coord = Tools3D.getCoordinate()
        self.ui.groupBox_WorkSpace_X.setTitle(coord[0])
        self.ui.groupBox_WorkSpace_Y.setTitle(coord[1])
        self.ui.groupBox_WorkSpace_Z.setTitle(coord[2])

    def getInfoFromObj(self):
        try:
            self.ui.lineEdit_Name.setText(self.obj.Label)
            Tools3D.setCoorToUI(self.ui, self.obj)

            self.ui.LineEdit_stride_x.setText(self.obj.stepSizeX)
            self.ui.LineEdit_stride_y.setText(self.obj.stepSizeY)
            self.ui.LineEdit_stride_z.setText(self.obj.stepSizeZ)
            # 启用按钮
            self.ui.checkBox.setChecked(self.obj.isStartUsing)
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def setInfoToObj(self):
        try:
            self.obj.Label = Tools3D.setLabel(self.ui.lineEdit_Name.text())
            Tools3D.getUICoordinate(self.obj, self.ui)

            self.obj.stepSizeX = self.ui.LineEdit_stride_x.text()
            self.obj.stepSizeY = self.ui.LineEdit_stride_y.text()
            self.obj.stepSizeZ = self.ui.LineEdit_stride_z.text()
            self.obj.isStartUsing = self.ui.checkBox.isChecked()
        except:
            Tools3D.sayz("error:" + traceback.format_exc())

    def slotOK(self):
        FreeCAD.ActiveDocument.Param.removeProperty("DX1")
        FreeCAD.ActiveDocument.Param.removeProperty("DX2")
        FreeCAD.ActiveDocument.Param.removeProperty("DX3")

        # 获取坐标系，根据坐标系添加DX1,DX2,DX3
        coodinate = FreeCAD.ActiveDocument.CoordinateSystem
        if coodinate == u'Rectangular' or coodinate == 'Rectangular':
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX1").DX1 = self.ui.LineEdit_stride_x.text()
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX2").DX2 = self.ui.LineEdit_stride_y.text()
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX3").DX3 = self.ui.LineEdit_stride_z.text()
        elif coodinate == u'Polar' or coodinate == 'Polar':
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX1").DX1 = self.ui.LineEdit_stride_x.text()
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyAngle", "DX2").DX2 = self.ui.LineEdit_stride_y.text()
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX3").DX3 = self.ui.LineEdit_stride_z.text()
        elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX1").DX1 = self.ui.LineEdit_stride_x.text()
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX2").DX2 = self.ui.LineEdit_stride_y.text()
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyAngle", "DX3").DX3 = self.ui.LineEdit_stride_z.text()
        self.isKeepData = True
        self.close()