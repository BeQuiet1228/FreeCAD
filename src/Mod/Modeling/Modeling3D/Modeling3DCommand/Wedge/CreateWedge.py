import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import WedgeInstance as Instance

def createWedge():
    App.Console.PrintError("fubiao6 \n")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", "Wedge")
    Wedge = Instance.Wedge(obj)
    Instance.ViewProviderWedge(obj.ViewObject)
    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj