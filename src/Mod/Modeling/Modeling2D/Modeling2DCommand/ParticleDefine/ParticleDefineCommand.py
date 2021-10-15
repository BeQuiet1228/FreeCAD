# encoding:utf-8
import FreeCAD
import FreeCADGui
import ParticleDefineInstance
from Modeling.Modeling2D.Modeling2DCommand.ParticleDefine import ParticleDefineDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateParticleDefineCommand:
    """
    注册ParticleDefine命令
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
        Form = ParticleDefineDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/新型粒子定义.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateParticleDefine',
            '新型粒子定义')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateParticleDefine',
            '新型粒子定义')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateParticleDefine', CreateParticleDefineCommand())