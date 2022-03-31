# -*- coding: UTF-8 -*-

import FreeCAD
import FreeCADGui

from PySide import QtGui

IconCommonPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/VisualizationResources/"

def QT_TRANSLATE_NOOP(ctx,txt): return txt # dummy function for the QT translator
from DraftTools import translate

