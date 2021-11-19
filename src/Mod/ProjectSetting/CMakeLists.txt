add_custom_target(ProjectSetting)
SET(Sources_Srcs
	Commands
	ProjectSettingGui
	ProjectSettingResources
	Tools
	InitGui.py
	__init__.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/ProjectSetting)
