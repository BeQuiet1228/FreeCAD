#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
class PartFeature:
    def __init__(self, obj):
        obj.Proxy = self

class OrthographicBody(PartFeature):
    def __init__(self, obj):
        ''' Add some custom properties to our OrthographicBody feature '''
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        obj.addProperty("App::PropertyVector","Point_1","OrthographicBodyFace","Point_1 of the OrthographicBody").Point_1=FreeCAD.Vector(0,0,0)
        obj.addProperty("App::PropertyVector","Point_2","OrthographicBodyFace","Point_2 of the OrthographicBody").Point_2=FreeCAD.Vector(0.001,0.001,0.001)
        PartFeature.__init__(self, obj)
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('flagRedraw',2)
#通过两个点算出长宽高，由此定义投影体（直角坐标系中投影体就是正方形）
    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        if prop == "Point_1" or prop == "Point_2":
            length=abs(fp.Point_1.x-fp.Point_2.x)
            width=abs(fp.Point_1.y-fp.Point_2.y)
            height=abs(fp.Point_1.z-fp.Point_2.z)
            dir=FreeCAD.Vector(0,0,1)
            obj=Part.makeBox(length,width,height,fp.Point_1,dir)
            fp.Shape=obj
    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        length = abs(fp.Point_1.x - fp.Point_2.x)
        width = abs(fp.Point_1.y - fp.Point_2.y)
        height = abs(fp.Point_1.z - fp.Point_2.z)
        dir=FreeCAD.Vector(0,0,1)
        obj = Part.makeBox(length, width, height, fp.Point_1, dir)
        fp.Shape = obj

class ViewProviderOrthographicBody:
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
        return "Wireframe"
    def setDisplayMode(self,mode):
        ''' Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done. This method is optinal.
        '''
        return mode
    def onChanged(self, vp, prop):
        ''' Print the name of the property that has changed '''
        pass

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