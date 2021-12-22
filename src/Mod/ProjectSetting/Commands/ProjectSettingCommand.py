#-*- coding: utf-8 -*-
import json
import sys
import FreeCAD
from PySide import QtCore,  QtGui

import WorkSpaceSettingDlgMain,NewMatericalDlgMain,FiledSettingDlgMain,TimeDomainComputingSettingDlgMain,DataProcessingSettingDlgMain,ModelingInfoDlgMain,RunOptionsDlgMain

import FreeCAD
import FreeCADGui
#json格式数据需要保持原有顺序输出
from collections import OrderedDict
# IndexCount = {"NewMaterical":1}
class WorkSpaceSettingsCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        className="WorkSpaceSettings"
        dlg=WorkSpaceSettingDlgMain.WorkSpaceSettings(className)
        dlg.show()
        dlg.exec_()
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/WorkSpaceSettings.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'WorkSpaceSettings',
            'WorkSpaceSettings')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'WorkSpaceSettings',
            'WorkSpaceSettings')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class NewMatericalCommand:
    def Activated(self):
        # if FreeCAD.activeDocument()==None:
        #     FreeCAD.newDocument()
        # FreeCAD_Comment_Dict = json.loads(FreeCAD.ActiveDocument.Comment,object_pairs_hook=OrderedDict)
        # className="NewMaterical" + str(IndexCount["NewMaterical"])
        # while className in FreeCAD_Comment_Dict.keys():
        #     IndexCount["NewMaterical"] += 1
        #     className="NewMaterical" + str(IndexCount["NewMaterical"])
        # dlg=NewMatericalDlgMain.NewMaterial(className)
        # dlg.show()
        # dlg.exec_()
        # IndexCount["NewMaterical"] += 1
        from Physics.PhysicsCommand import Simulation
        className = "NewMaterical" + str(Simulation.IndexCount["NewMaterical"])
        NewMatericalDlgMain.show("new",className,className)
        Simulation.IndexCount["NewMaterical"]+=1 
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/NewMaterical.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'NewMaterical',
            'New Material')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'NewMaterical',
            'New Material')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False
class FiledSettingCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        className="FiledSetting"
        dlg=FiledSettingDlgMain.FieldSetting(className)
        dlg.show()
        dlg.exec_()
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/FiledSetting.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'FiledSetting',
            'FiledSetting')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'FiledSetting',
            'FiledSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class TimeDomainComputingCommandMenu:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        className="TimeDomainComputing"
        dlg=TimeDomainComputingSettingDlgMain.TimeDomainComputingSetting(className,"menu")
        dlg.show()
        dlg.exec_()
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/TimeDomainComputingMenu.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'TimeDomainComputingMenu',
            'TimeDomainComputing')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'TimeDomainComputingMenu',
            'TimeDomainComputing')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class TimeDomainComputingCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        className="TimeDomainComputing"
        dlg=TimeDomainComputingSettingDlgMain.TimeDomainComputingSetting(className,"toolBar")
        dlg.show()
        dlg.exec_()
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/TimeDomainComputingMenu.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'TimeDomainComputing',
            'Particle Merge')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'TimeDomainComputing',
            'Particle Merge')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


class DataProcessingSettingCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        className="DataProcessingSetting"
        dlg=DataProcessingSettingDlgMain.DataProcessingSetting(className)
        dlg.show()
        dlg.exec_()
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/DataProcessingSetting.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'DataProcessingSetting',
            'DataProcessingSetting')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'DataProcessingSetting',
            'DataProcessingSetting')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class ModelingInfoCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        className="ModelingInfo"
        dlg=ModelingInfoDlgMain.ModelingInfo(className)
        dlg.show()
        dlg.exec_()
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/ModelingInfo.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'ModelingInfo',
            'ModelingInfo')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'ModelingInfo',
            'ModelingInfo')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

class RunOptiosCommand:
    def Activated(self):
        if FreeCAD.activeDocument()==None:
            FreeCAD.newDocument()
        className="RunOptions"
        dlg=RunOptionsDlgMain.RunOptions(className)
        dlg.show()
        dlg.exec_()
        # className="WorkSpaceSettings"
        # dlg=WorkSpaceSettingDlgMain.show(className)        

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/ProjectSetting/ProjectSettingResources/RunOptions.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'RunOptions',
            'RunOptions')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'RunOptions',
            'RunOptions')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False


def getCooedinate():
    coordinate=FreeCAD.ActiveDocument.CoordinateSystem
    if coordinate == u'Rectangular':
        unitList = ["X", "Y", "Z", "mm", "mm", "mm"]
    elif coordinate == u'Polar':
        unitList = ["R", u"θ", "Z", "mm", "deg", "mm"]
    elif coordinate == u'Cylindrical':
        unitList = ["Z", "R", u"θ", "mm", "mm", "deg"]
    return unitList

FreeCADGui.addCommand('WorkSpaceSettings',WorkSpaceSettingsCommand())
FreeCADGui.addCommand('NewMaterical',NewMatericalCommand())
FreeCADGui.addCommand('FiledSetting',FiledSettingCommand())
FreeCADGui.addCommand('TimeDomainComputingMenu',TimeDomainComputingCommandMenu())
FreeCADGui.addCommand('TimeDomainComputing',TimeDomainComputingCommand())
FreeCADGui.addCommand('DataProcessingSetting',DataProcessingSettingCommand())
FreeCADGui.addCommand('ModelingInfo',ModelingInfoCommand())
FreeCADGui.addCommand('RunOptions',RunOptiosCommand())

