
add_subdirectory(App)
INSTALL(
    FILES
        Init.py
        InitGui.py
    DESTINATION
        Mod/PartChipic
)
Set(Sources_Srcs
	Init.py
    InitGui.py
)
File(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/PartChipic)