def Load(workbench):
    # fileList = ["Std_New"]
    # workbench.appendMenu('File', fileList)
    cmdlst2 = ["CreateHollowedCylinder",
                "CreateTorusFace",
                "CreateCylinder",
                "CreateCone",
                "CreateSpecialCone",
                "CreateTorus",
                "CreateOrthographicBody",
                "CreateParallelogram",
                "CreateSphere",
                "CreateWedge",
                "CreatePyramid"]
    workbench.appendMenu('3D Modeling', cmdlst2)