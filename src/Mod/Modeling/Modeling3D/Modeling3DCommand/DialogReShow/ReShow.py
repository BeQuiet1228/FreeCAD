# encoding:utf-8
import FreeCAD
import FreeCADGui

#fubiao
import PySide
from PySide import QtCore, QtGui
import os
import Units
from Modeling.Common.Tools.ObjectsTools import *

def getSelectionobj():
    obj = Gui.Selection.getSelection()
    # FreeCAD.Console.PrintError('obj')
    if len(obj)==0:
        pass
    elif len(obj)==1:
        from Modeling.Modeling3D import Modeling3DCommand
        if 'Type' in obj[0].PropertiesList:
            if obj[0].Type==ObjectType.Point:
                Form=Modeling3DCommand.Point.PointNewDialog.reshowPointDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Line_Conformal :
                # addGroupForObj(obj[0],"Line","线")
                Form=Modeling3DCommand.Line_Conformal.ConformalLineNewDialog.reshowConformalLineDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Line_Oblique :
                Form=Modeling3DCommand.Line_Oblique.ObliqueLineNewDialog.reshowObliqueLineDialog(obj[0])
                Form.show()
                Form.exec_()
            elif obj[0].Type==ObjectType.Area_Conformal :
                # addGroupForObj(obj[0],"Area","面")
                Form=Modeling3DCommand.Area_Conformal.ConformalAreaNewDialog.reshowConformalAreaDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            # @fubiao
            elif obj[0].Type==ObjectType.Area_Function:
                Form=Modeling3DCommand.Area_Function.AreaFunctionDlgMain.AreaFunctionDlgMain(obj[0])
                Form.show()
                Form.exec_()
            elif obj[0].Type==ObjectType.Area_Polygonal:
                Form=Modeling3DCommand.Area_Polygonal.PolygonalNewDialog.reshowPolygonalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Area_Rectangular:
                Form=Modeling3DCommand.Area_Rectangular.RectangularAreaNewDialog.reshowRectangularAreaDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Annular:
                # addGroupForObj(obj[0],"Annular","环形体")
                Form=Modeling3DCommand.Vol_Annular.AnnularNewDialog.reshowAnnularDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Annular_Section:
                # addGroupForObj(obj[0],"Annular_Section","环形区域体")
                Form=Modeling3DCommand.Vol_Annular_Section.AnnularSectionNewDialog.reshowAnnularSectionDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Conformal:
                # addGroupForObj(obj[0],"Conformal","正投影体")
                Form=Modeling3DCommand.Vol_Conformal.ConformalNewDialog.reshowConformalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Cylinder:
                # Form=Modeling3DCommand.Vol_Cylinder.CylinderNewDialog.showCylinderDialog(obj[0])
                Form=Modeling3DCommand.Vol_Cylinder.CylinderNewDialog.reshowCylinderDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Extruded:
                # addGroupForObj(obj[0],"Extruded","挤出体")
                pass
            elif obj[0].Type==ObjectType.Vol_Function:
                # addGroupForObj(obj[0],"Function","函数体")
                Form=Modeling3DCommand.Vol_Function.FunctionNewDialog.reshowFunctionDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Helical:
                # addGroupForObj(obj[0],"Helical","螺旋体")
                Form=Modeling3DCommand.Vol_Helical.HelicalNewDialog.reshowHelicalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Parallelepipedal:
                # addGroupForObj(obj[0],"Parallelepipedal","平行六面体")
                Form=Modeling3DCommand.Vol_Parallelepipedal.ParallelepipedalNewDialog.reshowParallelepipedalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Pyramid:
                # addGroupForObj(obj[0],"Pyramid","金字塔体")
                Form=Modeling3DCommand.Vol_Pyramid.PyramidNewDialog.reshowPyramidDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Rhombus:
                # addGroupForObj(obj[0],"Rhombus","菱形体")  
                Form=Modeling3DCommand.Vol_Rhombus.RhombusNewDialog.reshowRhombusDialog(obj[0])
                Form.show()
                Form.exec_()
                pass  
            elif obj[0].Type==ObjectType.Vol_SpecialCone:
                # addGroupForObj(obj[0],"SpecialCone","圆锥体")
                Form=Modeling3DCommand.Vol_SpecialCone.SpecicalConeNewDialog.reshowSpecialConeDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Spherical:
                # addGroupForObj(obj[0],"Spherical","球体")
                Form=Modeling3DCommand.Vol_Spherical.SphericalNewDialog.reshowSphericalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Tetrahedron:
                # addGroupForObj(obj[0],"Tetrahedron","四面体")
                Form=Modeling3DCommand.Vol_Tetrahedron.TetrahedronNewDialog.reshowTetrahedronDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Toroidal_Section:
                # addGroupForObj(obj[0],"Toroidal_Section","半圆环体")
                Form=Modeling3DCommand.Vol_Toroidal_Section.ToroidalSectionNewDialog.reshowToroidalSectionDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Wedge:
                # addGroupForObj(obj[0],"Wedge","楔形体")
                Form=Modeling3DCommand.Vol_Wedge.WedgeNewDialog.reshowWedgeDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectType.Vol_Array:
                # addGroupForObj(obj[0],"Array","阵列体")
                Form=Modeling3DCommand.Object_Array.ArrayNewDialog.reshowArrayDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            #@fubiao
            elif obj[0].Type==ObjectType.Vol_ParamArray:
                From=Modeling3DCommand.Vol_Array.Command.Vol_Array_Dlg_Main.VolArray(obj=obj[0])
                From.show()
                From.exec_()
            elif obj[0].Type==ObjectType.Vol_Draft_Extrude:
                Modeling3DCommand.DraftModeling_Extrude.Command.DraftModeling_ExtrudeDlgMain.CreateNewDraftModeling_ExtrudeCommand().Activated()
            elif obj[0].Type==ObjectType.Vol_Draft_Revolution:
                Modeling3DCommand.DraftModeling_Revolution.Command.DraftModeling_RevolutionDlgMain.CreateNewDraftModeling_RevolutionCommand().Activated()
            elif obj[0].Type==ObjectType.Vol_Revolution:
                import Modeling.Modeling3D.Modeling3DCommand.Vol_Revolution.Command.RevolutionDlgMain
                From=Modeling3DCommand.Vol_Revolution.Command.RevolutionDlgMain.VolRevolotion(obj=obj[0])
                From.show()
                From.exec_()
                pass

    elif len(obj)>1:
        pass
    pass
