#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

class Wedge:
    def __init__(self, obj):
        ''' Add some custom properties to our Wedge feature '''
        obj.addProperty("App::PropertyVector","Point_1","Wedge","Corner Point_1 of the Wedge").Point_1=FreeCAD.Vector(0,0,0)
        obj.addProperty("App::PropertyVector","Point_2","Wedge","Corner Point_2 of the Wedge").Point_2=FreeCAD.Vector(5,0,0)
        obj.addProperty("App::PropertyVector","Point_3","Wedge","Corner Point_3 of the Wedge").Point_3=FreeCAD.Vector(5,5,0)
        obj.addProperty("App::PropertyVector","Point_4","Wedge","Corner Point_4 of the Wedge").Point_4=FreeCAD.Vector(0,5,0)
        obj.addProperty("App::PropertyVector","Point_5","Wedge","Vertex Point_5 of the Wedge").Point_5=FreeCAD.Vector(0,5,5)
        obj.addProperty("App::PropertyVector","Point_6","Wedge","Vertex Point_6 of the Wedge").Point_6=FreeCAD.Vector(5,5,5)
        obj.Proxy = self
        obj.setEditorMode('Placement', 2)

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop=="Point_1" or prop=="Point_2"  or prop=="Point_3"  or prop=="Point_4"  or prop=="Point_5"  or prop=="Point_6" :
            buttom_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_4,fp.Point_1])
            buttom_wire_right_top = Part.makePolygon([ fp.Point_2, fp.Point_3, fp.Point_4,fp.Point_2])
            left_wire = Part.makePolygon([fp.Point_1, fp.Point_4, fp.Point_5,fp.Point_1])
            right_wire = Part.makePolygon([fp.Point_2, fp.Point_3, fp.Point_6,fp.Point_2])
            front_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_5,fp.Point_1])
            front_wire_right_top = Part.makePolygon([ fp.Point_2, fp.Point_6,fp.Point_5, fp.Point_2])
            back_wire_left_bottom = Part.makePolygon([fp.Point_3,  fp.Point_5, fp.Point_4,fp.Point_3])
            back_wire_right_top = Part.makePolygon([fp.Point_3, fp.Point_6, fp.Point_5, fp.Point_3])
            bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
            buttom_face_right_top= Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
            right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
            left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
            front_face_left_bottom = Part.makeFace(front_wire_left_bottom, "Part::FaceMakerExtrusion")
            front_face_right_top = Part.makeFace(front_wire_right_top, "Part::FaceMakerExtrusion")
            back_face_left_bottom = Part.makeFace(back_wire_left_bottom, "Part::FaceMakerExtrusion")
            back_face_right_top = Part.makeFace(back_wire_right_top, "Part::FaceMakerExtrusion")
            '''Every three points make up a face'''
            obj = Part.makeShell([back_face_right_top,
                                  back_face_left_bottom,
                                  bottom_face_left_bottom,
                                  buttom_face_right_top ,
                                  right_face,
                                  left_face,
                                  front_face_left_bottom,
                                  front_face_right_top])
            fp.Shape = obj

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        '''Part.makeWedge()'''
        buttom_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_4, fp.Point_1])
        buttom_wire_right_top = Part.makePolygon([fp.Point_2, fp.Point_3, fp.Point_4, fp.Point_2])
        left_wire = Part.makePolygon([fp.Point_1, fp.Point_4, fp.Point_5, fp.Point_1])
        right_wire = Part.makePolygon([fp.Point_2, fp.Point_3, fp.Point_6, fp.Point_2])
        front_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_5, fp.Point_1])
        front_wire_right_top = Part.makePolygon([fp.Point_2, fp.Point_6, fp.Point_5, fp.Point_2])
        back_wire_left_bottom = Part.makePolygon([fp.Point_3, fp.Point_5, fp.Point_4, fp.Point_3])
        back_wire_right_top = Part.makePolygon([fp.Point_3, fp.Point_6, fp.Point_5, fp.Point_3])
        bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
        buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
        right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
        left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
        front_face_left_bottom = Part.makeFace(front_wire_left_bottom, "Part::FaceMakerExtrusion")
        front_face_right_top = Part.makeFace(front_wire_right_top, "Part::FaceMakerExtrusion")
        back_face_left_bottom = Part.makeFace(back_wire_left_bottom, "Part::FaceMakerExtrusion")
        back_face_right_top = Part.makeFace(back_wire_right_top, "Part::FaceMakerExtrusion")
        '''Every three points make up a face'''
        obj = Part.makeShell([back_face_right_top,
                              back_face_left_bottom,
                              bottom_face_left_bottom,
                              buttom_face_right_top,
                              right_face,
                              left_face,
                              front_face_left_bottom,
                              front_face_right_top])
        fp.Shape = obj



class ViewProviderWedge:
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
            static const char * ViewProviderWedge_xpm[] = {
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
