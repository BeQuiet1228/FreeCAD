SET(Sourcse_Srcs
Common
MathMod
Modeling2D
Modeling3D
InitGui.py
__init__.py
)
add_custom_target(Modeling ALL SOURCES)
File(COPY ${Sourcse_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Modeling)
