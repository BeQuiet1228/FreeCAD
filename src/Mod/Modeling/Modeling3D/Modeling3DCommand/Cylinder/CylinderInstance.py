import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self

class Cylinder(PartFeature):
    def __init__(self, obj):
        ''' Add some custom properties to our box feature '''
        obj.addProperty("App::PropertyVector","StartPoint","Cylinder","StartPoint of the Cylinder").StartPoint=FreeCAD.Vector(0,0,0)
        obj.addProperty("App::PropertyVector","EndPoint","Cylinder","EndPoint of the Cylinder").EndPoint=FreeCAD.Vector(1,1,1)
        obj.addProperty("App::PropertyLength","Radius","Cylinder","Radius of the Cylinder").Radius=1.0
        PartFeature.__init__(self, obj)

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop=="StartPoint" or prop=="EndPoint" or prop == "Radius":
            line=Part.makeLine(fp.StartPoint,fp.EndPoint)
            path=Part.Wire(line)
            dir=fp.EndPoint-fp.StartPoint
            e1=Part.makeCircle(fp.Radius,fp.StartPoint,dir)
            shapeCircle=Part.makeFace([Part.Wire([e1])],"Part::FaceMakerBullseye")
            obj=path.makePipe(shapeCircle)
            fp.Shape=obj

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        FreeCAD.Console.PrintMessage("Recompute Python Cylinder feature\n")
        line=Part.makeLine(fp.StartPoint,fp.EndPoint)
        path=Part.Wire(line)
        dir=fp.EndPoint-fp.StartPoint
        e1=Part.makeCircle(fp.Radius,fp.StartPoint,dir)
        shapeCircle=Part.makeFace([Part.Wire([e1])],"Part::FaceMakerBullseye")
        fp.Shape=path.makePipe(shapeCircle)


class ViewProviderCylinder:
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