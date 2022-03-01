# encoding:utf-8
import FreeCAD
import FreeCADGui
import SymtryInstance
from Model3D.Tools import Tools3D
import SymtryDialogMain

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
        obj = SymtryInstance.getObject()
        # 在这里打开Ui
        Form = SymtryDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/sym.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateSymtry',
            '对称边界')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateSymtry',
            'Symmetric Boundary')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create3DSymtry', CreateFreeSpaceCommand())