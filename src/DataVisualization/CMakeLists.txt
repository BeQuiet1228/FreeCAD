#添加子文件目录
add_subdirectory(qwt)
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
SET(QRC_SRC "")
SET(UI_SRC "")
SET(MY_MOC_HDR RenderThread.h
	RenderThreadManager.h
	Plot.h
	Canvas.h
	Axis.h
	ListTreeWidget.h
	Dataresource.h)

SET(TIME_SRC TimeData.h
	TimeData.cpp
	TimeRenderer.cpp
	TimeRenderer.h
)

SET(PARTICLE_SRC ParticleData.h
	ParticleData.cpp
	ParticleRenderer.h
	ParticleRenderer.cpp
)

SET(STRUCT_SRC StructRenderer.h
	StructRenderer.cpp
	structureData.h
	structureData.cpp)
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
)
SET(PHASOR_SRC phasorData.h
	phasorData.cpp
	phasorRenderer.h
	phasorRenderer.cpp
)
SET(CONFIG_SRC Config.cpp
	Config.h
	xml/pugiconfig.hpp
	xml/pugixml.cpp
	xml/pugixml.hpp)

SET(LISTTREE_SRC ListTreeWidget.h
	ListTreeWidget.cpp
	Dataresource.h
	Dataresource.cpp)
SET(SRC main.cpp
	Data.h
	Data.cpp
	Renderer.cpp
	Renderer.h
	Plot.cpp
	Plot.h
	Canvas.cpp
	Canvas.h
	Axis.cpp
	Axis.h
	RenderTask.cpp
	RenderTask.h
	RenderThreadManager.cpp
	RenderThreadManager.h
	RenderThread.cpp
	RenderThread.h
	RendererFactory.h
	RendererFactory.cpp
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
)
add_definitions(-DMY_DEBUG)
#设置编译生成文件类型
add_executable(DataVisualization ${DataVisualization_src}) # 生成可执行文件
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