# -*- coding: UTF-8 -*-
import FreeCADGui, FreeCAD
from Modeling.Modeling2D.Tools import Tools2D
import DraftTools


def Load(workbench):
    # cmdlst = ["Std_New"]
    # workbench.appendMenu('File', cmdlst)

    cmdProjectSettinglst = ["CreateModelInfo", "CreateNetStepSetting", "CreateFiledSetting", "CreateTimeDomainSetting", "CreateDataExportSetting", "CreateRunProcessingOptions"]
    FreeCADGui.addLanguagePath(getLanguagePath())
    FreeCADGui.updateLocale()
    workbench.appendMenu(Tools2D.QT_TRANSLATE_NOOP("Workbench", "Project Settings"), cmdProjectSettinglst)


def getLanguagePath():
    import os
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "modeling2DResources/translations")
