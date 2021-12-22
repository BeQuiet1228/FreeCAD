# encoding:utf-8
import FreeCAD
import FreeCADGui
import VectorInstance
from Modeling.Modeling2D.Modeling2DCommand.Vector import VectorDlgMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateVectorCommand:
    """
    注册Cntr命令
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
        obj = VectorInstance.getObject()
        # 在这里打开Ui
        Form = VectorDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/vec.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateVector',
            '矢量图')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateVector',
            'Vectorgraph')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateVector', CreateVectorCommand())