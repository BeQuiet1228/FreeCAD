# encoding:utf-8
import FreeCAD
import FreeCADGui
from Model3D.Tools import Tools3D
import ParticleDefineInstance
import ParticleDefineDialogMain

class CreateParticleDefineCommand:
    """
    注册气体电离命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = ParticleDefineInstance.getObject()
        # 在这里打开Ui
        Form = ParticleDefineDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/ProjectSetting/NewSpecies.svg"
        MenuText = Tools3D.QT_TRANSLATE_NOOP(
            'CreateParticleDefine',
            '新型粒子定义')
        ToolTip = Tools3D.QT_TRANSLATE_NOOP(
            'CreateParticleDefine',
            '新型粒子定义')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateParticleDefine_3D', CreateParticleDefineCommand())