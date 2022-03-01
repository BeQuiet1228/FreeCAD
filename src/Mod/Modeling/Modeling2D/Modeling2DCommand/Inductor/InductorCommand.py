# encoding:utf-8
import FreeCAD
import FreeCADGui
import InductorInstance
from Modeling.Modeling2D.Tools import Tools2D
import IndDialogMain


class CreateInductorCommand:
    """
    注册NewMaterial命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = InductorInstance.getObject()
        # 在这里打开Ui
        Form = IndDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/电感.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateInductor',
            '电感')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateInductor',
            'Inductance')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateInductor',CreateInductorCommand())