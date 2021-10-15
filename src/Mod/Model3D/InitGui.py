# -*- coding: utf-8 -*-
import FreeCAD
import FreeCADGui


class Modeling3DWorkbench(Workbench):
    # MenuText = "My Workbench"
    # ToolTip = "A description of my workbench"
    # Icon = """paste here the contents of a 16x16 xpm icon"""

    def __init__(self):
        self.__class__.Icon = FreeCAD.getResourceDir() + "Mod/Draft/Resources/icons/DraftWorkbench.svg"
        self.__class__.MenuText = "Draft123123123"
        self.__class__.ToolTip = "The Draft module is used for basic 2D CAD Drafting"

    def Initialize(self):
        """This function is executed when FreeCAD starts"""
        # import MyModuleA, MyModuleB  # import here all the needed files that create your FreeCAD commands
        import Modeling.Modeling2D.Modeling2DCommand
        import Model3D.Command3D.Model3DCommand
        # self.list = []  # A list of command names created in the line above
        import Gui3D
        Gui3D.LoadAll(self)
        # # @wangzhenguo 建的模型
        # wzg_list = ['CreateVolConformal_3D', 'CreateVolAnnular_3D', 'CreateVolPyramid_3D',
        #             'CreateVolRhombus_3D', 'CreateVolRevolution_3D', 'CreateAreaFunction_3D',
        #             'CreateParameter', 'UpdateBooleanCommand_3D', 'CreateM3D_new',
        #             'CreateDraftExtruded_3D', 'CreateDraftRevolution_3D']
        # # @赵洲建的模型
        # zz_list = ['CreatePoint_3D', 'CreateLineOblique_3D', 'CreateLineConformal_3D',
        #              'CreateAreaConformal_3D', 'CreateAreaRectangle_3D']
        # # @钟宾阳建的模型
        # zby_list = ['Create_3D_SpecialCone', 'Create_3D_Cylinder', "Create_3D_Tetrahedron",
        #             "Create_3D_Wedge", "Create3DExtruded", "CreatePolygonal"]
        # # @夏琦洋建的模型
        # xqy_list = ['CreateVolSpherical_3D', 'CreateVolAnnular_Section_3D', 'CreateVolToroidal_Section_3D',
        #             'CreateVolParallelepipedal_3D', 'CreateVolFunction_3D', 'CreateVolHelical_3D']
        # # 防止改到同一行代码，暂时分开处理
        # self.list += wzg_list+zz_list+zby_list+xqy_list
        #
        # # @王振国物理设置
        # wzg_phy_list = ['CreateBeam_3D', 'CreateExps_3D', 'CreateGyro_3D', 'CreateFeld_3D', 'CreateTher_3D',
        #                 'CreateSecd_3D', 'CreatePort_3D']
        # # @赵洲
        # zz_phy_list = ['CreateCustomTimer_3D', 'CreateNewMaterial_3D', 'CreateMacroParticle_3D',
        #                'CreateParticleDefine_3D', 'CreateFieldSetting_3D', 'CreateMark', 'CreateModelingInfo']
        # # @钟宾阳
        # zby_phy_list = ['Create_3D_Foil', 'Create3DFreeSpace', 'Create3DSymtry', 'Create3D_Driv', 'Create3D_Popu',
        #                 'CreateSolend', 'CreateInductor_3D', 'CreateRunOptions', 'CreateDataProcessingSetting']
        # # 夏琦洋
        # xqy_phy_list = ['CreateIoni_3D', 'CreateCntr_3D', 'CreateVector_3D', 'CreateAreaRan_3D',
        #                 'CreatePhasSpace_3D', 'CreateDefTimer_3D', 'CreateObserve_3D',
        #                 'NetStepSetting_3D', 'TimeDomainSetting_3D']
        #
        # self.list += wzg_phy_list + zz_phy_list + zby_phy_list + xqy_phy_list
        #
        # self.appendToolbar("My Commands", self.list)  # creates a new toolbar with your commands
        # self.appendMenu("My New Menu", self.list)  # creates a new menu
        # self.appendMenu(["An existing Menu", "My submenu"], self.list)  # appends a submenu to an existing menu

    # def Activated(self):
    #     """This function is executed when the workbench is activated"""
    #     FreeCAD.Console.PrintError("init!\n")
    #     return
    #
    # def Deactivated(self):
    #     """This function is executed when the workbench is deactivated"""
    #     return
    #
    # def ContextMenu(self, recipient):
    #     """This is executed whenever the user right-clicks on screen"""
    #     # "recipient" will be either "view" or "tree"
    #     self.appendContextMenu("My commands", self.list)  # add commands to the context menu
    #
    # def GetClassName(self):
    #     # This function is mandatory if this is a full python workbench
    #     # This is not a template, the returned string should be exactly "Gui::PythonWorkbench"
    #     return "Gui::PythonWorkbench"


FreeCADGui.addWorkbench(Modeling3DWorkbench())
