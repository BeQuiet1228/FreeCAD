# encoding:utf-8
import FreeCAD
import FreeCADGui
import DrivInstance
from Model3D.Tools import Tools3D
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
            return
        obj = DrivInstance.getObject()
        # 在这里打开Ui
        Form = DrivDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/driver.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateDriv',
            '电流源')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateDriv',
            'Excitation Power')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Create3D_Driv',CreateDrivCommand())