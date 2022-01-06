# -*- coding: UTF-8 -*-
import FreeCADGui,FreeCAD
import DraftTools
def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

def Load(workbench):

    # fileList = ["Std_New"]
    # workbench.appendMenu('File', fileList)
    cmdlst2 = ["CreatePoint",
              "CreateConformalLine",
              "CreateObliqueLine",
              "CreateConformalArea",
              "CreateFunctionAreaCommand",
              "CreateRectangular",
              "CreatePolygonal",
              # "PolygonalCommand",
              "CreateConformal",
              "CreateAnnular",
              # "CreateTorusFace",
              "CreateCylinder",
              # "CreateCone",
              "CreateSpecialCone",
            #   "CreateTorus",
            #   "CreateOrthographicBody",
              "CreateParallelepipedal",
              "CreateSpherical",
              "CreateWedge",
              "CreatePyramid",
              "CreateRhombus",
              "CreateExtruded",
              "CreateTetrahedron",
              "CreateToroidal_Section",
              "CreateAnnular_Section",
              "CreateHelical",
              "CreateRevolutionCommand",
              "Object_Array",
              "CreateFunction",
              "CreateNewVolArrayCommand",
              "CreateNewDraftModeling_ExtrudeCommand",
              "CreateNewDraftModeling_RevolutionCommand",
              #"CreateArray",
              #"TestCommand"
              ]
    # "CreateFunction"]

    # 物理建模
    cmdlst_comboundary = ["Port", "Free", "Sym"]
    cmdlst_emit = ["EmB", "EmE", "EmG","Popu", "EmH", "EmT","Secd","Ioni"]
    cmdlst_spboundary = ["Sol", "Excitation power", "Foil", "Ind"]
    cmdlst_observe = ["Cntr", "Vec", "Pha", "Ran", "Obs"]
    cmdlst_Timer = ["TimerDef", "Timer"]

    workbench.appendMenu([QT_TRANSLATE_NOOP("Workbench","3D Modeling"), QT_TRANSLATE_NOOP("Workbench","Geometric Model")], cmdlst2)
    # 添加物理建模菜单栏
    workbench.appendMenu(["3D Modeling", QT_TRANSLATE_NOOP("Workbench","Common Boundary")], cmdlst_comboundary)
    workbench.appendMenu(["3D Modeling", QT_TRANSLATE_NOOP("Workbench","Emission Processing")], cmdlst_emit)
    workbench.appendMenu(["3D Modeling", QT_TRANSLATE_NOOP("Workbench","Special Boundary")], cmdlst_spboundary)
    workbench.appendMenu(["3D Modeling", QT_TRANSLATE_NOOP("Workbench","Observation")], cmdlst_observe)
    workbench.appendMenu(["3D Modeling", QT_TRANSLATE_NOOP("Workbench","SetTimer")], cmdlst_Timer)

####################################################ProjectSettings##########################################
    cmdProjectSettinglst=["ModelingInfo",
                          "WorkSpaceSettings",
                           "NewMaterical",
                           "FiledSetting",
                           "TimeDomainComputingMenu",
                           "DataProcessingSetting",
                           "RunOptions",
                           "Species"]
    # FreeCADGui.addLanguagePath("D:/PICGUI/buildD/Mod/Modeling/Modeling3D/modeling3DResources/translations")
    # FreeCAD.Console.PrintMessage("getLanguagePath: "+str(getLanguagePath()))
    FreeCADGui.addLanguagePath(getLanguagePath())
    FreeCADGui.updateLocale()
    workbench.appendMenu(QT_TRANSLATE_NOOP("Workbench","Project Settings"),cmdProjectSettinglst)

def getLanguagePath():
    import os
    return os.path.join(os.path.dirname(os.path.dirname(__file__)),"modeling3DResources/translations")