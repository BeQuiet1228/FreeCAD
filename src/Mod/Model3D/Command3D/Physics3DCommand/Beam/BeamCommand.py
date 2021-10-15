# encoding:utf-8
import FreeCAD
import FreeCADGui
import BeamInstance
from Model3D.Tools import Tools3D
import BeamDialogMain


class CreateBeamCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = BeamInstance.getObject()
        # 在这里打开Ui
        Form = BeamDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/emb.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'EmB',
            '束发射')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'EmB',
            'Beam Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateBeam_3D', CreateBeamCommand())