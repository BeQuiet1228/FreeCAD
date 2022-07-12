# encoding:utf-8
import FreeCAD
import FreeCADGui
import InductorInstance
from Model3D.Tools import Tools3D
import InductorDialogMain


class CreateInductorCommand:
    """
    注册NewMaterial命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = InductorInstance.getObject()
        # 在这里打开Ui
        Form = InductorDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Physics/ind.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateInductor',
            '电感')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateInductor',
            '电感')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateInductor_3D', CreateInductorCommand())
