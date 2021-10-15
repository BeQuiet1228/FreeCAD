# encoding:utf-8
import FreeCAD
import FreeCADGui
import PolygonalInstance
import PolygonalDialogMain
from Model3D.Tools import Tools3D


class CreatePolygonalCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
           return
        obj = PolygonalInstance.getObject()
        # 在这里打开Ui
        Form = PolygonalDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Area_Polygonal.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '创建多边形',
            '多边形')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '创建多边形',
            '创建一个多边形')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePolygonal_3D', CreatePolygonalCommand())
