project(Editor)

#添加外部库
list(APPEND QT_LIB
    debug MSVCRTD.LIB
    debug MSVCPRTD.LIB
    optimized MSVCRT.LIB
    optimized MSVCPRT.LIB
	)
set(MOC_HEADER
	FindDialog.h
	matchwordsthrea.h
	codeeditor.h
	M3dEditor.h
)
set(UI_SRC
	FindDialog.ui
)

#引入头文件
include_directories(
    ${CMAKE_BINARY_DIR}/src
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
)

add_definitions(-D_EDITOR_)

#生成moc文件
fc_wrap_cpp(MOC_SRCS ${MOC_HEADER})

if (BUILD_QT5)
    include_directories(
        ${Qt5Core_INCLUDE_DIRS}
        ${Qt5Widgets_INCLUDE_DIRS}
        ${Qt5OpenGL_INCLUDE_DIRS}
        ${Qt5PrintSupport_INCLUDE_DIRS}
        ${Qt5Svg_INCLUDE_DIRS}
        ${Qt5Network_INCLUDE_DIRS}
        ${Qt5UiTools_INCLUDE_DIRS}
    )
    list(APPEND QT_LIB
        ${Qt5Core_LIBRARIES}
        ${Qt5Widgets_LIBRARIES}
        ${Qt5OpenGL_LIBRARIES}
        ${Qt5PrintSupport_LIBRARIES}
        ${Qt5Svg_LIBRARIES}
        ${Qt5Network_LIBRARIES}
        ${Qt5UiTools_LIBRARIES}
    )
	QT5_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
else()
    include_directories(
        ${QT_INCLUDE_DIR}
    )
    list(APPEND QT_LIB
        ${QT_LIBRARIES}
        ${QT_QTUITOOLS_LIBRARY}
    )
	QT4_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
endif()

SET(EDIT_SRC
	casewordlistwidget.cpp
	casewordlistwidget.h
	codeeditor.cpp
	codeeditor.h
	matchwordsthrea.cpp
	matchwordsthrea.h
	M3dHightLighter.cpp
	M3dHightLighter.h
	FindDialog.ui
	FindDialog.h
	FindDialog.cpp
	EditorExportConfig.hpp
	M3dEditor.h
	M3dEditor.cpp
)
source_group("moc" FILES ${MOC_SRCS})
source_group("ui_h" FILES ${Gui_UIC_HDRS})
source_group("src" FILES ${EDIT_SRC})


	add_library(Editor SHARED
	main.cpp
	${EDIT_SRC}
	${Gui_UIC_HDRS}
	${MOC_SRCS})



#链接静态库
target_link_libraries(Editor ${QT_LIB})
SET_BIN_DIR(Editor Editor) #设置文件输出目录
