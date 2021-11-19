# -*- coding: utf-8 -*-
import FreeCAD, Part, math, PartChipic
from FreeCAD import Base
import FreeCADGui
from pivy import coin
from PySide import QtGui, QtCore
from Common.Tools import CoordinateSystemTools
from Common.Tools import PlacementTools,ObjectsTools
import os
import subprocess
import time
import math
from Modeling3D.Tools import  OtherTools
class Function:
    def __init__(self, obj):
        # 这里加一个flagRedraw是为了能够通过obj的这个属性的改变，使得这个模型可以间接调用redraw函数
        obj.addProperty("App::PropertyBool","flagRedraw","","").flagRedraw=True
        self.curCoordinateSystem=FreeCAD.ActiveDocument.CoordinateSystem
        self.vectorList=[]
        obj.addProperty("App::PropertyString","Expression","Object of a Function","").Expression="" #"x*x+y*y+z*z-1" #ZD
        ''' Add some custom properties to our box feature '''
        if self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Rectangular:
            obj.addProperty("App::PropertyVectorDistance", "Point_1", "Object of a Function", "Length of the box").Point_1 = FreeCAD.Vector(-2,-2,-2)
            obj.addProperty("App::PropertyVectorDistance", "Point_2", "Object of a Function", "Length of the box").Point_2 = FreeCAD.Vector(2,2,2)
            self.vectorList=[obj.Point_1,obj.Point_2]
        # '''极坐标系下的属性面板'''
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Polar:
            obj.Expression="" #"r**2+z**2-0.0001"
            obj.addProperty("App::PropertyPolVecDistance", "Point_1", "Object of a Function", "Length of the box").Point_1 = FreeCAD.Vector(0,0,0)
            obj.addProperty("App::PropertyPolVecDistance", "Point_2", "Object of a Function", "Length of the box").Point_2 = FreeCAD.Vector(0.01,30,0.01)
            
            self.vectorList=[obj.Point_1,obj.Point_2]
        elif self.curCoordinateSystem==CoordinateSystemTools.CoordinateType.Cylindrical:
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_1", "Object of a Function", "Length of the box").Point_1 = FreeCAD.Vector(0,0,-2)
            obj.addProperty("App::PropertyCylinderVecDistance", "Point_2", "Object of a Function", "Length of the box").Point_2 = FreeCAD.Vector(2,360,2)
            self.vectorList=[obj.Point_1,obj.Point_2]

        obj.addProperty("App::PropertyInteger", "Precision", "Object of a Function", "Precision of the function").Precision = 20
        ObjectsTools.addPropertyForVol(obj,ObjectsTools.ObjectType.Vol_Function,self.curCoordinateSystem)
        obj.addProperty("App::PropertyInteger","Order","","Order of the Extruded").Order=100

        self.orderBefore=obj.Order
        self.labelBofroe=obj.Label

        obj.Proxy = self
        self.placementBefore = obj.Placement
        #flagShape和flagPalcement为在移动过程中不能在属性面板中输入值，在输入值的时候不移动
        self.flagShape=True
        self.flagPlacement=True
        self.flagExcute=False
        obj.setEditorMode('Placement',2)
        obj.setEditorMode('flagRedraw',2)
        self.initObject(obj)
        #初始化重绘
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
        if prop=="flagRedraw":
            self.flagExcute=True
        #物体对象的Order发生改变时
        if prop=="Order":
            # if self.flagOrder:
                # self.flagLabel=False
            ObjectsTools.updateWhenOrderChanged(fp,self.orderBefore,fp.Order)
                # self.flagLabel=True
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

        ''' Print the name of the property that has changed '''
        if prop == "Point_1" or prop == "Point_2" or prop=="Expression" or prop=="Precision":
            if self.flagShape:
                self.flagShape=False
                self.flagPlacement=False
                #将物体置为原点
                fp.Placement=FreeCAD.Placement(FreeCAD.Vector(0.0,0.0,0.0),FreeCAD.Rotation(0.0,0.0,0.0,1.0))
                self.vectorList=[fp.Point_1,fp.Point_2]
                self.flagShape=True
                self.flagPlacement=True
                self.flagExcute=True
        elif prop == "Placement" :
            if self.flagPlacement:
                self.flagPlacement=False
                self.flagShape=False
                #设置属性自定义属性只读
                fp.setEditorMode("Point_1",1)
                fp.setEditorMode("Point_2",1)
                #坐标转换
                vectorList=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
                #转换结束
                pos = fp.Placement.Base.sub(self.placementBefore.Base)
                resultVectors=[]
                #
                #位移
                if pos!=FreeCAD.Vector(0.0,0.0,0.0):
                    resultVectors=PlacementTools.moveAdd(pos,vectorList)
                #旋转
                else:
                    resultVectors=PlacementTools.rotate(self.placementBefore,fp.Placement,vectorList)
                resultVectors=CoordinateSystemTools.recToOther(self.curCoordinateSystem,resultVectors)
                #转换完成
                fp.Point_1=resultVectors[0]
                fp.Point_2=resultVectors[1]
                self.vectorList=[fp.Point_1,fp.Point_2]
                self.flagPlacement=True
                self.flagShape=True
                self.flagExcute=False
                # 重塑
                pass
        ObjectsTools.fucNonUniformGrid(self.curCoordinateSystem,fp,prop)
        ObjectsTools.fucAttributeChange(fp,prop)

    def time_me(fn):
        def _wrapper(*args, **kwargs):
            start = time.clock()
            fn(*args, **kwargs)
            FreeCAD.Console.PrintError("Function time: "+str(time.clock()-start)+"\n")
            # print "%s cost %s second"%(fn.__name__, time.clock() - start)
        return _wrapper
    @time_me
    def redraw(self,obj):
        
        if obj.Precision>=30:
            obj.Precision=30
        if obj.Precision<=10:
            obj.Precision=10

       
        try:
            # @fubiao这里涉及一个解析过程
            expressionStr=OtherTools.parseExpressionStr(obj.Expression.replace(" ",""))
            p1x=float(OtherTools.parseExpressionStr(str(obj.Point_1[0]).replace(" ","")))
            p2x=float(OtherTools.parseExpressionStr(str(obj.Point_2[0]).replace(" ","")))
            p1y=float(OtherTools.parseExpressionStr(str(obj.Point_1[1]).replace(" ","")))
            p2y=float(OtherTools.parseExpressionStr(str(obj.Point_2[1]).replace(" ","")))
            p1z=float(OtherTools.parseExpressionStr(str(obj.Point_1[2]).replace(" ","")))
            p2z=float(OtherTools.parseExpressionStr(str(obj.Point_2[2]).replace(" ","")))
            FreeCAD.Console.PrintError("expressionStr: "+str(expressionStr)+" p1x:"+str(p1x)+" p2x:"+str(p2x)+" p1y:"+str(p1y)+" p2y:"+str(p2y)+" p1z:"+str(p1z)+" p2z: "+str(p2z)+"\n")
            
            obj.Shape=PartChipic.makeFuncMesh(1,expressionStr,p1x,p2x,p1y,p2y,p1z,p2z,self.curCoordinateSystem,str(obj.Precision),obj.Attribute)
            # obj.Shape=PartChipic.makeFuncMesh(1,obj.Expression,obj.Point_1[0],obj.Point_2[0],obj.Point_1[1],obj.Point_2[1],obj.Point_1[2],obj.Point_2[2],self.curCoordinateSystem,str(obj.Precision),obj.Attribute)
            # FreeCAD.Console.PrintError("expressionStr: "+str(obj.Expression)+" p1x:"+str(obj.Point_1[0])+" p2x:"+str(obj.Point_2[0])+" p1y:"+str(obj.Point_1[1])+" p2y:"+str(obj.Point_2[1])+" p1z:"+str(obj.Point_1[2])+" p2z: "+str(obj.Point_2[2])+"\n")
        except:
            from Modeling.Common.Tools import DocumentTools
            DocumentTools.printErrorMessage("Redraw Function Failed!")

    def redraw2(self,obj):
        expressionStr=OtherTools.parseExpressionStr(obj.Expression.replace(" ",""))
        import re
        expressionStr=re.sub(r"\b[r|R]\b","(sqrt(x*x+y*y))",expressionStr)
        expressionStr=re.sub(r"\btheta\b","(atan(y/x))",expressionStr,flags=re.IGNORECASE)
        expressionStr=OtherTools.parseFunctionObjStr(expressionStr)
        errorCode=-1
        if obj.Precision>=30:
            obj.Precision=30
        if obj.Precision<=10:
            obj.Precision=10
        try:
            # t0=time.clock()
            [tempPoint1,tempPoint2]=ObjectsTools.getRMinMaxPoints(obj.Point_1,obj.Point_2,self.curCoordinateSystem)
            # t1=time.clock()
            # FreeCAD.Console.PrintError("turn points time"+str(t1-t0)+"\n")
            # tempPoints=CoordinateSystemTools.otherToRec(self.curCoordinateSystem,self.vectorList)
            # tempPoint1=tempPoints[0]
            # tempPoint2=tempPoints[1]
            FreeCAD.Console.PrintError(tempPoint1)
            FreeCAD.Console.PrintError(tempPoint2)
            errorCode=0
            shell=Part.makeFuncMesh(1,expressionStr,tempPoint1[0],tempPoint2[0],tempPoint1[1],tempPoint2[1],tempPoint1[2],tempPoint2[2],FreeCAD.getUserAppDataDir()+"\\tempFunc.json",str(obj.Precision))
            # Part.show(shell)
            errorCode=1
            funcShape=Part.makeSolid(shell)
            # Part.show(funcShape)
            # FreeCAD.Console.PrintError(obj.Point_1)
            # FreeCAD.Console.PrintError(obj.Point_2)
            errorCode=2
            borderShape=ObjectsTools.getShapeOfComformal(self.curCoordinateSystem,obj.Point_1,obj.Point_2)
            # Part.show(borderShape)
            errorCode=3
            commonShape=borderShape.common(funcShape)

            # Part.show(commonShape)
            errorCode=4
            obj.Shape=commonShape
            # obj.Shape=Part.makeSolid(Part.makeFuncMesh(1,expressionStr,tempPoint1[0],tempPoint2[0],tempPoint1[1],tempPoint2[1],tempPoint1[2],tempPoint2[2],"E:\\tempFunc.json",str(obj.Precision)))
        
        except:
            from Modeling.Common.Tools import DocumentTools
            DocumentTools.printErrorMessage("Redraw Function Failed!")
            if errorCode==-1:
                DocumentTools.printErrorMessage("getRMinMaxPoints error!")
            elif errorCode==0:
                DocumentTools.printErrorMessage("makeFuncMesh error!")
            elif errorCode==1:
                DocumentTools.printErrorMessage("make solid error!")
            elif errorCode==2:
                DocumentTools.printErrorMessage("getShapeOfComformal Error!")
            elif errorCode==3:
                DocumentTools.printErrorMessage("common error!")
            elif errorCode==4:
                DocumentTools.printErrorMessage("Shape error!")
            obj.Shape=Part.Shape()
        FreeCAD.Console.PrintMessage("ErorCOde: "+str(errorCode)+"\n")

    def execute(self, fp):
        #设置自定义属性可编辑
        fp.setEditorMode("Point_1",0)
        fp.setEditorMode("Point_2",0)
        if self.flagExcute:
            self.redraw(fp)
            self.flagExcute=False




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


class ViewProviderFunction:
    def __init__(self, obj):
        ''' Set this object to the proxy object of the actual view provider '''
        obj.Proxy = self

    def attach(self, obj):
        ''' Setup the scene sub-graph of the view provider, this method is mandatory '''
        return

    def updateData(self, fp, prop):
        ''' If a property of the handled feature has changed we have the chance to handle this here '''
        return

    def getDisplayModes(self, obj):
        ''' Return a list of display modes. '''
        modes = []
        return modes

    def getDefaultDisplayMode(self):
        ''' Return the name of the default display mode. It must be defined in getDisplayModes. '''
        return "Wireframe"

    def setDisplayMode(self, mode):
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

    def __setstate__(self, state):
        ''' When restoring the pickled object from document we have the chance to set some
        internals here. Since no data were pickled nothing needs to be done here.
        '''
        return None


# # Create a 3D parametric Curve.
# # Author: Gomez Lucio
# # Modified by Laurent Despeyroux on 9th feb 2015
# #   - 3 helping variables added a, b and c
# #   - enlarged GUI
# #   - more flexible GUI
# #   - basic error mangement
 
# import FreeCAD
# from PySide import QtGui,QtCore
# import Part
# import Draft
# from math import *
 
# class ParamCurv(QtGui.QWidget):
#     def __init__(self):
#         super(ParamCurv, self).__init__()
#         self.initUI()
#     def initUI(self):
#         self.t0 = QtGui.QLabel("Equation :",self)
#         self.ta = QtGui.QLabel("    a(t) ",self)
#         self.la = QtGui.QLineEdit(self)
#         self.la.setText("37")
#         self.tb = QtGui.QLabel("    b(a,t) ",self)
#         self.lb = QtGui.QLineEdit(self)
#         self.lb.setText("1")
#         self.tc = QtGui.QLabel("    c(a,b,t) ",self)
#         self.lc = QtGui.QLineEdit(self)
#         self.lc.setText("(a+cos(a*t)*2)*b")
#         self.t1 = QtGui.QLabel("    X(a,b,c,t) ",self)
#         self.l1 = QtGui.QLineEdit(self)
#         self.l1.setText("cos(t)*c")
#         self.t2 = QtGui.QLabel("    Y(a,b,c,t) ",self)
#         self.l2 = QtGui.QLineEdit(self)
#         self.l2.setText("sin(t)*c")
#         self.t3 = QtGui.QLabel("    Z(a,b,c,t) ",self)
#         self.l3 = QtGui.QLineEdit(self)
#         self.l3.setText("0")
#         self.t31 = QtGui.QLabel("Parameters :",self)
#         self.t4 = QtGui.QLabel("    Min t ",self)
#         self.l4 = QtGui.QLineEdit(self)
#         self.l4.setText("0")
#         self.t5 = QtGui.QLabel("    Max t ",self)
#         self.l5 = QtGui.QLineEdit(self)
#         self.l5.setText("6.283185")
#         self.t6 = QtGui.QLabel("    Interval ",self)
#         self.l6 = QtGui.QLineEdit(self)
#         self.l6.setText("0.01")
#         self.t7 = QtGui.QLabel("Type of Line :",self)
#         self.op1 = QtGui.QCheckBox("    Polyline",self)
#         self.poly = False
#         self.op1.stateChanged.connect(self.polyState)
#         self.op1.setCheckState(QtCore.Qt.Checked)
#         self.op2 = QtGui.QCheckBox("    Bspline",self)
#         self.bsline = False
#         self.op2.stateChanged.connect(self.bsplineState)
#         self.t8 = QtGui.QLabel("    Closed Curve",self)
#         self.op3 = QtGui.QCheckBox("",self)
#         self.cclose = False
#         self.op3.stateChanged.connect(self.ccloseState)
#         self.createbutt = QtGui.QPushButton("Create Curve",self)
#         self.exitbutt = QtGui.QPushButton("Close",self)
#         layout = QtGui.QGridLayout()
#         self.resize(420, 380)
#         self.setWindowTitle("Parametric Curve ")
#         i = 0
#         layout.addWidget(self.t0, i, 0)
#         i = i+1
#         layout.addWidget(self.ta, i, 0)
#         layout.addWidget(self.la, i, 1)
#         i = i+1
#         layout.addWidget(self.tb, i, 0)
#         layout.addWidget(self.lb, i, 1)
#         i = i+1
#         layout.addWidget(self.tc, i, 0)
#         layout.addWidget(self.lc, i, 1)
#         i = i+1
#         layout.addWidget(self.t1, i, 0)
#         layout.addWidget(self.l1, i, 1)
#         i = i+1
#         layout.addWidget(self.t2, i, 0)
#         layout.addWidget(self.l2, i, 1)
#         i = i+1
#         layout.addWidget(self.t3, i, 0)
#         layout.addWidget(self.l3, i, 1)
#         i = i+1
#         layout.addWidget(self.t31, i, 0)
#         i = i+1
#         layout.addWidget(self.t4, i, 0)
#         layout.addWidget(self.l4, i, 1)
#         i = i+1
#         layout.addWidget(self.t5, i, 0)
#         layout.addWidget(self.l5, i, 1)
#         i = i+1
#         layout.addWidget(self.t6, i, 0)
#         layout.addWidget(self.l6, i, 1)
#         i = i+1
#         layout.addWidget(self.t8, i, 0)
#         layout.addWidget(self.op3, i, 1)
#         i = i+1
#         layout.addWidget(self.t7, i, 0)
#         i = i+1
#         layout.addWidget(self.op1, i, 0)
#         layout.addWidget(self.op2, i, 1)
#         i = i+1
#         layout.addWidget(self.createbutt, i, 0)
#         layout.addWidget(self.exitbutt, i, 1)
#         self.setLayout(layout)
#         self.show()
#         QtCore.QObject.connect(self.createbutt, QtCore.SIGNAL("pressed()"),self.draw)
#         QtCore.QObject.connect(self.exitbutt, QtCore.SIGNAL("pressed()"),self.close)
#     def ccloseState(self, state):
#         if state == QtCore.Qt.Checked:
#             self.cclose = True
#         else:
#             self.cclose = False
#     def bsplineState(self, state):
#         if state == QtCore.Qt.Checked:
#             self.bsline = True
#             self.op1.setCheckState(QtCore.Qt.Unchecked)
#         else:
#             self.bsline = False
#     def polyState(self, state):
#         if state == QtCore.Qt.Checked:
#             self.poly = True
#             self.op2.setCheckState(QtCore.Qt.Unchecked)
#         else:
#             self.poly = False
#     def draw(self):
#         msgBox = QtGui.QMessageBox()
#         fa = str(self.la.text())
#         fb = str(self.lb.text())
#         fc = str(self.lc.text())
#         fx = str(self.l1.text())
#         fy = str(self.l2.text())
#         fz = str(self.l3.text())
#         t = float(str(self.l4.text()))
#         tf = float(self.l5.text())
#         intv = float(str(self.l6.text()))
#         d=(tf-t)/intv
#         matriz = []
#         for i in range(int(d)):
#             try:
#               value="a"
#               a=eval(fa)
#               value="b"
#               b=eval(fb)
#               value="c"
#               c=eval(fc)
#               value="X"
#               fxx=eval(fx)
#               value="Y"
#               fyy=eval(fy)
#               value="Z"
#               fzz=eval(fz)
#             except ZeroDivisionError:
#               msgBox.setText("Error division by zero in calculus of "+value+"() for t="+str(t)+" !")
#               msgBox.exec_()
#             except:
#               msgBox.setText("Error in the formula of "+value+"() !")
#               msgBox.exec_()
#             matriz.append(FreeCAD.Vector(fxx,fyy,fzz))
#             t+=intv
#         curva = Part.makePolygon(matriz)
#         if self.bsline == True:
#             Draft.makeBSpline(curva,closed=self.cclose,face=False)
#         if self.poly == True:
#             Draft.makeWire(curva,closed=self.cclose,face=True)
#     def close(self):
#         self.hide()
 
# ParamCurv()