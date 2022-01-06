SET(TemplatePyMod_Srcs
./Automation.py
./Commands.py
./DocumentObject.py
./FeaturePython.py
./Init.py
./InitGui.py
./MengerSponge.py
./Mesh2Shape.py
./PythonQt.py
./SplineSurface.py
./TaskPanel.py
./TaskPanel.ui
./Tests.py
./Texture.py
)
add_custom_target(TemplatePyMod ALL SOURCES ${TemplatePyMod_Srcs})
fc_copy_sources(TemplatePyMod "${CMAKE_BINARY_DIR}/Mod/TemplatePyMod" ${TemplatePyMod_Srcs})
install(
	FILES
	${TemplatePyMod}
	DESTINATION
	Mod/TemplatePyMod
)
