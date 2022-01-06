# encoding:utf-8
import FreeCAD
import FreeCADGui
import FreeSpaceInstance
from Modeling.Modeling2D.Tools import Tools2D
import FreeDialogMain

class CreateFreeSpaceCommand:
    """
    注册FreeSpace命令
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
        obj = FreeSpaceInstance.getObject() 
        # 在这里打开Ui
        Form = FreeDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/free.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFreeSpace',
            'Create FreeSpace')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateFreeSpace',
            'Absorption Space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateFreeSpace', CreateFreeSpaceCommand())