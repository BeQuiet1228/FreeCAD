add_custom_target(M3DFileEditor)

SET(Sources_Srcs
	M3DFileEditorCommand
	M3DFileEditorGui
	M3DFileEditorResources
	__init__.py
	InitGui.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/M3DFileEditor)