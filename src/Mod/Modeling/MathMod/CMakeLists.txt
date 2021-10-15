SET(MathMod_Srcs
libgcc_s_seh-1.dll
libstdc++-6.dll
libwinpthread-1.dll
MathMod.exe
mathmodcollection.json
mathmodconfig.json
Qt5Core.dll
Qt5Gui.dll
Qt5OpenGL.dll
Qt5Svg.dll
Qt5Widgets.dll
)
SET(platforms_Srcs
./platforms/qminimal.dll
./platforms/qoffscreen.dll
./platforms/qwindows.dll
)

SET(all_Srcs
${MathMod_Srcs}
${platforms_Srcs}
)

add_custom_target(MathMod ALL SOURCES ${all_Srcs})

fc_copy_sources(MathMod "${CMAKE_BINARY_DIR}/Mod/Modeling/MathMod" ${all_Srcs})

install(
	FILES
	${MathMod_Srcs}
	DESTINATION
	Mod/Modeling/MathMod
)
install(
	FILES
	${platforms_Srcs}
	DESTINATION
	Mod/Modeling/MathMod/platforms
)