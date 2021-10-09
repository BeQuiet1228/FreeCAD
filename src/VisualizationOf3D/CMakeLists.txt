project(VisualizationOf3D)

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
	${CMAKE_CURRENT_BINARY_DIR}
)
INCLUDE(${VTK_USE_FILE})

add_definitions(-D_VISUALZATION3D_)
SET(QRC_SRC "")
SET(UI_SRC "")
SET(MOC_SRC 
Widget3D.h
)

SET(DATAPROCESS_SRC
Widget3DFactory.h
Widget3DFactory.cpp
DataProcess.h
DataProcess.cpp
Widget3D.h
Widget3D.cpp
)

#处理ui和qrc文件
if(BUILD_QT5)
	QT5_ADD_RESOURCES(Gui_QRC_SRCs ${QRC_SRC})
	QT5_WRAP_UI(Gui_UIC_HDRs ${UI_SRC})
else()
	QT4_ADD_RESOURCES(Gui_QRC_SRCs ${QRC_SRC})
	QT4_WRAP_UI(Gui_UIC_HDRs ${UI_SRC})
endif()
SET(SRC
${UI_SRC}
${DATAPROCESS_SRC}
exPortConfig.hpp
main.cpp

)
if(VisualizationOf3DDLL)
add_definitions(-D_VISUALZATION3D_DLL)
add_library(VisualizationOf3D SHARED ${SRC})
else()
add_executable(VisualizationOf3D ${SRC})
endif()

#设置执行文件的输出目录
SET(DEBUG_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)
SET(RELEASE_MAIN_OUTPUT_PATH ${CMAKE_BINARY_DIR}/bin)

SET_BIN_DIR(VisualizationOf3D VisualizationOf3D)
list(APPEND NEED_LIBRARY
    debug MSVCRTD.LIB
    debug MSVCPRTD.LIB
    optimized MSVCRT.LIB
    optimized MSVCPRT.LIB
	HDF5Reader
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
fc_wrap_cpp(MY_MOC_SRCS ${MOC_SRC})
target_link_libraries(VisualizationOf3D ${NEED_LIBRARY} ${VTK_LIBRARIES})
source_group("dataprocess" FILES ${DATAPROCESS_SRC})