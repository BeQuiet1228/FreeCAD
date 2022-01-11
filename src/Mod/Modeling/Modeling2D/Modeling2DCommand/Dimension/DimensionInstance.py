# -*- coding: utf-8 -*-
import FreeCAD
import DraftVecUtils
from DraftTools import Creator, translate, msg, sys, getPoint, redraw3DView, Dimension
import DraftTools
import FreeCADGui
import FreeCAD
from Modeling.Modeling2D.Tools import Tools2D


class Dimension(DraftTools.Dimension):
    def createObject(self):
        "creates an object in the current doc"
        FreeCADGui.addModule("Draft")
        if self.angledata:
            normal = "None"
            if len(self.edges) == 2:
                import DraftGeomUtils
                v1 = DraftGeomUtils.vec(self.edges[0])
                v2 = DraftGeomUtils.vec(self.edges[1])
                normal = DraftVecUtils.toString((v1.cross(v2)).normalize())
            self.commit(translate("draft","Create Dimension"),
                        ['dim = Draft.makeAngularDimension(center='+DraftVecUtils.toString(self.center)+',angles=['+str(self.angledata[0])+','+str(self.angledata[1])+'],p3='+DraftVecUtils.toString(self.node[-1])+',normal='+normal+')',
                        'Draft.autogroup(dim)',
                        'asdasd = 1'])
        elif self.link and (not self.arcmode):
            ops = []
            if self.force == 1:
                self.commit(translate("draft","Create Dimension"),
                        ['dim = Draft.makeDimension(FreeCAD.ActiveDocument.'+self.link[0].Name+','+str(self.link[1])+','+str(self.link[2])+','+DraftVecUtils.toString(self.node[2])+')','dim.Direction=FreeCAD.Vector(0,1,0)',
                        'Draft.autogroup(dim)',
                         'asdasd = 2'])
            elif self.force == 2:
                self.commit(translate("draft","Create Dimension"),
                        ['dim = Draft.makeDimension(FreeCAD.ActiveDocument.'+self.link[0].Name+','+str(self.link[1])+','+str(self.link[2])+','+DraftVecUtils.toString(self.node[2])+')','dim.Direction=FreeCAD.Vector(1,0,0)',
                        'Draft.autogroup(dim)',
                         'asdasd = 3'])
            else:
                self.commit(translate("draft","Create Dimension"),
                        ['dim = Draft.makeDimension(FreeCAD.ActiveDocument.'+self.link[0].Name+','+str(self.link[1])+','+str(self.link[2])+','+DraftVecUtils.toString(self.node[2])+')',
                        'Draft.autogroup(dim)',
                         'asdasd = 4'])
        elif self.arcmode:
            self.commit(translate("draft","Create Dimension"),
                        ['dim = Draft.makeDimension(FreeCAD.ActiveDocument.'+self.link[0].Name+','+str(self.link[1])+',"'+str(self.arcmode)+'",'+DraftVecUtils.toString(self.node[2])+')',
                        'Draft.autogroup(dim)',
                         'asdasd = 5'])
        else:
            self.commit(translate("draft","Create Dimension"),
                        ['dim = Draft.makeDimension('+DraftVecUtils.toString(self.node[0])+','+DraftVecUtils.toString(self.node[1])+','+DraftVecUtils.toString(self.node[2])+')',
                        'Draft.autogroup(dim)',
                        'import Modeling',
                        'Modeling.Modeling2D.Modeling2DCommand.Dimension.DimensionInstance.setSize(dim)',
                        'Modeling.Modeling2D.Tools.InitDoc.addObjectToGroup_helper(dim, "AnnotationG", "注释")',
                         'dim.ViewObject.setEditorMode("DisplayMode", 2)'
                         ])
        if self.ui.continueMode:
            self.cont = self.node[2]
            if not self.dir:
                if self.link:
                    v1 = self.link[0].Shape.Vertexes[self.link[1]].Point
                    v2 = self.link[0].Shape.Vertexes[self.link[2]].Point
                    self.dir = v2.sub(v1)
                else:
                    self.dir = self.node[1].sub(self.node[0])
            self.node = [self.node[1]]
        self.link = None

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/测距.svg"
        MenuText = Tools2D.QT_TRANSLATE_NOOP(
            'CreateDimension',
            '测距')
        ToolTip = Tools2D.QT_TRANSLATE_NOOP(
            'CreateDimension',
            'Dimension')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}


FreeCADGui.addCommand("CreateDimension2D", Dimension())


def setSize(dim):
    # 根据网格大小调整
    gridObj = FreeCAD.ActiveDocument.DiyGrid
    gridSize = min(gridObj.gridSizeX, gridObj.gridSizeY)
    # 箭头
    dim.ViewObject.ArrowType = u"Arrow"
    # 箭头大小
    dim.ViewObject.ArrowSize = gridSize/(2.0*1000)
    # 字体大小
    dim.ViewObject.FontSize = gridSize*2/1000.0
    # 线宽
    dim.ViewObject.LineWidth = 1.0
    # 文本与线的距离
    dim.ViewObject.TextSpacing = 0.001
