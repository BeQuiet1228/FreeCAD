add_custom_target(CustomParameter)
SET(Sources_Srcs
CustomParameterCommand
CustomParameterGui
CustomParameterResources
__init__.py
)
File(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/CustomParameter)
#SET(CustomParameter_Srcs
#	__init__.py
#)
#SET(CustomParameterCommand_Srcs
#	./CustomParameterCommand/__init__.py
#	#./CustomParameterCommand/CodeEdit.py
#	./CustomParameterCommand/DlgCustomParameterMain.py
#	./CustomParameterCommand/INHighLighter.py
#	./CustomParameterCommand/newParam.py
#	./CustomParameterCommand/TestTableView.py
#)
#SET(CustomParameterGui_Srcs
#	./CustomParameterGui/__init__.py
#	./CustomParameterGui/DlgCustomeParameter.py
#	./CustomParameterGui/DlgCustomeParameter.ui
#	./CustomParameterGui/searchTool.py
#	./CustomParameterGui/searchTool.ui
#	./CustomParameterGui/TableView.py
#	./CustomParameterGui/TableView.ui
#)
#SET(CustomParameterResources_Srcs
#	./CustomParameterResources/Parameter.svg
#)
#SET(all_Srcs
#${CustomParameter_Srcs}
#${CustomParameterCommand_Srcs}
#${CustomParameterGui_Srcs}
#${CustomParameterResources_Srcs}
#)
#ADD_CUSTOM_TARGET(CustomParameter ALL
#	SOURCES ${all_Srcs}
#)
##fc_copy_sources(CustomParameter "${CMAKE_BINARY_DIR}/Mod/CustomParameter" ${CustomParameter_Srcs})
##fc_copy_sources(CustomParameter "${CMAKE_BINARY_DIR}/Mod/CustomParameter/CustomParameterCommand" ${CustomParameterCommand_Srcs})
##fc_copy_sources(CustomParameter "${CMAKE_BINARY_DIR}/Mod/CustomParameter/CustomParameterGui" ${CustomParameterGui_Srcs})
##fc_copy_sources(CustomParameter "${CMAKE_BINARY_DIR}/Mod/CustomParameter/CustomParameterResources" ${CustomParameterResources_Srcs})
#fc_copy_sources(CustomParameter "${CMAKE_BINARY_DIR}/Mod/CustomParameter" ${all_Srcs})
#INSTALL(
#	FILES
#	${CustomParameter_Srcs}
#	DESTINATION
#	Mod/CustomParameter
#)
#INSTALL(
#	FILES
#	${CustomParameterCommand_Srcs}
#	DESTINATION
#	Mod/CustomParameter/CustomParameterCommand
#)
#INSTALL(
#	FILES
#	${CustomParameterGui_Srcs}
#	DESTINATION
#	Mod/CustomParameter/CustomParameterGui
#)
#INSTALL(
#	FILES
#	${CustomParameterResources_Srcs}
#	DESTINATION
#	Mod/CustomParameter/CustomParameterResources
#)
