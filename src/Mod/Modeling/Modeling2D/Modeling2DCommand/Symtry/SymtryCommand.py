# encoding:utf-8
import FreeCAD
import FreeCADGui
import SymtryInstance
from Modeling.Modeling2D.Tools import Tools2D
import SymtryDialogMain

class CreateSymtryCommand:
    """
    注册Symtry命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        obj = SymtryInstance.getObject() 
        # 在这里打开Ui
        Form = SymtryDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/sym.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateSymtry',
            '对称边界')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateSymtry',
            'Symmetric Boundary')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateSymtry', CreateSymtryCommand())