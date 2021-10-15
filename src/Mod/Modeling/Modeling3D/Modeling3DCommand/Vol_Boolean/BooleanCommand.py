import FreeCAD
import FreeCADGui
from Common.Tools import ObjectsTools
#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units

global flaglastDoWhichCommand
flaglastDoWhichCommand=3
#end
#Create a Torus
class RecomputeBooleanForAllObjsCommand:
    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Boolean")
        global flaglastDoWhichCommand
        FreeCAD.Console.PrintMessage("1: "+str(flaglastDoWhichCommand)+"\n")
        ObjectsTools.reComputeBooleanForAllObjs(flagLastDoWhichCommand=flaglastDoWhichCommand)
        flaglastDoWhichCommand=1
        FreeCAD.ActiveDocument.commitTransaction()
        #FreeCADGui.ActiveDocument.getObject("ResultShape").Transparency = 95
        # if FreeCAD.activeDocument() == None:
        #     FreeCAD.newDocument()
        # import DoBoolean
        # DoBoolean.createTorus()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/refreshAll.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'RecomputeAll',
            'Recompute all of objects')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'RecomputeAll',
            'Recompute all of objects')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('RecomputeBooleanForAllObjs',RecomputeBooleanForAllObjsCommand())
#end
class RecomputeBooleanForPartObjsCommand:
    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Boolean")
        global flaglastDoWhichCommand
        FreeCAD.Console.PrintMessage("2: "+str(flaglastDoWhichCommand)+"\n")
        ObjectsTools.reComputeBooleanBySubVacuo(flagLastDoWhichCommand=flaglastDoWhichCommand)
        flaglastDoWhichCommand=2
        FreeCAD.ActiveDocument.commitTransaction()
        # if FreeCAD.activeDocument() == None:
        #     FreeCAD.newDocument()
        # import DoBoolean
        # DoBoolean.createTorus()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/refreshPart.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'RecomputePart',
            'Recompute part of objects')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'RecomputePart',
            'Recompute part of objects')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

FreeCADGui.addCommand('RecomputeBooleanForPartObjs',RecomputeBooleanForPartObjsCommand())