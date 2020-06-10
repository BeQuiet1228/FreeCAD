import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import ParallelogramInstance as Instance

def createParallelogram():
    obj = App.ActiveDocument.addObject("Part::FeaturePython","Parallelogram")
    Parallelogram = Instance.Parallelogram(obj)
    Instance.ViewProviderParallelogram(obj.ViewObject)
    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj