# encoding:utf-8
import FreeCAD
import FreeCADGui
import ExpsInstance
from Model3D.Tools import Tools3D
import ExpsDialogMain


class CreateExpsCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = ExpsInstance.getObject()
        # 在这里打开Ui
        Form = ExpsDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/eme.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'EmB',
            '爆炸式发射')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'EmB',
            'Exps Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateExps_3D', CreateExpsCommand())