# encoding:utf-8
import FreeCAD
import FreeCADGui
import PortInstance
from Modeling.Modeling2D.Tools import Tools2D
import PortDialogMain


class CreatePortCommand:
    """
    注册Port命令
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
        obj = PortInstance.getObject() 
        # 在这里打开Ui
        Form = PortDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/port.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePort',
            '波导端口')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePort',
            'Waveguide Port')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePort', CreatePortCommand())