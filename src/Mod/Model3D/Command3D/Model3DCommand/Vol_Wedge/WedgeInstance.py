# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui
import Part
from Model3D.Tools import Tools3D, ObjectTools, InitDoc3D


class CreateWedge:
    def __init__(self, obj):
        obj.Proxy = self

    def onChanged(self, fp, prop):
        pass

    def execute(self, fp):
        """
          排除三点重合无法形成图形的情况，再排除无法形成底面的情况，然后按点的顺序连线形成面再形成体建模。知道楔形体具体要求后还需补充后续错误处理。
          此种建模point5和point6必须按顺序，否则建模错误。此限制询问老师后看是否要完善更改。
           上面一条线必须与下面的平行，此错误判断需要在后续补充。
           楔形体不了解实际的图形要求，目前只进行了初步错误判断，需要在询问老师后补充更多的错误判断。
            """
        try:
            point1 = Tools3D.transToRecVector(fp.Point1X.Value, fp.Point1Y.Value, fp.Point1Z.Value)
            point2 = Tools3D.transToRecVector(fp.Point2X.Value, fp.Point2Y.Value, fp.Point2Z.Value)
            point3 = Tools3D.transToRecVector(fp.Point3X.Value, fp.Point3Y.Value, fp.Point3Z.Value)
            point4 = Tools3D.transToRecVector(fp.Point4X.Value, fp.Point4Y.Value, fp.Point4Z.Value)
            point5 = Tools3D.transToRecVector(fp.Point5X.Value, fp.Point5Y.Value, fp.Point5Z.Value)
            point6 = Tools3D.transToRecVector(fp.Point6X.Value, fp.Point6Y.Value, fp.Point6Z.Value)

            if point1 == point2 and point1 == point4:
                # 警告用户数据错误及错误原因
                pass
            if point2 == point4 and point2 == point3:
                # 警告用户数据错误及错误原因
                pass
            if point2 == point1 and point2 == point5:
                # 警告用户数据错误及错误原因
                pass
            if point3 == point5 and point3 == point4:
                # 警告用户数据错误及错误原因
                pass
            if point1 == point5 and point1 == point4:
                # 警告用户数据错误及错误原因
                pass
            if point2 == point5 and point3 == point2:
                # 警告用户数据错误及错误原因
                pass
            if point2 == point3 and point3 == point6:
                # 警告用户数据错误及错误原因
                pass
            if point2 == point5 and point6 == point2:
                # 警告用户数据错误及错误原因
                pass
            if point6 == point5 and point3 == point6:
                # 警告用户数据错误及错误原因
                pass

            if not ObjectTools.isFourPointsOnTheSamePlane([point1, point2, point3, point4]):
                # 警告用户数据错误及错误原因
                pass

            wire_bottom = Part.makePolygon([point1, point2, point3, point4, point1])
            wire_left = Part.makePolygon([point1, point2, point6, point5, point1])
            wire_right = Part.makePolygon([point4, point3, point6, point5, point4])
            wire_front = Part.makePolygon([point2, point3, point6, point2])
            wire_back = Part.makePolygon([point1, point4, point5, point1])
            bottom_face = Part.makeFace(wire_bottom, "Part::FaceMakerExtrusion")
            left_face = Part.makeFace(wire_left, "Part::FaceMakerExtrusion")
            right_face = Part.makeFace(wire_right, "Part::FaceMakerExtrusion")
            front_face = Part.makeFace(wire_front, "Part::FaceMakerExtrusion")
            back_face = Part.makeFace(wire_back, "Part::FaceMakerExtrusion")
            Shape1 = Part.makeShell([bottom_face, left_face, right_face, front_face, back_face])
            fp.Shape = Part.makeSolid(Shape1)
        except:
            Tools3D.sayz("Redraw Wedge Failed!")

            # 56可以与12平行，也可以与14平行，前提是5这个点必须在1点所对应的位置 @ lzg
            # if not ObjectsTools.isFourPointsOnTheSamePlane([point1,point2,point5,point6]):
            #     DocumentTools.errorMessage(QtGui.QApplication.translate(
            #                             "ObjectsTools",
            #                             "Point_1,Point_2,Point_5,Point_6   cnn't on the same plane.",
            #                             None))
            # if not ObjectsTools.isFourPointsOnTheSamePlane([point5,point6,point3,point4]):
            #     DocumentTools.errorMessage(QtGui.QApplication.translate(
            #                             "ObjectsTools",
            #                             "Point_3,Point_4,Point_5,Point_6   cnn't on the same plane.",
            #                             None))

        #     if ObjectTools.isFourPointsOnTheSamePlane([point1, point2, point5, point6]):
        #         buttom_wire_left_bottom = Part.makePolygon([point1, point2, point4, point1])
        #         buttom_wire_right_top = Part.makePolygon([point2, point3, point4, point2])
        #         left_wire = Part.makePolygon([point1, point4, point5, point1])
        #         right_wire = Part.makePolygon([point2, point3, point6, point2])
        #         front_wire_left_bottom = Part.makePolygon([point1, point2, point5, point1])
        #         front_wire_right_top = Part.makePolygon([point2, point6, point5, point2])
        #         back_wire_left_bottom = Part.makePolygon([point3, point5, point4, point3])
        #         back_wire_right_top = Part.makePolygon([point3, point6, point5, point3])
        #     else:
        #         # 构造56和14在同一平面的Wedge
        #         buttom_wire_left_bottom = Part.makePolygon([point1, point2, point4, point1])
        #         buttom_wire_right_top = Part.makePolygon([point2, point3, point4, point2])
        #         left_wire = Part.makePolygon([point1, point2, point5, point1])
        #         right_wire = Part.makePolygon([point4, point3, point6, point4])
        #         front_wire_left_bottom = Part.makePolygon([point2, point5, point6, point2])
        #         front_wire_right_top = Part.makePolygon([point2, point6, point3, point2])
        #         back_wire_left_bottom = Part.makePolygon([point1, point5, point6, point1])
        #         back_wire_right_top = Part.makePolygon([point1, point4, point6, point1])
        #
        #     bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
        #     buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
        #     right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
        #     left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
        #     front_face_left_bottom = Part.makeFace(front_wire_left_bottom, "Part::FaceMakerExtrusion")
        #     front_face_right_top = Part.makeFace(front_wire_right_top, "Part::FaceMakerExtrusion")
        #     back_face_left_bottom = Part.makeFace(back_wire_left_bottom, "Part::FaceMakerExtrusion")
        #     back_face_right_top = Part.makeFace(back_wire_right_top, "Part::FaceMakerExtrusion")
        #     '''Every three points make up a face'''
        #     Shape1 = Part.makeShell([back_face_right_top,
        #                                 back_face_left_bottom,
        #                                 bottom_face_left_bottom,
        #                                 buttom_face_right_top,
        #                                 right_face,
        #                                 left_face,
        #                                 front_face_left_bottom,
        #                                 front_face_right_top])
        #     fp.Shape = Part.makeSolid(Shape1)
        # except:
        #     Tools3D.sayz("Redraw Wedge Failed!")


class Wedge:
    """
    工厂类
    """
    def __init__(self):
        FreeCAD.ActiveDocument.openTransaction('Create_3D_Wedge')
        self.obj = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Vol_Wedge")
        self.__setProperty(self.obj)
        InitDoc3D.addObjectToGroup_helper(self.obj, "Wedge", "楔形体")
        FreeCAD.ActiveDocument.commitTransaction()
        # self.__setProperty(self.obj)

    def __setProperty(self, obj):
        obj.addProperty("App::PropertyString", "Type").Type = "Vol_Wedge"
        if FreeCAD.ActiveDocument.CoordinateSystem == "Rectangular":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0.05
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X", "Cone", " centre point3 X").Point3X = 0.05
            obj.addProperty("App::PropertyDistance", "Point3Y", "Cone", " centre point3 Y").Point3Y = 0.05
            obj.addProperty("App::PropertyDistance", "Point3Z", "Cone", " centre point3 Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X", "Cone", " centre point4 X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y", "Cone", " centre point4 Y").Point4Y = 0.05
            obj.addProperty("App::PropertyDistance", "Point4Z", "Cone", " centre point4 Z").Point4Z = 0
            obj.addProperty("App::PropertyDistance", "Point5X", "Cone", " centre point5 X").Point5X = 0
            obj.addProperty("App::PropertyDistance", "Point5Y", "Cone", " centre point5 Y").Point5Y = 0.05
            obj.addProperty("App::PropertyDistance", "Point5Z", "Cone", " centre point5 Z").Point5Z = 0.05
            obj.addProperty("App::PropertyDistance", "Point6X", "Cone", " centre point6 X").Point6X = 0.05
            obj.addProperty("App::PropertyDistance", "Point6Y", "Cone", " centre point6 Y").Point6Y = 0.05
            obj.addProperty("App::PropertyDistance", "Point6Z", "Cone", " centre point6 Z").Point6Z = 0.05
        elif FreeCAD.ActiveDocument.CoordinateSystem == "Polar":
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyAngle", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyDistance", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyAngle", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyDistance", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X", "Cone", " centre point3 X").Point3X = 0
            obj.addProperty("App::PropertyAngle", "Point3Y", "Cone", " centre point3 Y").Point3Y = 0
            obj.addProperty("App::PropertyDistance", "Point3Z", "Cone", " centre point3 Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X", "Cone", " centre point4 X").Point4X = 0
            obj.addProperty("App::PropertyAngle", "Point4Y", "Cone", " centre point4 Y").Point4Y = 0
            obj.addProperty("App::PropertyDistance", "Point4Z", "Cone", " centre point4 Z").Point4Z = 0
            obj.addProperty("App::PropertyDistance", "Point5X", "Cone", " centre point5 X").Point5X = 0
            obj.addProperty("App::PropertyAngle", "Point5Y", "Cone", " centre point5 Y").Point5Y = 0
            obj.addProperty("App::PropertyDistance", "Point5Z", "Cone", " centre point5 Z").Point5Z = 0
            obj.addProperty("App::PropertyDistance", "Point6X", "Cone", " centre point6 X").Point6X = 0
            obj.addProperty("App::PropertyAngle", "Point6Y", "Cone", " centre point6 Y").Point6Y = 0
            obj.addProperty("App::PropertyDistance", "Point6Z", "Cone", " centre point6 Z").Point6Z = 0
        else:
            obj.addProperty("App::PropertyDistance", "Point1X", "Cone", " centre point1 X").Point1X = 0
            obj.addProperty("App::PropertyDistance", "Point1Y", "Cone", " centre point1 Y").Point1Y = 0
            obj.addProperty("App::PropertyAngle", "Point1Z", "Cone", " centre point1 Z").Point1Z = 0
            obj.addProperty("App::PropertyDistance", "Point2X", "Cone", " centre point2 X").Point2X = 0
            obj.addProperty("App::PropertyDistance", "Point2Y", "Cone", " centre point2 Y").Point2Y = 0
            obj.addProperty("App::PropertyAngle", "Point2Z", "Cone", " centre point2 Z").Point2Z = 0
            obj.addProperty("App::PropertyDistance", "Point3X", "Cone", " centre point3 X").Point3X = 0
            obj.addProperty("App::PropertyDistance", "Point3Y", "Cone", " centre point3 Y").Point3Y = 0
            obj.addProperty("App::PropertyAngle", "Point3Z", "Cone", " centre point3 Z").Point3Z = 0
            obj.addProperty("App::PropertyDistance", "Point4X", "Cone", " centre point4 X").Point4X = 0
            obj.addProperty("App::PropertyDistance", "Point4Y", "Cone", " centre point4 Y").Point4Y = 0
            obj.addProperty("App::PropertyAngle", "Point4Z", "Cone", " centre point4 Z").Point4Z = 0
            obj.addProperty("App::PropertyDistance", "Point5X", "Cone", " centre point5 X").Point5X = 0
            obj.addProperty("App::PropertyDistance", "Point5Y", "Cone", " centre point5 Y").Point5Y = 0
            obj.addProperty("App::PropertyAngle", "Point5Z", "Cone", " centre point5 Z").Point5Z = 0
            obj.addProperty("App::PropertyDistance", "Point6X", "Cone", " centre point6 X").Point6X = 0
            obj.addProperty("App::PropertyDistance", "Point6Y", "Cone", " centre point6 Y").Point6Y = 0
            obj.addProperty("App::PropertyAngle", "Point6Z", "Cone", " centre point6 Z").Point6Z = 0
        Tools3D.addCommonPropertyToObject(obj)
        Tools3D.addAttributeToObject(obj)
        Tools3D.addHelperProperty(obj, 6)
        Tools3D.getHelperValue(obj)


def getObject():
    wedge = Wedge()
    CreateWedge(wedge.obj)
    Tools3D.ViewProvider(wedge.obj.ViewObject)
    return wedge.obj
