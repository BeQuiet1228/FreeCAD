import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import SphereInstance as Instance



def createSphere():
    App.Console.PrintError("fubiao6 \n")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", "Sphere")
    Sphere = Instance.Sphere(obj)
    Instance.ViewProviderSphere(obj.ViewObject)

    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj