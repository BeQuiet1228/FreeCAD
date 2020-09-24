#-------------------------------------------------
#
# Project created by QtCreator 2015-04-16T13:29:25
#
#-------------------------------------------------

QT *= opengl
DEFINES += GLEW_STATIC
TARGET = core
TEMPLATE = lib
DESTDIR = ../bin
INCLUDEPATH *=  ../glew/include \
               ../vcglib \
                ../csg \


HEADERS += \
    pm3core.h \
    system.h \
    rendersettings.h \
    render_state_gl.h \
    Point.h \
    pm3parser.h \    
    paraDefine.h \
    Material.h \
    Line.h \
    Light.h \
    IsoMatrix3D.h \
    Iso3D.h \
    DefValue.h \
    basicstring.h \
    basicmath.h \
    algebra.h \
    ableOut.h \
    ableglRender.h \
    highlighter.h \
    createVolume.h \
    grid.h

SOURCES += \
    ../vcglib/wrap/ply/plylib.cpp \
    src/system.cpp \
    src/rendersettings.cc \
    src/Point.cpp \
    src/pm3parser.cpp \
    src/paraDefine.cpp \
    src/Material.cpp \
    src/Line.cpp \
    src/Light.cpp \
    src/IsoMatrix3D.cpp \
    src/Iso3D.cpp \
    src/DefValue.cpp \
    src/basicstring.cpp \
    src/basicmath.cpp \
    src/highlighter.cpp \
    src/createVolume.cpp \
    grid.cpp

build_pass:CONFIG(debug, debug|release) {
  TARGET = $$join(TARGET,,,d)
}

win32:CONFIG(release, debug|release): LIBS += ../bin/libopencsg.a
else:win32:CONFIG(debug, debug|release): LIBS += ../bin/libopencsgd.a

win32:CONFIG(release, debug|release): LIBS += ../bin/libglewlib.a
else:win32:CONFIG(debug, debug|release): LIBS += ../bin/libglewlibd.a
