# encoding:utf-8
import math
import FreeCADGui
import FreeCAD
import Part
from Model3D.Tools import Tools3D, ObjectTools, ExpressionTools3D, InitDoc3D
from Model3D.Command3D.Model3DCommand.BaseUI import BaseDialogMain, BaseDialog


def new_getSelectionObj3D():
    """
    该函数为树结构双击时间所连接的槽函数，负责打开被双击物体的Dialog
    该函数被2D DisplayDialog的函数调用了
    """
    obj = FreeCADGui.Selection.getSelection()
    if len(obj) == 0:
        pass
    elif len(obj) == 1:
        from Model3D.Command3D import Model3DCommand, Physics3DCommand
        if 'Type' in obj[0].PropertiesList:
            Form = getFormByObj(obj[0])
            if Form is not None:
                # Form.show()
                Form.exec_()
        # 阵列体的baseObj的弹窗功能，暂时没有经过严格测试，不做发布
        else:
            """
            这里暂时只写入阵列体的baseObj的双击弹窗
            之后又其他的体需要baseObj的双击弹窗，可以参照
            """
            # 调取当前点击的obj对应的arry
            ArryObj = ObjectTools.getBaseTypeByType(ObjectTools.ObjectType.Vol_Array)

            if ArryObj.has_key(obj[0].Label) is not None:
                # 将最开始建立arry时删除的Type和Order属性添加到baseObj，致使baseObj的对话框弹出
                obj[0].addProperty("App::PropertyString", "Type").Type = ArryObj[obj[0].Label].BaseObjType
                obj[0].addProperty("App::PropertyInteger", "Order", "").Order = ArryObj[obj[0].Label].Order
                Form = getFormByObj(obj[0])
                Form.ui.spinBox_order.setEnabled(False)
                Form.exec_()
                if True:
                    # 至此baseObj对话框成功弹出，等待对话快关闭后，对baseObj做删除Type和Order及从分组中删除
                    # 整体目的：将baseObj调出用来更改arry模型，但caseObj不参与bool运算，并且不生成M3D，所以临时使用后要将其删除
                    group = obj[0].InList
                    obj[0].ViewObject.hide()
                    # 删除原group下的baseObj，这里的group[0]为阵列体，group[1]为baseObj
                    group[1].removeObject(obj[0])
                    # 删除Type属性和Order属性
                    obj[0].removeProperty("Type")
                    obj[0].removeProperty("Order")
                    # 将baseObj和arry都重新recompute，达到和FreeCADGui.runCommand("Refresh_3D")一样的效果，但不用将所有obj都遍历，节约时间
                    obj[0].recompute()
                    ArryObj[obj[0].Label].recompute()
                    FreeCADGui.runCommand("CreateM3D_new")
                    FreeCADGui.runCommand("UpdateBooleanCommand_3D")
    else:
        # 如果被选中数量大于一个，则不显示Dialog
        pass


def getFormByObj(obj):
    from Model3D.Command3D import Model3DCommand, Physics3DCommand
    Form = None
    if obj.Type == ObjectTools.ObjectType.Point:
        # 点
        Form = Model3DCommand.Point_3D.Point3DDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Line_Conformal:
        # 正投影线
        Form = Model3DCommand.Line_Conformal.LineConformalDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Line_Oblique:
        # 斜线
        Form = Model3DCommand.Line_Oblique.LineObliqueDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Area_Conformal:
        # 正投影面
        Form = Model3DCommand.Area_Conformal.AreaConformalDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Area_Rectangular:
        # 矩形面
        Form = Model3DCommand.Area_Rectangle.AreaRectangleDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Area_Polygonal:
        # 多边形面
        Form = Model3DCommand.Area_Polygonal.PolygonalDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Area_Function:
        # 函数面
        Form = Model3DCommand.Area_Function.AreaFunctionDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Conformal:
        # 正投影体
        Form = Model3DCommand.Vol_Conformal.ConformalDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_SpecialCone:
        # 圆台
        Form = Model3DCommand.Vol_SpecialCone.SpecialConeDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Cylinder:
        # 圆柱
        Form = Model3DCommand.Vol_Cylinder.CylinderDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Parallelepipedal:
        # 平行六面体
        Form = Model3DCommand.Vol_Parallelepipedal.ParallelepipedalDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Annular:
        # 环形体
        Form = Model3DCommand.Vol_Annular.AnnularDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Pyramid:
        # 金字塔体
        Form = Model3DCommand.Vol_Pyramid.PyramidDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Rhombus:
        # 菱形体
        Form = Model3DCommand.Vol_Rhombus.RhombusDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Spherical:
        # 球
        Form = Model3DCommand.Vol_Spherical.SphericalDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Wedge:
        # 锲形体
        Form = Model3DCommand.Vol_Wedge.WedgeDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Tetrahedron:
        # 四面体
        Form = Model3DCommand.Vol_Tetrahedron.TetrahedronDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Toroidal_Section:
        # 圆环区域体
        Form = Model3DCommand.Vol_Toroidal_Section.Toroidal_SectionDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Annular_Section:
        # 环形区域体
        Form = Model3DCommand.Vol_Annular_Section.Annular_SectionDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Function:
        # 函数体
        Form = Model3DCommand.Vol_Function.FunctionDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Extruded:
        # 挤出体
        Form = Model3DCommand.Vol_Extruded.ExtrudedDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Helical:
        # 螺旋体
        Form = Model3DCommand.Vol_Helical.HelicalDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Array:
        # 阵列体
        Form = Model3DCommand.Object_Array.ObjectArrayDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Draft_Revolution:
        # 草图旋转体
        Form = Model3DCommand.Draft_Revolution.DraftRevolutionDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Revolution:
        # 旋转体
        Form = Model3DCommand.Vol_Revolution.RevolutionDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_ParamArray:
        # 参数阵列体
        Form = Model3DCommand.Vol_Array.ArrayDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vol_Draft_Extrude:
        Form = Model3DCommand.Draft_Extruded.DraftExtrudedDialogMain.ShowDialog(obj)
    # 边界设置
    elif obj.Type == ObjectTools.ObjectType.SOLE:
        # 螺旋线圈
        Form = Physics3DCommand.Solend.SolendDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.DRIV:
        # 空间电流源
        Form = Physics3DCommand.Driv.DrivDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.FOIL:
        # 泊片
        Form = Physics3DCommand.Foil.FoilDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.IND:
        # 电感
        Form = Physics3DCommand.Inductor.InductorDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.PORT:
        Form = Physics3DCommand.Port.PortDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.FREE:
        # 吸收边界
        Form = Physics3DCommand.FreeSpace.FreeSpaceDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.SYMT:
        # 对称边界
        Form = Physics3DCommand.Sysmtry.SymtryDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.MARK:
        # Mark设置
        Form = Physics3DCommand.Mark.MarkDialogMain.ShowDialog(obj)
    # 发射处理
    elif obj.Type == ObjectTools.ObjectType.BEAM:
        # 束发射
        Form = Physics3DCommand.Beam.BeamDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.EXPS:
        # 爆炸式发射
        Form = Physics3DCommand.Exps.ExpsDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.GYRO:
        # 回旋发射
        Form = Physics3DCommand.Gyro.GyroDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.POPU:
        # 粒子设置
        Form = Physics3DCommand.Popu.PopuDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.FELD:
        # 强场发射
        Form = Physics3DCommand.Feld.FeldDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.THER:
        # 热致发射
        Form = Physics3DCommand.Ther.TherDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.SECD:
        # 二次发射
        Form = Physics3DCommand.Secd.SecdDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.IONI:
        # 气体电离
        Form = Physics3DCommand.Ioni.IoniDialogMain.ShowDialog(obj)
    # 观测设置
    elif obj.Type == ObjectTools.ObjectType.CNTR:
        Form = Physics3DCommand.Cntr.CntrDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Vector:
        Form = Physics3DCommand.Vector.VectorDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.PhasSpace:
        Form = Physics3DCommand.PhasSpace.PhasSpaceDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.AreaRan:
        Form = Physics3DCommand.AreaRan.AreaRanDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Observe or obj.Type == "Observe":
        Form = Physics3DCommand.Observe.ObserveDialogMain.ShowDialog(obj)
    # 定时器
    elif obj.Type == ObjectTools.ObjectType.DefaultTimer:
        Form = Physics3DCommand.DefTimer.DefTimerDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.CustomTimer:
        Form = Physics3DCommand.CustomTimer.CustomTimerDialogMain.ShowDialog(obj)
    # 工程设置
    elif obj.Type == ObjectTools.ObjectType.Info:
        Form = Physics3DCommand.ModelingInfo.ModelingInfoDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.Simu:
        Form = Physics3DCommand.NetStepSetting.NetStepSettingDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.NewMaterial:
        Form = Physics3DCommand.NewMaterial.NewMaterialDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.FieldSetting:
        Form = Physics3DCommand.FieldSetting.FieldSettingDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.TimeDomain:
        Form = Physics3DCommand.TimeDomainSetting.TimeDomainSettingDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.DataProcess:
        Form = Physics3DCommand.DataProcessingSetting.DataProcessingSettingDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.RunOptions:
        Form = Physics3DCommand.RunOptions.RunOptionsDialogMain.ShowDialog(obj)
    elif obj.Type == ObjectTools.ObjectType.NewParticle:
        Form = Physics3DCommand.ParticleDefine.ParticleDefineDialogMain.ShowDialog(obj)
    # 宏粒子合并
    elif obj.Type == ObjectTools.ObjectType.MacroParticle:
        Form = Physics3DCommand.MacroParticle.MacroParticleDialogMain.ShowDialog(obj)
    return Form
