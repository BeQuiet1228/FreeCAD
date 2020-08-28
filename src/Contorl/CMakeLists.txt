#设置预定义
if(WIN32)
#add_definitions(-D_CONTORL_ -DMY_DEBUG -DMY_LOG -DSERVICE)
#add_definitions(-D_CONTORL_ -DMY_DEBUG -DMY_LOG)
add_definitions(-D_CONTORL_ -DMY_LOG)
endif(WIN32)
#设置项目名称
project(Contorl)
#源文件
SET(UI_SRC
	Contorl.ui
	HintDailog.ui
	ContorlDataBar.ui
	ContorlButtonBar.ui
	ThreadCountDialog.ui
	LoadingDialog.ui
	NetworkClientLoginDailog.ui
	ServiceUI.ui
)
SET(QRC_SRC
	Contorl.qrc
)
SET(JSON_SRC
	cJSON.c
	cJSON.h
	CJsonObject.cpp
	CJsonObject.hpp
)
SET(MY_MOC_HDR
	Contorl.h
	JsonMessageGetter.h
	Chipic.h
	ChipicManager.h
	HintDailog.h
	ContorlDataBar.h
	ContorlButtonBar.h
	ThreadCountDialog.h
	LoadingDialog.h
	NetworkClient.h
	NetworkServer.h
	NetworkSocket.h
	NetworkClientLoginDailog.h
	ServiceUI.h
)
SET(MY_MOC_SRC
	Contorl.cpp
	JsonMessageGetter.cpp
	Chipic.cpp
	ChipicManager.cpp
	HintDailog.cpp
	ContorlDataBar.cpp
	ThreadCountDialog.cpp
	LoadingDialog.cpp
	ContorlButtonBar.cpp
)
SET(NETWORK_SRC
	NetworkClient.cpp
	NetworkClient.h
	NetworkServer.h
	NetworkServer.cpp
	NetworkSocket.cpp
	NetworkSocket.h
	NetworkEmitter.h
	NetworkEmitter.cpp
	NetworkClientLoginDailog.h
	NetworkClientLoginDailog.cpp
	NetworkUser.h
	NetworkUser.cpp
	File.cpp
	File.h
	ServiceUI.h
	ServiceUI.cpp
)
#引入头文件
include_directories(
    ${CMAKE_BINARY_DIR}/src
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_CURRENT_BINARY_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${Boost_INCLUDE_DIRS}
    ${PYTHON_INCLUDE_DIRS}
    ${XercesC_INCLUDE_DIRS}
    ${ZLIB_INCLUDE_DIR}
    ${PYCXX_INCLUDE_DIR}
)

#处理ui和qrc文件
if (BUILD_QT5)
    QT5_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT5_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
else()
    QT4_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT4_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
endif()
SET(Contorl_src
	main.cpp
	runchipic3d.cpp
	runchipic3d.h
	RunChipic3dListener.cpp
	RunChipic3dListener.h
	MessageTransition.cpp
	MessageTransition.h
	MessageSender.cpp
	MessageSender.h
	EmitterInterface.h
	LocalEimtter.cpp
	LocalEimtter.h
	ContorlInterface.h
	ContorlInterface.cpp
	ContorlConfig.hpp
	openLog.cpp
	openLog.h
	${UI_SRC}
	${JSON_SRC}
	${MY_MOC_SRC}
	${MY_MOC_HDR}
	${Gui_QRC_SRCS}
	${NETWORK_SRC}
)
#设置编译生成文件类型
#add_executable(Contorl ${Contorl_src}) # 生成可执行文件
#SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录

#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORYMY_DEBUG ${CMAKE_CURRENT_BINARY_DIR}/../../bin)
#add_library(common STATIC util.cpp) # 生成静态库
#add_library(common SHARED util.cpp) # 生成动态库或共享库
add_library(Contorl SHARED ${Contorl_src})

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
SET_BIN_DIR(Contorl Contorl) #设置文件输出目录
#生成moc文件
fc_wrap_cpp(MY_MOC_SRCS ${MY_MOC_HDR})

source_group("Properties" Files ${MY_MOC_SRCS})

SOURCE_GROUP("Uic" FILES ${Gui_UIC_HDRS})

SOURCE_GROUP("Network" FILES ${NETWORK_SRC})