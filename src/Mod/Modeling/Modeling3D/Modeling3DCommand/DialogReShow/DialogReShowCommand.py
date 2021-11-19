# encoding:utf-8
import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
import ReShow
#end
#Create a Annular
class ReShowCommand:
    def IsActive(self):
        # if FreeCADGui.ActiveDocument:
        #     return True
        # else:
        #     return False
        pass
        return True

    def Activated(self):
        ReShow.getSelectionobj()
        # FreeCAD.Console.PrintError('obj11')
        pass

    def GetResources(self):
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
class My_Command_Class():
    """My new command"""

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Annular.png"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def Activated(self):
        """Do something here"""
        FreeCAD.Console.PrintError('obj111111111')
        # ReShow.getSelectionobj()
        FreeCAD.Console.PrintError('obj11')
        return

    def IsActive(self):
        """Here you can define if the command must be active or not (greyed) if certain conditions
        are met or not. This function is optional."""
        return True

FreeCADGui.addCommand('My_Command11',My_Command_Class())


FreeCADGui.addCommand('ReShowDialog',ReShowCommand())