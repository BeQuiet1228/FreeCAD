# encoding:utf-8
import FreeCAD
import FreeCADGui
from Modeling.Modeling2D.Tools import Tools2D


class ViewCommand:
    """
    注册Foil命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        FreeCADGui.activeDocument().activeView().viewTop()
        # FreeCADGui.SendMsgToActiveView("ViewFit")
        res = FreeCAD.ActiveDocument.ResultShape
        if res.Shape.isNull():
            FreeCADGui.SendMsgToActiveView("ViewFit")
        else:
            FreeCADGui.Selection.clearSelection()
            FreeCADGui.Selection.addSelection(res)
            FreeCADGui.SendMsgToActiveView("ViewSelection")

        # for i in range(10):
        #     FreeCADGui.ActiveDocument.ActiveView.zoomIn()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/调整视角.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateView',
            '调整视野')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateView',
            'View')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('AdjustView', ViewCommand())