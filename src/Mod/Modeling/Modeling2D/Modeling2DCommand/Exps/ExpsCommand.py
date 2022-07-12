# encoding:utf-8
import FreeCAD
import FreeCADGui
import ExpsInstance
from Modeling.Modeling2D.Tools import Tools2D
import ExpsDialogMain


class CreateExpsCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = ExpsInstance.getObject()
        # 在这里打开Ui
        Form = ExpsDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/爆炸式发射.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'Exps',
            '爆炸式发射')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'Exps',
            'Explosive Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateExps',CreateExpsCommand())