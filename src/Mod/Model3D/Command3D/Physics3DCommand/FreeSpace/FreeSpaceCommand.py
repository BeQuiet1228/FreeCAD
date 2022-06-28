# encoding:utf-8
import FreeCAD
import FreeCADGui
import FreeSpaceInstance
from Model3D.Tools import Tools3D
import FreeSpaceDialogMain

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
            return
        obj = FreeSpaceInstance.getObject()
        # 在这里打开Ui
        Form = FreeSpaceDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/free.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFreeSpace',
            '吸收边界')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateFreeSpace',
            'Absorption Space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create3DFreeSpace', CreateFreeSpaceCommand())