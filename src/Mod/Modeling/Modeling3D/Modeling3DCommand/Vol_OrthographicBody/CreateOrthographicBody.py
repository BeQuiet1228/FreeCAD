import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import OrthographicBodyInstance as Instance

def createOrthographicBody():
    obj = App.ActiveDocument.addObject("Part::FeaturePython","OrthographicBody")
    OrthographicBody = Instance.OrthographicBody(obj)
    Instance.ViewProviderOrthographicBody(obj.ViewObject)
    App.ActiveDocument.recompute()
    # FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj