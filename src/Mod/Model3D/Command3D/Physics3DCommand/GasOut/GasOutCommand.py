# encoding:utf-8
import FreeCAD
import FreeCADGui
import GasOutInstance
from Model3D.Tools import Tools3D
import GasOutDialogMain

class CreateGasOutCommand:
    """
    注册GasOut命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = GasOutInstance.getObject()
        # 在这里打开Ui
        Form = GasOutDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/driver.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateGasOut',
            '气体解吸附')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateGasOut',
            'Excitation Power')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateGasOut_3D',CreateGasOutCommand())