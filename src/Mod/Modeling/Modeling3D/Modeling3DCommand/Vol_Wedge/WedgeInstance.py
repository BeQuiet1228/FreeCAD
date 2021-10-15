#-*- coding: utf-8 -*-
import FreeCAD, Part, math
from FreeCAD import Base
from pivy import coin
from PySide import QtCore, QtGui

from Common.Tools import CoordinateSystemTools,DocumentTools,ObjectsTools,PlacementTools
class Wedge:
    def __init__(self, obj):
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        ''' Add some custom properties to our Wedge feature '''
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance","Point_1","Object of a Wedge","Corner Point_1 of the Wedge").Point_1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point_2","Object of a Wedge","Corner Point_2 of the Wedge").Point_2=FreeCAD.Vector(0.005,0,0)
            obj.addProperty("App::PropertyVectorDistance","Point_3","Object of a Wedge","Corner Point_3 of the Wedge").Point_3=FreeCAD.Vector(0.005,0.005,0)
            obj.addProperty("App::PropertyVectorDistance","Point_4","Object of a Wedge","Corner Point_4 of the Wedge").Point_4=FreeCAD.Vector(0,0.005,0)
            obj.addProperty("App::PropertyVectorDistance","Point_5","Object of a Wedge","Vertex Point_5 of the Wedge").Point_5=FreeCAD.Vector(0,0.005,0.005)
            obj.addProperty("App::PropertyVectorDistance","Point_6","Object of a Wedge","Vertex Point_6 of the Wedge").Point_6=FreeCAD.Vector(0.005,0.005,0.005)
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.addProperty("App::PropertyPolVecDistance","Point_1","Object of a Wedge","Corner Point_1 of the Wedge").Point_1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance","Point_2","Object of a Wedge","Corner Point_2 of the Wedge").Point_2=FreeCAD.Vector(0.002,20,0)
            obj.addProperty("App::PropertyPolVecDistance","Point_3","Object of a Wedge","Corner Point_3 of the Wedge").Point_3=FreeCAD.Vector(0.004,45,0)
            obj.addProperty("App::PropertyPolVecDistance","Point_4","Object of a Wedge","Corner Point_4 of the Wedge").Point_4=FreeCAD.Vector(0.002,60,0)
            obj.addProperty("App::PropertyPolVecDistance","Point_5","Object of a Wedge","Vertex Point_5 of the Wedge").Point_5=FreeCAD.Vector(0.001,30,0.005)
            obj.addProperty("App::PropertyPolVecDistance","Point_6","Object of a Wedge","Vertex Point_6 of the Wedge").Point_6=FreeCAD.Vector(0.003,25,0.005)
        else:
            obj.addProperty("App::PropertyCylinderVecDistance","Point_1","Object of a Wedge","Corner Point_1 of the Wedge").Point_1=FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_2","Object of a Wedge","Corner Point_2 of the Wedge").Point_2=FreeCAD.Vector(0.002,20,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_3","Object of a Wedge","Corner Point_3 of the Wedge").Point_3=FreeCAD.Vector(0.004,45,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_4","Object of a Wedge","Corner Point_4 of the Wedge").Point_4=FreeCAD.Vector(0.002,60,0)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_5","Object of a Wedge","Vertex Point_5 of the Wedge").Point_5=FreeCAD.Vector(0.001,30,0.005)
            obj.addProperty("App::PropertyCylinderVecDistance","Point_6","Object of a Wedge","Vertex Point_6 of the Wedge").Point_6=FreeCAD.Vector(0.003,25,0.005)
        self.vectorList=[obj.Point_1,obj.Point_2,obj.Point_3,obj.Point_4,obj.Point_5,obj.Point_6]
        obj.addProperty("App::PropertyInteger","Order","","Order of the Conformal").Order=100

        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Wedge,self.curCoordinateSystem)

        obj.Proxy = self
        self.placementBefore = obj.Placement
        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label

        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('flagRedraw',2)

        self.initObject(obj)
        self.redraw(obj)

    def initObject(self,obj):
        ObjectsTools.setInitOrderForObject(obj)
        # obj.Label="["+str(obj.Order)+"]"+"_"+obj.Label
        pass

    def onBeforeChange(self, obj, prop):
        if hasattr(obj,"Placement"):
            obj.setEditorMode('Placement',2)
        if hasattr(obj,"Type"):
            obj.setEditorMode("Type",2)
        if hasattr(obj,"flagRedraw"):
            obj.setEditorMode("flagRedraw",2)
        if prop == "Placement":
            self.placementBefore = FreeCAD.Placement(obj.Placement)
        if prop=="Order":
            self.orderBefore=obj.Order
        if prop=="Label":
            self.labelBofroe=obj.Label

    def onChanged(self, fp, prop):
        ''' Print the name of the property that has changed '''
        if prop=="flagRedraw":
            self.flagExcute=True
        #物体对象的Order发生改变时
        if prop=="Order":
            ObjectsTools.updateWhenOrderChanged(fp,self.orderBefore,fp.Order)
            pass
        if prop=="Label":
            if not hasattr(self,"flagLabel"):
                self.flagLabel=True
            # 此处flagLabel的作用是updateWhenLabelChanged函数中会改变Label的值\
            # 为了不让onChanged函数循环执行导致程序崩溃
            if self.flagLabel:
                self.flagLabel=False
                # fp.Label="Test"
                #这里加个判断是为了解决b=FreeCAD.ActiveDocument.copyObject(o)，copy时不能读到labelBofore
                if not ObjectsTools.hasThePropertyByObj(fp,"labelBofroe"):
                    ObjectsTools.updateWhenLableChanged(fp,fp.Label,fp.Label)
                else:
                    ObjectsTools.updateWhenLableChanged(fp,self.labelBofroe,fp.Label)
                pass
                self.flagLabel=True
        # FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop=="Point_1" or prop=="Point_2"  or prop=="Point_3"  or prop=="Point_4"  or prop=="Point_5"  or prop=="Point_6" :
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False

                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.Point_1,fp.Point_2,fp.Point_3,fp.Point_4,fp.Point_5,fp.Point_6]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop == "Placement" :
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False

                fp.setEditorMode("Point_1",1)
                fp.setEditorMode("Point_2",1)
                fp.setEditorMode("Point_3",1)
                fp.setEditorMode("Point_4",1)
                fp.setEditorMode("Point_5",1)
                fp.setEditorMode("Point_6",1)

                vectorList=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)

                pos = fp.Placement.Base.sub(self.placementBefore.Base)
                resultVectors=[]

                if pos!=FreeCAD.Vector(0.0,0.0,0.0):
                    resultVectors=PlacementTools.moveAdd(pos,vectorList)

                else:
                    resultVectors=PlacementTools.rotate(self.placementBefore,fp.Placement,vectorList)
                resultVectors=CoordinateSystemTools.recToOther(self.curCoordinateSystem,resultVectors)

                fp.Point_1=resultVectors[0]
                fp.Point_2=resultVectors[1]
                fp.Point_3=resultVectors[2]
                fp.Point_4=resultVectors[3]
                fp.Point_5=resultVectors[4]
                fp.Point_6=resultVectors[5]
                self.vectorList=[fp.Point_1,fp.Point_2,fp.Point_3,fp.Point_4,fp.Point_5,fp.Point_6]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False

                pass
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        ObjectsTools.fucAttributeChange(fp,prop)

    def redraw(self,obj):
        try:
            tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            tempPoint_1=tempPoints[0]
            tempPoint_2=tempPoints[1]
            tempPoint_3=tempPoints[2]
            tempPoint_4=tempPoints[3]
            tempPoint_5=tempPoints[4]
            tempPoint_6=tempPoints[5]
            
            if tempPoint_1==tempPoint_2 and tempPoint_1==tempPoint_4:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_1 , tempPoint_2 ,tempPoint_4 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_2==tempPoint_4 and tempPoint_2==tempPoint_3:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_2 , tempPoint_3 ,tempPoint_4 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_2==tempPoint_1 and tempPoint_2==tempPoint_5:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_1 , tempPoint_2 ,tempPoint_5 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_3==tempPoint_5 and tempPoint_3==tempPoint_4:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_3 , tempPoint_4 ,tempPoint_5 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_1==tempPoint_5 and tempPoint_1==tempPoint_4:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_1 , tempPoint_4 ,tempPoint_5 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_2==tempPoint_5 and tempPoint_3==tempPoint_2:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_2 , tempPoint_3 ,tempPoint_5 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_2==tempPoint_3 and tempPoint_3==tempPoint_6:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_2 , tempPoint_3 ,tempPoint_6 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_2==tempPoint_5 and tempPoint_6==tempPoint_2:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_2 , tempPoint_5 ,tempPoint_6 cann't be same.",
                                            None))
                return
                pass
            if tempPoint_6==tempPoint_5 and tempPoint_3==tempPoint_6:
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                            "PyramidInstance",
                                            "tempPoint_3 , tempPoint_5 ,tempPoint_6 cann't be same.",
                                            None))
                return
                pass

            if not ObjectsTools.isFourPointsOnTheSamePlane([tempPoint_1,tempPoint_2,tempPoint_3,tempPoint_4]):
                DocumentTools.errorMessage(QtGui.QApplication.translate(
                                        "ObjectsTools",
                                        "Point_1,Point_2,Point_3,Point_4   cnn't on the same plane.",
                                        None))
            # 56可以与12平行，也可以与14平行，前提是5这个点必须在1点所对应的位置 @ lzg
            # if not ObjectsTools.isFourPointsOnTheSamePlane([tempPoint_1,tempPoint_2,tempPoint_5,tempPoint_6]):
            #     DocumentTools.errorMessage(QtGui.QApplication.translate(
            #                             "ObjectsTools",
            #                             "Point_1,Point_2,Point_5,Point_6   cnn't on the same plane.",
            #                             None))
            # if not ObjectsTools.isFourPointsOnTheSamePlane([tempPoint_5,tempPoint_6,tempPoint_3,tempPoint_4]):
            #     DocumentTools.errorMessage(QtGui.QApplication.translate(
            #                             "ObjectsTools",
            #                             "Point_3,Point_4,Point_5,Point_6   cnn't on the same plane.",
            #                             None))
            if  ObjectsTools.isFourPointsOnTheSamePlane([tempPoint_1,tempPoint_2,tempPoint_5,tempPoint_6]):
                buttom_wire_left_bottom = Part.makePolygon([tempPoint_1, tempPoint_2, tempPoint_4, tempPoint_1])
                buttom_wire_right_top = Part.makePolygon([tempPoint_2, tempPoint_3, tempPoint_4, tempPoint_2])
                left_wire = Part.makePolygon([tempPoint_1, tempPoint_4, tempPoint_5, tempPoint_1])
                right_wire = Part.makePolygon([tempPoint_2, tempPoint_3, tempPoint_6, tempPoint_2])
                front_wire_left_bottom = Part.makePolygon([tempPoint_1, tempPoint_2, tempPoint_5, tempPoint_1])
                front_wire_right_top = Part.makePolygon([tempPoint_2, tempPoint_6, tempPoint_5, tempPoint_2])
                back_wire_left_bottom = Part.makePolygon([tempPoint_3, tempPoint_5, tempPoint_4, tempPoint_3])
                back_wire_right_top = Part.makePolygon([tempPoint_3, tempPoint_6, tempPoint_5, tempPoint_3])
            else:
                # 构造56和14在同一平面的Wedge@lzg
                buttom_wire_left_bottom = Part.makePolygon([tempPoint_1, tempPoint_2, tempPoint_4, tempPoint_1])
                buttom_wire_right_top = Part.makePolygon([tempPoint_2, tempPoint_3, tempPoint_4, tempPoint_2])
                left_wire = Part.makePolygon([tempPoint_1, tempPoint_2, tempPoint_5, tempPoint_1])
                right_wire = Part.makePolygon([tempPoint_4, tempPoint_3, tempPoint_6, tempPoint_4])
                front_wire_left_bottom = Part.makePolygon([tempPoint_2, tempPoint_5, tempPoint_6, tempPoint_2])
                front_wire_right_top = Part.makePolygon([tempPoint_2, tempPoint_6, tempPoint_3, tempPoint_2])
                back_wire_left_bottom = Part.makePolygon([tempPoint_1, tempPoint_5, tempPoint_6, tempPoint_1])
                back_wire_right_top = Part.makePolygon([tempPoint_1, tempPoint_4, tempPoint_6, tempPoint_1])


            bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
            buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
            right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
            left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
            front_face_left_bottom = Part.makeFace(front_wire_left_bottom, "Part::FaceMakerExtrusion")
            front_face_right_top = Part.makeFace(front_wire_right_top, "Part::FaceMakerExtrusion")
            back_face_left_bottom = Part.makeFace(back_wire_left_bottom, "Part::FaceMakerExtrusion")
            back_face_right_top = Part.makeFace(back_wire_right_top, "Part::FaceMakerExtrusion")
            '''Every three points make up a face'''
            obj.Shape = Part.makeShell([back_face_right_top,
                                back_face_left_bottom,
                                bottom_face_left_bottom,
                                buttom_face_right_top,
                                right_face,
                                left_face,
                                front_face_left_bottom,
                                front_face_right_top])
            obj.Shape= Part.makeSolid(obj.Shape)
        except:
            DocumentTools.printErrorMessage("Redraw Wedge Failed!")
        ObjectsTools.doSomethingAfterRecomputerVolShape(obj)

    def execute(self, fp):
        ''' Print a short message when doing a recomputation, this method is mandatory '''
        '''Part.makeWedge()'''
        fp.setEditorMode("Point_1",0)
        fp.setEditorMode("Point_2",0)
        fp.setEditorMode("Point_3",0)
        fp.setEditorMode("Point_4",0)
        fp.setEditorMode("Point_5",0)
        fp.setEditorMode("Point_6",0)
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False
        # buttom_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_4, fp.Point_1])
        # buttom_wire_right_top = Part.makePolygon([fp.Point_2, fp.Point_3, fp.Point_4, fp.Point_2])
        # left_wire = Part.makePolygon([fp.Point_1, fp.Point_4, fp.Point_5, fp.Point_1])
        # right_wire = Part.makePolygon([fp.Point_2, fp.Point_3, fp.Point_6, fp.Point_2])
        # front_wire_left_bottom = Part.makePolygon([fp.Point_1, fp.Point_2, fp.Point_5, fp.Point_1])
        # front_wire_right_top = Part.makePolygon([fp.Point_2, fp.Point_6, fp.Point_5, fp.Point_2])
        # back_wire_left_bottom = Part.makePolygon([fp.Point_3, fp.Point_5, fp.Point_4, fp.Point_3])
        # back_wire_right_top = Part.makePolygon([fp.Point_3, fp.Point_6, fp.Point_5, fp.Point_3])
        # bottom_face_left_bottom = Part.makeFace(buttom_wire_left_bottom, "Part::FaceMakerExtrusion")
        # buttom_face_right_top = Part.makeFace(buttom_wire_right_top, "Part::FaceMakerExtrusion")
        # right_face = Part.makeFace(right_wire, "Part::FaceMakerExtrusion")
        # left_face = Part.makeFace(left_wire, "Part::FaceMakerExtrusion")
        # front_face_left_bottom = Part.makeFace(front_wire_left_bottom, "Part::FaceMakerExtrusion")
        # front_face_right_top = Part.makeFace(front_wire_right_top, "Part::FaceMakerExtrusion")
        # back_face_left_bottom = Part.makeFace(back_wire_left_bottom, "Part::FaceMakerExtrusion")
        # back_face_right_top = Part.makeFace(back_wire_right_top, "Part::FaceMakerExtrusion")
        # '''Every three points make up a face'''
        # obj = Part.makeShell([back_face_right_top,
        #                       back_face_left_bottom,
        #                       bottom_face_left_bottom,
        #                       buttom_face_right_top,
        #                       right_face,
        #                       left_face,
        #                       front_face_left_bottom,
        #                       front_face_right_top])
        # fp.Shape = obj
    def __getstate__(self):
        state={}
        state["curCoordinateSystem"]=self.curCoordinateSystem
        state["flagShape"]=self.flagShape
        state["flagPlacement"]=self.flagPlacement
        state["flagExcute"]=self.flagExcute
        state["vectorList"]=[]
        for i in range(len(self.vectorList)):
            v=[self.vectorList[i].x,self.vectorList[i].y,self.vectorList[i].z]
            state["vectorList"].append(v)
        return state
    
    def __setstate__(self,state):
        self.curCoordinateSystem=state["curCoordinateSystem"]
        self.flagShape=True
        self.flagPlacement=state["flagPlacement"] 
        self.flagExcute=state["flagExcute"]
        vectorList=[]
        
        for i in range(len(state["vectorList"])):
            v=FreeCAD.Vector(state["vectorList"][i][0],state["vectorList"][i][1],state["vectorList"][i][2])
            vectorList.append(v)
        self.vectorList=vectorList


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
