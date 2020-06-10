#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

class Pyramid:
    def __init__(self, obj):
        ''' Add some custom properties to our Pyramid feature '''
        obj.addProperty("App::PropertyVector","Point_1","Pyramid","Corner Point_1 of the Pyramid").Point_1=FreeCAD.Vector(0,0,0)
        obj.addProperty("App::PropertyVector","Point_2","Pyramid","Corner Point_2 of the Pyramid").Point_2=FreeCAD.Vector(5,0,0)
        obj.addProperty("App::PropertyVector","Point_3","Pyramid","Corner Point_3 of the Pyramid").Point_3=FreeCAD.Vector(5,5,0)
        obj.addProperty("App::PropertyVector","Point_4","Pyramid","Corner Point_4 of the Pyramid").Point_4=FreeCAD.Vector(0,5,0)
        obj.addProperty("App::PropertyVector","Point_5","Pyramid","peak of the Pyramid").Point_5=FreeCAD.Vector(0,0,5)
        obj.Proxy = self
        obj.setEditorMode('Placement', 2)

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop=="Point_1" or prop=="Point_2"  or prop=="Point_3"  or prop=="Point_4"  or prop=="Point_5"   :
            buttom_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_4,fp.Point_1])
            buttom_wire_right_top = Part.makePolygon([ fp.Point_2, fp.Point_3, fp.Point_4,fp.Point_2])
            front_wire=Part.makePolygon([fp.Point_1,fp.Point_2,fp.Point_5,fp.Point_1])
            back_wire=Part.makePolygon([fp.Point_3,fp.Point_5,fp.Point_4,fp.Point_3])
            left_wire=Part.makePolygon([fp.Point_1,fp.Point_5,fp.Point_4,fp.Point_1])
            right_wire=Part.makePolygon([fp.Point_2,fp.Point_5,fp.Point_3,fp.Point_2])
            bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
            buttom_face_right_top= Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
            front_face=Part.makeFace(front_wire,"Part::FaceMakerExtrusion")
            back_face=Part.makeFace(back_wire,"Part::FaceMakerExtrusion")
            right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
            left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
            #每个面都划分为三角形
            obj = Part.makeShell([front_face,
                                  bottom_face_left_bottom,
                                  buttom_face_right_top ,
                                  right_face,
                                  left_face,
                                  back_face])
            fp.Shape = obj

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        '''API中自带有建立楔形体，后面可参看'''
        buttom_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_4, fp.Point_1])
        buttom_wire_right_top = Part.makePolygon([fp.Point_2, fp.Point_3, fp.Point_4, fp.Point_2])
        front_wire = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_5, fp.Point_1])
        back_wire = Part.makePolygon([fp.Point_3, fp.Point_5, fp.Point_4, fp.Point_3])
        left_wire = Part.makePolygon([fp.Point_1, fp.Point_5, fp.Point_4, fp.Point_1])
        right_wire = Part.makePolygon([fp.Point_2, fp.Point_5, fp.Point_3, fp.Point_2])
        bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
        buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
        front_face = Part.makeFace(front_wire, "Part::FaceMakerExtrusion")
        back_face = Part.makeFace(back_wire, "Part::FaceMakerExtrusion")
        right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
        left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
        # 每个面都划分为三角形
        obj = Part.makeShell([front_face,
                              bottom_face_left_bottom,
                              buttom_face_right_top,
                              right_face,
                              left_face,
                              back_face])



class ViewProviderPyramid:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self

    def attach(self, obj):
        ''' Setup the scene sub-graph of the view provider, this method is mandatory '''
        return

    def updateData(self, fp, prop):
        ''' If a property of the handled feature has changed we have the chance to handle this here '''
        return
    def getDisplayModes(self,obj):
        ''' Return a list of display modes. '''
        modes=[]
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Shaded"
    def setDisplayMode(self,mode):
        ''' Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done. This method is optinal.
        '''
        return mode
    def onChanged(self, vp, prop):
        ''' Print the name of the property that has changed '''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def getIcon(self):
        ''' Return the icon in XMP format which will appear in the tree view. This method is optional
        and if not defined a default icon is shown.
        '''
        return """
            /* XPM */
            static const char * ViewProviderPyramid_xpm[] = {
            "16 16 6 1",
            " 	c None",
            ".	c #141010",
            "+	c #615BD2",
            "@	c #C39D55",
            "#	c #000000",
            "$	c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def __getstate__(self):
        ''' When saving the document this object gets stored using Python's cPickle module.
        Since we have some un-pickable here -- the Coin stuff -- we must define this method
        to return a tuple of all pickable objects or None.
        '''
        return None

    def __setstate__(self,state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return None


    def __setstate__(self,state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return None