import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import HollowedCylinderInstance as Instance



def createHollowedCylinder():
    App.Console.PrintError("fubiao6 \n")
    """Create a new HollowedCylinder instance

    Position arguments:
    solids -- List of solid shapes
    ship -- Ship owner

    Returned value:
    The new HollowedCylinder object
    """
    obj = App.ActiveDocument.addObject("Part::FeaturePython", "HollowedCylinder")
    HollowedCylinder = Instance.HollowedCylinder(obj)
    Instance.ViewProviderHollowedCylinder(obj.ViewObject)
    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj
