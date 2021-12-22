# encoding:utf-8
import FreeCAD
import FreeCADGui
import TherInstance
import TherDialogMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateTherCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = TherInstance.getObject()
        # 在这里打开Ui
        Form = TherDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/emt.png"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'Ther',
            'Ther Emission')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'Ther',
            'Thermal Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateTher', CreateTherCommand())