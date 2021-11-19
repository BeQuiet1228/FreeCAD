SET(Model3D_Srcs
__init__.py
Init.py
InitGui.py
ReadmeWithVolume.md
)
add_custom_target(Model3D ALL SOURCES ${Model3D_Srcs})
fc_copy_sources(Model3D "${CMAKE_BINARY_DIR}/Mod/Model3D" ${Model3D_Srcs})
install(
	FILES
	${Model3D_Srcs}
	DESTINATION
	Mod/Model3D
)
SET(Sources_Srcs
Command3D
Gui3D
M3DFileNew
Resources3D
Tools
)
File(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Model3D)