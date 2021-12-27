add_custom_target(Physics)
SET(Sources_Srcs
	StyledComboBox.py
	SwitchWorkbench.py
	__init__.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/Physics)