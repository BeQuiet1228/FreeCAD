# encoding:utf-8
import FreeCAD
import FreeCADGui

from File.FileCommand.M2dFile import M2dPhysics, M2dEmission, M2dObject, M2dProject
from Modeling.Modeling2D.Tools import Tools2D, FileView
blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","

def setM2DToInterface():
    m2d = M2D()
    m2d_text = m2d.getM2DText()
    FileView.FileView().updateText(m2d_text)
    return m2d_text


class CreateM2DCommand:
    """
    注册Foil命令
    """

    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        # 如果当前窗口没有m2d对应的窗口，则创建一个新的窗口
        fileView = FileView.FileView()
        if fileView.getThisSubWindow() is None:
            fileView.showThisSubWindow()
        m2d = M2D()
        m2d_text = m2d.getM2DText()
        FileView.FileView().updateText(m2d_text)
        pass

    def GetResources(self):

        return {'Accel': "M2D",
                'MenuText': "M2D",
                'ToolTip': "生成M2D文本", }


FreeCADGui.addCommand('CreateM2D', CreateM2DCommand())


class M2D:
    """
    生成完整的M2D文本
    """

    def __init__(self):
        self.PropertiesAndProcessesStr = []
        # self.getPropertiesAndProcessesStr()
        self.getM2DText()
        # SYSTEM
        # HEADER
        # PARAMETER
        # DEFINE OBJECTS
        # PANEL OBJECTS
        # GENERATE GRID/MESH
        # COMMON PRESETS
        # PROPERTIES AND PROCESSES
        # SIMULATION SETTINGS
        # ALL PLOTS
        # DUMP OPTIONS
        # RUN OPTIONS
        # RUN

        self.system_str = ""
        self.header_str = ""
        self.parameter_str = ""
        self.defineObjects_str = ""
        self.panelObjects_str = ""
        self.fromObserveToPanelStr = ""
        self.generate_str = ""
        self.grid_str = ""
        self.common_str = ""
        self.property_str = ""
        self.properties_str = ""
        self.simulation_str = ""
        self.defTimerStr = ""
        self.plots_str = ""
        self.dump_str = ""
        self.runOptions_str = ""
        self.run_str = ""

    def getM2DText(self):
        m2d_text = ""
        self.system_str = self.getSystemStr()
        self.header_str = self.getHeaderStr()
        self.parameter_str, self.grid_str = self.getParameterStr()
        self.defineObjects_str = self.getModelStr()
        self.generate_str = self.getGenerateGridStr()
        self.common_str = self.getCommonPresetsStr()
        self.property_str = self.getAreaAttribute()
        self.goldMaterial, self.panelObjects_str, self.properties_str = self.getPropertiesAndProcessesStr()
        self.simulation_str = self.getSimulationSettingStr()
        self.defTimerStr, self.fromObserveToPanelStr, self.plots_str = self.getAllPlotsStr()
        self.dump_str = self.getDumpOptionsStr()
        self.runOptions_str = self.getRunOptionsStr()
        self.run_str = self.getRunStr()
        # SYSTEM
        m2d_text += getNewBlock("SYSTEM")
        m2d_text += self.system_str
        # HEADER
        m2d_text += getNewBlock("HEADER")
        m2d_text += self.header_str
        # PARAMETER
        m2d_text += getNewBlock("PARAMETER")
        m2d_text += self.parameter_str
        # DEFINE OBJECTS
        m2d_text += getNewBlock("DEFINE OBJECTS")
        m2d_text += self.defineObjects_str
        # PANEL OBJECTS
        m2d_text += getNewBlock("PANEL OBJECTS")
        m2d_text += self.panelObjects_str
        m2d_text += self.fromObserveToPanelStr
        # GENERATE GRID/MESH
        m2d_text += getNewBlock("GENERATE GRID/MESH")
        m2d_text += self.grid_str
        m2d_text += self.generate_str
        # COMMON PRESETS
        m2d_text += getNewBlock("COMMON PRESETS")
        m2d_text += self.goldMaterial
        m2d_text += self.common_str
        # PROPERTIES AND PROCESSES
        m2d_text += getNewBlock("PROPERTIES AND PROCESSES")
        # property_str 表示点线面的属性生成的m2d
        m2d_text += self.property_str
        m2d_text += self.properties_str
        # SIMULATION SETTINGS
        m2d_text += getNewBlock("SIMULATION SETTINGS")
        m2d_text += self.simulation_str
        # ALL PLOTS
        m2d_text += getNewBlock("ALL PLOTS")
        m2d_text += self.defTimerStr
        m2d_text += self.plots_str
        # DUMP OPTIONS
        m2d_text += getNewBlock("DUMP OPTIONS")
        m2d_text += self.dump_str
        # RUN OPTIONS
        m2d_text += getNewBlock("RUN OPTIONS")
        m2d_text += self.runOptions_str
        # RUN
        m2d_text += getNewBlock("RUN")
        m2d_text += self.run_str

        # Tools2D.sayz(m2d_text)
        return m2d_text

    def getSystemStr(self):
        curSystem = "SYSTEM "
        # 暂时写成柱坐标
        if FreeCAD.ActiveDocument.CoordinateSystem == u'Rectangular' or \
                FreeCAD.ActiveDocument.CoordinateSystem == 'Rectangular':
            curSystem += "CARTESIAN"
        else:
            # 如果二维建模出现新的坐标系，将坐标系命令写在这里
            curSystem += "CYLINDRICAL"
        curSystem += ";\n\n"
        return curSystem

    def getHeaderStr(self):
        res_header_str = ""
        res_header_str += "HEADER" + blankSpace + "ORGANIZATION" + blankSpace + "NONE" + semicolon + newLine + \
                      "HEADER" + blankSpace + "AUTHOR" + blankSpace + "NONE" + semicolon + newLine + \
                      "HEADER" + blankSpace + "DEVICE" + blankSpace + "NONE" + semicolon + newLine + \
                      "HEADER" + blankSpace + "REMARKS" + blankSpace + "NONE" + semicolon + newLine + newLine
        header_dict = Tools2D.getHeaderDict()
        for i in header_dict[Tools2D.ObjectType.Info]:
            res_header_str = M2dProject.ModelInfo(i)
            if len(res_header_str) != 0:
                res_header_str += "\n"
        return res_header_str

    def getParameterStr(self):
        res_grid_str = ""
        gg_str = ""
        res_net_str = ""
        coodinate = FreeCAD.ActiveDocument.CoordinateSystem
        if coodinate == u'Rectangular':
            res_net_str += "DX1" + " = " + "1mm" + ";" + "\n\n"
            res_net_str += "DX2" + " = " + "1mm" + ";" + "\n\n"
        elif coodinate == u'Polar':
            res_net_str += "DX1" + " = " + "1mm" + ";" + "\n\n"
            res_net_str += "DX2" + " = " + "18deg" + ";" + "\n\n"
        elif coodinate == u'Cylindrical':
            res_net_str += "DX1" + " = " + "1mm" + ";" + "\n\n"
            res_net_str += "DX2" + " = " + "1mm" + ";" + "\n\n"

        res_grid_str += M2dProject.getParameterM2D()
        if len(res_grid_str) != 0:
            res_grid_str += "\n"
        grid_dict = Tools2D.getGridDict()
        for i in grid_dict[Tools2D.ObjectType.Simu]:
            res_net_str, gg_str = M2dProject.NetStep(i)
            if len(res_net_str) != 0:
                res_net_str += "\n"
            res_grid_str += res_net_str
        # res_grid_str += M2dProject.getParameterM2D()
        return res_grid_str, gg_str

    def getModelStr(self):
        obj_dict = Tools2D.getAllModelObjDict()
        self.getAllModelObjStr = []
        self.objToOtherStr = []     # 点线面有两个返回值，属性相关的m2d放到pap容器中

        for i in obj_dict[Tools2D.ObjectType.Point]:
            model_str, pap_str = M2dObject.Point(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[Tools2D.ObjectType.Line]:
            model_str, pap_str = M2dObject.Line(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[Tools2D.ObjectType.LineConformal]:
            model_str, pap_str = M2dObject.LineConformal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[Tools2D.ObjectType.AreaPolygonal]:
            model_str, pap_str = M2dObject.AreaPolygonal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[Tools2D.ObjectType.AreaConformal]:
            model_str, pap_str = M2dObject.AreaComformal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        # for i in obj_dict[Tools2D.ObjectType.AreaCircular]:
        #     model_str, pap_str = M2dObject.Circle(i)
        #     self.getAllModelObjStr.append(model_str)
        #     self.objToOtherStr.append(pap_str)

        for i in obj_dict[Tools2D.ObjectType.Rectangle]:
            model_str, pap_str = M2dObject.Rectangle(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[Tools2D.ObjectType.Sector]:
            model_str, pap_str = M2dObject.Sector(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[Tools2D.ObjectType.Fillet]:
            model_str, pap_str = M2dObject.Fillet(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        res_obj_str = ""
        for i in self.getAllModelObjStr:
            if len(i) == 0:
                continue
            res_obj_str += i + "\n"

        # res_pap_str = ""
        # for i in self.objToOtherStr:
        #     if len(i) == 0:
        #         continue
        #     res_pap_str += i + "\n"

        return res_obj_str

    def getGenerateGridStr(self):
        generateGrid_str = "AUTOGRID" + ";" + "\n\n"
        return generateGrid_str

    def getCommonPresetsStr(self):
        cp_dict = Tools2D.getCommonPresets()
        self.cp_str = []
        for i in cp_dict[Tools2D.ObjectType.NewParticle]:
            commonPresets_str = M2dProject.NewParticle(i)
            self.cp_str.append(commonPresets_str)

        for i in cp_dict[Tools2D.ObjectType.NewMaterial]:
            commonPresets_str = M2dProject.NewMaterial(i)
            self.cp_str.append(commonPresets_str)

        for i in cp_dict[Tools2D.ObjectType.FieldSetting]:
            commonPresets_str = M2dProject.Filed(i)
            self.cp_str.append(commonPresets_str)

        res_cp_str = ""
        for i in self.cp_str:
            if len(i) == 0:
                continue
            res_cp_str += i + "\n"
        return res_cp_str

    def getSimulationSettingStr(self):
        res_cp_str = ""
        res_cp_str += "MAXWELL BIASED;" + "\n"
        res_cp_str += "DURATION 20NANOSECOND;" + "\n\n"
        ss_dict = Tools2D.getSimulationSetting()
        for i in ss_dict[Tools2D.ObjectType.TimeDomain]:
            res_cp_str = M2dProject.TimeDomain(i)
            if len(res_cp_str) != 0:
                res_cp_str += "\n"
        return res_cp_str

    def getAllPlotsStr(self):
        ap_dict = Tools2D.getAllPlotsDict()
        self.getObjectsStr = []
        self.getObseverStr = []
        timer_str = ""
        timer_str += "TIMER DefTimer PERIODIC INTEGER 10 100000 5000;" + "\n\n"
        for i in ap_dict[Tools2D.ObjectType.DefaultTimer]:
            timer_str = M2dProject.Timer(i)
            if len(timer_str) != 0:
                timer_str += "\n"

        for i in ap_dict[Tools2D.ObjectType.Timer]:
            ap_str = M2dProject.Timer(i)
            self.getObseverStr.append(ap_str)

        for i in ap_dict[Tools2D.ObjectType.CNTR]:
            model_str, ap_str = M2dProject.Cntr(i)
            self.getObjectsStr.append(model_str)
            self.getObseverStr.append(ap_str)

        for i in ap_dict[Tools2D.ObjectType.Vector]:
            model_str, ap_str = M2dProject.Vector(i)
            self.getObjectsStr.append(model_str)
            self.getObseverStr.append(ap_str)

        for i in ap_dict[Tools2D.ObjectType.PhasSpace]:
            ap_str = M2dProject.PhasSpace(i)
            self.getObseverStr.append(ap_str)

        for i in ap_dict[Tools2D.ObjectType.AreaRan]:
            model_str, ap_str = M2dProject.AreaRan(i)
            self.getObjectsStr.append(model_str)
            self.getObseverStr.append(ap_str)

        for i in ap_dict[Tools2D.ObjectType.Observe]:
            model_str, ap_str = M2dProject.Observe(i)
            self.getObjectsStr.append(model_str)
            self.getObseverStr.append(ap_str)
        res_obj_str = ""
        for i in self.getObjectsStr:
            if len(i) == 0:
                continue
            res_obj_str += i + "\n"

        res_ap_str = ""
        for i in self.getObseverStr:
            if len(i) == 0:
                continue
            res_ap_str += i + "\n"
        # 第一个返回值是为了m2d生成默认定时器
        return timer_str, res_obj_str, res_ap_str

    def getDumpOptionsStr(self):
        do_str = ""
        do_str += "DUMP NAME Unnamed_TIME;" + "\n"
        do_str += "DUMP FORMAT ASCII;" + "\n\n"
        do_dict = Tools2D.getDumpOptions()
        for i in do_dict[Tools2D.ObjectType.DataProcess]:
            do_str = M2dProject.DataExport(i)
            if len(do_str) != 0:
                do_str += "\n"
        return do_str

    def getRunOptionsStr(self):
        ro_str = ""
        ro_str += "DISPLAY ;"+"\n\n"
        ro_dict = Tools2D.getRunOptions()
        for i in ro_dict[Tools2D.ObjectType.RunOptions]:
            ro_str = M2dProject.RunProcessing(i)
            if len(ro_str) != 0:
                ro_str += "\n"
        return ro_str

    def getRunStr(self):
        run_str = "START;" + "\n" + "STOP;" + "\n\n"
        return run_str

    def getPropertiesAndProcessesStr(self):
        """
        生成所有与Properties And Processes相关的M2D
        """
        pp_dict = Tools2D.getAllPropertiesAndProcessesObj()
        # 每次生成前清空一下原有数据
        self.PropertiesAndProcessesStr = []
        self.PanelStr = []      #生成与点线面有关的m2d
        self.GoldMaterial = []  # 生成金属材料的Foil的命令
        # SOLE
        for i in pp_dict[Tools2D.ObjectType.SOLE]:
            # model_str, sole_str =
            # self.PropertiesAndProcessesStr.append()
            pass
        # DRIV
        for i in pp_dict[Tools2D.ObjectType.DRIV]:
            model_str, driv_str = M2dPhysics.Driv(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(driv_str)

        # FOIL
        for i in pp_dict[Tools2D.ObjectType.FOIL]:
            material_str, model_str, foil_str = M2dPhysics.Foil(i)
            self.GoldMaterial.append(material_str)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(foil_str)

        # IND
        for i in pp_dict[Tools2D.ObjectType.IND]:
            model_str, ind_str = M2dPhysics.Inductor(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(ind_str)

        # PORT
        for i in pp_dict[Tools2D.ObjectType.PORT]:
            model_str, prot_str = M2dPhysics.Port(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(prot_str)

        # FREE
        for i in pp_dict[Tools2D.ObjectType.FREE]:
            model_str, free_str = M2dPhysics.FreeSpace(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(free_str)

        # SYMT
        for i in pp_dict[Tools2D.ObjectType.SYMT]:
            model_str, symt_str = M2dPhysics.Symmry(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(symt_str)

        # 发射处理 -------------------------分隔线---------------------------
        # BEAM
        for i in pp_dict[Tools2D.ObjectType.BEAM]:
            beam_str = M2dEmission.Beam(i)
            self.PropertiesAndProcessesStr.append(beam_str)

        # EXPS
        for i in pp_dict[Tools2D.ObjectType.EXPS]:
            exps_str = M2dEmission.Exps(i)
            self.PropertiesAndProcessesStr.append(exps_str)

        # GYRO
        for i in pp_dict[Tools2D.ObjectType.GYRO]:
            gyro_str = M2dEmission.Gyro(i)
            self.PropertiesAndProcessesStr.append(gyro_str)

        # POPU
        for i in pp_dict[Tools2D.ObjectType.POPU]:
            popu_str = M2dEmission.Popu(i)
            self.PropertiesAndProcessesStr.append(popu_str)

        # FELD
        for i in pp_dict[Tools2D.ObjectType.FELD]:
            feld_str = M2dEmission.Feld(i)
            self.PropertiesAndProcessesStr.append(feld_str)

        # THER
        for i in pp_dict[Tools2D.ObjectType.THER]:
            ther_str = M2dEmission.Ther(i)
            self.PropertiesAndProcessesStr.append(ther_str)

        # SECD
        for i in pp_dict[Tools2D.ObjectType.SECD]:
            secd_str = M2dEmission.Secd(i)
            self.PropertiesAndProcessesStr.append(secd_str)

        # IONI
        for i in pp_dict[Tools2D.ObjectType.IONI]:
            ioni_str = M2dEmission.Ioni(i)
            self.PropertiesAndProcessesStr.append(ioni_str)

        # MarcoParticle
        for i in pp_dict[Tools2D.ObjectType.MarcoParticle]:
            marcoParticle_str = M2dProject.MacParticle(i)
            self.PropertiesAndProcessesStr.append(marcoParticle_str)

        res_material_str = ""
        for i in self.GoldMaterial:
            if len(i) == 0:
                continue
            res_material_str = i

        res_panel_str = ""
        for i in self.PanelStr:
            if len(i) == 0:
                continue
            res_panel_str += i + "\n"
        # Tools2D.sayz(res_panel_str)

        res_pap_str = ""
        for i in self.PropertiesAndProcessesStr:
            if len(i) == 0:
                continue
            res_pap_str += i + "\n"
        # Tools2D.sayz(res_pap_str)

        return res_material_str, res_panel_str, res_pap_str

    # 获取根据面的顺序，来排列相应的属性
    def getAreaAttribute(self):
        AreaOrderList = []
        AreaOrderListStr = ""
        model_str = ""
        pap_str = ""
        AreaList = Tools2D.getAllValidModelObj()
        for i in AreaList:
            if i.Type == Tools2D.ObjectType.AreaConformal:
                model_str, pap_str = M2dObject.AreaComformal(i)
            elif i.Type == Tools2D.ObjectType.AreaPolygonal:
                model_str, pap_str = M2dObject.AreaPolygonal(i)
            elif i.Type == Tools2D.ObjectType.Rectangle:
                model_str, pap_str = M2dObject.Rectangle(i)
            elif i.Type == Tools2D.ObjectType.Sector:
                model_str, pap_str = M2dObject.Sector(i)
            elif i.Type == Tools2D.ObjectType.Fillet:
                model_str, pap_str = M2dObject.Fillet(i)
            AreaOrderList.append(pap_str)
        for i in AreaOrderList:
            if len(i) == 0:
                continue
            AreaOrderListStr += i + "\n"
        return AreaOrderListStr


def getNewBlock(name):
    temp_str = "! ==============================================================================!"
    temp_str += "\n! " + name + "\n\n"
    return temp_str
