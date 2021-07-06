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
	VariateItemWidget.ui
	VariateInputDialog.ui
)
SET(QRC_SRC

)

SET(LUA_SRC
	lua/lapi.c
	lua/lapi.h
	lua/lauxlib.c
	lua/lauxlib.h
	lua/lbaselib.c
	lua/lcode.c
	lua/lcode.h
	lua/lcorolib.c
	lua/lctype.c
	lua/lctype.h
	lua/ldblib.c
	lua/ldebug.c
	lua/ldebug.h
	lua/ldo.c
	lua/ldo.h
	lua/ldump.c
	lua/lfunc.c
	lua/lfunc.h
	lua/lgc.c
	lua/lgc.h
	lua/linit.c
	lua/liolib.c
	lua/ljumptab.h
	lua/llex.c
	lua/llex.h
	lua/llimits.h
	lua/lmathlib.c
	lua/lmem.c
	lua/lmem.h
	lua/loadlib.c
	lua/lobject.c
	lua/lobject.h
	lua/lopcodes.c
	lua/lopcodes.h
	lua/lopnames.h
	lua/loslib.c
	lua/lparser.c
	lua/lparser.h
	lua/lprefix.h
	lua/lstate.c
	lua/lstate.h
	lua/lstring.c
	lua/lstring.h
	lua/lstrlib.c
	lua/ltable.c
	lua/ltable.h
	lua/ltablib.c
	lua/ltm.c
	lua/ltm.h
	lua/lua.c
	lua/lua.h
	lua/lua.hpp
	lua/luac.c
	lua/luaconf.h
	lua/lualib.h
	lua/lundump.c
	lua/lundump.h
	lua/lutf8lib.c
	lua/lvm.c
	lua/lvm.h
	lua/lzio.c
	lua/lzio.h
)
SET(XML_SRC
	xml/pugiconfig.hpp
	xml/pugixml.cpp
	xml/pugixml.hpp
)
SET(JSON_SRC

)
SET(MY_MOC_HDR
	SmartContorlUI.h
	SmartContorl.h
	VariateItemWidget.h
	VariateInputDialog.h
	qcustomplot.h
	SmartContorlInterface.h
	VariableStorer.h
	
)
SET(MY_MOC_SRC
	SmartContorlUI.cpp
	SmartContorl.cpp
	VariateItemWidget.cpp
	VariateInputDialog.cpp
	qcustomplot.cpp
	SmartContorlInterface.cpp
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
	SmartContorlData.cpp
	SmartContorlData.h
	LuaCInterface.h
	LuaCInterface.cpp
	ChipicRunData.cpp
	ChipicRunData.h
	CInterfaceStack.cpp
	CInterfaceStack.h
	LuaEditView.h
	LuaEditView.cpp
	SmartContorlConfig.hpp
	VariateChart.h
	VariateChart.cpp
	VariableStorer.cpp
	VariableStorer.h
	${UI_SRC}
	${JSON_SRC}
	${MY_MOC_SRC}
	${MY_MOC_HDR}
	${Gui_QRC_SRCS}
	${NETWORK_SRC}
	${LUA_SRC}
	${XML_SRC}
)
#设置编译生成文件类型
#add_executable(Contorl ${Contorl_src}) # 生成可执行文件
#SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录

#SET(CMAKE_RUNTIME_OUTPUT_DIRECTORYMY_DEBUG ${CMAKE_CURRENT_BINARY_DIR}/../../bin)
#add_library(common STATIC util.cpp) # 生成静态库
#add_library(common SHARED util.cpp) # 生成动态库或共享库
#add_library(Contorl SHARED ${Contorl_src})

if(smart_contorl_exe)
	add_executable(SmartContorl ${SmartContorl_src}) # 生成可执行文件
	SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录
	add_definitions( -DMY_DEBUG -DMY_LOG -D_SMARTCONTORL_ -DSMART_EXE)
endif()
if(smart_contorl_dll)
	add_definitions(-DMY_LOG -D_SMARTCONTORL_)
	add_library(SmartContorl SHARED ${SmartContorl_src})
endif()


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
	HDF5Reader
	Editor
	)
if(contorl_client_dll)
list(APPEND QT_LIB
	Contorl)
endif()
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
SOURCE_GROUP("lua" FILES ${LUA_SRC})
SOURCE_GROUP("xml" FILES ${XML_SRC})