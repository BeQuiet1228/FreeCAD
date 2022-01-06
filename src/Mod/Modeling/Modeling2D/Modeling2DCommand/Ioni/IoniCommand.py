# encoding:utf-8
import FreeCAD
import FreeCADGui
import IoniInstance
from Modeling.Modeling2D.Modeling2DCommand.Ioni import IoniDlgMain
from Modeling.Modeling2D.Tools import Tools2D

class CreateIoniCommand:

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = IoniInstance.getObject()
        # 在这里打开Ui
        Form = IoniDlgMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/气体电离.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'Ioni',
            '气体电离')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'Ioni',
            'Gas Ionization')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateIoni', CreateIoniCommand())