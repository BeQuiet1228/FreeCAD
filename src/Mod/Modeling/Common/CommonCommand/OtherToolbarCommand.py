# -*- coding: utf-8 -*-
import FreeCAD

import FreeCADGui

# 左旋转视点
class RotateViewLeft:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        FreeCADGui.activeDocument().activeView().viewRotateLeft()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/RotateViewLeft.svg"
        MenuText = "Rotate View Left"
        ToolTip = "Rotate View Left"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

# 右旋转视点
class RotateViewRight:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
    def Activated(self):
        FreeCADGui.activeDocument().activeView().viewRotateRight()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/RotateViewRight.svg"
        MenuText = "Rotate View Right"
        ToolTip = "Rotate View Right"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('RotateViewLeft', RotateViewLeft())
FreeCADGui.addCommand('RotateViewRight', RotateViewRight())