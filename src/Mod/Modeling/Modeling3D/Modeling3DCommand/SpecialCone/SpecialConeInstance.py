import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin

class SpecialCone:
    def __init__(self, obj):
        ''' Add some custom properties to our SpecialCone feature '''
        obj.addProperty("App::PropertyVector","StartPoint","SpecialCone","StartPoint of the SpecialCone").StartPoint=FreeCAD.Vector(0,0,0)
        obj.addProperty("App::PropertyVector","EndPoint","SpecialCone","LeEndPointngth of the SpecialCone").EndPoint=FreeCAD.Vector(5,5,5)
        obj.addProperty("App::PropertyLength","TopRadius","SpecialCone","TopRadius of the SpecialCone").TopRadius=1.0
        obj.addProperty("App::PropertyLength","BottomRadius","SpecialCone", "BottomRadius of the SpecialCone").BottomRadius=10.0
        obj.Proxy = self
        obj.setEditorMode('Placement',2)

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop=="StartPoint" or prop=="EndPoint" or prop == "BottomRadius" or prop=="TopRadius":
            height = fp.StartPoint.distanceToPoint(fp.EndPoint)
            dir = fp.EndPoint - fp.StartPoint
            obj = Part.makeCone(fp.BottomRadius,fp.TopRadius , height, fp.EndPoint, -dir)
            fp.Shape = obj
            '''fp.Shape = Part.makeFace([Part.Wire([e1]),Part.Wire([e2])],"Part::FaceMakerBullseye")'''

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        height = fp.StartPoint.distanceToPoint(fp.EndPoint)
        dir = fp.EndPoint - fp.StartPoint
        obj = Part.makeCone(fp.BottomRadius, fp.TopRadius, height, fp.EndPoint, -dir)
        fp.Shape = obj
        '''fp.Shape = Part.makeFace([Part.Wire([e1]),Part.Wire([e2])],"Part::FaceMakerBullseye")'''

class ViewProviderSpecialCone:
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
            static const char * ViewProviderSpecialCone_xpm[] = {
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

