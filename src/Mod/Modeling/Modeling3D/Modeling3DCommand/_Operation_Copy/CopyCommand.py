# -*- coding: UTF-8 -*-
import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
#end

objs = None
# class CopyObjs:
#     objects
#     @staticmethod
#     def getObjs():
#         return objects
#     @staticmethod
#     def setObjs(objs):
#         objects=objs


class CopyCommand:
    def Activated(self):
        # 点复制按钮时不需要openTransaction！ @pingyue
        # FreeCAD.ActiveDocument.openTransaction("Copy")
        import Copy
        Copy.doCopy()
        global objs
        objs.insert(0, 1)
        FreeCAD.Console.PrintMessage("objs1: "+str(objs)+'\n')

        # The CrossSectionWindow will do all the work

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/_Operation_Copy.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Copy',
            '复制对象')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Copy',
            '复制选中的对象')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip,
                'Accel':"Ctrl+C"}

    def IsActive(self):
        sel = FreeCADGui.Selection.getCompleteSelection()
        if not sel:
            return False
        isSelValid = True
        try:
            # 依次检查选中对象是否是一个形状，如果有不是形状的对象则不允许复制
            for i in range(len(sel)):
                sel[i].Shape
                if sel[i].Label == "ResultShape":
                    isSelValid = False
            # 在这里commitTransaction会导致程序不停地commitTransaction @pingyue
            # FreeCAD.ActiveDocument.commitTransaction()
        except:
            isSelValid = False

        if FreeCADGui.ActiveDocument and isSelValid:
            return True
        else:
            return False



class PasteCommand:
    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Paste")
        import Copy
        global objs
        if objs is None:
            return
        FreeCAD.Console.PrintMessage("objs2: "+str(objs))
        Copy.doPaste(objs)
        FreeCAD.ActiveDocument.commitTransaction()

        # The CrossSectionWindow will do all the work

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/_Operation_Paste.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Paste',
            '粘贴对象')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Paste',
            '粘贴剪贴板中的对象')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip,
                'Accel':"Ctrl+V"}

    def IsActive(self):
        if FreeCADGui.ActiveDocument and objs is not None:
            return True
        else:
            return False


class CutCommand:
    def Activated(self):
        
        import Copy
        Copy.doCopy()
        global objs
        objs.insert(0, 0)
        FreeCAD.Console.PrintMessage("objs1: "+str(objs)+'\n')

        # The CrossSectionWindow will do all the work

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/_Operation_Cut.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Cut',
            '剪切对象')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Cut',
            '剪切选中的对象')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip,
                'Accel':"Ctrl+X"}

    def IsActive(self):
        sel = FreeCADGui.Selection.getCompleteSelection()
        if not sel:
            return False
        isSelValid = True
        try:
            # 依次检查选中对象是否是一个形状，如果有不是形状的对象则不允许复制
            for i in range(len(sel)):
                sel[i].Shape
                if sel[i].Label == "ResultShape":
                    isSelValid = False
            # FreeCAD.ActiveDocument.commitTransaction()
        except:
            isSelValid = False

        if FreeCADGui.ActiveDocument and isSelValid:
            return True
        else:
            return False
# 让C++部分可以清除这里的剪贴板
class ClearClipboardCommand:
    def Activated(self):
        
        global objs
        objs = None

    def GetResources(self):

        return {'Pixmap': "",
                'MenuText': "",
                'ToolTip': ""}

    def IsActive(self):
        return objs is not None

FreeCADGui.addCommand('CopyCommand',CopyCommand())
FreeCADGui.addCommand('CutCommand',CutCommand())
FreeCADGui.addCommand('PasteCommand',PasteCommand())
FreeCADGui.addCommand('ClearClipboardCommand',ClearClipboardCommand())