# -*- coding: utf-8 -*-
import FreeCADGui
import Draft
import DraftVecUtils
import DraftTools
import DraftGui
import FreeCAD
class RegularPolygon(DraftTools.Polygon):
    def drawPolygon(self):
        "actually draws the FreeCAD object"
        rot,sup,pts,fil = self.getStrings()
        if Draft.getParam("UsePartPrimitives",False):
            self.commit(DraftGui.translate("draft","Create Polygon"),
                        ['import Part',
                         'pl=FreeCAD.Placement()',
                         'pl.Rotation.Q=' + rot,
                         'pl.Base=' + DraftVecUtils.toString(self.center),
                         'pol = FreeCAD.ActiveDocument.addObject("Part::RegularPolygon","RegularPolygon")',
                         'pol.Polygon = ' + str(self.ui.numFaces.value()),
                         'pol.Circumradius = ' + str(self.rad),
                         'pol.Placement = pl',
                         'Draft.autogroup(pol)'
                         'FreeCAD.ActiveDocument.recompute()'])
        else:
            # building command string
            FreeCADGui.addModule("Draft")
            FreeCADGui.addModule("Modeling")
            FreeCADGui.doCommand("from Modeling.Modeling2D import Modeling2DCommand")
            self.commit(DraftGui.translate("draft","Create Polygon"),
                        ['pl=FreeCAD.Placement()',
                         'pl.Rotation.Q = ' + rot,
                         'pl.Base = ' + DraftVecUtils.toString(self.center),
                         'pol = Draft.makePolygon(' + str(self.ui.numFaces.value()) + ',radius=' + str(self.rad) + ',inscribed=True,placement=pl,face=' + fil + ',support=' + sup + ')',
                         'Draft.autogroup(pol)',
                         'Modeling2DCommand.CallBack.CallBackTools.processObject(pol, \"RegularPolygon\")',
                         'Form = Modeling2DCommand.RegularPolygon.RegularPolygonDlgMain.ShowCircularDialog(pol)',
                         'Form.show()'
                         ])
        FreeCAD.ActiveDocument.recompute()
        self.finish(cont=True)
    pass
FreeCADGui.addCommand('RegularPolygon_2D', RegularPolygon())