import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import TorusInstance as Instance

def createTorus():
    obj = App.ActiveDocument.addObject("Part::FeaturePython", "Torus")
    Torus = Instance.Torus(obj)
    Instance.ViewProviderTorus(obj.ViewObject)
    App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj