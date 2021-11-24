#添加子文件目录
add_subdirectory(qwt)
add_subdirectory(3D)
#设置项目名称
project(DataVisualization)
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
	./qwt
	./qwt/polar
)
SET(QRC_SRC resource/rce.qrc)
SET(UI_SRC 
ConfigWidget.ui
realTimewidget.ui
)
SET(MY_MOC_HDR RenderThread.h
	RenderThreadManager.h
	Plot.h
	AxisLable.h
	Canvas.h
	Axis.h
	CombAxis.h
	ListTreeWidget.h
	Dataresource.h
	DoubleSilder.h
	ConfigWidget.h
	Arrowctrl.h
	ColorTab.h
	TLabel.h
	ColorMapWidget.h
	realTimewidget.h
	ScaleWidget.h
	rightScaleWidget.h
	ContourPlotAdapter.h
	phasorPlotAdapter.h
	PlotAdapter.h
	PlotAdapterNeedStruct.h
	)
SET(TIME_SRC TimeData.h
	TimeData.cpp
	TimeRenderer.cpp
	TimeRenderer.h
)
SET(CHAR_ENCODE C_encoding.cpp
	C_encoding.h)

SET(PARTICLE_SRC ParticleData.h
	ParticleData.cpp
	ParticleRenderer.h
	ParticleRenderer.cpp
)

SET(STRUCT_SRC 
	StructData.cpp
	StructData.h
	StructRender.cpp
	StructRender.h
	)
SET(STRUCT2D_SRC Struct2dRenderer.h
	Struct2dRenderer.cpp
	Struct2dData.h
	Struct2dData.cpp)
SET(INTERSPACE_SRC InterspaceData.h
	InterspaceData.cpp
	InterspaceRender.h
	InterspaceRender.cpp
)
SET(CONTOUR_SRC ContourData.h
	ContourData.cpp
	ContourRender.h
	ContourRender.cpp
	ContourRenderPolar.cpp
	ContourRenderPolar.h
	ContourDataPolar.cpp
	ContourDataPolar.h
	ContourRenderStateGetter.cpp
	ContourRenderStateGetter.h
	ContourPlotAdapter.cpp
	ContourPlotAdapter.h
)
SET(PHASOR_SRC phasorData.h
	phasorData.cpp
	phasorRenderer.h
	phasorRenderer.cpp
	DirData.cpp
	DirData.h
	phasorPlotAdapter.cpp
	phasorPlotAdapter.h
)
SET(CONFIG_SRC CustomConfig.cpp
	CustomConfig.h
	xml/pugiconfig.hpp
	xml/pugixml.cpp
	xml/pugixml.hpp)

SET(LISTTREE_SRC ListTreeWidget.h
	ListTreeWidget.cpp
	Dataresource.h
	Dataresource.cpp)
SET(AXIS_SRC
	Axis.cpp
	Axis.h
	AxisLable.cpp
	AxisLable.h
	CombAxis.cpp
	CombAxis.h
	)
SET(SRC main.cpp
	Data.h
	Data.cpp
	Renderer.cpp
	Renderer.h
	Plot.cpp
	Plot.h
	#AxisLable.h
	#AxisLable.cpp
	Canvas.cpp
	Canvas.h
	#Axis.cpp
	#Axis.h
	RenderTask.cpp
	RenderTask.h
	RenderThreadManager.cpp
	RenderThreadManager.h
	RenderThread.cpp
	RenderThread.h
	RendererFactory.h
	RendererFactory.cpp
	exportConfig.hpp
	RenderGrid.cpp
	RenderGrid.h
	DataInformationGetter.cpp
	DataInformationGetter.h
	PlotAdapter.cpp
	PlotAdapter.h
	PlotAdapterNeedStruct.h
	PlotAdapterNeedStruct.cpp
	)
SET(SRC_TOOL ConfigWidget.h
	ConfigWidget.cpp
	Arrowctrl.h
	Arrowctrl.cpp
	ColorTab.cpp
	ColorTab.h
	ColorMapWidget.h
	ColorMapWidget.cpp
	realTimewidget.cpp
	realTimewidget.h
	ScaleWidget.h
	ScaleWidget.cpp
	rightScaleWidget.h
	rightScaleWidget.cpp
	TLabel.h
	TLabel.cpp
	SysInfo.h
	SysInfo.cpp
	)
#处理ui和qrc文件
if (BUILD_QT5)
    QT5_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT5_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
else()
    QT4_ADD_RESOURCES(Gui_QRC_SRCS ${QRC_SRC})
    QT4_WRAP_UI(Gui_UIC_HDRS ${UI_SRC})
endif()
SET(DataVisualization_src
	${SRC}
	${UI_SRC}
	${PARTICLE_SRC}
	${TIME_SRC}
	${STRUCT_SRC}
	${INTERSPACE_SRC}
	${CONTOUR_SRC}
	${PHASOR_SRC}
	${PHASOR_SRC}
	${CONTOUR_SRC}
	${STRUCT2D_SRC}
	${LISTTREE_SRC}
	${CONFIG_SRC}
	${CHAR_ENCODE}
	${SRC_TOOL}
	${Gui_QRC_SRCS}
	${AXIS_SRC}
	)
add_definitions( -D_DATA_VISUALIZATION_)
if(DataVisualizationDll)
add_definitions(-DDATA_VISUALIZATIONG_DLL)
add_library(DataVisualization SHARED ${DataVisualization_src})
else()
#设置编译生成文件类型
add_executable(DataVisualization ${DataVisualization_src}) # 生成可执行文件
endif()

#设置执行文件的输出目录
set(DEBUG_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
set(RELEASE_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

SET_BIN_DIR(DataVisualization DataVisualization)

#添加目录分类
SOURCE_GROUP("src" FILES ${SRC})
SOURCE_GROUP("time" FILES ${TIME_SRC})
SOURCE_GROUP("particle" FILES ${PARTICLE_SRC})
SOURCE_GROUP("struct" FILES ${STRUCT_SRC})
SOURCE_GROUP("interspace" FILES ${INTERSPACE_SRC})
SOURCE_GROUP("contour" FILES ${CONTOUR_SRC})
SOURCE_GROUP("phasor" FILES ${PHASOR_SRC})
SOURCE_GROUP("contour" FILES ${CONTOUR_SRC})
SOURCE_GROUP("struct2d" FILES ${STRUCT2D_SRC})
SOURCE_GROUP("dataManage" FILES ${LISTTREE_SRC})
SOURCE_GROUP("config" FILES ${CONFIG_SRC})
SOURCE_GROUP("character_encoding" FILES ${CHAR_ENCODE})
SOURCE_GROUP("tool" FILES ${SRC_TOOL})
SOURCE_GROUP("uifile" FILES ${UI_SRC})
SOURCE_GROUP("qrcfile" FILES ${QRC_SRC})
SOURCE_GROUP("axis" FILES ${AXIS_SRC})
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
	qwt
	HDF5Reader
	qwt_polar
	)
if(VisualizationOf3DDLL)
list(APPEND QT_LIB
	VisualizationOf3D
	)
endif()

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
target_link_libraries(DataVisualization ${QT_LIB})