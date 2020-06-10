def Load(workbench):
    # fileList = ["Std_New"]
    # workbench.appendToolbar('File', fileList)
    cmdlst = ["CreateHollowedCylinder",
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
    benches = ["Simulation","Post Processing"]
    workbench.appendToolbar('File',benches)
    workbench.appendToolbar('3D Modeling', cmdlst)