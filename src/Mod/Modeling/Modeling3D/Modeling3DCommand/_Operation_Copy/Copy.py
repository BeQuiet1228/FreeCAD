# encoding:utf-8
import FreeCAD as App
import FreeCADGui as Gui
import CopyCommand


def doCopy():
    objs=Gui.Selection.getCompleteSelection()
    for objItem in objs:
        if not hasattr(objItem,"Order"):
            objs.remove(objItem)
    CopyCommand.objs=objs
    # CopyCommand.CopyObjs.setObjs(objs)
    

def doPaste(objs):
    App.Console.PrintMessage("len(objs)"+str(len(objs))+" "+str(objs)+"\n")
    if len(objs)<1:
        return
    minOrder=-1
    #copy
    if objs[0]==1:
        objs=objs[1:]
        for objItem in objs:
            o=App.ActiveDocument.copyObject(objItem)
            if hasattr(o,"Order"):
                if getattr(o,"Order")<minOrder or minOrder<0:
                    minOrder=getattr(o,"Order")
    else:
        objs=objs[1:]
        for objItem in objs:
            o=App.ActiveDocument.copyObject(objItem)
            if hasattr(o,"Order"):
                if getattr(o,"Order")<minOrder or minOrder<0:
                    minOrder=getattr(o,"Order")
            o=App.ActiveDocument.removeObject(objItem.Name)
            if hasattr(o,"Order"):
                if getattr(o,"Order")<minOrder or minOrder<0:
                    minOrder=getattr(o,"Order")
        # 不允许剪切后多次粘贴
        CopyCommand.objs = None
    App.ActiveDocument.recompute()
    import PartGui,PartChipic
    #PartGui.updateBoolean(minOrder) #ZD
    PartChipic.updateBoolean(minOrder, 0) #这儿minOrder是最大的

def doCut(objs):
    # objs=Gui.Selection.getSelection()
    for objItem in objs:
        App.ActiveDocument.copyObject(objItem)
        App.ActiveDocument.removeObject(objItem.Name)