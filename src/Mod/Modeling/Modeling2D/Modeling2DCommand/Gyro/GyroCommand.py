# encoding:utf-8
import FreeCAD
import FreeCADGui
import GyroInstance
import GyroDialogMain
from Modeling.Modeling2D.Tools import Tools2D


class CreateGyroCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = GyroInstance.getObject()
        # 在这里打开Ui
        Form = GyroDialogMain.ShowDialog(obj,True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/回旋发射.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'Gyro',
            '回旋发射')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'Gyro',
            'Gyclotron Emission')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateGyro', CreateGyroCommand())