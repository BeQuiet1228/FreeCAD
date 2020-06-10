#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self
'''一条边绕沿着另一条边扫过，形成一个面，
   面再沿着另一条线扫过，形成一个平行四面体'''
class Parallelogram(PartFeature):
    def __init__(self, obj):
        ''' Add some custom properties to our box feature '''
        obj.addProperty("App::PropertyVector","Point_0","Parallelogram","Point 0").Point_0=FreeCAD.Vector(2,1,0)
        obj.addProperty("App::PropertyVector","Point_1","Parallelogram","Point 1").Point_1=FreeCAD.Vector(2,3,0)
        obj.addProperty("App::PropertyVector","Point_2","Parallelogram","Point 2").Point_2=FreeCAD.Vector(2,0,2)
        obj.addProperty("App::PropertyVector", "Point_3", "Parallelogram", "Point 3").Point_3 = FreeCAD.Vector(1,1,0)
        PartFeature.__init__(self, obj)
        obj.setEditorMode('Placement',2)

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop == "Point_0"or prop == "Point_1" or prop == "Point_2" or prop == "Point_3":
            line1=Part.makeLine(fp.Point_0,fp.Point_3)
            line2=Part.makeLine(fp.Point_0,fp.Point_2)
            path1=Part.Wire(line1)
            face=path1.makePipe(line2)
            line2=Part.makeLine(fp.Point_0,fp.Point_1)
            path2=Part.Wire(line2)
            obj=path2.makePipe(face)
            fp.Shape=obj
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        line1 = Part.makeLine(fp.Point_0, fp.Point_3)
        line2 = Part.makeLine(fp.Point_0, fp.Point_2)
        path1 = Part.Wire(line1)
        face = path1.makePipe(line2)
        line2=Part.makeLine(fp.Point_0,fp.Point_1)
        path2=Part.Wire(line2)
        obj=path2.makePipe(face)
        fp.Shape=obj


class ViewProviderParallelogram:
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
