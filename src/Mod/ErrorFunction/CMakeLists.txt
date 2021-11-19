SET(ErrorFunction_Srcs
__init__.py
ErrorDialog.py
warning.py
warning.ui
)

add_custom_target(ErrorFunction ALL
	SOURCES ${ErrorFunction_Srcs}
)

fc_copy_sources(ErrorFunction "${CMAKE_BINARY_DIR}/Mod/ErrorFunction" ${ErrorFunction_Srcs})

install(
	FILES
	${ErrorFunction_Srcs}
	DESTINATION
	Mod/ErrorFunction
)