import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end

class CreateParallelogramCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        import CreateParallelogram
        CreateParallelogram.createParallelogram()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3DParallelogram.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Parallelogram',
            'Create a new Parallelogram')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Parallelogram',
            'Create a new Parallelogram instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateParallelogram',CreateParallelogramCommand())