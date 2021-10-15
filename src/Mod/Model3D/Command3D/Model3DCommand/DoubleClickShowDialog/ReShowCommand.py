# encoding:utf-8
import FreeCAD
import FreeCADGui
import ReShowDialogMain
from PySide import QtCore, QtGui


class ReShowCommand:
    def IsActive(self):
        return True

    def Activated(self):
        ReShowDialogMain.slotDoubleClicked()

    def GetResources(self):
        """该命令不会显示在界面上，这个函数的代码并不会被调用"""
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


FreeCADGui.addCommand('ReShowDialog_3D', ReShowCommand())
