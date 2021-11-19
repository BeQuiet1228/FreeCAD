
add_subdirectory(App)
if(BUILD_GUI)
    add_subdirectory(Gui)
endif(BUILD_GUI)

INSTALL(
    FILES
        Init.py
        InitGui.py
        DrawingExample.py
        DrawingTests.py
        DrawingPatterns.py
    DESTINATION
        Mod/Drawing
)
SET(Srcs
DrawingExample.py
DrawingPatterns.py
DrawingTests.py
Templates
#App
#Gui
)
INSTALL(
    DIRECTORY
        Templates
    DESTINATION
        ${CMAKE_INSTALL_DATADIR}/Mod/Drawing
    FILES_MATCHING 
        PATTERN "*.svg*"
        PATTERN "*.dxf*"
)
#File(COPY "Templates" DESTINATION ${CMAKE_BINARY_DIR}/Mod/Drawing)
File(COPY ${Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Drawing)
