# encoding:utf-8
import FreeCAD
import FreeCADGui
import PySide
from PySide import QtCore, QtGui
from Modeling.Common.Tools import ObjectsTools 
from Physics.PhysicsTools import SetVisibilityOfModels
# import os
# import Units

class SingleClickCommand:
    # @伏彪这里将lastclick重新定义为： 之前的模型，之前模型的颜色，即这个list肯定是成对出现的
    lastClick = []
    # FreeCAD.Console.PrintError('\n创建SigleClick对象！！！！')
    def IsActive(self):
        pass
        return True

    def Activated(self):
        self.changeClickObj()
        self.SingleClickDisplayMode()
        pass

    def GetResources(self):
        #为了方便此处不修改，用不到
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/Modeling3DResources/3D_Vol_Annular.svg"
        MenuText = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular')
        ToolTip = QtCore.QT_TRANSLATE_NOOP(
            'Annular',
            'Create a new Annular instance on top of the hull geometry')
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}
    def SingleClickDisplayMode(self):
        objs = FreeCADGui.Selection.getSelection()
        # FreeCAD.Console.PrintError('\n 所选中的obj： '+str(obj) + '\n')
        if len(objs)==0:
            pass
        elif len(objs)==1:
            if 'Type' in objs[0].PropertiesList:
                try:
                    # 将被引用的模型设置85的透明度
                    objsBeUsed=SetVisibilityOfModels.setVisibility(85)
                    FreeCAD.Console.PrintError('\n进入单机效果函数')
                    obj_resultshape = FreeCAD.ActiveDocument.ResultShape
                    obj_resultshape.ViewObject.DisplayMode = u'Flat Lines'
                    # obj_resultshape.ViewObject.ShapeColor = (0.58, 0.58, 0.58)
                    obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
                    obj_resultshape.ViewObject.Transparency = 85
                    FreeCAD.Console.PrintError('   执行完resultshape')
                    # obj[0].ViewObject.ShapeColor = (0.00, 1.00, 0.00)
                    objs[0].ViewObject.DisplayMode = u'Flat Lines'
                    objs[0].ViewObject.Transparency = 0
                    objs[0].ViewObject.Visibility = True
                    self.lastClick.append(objs[0])
                    self.lastClick.append(objs[0].ViewObject.ShapeColor)
                    # 判断这个选择的模型是不是属于被引用的，如果是被引用的，就显示原来的颜色，否则显示为绿色
                    FreeCAD.Console.PrintError(self.lastClick)
                    if not objs[0] in objsBeUsed:
                        objs[0].ViewObject.ShapeColor = (0.00, 1.00, 0.00)
                    FreeCAD.Console.PrintError('   执行完选中物体')
                    # FreeCAD.Console.PrintError(objs[0].ViewObject.ShapeColor)
                    
                except:
                    FreeCAD.Console.PrintError('\n执行单击效果失败')
        elif len(objs) > 1:
            for i in objs:
                if 'Type' in i.PropertiesList:
                    try:
                        # 将被引用的模型设置85的透明度
                        objsBeUsed=SetVisibilityOfModels.setVisibility(85)

                        obj_resultshape = FreeCAD.ActiveDocument.ResultShape
                        obj_resultshape.ViewObject.DisplayMode = u'Flat Lines'
                        # obj_resultshape.ViewObject.ShapeColor = (0.58, 0.58, 0.58)
                        obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
                        obj_resultshape.ViewObject.Transparency = 85
                        # i.ViewObject.ShapeColor = (0.00, 1.00, 0.00)
                        i.ViewObject.DisplayMode = u'Flat Lines'
                        i.ViewObject.Transparency = 0
                        i.ViewObject.Visibility = True
                        self.lastClick.append(i)
                        self.lastClick.append(i.ViewObject.ShapeColor)
                        # 判断这个选择的模型是不是属于被引用的，如果是被引用的，就显示原来的颜色，否则显示为绿色
                        if not i in objsBeUsed:
                            i.ViewObject.ShapeColor = (0.00, 1.00, 0.00)
                        
                        # FreeCAD.Console.PrintError('\n执行了向lastClick添加i的操作')
                    except:
                        FreeCAD.Console.PrintError('\n执行了向lastClick添加i的操作')
                        pass
    def changeClickObj(self):
        if self.lastClick is None:
            pass
        else:
            try:
            # if True:
                obj = FreeCADGui.Selection.getSelection()
                
                obj_resultshape = FreeCAD.ActiveDocument.ResultShape
                obj_resultshape.ViewObject.DisplayMode = u'Flat Lines'
                # obj_resultshape.ViewObject.ShapeColor = (0.58, 0.58, 0.58)
                obj_resultshape.ViewObject.LineColor = (0.33, 0.33, 0.33)
                obj_resultshape.ViewObject.Transparency = 0
                    # obj.ViewObject.Visibility = False
                # for i in self.lastClick:
                #     i.ViewObject.Visibility = False
                # FreeCAD.Console.PrintError('\n被选中的物体:'+str(obj))
                # FreeCAD.Console.PrintError('\n被选中的物体的长度:'+str(len(obj)))
                # FreeCAD.Console.PrintError(self.lastClick)
                for itemIndex in range(0,len(self.lastClick),2):
                    lastObj=self.lastClick[itemIndex]
                    shapeColorObj=self.lastClick[itemIndex+1]
                    lastObj.ViewObject.ShapeColor=shapeColorObj
                    lastObj.ViewObject.Visibility=False
                    ObjectsTools.checkVolShape(lastObj)
                SetVisibilityOfModels.setVisibility()
                self.lastClick = []

                # if len(obj) == 1:
                #     for i in self.lastClick:
                #         i.ViewObject.Visibility = False
                #         from Modeling.Common.Tools import ObjectsTools
                #         ObjectsTools.checkVolShape(i)
                #         # from Physics.PhysicsTools import SetVisibilityOfModels
                #         SetVisibilityOfModels.setVisibility()
                        
                #     self.lastClick = []
            except:
                self.lastClick = []
                pass


FreeCADGui.addCommand('SingleClickDisplayMode', SingleClickCommand())

