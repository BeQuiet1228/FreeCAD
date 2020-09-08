#设置项目名称
project(HDF5Reader)

#设置生成工程类型
SET(generate_exe " ")
#SET(generate_dll " ")

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


SET(HDF5Reader_src
	hdf5io.h
	hdf5io.cpp
	main.cpp
)

if(generate_exe)
	add_definitions(-D_CONTORL_ -DMY_DEBUG -DMY_LOG -DSERVICE -DH5_BUILT_AS_DYNAMIC_LIB)
	add_executable(HDF5Reader ${HDF5Reader_src}) # 生成可执行文件
	SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录
endif()
if(generate_dll)
	add_definitions(-D_CONTORL_ -DMY_LOG -DH5_BUILT_AS_DYNAMIC_LIB)
	add_library(HDF5Reader SHARED ${HDF5Reader_src})
endif()


#增加包含目录
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
)
#增加外部库
list(APPEND HDF5Reader_LIB
	debug MSVCRTD.LIB
    debug MSVCPRTD.LIB
    optimized MSVCRT.LIB
    optimized MSVCPRT.LIB
	debug hdf5_D.lib
	debug hdf5_cpp_D.lib
	debug zlibd.lib
	debug zlibstaticd.lib
	optimized hdf5.lib
	optimized hdf5_cpp.lib
	optimized zlib.lib
	optimized zlibstatic.lib
	)

#链接静态库
target_link_libraries(HDF5Reader ${HDF5Reader_LIB})
SET_BIN_DIR(HDF5Reader HDF5Reader) #设置文件输出目录
