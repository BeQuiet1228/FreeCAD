# -*- coding: utf-8 -*-

from DraftTools import Modifier, msg, selectObject
from DraftGui import todo, QtCore, QtGui, translate, utf8_decode
import FreeCADGui
import FreeCAD
from DraftSnap import *
from DraftTrackers import *
from Modeling.Common.Tools import CoordinateSystemTools
import ArrayDraft
import ArrayNewDialog
# from PyQt4 import QtGUi
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

class Array(Modifier):
    "The Shape2DView FreeCAD command definition"

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Array.svg"
        return {'Pixmap'  : IconPath,
                'MenuText': QT_TRANSLATE_NOOP("Object_Array", "Create a Array"),
                'ToolTip': QT_TRANSLATE_NOOP("Object_Array", "Creates a polar or rectangular array from a selected object")}

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Vol_Array")
        Modifier.Activated(self)
        # 未选中模型
        obj = self.proceed()
        if not FreeCADGui.Selection.getSelection() or not obj:
            if self.ui:
                self.ui.selectUi()
                msg(translate("draft", "Select an object to array\n"))
                QtGui.QMessageBox.information(None,"Warning",u"需要选择目标")
                self.call = self.view.addEventCallback("SoEvent", selectObject)
                self.finish()
                FreeCAD.ActiveDocument.abortTransaction()
        else:
            # obj = self.proceed()
            Form = ArrayNewDialog.showArrayDialog(obj)
            Form.show()
            Form.exec_()
        FreeCAD.ActiveDocument.commitTransaction()
            

    def proceed(self):
        curCoordinateSystem = FreeCAD.ActiveDocument.CoordinateSystem
        if self.call:
            self.view.removeEventCallback("SoEvent", self.call)

        if FreeCADGui.Selection.getSelection():
            obj = FreeCADGui.Selection.getSelection()[0]
            if not hasattr(obj,"Attribute"):
                FreeCAD.Console.PrintError("Select a wrong object!\n")
                return
            else:
                FreeCAD.Console.PrintMessage("Select Obj:"+str(obj.Name)+"\n")

            import copy
            import Modeling.Common.Tools.ObjectsTools as ObjectTools

            # # 将原模型复制一份，使用新模型进行阵列 @pingyue
            # # （因为阵列时会删除Order属性，但属性的增减不记录在事务中）
            # 修改了复制那边的问题就可以直接使用copyObject函数了
            # obj2 = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", obj.Type)
            # obj2.Shape = obj.Shape.copy()
            # obj2.ViewObject.Proxy = copy.deepcopy(obj.ViewObject.Proxy)
            # ObjectTools.addPropertyForVol(obj2, obj.Type, FreeCAD.ActiveDocument.CoordinateSystem)
            # obj2.addProperty("App::PropertyInteger", "Order", "", "Order of the Conformal").Order = 100
            
            # 复制模型
            obj2=FreeCAD.ActiveDocument.copyObject(obj)

            obj2Label = obj.Label
            # 删除原模型
            FreeCAD.ActiveDocument.removeObject(obj.Name)
            obj2.Label = obj2Label

            # 模型进行阵列操作后基本模型与阵列模型会有重复部分，若对阵列选中操作，会不断提示有重复部分，
            # 为了解决这个问题将选中物体默认为所有物体（C++部分：QMimeData * MainWindow::createMimeDataFromSelection () const）
            # 将基本模型与阵列模型合并
            # obj 所属类别
            group = obj2.InList
            activeDoc = FreeCAD.ActiveDocument
            # 选中物体同时属于当前模型组和阵列组
            if len(group) == 1:
                # 与 obj 同类别的所有模型
                #@ fubiao:这里先注释一下，因为，现在分组一开始就会建立，所以不需要删除分组
                # groupObjs = activeDoc.getObject(group[0].Name)
                # if len(groupObjs.Group) == 1:
                #     activeDoc.removeObject(group[0].Name)
                #     activeDoc.recompute()
                # elif len(groupObjs.Group) > 1:
                # 当 obj 的所在类别中包含不止一个模型时，将 obj 移除当前类别
                activeDoc.getObject(group[0].Name).removeObject(activeDoc.getObject(obj2.Name))
            curOrder=getattr(obj2,"Order")
            if curCoordinateSystem == CoordinateSystemTools.CoordinateType.Rectangular:
                # 默认x、y轴方向各复制两个
                objArray = ArrayDraft.makeArray(FreeCAD.ActiveDocument.getObject(obj2.Name), "Vol_Array", "linear", 0.001, 0.001, 0.001, 2)
            elif curCoordinateSystem == CoordinateSystemTools.CoordinateType.Polar or curCoordinateSystem == CoordinateSystemTools.CoordinateType.Cylindrical:
                objArray = ArrayDraft.makeArrayPolar(FreeCAD.ActiveDocument.getObject(obj2.Name), "Vol_Array", "linear", 0.001, 0.0, 0.001, 2)

            # print("finish makeArray")
            ArrayDraft.autogroup(objArray)
            import PartGui,PartChipic
            #PartGui.updateBoolean(curOrder) #ZD
            PartChipic.updateBoolean(curOrder, 1)
            FreeCAD.ActiveDocument.recompute()
            return objArray

            # elif curCoordinateSystem == CoordinateSystemTools.CoordinateType.Cylindrical:
            #     objArray = ArrayDraft.makeArrayCylindrical(FreeCAD.ActiveDocument.getObject(obj.Name), 10, 10, 2, 2, name="Array")
            #     ArrayDraft.autogroup(objArray)
            #     FreeCAD.ActiveDocument.recompute()
        self.finish()

FreeCADGui.addCommand('Object_Array', Array())