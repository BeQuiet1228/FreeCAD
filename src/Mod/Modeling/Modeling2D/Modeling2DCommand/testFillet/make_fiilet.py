# -*- coding: utf8 -*-
import FreeCAD as App
import Part
import math


# 这里是FreeCAD自带的求倒角，拿过来部分代码。可以自己重写优化一下。
PARAMGRP = App.ParamGet("User parameter:BaseApp/Preferences/Mod/Draft")
def precision():
    """Return the Draft precision setting."""
    precisionMax = 10
    precisionInt = PARAMGRP.GetInt("precision", 6)
    precisionInt = (precisionInt if precisionInt <= 10 else precisionMax)
    return precisionInt  # return PARAMGRP.GetInt("precision", 6)


def fillet(lEdges, r, chamfer=False):
    """Return a list of sorted edges describing a round corner.

    Author: Jacques-Antoine Gaudin
    """

    def getCurveType(edge, existingCurveType=None):
        """Build or complete a dictionary containing edges.

        The dictionary contains edges with keys 'Arc' and 'Line'.
        """
        if not existingCurveType:
            existingCurveType = {'Line': [],
                                 'Arc': []}
        if issubclass(type(edge.Curve), Part.LineSegment):
            existingCurveType['Line'] += [edge]
        elif issubclass(type(edge.Curve), Part.Line):
            existingCurveType['Line'] += [edge]
        elif issubclass(type(edge.Curve), Part.Circle):
            existingCurveType['Arc'] += [edge]
        else:
            raise ValueError("Edge's curve must be either Line or Arc")
        return existingCurveType

    rndEdges = lEdges[0:2]
    rndEdges = Part.__sortEdges__(rndEdges)

    if len(rndEdges) < 2:
        return rndEdges

    if r <= 0:
        print("DraftGeomUtils.fillet: Error: radius is negative.")
        return rndEdges

    curveType = getCurveType(rndEdges[0])
    curveType = getCurveType(rndEdges[1], curveType)

    lVertexes = rndEdges[0].Vertexes + [rndEdges[1].Vertexes[-1]]
    if len(curveType['Line']) == 2:
        # Deals with 2-line-edges lists
        U1 = lVertexes[0].Point.sub(lVertexes[1].Point)
        U1.normalize()

        U2 = lVertexes[2].Point.sub(lVertexes[1].Point)
        U2.normalize()

        alpha = U1.getAngle(U2)

        if chamfer:
            # correcting r value so the size of the chamfer = r
            beta = math.pi - alpha/2
            r = (r/2)/math.cos(beta)

        # Edges have same direction
        if (round(alpha, precision()) == 0
                or round(alpha - math.pi, precision()) == 0):
            print("DraftGeomUtils.fillet: Warning: "
                  "edges have same direction. Did nothing")
            return rndEdges

        dToCenter = r / math.sin(alpha/2.0)
        dToTangent = (dToCenter**2-r**2)**(0.5)
        dirVect = App.Vector(U1)
        dirVect.scale(dToTangent, dToTangent, dToTangent)
        arcPt1 = lVertexes[1].Point.add(dirVect)

        dirVect = U2.add(U1)
        dirVect.normalize()
        dirVect.scale(dToCenter - r, dToCenter - r, dToCenter - r)
        arcPt2 = lVertexes[1].Point.add(dirVect)

        # python赋值和引用迷惑了，所以再重写上面的变量
        # 圆弧的圆心坐标
        temp_arc_center = U2.add(U1)
        temp_arc_center.normalize()

        temp_arc_center.scale(dToCenter, dToCenter, dToCenter)
        arc_center = lVertexes[1].Point.add(temp_arc_center)

        dirVect = App.Vector(U2)
        dirVect.scale(dToTangent, dToTangent, dToTangent)
        arcPt3 = lVertexes[1].Point.add(dirVect)

        if (dToTangent > lEdges[0].Length) or (dToTangent > lEdges[1].Length):
            print("DraftGeomUtils.fillet: Error: radius value ", r,
                  " is too high")
            return rndEdges

        if chamfer:
            rndEdges[1] = Part.Edge(Part.LineSegment(arcPt1, arcPt3))
        else:
            rndEdges[1] = Part.Edge(Part.Arc(arcPt1, arcPt2, arcPt3))
            # 返回四个坐标，三个圆弧上的坐标，一个圆心上的坐标
            return [arcPt1, arcPt2, arcPt3, arc_center]

