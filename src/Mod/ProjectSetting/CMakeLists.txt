add_custom_target(ProjectSetting)
SET(Sources_Srcs
	Commands
	InitGui.py
	ProjectSettingGui
	ProjectSettingResources
	Tools
	__init__.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/ProjectSetting)
