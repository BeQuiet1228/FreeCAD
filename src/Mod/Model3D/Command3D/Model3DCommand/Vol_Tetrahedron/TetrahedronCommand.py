# encoding:utf-8
import FreeCAD
import FreeCADGui
import TetrahedronInstance
import TetrahedronDialogMain
from Model3D.Tools import Tools3D


class CreateTetrahedronCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
           return
        obj = TetrahedronInstance.getObject()
        # 在这里打开Ui
        Form = TetrahedronDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/3D_Vol_Tetrahedron.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            '四面体',
            '四面体')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            '四面体',
            '创建四面体')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create_3D_Tetrahedron', CreateTetrahedronCommand())