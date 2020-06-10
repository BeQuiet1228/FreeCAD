import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import PyramidInstance as Instance

def createPyramid():
    obj = App.ActiveDocument.addObject("Part::FeaturePython","Pyramid")
    Pyramid = Instance.Pyramid(obj)
    Instance.ViewProviderPyramid(obj.ViewObject)
    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj