# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
import RegularPolygonDialog
from PySide import QtGui
import FreeCAD

from Modeling.Modeling2D.Tools.Tools2D import sayz


class ShowCircularDialog(QtGui.QDialog):
    def __init__(self, obj, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.ui = RegularPolygonDialog.Ui_Dialog()
        self.ui.setupUi(self)

        # 暂时写在这里
        self.setModal(False)
        self.obj = FreeCAD.ActiveDocument.getObject(obj.Name)
        self.initDialog()
        self.getInfoFromObj()
    def getInfoFromObj(self):
        """
        从Object获取信息，并且设置到Dialog
        """
        try:
            self.ui.le_name.setText(self.obj.Label)
            self.ui.le_order.setText(str(self.obj.Order))
            self.ui.le_markx.setText(self.obj.MarkX)
            self.ui.le_marky.setText(self.obj.MarkY)
            self.ui.checkBox_isMarkX.setChecked(self.obj.isMarkX)
            self.ui.checkBox_isMarkY.setChecked(self.obj.isMarkY)
            self.ui.le_x.setText(str(self.obj.Placement.Base.x))
            self.ui.le_y.setText(str(self.obj.Placement.Base.y))
            self.ui.le_radius.setText(str(self.obj.Radius))
            self.ui.le_facesNumber.setText(str(self.obj.FacesNumber))
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def setInfoToObj(self):
        """
        从Dialog获取信息，并且赋值到Object
        """
        self.close()
        try:
            self.obj.Label = self.ui.le_name.text()
            self.obj.Order = int(self.ui.le_order.text())
            self.obj.MarkX = self.ui.le_markx.text()
            self.obj.MarkY = self.ui.le_marky.text()
            self.obj.isMarkX = self.ui.checkBox_isMarkX.isChecked()
            self.obj.isMarkY = self.ui.checkBox_isMarkY.isChecked()
            self.obj.Placement.Base.x = float(self.ui.le_x.text())
            self.obj.Placement.Base.y = float(self.ui.le_y.text())
            self.obj.Radius = self.ui.le_radius.text()
            self.obj.FacesNumber = int(self.ui.le_facesNumber.text())
            self.obj.recompute()
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass

    def initDialog(self):
        """
        初始化界面，设置界面逻辑
        """
        try:
            self.ui.pb_cancel.clicked.connect(self.close)
            self.ui.pb_ok.clicked.connect(self.slotOK)
            self.ui.checkBox_isMarkX.stateChanged.connect(self.isMarkXFun)
            self.ui.checkBox_isMarkY.stateChanged.connect(self.isMarkYFun)
        except:
            import traceback
            sayz("error:" + traceback.format_exc())
        pass
    def isMarkXFun(self):
        self.ui.le_markx.setEnabled(self.ui.checkBox_isMarkX.isChecked())
        pass
    def isMarkYFun(self):
        self.ui.le_marky.setEnabled(self.ui.checkBox_isMarkY.isChecked())
        pass
    def slotOK(self):
        self.setInfoToObj()
        pass