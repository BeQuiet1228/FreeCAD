# encoding:utf-8
import FreeCAD
import FreeCADGui
import PhasSpaceInstance
from Modeling.Modeling2D.Modeling2DCommand.PhasSpace import PhasSpaceDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreatePhasSpaceCommand:
    """
    注册PhasSpace命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = PhasSpaceInstance.getObject()
        # 在这里打开Ui
        Form = PhasSpaceDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/粒子相对空间观测.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePhasSpace',
            '相空间图')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreatePhasSpace',
            'Observe Particle phase space')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePhasSpace', CreatePhasSpaceCommand())