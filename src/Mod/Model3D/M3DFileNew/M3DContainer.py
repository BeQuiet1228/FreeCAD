# encoding:utf-8
import FreeCAD
import FreeCADGui
from Model3D.Tools import FileView3D, M3DTools, ObjectTools
from Model3D.M3DFileNew import M3DObject, M3DEmission, M3DObserve, M3DProject, M3DPhysices

blankSpace = " "
semicolon = ";"
newLine = "\n"
tab = "\t"
comma = ","


class CreateM3DCommand:
    """
    注册M3D命令
    """
    def IsActive(self):
        if FreeCADGui.ActiveDocument:
            return True
        else:
            return False

    def Activated(self):
        # 如果当前窗口没有m3d对应的窗口，则创建一个新的窗口
        m3d = M3D()
        m3d_text = m3d.getM3DText()
        FreeCADGui.displayText(m3d_text)
        pass

    def GetResources(self):
        return {'Accel': "M3D",
                'MenuText': "M3D",
                'ToolTip': "生成M3D文本", }


FreeCADGui.addCommand('CreateM3D_new', CreateM3DCommand())


def setM3DToInterface():
    m3d = M3D()
    m3d_text = m3d.getM3DText()
    FreeCADGui.displayText(m3d_text)
    return m3d_text


class M3D:
    """
    生成完整的M3D文本
    SYSTEM
    HEADER
    PARAMETER
    DEFINE OBJECTS
    PANEL OBJECTS
    GENERATE GRID/MESH
    COMMON PRESETS
    PROPERTIES AND PROCESSES
    SIMULATION SETTINGS
    ALL PLOTS
    DUMP OPTIONS
    RUN OPTIONS
    RUN
    """
    def __init__(self):
        self.getM3DText()
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

    def getM3DText(self):
        m3d_text = ""
        self.system_str = self.getSystemStr()
        self.header_str = self.getHeaderStr()
        self.parameter_str, self.grid_str = self.getParameterStr()
        self.defineObjects_str = self.getModelStr()
        self.generate_str = self.getGenerateGridStr()
        self.common_str = self.getCommonPresetsStr()
        self.property_str = self.getVolAttribute()
        self.goldMaterial, self.panelObjects_str, self.properties_str = self.getPropertiesAndProcessesStr()
        self.simulation_str = self.getSimulationSettingStr()
        self.defTimerStr, self.fromObserveToPanelStr, self.plots_str = self.getAllPlotsStr()
        self.dump_str = self.getDumpOptionsStr()
        self.runOptions_str = self.getRunOptionsStr()
        self.run_str = self.getRunStr()
        # SYSTEM
        m3d_text += getNewBlock("SYSTEM")
        m3d_text += self.system_str
        # HEADER
        m3d_text += getNewBlock("HEADER")
        m3d_text += self.header_str
        # PARAMETER
        m3d_text += getNewBlock("PARAMETER")
        m3d_text += self.parameter_str
        # DEFINE OBJECTS
        m3d_text += getNewBlock("DEFINE OBJECTS")
        m3d_text += self.defineObjects_str
        # PANEL OBJECTS
        m3d_text += getNewBlock("PANEL OBJECTS")
        m3d_text += self.panelObjects_str
        m3d_text += self.fromObserveToPanelStr
        # GENERATE GRID/MESH
        m3d_text += getNewBlock("GENERATE GRID/MESH")
        m3d_text += self.grid_str
        m3d_text += self.generate_str
        # COMMON PRESETS
        m3d_text += getNewBlock("COMMON PRESETS")
        m3d_text += self.goldMaterial
        m3d_text += self.common_str
        # PROPERTIES AND PROCESSES
        m3d_text += getNewBlock("PROPERTIES AND PROCESSES")
        # property_str 表示点线面的属性生成的m2d
        m3d_text += self.property_str
        m3d_text += self.properties_str
        # SIMULATION SETTINGS
        m3d_text += getNewBlock("SIMULATION SETTINGS")
        m3d_text += self.simulation_str
        # ALL PLOTS
        m3d_text += getNewBlock("ALL PLOTS")
        m3d_text += self.defTimerStr
        m3d_text += self.plots_str
        # DUMP OPTIONS
        m3d_text += getNewBlock("DUMP OPTIONS")
        m3d_text += self.dump_str
        # RUN OPTIONS
        m3d_text += getNewBlock("RUN OPTIONS")
        m3d_text += self.runOptions_str
        # RUN
        m3d_text += getNewBlock("RUN")
        m3d_text += self.run_str

        return m3d_text

    def getSystemStr(self):
        curSystem = "SYSTEM "
        if FreeCAD.ActiveDocument.CoordinateSystem == u'Rectangular':
            curSystem += "CARTESIAN"
        elif FreeCAD.ActiveDocument.CoordinateSystem == u'Cylindrical':
            curSystem += "CYLINDRICAL"
        else:
            curSystem += "POLAR"
        curSystem += ";\n\n"
        return curSystem

    def getHeaderStr(self):
        obj_dict = M3DTools.getHeaderDict()
        self.HeaderStr = []

        for i in obj_dict[ObjectTools.ObjectType.Info]:
            tempStr = M3DProject.ModelingInfo(i)
            self.HeaderStr.append(tempStr)

        res_hea_str = ""
        for i in self.HeaderStr:
            res_hea_str += i + "\n"
        return res_hea_str

    def getParameterStr(self):
        """
        此函数应有两个返回值
        1.参数部分的返回值
        2.网格部分的返回值
        """
        #暂时只写网格部分，参数设置有自定义设置，暂时不做
        gg_str = ""
        res_grid_str = ""
        parmeter_str=[]
        grid_dict = M3DTools.getGridDict()
        for i in grid_dict[ObjectTools.ObjectType.Simu]:
            res_net_str, gg_str = M3DProject.NetStepSetting(i)
            parmeter_str.append(res_net_str)
        for i in parmeter_str:
            res_grid_str += i+"\n"
        return res_grid_str, gg_str

    def getModelStr(self):
        obj_dict = M3DTools.getAllModelObjDict()
        self.getAllModelObjStr = []
        self.objToOtherStr = []

        for i in obj_dict[ObjectTools.ObjectType.Point]:
            model_str, pap_str = M3DObject.Point(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[ObjectTools.ObjectType.Line_Oblique]:
            model_str, pap_str = M3DObject.Line(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[ObjectTools.ObjectType.Line_Conformal]:
            model_str, pap_str = M3DObject.LineConformal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[ObjectTools.ObjectType.Area_Polygonal]:
            model_str, pap_str = M3DObject.AreaPolygonal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[ObjectTools.ObjectType.Area_Conformal]:
            model_str, pap_str = M3DObject.AreaComformal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[ObjectTools.ObjectType.Area_Function]:
            model_str, pap_str = M3DObject.AreaFunction(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        for i in obj_dict[ObjectTools.ObjectType.Area_Rectangular]:
            model_str, pap_str = M3DObject.Rectangle(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        # 正投影体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Conformal]:
            model_str, pap_str = M3DObject.VolConformal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 环形体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Annular]:
            model_str, pap_str = M3DObject.VolAnnular(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 圆柱
        for i in obj_dict[ObjectTools.ObjectType.Vol_Cylinder]:
            model_str, pap_str = M3DObject.VolCylinder(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 圆台
        for i in obj_dict[ObjectTools.ObjectType.Vol_SpecialCone]:
            model_str, pap_str = M3DObject.VolSpecialCone(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 球体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Spherical]:
            model_str, pap_str = M3DObject.VolSpherical(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 圆环区域体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Toroidal_Section]:
            model_str, pap_str = M3DObject.VolToroidal_Section(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 环形区域体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Annular_Section]:
            model_str, pap_str = M3DObject.VolAnnular_Section(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 平行六面体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Parallelepipedal]:
            model_str, pap_str = M3DObject.VolParallelepipedal(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 函数体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Function]:
            model_str, pap_str = M3DObject.VolFunction(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 金字塔体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Pyramid]:
            model_str, pap_str = M3DObject.VolPyramid(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 楔形体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Wedge]:
            model_str, pap_str = M3DObject.VolWedge(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 棱形体体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Rhombus]:
            model_str, pap_str = M3DObject.VolRhombus(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 挤出体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Extruded]:
            model_str, pap_str = M3DObject.VolExtruded(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 四面体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Tetrahedron]:
            model_str, pap_str = M3DObject.VolTetrahedron(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 螺旋体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Helical]:
            model_str, pap_str = M3DObject.VolHelical(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 旋转体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Revolution]:
            model_str, pap_str = M3DObject.VolRevolution(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 阵列体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Array]:
            model_str, pap_str = M3DObject.VolArray(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 参数阵列体
        for i in obj_dict[ObjectTools.ObjectType.Vol_ParamArray]:
            model_str, pap_str = M3DObject.ParamArray(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 草图拉伸体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Draft_Extrude]:
            model_str, pap_str = M3DObject.VolDraft_Extrude(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)
        # 草图旋转体
        for i in obj_dict[ObjectTools.ObjectType.Vol_Draft_Revolution]:
            model_str, pap_str = M3DObject.VolDraft_Revolution(i)
            self.getAllModelObjStr.append(model_str)
            self.objToOtherStr.append(pap_str)

        # Mark
        for i in obj_dict[ObjectTools.ObjectType.MARK]:
            model_str = M3DPhysices.Mark(i)
            self.getAllModelObjStr.append(model_str)

        res_obj_str = ""
        for i in self.getAllModelObjStr:
            if len(i) == 0:
                continue
            res_obj_str += i + "\n"
        return res_obj_str

    def getGenerateGridStr(self):
        res_gg_str = "AUTOGRID;\n\n"
        return res_gg_str

    def getCommonPresetsStr(self):
        """
            返回CommonPresets的M3D
        """
        cp_dict = M3DTools.getCommonPresets()
        self.cp_str = []
        for i in cp_dict[ObjectTools.ObjectType.NewParticle]:
            commonPresets_str = M3DPhysices.NewParticle(i)
            self.cp_str.append(commonPresets_str)

        for i in cp_dict[ObjectTools.ObjectType.NewMaterial]:
            commonPresets_str = M3DPhysices.NewMaterial(i)
            self.cp_str.append(commonPresets_str)

        for i in cp_dict[ObjectTools.ObjectType.FieldSetting]:
            commonPresets_str = M3DProject.FieldSetting(i)
            self.cp_str.append(commonPresets_str)

        res_cp_str = ""
        for i in self.cp_str:
            if len(i) == 0:
                continue
            res_cp_str += i + "\n"
        return res_cp_str

    def getVolAttribute(self):
        """
        按顺序返回与体属性相关的命令，可以参与布尔运算的体
        """
        VolOrderList = []
        VolOrderListStr = ""
        model_str = ""
        pap_str = ""
        VolList = ObjectTools.getAllValidModelObj()

        for i in VolList:
            if i.Type == ObjectTools.ObjectType.Vol_Conformal:
                model_str, pap_str = M3DObject.VolConformal(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Annular:
                model_str, pap_str = M3DObject.VolAnnular(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Cylinder:
                model_str, pap_str = M3DObject.VolCylinder(i)
            elif i.Type == ObjectTools.ObjectType.Vol_SpecialCone:
                model_str, pap_str = M3DObject.VolSpecialCone(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Spherical:
                model_str, pap_str = M3DObject.VolSpherical(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Toroidal_Section:
                model_str, pap_str = M3DObject.VolToroidal_Section(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Annular_Section:
                model_str, pap_str = M3DObject.VolAnnular_Section(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Function:
                model_str, pap_str = M3DObject.VolFunction(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Parallelepipedal:
                model_str, pap_str = M3DObject.VolParallelepipedal(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Pyramid:
                model_str, pap_str = M3DObject.VolPyramid(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Wedge:
                model_str, pap_str = M3DObject.VolWedge(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Rhombus:
                model_str, pap_str = M3DObject.VolRhombus(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Extruded:
                model_str, pap_str = M3DObject.VolExtruded(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Tetrahedron:
                model_str, pap_str = M3DObject.VolTetrahedron(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Helical:
                model_str, pap_str = M3DObject.VolHelical(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Revolution:
                model_str, pap_str = M3DObject.VolRevolution(i)
            # 草图拉伸体
            elif i.Type == ObjectTools.ObjectType.Vol_Draft_Extrude:
                model_str, pap_str = M3DObject.VolDraft_Extrude(i)
            elif i.Type == ObjectTools.ObjectType.Vol_Array:
                model_str, pap_str = M3DObject.VolArray(i)
            elif i.Type == ObjectTools.ObjectType.Vol_ParamArray:
                model_str, pap_str = M3DObject.ParamArray(i)
            VolOrderList.append(pap_str)

        for i in VolOrderList:
            if len(i) == 0:
                continue
            VolOrderListStr += i + "\n"
        return VolOrderListStr

    def getPropertiesAndProcessesStr(self):
        """
        三个返回值
        1.生成金属材料的一条Foil的命令
        2.生成物理坐标的命令
        3.其他物理设置的命令
        """
        pp_dict = M3DTools.getAllPropertiesAndProcessesObj()
        self.PropertiesAndProcessesStr = []
        self.PanelStr = []  # 生成与点线面有关的m2d
        self.GoldMaterial = []  # 生成金属材料的Foil的命令

        # BEAM
        for i in pp_dict[ObjectTools.ObjectType.BEAM]:
            beam_str = M3DEmission.Beam(i)
            self.PropertiesAndProcessesStr.append(beam_str)

        # EXPS
        for i in pp_dict[ObjectTools.ObjectType.EXPS]:
            exps_str = M3DEmission.Exps(i)
            self.PropertiesAndProcessesStr.append(exps_str)

        # GYRO
        for i in pp_dict[ObjectTools.ObjectType.GYRO]:
            gyro_str = M3DEmission.Gyro(i)
            self.PropertiesAndProcessesStr.append(gyro_str)

        # POPU
        for i in pp_dict[ObjectTools.ObjectType.POPU]:
            popu_str = M3DEmission.Popu(i)
            self.PropertiesAndProcessesStr.append(popu_str)

        # FELD
        for i in pp_dict[ObjectTools.ObjectType.FELD]:
            feld_str = M3DEmission.Feld(i)
            self.PropertiesAndProcessesStr.append(feld_str)

        # THER
        for i in pp_dict[ObjectTools.ObjectType.THER]:
            ther_str = M3DEmission.Ther(i)
            self.PropertiesAndProcessesStr.append(ther_str)

        # SECD
        for i in pp_dict[ObjectTools.ObjectType.SECD]:
            secd_str = M3DEmission.Secd(i)
            self.PropertiesAndProcessesStr.append(secd_str)

        # IONI
        for i in pp_dict[ObjectTools.ObjectType.IONI]:
            ioni_str = M3DEmission.Ioni(i)
            self.PropertiesAndProcessesStr.append(ioni_str)

        # PORT
        for i in pp_dict[ObjectTools.ObjectType.PORT]:
            model_str, prot_str = M3DPhysices.Port(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(prot_str)

        # Free
        for i in pp_dict[ObjectTools.ObjectType.FREE]:
            model_str, free_str = M3DPhysices.FreeSpace(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(free_str)

        # SYMT
        for i in pp_dict[ObjectTools.ObjectType.SYMT]:
            model_str, symt_str = M3DPhysices.Symmry(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(symt_str)
        # Solend
        for i in pp_dict[ObjectTools.ObjectType.SOLE]:
            solend_str = M3DPhysices.Solend(i)
            self.PropertiesAndProcessesStr.append(solend_str)

        # DRIV
        for i in pp_dict[ObjectTools.ObjectType.DRIV]:
            model_str, driv_str = M3DPhysices.Driv(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(driv_str)

        # FOIL
        for i in pp_dict[ObjectTools.ObjectType.FOIL]:
            material_str, model_str, foil_str = M3DPhysices.Foil(i)
            self.GoldMaterial.append(material_str)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(foil_str)

        # IND
        for i in pp_dict[ObjectTools.ObjectType.IND]:
            model_str, ind_str = M3DPhysices.Inductor(i)
            self.PanelStr.append(model_str)
            self.PropertiesAndProcessesStr.append(ind_str)

        # MacroParticle
        for i in pp_dict[ObjectTools.ObjectType.MacroParticle]:
            marcoParticle_str = M3DPhysices.MacParticle(i)
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

        res_pap_str = ""
        for i in self.PropertiesAndProcessesStr:
            if len(i) == 0:
                continue
            res_pap_str += i + "\n"

        return res_material_str, res_panel_str, res_pap_str

    def getSimulationSettingStr(self):
        """
        返回时域计算设置
        """
        res_ss_str = ""
        ss_dict = M3DTools.getSimulationSetting()
        for i in ss_dict[ObjectTools.ObjectType.TimeDomain]:
            res_ss_str = M3DProject.TimeDomainSetting(i)
            if len(res_ss_str) != 0:
                res_ss_str += "\n"
        return res_ss_str

    def getAllPlotsStr(self):
        """
        三个返回值
        1.定时器的返回值
        2.观测坐标的返回值
        3.观测的物理设置
        """
        ap_dict = M3DTools.getAllPlotsDict()
        self.getObjectsStr = []
        self.getObseverStr = []
        timer_str = ""

        # DefaultTimer
        for i in ap_dict[ObjectTools.ObjectType.DefaultTimer]:
            timer_str = M3DObserve.DefaultTimer(i)
            if len(timer_str) != 0:
                timer_str += "\n"

        # CustomTimer
        for i in ap_dict[ObjectTools.ObjectType.CustomTimer]:
            ap_str = M3DObserve.CustomTimer(i)
            self.getObseverStr.append(ap_str)

        # CNTR
        for i in ap_dict[ObjectTools.ObjectType.CNTR]:
            model_str, ap_str = M3DObserve.Cntr(i)
            self.getObjectsStr.append(model_str)
            self.getObseverStr.append(ap_str)

        # Vector
        for i in ap_dict[ObjectTools.ObjectType.Vector]:
            model_str, ap_str = M3DObserve.Vector(i)
            self.getObjectsStr.append(model_str)
            self.getObseverStr.append(ap_str)

        # PhasSpace
        for i in ap_dict[ObjectTools.ObjectType.PhasSpace]:
            ap_str = M3DObserve.PhasSpace(i)
            self.getObseverStr.append(ap_str)

        # AreaRan
        for i in ap_dict[ObjectTools.ObjectType.AreaRan]:
            model_str, ap_str = M3DObserve.AreaRan(i)
            self.getObjectsStr.append(model_str)
            self.getObseverStr.append(ap_str)

        # Observe
        for i in ap_dict[ObjectTools.ObjectType.Observe]:
            model_str, ap_str = M3DObserve.Observe(i)
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
        res_do_str = ""
        do_dict = M3DTools.getDumpOptions()
        for i in do_dict[ObjectTools.ObjectType.DataProcess]:
            res_do_str = M3DProject.DataProcessingSetting(i)
            if len(res_do_str) != 0:
                res_do_str += "\n"
        return res_do_str

    def getRunOptionsStr(self):
        res_ro_str = ""
        ro_dict = M3DTools.getRunOptions()
        for i in ro_dict[ObjectTools.ObjectType.RunOptions]:
            res_ro_str = M3DProject.RunOptions(i)
            if len(res_ro_str) != 0:
                res_ro_str += "\n"
        return res_ro_str

    def getRunStr(self):
        run_str = "START;" + "\n" + "STOP;" + "\n\n"
        return run_str


def getNewBlock(name):
    temp_str = "! ==============================================================================!"
    temp_str += "\n! " + name + "\n\n"
    return temp_str

