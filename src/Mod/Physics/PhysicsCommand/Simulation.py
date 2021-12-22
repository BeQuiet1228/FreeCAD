# -*- coding: UTF-8 -*-

import FreeCAD 
import FreeCADGui

import PortDlgMain
import FreeDlgMain
import SymDlgMain

import EmbDlgMain
import EmeDlgMain
import EmgDlgMain
import EmhDlgMain
import EmtDlgMain
import EmseDlgMain
import MergeDlgMain
import PopulateDlgMain
import GasgasDlgMain
import SpeciesDlgMain
import MarkDlgMain

import SolDlgMain
import ExpDlgMain
import FoilDlgMain
import IndDlgMain

import CntrDlgMain
import VecDlgMain
import PhaDlgMain
import RanDlgMain
import ObsDlgMain

import TimerDlgMain
import DefaultTimerDlgMain
from PySide import QtGui, QtCore
from DlgData import sayz
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
import json
IndexCount={"Port":1,"Free":1,"Sym":1,"EmB":1,"EmE":1,"EmG":1,"EmH":1,"EmT":1,"EmSE":1,"Sol":1,"ExP":1,"Foil":1,"Ind":1,"Cntr":1,"Vec":1,"Pha":1,"Ran":1,"Obs":1,"TimerDef":1,"Timer":1,"Merge":1,"Populate":1,"Gasgas":1,"Species":1,"Mark":1,"NewMaterical":1}

def modifyData(Dialog,itemClassName,itemUserName):
    if Dialog == "Port":              
        PortDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Free":
        FreeDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Sym":
        SymDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "EmB":
        EmbDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "EmE":
        EmeDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "EmG":
        EmgDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "EmH":
        EmhDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "EmT":
        EmtDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "EmSE":
        EmseDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Merge":
        MergeDlgMain.show("old", itemClassName, itemUserName)
    if Dialog == "Populate":
        PopulateDlgMain.show("old",itemClassName, itemUserName)
    if Dialog == "Gasgas":
        GasgasDlgMain.show("old",itemClassName, itemUserName)
    if Dialog == "Species":
        SpeciesDlgMain.show("old",itemClassName, itemUserName)
    if Dialog == "Mark":
        MarkDlgMain.show("old",itemClassName, itemUserName)

    if Dialog == "Sol":
        SolDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "ExP":
        ExpDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Foil":
        FoilDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Ind":
        IndDlgMain.show("old",itemClassName,itemUserName)

    if Dialog == "Cntr":
        CntrDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Vec":
        VecDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Pha":
        PhaDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Ran":
        RanDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Obs":
        ObsDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "Timer":
        TimerDlgMain.show("old",itemClassName,itemUserName)
    if Dialog == "DefTimer":
        DefaultTimerDlgMain.show("old",itemClassName,itemUserName)

    if Dialog == "NewMaterical":

        from ProjectSetting.Commands import NewMatericalDlgMain
        NewMatericalDlgMain.show("old",itemClassName,itemUserName)
    
                                                        
class Port:
    def Activated(self):         
        className = "Port" + str(IndexCount["Port"])
        PortDlgMain.show("new",className,className)
        IndexCount["Port"]+=1
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/port.svg"
        MenuText = "波导端口"
        ToolTip = "Waveguide Port"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class Free:
    def Activated(self):          
        className = "Free" + str(IndexCount["Free"])
        FreeDlgMain.show("new",className,className)
        IndexCount["Free"]+=1               
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/free.svg"
        MenuText = "吸收边界"
        ToolTip = "Absorption Space"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class Sym:
    def Activated(self):
        className = "Sym" + str(IndexCount["Sym"])
        SymDlgMain.show("new",className,className)
        IndexCount["Sym"]+=1
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/sym.svg"
        MenuText = "对称边界"
        ToolTip = "Symmetric Boundary"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class EmB:
    def Activated(self):  
        className = "EmB" + str(IndexCount["EmB"])
        EmbDlgMain.show("new",className,className)
        IndexCount["EmB"]+=1                   
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/emb.svg"
        MenuText = "束发射"
        ToolTip = "Beam Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
# 由于svn不能连接，暂时做一个temp来测试，之后再调整调用武紫凝代码的接口@lzg
class EmSE_temp:
    def Activated(self):  
        className = "EmSE" + str(IndexCount["EmSE"])
        EmseDlgMain.show("new",className,className)
        IndexCount["EmSE"]+=1 
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/emb.svg"
        MenuText = "爆炸式发射"
        ToolTip = "Beam Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Merge_temp:
    def Activated(self):  
        className = "Merge" + str(IndexCount["Merge"])
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        while className in JSON_CADComment.keys():
            IndexCount["Merge"]+=1
            className = "Merge" + str(IndexCount["Merge"])
        MergeDlgMain.show("new",className,className)
        IndexCount["Merge"]+=1 
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Modeling/Modeling2D/modeling2DResources/宏粒子合并.svg"
        MenuText = "宏粒子合并"
        ToolTip = "Beam Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Populate_temp:
    def Activated(self):  
        className = "Populate" + str(IndexCount["Populate"])
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        while className in JSON_CADComment.keys():
            IndexCount["Populate"]+=1
            className = "Populate" + str(IndexCount["Populate"])
        PopulateDlgMain.show("new",className,className)
        IndexCount["Populate"]+=1 
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/emb.svg"
        MenuText = "束发射"
        ToolTip = "Beam Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class EmE:
    def Activated(self):
        className = "EmE" + str(IndexCount["EmE"])
        EmeDlgMain.show("new",className,className)
        IndexCount["EmE"]+=1           
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/eme.svg"
        MenuText = "爆炸式发射"
        ToolTip = "Explosive Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class EmG:
    def Activated(self):
        className = "EmG" + str(IndexCount["EmG"])
        EmgDlgMain.show("new",className,className)
        IndexCount["EmG"]+=1          
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/emg.svg"
        MenuText = "回旋发射"
        ToolTip = "Cyclotron Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class EmH:
    def Activated(self):
        className = "EmH" + str(IndexCount["EmH"])
        EmhDlgMain.show("new",className,className)
        IndexCount["EmH"]+=1          
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/emh.svg"
        MenuText = "强场发射"
        ToolTip = "High Field Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class EmT:
    def Activated(self):
        className = "EmT" + str(IndexCount["EmT"])
        EmtDlgMain.show("new",className,className)
        IndexCount["EmT"]+=1          
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/emt.svg"
        MenuText = "热致发射"
        ToolTip = "Thermal Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Mark:
    def Activated(self):
        className = "Mark" + str(IndexCount["Mark"])
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        Mark_className = []
        for i in JSON_CADComment.keys():
            if JSON_CADComment[i]["Dlg_Type"] == "Mark_Type":
                Mark_className.append(JSON_CADComment[i]["className"])
        while className in Mark_className:
            IndexCount["Mark"]+=1
            className = "Mark" + str(IndexCount["Mark"])
        MarkDlgMain.show("new",className,className)
        IndexCount["Mark"]+=1 
        pass        
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/mark.svg"
        MenuText = "Mark"
        ToolTip = "Mark"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Popu:
    def Activated(self):
        className = "Populate" + str(IndexCount["Populate"])
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        while className in JSON_CADComment.keys():
            IndexCount["Populate"]+=1
            className = "Populate" + str(IndexCount["Populate"])
        PopulateDlgMain.show("new",className,className)
        IndexCount["Populate"]+=1 
        pass         
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/popu.svg"
        MenuText = "粒子设置"
        ToolTip = "Particle Population"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Species:
    def Activated(self):
        className = "Species" + str(IndexCount["Species"])
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        Species_className = []
        for i in JSON_CADComment.keys():
            if JSON_CADComment[i]["Dlg_Type"] == "Species_Type":
                Species_className.append(JSON_CADComment[i]["className"])
        while className in Species_className:
            IndexCount["Species"]+=1
            className = "Species" + str(IndexCount["Species"])
        SpeciesDlgMain.show("new",className,className)
        IndexCount["Species"]+=1 
        pass         
    def GetResources(self):
        # IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/popu.png"
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/NewSpecies.svg"
        MenuText =QtCore.QT_TRANSLATE_NOOP(
                                        "Species",
                                        "NewSpecies")
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
                                        "Species",
                                        "NewSpecies")
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Secd:
    def Activated(self):
        className = "EmSE" + str(IndexCount["EmSE"])
        EmseDlgMain.show("new",className,className)
        IndexCount["EmSE"]+=1 
        pass         
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/secd.svg"
        MenuText = "二次发射"
        ToolTip = "Secondary Emission"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class Ioni:
    def Activated(self):
        className = "Gasgas" + str(IndexCount["Gasgas"])
        JSON_CADComment = json.loads(FreeCAD.ActiveDocument.Begin,object_pairs_hook=OrderedDict) 
        while className in JSON_CADComment.keys():
            IndexCount["Gasgas"]+=1
            className = "Gasgas" + str(IndexCount["Gasgas"])
        GasgasDlgMain.show("new",className,className)
        IndexCount["Gasgas"]+=1 
        pass         
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/ioni.svg"
        MenuText = "气体电离"
        ToolTip = "Gas Ionization"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class Sol:
    def Activated(self):
        className = "Sol" + str(IndexCount["Sol"])
        SolDlgMain.show("new",className,className)
        IndexCount["Sol"]+=1   
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/sole.svg"
        MenuText = "螺旋线圈"
        ToolTip = "Solenoid"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class ExcitationPower:
    def Activated(self):
        className = "ExP" + str(IndexCount["ExP"])
        ExpDlgMain.show("new",className,className)
        IndexCount["ExP"]+=1          
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/driver.svg"
        MenuText = "空间电流源"
        ToolTip = "Excitation Power"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Foil:
    def Activated(self):
        className = "Foil" + str(IndexCount["Foil"])
        FoilDlgMain.show("new",className,className)
        IndexCount["Foil"]+=1  
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/foil.svg"
        MenuText = "箔片"
        ToolTip = "Foil"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Ind:
    def Activated(self):
        className = "Ind" + str(IndexCount["Ind"])
        IndDlgMain.show("new",className,className)
        IndexCount["Ind"]+=1          
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/ind.svg"
        MenuText = "电感"
        ToolTip = "Inductance"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Cntr:
    def Activated(self):
        className = "Cntr" + str(IndexCount["Cntr"])
        CntrDlgMain.show("new",className,className)
        IndexCount["Cntr"]+=1        
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/cntr.svg"
        MenuText = "等位图"
        ToolTip = "Coordinatograph"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Vec:
    def Activated(self):
        className = "Vec" + str(IndexCount["Vec"])
        VecDlgMain.show("new",className,className)
        IndexCount["Vec"]+=1        
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/vec.svg"
        MenuText = "矢量图"
        ToolTip = "Vectorgraph"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Pha:
    def Activated(self):
        className = "Pha" + str(IndexCount["Pha"])
        PhaDlgMain.show("new",className,className)
        IndexCount["Pha"]+=1          
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/pha.svg"
        MenuText = "相空间图"
        ToolTip = "Observing particle phase space"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Ran:
    def Activated(self):
        className = "Ran" + str(IndexCount["Ran"])
        RanDlgMain.show("new",className,className)
        IndexCount["Ran"]+=1
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") +  "Mod/Physics/PhysicsResources/ran.svg"
        MenuText = "空间图"
        ToolTip = "range(space)"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Obs:
    def Activated(self):
        className = "Obs" + str(IndexCount["Obs"])
        ObsDlgMain.show("new",className,className)
        IndexCount["Obs"]+=1
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/obs.svg"
        MenuText = "时间图"
        ToolTip = "Observe(time)"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class TimerDef:
    def Activated(self):
        className = "DefTimer"
        DefaultTimerDlgMain.show("old","DefTimer",className)
               
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/default-timer.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
                'TimerDef',
                'Default timer')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
                'TimerDef',
                'Default timer')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class Timer:
    def Activated(self):
        className = "Timer" + str(IndexCount["Timer"])
        TimerDlgMain.show("new",className,className)
        IndexCount["Timer"]+=1            
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/timer.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
                'Timer',
                'Timer')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
                'Timer',
                'Timer')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class UndoPal:
    def Activated(self):
        import DoManager
        sayz("undo")
        DoManager.undo()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/undoPal.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'PalUndo',
            'Undo Pal')
        ToolTip = "Undo Panel Operation"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        from Physics.PhysicsCommand.__init__ import undoStack
        if undoStack ==[]:
            return False
        toplevel = QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                qtab = i.findChild(QtGui.QTabWidget, 'combiTab')
                index = qtab.currentIndex()
                if qtab.tabText(index) in [u'边界设置', u'观测设置']:
                    return True
        return False

class RedoPal:
    def Activated(self):
        import DoManager
        sayz("redo")
        DoManager.redo()

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/redoPal.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'PalRedo',
            'Redo Pal')
        ToolTip = "Redo Panel Operation"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        from Physics.PhysicsCommand.__init__ import redoStack
        if redoStack == []:
            return False
        toplevel = QApplication.topLevelWidgets()
        for i in toplevel:
            if i.metaObject().className() == "Gui::MainWindow":
                qtab = i.findChild(QtGui.QTabWidget, 'combiTab')
                index = qtab.currentIndex()
                if qtab.tabText(index) in [u'边界设置',u'观测设置']:
                    return True
        return False
# taskControl = None
# class Run:
#     def Activated(self):
#         import Control
#         import Control.controlCommand as controlCommand
#         global taskControl
#
#         import Visualization.VisualizationCommand.VisualizationTree as VT
#         # 判断是M3DEditor点击的“Run”还是从SImulation过来的“Run”
#         if FreeCAD.Gui.activeWorkbench().ToolTip=='M3D File Editor workbench':
#             if taskControl == None:
#                 taskControl = controlCommand.TaskControlMain.TaskControlMain(comeFrom="M3DFileEditor")
#             # 显示运行结果树形列表
#             taskControl.show()
#             from M3DFileEditor.M3DFileEditorCommand import EditorActions
#             if EditorActions.FilePath.filePath!="":
#                 FreeCAD.Console.PrintMessage("EditorActions.filePath: "+EditorActions.FilePath.filePath+"\n")
#                 VT.showPlotTree(EditorActions.FilePath.filePath)
#             else:
#                 FreeCAD.Console.PrintMessage("EditorActions.filePath: "+EditorActions.FilePath.filePath+"\n")
#                 FreeCAD.Console.PrintError("Simulation/Run: Error file")
#         else:
#             if taskControl == None:
#                 taskControl = controlCommand.TaskControlMain.TaskControlMain(comeFrom="Simulation")
#             # 显示运行结果树形列表
#             taskControl.show()
#
#             FreeCAD.Console.PrintMessage("\nactiveWorkbench:  "+FreeCAD.Gui.activeWorkbench().ToolTip+"\n")
#             VT.showPlotTree()
#
#         # taskControl.show()
#
#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/run.svg"
#         MenuText = "Run"
#         ToolTip = "Run Task"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

class AllRun:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Collateral Run\n")
        reply = QtGui.QMessageBox.information(None, "", "Collateral Run")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/all-run.svg"
        MenuText = " Collateral Run"
        ToolTip = "Collateral Run"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

# class M3DEditorWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("M3DFileEditorWorkbench")
#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(False)
 
#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/M3DFileEditor/M3DFileEditorResources/M3DFileEditorWorkbench.png"
#         MenuText = "M3D File Editor"
#         ToolTip = "To M3D File Editor Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# class PostProcessingWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("VisualWorkbench")

#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(False)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/VisualWorkbench.svg"
#         MenuText = "Post Processing"
#         ToolTip = "To Post Processing Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# class Modeling3DWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("Modeling3DWorkbench")
#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(True)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/3DModelingWorkbench.svg"
#         MenuText = "3D Modeling"
#         ToolTip = "To 3D Modeling Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# class Modeling2DWorkbench:
#     def Activated(self):
#         FreeCADGui.activateWorkbench("Modeling2DWorkbench")

#         mainWindow = FreeCADGui.getMainWindow()
#         propertyView = mainWindow.findChild(QtGui.QDockWidget, "Property view")
#         propertyView.setVisible(True)

#     def GetResources(self):
#         IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2DModelingWorkbench.svg"
#         MenuText = "2D Modeling"
#         ToolTip = "To 2D Modeling Part"
#         return {'Pixmap': IconPath,
#                 'MenuText': MenuText,
#                 'ToolTip': ToolTip}

# 获取坐标系
def getCoordinate():
    from Modeling.Common.Tools import InputTools
    length = InputTools.currentLengthUnits()
    angle = InputTools.currentAngleUnits()
    coodinate = FreeCAD.ActiveDocument.CoordinateSystem
    if coodinate == u'Rectangular':
        # unitList = ["X", "Y", "Z", "m", "m", "m"]
        unitList = ["X","Y","Z",length,length,length]
    elif coodinate == u'Polar':
        # unitList = ["R", u"θ", "Z", "m", "deg", "m"]
        unitList = ["R",u"θ", "Z", length,angle,length]
    elif coodinate == u'Cylindrical':
        # unitList = ["Z", "R", u"θ", "m", "m", "deg"]
        unitList = ["Z", "R", u"θ", length, length, angle]
    return unitList

# by mx
# 为了解决直接打开freeCAD文件，面板信息不加载的问题

from PySide.QtGui import QApplication
class InitPanel:
    def Activated(self):
        try:
            from Physics.PhysicsCommand.BoundPalMain import BoundSettingTreeShow, BoundSettingTree
            from Physics.PhysicsCommand.ObservePalMain import ObserveSettingTreeShow,ObserveSettingTree
            toplevel = QApplication.topLevelWidgets()
            for i in toplevel:
                if i.metaObject().className() == "Gui::MainWindow":
                    # tr = i.findChild(QtGui.QTreeWidget,'treeWidget_OperatingPanel')
                    # if not tr:
                    #     tree = FigTree()
                    #     tree.show()
                    tr1 = i.findChild(QtGui.QTreeWidget, 'treeWidget_boundSettingTree')
                    if not tr1:
                        boundTree = BoundSettingTree()
                        boundTree.show()
                    tr2= i.findChild(QtGui.QTreeWidget, 'treeWidget_observeSettingTree')
                    if not tr2:
                        observeTree = ObserveSettingTree()
                        observeTree.show()
            # FigTreeShow()

            BoundSettingTreeShow()
            ObserveSettingTreeShow()
        except:
            pass
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Common/CommonResources/document-open.svg"
        MenuText = "init panel"
        ToolTip = "init panel"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
FreeCADGui.addCommand('Customize_init_panel', InitPanel())

FreeCADGui.addCommand('Port', Port())
FreeCADGui.addCommand('Free', Free())
FreeCADGui.addCommand('Sym', Sym())
FreeCADGui.addCommand('EmB', EmB())
FreeCADGui.addCommand('EmE', EmE())
FreeCADGui.addCommand('EmG', EmG())
FreeCADGui.addCommand('Popu', Popu())
FreeCADGui.addCommand('EmH', EmH())
FreeCADGui.addCommand('EmT', EmT())
FreeCADGui.addCommand('Secd', Secd())
FreeCADGui.addCommand('Ioni', Ioni())
FreeCADGui.addCommand('Sol', Sol())
FreeCADGui.addCommand('Excitation power', ExcitationPower())
FreeCADGui.addCommand('Foil', Foil())
FreeCADGui.addCommand('Ind', Ind())
FreeCADGui.addCommand('Cntr', Cntr())
FreeCADGui.addCommand('Vec', Vec())
FreeCADGui.addCommand('Pha', Pha())
FreeCADGui.addCommand('Ran', Ran())
FreeCADGui.addCommand('Obs', Obs())
FreeCADGui.addCommand('TimerDef', TimerDef())
FreeCADGui.addCommand('Timer', Timer())
FreeCADGui.addCommand('EmSE',EmSE_temp())
FreeCADGui.addCommand("Merge",Merge_temp())
FreeCADGui.addCommand("Populate",Populate_temp())
FreeCADGui.addCommand('UndoPal', UndoPal())
FreeCADGui.addCommand('RedoPal', RedoPal())
FreeCADGui.addCommand('Species',Species())
FreeCADGui.addCommand("Mark", Mark())
#FreeCADGui.addCommand('Run', Run())
#FreeCADGui.addCommand('AllRun', AllRun())
# FreeCADGui.addCommand('M3D File Editor', M3DEditorWorkbench())
# FreeCADGui.addCommand('Modeling 2D', Modeling2DWorkbench())
# FreeCADGui.addCommand('Modeling 3D', Modeling3DWorkbench())
# FreeCADGui.addCommand('Post Processing', PostProcessingWorkbench())
import SwitchWorkbench
