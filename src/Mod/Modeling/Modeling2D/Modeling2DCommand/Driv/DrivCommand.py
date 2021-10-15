# encoding:utf-8
import FreeCAD
import FreeCADGui
import DrivInstance
from Modeling.Modeling2D.Tools import Tools2D
import DrivDialogMain


class CreateDrivCommand:
    """
    注册Driv命令
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
        obj = DrivInstance.getObject() 
        # 在这里打开Ui
        Form = DrivDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/driver.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateDriv',
            '电流源')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateDriv',
            'Excitation Power')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('CreateDriv',CreateDrivCommand())