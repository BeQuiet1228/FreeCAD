# encoding:utf-8
import FreeCAD
import FreeCADGui
import FeldInstance
from Model3D.Tools import Tools3D
import FeldDialogMain


class CreateFeldCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = FeldInstance.getObject()
        # 在这里打开Ui
        Form = FeldDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/emg.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'EmF',
            '强场发射')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'EmF',
            'Feld Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateFeld_3D', CreateFeldCommand())
