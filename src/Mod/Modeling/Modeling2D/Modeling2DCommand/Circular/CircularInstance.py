# -*- coding: utf-8 -*-
import math

import Draft
import DraftTools, DraftVecUtils
import FreeCADGui
import DraftGui
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D


class Circular2D(DraftTools.Circle):
    def __init__(self):
        DraftTools.Circle.__init__(self)

    def drawArc(self):
        "actually draws the FreeCAD object"
        rot,sup,pts,fil = self.getStrings()
        if self.closedCircle:
            try:
                if Draft.getParam("UsePartPrimitives",False):
                    # use primitive
                    self.commit(DraftGui.translate("draft","Create Circle"),
                                ['circle = FreeCAD.ActiveDocument.addObject("Part::Circle","Circle")',
                                 'circle.Radius = '+str(self.rad),
                                 'pl = FreeCAD.Placement()',
                                 'pl.Rotation.Q = '+rot,
                                 'pl.Base = '+DraftVecUtils.toString(self.center),
                                 'circle.Placement = pl',
                                 'Draft.autogroup(circle)'])
                else:
                    # building command string
                    FreeCADGui.addModule("Draft")
                    FreeCADGui.addModule("Modeling")
                    FreeCADGui.doCommand("from Modeling.Modeling2D import Modeling2DCommand")
                    self.commit(DraftGui.translate("draft","Create Circle"),
                                ['pl=FreeCAD.Placement()',
                                 'pl.Rotation.Q='+rot,
                                 'pl.Base='+DraftVecUtils.toString(self.center),
                                 'circle = Draft.makeCircle(radius='+str(self.rad)+',placement=pl,face='+fil+',support='+sup+')',
                                 'Draft.autogroup(circle)',
                                 'Modeling2DCommand.CallBack.CallBackTools.processObject(circle, "Circular")',
                                 'Form = Modeling2DCommand.Circular.CircularDlgMain.ShowDialog(circle, True)',
                                 'Modeling2DCommand.Circular.CircularInstance.CircularProxy(circle)',
                                 'Form.show()'])
            except:
                print("Draft: error delaying commit")
        else:
            sta = math.degrees(self.firstangle)
            end = math.degrees(self.firstangle+self.angle)
            if end < sta: sta,end = end,sta
            while True:
                if sta > 360:
                    sta = sta - 360
                elif end > 360:
                    end = end - 360
                else:
                    break
            try:
                if Draft.getParam("UsePartPrimitives",False):
                    # use primitive
                    self.commit(DraftGui.translate("draft","Create Arc"),
                                ['circle = FreeCAD.ActiveDocument.addObject("Part::Circle","Circle")',
                                 'circle.Radius = '+str(self.rad),
                                 'circle.Angle0 = '+str(sta),
                                 'circle.Angle1 = '+str(end),
                                 'pl = FreeCAD.Placement()',
                                 'pl.Rotation.Q = '+rot,
                                 'pl.Base = '+DraftVecUtils.toString(self.center),
                                 'circle.Placement = pl',
                                 'Draft.autogroup(circle)'])
                else:
                    # building command string
                    FreeCADGui.addModule("Draft")
                    self.commit(DraftGui.translate("draft","Create Arc"),
                                ['pl=FreeCAD.Placement()',
                                 'pl.Rotation.Q='+rot,
                                 'pl.Base='+DraftVecUtils.toString(self.center),
                                 'circle = Draft.makeCircle(radius='+str(self.rad)+',placement=pl,face='+fil+',startangle='+str(sta)+',endangle='+str(end)+',support='+sup+')',
                                 'Draft.autogroup(circle)'])
            except:
                    print("Draft: error delaying commit")
        self.finish(cont=True)

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2d圆形.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateCircular',
            '圆形面')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateCircular',
            'Circular')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand("CreateCircular2D", Circular2D())


class CircularProxy:
    def __init__(self, obj):
        """
        草图圆创建时就存在代理，在此处添加代理会覆盖原有代理，
        所以将原有的execute添加到该代理处
        """
        obj.Proxy = self

    def onChanged(self, fp, prop):
        if prop == "x_helper":
            fp.Placement.Base.x = fp.x_helper.Value
        if prop == "y_helper":
            fp.Placement.Base.y = fp.y_helper.Value

    def execute(self, obj):
        import Part
        plm = obj.Placement
        shape = Part.makeCircle(obj.Radius.Value,FreeCAD.Vector(0,0,0),FreeCAD.Vector(0,0,1),obj.FirstAngle.Value,obj.LastAngle.Value)
        if obj.FirstAngle.Value == obj.LastAngle.Value:
            shape = Part.Wire(shape)
            if hasattr(obj,"MakeFace"):
                if obj.MakeFace:
                    shape = Part.Face(shape)
            else:
                shape = Part.Face(shape)
        obj.Shape = shape
        obj.Placement = plm
        obj.positionBySupport()
        # 根据Attribute来设置模型的颜色，此处对源码进行了修改 @lzg
        from Modeling.Modeling2D.Tools import ToolsForDisplay
        ToolsForDisplay.setColors(obj)
