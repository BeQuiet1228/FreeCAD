# encoding:utf-8
import FreeCAD
import FreeCADGui

from Modeling.Modeling2D.Tools import Tools2D


class RepairCommand:
    """
    注册Foil命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        if FreeCAD.activeDocument() is None:
            return
        import Draft
        p = FreeCAD.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
        t = Draft.getParamType("fillmode")
        default = False
        if not p.GetBool("fillmode", default):
            p.SetBool("fillmode", True)
            Tools2D.sayz("重新设置模型是否形成面的配置信息，请重启")

        # 修改草图的默认选项
        import Draft
        Draft.setParam("snapModes", '100011000001000')

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/修理.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateRepair',
            '修复')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateRepair',
            'Repair')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('RepairModel', RepairCommand())