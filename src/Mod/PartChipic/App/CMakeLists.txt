if(MSVC)
    add_definitions(-DFCAppPart -DHAVE_ACOSH -DHAVE_ASINH -DHAVE_ATANH)
else(MSVC)
    add_definitions(-DHAVE_LIMITS_H -DHAVE_CONFIG_H -DHAVE_ACOSH -DHAVE_ATANH -DHAVE_ASINH)
endif(MSVC)

FIND_PACKAGE( OpenMP REQUIRED) 
if(OPENMP_FOUND) 
message("OPENMP FOUND") 
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}") 
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}") 
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}") 
set(CMAKE_SHARE_LINKER_FLAGS "${CMAKE_SHARE_LINKER_FLAGS} ${OpenMP_SHARE_LINKER_FLAGS}") 
set(PartChipic_LIBS vcomp)
else(OPENMP_FOUND)
message ("Not found OpenMP")
endif()

include_directories(
	vcglib
	glew	
    ${CMAKE_BINARY_DIR}
    ${Boost_INCLUDE_DIRS}
    ${OCC_INCLUDE_DIR}
    ${ZLIB_INCLUDE_DIR}
    ${PYTHON_INCLUDE_DIRS}
    ${XercesC_INCLUDE_DIRS}
)
link_directories(${OCC_LIBRARY_DIR})

set(PartChipic_LIBS 
    Part
	PartGui
	Mesh
    FreeCADApp
)

SET(PartChipic_SRCS
    AppPartChipic.cpp
    AppPartChipicPy.cpp
	ChipicConst.h
	PM3mesh.h
	PM3mesh.cpp
	MathMod.h
	MathMod.cpp
	PM3Volume.h
	PM3Volume.cpp
	PM3VGrid.h
	PM3VGrid.cpp
	PM3VFunctional.h
	PM3VFunctional.cpp
	PreCompiled.h
	PreCompiled.cpp
)

SET(Core_SRCS
	core/ableglRender.h
	core/ableOut.h
	core/algebra.h
    core/src/basicmath.cpp
	core/basicmath.h
    core/src/basicstring.cpp
	core/basicstring.h
	core/src/createVolume.cpp
	core/createVolume.h
	core/src/DefValue.cpp
	core/DefValue.h
	core/grid.h
	core/src/grid.cpp
	core/Iso3D.h
	core/src/Iso3D.cpp
	core/IsoMatrix3D.h
	core/src/IsoMatrix3D.cpp
	core/Line.h
	core/src/Line.cpp
	core/pm3core.h
	core/paraDefine.h
	core/src/paraDefine.cpp
	core/src/pm3parser.cpp
	core/pm3parser.h
	core/src/Point.cpp
	core/Point.h
	core/render_state_gl.h
	core/src/rendersettings.cpp
	core/rendersettings.h
	core/src/system.cpp
	core/system.h
)

SET(MathMod_SRCS
	mathmod/pariso/objectparameters.h
	mathmod/pariso/objectparameters.cpp
	mathmod/pariso/commun.h
	mathmod/pariso/commun.cpp
	mathmod/pariso/isosurface/MIso3D.h
	mathmod/pariso/isosurface/MIso3D.cpp
	mathmod/ui_modules/ParisoMathObject.h
	mathmod/ui_modules/ParisoMathObject.cpp
	mathmod/ui_modules/parametersoptions.h
	mathmod/ui_modules/parametersoptions.cpp
	mathmod/json_parser/parisodef.h
	mathmod/json_parser/parisodef.cpp
	mathmod/json_parser/jpar.h
	mathmod/json_parser/jpar.cpp
	mathmod/json_parser/jiso.h
	mathmod/json_parser/jiso.cpp
	mathmod/pariso/isosurface/povfunctions.cpp
	mathmod/pariso/isosurface/povfunctions.h
	mathmod/fparser/fparser.hh
	mathmod/fparser/fparser.cc
)

SOURCE_GROUP("Chipic" FILES ${PartChipic_SRCS})
SOURCE_GROUP("Core" FILES ${Core_SRCS})
SOURCE_GROUP("MathMode" FILES ${MathMod_SRCS})

add_library(PartChipic SHARED ${PartChipic_SRCS} ${Core_SRCS} ${MathMod_SRCS})
target_link_libraries(PartChipic ${PartChipic_LIBS})
if(OPENMP_FOUND)
    target_link_libraries(PartChipic VCOMP.lib)
endif()

SET(PartChipic_Scripts
    Init.py
)
fc_target_copy_resource(PartChipic 
    ${CMAKE_SOURCE_DIR}/src/Mod/PartChipic
    ${CMAKE_BINARY_DIR}/Mod/PartChipic
	${PartChipic_Scripts})

SET_BIN_DIR(PartChipic PartChipic /Mod/PartChipic)
SET_PYTHON_PREFIX_SUFFIX(PartChipic)

INSTALL(TARGETS PartChipic DESTINATION ${CMAKE_INSTALL_LIBDIR})
