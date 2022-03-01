# encoding:utf-8
import FreeCAD
import FreeCADGui
import BeamInstance
import BeamDlgMain
from Modeling.Modeling2D.Tools import Tools2D
import BeamDialogMain

class CreateBeamCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = BeamInstance.getObject()
        # 在这里打开Ui
        Form = BeamDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/束发射.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'EmB',
            '束发射')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'EmB',
            'Beam Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateBeam',CreateBeamCommand())