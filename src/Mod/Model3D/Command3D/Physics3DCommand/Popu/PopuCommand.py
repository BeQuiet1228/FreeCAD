# encoding:utf-8
import FreeCAD
import FreeCADGui
import PopuInstance
from Model3D.Tools import Tools3D
import PopuDialogMain

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
        obj = PopuInstance.getObject()
        # 在这里打开Ui
        Form = PopuDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/popu.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'Popu',
            '粒子设置')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'Popu',
            'Particle Population')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create3D_Popu', CreateFreeSpaceCommand())