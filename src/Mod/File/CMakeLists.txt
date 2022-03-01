add_custom_target(File)
SET(Sources_Srcs
	FileCommand
	FileGui
	FileResources
	InitGui.py
	__init__.py
)
file(COPY ${Sources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/File)
#SET(FileCommand_Srcs
#FileCommand/FileActions.py
#FileCommand/__init__.py
#)
#SET(FileCommand_M2dFile_Srcs
#FileCommand/M2dFile/M2DContainer.py
#FileCommand/M2dFile/M2dEmission.py
#FileCommand/M2dFile/M2dObject.py
#FileCommand/M2dFile/M2dPhysics.py
#FileCommand/M2dFile/M2dProject.py
#FileCommand/M2dFile/__init__.py
#)
#SET(FileCommand_M3DFile_Srcs
#FileCommand/M3DFile/CHIPICCommand.py
#FileCommand/M3DFile/GetCommandByParameter.py
#FileCommand/M3DFile/GetParameterByCommand.py
#FileCommand/M3DFile/M3DFileUtil.py
#FileCommand/M3DFile/ParseM3DFile.py
#FileCommand/M3DFile/__init__.py
#)
#SET(FileCommand_TextUI_Srcs
#FileCommand/TextUI/FileTextView.py
#FileCommand/TextUI/FindDialogMain.py
#FileCommand/TextUI/MyQSyntaxHighlighter.py
#FileCommand/TextUI/__init__.py
#)
#SET(FileGui_Srcs
#FileGui/FileTextEditor.py
#FileGui/FileTextEditor.ui
#FileGui/__init__.py
#)
#SET(FileResources_Srcs
#FileResources/application-exit.svg
#FileResources/file-close.svg
#FileResources/file-m3dFind.svg
#FileResources/file-m3dView.png
#FileResources/file-m3dView.svg
#FileResources/file-recent.svg
#FileResources/file-save-as.svg
#FileResources/file-workbench.svg
#FileResources/__init__.py
#)
#SET(File_Srcs
#InitGui.py
#__init__.py
#)
#
##add_custom_target(File ALL SOURCES ${File_Srcs})
##fc_copy_sources(File "${CMAKE_BINARY_DIR}/Mod/File" ${File_Srcs})
##install(
##	FILES
##	${File_Srcs}
##	DESTINATION
##	Mod/File
##)
#FILE(COPY ${CMAKE_SOURCE_DIR}/src/Mod/File/${FileCommand_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/File/FileCommand)
#FILE(COPY ${CMAKE_SOURCE_DIR}/src/Mod/File/${FileCommand_M2dFile_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/File/FileCommand/M2dFile)
#FILE(COPY ${CMAKE_SOURCE_DIR}/src/Mod/File/${FileCommand_M3DFile_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/File/FileCommand/M3DFile)
#FILE(COPY ${CMAKE_SOURCE_DIR}/src/Mod/File/${FileCommand_TextUI_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/File/FileCommand/TextUI)
#FILE(COPY ${CMAKE_SOURCE_DIR}/src/Mod/File/${FileGui_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/File/FileGui)
#FILE(COPY ${CMAKE_SOURCE_DIR}/src/Mod/File/${FileResources_Srcs} DESTINATION ${CMAKE_BINARY_DIR}/Mod/File/FileResources)
#FILE(COPY ${CMAKE_SOURCE_DIR}/src/Mod/File/${File_Srcs} DESTINATION "${CMAKE_BINARY_DIR}/Mod/File")
#