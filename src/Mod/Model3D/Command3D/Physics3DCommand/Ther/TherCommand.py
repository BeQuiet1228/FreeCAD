# encoding:utf-8
import FreeCAD
import FreeCADGui
import TherInstance
from Model3D.Tools import Tools3D
import TherDialogMain


class CreateTherCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = TherInstance.getObject()
        # 在这里打开Ui
        Form = TherDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/emt.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'EmT',
            '热致发射')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'EmT',
            'Ther Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateTher_3D', CreateTherCommand())