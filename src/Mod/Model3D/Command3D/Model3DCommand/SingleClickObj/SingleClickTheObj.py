# encoding:utf-8
import FreeCAD
import FreeCADGui
from PySide import QtCore
from Model3D.Tools import ObjectTools, Tools3D


class SingleClickCommand:
    lastClick = []
    def IsActive(self):
        return True

    def Activated(self):
        if FreeCAD.ActiveDocument.Comment == "new3D":
            self.SingleClickDisplayMode()
        pass

    def GetResources(self):
        #为了方便此处不修改，用不到
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/3D_Vol_Annular.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'SingleClickTheObj',
            'add Single Click')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'SingleClickTheObj',
            'add Single Click')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def SingleClickDisplayMode(self):
        objs = FreeCADGui.Selection.getSelection()
        allModelObj = ObjectTools.getAllObjects()
        # 包含创建所有点线面体的list
        selModelObj = []
        # 过滤器
        for i in objs:
            if hasattr(i, "Order") and hasattr(i, "Type"):
                selModelObj.append(i)

        # 隐藏所有其他模型
        for i in allModelObj:
            i.ViewObject.Visibility = False

        # 被物理设置选中的线，面
        inductorLine = InductorLineList()
        portArea = PortAreaList()
        systryArea = SysmtryAreaList()
        drivArea = DrivAreaList()
        select_list = inductorLine + portArea + systryArea + drivArea

        if len(selModelObj) == 0:
            obj_resultshape = FreeCAD.ActiveDocument.ResultShape
            obj_resultshape.ViewObject.Transparency = 0

            for i in select_list:
                i.ViewObject.Transparency = 0

        elif len(selModelObj) == 1:
            obj_resultshape = FreeCAD.ActiveDocument.ResultShape
            obj_resultshape.ViewObject.Transparency = 85
            selModelObj[0].ViewObject.Visibility = True

            # 除了当前选中的点线面，其他的点线面透明度都设置为85
            for i in select_list:
                i.ViewObject.Transparency = 85

            if selModelObj[0] in portArea:
                selModelObj[0].ViewObject.Transparency = 0
                selModelObj[0].ViewObject.ShapeColor = (0.247, 0.282, 0.792)

            elif selModelObj[0] in systryArea:
                selModelObj[0].ViewObject.Transparency = 0
                selModelObj[0].ViewObject.ShapeColor = (1.0, 0.66, 1.0)

            elif selModelObj[0] in drivArea:
                selModelObj[0].ViewObject.Transparency = 0
                selModelObj[0].ViewObject.ShapeColor = (0.72, 0.81, 1.0)
            else:
                selModelObj[0].ViewObject.ShapeColor = (0.00, 1.00, 0.00)

        elif len(selModelObj) > 1:
            obj_resultshape = FreeCAD.ActiveDocument.ResultShape
            obj_resultshape.ViewObject.Transparency = 85
            for i in selModelObj:
                i.ViewObject.Visibility = True
                i.ViewObject.ShapeColor = (0.00, 1.00, 0.00)

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


FreeCADGui.addCommand('SingleClickDisplayMode', SingleClickCommand())


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

class SingleClickParaCommand:
    lastClick = []
    def IsActive(self):
        return True

    def Activated(self):
        if FreeCAD.ActiveDocument.Comment == "new3D":
            self.SingleClickDisplayMode()
        pass

    def GetResources(self):
        #为了方便此处不修改，用不到
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Model3D/Resources3D/3D_Vol_Annular.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'SingleClickTheObj',
            'add Single Click')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'SingleClickTheObj',
            'add Single Click')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def SingleClickDisplayMode(self):
        param = FreeCAD.ActiveDocument.Param
        paramList = param.PropertiesList
        for i in paramList:
            param.setEditorMode(i, 1)

FreeCADGui.addCommand('SingleClickParaCommand', SingleClickParaCommand())