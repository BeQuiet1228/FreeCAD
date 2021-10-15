SET(Common_Srcs
	__init__.py
	Init.py
)
SET(CommonCommand_Srcs
	./CommonCommand/__init__.py
	./CommonCommand/M3DEditorWorkbench.py
	./CommonCommand/NewDocument.py
	./CommonCommand/OtherToolbarCommand.py
	./CommonCommand/PostProcessingWorkbench.py
	./CommonCommand/SimulationWorkbench.py
)
SET(CommonGui_Srcs
	./CommonGui/__init__.py
	./CommonGui/CoordinateSystemDialogMain.py
	./CommonGui/CoordinateSystemMode.py
	./CommonGui/CoordinateSystemUI.py
	./CommonGui/NewCoordinateSystem.py
	./CommonGui/SelectCoordinateSystem.py
	./CommonGui/SetWorkRangeUI.py
)
SET(CommonResources_Srcs
	./CommonResources/document-new.svg
	./CommonResources/RotateViewLeft.svg
	./CommonResources/RotateViewRight.svg
)
SET(Tools_Srcs
	./Tools/__init__.py
	./Tools/AllDialogFather.py
	./Tools/BaseObjDialog.py
	./Tools/BooleanOperation.py
	./Tools/Completer.py
	./Tools/CoordinateSystemTools.py
	./Tools/DocumentTools.py
	./Tools/GuiTools.py
	./Tools/InputTools.py
	./Tools/ModelingByM3dFile.py
	./Tools/ModelingCommandForM3dFile.py
	./Tools/ObjectsTools.py
	./Tools/PhysicsDialog.py
	./Tools/PlacementTools.py
	./Tools/UnitTools.py
)

SET(all_Srcs
${Common_Srcs}
${CommonCommand_Srcs}
${CommonGui_Srcs}
${CommonResources_Srcs}
${Tools_Srcs}
)
add_custom_target(Common ALL SOURCES ${all_Srcs})
fc_copy_sources(Common "${CMAKE_BINARY_DIR}/Mod/Modeling/Common" ${all_Srcs})
install(FILES ${all_Srcs} DESTINATION Mod/Modeling/Common)
#install(
#	FILES
#	${Common_Srcs}
#	DESTINATION
#	Mod/Modeling/Common
#)
#install(
#	FILES
#	${CommonCommand_Srcs}
#	DESTINATION
#	Mod/Modeling/Common/CommonCommand
#)
#install(
#	FILES
#	${CommonGui_Srcs}
#	DESTINATION
#	Mod/Modeling/Common/CommonGui
#)
#install(
#	FILES
#	${CommonResources_Srcs}
#	DESTINATION
#	Mod/Modeling/Common/CommonResources
#)
#install(
#	FILES
#	${Tools_Srcs}
#	DESTINATION
#	Mod/Modeling/Common/Tools
#)