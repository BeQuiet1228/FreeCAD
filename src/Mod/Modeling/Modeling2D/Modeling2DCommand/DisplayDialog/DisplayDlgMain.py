# encoding:utf-8
import FreeCAD
import FreeCADGui

from Modeling.Common.Tools import ObjectsTools
from Modeling.Modeling2D.Tools import Tools2D
from Model3D.Command3D.Model3DCommand.DoubleClickShowDialog import ReShowDialogMain


def slotDoubleClicked():
    """
    该函数为树结构双击时间所连接的槽函数，负责打开被双击物体的Dialog
    信号相关代码在C++
    """
    if FreeCAD.ActiveDocument.Comment == "2D":
        getSelectionObj2D()
    # 3D新版本
    else:
        ReShowDialogMain.new_getSelectionObj3D()


def getSelectionObj2D():
    obj = FreeCADGui.Selection.getSelection()
    if len(obj) == 0:
        pass
    elif len(obj) == 1:
        from Modeling.Modeling2D import Modeling2DCommand
        # 只有有Type属性的obj才有对应的Dialog，除了Annotation
        if 'Type' in obj[0].PropertiesList:
            Form = None
            # 变量
            if obj[0].Type == Tools2D.ObjectType.Variable:
                pass
            # 体
            elif obj[0].Type == Tools2D.ObjectType.Point:
                Form = Modeling2DCommand.Point.PointDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.Line:
                Form = Modeling2DCommand.Line.LineDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.LineConformal:
                Form = Modeling2DCommand.LineConformal.LineConformalDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.AreaPolygonal:
                Form = Modeling2DCommand.Wire.WireDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.AreaCircular:
                Form = Modeling2DCommand.Circular.CircularDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.AreaConformal:
                Form = Modeling2DCommand.AreaConformal.AreaConformalDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.Rectangle:
                Form = Modeling2DCommand.Rectangle.RectangleDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.Sector:
                Form = Modeling2DCommand.Sector.SectorDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.Fillet:
                Form = Modeling2DCommand.Fillet.FilletDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.AreaFunction:
                Form = Modeling2DCommand.AreaFunction.AreaFunctionDlgMain.ShowDialog(obj[0])
            # 边界设置
            elif obj[0].Type == Tools2D.ObjectType.SOLE:
                pass
            elif obj[0].Type == Tools2D.ObjectType.DRIV:
                Form = Modeling2DCommand.Driv.DrivDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.FOIL:
                Form = Modeling2DCommand.Foil.FoilDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.IND:
                Form = Modeling2DCommand.Inductor.IndDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.PORT:
                Form = Modeling2DCommand.Port.PortDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.FREE:
                Form = Modeling2DCommand.FreeSpace.FreeDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.SYMT:
                Form = Modeling2DCommand.Symtry.SymtryDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.MARK:
                Form = Modeling2DCommand.Mark.MarkDialogMain.ShowDialog(obj[0])
            # 发射处理
            elif obj[0].Type == Tools2D.ObjectType.BEAM:
                Form = Modeling2DCommand.Beam.BeamDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.EXPS:
                Form = Modeling2DCommand.Exps.ExpsDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.GYRO:
                Form = Modeling2DCommand.Gyro.GyroDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.POPU:
                Form = Modeling2DCommand.Popu.PopuDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.FELD:
                Form = Modeling2DCommand.Feld.FeldDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.THER:
                Form = Modeling2DCommand.Ther.TherDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.SECD:
                Form = Modeling2DCommand.Secd.SecdDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.IONI:
                Form = Modeling2DCommand.Ioni.IoniDlgMain.ShowDialog(obj[0])
            # 观测设置
            elif obj[0].Type == Tools2D.ObjectType.CNTR:
                Form = Modeling2DCommand.Cntr.CntrDlgMain.ShowDialog(obj[0])
                pass
            elif obj[0].Type == Tools2D.ObjectType.Vector:
                Form = Modeling2DCommand.Vector.VectorDlgMain.ShowDialog(obj[0])
                pass
            elif obj[0].Type == Tools2D.ObjectType.PhasSpace:
                Form = Modeling2DCommand.PhasSpace.PhasSpaceDlgMain.ShowDialog(obj[0])
                pass
            elif obj[0].Type == Tools2D.ObjectType.AreaRan:
                Form = Modeling2DCommand.AreaRan.AreaRanDlgMain.ShowDialog(obj[0])
                pass
            elif obj[0].Type == Tools2D.ObjectType.Observe:
                Form = Modeling2DCommand.Observe.ObserveDlgMain.ShowDialog(obj[0])
                pass
            # 定时器
            elif obj[0].Type == Tools2D.ObjectType.DefaultTimer:
                Form = Modeling2DCommand.DefTimer.DefTimerDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.Timer:
                Form = Modeling2DCommand.CustomTimer.CustomTimerDlgMain.ShowDialog(obj[0])
            # 新材料
            elif obj[0].Type == Tools2D.ObjectType.NewMaterial:
                Form = Modeling2DCommand.NewMaterial.NewMaterialDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.NewParticle:
                Form = Modeling2DCommand.ParticleDefine.ParticleDefineDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.MarcoParticle:
                Form = Modeling2DCommand.MacroParticle.MarcoParticleDlgMain.ShowDialog(obj[0])
            # 工程设置
            elif obj[0].Type == Tools2D.ObjectType.Info:
                Form = Modeling2DCommand.ModelInfo.ModelInfoDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.Simu:
                Form = Modeling2DCommand.NetStepSetting.NetStepSettingDialogMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.TimeDomain:
                Form = Modeling2DCommand.TimeDomainSetting.TimeDomainSettingDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.DataProcess:
                Form = Modeling2DCommand.DataExportSetting.DataExportSettingDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.RunOptions:
                Form = Modeling2DCommand.RunProcessingOptions.RunProcessingOptionsDlgMain.ShowDialog(obj[0])
            elif obj[0].Type == Tools2D.ObjectType.FieldSetting:
                Form = Modeling2DCommand.FiledSetting.FiledSettingDialogMain.ShowDialog(obj[0])
            if Form is not None:
                # Form.show()
                Form.exec_()
        else:
            if obj[0].TypeId == 'App::Annotation':
                Form = Modeling2DCommand.Text.TextDlgMain.ShowDialog(obj[0])
                Form.exec_()
    else:
        # 如果被选中数量大于一个，则不显示Dialog
        pass


def getSelectionObj3D():
    obj = FreeCADGui.Selection.getSelection()
    # FreeCAD.Console.PrintError('obj')
    if len(obj)==0:
        pass
    elif len(obj)==1:
        from Modeling.Modeling3D import Modeling3DCommand
        if 'Type' in obj[0].PropertiesList:
            if obj[0].Type != ObjectsTools.ObjectType.Point and \
               obj[0].Type != ObjectsTools.ObjectType.Line_Conformal and \
               obj[0].Type != ObjectsTools.ObjectType.Line_Oblique:
                FreeCADGui.SendMsgToActiveView("ViewSelection")

            if obj[0].Type==ObjectsTools.ObjectType.Point:
                Form=Modeling3DCommand.Point.PointNewDialog.reshowPointDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Line_Conformal :
                # addGroupForObj(obj[0],"Line","线")
                Form=Modeling3DCommand.Line_Conformal.ConformalLineNewDialog.reshowConformalLineDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Line_Oblique :
                Form=Modeling3DCommand.Line_Oblique.ObliqueLineNewDialog.reshowObliqueLineDialog(obj[0])
                Form.show()
                Form.exec_()
            elif obj[0].Type==ObjectsTools.ObjectType.Area_Conformal :
                # addGroupForObj(obj[0],"Area","面")
                Form=Modeling3DCommand.Area_Conformal.ConformalAreaNewDialog.reshowConformalAreaDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            # @fubiao
            elif obj[0].Type==ObjectsTools.ObjectType.Area_Function:
                Form=Modeling3DCommand.Area_Function.AreaFunctionDlgMain.AreaFunctionDlgMain(obj[0])
                Form.show()
                Form.exec_()
            elif obj[0].Type==ObjectsTools.ObjectType.Area_Polygonal:
                Form=Modeling3DCommand.Area_Polygonal.PolygonalNewDialog.reshowPolygonalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Area_Rectangular:
                Form=Modeling3DCommand.Area_Rectangular.RectangularAreaNewDialog.reshowRectangularAreaDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Annular:
                # addGroupForObj(obj[0],"Annular","环形体")
                Form=Modeling3DCommand.Vol_Annular.AnnularNewDialog.reshowAnnularDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Annular_Section:
                # addGroupForObj(obj[0],"Annular_Section","环形区域体")
                Form=Modeling3DCommand.Vol_Annular_Section.AnnularSectionNewDialog.reshowAnnularSectionDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Conformal:
                # addGroupForObj(obj[0],"Conformal","正投影体")
                Form=Modeling3DCommand.Vol_Conformal.ConformalNewDialog.reshowConformalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Cylinder:
                # Form=Modeling3DCommand.Vol_Cylinder.CylinderNewDialog.showCylinderDialog(obj[0])
                Form=Modeling3DCommand.Vol_Cylinder.CylinderNewDialog.reshowCylinderDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Extruded:
                # addGroupForObj(obj[0],"Extruded","挤出体")
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Function:
                # addGroupForObj(obj[0],"Function","函数体")
                Form=Modeling3DCommand.Vol_Function.FunctionNewDialog.reshowFunctionDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Helical:
                # addGroupForObj(obj[0],"Helical","螺旋体")
                Form=Modeling3DCommand.Vol_Helical.HelicalNewDialog.reshowHelicalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Parallelepipedal:
                # addGroupForObj(obj[0],"Parallelepipedal","平行六面体")
                Form=Modeling3DCommand.Vol_Parallelepipedal.ParallelepipedalNewDialog.reshowParallelepipedalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Pyramid:
                # addGroupForObj(obj[0],"Pyramid","金字塔体")
                Form=Modeling3DCommand.Vol_Pyramid.PyramidNewDialog.reshowPyramidDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Rhombus:
                # addGroupForObj(obj[0],"Rhombus","菱形体")
                Form=Modeling3DCommand.Vol_Rhombus.RhombusNewDialog.reshowRhombusDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_SpecialCone:
                # addGroupForObj(obj[0],"SpecialCone","圆锥体")
                Form=Modeling3DCommand.Vol_SpecialCone.SpecicalConeNewDialog.reshowSpecialConeDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Spherical:
                # addGroupForObj(obj[0],"Spherical","球体")
                Form=Modeling3DCommand.Vol_Spherical.SphericalNewDialog.reshowSphericalDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Tetrahedron:
                # addGroupForObj(obj[0],"Tetrahedron","四面体")
                Form=Modeling3DCommand.Vol_Tetrahedron.TetrahedronNewDialog.reshowTetrahedronDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Toroidal_Section:
                # addGroupForObj(obj[0],"Toroidal_Section","半圆环体")
                Form=Modeling3DCommand.Vol_Toroidal_Section.ToroidalSectionNewDialog.reshowToroidalSectionDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Wedge:
                # addGroupForObj(obj[0],"Wedge","楔形体")
                Form=Modeling3DCommand.Vol_Wedge.WedgeNewDialog.reshowWedgeDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Array:
                # addGroupForObj(obj[0],"Array","阵列体")
                Form=Modeling3DCommand.Object_Array.ArrayNewDialog.reshowArrayDialog(obj[0])
                Form.show()
                Form.exec_()
                pass
            #@fubiao
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_ParamArray:
                From=Modeling3DCommand.Vol_Array.Command.Vol_Array_Dlg_Main.VolArray(obj=obj[0])
                From.show()
                From.exec_()
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Draft_Extrude:
                Modeling3DCommand.DraftModeling_Extrude.Command.DraftModeling_ExtrudeDlgMain.CreateNewDraftModeling_ExtrudeCommand().Activated()
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Draft_Revolution:
                Modeling3DCommand.DraftModeling_Revolution.Command.DraftModeling_RevolutionDlgMain.CreateNewDraftModeling_RevolutionCommand().Activated()
            elif obj[0].Type==ObjectsTools.ObjectType.Vol_Revolution:
                import Modeling.Modeling3D.Modeling3DCommand.Vol_Revolution.Command.RevolutionDlgMain
                From=Modeling3DCommand.Vol_Revolution.Command.RevolutionDlgMain.VolRevolotion(obj=obj[0])
                From.show()
                From.exec_()
                pass

    elif len(obj)>1:
        pass
    pass
