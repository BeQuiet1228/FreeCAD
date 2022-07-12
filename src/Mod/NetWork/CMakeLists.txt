SET(NetWork_Srcs
./NetWorkCommand/ConfigDlgMain.py
./NetWorkCommand/__init__.py
./NetWorkGui/ConfigDlg.py
./NetWorkGui/ConfigDlg.ui
./NetWorkGui/__init__.py
./__init__.py
)
add_custom_target(NetWork ALL SOURCES ${NetWork_Srcs})
fc_copy_sources(NetWork "${CMAKE_BINARY_DIR}/Mod/NetWork" ${NetWork_Srcs})

install(
	FILES
	${NetWork_Srcs}
	DESTINATION
	Mod/NetWork
)