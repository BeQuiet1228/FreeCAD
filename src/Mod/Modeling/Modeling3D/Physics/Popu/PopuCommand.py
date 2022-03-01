# encoding:utf-8
import FreeCAD
import FreeCADGui
import PopuInstance
from Modeling.Modeling2D.Tools import Tools2D


class CreatePopuCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() == None:
            from Common import CommonCommand
            CommonCommand.NewDocument()
        obj = PopuInstance.getObject()
        # 在这里打开Ui
        # Form = PointNewDialog.showPointDialog(obj)
        # Form.show()
        # Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/popu.png"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'Popu',
            'Popu Emission')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'Popu',
            'Particle Population')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreatePopu', CreatePopuCommand())