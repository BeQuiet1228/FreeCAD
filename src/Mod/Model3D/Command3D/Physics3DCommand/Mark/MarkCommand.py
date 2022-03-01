# encoding:utf-8
import FreeCAD
import FreeCADGui
import MarkInstance
from Model3D.Tools import Tools3D
import MarkDialogMain

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
        obj = MarkInstance.getObject()
        # 在这里打开Ui
        Form = MarkDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/mark.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateMark',
            'Mark设置')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateMark',
            'Mark')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateMark', CreateFreeSpaceCommand())