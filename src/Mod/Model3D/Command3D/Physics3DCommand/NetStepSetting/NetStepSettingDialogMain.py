# -*- coding: utf-8 -*-
import NetStepSettingDialog
import traceback
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain
from Model3D.Tools import Tools3D, ExpressionTools3D
import FreeCAD


class ShowDialog(BaseDialogMain.BasePhysicsDialog):
    def __init__(self, obj, isNew=False, parent=None):
        BaseDialogMain.BasePhysicsDialog.__init__(self, obj, isNew, parent)

    def setUI(self):
        self.ui = NetStepSettingDialog.Ui_Dialog_WorkSpaceDlg()
        self.ui.setupUi(self)

    def loadDialog(self):
        Tools3D.setLineEditsCompleter(Tools3D.getAllLineEdits(self.ui))
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
        paramList = Tools3D.getParamsList()
        if 'DX1' in paramList:
            FreeCAD.ActiveDocument.Param.removeProperty("DX1")
        if 'DX2' in paramList:
            FreeCAD.ActiveDocument.Param.removeProperty("DX2")
        if 'DX3' in paramList:
            FreeCAD.ActiveDocument.Param.removeProperty("DX3")

        # 获取坐标系，根据坐标系添加DX1,DX2,DX3
        coodinate = FreeCAD.ActiveDocument.CoordinateSystem
        Dx1Str = ExpressionTools3D.processingLengthExpression(self.ui.LineEdit_stride_x.text())
        Dx2Str = ExpressionTools3D.processingLengthExpression(self.ui.LineEdit_stride_y.text())
        Dx3Str = ExpressionTools3D.processingLengthExpression(self.ui.LineEdit_stride_z.text())
        if coodinate == u'Rectangular' or coodinate == 'Rectangular':
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX1")
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX2")
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX3")
        elif coodinate == u'Polar' or coodinate == 'Polar':
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX1")
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyAngle", "DX2")
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX3")
        elif coodinate == u'Cylindrical' or coodinate == 'Cylindrical':
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX1")
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyLength", "DX2")
            FreeCAD.ActiveDocument.Param.addProperty("App::PropertyAngle", "DX3")

        FreeCAD.ActiveDocument.Param.setExpression("DX1", Dx1Str.replace("", ""))
        FreeCAD.ActiveDocument.Param.setExpression("DX2", Dx2Str.replace("", ""))
        FreeCAD.ActiveDocument.Param.setExpression("DX3", Dx3Str.replace("", ""))

        self.isKeepData = True
        self.close()