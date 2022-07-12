# encoding:utf-8
import ClipDialogMain
import FreeCAD, FreeCADGui
from PySide import QtCore, QtGui
from Model3D.Tools import ObjectTools


class ClipCommand:
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        # dlg=ClipDlg.Clip()
        # 还原ReslutShape的模型
        if FreeCAD.ActiveDocument.getObject("Generated__cross_section") is not None:
            FreeCAD.ActiveDocument.removeObject("Generated__cross_section")
        if FreeCAD.ActiveDocument.getObject("ResultShape") is not None:
            a = FreeCAD.ActiveDocument.ResultShape
            if a.ViewObject.Visibility is False:
                a.ViewObject.Visibility = True
                # 被物理设置选中的线，面
                inductorLine = InductorLineList()
                portArea = PortAreaList()
                systryArea = SysmtryAreaList()
                drivArea = DrivAreaList()
                for i in inductorLine:
                    i.ViewObject.Visibility = True
                    i.ViewObject.ShapeColor = (0.58, 0.58, 0.58)

                for i in portArea:
                    i.ViewObject.Visibility = True
                    i.ViewObject.ShapeColor = (0.247, 0.282, 0.792)

                for i in systryArea:
                    i.ViewObject.Visibility = True
                    i.ViewObject.ShapeColor = (1.0, 0.66, 1.0)

                for i in drivArea:
                    i.ViewObject.Visibility = True
                    i.ViewObject.ShapeColor = (0.72, 0.81, 1.0)

        dlg = None
        mw = FreeCADGui.getMainWindow()
        dws = mw.findChildren(QtGui.QDockWidget)
        for dw in dws:
            if dw.windowTitle() == "Clip":
                dlg = dw
                dlg.hideObjects()
                dlg.show()
                break
        if dlg is None:
            dlg = ClipDialogMain.Clip()
            mw.addDockWidget(QtCore.Qt.DockWidgetArea.RightDockWidgetArea, dlg)
            dlg.show()
        # 找到property view面板
        dwPropertyView = mw.findChild(QtGui.QDockWidget, 'Property view')
        if dwPropertyView:
            mw.tabifyDockWidget(dlg, dwPropertyView)
            dlg.raise_()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/Model/_Operation_Clip.svg"
        # IconPath=""
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Clip',
            '切开模型')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Clip',
            'Clip Model')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand('Clip_3D', ClipCommand())

# @wzg 2021.7.21
# 为了还原原来的模型，把物理设置的点线面显示出来
# 被电感选中的线
def InductorLineList():
    model_list = [ObjectTools.ObjectType.Line_Conformal, ObjectTools.ObjectType.Line_Oblique,
                  ObjectTools.ObjectType.Area_Conformal, ObjectTools.ObjectType.Area_Rectangular,
                  ObjectTools.ObjectType.Area_Polygonal, ObjectTools.ObjectType.Area_Function]
    displayLine = []
    allPhyObjs = ObjectTools.getAllPhyAndProObjects()
    for i in allPhyObjs:
        if i.Type == ObjectTools.ObjectType.IND and hasattr(i, "inductorType") and i.inductorType != "未指定":
            if hasattr(ObjectTools.getObjByLabel(i.inductorType), "Type"):
                if ObjectTools.getObjByLabel(i.inductorType).Type in model_list:
                    displayLine.append(ObjectTools.getObjByLabel(i.inductorType))
    return displayLine


# 被波导端口选中的面
def PortAreaList():
    model_list = [ObjectTools.ObjectType.Line_Conformal, ObjectTools.ObjectType.Line_Oblique,
                  ObjectTools.ObjectType.Area_Conformal, ObjectTools.ObjectType.Area_Rectangular,
                  ObjectTools.ObjectType.Area_Polygonal, ObjectTools.ObjectType.Area_Function]
    displayArea = []
    allPhyObjs = ObjectTools.getAllPhyAndProObjects()
    for i in allPhyObjs:
        if hasattr(i, "orthogonalProjectionPlane") and i.Type == ObjectTools.ObjectType.PORT \
                and i.orthogonalProjectionPlane != "未指定":
            if hasattr(ObjectTools.getObjByLabel(i.orthogonalProjectionPlane), "Type"):
                if ObjectTools.getObjByLabel(i.orthogonalProjectionPlane).Type in model_list:
                    displayArea.append(ObjectTools.getObjByLabel(i.orthogonalProjectionPlane))
    return displayArea


# 被对称边界选中的面
def SysmtryAreaList():
    model_list = [ObjectTools.ObjectType.Area_Conformal, ObjectTools.ObjectType.Area_Rectangular,
                  ObjectTools.ObjectType.Area_Polygonal, ObjectTools.ObjectType.Area_Function]
    displayArea = []
    allPhyObjs = ObjectTools.getAllPhyAndProObjects()
    for i in allPhyObjs:
        if hasattr(i, "orthogonalProjectionPlane") and i.Type == ObjectTools.ObjectType.SYMT and \
                i.orthogonalProjectionPlane != "未指定":
            if hasattr(ObjectTools.getObjByLabel(i.orthogonalProjectionPlane), "Type"):
                if ObjectTools.getObjByLabel(i.orthogonalProjectionPlane).Type in model_list:
                    displayArea.append(ObjectTools.getObjByLabel(i.orthogonalProjectionPlane))
    return displayArea


# 被空间电流源选中的面
def DrivAreaList():
    model_list = [ObjectTools.ObjectType.Area_Conformal, ObjectTools.ObjectType.Area_Rectangular,
                  ObjectTools.ObjectType.Area_Polygonal, ObjectTools.ObjectType.Area_Function]
    displayArea = []
    allPhyObjs = ObjectTools.getAllPhyAndProObjects()
    for i in allPhyObjs:
        if hasattr(i, "orthogonalProjectionPlane") and i.Type == ObjectTools.ObjectType.DRIV and \
                i.orthogonalProjectionPlane != "未指定":
            if hasattr(ObjectTools.getObjByLabel(i.orthogonalProjectionPlane), "Type"):
                if ObjectTools.getObjByLabel(i.orthogonalProjectionPlane).Type in model_list:
                    displayArea.append(ObjectTools.getObjByLabel(i.orthogonalProjectionPlane))
    return displayArea