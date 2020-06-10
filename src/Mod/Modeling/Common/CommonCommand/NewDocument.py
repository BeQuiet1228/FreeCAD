import FreeCAD
import FreeCADGui
import CommonGui
class NewDocument:
    def Activated(self):
        dlg = CommonGui.CoordinateSystemUI.CoordinateSystemDialog()
        dlg.exec_()
        if dlg.Result == "2D":
            FreeCADGui.activateWorkbench("Modeling2DWorkbench")
            FreeCAD.newDocument()
            FreeCAD.ActiveDocument.CoordinateSystem = dlg.CoordinateSystem

        if dlg.Result == "3D":
            FreeCADGui.activateWorkbench("Modeling3DWorkbench")
            FreeCAD.newDocument()
            FreeCAD.ActiveDocument.CoordinateSystem = dlg.CoordinateSystem

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/document-new.svg"
        MenuText = "New"
        Accel = "Ctrl+N"
        ToolTip = "Create new document"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'Accel': Accel,
                'ToolTip': ToolTip}
# override default function File->New
FreeCADGui.addCommand('Std_New', NewDocument())