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
	clipper.h
	clipper.cpp
	ControlerItem.cpp
	ControlerItem.h
	action.cpp
	action.h
	ControlerAction.cpp
	ControlerAction.h
	ControlerFactory.cpp
	ControlerFactory.h
	controlerItemFactor.cpp
	controlerItemFactor.h
	DataVisualization3DExport.hpp
	ClipPlaneWidget.h
	ClipPlaneWidget.cpp
	
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
	PolarStructActorPipeline.h
	PolarStructActorPipeline.cpp
)
SET(VECTOR3D_SRC
	CartesianVector3dDatasetConstructor.h
	CartesianVector3dDatasetConstructor.cpp
	CylinderVector3dDatasetConstructor.h
	CylinderVector3dDatasetConstructor.cpp
	Vector3dActorPipeline.h
	Vector3dActorPipeline.cpp
)
SET(PARTICLE_SRC 
	particle3dDataSetConstructor.cpp
	particle3dDataSetConstructor.h
	particle3dActorPipeline.cpp
	particle3dActorPipeline.h
)

SET(CONTOUR_SRCS
	ContourDataSetConstructor.h
	ContourDataSetConstructor.cpp
	ContourActorPipeline.h
	ContourActorPipeline.cpp
	PolarContourDataSetConstructor.h
	PolarContourDataSetConstructor.cpp
)
SET(CONTOUR3D_SRCS
	Contour3dataSetConstructor.cpp
	Contour3dataSetConstructor.h
	PolarContour3dDataSetConstructor.cpp
	PolarContour3dDataSetConstructor.h
	Contour3dActorPipeline.h
	Contour3dActorPipeline.cpp
	Contour3dControler.h
	Contour3dControler.cpp
	Contour3dControlerAction.h
	Contour3dControlerAction.cpp
	Contour3dControlerWidget.h
	Contour3dControlerWidget.cpp
)

SET(UI_SRC
	ControlerItem.ui
	ClipPlaneWidget.ui
	)

SET(MY_MOC_HDR
	ControlerItem.h
	ClipPlaneWidget.h
	Contour3dControlerWidget.h
	#Contour3dControlerAction.h
)
SET(QRC_SRC
	resource/rce.qrc
)

#生成moc文件
fc_wrap_cpp(MY_MOC_SRCS ${MY_MOC_HDR})


#处理ui和qrc文件
if(BUILD_QT5)
	QT5_ADD_RESOURCES(Gui_QRC_SRCs ${QRC_SRC})
	QT5_WRAP_UI(Gui_UIC_HDRs ${UI_SRC})
else()
	QT4_ADD_RESOURCES(Gui_QRC_SRCs ${QRC_SRC})
	QT4_WRAP_UI(Gui_UIC_HDRs ${UI_SRC})
endif()

SET(DataVisualization3D_src
	${SRC}
	${STRUCT_SRC}
	${UI_SRC}
	${MY_MOC_SRCS}
	${QRC_SRC}
	${Gui_QRC_SRCs}
	${PARTICLE_SRC}
	${CONTOUR_SRCS}
	${CONTOUR3D_SRCS}
	${VECTOR3D_SRC}
	)

	
source_group("src" FILES ${SRC})
source_group("struct" FILES ${STRUCT_SRC})
source_group("ui" FILES ${UI_SRC})
source_group("moc" FILES ${MY_MOC_SRCS})
source_group("resource" FILES ${Gui_QRC_SRCs} ${QRC_SRC})
source_group("particle3d" FILES ${PARTICLE_SRC})
source_group("contour" FILES ${CONTOUR_SRCS})
source_group("contour3d" FILES ${CONTOUR3D_SRCS})
source_group("vector3d" FILES ${VECTOR3D_SRC})
add_executable(DataVisualization3D ${DataVisualization3D_src})
add_definitions(-D_DATA_VISUALIZATION_3D)

#add_library(DataVisualization3D SHARED ${DataVisualization3D_src})
#设置执行文件的输出目录
set(DEBUG_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(RELEASE_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

SET_BIN_DIR(DataVisualization3D DataVisualization3D)


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

target_link_libraries(DataVisualization3D ${QT_LIB})