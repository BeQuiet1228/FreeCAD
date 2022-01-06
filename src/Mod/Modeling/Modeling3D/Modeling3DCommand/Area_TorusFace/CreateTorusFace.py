import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import TorusFaceInstance as Instance

def createTorusFace():
    obj = App.ActiveDocument.addObject("Part::FeaturePython", "TorusFace")
    TorusFace = Instance.TorusFace(obj)
    Instance.ViewProviderTorusFace(obj.ViewObject)
    App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj