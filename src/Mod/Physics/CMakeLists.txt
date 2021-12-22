add_custom_target(Physics)
SET(Sources_Srcs
	PhysicsCommand
	PhysicsGui
	PhysicsResources
	PhysicsTools
	StyledComboBox.py
	SwitchWorkbench.py
	__init__.py
	InitGui.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Physics)