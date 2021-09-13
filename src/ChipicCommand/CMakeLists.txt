#设置预定义
if(WIN32)
#add_definitions(-D_CONTORL_)
add_definitions(-D_CONTORL_ )
endif(WIN32)
#设置项目名称
project(ChipicCommand)
#源文件
SET(UI_SRC

)
SET(QRC_SRC

)

SET(MY_MOC_HDR

)
SET(MY_MOC_SRC

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
SET(volume_src
	Model.h
	Model.cpp
	Point.cpp
	Point.h
	ModelTexture.h
	ModelTexture.cpp
	Line.h
	Line.cpp
	LineOblique.h
    LineOblique.cpp
    AreaConformal.h
    AreaConformal.cpp
    AreaRectangular.h
    AreaRectangular.cpp
    VolConformal.h
    VolConformal.cpp
    VolAnnular.h
    VolAnnular.cpp
    VolParallelepipedal.h
    VolParallelepipedal.cpp
    VolSpherical.h
    VolSpherical.cpp
    VolWedge.h
    VolWedge.cpp
    VolPyramid.h
    VolPyramid.cpp
    VolRhombus.h
    VolRhombus.cpp
    VolTetrahedron.h
    VolTetrahedron.cpp
    VolToroidalSection.h
    VolToroidalSection.cpp
    VolAnnularSection.h
    VolAnnularSection.cpp
    VolHelical.h
    VolHelical.cpp
    VolFunction.h
    VolFunction.cpp
)
SET(observation_src
	Observation.h
	Observation.cpp
)
SOURCE_GROUP("Volume" FILES ${volume_src})
SOURCE_GROUP("Observation" FILES ${observation_src})
#处理ui和qrc文件
if (BUILD_QT5)
    QT5_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT5_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
else()
    QT4_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT4_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
endif()
SET(ChipicCommand_src
	main.cpp
	CommandObject.cpp
	CommandObject.h
	MarkGrid.cpp
	MarkGrid.h
	${UI_SRC}
	${MY_MOC_SRC}
	${MY_MOC_HDR}
	${Gui_QRC_SRCS}
	${volume_src}
	${observation_src}
)
#设置编译生成文件类型
add_executable(ChipicCommand ${ChipicCommand_src}) # 生成可执行文件
SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录

SET(CMAKE_RUNTIME_OUTPUT_DIRECTORYMY_DEBUG ${CMAKE_CURRENT_BINARY_DIR}/../../bin)
#add_library(common STATIC util.cpp) # 生成静态库
#add_library(common SHARED util.cpp) # 生成动态库或共享库
#add_library(ChipicCommand SHARED ${ChipicCommand_src})

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
target_link_libraries(ChipicCommand ${QT_LIB})
SET_BIN_DIR(ChipicCommand ChipicCommand) #设置文件输出目录
fc_wrap_cpp(MY_MOC_SRCS ${MY_MOC_HDR})
source_group("Properties" Files ${MY_MOC_SRCS})

SOURCE_GROUP("Uic" FILES ${Gui_UIC_HDRS})