add_custom_target(Visualization)
SET(Sources_Srcs
    InitGui.py
    VisualizationCommand
    VisualizationResources
    __init__.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Visualization)
