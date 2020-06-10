#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

class HollowedCylinder:
    def __init__(self, obj):
        ''' Add some custom properties to our box feature '''
        obj.addProperty("App::PropertyVector","Point_1","TorusFace","Length of the box").Point_1=FreeCAD.Vector(0,0,0)
        obj.addProperty("App::PropertyVector","Point_2","TorusFace","Length of the box").Point_2=FreeCAD.Vector(1,1,1)
        obj.addProperty("App::PropertyLength","RadiusInside","TorusFace","Width of the box").RadiusInside=1.0
        obj.addProperty("App::PropertyLength","RadiusOutside","TorusFace", "Height of the box").RadiusOutside=10.0
        obj.Proxy = self

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop=="Point_1" or prop=="Point_2" or prop == "RadiusInside" or prop == "RadiusOutside":
            line=Part.makeLine(fp.Point_1,fp.Point_2)
            path=Part.Wire(line)
            dir=fp.Point_2-fp.Point_1
            e1=Part.makeCircle(fp.RadiusInside,fp.Point_1,dir)
            e2=Part.makeCircle(fp.RadiusOutside,fp.Point_1,dir)
            shapeCircle=Part.makeFace([Part.Wire([e1]),Part.Wire([e2])],"Part::FaceMakerBullseye")
            obj=path.makePipe(shapeCircle)
            fp.Shape=obj

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        '''两个半径的圆形成一个带孔的环面，环面沿两个点形成的线段横扫，形成带孔的圆柱体'''
        FreeCAD.Console.PrintMessage("Recompute Python HollowedCylinder feature\n")
        line=Part.makeLine(fp.Point_1,fp.Point_2)
        path=Part.Wire(line)
        dir=fp.Point_2-fp.Point_1
        e1=Part.makeCircle(fp.RadiusInside,fp.Point_1,dir)
        e2=Part.makeCircle(fp.RadiusOutside,fp.Point_1,dir)
        shapeCircle=Part.makeFace([Part.Wire([e1]),Part.Wire([e2])],"Part::FaceMakerBullseye")
        fp.Shape=path.makePipe(shapeCircle)

class ViewProviderHollowedCylinder:
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
            static const char * ViewProviderBox_xpm[] = {
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
