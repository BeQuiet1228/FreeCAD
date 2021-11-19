# encoding:utf-8
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication, QMainWindow, QDockWidget, QTreeWidgetItem
import FreeCAD,FreeCADGui
from Modeling3DCommand._Operation_Clip.UI import Vol_Clip_Dlg
import Part
import Draft
import datetime
import os
from FreeCAD import Base
try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Clip(QtGui.QDockWidget):
    def __init__(self, obj=None):
        QtGui.QDockWidget.__init__(self)
        self.ui = Vol_Clip_Dlg.Ui_DockWidget()
        self.ui.setupUi(self)


        self.ui.pushButton_ok.clicked.connect(self.pushBtnOk)
        self.ui.pushButton_cancel.clicked.connect(self.pushBtnCancle)
        self.ui.horizontalSlider.valueChanged.connect(self.sliderChanged)
        self.ui.doubleSpinBox_progress.valueChanged.connect(self.spinBoxChanged)
        self.ui.radioButton_outline.setChecked(False)
        self.ui.radioButton_object.setChecked(True)
        self.ui.doubleSpinBox_X.valueChanged.connect(self.dirxChange)
        self.ui.doubleSpinBox_Y.valueChanged.connect(self.diryChange)
        self.ui.doubleSpinBox_Z.valueChanged.connect(self.dirzChange)

        # self.ui.checkBox_showCutFace.set
        # 先隐藏模型
        self.hideObjects()
        # self.ui.radioButton_outline.
        #init value
        self.ui.doubleSpinBox_X.setValue(1.0)
        self.ui.doubleSpinBox_Y.setValue(0.0)
        self.ui.doubleSpinBox_Z.setValue(1.0)
        self.ui.horizontalSlider.setValue(50.0)

        pass
    def closeEvent(self,event):
        self.restoreObjects()
    def pushBtnOk(self):
        #test
        # print "test"
        # default to no visible cross-ection
        self.cs.ViewObject.Visibility = False

        # check if the sliding axis is invalid
        if self.xdir == 0.0 and self.ydir == 0.0 and self.zdir == 0.0:
            QtGui.QMessageBox.warning(None, _translate("MainWindow",
                                                       "Cross-section", None),
                                      _translate("MainWindow", "The sliding axis has zero length\n" +
                                                 "Please set a valid axis.", None),
                                      QtGui.QMessageBox.Ok,
                                      QtGui.QMessageBox.Ok)
        else:
            # First we compute the 0% and 100% positions on the sliding axis
            if self.xdir < 0.0:
                x = self.xmax + self.fraction * self.xdir
            else:
                x = self.xmin + self.fraction * self.xdir
            if self.ydir < 0.0:
                y = self.ymax + self.fraction * self.ydir
            else:
                y = self.ymin + self.fraction * self.ydir
            if self.zdir < 0.0:
                z = self.zmax + self.fraction * self.zdir
            else:
                z = self.zmin + self.fraction * self.zdir

            r = 2 * max(self.xmax - self.xmin, self.ymax - self.ymin,
                        self.zmax - self.xmin)
            mp(r)
            # Display the dimensions
            dimDep = "X " + str(x) + " mm , Y " + str(y) + " mm , Z " + str(z) + " mm"
            # FreeCAD.Console.PrintMessage(dimDep + "\n")

            # Create a big enough disc in the cross-section plane
            c = Part.makeCircle(r, Base.Vector(x, y, z),
                                Base.Vector(self.xdir, self.ydir, self.zdir))
            f = Part.Face(Part.Wire(c))
            # FreeCAD.Console.PrintMessage("r:"+str(r)+"x:"+str(x)+"y:"+str(y)+"z:"+str(z)+"xdir:"+str(self.xdir)+"ydir:"+str(self.ydir)+"zdir:"+str(self.zdir)+"\n")
            # Part.show(f)
            # 测试
            # Part.show(f)
            l = list()  # list for cross-section parts
            n = 0
            for p in self.oblist:  # stupid Python list has no length function
                n = n + 1
            # mp("N:")
            # mp(n)
            # #测试
            # for i in range(len(self.oblist)):
            #     FreeCAD.Console.PrintMessage("oblist: "+str(self.oblist[i].Label)+"\n")
            # mp("LIST:")
            # mp(self.oblist)
            something = 0
            # if self.cross_section_type == 1:
            cyl=None
            if self.ui.radioButton_outline.isChecked():
                # wire line cross-section
                for i in range(n):
                    if self.oblist[i].TypeId != str("Drawing::FeatureViewPython"):  # add
                        if self.OriginalVisibilities[i]:
                            ob = self.oblist[i].Shape.section(f)
                            # check for valid section part
                            if ob.BoundBox.XMin <= ob.BoundBox.XMax:
                                l.append(ob)
                                something = 1
            else:
                FreeCAD.Console.PrintMessage("DO  once\n")
                # cut shape cross-section
                # extrude our cross-ection disc into a cylinder
                cyl = f.extrude(Base.Vector(self.xdir, self.ydir, self.zdir))
                # Part.show(cyl)
                # return
                # FreeCAD.Console.PrintMessage("oblist "+str(len(self.oblist))+"\n")
                # for obs in self.oblist:
                #     FreeCAD.Console.PrintMessage(str(obs.Label)+"\n")
                # return;
                # doc = FreeCAD.ActiveDocument
                # starttime = datetime.datetime.now()

                # solidShapes=[]
                # clipShapes=[]
                # # if len(self.oblist)!=0:
                # #     solidShapes=self.oblist[0].Shape.Solids
                # comlistBase=[]
                # for objItem in self.oblist:
                #     comlistBase.append(objItem)
                #     FreeCAD.Console.PrintError("objItem.Name:"+str(objItem.Label)+"\n")
                #     solidShapes=solidShapes+objItem.Shape.Solids
                # progress_bar = FreeCAD.Base.ProgressIndicator()
                # progress_bar.start("Do clipping command...",len(solidShapes))
                # threads=[]
                # '''for i in range(n):
                #     if self.oblist[i].TypeId != str("Drawing::FeatureViewPython"):  # add
                #         if self.OriginalVisibilities[i]:
                #             if (self.oblist[i].Shape.Volume <= 0.0):
                #                 continue
                #             doc.recompute()
                #             # error log:  FeaturePartBoolean.cpp line 80 
                #             # Linked object is not a Part object
                #             acut = doc.addObject("Part::Cut", "Cut")
                #             abase = Draft.clone(self.oblist[i])
                #             # abase=doc.addObject("Part::FeaturePython","abase")
                #             # abase.Shape=self.oblist[i].Shape
                #             # abase.ViewObject.Proxy=0
                #             abase.ViewObject.DiffuseColor = self.oblist[i].ViewObject.DiffuseColor
                #             abase.ViewObject.Transparency = self.oblist[i].ViewObject.Transparency
                #             doc.recompute()
                #             atool = doc.addObject("Part::Feature")
                #             atool.Shape = cyl
                #             # atool.ViewObject.ShapeColor = self.oblist[i].ViewObject.ShapeColor  # (0.25,0.57,0.35)
                #             # atool.ViewObject.Transparency = self.oblist[i].ViewObject.Transparency
                #             doc.recompute()
                #             acut.Base = abase
                #             acut.Tool = atool
                #             acut.ViewObject.DiffuseColor = abase.ViewObject.DiffuseColor
                #             doc.recompute()
                #             if acut.Shape.isValid() and acut.Shape.Volume > 0.0:
                #                 ob = doc.addObject("Part::Feature")
                #                 ob.Shape = acut.Shape
                #                 ob.ViewObject.DiffuseColor = acut.ViewObject.DiffuseColor
                #                 doc.recompute()
                #                 l.append(ob)
                #                 something = 2
                #             doc.removeObject(acut.Name)
                #             # doc.recompute()
                #             doc.removeObject(abase.Name)
                #             # doc.recompute()
                #             doc.removeObject(atool.Name)
                #             doc.recompute()
                #     progress_bar.next()
                # '''
                something=2
                # FreeCAD.Console.PrintError("len of solidsShapes:"+str(len(solidShapes))+"\n")
                # for i in range(len(solidShapes)):
                #     try:
                #     # FreeCAD.Console.PrintMessage(str(i)+"\n")
                #         s=solidShapes[i].cut(cyl)
                #     # Part.show(s)
                #     # FreeCAD.Console.PrintMessage("a\n")
                #         l.append(s)
                #     # FreeCAD.Console.PrintMessage("b\n")

                #     # l.append(solidShapes[i].cut(cyl.Shape))
                #     except:
                #         FreeCAD.Console.PrintError("solidShapes "+str(i)+"error\n")
                #     progress_bar.next()
                # FreeCAD.Console.PrintError("end\n")
                # makeCompound
                
                # progress_bar.stop()
                # endtime = datetime.datetime.now()
                # FreeCAD.Console.PrintMessage("time1: \n")
                # FreeCAD.Console.PrintMessage((endtime-starttime).seconds)
                # FreeCAD.Console.PrintMessage("time1End: \n")
            # ltemp=[]
            # for lItem in l:
            #     if str(lItem) != "<group object>":
            #         ltemp.append(lItem)
            # l=ltemp
            FreeCAD.Console.PrintMessage("Here "+str(something)+"\n")
            if something == 1:
                s = Part.makeCompound(l)
                if s.isValid():
                    self.cs.Shape = s
                    self.cs.ViewObject.Visibility = True
            starttime = datetime.datetime.now()
            if something == 2:
                
                '''
                feature = FreeCAD.ActiveDocument.addObject("Part::Compound", "Compound")
                # error log: ViewProviderExt.cpp line 1211
                # Cannot compute Inventor representation for the shape of %s.\n",pcObject->getNameInDocument()
                feature.Links = l
                FreeCAD.ActiveDocument.recompute()
                if feature.Shape.isValid():
                    self.cs.Shape = feature.Shape.copy()
                    self.cs.ViewObject.DiffuseColor = feature.ViewObject.DiffuseColor
                    self.cs.ViewObject.Visibility = True
                    # FreeCADGui.ActiveDocument.getObject(self.cs.Name).DisplayMode=u"Flat Lines"
                    FreeCAD.ActiveDocument.recompute()
                for od in l:
                    FreeCAD.ActiveDocument.removeObject(od.Name)
                    # FreeCAD.ActiveDocument.recompute()
                FreeCAD.ActiveDocument.removeObject(feature.Name)
                FreeCAD.ActiveDocument.recompute()
                '''
                # Part.show(Part.makeCompound(l))
                # for i in range(len(l)):
                #     Part.show(l[i])
                # self.cs.Shape=Part.makeCompound(l)
                # FreeCAD.Console.PrintMessage(len(comlistBase))
                # for obtitem in comlistBase:
                #     FreeCAD.Console.PrintError("objItem.Name:"+str(obtitem.Label)+"\n")

                # s=Part.makeCompound(l)
                # Part.show(s)
                # FreeCAD.Console.PrintError("0\n")
                # resultCom=FreeCAD.activeDocument().addObject("Part::MultiCommon","Common")
                # FreeCAD.Console.PrintError("1\n")

                # resultCom.Shapes=comlistBase
                
                # self.cs.Shape=Part.makeCompound(l)
                # self.cs.ViewObject.DiffuseColor=self.test(cyl,self.cs)
                # FreeCAD.Console.PrintError("L0g2\n")
                import PartGui
                # FreeCAD.Console.PrintError(cyl)

                # if self.ui.checkBox_showCutFace.isChecked():
                #     PartGui.customBoolean(self.beBooleanObj,cyl,self.cs,1)
                # else:
                #     PartGui.customBoolean(self.beBooleanObj,cyl,self.cs,0)
                PartGui.customBoolean(self.beBooleanObj,cyl,self.cs,1)
                # PartGui.customBoolean(cyl,self.cs)
                # FreeCAD.Console.PrintError(str(self.ui.checkBox_showCutFace.isChecked()))
                for obj in self.oblist:
                    obj.ViewObject.Visibility = False
                # self.hideObjects()
                # FreeCAD.Console.PrintMessage(self.getDiffuseColor(self.oblist,self.cs)) 
                # self.cs.ViewObject.DiffuseColor=self.getDiffuseColor(self.oblist,self.cs)
                # self.cs.ViewObject.DiffuseColor=FreeCAD.ActiveDocument.ResultShape.ViewObject.DiffuseColor
                self.cs.ViewObject.Visibility = True
                self.cs.ViewObject.Transparency=50
            # endtime = datetime.datetime.now()
            # FreeCAD.Console.PrintMessage("time2: \n")
            # FreeCAD.Console.PrintMessage((endtime-starttime).seconds)
            # FreeCAD.Console.PrintMessage("time2End: \n")

            FreeCADGui.updateGui()
            
        #是否保存当前图片
        if self.ui.checkBox_savePic.isChecked():
            self.savePicture()

        pass
    def test(self,cy1,resultObj):
        # FreeCAD.Console.PrintMessage(cy1.Faces)
        # 经测试，是第二个面与模型相切
        # FreeCAD.Console.PrintMessage("0\n")
        cutFace0=cy1.Faces[0]
        cutFace1=cy1.Faces[1]
        cutFace2=cy1.Faces[2]

        FreeCAD.Console.PrintMessage("1\n")

        resFaces=resultObj.Shape.Faces
        FreeCAD.Console.PrintMessage("2\n")
        diffuseCol=resultObj.ViewObject.DiffuseColor

        for i in range(len(resFaces)):
            distanceInfos1=cutFace1.distToShape(resFaces[i])
            # distanceInfos1=cutFace1.distToShape(resFaces[i])
            # distanceInfos2=cutFace2.distToShape(resFaces[i])

            # if distanceInfos0==0.0 or distanceInfos1==0.0 or distanceInfos2==0.0:
            if distanceInfos1[0]==0.0:
                if len(diffuseCol)>i:
                    diffuseCol[i]=(0.8,0.0,0.0)
                else:
                    FreeCAD.Console.PrintError("len difCol:"+str(len(diffuseCol))+"\n")
                FreeCAD.Console.PrintMessage("cut: i:"+str(i)+"\n")
                continue
        return diffuseCol

    def getDiffuseColor(self,baseObjs,resultObj):
        objHasSelect=[]
        st = datetime.datetime.now()
        diffuseColor=[]
        for faceItem in resultObj.Shape.Faces:
            flagFound=False
            # 遍历模型
            for objItem in baseObjs:
                fs=objItem.Shape.Faces
                for faceIndex in range(len(fs)):
                    # FreeCAD.Console.PrintMessage("2\n")

                    distanceInfos=faceItem.distToShape(fs[faceIndex])
                    # FreeCAD.Console.PrintMessage("0\n")
                    # FreeCAD.Console.PrintMessage(str(distanceInfos[0])+" ")
                    # FreeCAD.Console.PrintMessage("1\n")

                    if distanceInfos[0]==0.0:
                        # indexFace=objItem.Shape.Faces.index(faceItem)
                        colors=objItem.ViewObject.DiffuseColor
                        if len(colors)>faceIndex:
                            diffuseColor.append(objItem.ViewObject.DiffuseColor[faceIndex])
                        else:
                            diffuseColor.append(objItem.ViewObject.ShapeColor)
                        flagFound=True
                        # FreeCAD.Console.PrintMessage("3\n")
                        break
                # FreeCAD.Console.PrintMessage("4\n")
                if flagFound:
                    break
            # FreeCAD.Console.PrintMessage("5\n")
            if flagFound:
                continue
            else:
                diffuseColor.append((0.80,0.80,0.80))
        et = datetime.datetime.now()
        FreeCAD.Console.PrintMessage("getDiffuseTime:"+str((et-st).seconds))
        return diffuseColor

        
    def pushBtnCancle(self):
        self.close()
        pass
    def savePicture(self):
        import shutil
        FreeCADGui.SendMsgToActiveView("ViewSelection")
        tempPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Temp"
        if os.path.exists(tempPath):
            shutil.rmtree(tempPath)
        os.makedirs(tempPath)
        picturePath = tempPath + "/cutPicture.bmp"
        FreeCADGui.activeDocument().activeView().saveImage(picturePath, 500, 500, 'Current')
        import ImageGui
        ImageGui.open(picturePath)

    def sliderChanged(self,val):
        self.fraction = val / 100.0
        self.ui.progressBar.setValue(val)
        self.ui.doubleSpinBox_progress.setValue(val)
        pass
    def spinBoxChanged(self,val):
        self.ui.progressBar.setValue(val)
        self.ui.horizontalSlider.setValue(val)
        pass
    # User changed axis vector
    # Compute a new axis vector whose length just covers the model
    def updateAxis(self):
        self.axisX=self.ui.doubleSpinBox_X.value()
        self.axisY=self.ui.doubleSpinBox_Y.value()
        self.axisZ=self.ui.doubleSpinBox_Z.value()

        # mp(str(self.axisX)+" "+str(self.axisY)+" "+str(self.axisZ))
        ldir = 0.0
        if self.axisX != 0.0:
            ldir = (self.xmax - self.xmin) / abs(self.axisX)
        if self.axisY != 0.0:
            ldir = max(ldir, (self.ymax - self.ymin) / abs(self.axisY))
        if self.axisZ != 0.0:
            ldir = max(ldir, (self.zmax - self.zmin) / abs(self.axisZ))
        self.xdir = self.axisX * ldir
        self.ydir = self.axisY * ldir
        self.zdir = self.axisZ * ldir
        # mp(str(self.xdir)+" "+str(self.ydir)+" "+str(self.zdir))
    def dirxChange(self,val):
        self.axisX = val
        self.updateAxis()
    def diryChange(self,val):
        self.axisY = val
        self.updateAxis()
    def dirzChange(self,val):
        self.axisZ = val
        self.updateAxis()

    def restoreObjects(self):
        FreeCAD.Console.PrintMessage("resotreObjexs\n")
        FreeCAD.Console.PrintMessage("name: "+str(self.cs.Name)+"\n")
        n = 0
        for p in self.oblist:  # stupid Python list has no length function
            n = n + 1
        for i in range(n):
            self.oblist[i].ViewObject.Visibility = self.OriginalVisibilities[i]
        try:
            
            FreeCAD.ActiveDocument.removeObject(self.cs.Name)
            # FreeCAD.ActiveDocument.removeObject(self.cs)
        except Exception:
            None

    def hideObjects(self):
        self.startup_failed = False
        self.fraction = 0.5
        self.axisX = 0.0
        self.axisY = 0.0
        self.axisZ = 1.0
        self.cross_section_type = 1

        # We must have something to do a cross-section on
        if FreeCAD.ActiveDocument is None:
            QtGui.QMessageBox.warning(None, _translate("MainWindow",
                                                       "Cross-section", None),
                                      _translate("MainWindow", "There is no Active Document\n" +
                                                 "Create one and run this macro again.", None),
                                      QtGui.QMessageBox.Cancel,
                                      QtGui.QMessageBox.Cancel)
            self.startup_failed = True
            self.parent.destroy()  # This will close the window
        else:

            # Make a list of the user's objects
            # WARNING!!
            # This list is persistent. We'll get confused if the user deletes or
            # adds objects while the macro is active
            self.oblist = []
            self.beBooleanObj=[]
            objectsAll= FreeCAD.ActiveDocument.Objects
            for obj in objectsAll:
                
                if obj.TypeId=='Part::FeaturePython'and obj.ViewObject.Visibility:
                    self.oblist.append(obj)
                    # # 体
                    # if hasattr(obj,"Attribute"):
                    #     self.oblist.append(obj)
                    # else:
                    #     obj.ViewObject.Visibility = False
                if hasattr(obj,"Attribute") and \
                            (getattr(obj,"Attribute")!="NotDefine" or(getattr(obj,"Attribute")=="NotDefine" and obj.ViewObject.Visibility)):
                    self.beBooleanObj.append(obj)
            # Create the cross-section object
            self.cs = FreeCAD.ActiveDocument.addObject("Part::FeaturePython",
                                                       "Generated__cross_section")
            self.cs.addProperty("Part::PropertyShapeHistory","History","","")
            self.cs.ViewObject.Proxy=0

            self.beBooleanObj.append(self.cs)

            self.OriginalVisibilities = list()
            self.xmin = 1000.0
            self.xmax = -1000.0
            self.ymin = 1000.0
            self.ymax = -1000.0
            self.zmin = 1000.0
            self.zmax = -1000.0
            #            n = 0
            #            for p in self.oblist: # stupid Python list has no length function
            #                n = n + 1
            ############################# Skip the <group object> ########################         # add
            b0 = []
            for x0 in self.oblist:
                if str(x0) != "<group object>":
                    b0.append(x0)
            self.oblist = b0
            n = len(self.oblist)
            ###############################################################################
            # Make a list of the visible objects and make them invisible while
            # the macro is active
            # Also we compute the bounding box of the model
            for i in range(n):
                # mp("a")
                vis = self.oblist[i].ViewObject.Visibility
                self.OriginalVisibilities.append(vis)
                if vis:
                    # mp("b")
                    if self.oblist[i].TypeId != str("Drawing::FeatureViewPython"):  # add
                        # mp("c")
                        # self.oblist[i].ViewObject.Visibility = False
                        b = self.oblist[i].Shape.BoundBox
                        if b.XMin < self.xmin:
                            self.xmin = b.XMin
                            # self.oxmin=self.oblist[i]
                            # mp(self.oxmin.Label)
                            # mp("1")
                        if b.XMax > self.xmax:
                            self.xmax = b.XMax
                            # self.oxmax=self.oblist[i]
                            # mp(self.oxmax.Label)
                            # mp("2")
                        if b.YMin < self.ymin:
                            self.ymin = b.YMin
                            # self.oymin=self.oblist[i]
                            # mp(self.oymin.Label)
                            # mp("3")
                        if b.YMax > self.ymax:
                            self.ymax = b.YMax
                            # self.oymax=self.oblist[i]
                            # mp(self.oymax.Label)
                            # mp("4")
                        if b.ZMin < self.zmin:
                            self.zmin = b.ZMin
                        #     self.ozmin=self.oblist[i]
                        #     mp(self.ozmin.Label)
                        #     mp("5")
                        if b.ZMax > self.zmax:
                            self.zmax = b.ZMax
                            # self.ozmax=self.oblist[i]
                            # mp(self.ozmax.Label)
                            # mp("6")
            # Moan and give up if there is nothing to cross-section
            if self.xmax <= self.xmin \
                    or self.ymax <= self.ymin \
                    or self.zmax <= self.zmin:
                QtGui.QMessageBox.warning(None, _translate("MainWindow",
                                                           "Cross-section", None),
                                          _translate("MainWindow",
                                                     "There are no visible solid objects\n" +
                                                     "Create some and run this macro again.", None),
                                          QtGui.QMessageBox.Cancel,
                                          QtGui.QMessageBox.Cancel)
                self.restoreObjects()
                self.startup_failed = True
                FreeCAD.ActiveDocument.removeObject("Generated__cross_section")
                self.parent.destroy()  # This will close the window
            else:
                # Trigger initial display
                self.updateAxis()
#答应测试
def mp(msg):
    FreeCAD.Console.PrintMessage(msg)
    FreeCAD.Console.PrintMessage("\n")