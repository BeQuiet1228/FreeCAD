# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui as Gui
from Modeling.Common.Tools import ObjectsTools

#根据物理设置中设置引用的模型，为模型显示不同的颜色值
def setColor(objName,physicsType="other"):
    
    if objName==u"未指定":
        return 
    else:
        obj=None
        try:
            doc=FreeCAD.ActiveDocument
            objs=ObjectsTools.getListOfOrderedObjects(doc.Name)
            for objItem in objs:
                if ObjectsTools.getRealNameBySplitObjectLabel(objItem)==str(objName):
                    Gui.ActiveDocument.getObject(objItem.Name).Visibility=True
                    obj=objItem
                    break
        except:
            FreeCAD.Console.PrintError("findObjByLabelWithoutOrderAndVisible Wrong!\n")
        if hasattr(obj,"Attribute") and obj.Attribute != ObjectsTools.Attribute.NotDefine:
            return
        else:
            FreeCAD.Console.PrintError(physicsType+"\n")
            if physicsType=="other":
                return
            else:
                if physicsType=="Foil":
                    #黄色
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.772549,0.717647,0.137255,0.0)
                    pass
                elif physicsType=="Ind":
                    #RGB 0,8,0
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.074510,0.803922,0.309804,0.0)
                    pass
                elif physicsType=="Port":
                    #RGB 63 72 201
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.247059,0.282353,0.788235,0.0)
                    pass
                elif physicsType=="Free":
                    #RGB 39,129,181
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.152941,0.505882,0.709804,0.0)
                    pass
                elif physicsType=="Syn":
                    # 69,69,0
                    Gui.ActiveDocument.getObject(obj.Name).ShapeColor=(0.2705882489681244, 0.2705882489681244, 0.0, 0.0)
                    pass


