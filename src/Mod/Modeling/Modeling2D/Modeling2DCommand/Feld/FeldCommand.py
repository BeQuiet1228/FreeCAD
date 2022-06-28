# encoding:utf-8
import FreeCAD
import FreeCADGui
import FeldInstance
import FeldDialogMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateFeldCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = FeldInstance.getObject()
        # 在这里打开Ui
        Form = FeldDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/强场发射.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'Feld',
            '强场发射')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'Feld',
            'High Field Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateFeld', CreateFeldCommand())