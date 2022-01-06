# encoding:utf-8
import FreeCAD
import FreeCADGui
import MarkInstance
from Modeling.Modeling2D.Tools import Tools2D
import MarkDialogMain

class CreateMarkCommand:
    """
    注册Mark命令
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
        obj = MarkInstance.getObject() 
        # 在这里打开Ui
        Form = MarkDialogMain.ShowDialog(obj, True)
        Form.show()
        Form.exec_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/mark设置.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateMark',
            'Mark设置')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateMark',
            'Mark')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('CreateMark', CreateMarkCommand())