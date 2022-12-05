#设置项目名称
project(FunctionShape)
add_compile_options(/bigobj)
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
    ${OCC_INCLUDE_DIR}
)

SET(SRC 
	main.cpp
	MyFunction.cpp
	MyFunction.h
	TestFunctionExport.h
	TestFunctionExport.cpp
	FunctionShape.cpp
	FunctionShape.h
	exprtk.hpp
	Function.cpp
	Function.h
)





	
source_group("src" FILES ${SRC})


#add_executable(FunctionShape  ${SRC})
add_definitions(-D_FUNCTION_SHAPE_)
add_library(FunctionShape SHARED ${SRC})

SET_BIN_DIR(FunctionShape FunctionShape)


#增加包含目录
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
	
)
#增加外部库
list(APPEND VTK_LIB
    debug MSVCRTD.LIB
    debug MSVCPRTD.LIB
    optimized MSVCRT.LIB
    optimized MSVCPRT.LIB
	${VTK_LIBRARIES}
    ${OCC_LIBRARIES}
    ${OCC_DEBUG_LIBRARIES}
	)

target_link_libraries(FunctionShape ${VTK_LIB})