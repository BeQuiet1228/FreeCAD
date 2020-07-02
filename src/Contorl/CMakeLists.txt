#设置项目名称
project(Contorl)
#源文件
SET(UI_SRC
	Contorl.ui
)
SET(JSON_SRC
	cJSON.c
	cJSON.h
	CJsonObject.cpp
	CJsonObject.hpp
)
SET(Contorl_src
	main.cpp
	Contorl.cpp
	Contorl.h
	LonelinessMode.cpp
	LonelinessMode.h
	runchipic3d.cpp
	runchipic3d.h
	WinMessageManager.cpp
	WinMessageManager.h
	MessageTransition.cpp
	MessageTransition.h
	JsonMessageGetter.cpp
	JsonMessageGetter.h
	Chipic.cpp
	Chipic.h
	ChipicManager.cpp
	ChipicManager.h
	${UI_SRC}
	${JSON_SRC}
)
#设置编译生成文件类型
add_executable(Contorl ${Contorl_src}) # 生成可执行文件
#SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录
SET_BIN_DIR(Contorl Contorl) #设置可执行文件目录
#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_BINARY_DIR}/../../bin)
#add_library(common STATIC util.cpp) # 生成静态库
#add_library(common SHARED util.cpp) # 生成动态库或共享库
#add_library(Contorl SHARED ${Contorl_src})
#增加包含目录
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
	
)
#增加外部库
list(APPEND QT_LIB
	FreeCADBase
    ${Boost_LIBRARIES}
	)
#引入Qt库
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
else()
    include_directories(
        ${QT_INCLUDE_DIR}
    )
    list(APPEND QT_LIB
        ${QT_LIBRARIES}
        ${QT_QTUITOOLS_LIBRARY}
    )
endif()
#链接静态库
target_link_libraries(Contorl ${QT_LIB})

SET(MY_MOC_HDR
	lonelinessmode.h
	Contorl.h
	JsonMessageGetter.h
	Chipic.h
	ChipicManager.h
)
SET(MY_MOC_SRC
	lonelinessmode.cpp
	Contorl.cpp
	JsonMessageGetter.cpp
	Chipic.cpp
	ChipicManager.cpp
)
fc_wrap_cpp(MY_MOC_SRCS ${MY_MOC_HDR})
source_group("Properties" Files ${MY_MOC_SRCS})

#处理ui文件
if (BUILD_QT5)
    #QT5_ADD_RESOURCES(Gui_QRC_SRCS ${Gui_RES_SRCS})
    QT5_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
else()
    #QT4_ADD_RESOURCES(Gui_QRC_SRCS ${Gui_RES_SRCS})
    QT4_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
endif()
SOURCE_GROUP("Uic" FILES ${Gui_UIC_HDRS})