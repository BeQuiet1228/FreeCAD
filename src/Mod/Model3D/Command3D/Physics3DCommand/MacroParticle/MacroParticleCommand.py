# encoding:utf-8
import FreeCAD
import FreeCADGui
import MacroParticleInstance
from Model3D.Tools import Tools3D
import MacroParticleDialogMain

class CreateMacroParticleCommand:
    """
    注册MacroParticle命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            return
        obj = MacroParticleInstance.getObject()
        # 在这里打开Ui
        Form = MacroParticleDialogMain.ShowDialog(obj)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/宏粒子合并.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateMacroParticle',
            '宏粒子合并')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateMacroParticle',
            'Absorption Space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateMacroParticle_3D', CreateMacroParticleCommand())