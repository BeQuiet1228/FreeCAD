# encoding:utf-8
import FreeCAD
import FreeCADGui
import PySide
from PySide import QtCore, QtGui
import SAFDialogMain

class ShowAllFunctionCommand:
    # FreeCAD.Console.PrintError('\n创建SigleClick对象！！！！')
    def IsActive(self):
        pass
        return True

    def Activated(self):
        SAF = SAFDialogMain.ShowAllFunctionDlgMain()
        SAF.show()
        SAF.exec_()
        pass

    def GetResources(self):
        #为了方便此处不修改，用不到
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Annular.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
FreeCADGui.addCommand('ShowAllFunctionCommand', ShowAllFunctionCommand())