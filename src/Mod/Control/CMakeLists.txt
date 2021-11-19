add_custom_target(Control)
SET(Sources_Srcs
controlCommand
controlGui
controlResources
InitGui.py
__init__.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Control)
#SET(Control_Srcs
#	InitGui.py
#)
#SET(controlResources_Srcs
#	./controlResources/__init__.py
#)
#SET(controlGui_Srcs
#	./controlGui/__init__.py
#)
#SET(controlCommand_Srcs
#	./controlCommand/__init__.py
#)
#SET(all_Srcs
#	${Control_Srcs}
#	${controlResources_Srcs}
#	${controlGui_Srcs}
#	${controlCommand_Srcs}
#)
#ADD_CUSTOM_TARGET(Control ALL
#	SOURCES ${all_Srcs}
#)
##fc_copy_sources(Control "${CMAKE_BINARY_DIR}/Mod/Control" ${Control_Srcs})
##fc_copy_sources(Control "${CMAKE_BINARY_DIR}/Mod/Control" ${controlResources_Srcs})
##fc_copy_sources(Control "${CMAKE_BINARY_DIR}/Mod/Control" ${controlGui_Srcs})
##fc_copy_sources(Control "${CMAKE_BINARY_DIR}/Mod/Control" ${controlCommand_Srcs})
#fc_copy_sources(Control "${CMAKE_BINARY_DIR}/Mod/Control" ${all_Srcs})
#INSTALL(
#	FILES
#	${Control_Srcs}
#	DESTINATION
#	Mod/Control
#)
#INSTALL(
#	FILES
#	${controlResources_Srcs}
#	DESTINATION
#	Mod/Control/controlResources
#)
#INSTALL(
#	FILES
#	${controlGui_Srcs}
#	DESTINATION
#	Mod/Control/controlGui
#)
#INSTALL(
#	FILES
#	${controlCommand_Srcs}
#	DESTINATION
#	Mod/Control/controlCommand
#)