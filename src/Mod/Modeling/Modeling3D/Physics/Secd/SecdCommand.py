# encoding:utf-8
import FreeCAD
import FreeCADGui
import SecdInstance
import SecdDialogMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateSecdCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = SecdInstance.getObject()
        # 在这里打开Ui
        Form = SecdDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/secd.png"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'Secd',
            'Secd Emission')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'Secd',
            'Secondary Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateSecd', CreateSecdCommand())
