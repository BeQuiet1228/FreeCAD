SET(Communication_Srcs
	InitGui.py
)
SET(communicationCommand_Srcs
	./communicationCommand/__init__.py
)
SET(communicationGui_Srcs
	./communicationGui/__init__.py
)
SET(communicationResources_Srcs
	./communicationResources/__init__.py
)
SET(all_Srcs
${Communication_Srcs}
${communicationCommand_Srcs}
${communicationGui_Srcs}
${communicationResources_Srcs}

)
ADD_CUSTOM_TARGET(Communication ALL 
	SOURCES ${all_Srcs}
	)
	#fc_copy_sources(Communication "${CMAKE_BINARY_DIR}/Mod/Communication" ${Communication_Srcs})
	#fc_copy_sources(Communication "${CMAKE_BINARY_DIR}/Mod/Communication/communicationCommand" ${communicationCommand_Srcs})
	#fc_copy_sources(Communication "${CMAKE_BINARY_DIR}/Mod/Communication/communicationGui" ${communicationGui_Srcs})
	#fc_copy_sources(Communication "${CMAKE_BINARY_DIR}/Mod/Communication/communicationResources" ${communicationResources_Srcs})
	fc_copy_sources(Communication "${CMAKE_BINARY_DIR}/Mod/Communication" ${all_Srcs})
	INSTALL(
		FILES
		${Communication_Srcs}
		DESTINATION
		Mod/Communication
	)
	INSTALL(
		FILES
		${communicationCommand_Srcs}
		DESTINATION
		Mod/Communication
	)
	INSTALL(
		FILES
		${communicationGui_Srcs}
		DESTINATION
		Mod/Communication
	)
	INSTALL(
		FILES
		${communicationResources_Srcs}
		DESTINATION
		Mod/Communication/communicationResources
	)