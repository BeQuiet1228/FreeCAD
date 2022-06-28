# encoding:utf-8
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D
import PortInstance
import PortDialogMain


class CreatePortCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = PortInstance.getObject()
        # 在这里打开Ui
        Form = PortDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/port.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'EmB',
            '波导端口')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'EmB',
            'Exps Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePort_3D', CreatePortCommand())