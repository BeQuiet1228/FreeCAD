# encoding:utf-8
import FreeCAD
import FreeCADGui
import SecdInstance
from Model3D.Tools import Tools3D
import SecdDialogMain


class CreateSecdCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = SecdInstance.getObject()
        # 在这里打开Ui
        Form = SecdDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/secd.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'EmS',
            '二次发射')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'EmS',
            'Seceod Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateSecd_3D', CreateSecdCommand())