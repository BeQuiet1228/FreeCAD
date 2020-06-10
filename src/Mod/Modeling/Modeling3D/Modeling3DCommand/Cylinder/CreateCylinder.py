import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import CylinderInstance as Instance

def createCylinder():
    obj = App.ActiveDocument.addObject("Part::FeaturePython","Cylinder")
    Cylinder = Instance.Cylinder(obj)
    Instance.ViewProviderCylinder(obj.ViewObject)
    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj