import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import ConeInstance as Instance

def createCone():
    obj = App.ActiveDocument.addObject("Part::FeaturePython","Cone")
    Cone = Instance.Cone(obj)
    Instance.ViewProviderCone(obj.ViewObject)
    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj