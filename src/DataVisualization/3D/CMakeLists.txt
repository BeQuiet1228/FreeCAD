#设置项目名称
project(DataVisualization3D)
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
	${VTK_INCLUDE_DIRS}
)


#处理ui和qrc文件
if (BUILD_QT5)
    QT5_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT5_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
else()
    QT4_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT4_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
endif()

SET(SRC 
	main.cpp
	controler.cpp
	controler.h
	dataSetConstructor.cpp
	dataSetConstructor.h
	widget3D.cpp
	widget3D.h
	actorPipeline.cpp
	actorPipeline.h
	object.h
	object.cpp
	dataSetConstructorFactory.cpp
	dataSetConstructorFactory.h
)
SET( STRUCT_SRC
	CartesianStructDataSetConstructor.cpp
	CartesianStructDataSetConstructor.h
	PolarStructDataSetConstructor.cpp
	PolarStructDataSetConstructor.h
	CartesianStructActorPipeline.h
	CartesianStructActorPipeline.cpp
	CylinderStructDataSetConstructor.h
	CylinderStructDataSetConstructor.cpp
	PolarPlanConstruct.h
	PolarPlanConstruct.cpp
	CylinderPlanConstruct.h
	CylinderPlanConstruct.cpp
)

SET(DataVisualization3D_src
	${SRC}
	${STRUCT_SRC}
	)
	
source_group("src" FILES ${SRC})
source_group("struct" FILES ${STRUCT_SRC})
	
add_executable(DataVisualization3D ${DataVisualization3D_src})

#设置执行文件的输出目录
set(DEBUG_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(RELEASE_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

SET_BIN_DIR(DataVisualization3D DataVisualization3D)

#添加目录分类

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
	DataVisualization
	${VTK_LIBRARIES}
	)

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
#生成moc文件
fc_wrap_cpp(MY_MOC_SRCS ${MY_MOC_HDR})
target_link_libraries(DataVisualization3D ${QT_LIB})