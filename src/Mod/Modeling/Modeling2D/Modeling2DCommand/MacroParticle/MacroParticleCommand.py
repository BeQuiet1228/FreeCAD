# encoding:utf-8
import FreeCAD
import FreeCADGui
import MacroParticleInstance
import MarcoParticleDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateMacroParticleCommand:
    """
    注册NewMaterial命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = MacroParticleInstance.getObject()
        # 在这里打开Ui
        Form = MarcoParticleDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/宏粒子合并.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateMacroParticle',
            '宏粒子合并')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateMacroParticle',
            '宏粒子合并')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateMacroParticle', CreateMacroParticleCommand())