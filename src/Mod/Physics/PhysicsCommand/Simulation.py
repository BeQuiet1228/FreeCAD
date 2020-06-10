import FreeCAD
import FreeCADGui
import PhysicsGui
import time,thread,random
from PySide import QtGui, QtCore
from PySide.QtGui import QApplication

class Port:
    def Activated(self):
        # FreeCAD.Console.PrintMessage("Setting Waveguide Port\n")
        # reply = QtGui.QMessageBox.information(None, "", "Waveguide Port")
        PhysicsGui.PortDlgMain.show()
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Port"
        ToolTip = "Waveguide Port"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Free:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Absorption Space\n")
        reply = QtGui.QMessageBox.information(None, "", "Absorption Space")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Free"
        ToolTip = "Absorption Space"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Sym:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Symmetric Boundary\n")
        reply = QtGui.QMessageBox.information(None, "", "Symmetric Boundary")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Sym"
        ToolTip = "Symmetric Boundary"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EmB:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Beam Emission\n")
        reply = QtGui.QMessageBox.information(None, "", "Beam Emission")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "EmB"
        ToolTip = "Beam Emission"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EmE:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Explosive Emission\n")
        reply = QtGui.QMessageBox.information(None, "", "Explosive Emission")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "EmE"
        ToolTip = "Explosive Emission"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EmG:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Cyclotron Emission\n")
        reply = QtGui.QMessageBox.information(None, "", "Cyclotron Emission")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "EmG"
        ToolTip = "Cyclotron Emission"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EmH:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting High Field Emission\n")
        reply = QtGui.QMessageBox.information(None, "", "High Field Emission")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "EmH"
        ToolTip = "High Field Emission"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class EmT:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Thermal Emission\n")
        reply = QtGui.QMessageBox.information(None, "", "Thermal Emission")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "EmT"
        ToolTip = "Thermal Emission"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Sol:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Solenoid\n")
        reply = QtGui.QMessageBox.information(None, "", "Solenoid")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Sol"
        ToolTip = "Solenoid"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class ExcitationPower:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Excitation Power\n")
        reply = QtGui.QMessageBox.information(None, "", "Excitation Power")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "ExP"
        ToolTip = "Excitation Power"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Foil:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Foil\n")
        reply = QtGui.QMessageBox.information(None, "", "Foil")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Foil"
        ToolTip = "Foil"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Ind:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Setting Inductance\n")
        reply = QtGui.QMessageBox.information(None, "", "Inductance")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Ind"
        ToolTip = "Inductance"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class CnTr:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Observing Coordinatograph\n")
        reply = QtGui.QMessageBox.information(None, "", "Coordinatograph")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "CnTr"
        ToolTip = "Coordinatograph"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Vec:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Observing Vectorgraph\n")
        reply = QtGui.QMessageBox.information(None, "", "Vectorgraph")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Vec"
        ToolTip = "Vectorgraph"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Pha:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Observing particle phase space\n")
        reply = QtGui.QMessageBox.information(None, "", "Particle Phase Space")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Pha"
        ToolTip = "Observing particle phase space"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Ran:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Observing space\n")
        reply = QtGui.QMessageBox.information(None, "", "Observing space")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Ran"
        ToolTip = "Observing space"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Obs:
    def Activated(self):
        FreeCAD.Console.PrintMessage("Observing time\n")
        reply = QtGui.QMessageBox.information(None, "", "Observing time")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/"
        MenuText = "Obs"
        ToolTip = "Observing time"
        return {'Pixmap': '',
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class TimerDef:
    def Activated(self):
        PhysicsGui.DefaultTimerDlgMain.show()
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/default-timer.svg"
        MenuText = "Default Timer"
        ToolTip = "Default timer"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Timer:
    def Activated(self):
        PhysicsGui.TimerDlgMain.show()
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/timer.svg"
        MenuText = "Timer"
        ToolTip = "Timer"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Run:
    def Activated(self):
        taskControl = PhysicsGui.TaskControlPal.Ui_DockWidget_TaskControl()
        app = QtGui.qApp
        FCmw = app.activeWindow()
        TaskControlWidget = QtGui.QDockWidget()
        TaskControlWidget.ui = taskControl
        TaskControlWidget.ui.setupUi(TaskControlWidget)
        FCmw.addDockWidget(QtCore.Qt.LeftDockWidgetArea, TaskControlWidget)
        # call clientRun method, start simulation
        print("start simulation ...")
        FreeCAD.clientRun("D:\jdk.exe")
        print("file send success !")
        # new a thread to set tsskInfo
        try:
            start = time.time()
            thread.start_new_thread(self.setTaskInfo, (65536, taskControl, start))
        except:
            print "Error: unable to start thread"
        # draw plot
        import visualizationCommand.VisualizationPlot as VisualizationPlot
        VisualizationPlot.plot()

    def setTaskInfo(self, total, taskControl, start):
        count = 0
        particle = 230
        while count < total:
            time.sleep(1)
            count += 256
            particle += random.randint(0, 500)
            if count % 1024 == 0:
                # set iterationResult content
                times = str(count) + "/" + str(total)
                taskControl.iterationResult.setText(times)
                # set iterationTimeResult content
                perTime = 120 / 65536.0
                curTime = perTime * count
                taskControl.iterationTimeResult.setText(str(curTime))
                # set consumingTimeResult content
                end = time.time()
                end = int(end - start)
                hour = end / 3600
                min = end % 3600 / 60
                sec = end % 60
                consumingTime = str(hour) + "; " + str(min) + ": " + str(sec)
                consumingTime = consumingTime + "/ 4:20:28"
                taskControl.consumingTimeResult.setText(consumingTime)
                # set particelNumberResult content
                taskControl.particelNumberResult.setText(str(particle))
                # set runningStateResult content
                taskControl.runningStateResult.setText("thread 1 is computing !")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/run.svg"
        MenuText = "Run"
        ToolTip = "Run"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class AllRun:
    def Activated(self):
        from PySide import QtGui, QtCore
        FreeCAD.Console.PrintMessage("Collateral Run\n")
        reply = QtGui.QMessageBox.information(None, "", "Collateral Run")
    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Physics/PhysicsResources/all-run.svg"
        MenuText = " Collateral Run"
        ToolTip = "Collateral Run"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class PostProcessingWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("VisualWorkbench")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Visualization/visualizationResources/VisualWorkbench.svg"
        MenuText = "Post Processing"
        ToolTip = "To Post Processing Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Modeling3DWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("Modeling3DWorkbench")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling3D/modeling3DResources/3DModelingWorkbench.svg"
        MenuText = "3D Modeling"
        ToolTip = "To 3D Modeling Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

class Modeling2DWorkbench:
    def Activated(self):
        FreeCADGui.activateWorkbench("Modeling2DWorkbench")

    def GetResources(self):
        IconPath = FreeCAD.ConfigGet("AppHomePath") + "Mod/Modeling/Modeling2D/modeling2DResources/2DModelingWorkbench.svg"
        MenuText = "2D Modeling"
        ToolTip = "To 2D Modeling Part"
        return {'Pixmap': IconPath,
                'MenuText': MenuText,
                'ToolTip': ToolTip}

FreeCADGui.addCommand('Port', Port())
FreeCADGui.addCommand('Free', Free())
FreeCADGui.addCommand('Sym', Sym())
FreeCADGui.addCommand('EmB', EmB())
FreeCADGui.addCommand('EmE', EmE())
FreeCADGui.addCommand('EmG', EmG())
FreeCADGui.addCommand('EmH', EmH())
FreeCADGui.addCommand('EmT', EmT())
FreeCADGui.addCommand('Sol', Sol())
FreeCADGui.addCommand('Excitation power', ExcitationPower())
FreeCADGui.addCommand('Foil', Foil())
FreeCADGui.addCommand('Ind', Ind())
FreeCADGui.addCommand('CnTr', CnTr())
FreeCADGui.addCommand('Vec', Vec())
FreeCADGui.addCommand('Pha', Pha())
FreeCADGui.addCommand('Ran', Ran())
FreeCADGui.addCommand('Obs', Obs())
FreeCADGui.addCommand('TimerDef', TimerDef())
FreeCADGui.addCommand('Timer', Timer())
FreeCADGui.addCommand('Run', Run())
FreeCADGui.addCommand('AllRun', AllRun())
FreeCADGui.addCommand('Modeling 2D', Modeling2DWorkbench())
FreeCADGui.addCommand('Modeling 3D', Modeling3DWorkbench())
FreeCADGui.addCommand('Post Processing', PostProcessingWorkbench())
