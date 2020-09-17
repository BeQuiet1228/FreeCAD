#设置项目名称
project(SmartContorl)


#设置预定义
#编译服务器端
#SET(contorl_service)
#以exe形式编译客户端
#SET(contorl_client_exe)
#以动态链接库的形式编译客户端
#SET(contorl_client_dll)




#源文件
SET(UI_SRC
	SmartContorlUI.ui
)
SET(QRC_SRC

)
SET(JSON_SRC

)
SET(MY_MOC_HDR
	SmartContorlUI.h
)
SET(MY_MOC_SRC
	SmartContorlUI.cpp
)
SET(NETWORK_SRC

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
SET(SmartContorl_src
	main.cpp
	VariateAnalysis.h
	VariateAnalysis.cpp
	FileMaker.h
	FileMaker.cpp
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
#add_library(Contorl SHARED ${Contorl_src})

#if(contorl_client_exe)
	add_executable(SmartContorl ${SmartContorl_src}) # 生成可执行文件
	SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录
	add_definitions( -DMY_DEBUG -DMY_LOG)
#endif()
#if(contorl_client_dll)
#	add_definitions( -DMY_LOG)
#	add_library(SmartContorl SHARED ${Contorl_src})
#endif()


#增加包含目录
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
	
)
#增加外部库
list(APPEND QT_LIB
    debug MSVCRTD.LIB
    debug MSVCPRTD.LIB
    optimized MSVCRT.LIB
    optimized MSVCPRT.LIB
	Contorl
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
target_link_libraries(SmartContorl ${QT_LIB})
SET_BIN_DIR(SmartContorl SmartContorl) #设置文件输出目录
#生成moc文件
fc_wrap_cpp(MY_MOC_SRCS ${MY_MOC_HDR})

source_group("Properties" Files ${MY_MOC_SRCS})

SOURCE_GROUP("Uic" FILES ${Gui_UIC_HDRS})

SOURCE_GROUP("Network" FILES ${NETWORK_SRC})