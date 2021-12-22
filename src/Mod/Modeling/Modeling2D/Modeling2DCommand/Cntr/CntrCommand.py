# encoding:utf-8
import FreeCAD
import FreeCADGui
import CntrInstance
from Modeling.Modeling2D.Tools import Tools2D
from Modeling.Modeling2D.Modeling2DCommand.Cntr import CntrDlgMain

class CreateCntrCommand:
    """
    注册Cntr命令
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
        obj = CntrInstance.getObject()
        # 在这里打开Ui
        Form = CntrDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/cntr.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateCntr',
            '等位图')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateCntr',
            'Coordinatograph')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateCntr', CreateCntrCommand())