#设置项目名称
project(PartChipic)

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

#添加源文件与头文件
SET(PartChipic_src
	main.cpp
)

if(generate_exe)
	add_executable(PartChipic ${PartChipic_src}) # 生成可执行文件
	SET(OUTPUT_BINDIR ${CMAKE_CURRENT_BINARY_DIR}/../../bin) #设置可执行文件输出目录
endif()
if(generate_dll)
	add_library(PartChipic SHARED ${PartChipic_src})
endif()


#增加包含目录
include_directories(
    ${CMAKE_CURRENT_BINARY_DIR}
)
#增加外部库
list(APPEND PartChipic_LIB
	debug MSVCRTD.LIB
    debug MSVCPRTD.LIB
    optimized MSVCRT.LIB
    optimized MSVCPRT.LIB
	)

#链接静态库
target_link_libraries(PartChipic ${PartChipic_LIB})
SET_BIN_DIR(PartChipic PartChipic) #设置文件输出目录
