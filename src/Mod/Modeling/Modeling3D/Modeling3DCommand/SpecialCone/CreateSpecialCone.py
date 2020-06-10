import FreeCADGui
import Modeling3DCommand
import FreeCAD as App
import Units
import SpecialConeInstance as Instance



def createSpecialCone():
    App.Console.PrintError("fubiao6 \n")
    obj = App.ActiveDocument.addObject("Part::FeaturePython", "SpecialCone")
    SpecialCone = Instance.SpecialCone(obj)
    Instance.ViewProviderSpecialCone(obj.ViewObject)
    App.ActiveDocument.recompute()
    FreeCADGui.SendMsgToActiveView("ViewFit")
    return obj