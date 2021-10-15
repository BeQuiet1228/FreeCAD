add_subdirectory(Common)
add_subdirectory(MathMod)
add_subdirectory(Modeling2D)
add_subdirectory(Modeling3D)
SET(Modeling_Srcs
InitGui.py
__init__.py
)
add_custom_target(Modeling ALL SOURCES ${Modeling_Srcs})
fc_copy_sources(Modeling "${CMAKE_BINARY_DIR}/Mod/Modeling" ${Modeling_Srcs})
install(
	FILES
	${Modeling_Srcs}
	DESTINATION
	Mod/Modeling
)