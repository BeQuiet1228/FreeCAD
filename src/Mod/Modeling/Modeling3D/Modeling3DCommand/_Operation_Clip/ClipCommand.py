import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end

class ClipCommand:
    def Activated(self):
                
        #######################################

        # Find FreeCAD's root window
        import Clip
        FreeCAD.Console.PrintMessage("ClipCommand1")
        Clip.FreeCADRootWindow= FreeCADGui.getMainWindow()
        FreeCAD.Console.PrintMessage("ClipCommand2")
        # Create the window and start it
        myWidget = Clip.CrossSectionWindow()
        FreeCAD.Console.PrintMessage("ClipCommand3")
        # The CrossSectionWindow will do all the work

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/_Operation_Clip.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Clip',
            'Clip the scene')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Clip',
            'Clip the scene')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('ClipCommand',ClipCommand())