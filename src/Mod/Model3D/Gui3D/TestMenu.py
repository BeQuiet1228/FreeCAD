# -*- coding: UTF-8 -*-
import FreeCADGui, FreeCAD
from Model3D.Tools import Tools3D


def Load(workbench):
    cmdProjectSettinglst = ["CreateModelInfo", "CreateNetStepSetting", "CreateFiledSetting", "CreateTimeDomainSetting",
                            "CreateDataExportSetting", "CreateRunProcessingOptions"]
    FreeCADGui.addLanguagePath(getLanguagePath())
    FreeCADGui.updateLocale()
    workbench.appendMenu(Tools3D.QT_TRANSLATE_NOOP("Workbench", "Project Settings"), cmdProjectSettinglst)


def getLanguagePath():
    import os
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "modeling2DResources/translations")