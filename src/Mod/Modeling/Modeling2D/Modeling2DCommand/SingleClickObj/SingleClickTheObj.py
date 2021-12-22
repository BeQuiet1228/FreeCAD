# encoding:utf-8
import FreeCAD
import FreeCADGui
import PySide
from PySide import QtCore, QtGui
from Modeling.Common.Tools import ObjectsTools
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Tools.Tools2D import ObjectType
from Physics.PhysicsTools import SetVisibilityOfModels

class SingleClickCommand:
    lastClick = []
    def IsActive(self):
        return True

    def Activated(self):
        if FreeCAD.ActiveDocument.Comment == "2D":
            self.SingleClickDisplayMode()
        pass

    def GetResources(self):
        #为了方便此处不修改，用不到
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Annular.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def SingleClickDisplayMode(self):
        objs = FreeCADGui.Selection.getSelection()
        allModelObj = Tools2D.getAllModelObjects()
        # 包含创建所有点线面的list
        selModelObj = []
        # 过滤器
        for i in objs:
            if hasattr(i, "Order"):
                selModelObj.append(i)

        # 隐藏所有其他模型
        for i in allModelObj:
            i.ViewObject.Visibility = False

        if len(selModelObj) == 0:
            pass

        elif len(selModelObj) == 1:
            selModelObj[0].ViewObject.Visibility = True

        elif len(selModelObj) > 1:
            for i in selModelObj:
                i.ViewObject.Visibility = True


# FreeCADGui.addCommand('SingleClickDisplayMode', SingleClickCommand())

