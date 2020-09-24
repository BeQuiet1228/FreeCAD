/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU Library General Public License as       *
 *   published by the Free Software Foundation; either version 2 of the    *
 *   License, or (at your option) any later version.                       *
 *   for detail see the LICENCE text file.                                 *
 *   Jürgen Riegel 2002                                                    *
 *                                                                         *
 ***************************************************************************/
#include "PreCompiled.h"
#ifndef _PreComp_
# include <Python.h>
# include <Interface_Static.hxx>
# include <IGESControl_Controller.hxx>
# include <STEPControl_Controller.hxx>
# include <Standard_Version.hxx>
# include <OSD.hxx>
# include <sstream>
#endif

#include <Base/Console.h>
#include <Base/Interpreter.h>
#include <Base/Parameter.h>

#include <App/Application.h>


namespace PartChipic {
extern PyObject* initModule();
}

PyMOD_INIT_FUNC(PartChipic)
{
	try {
		Base::Interpreter().loadModule("Part");
		//Base::Interpreter().loadModule("Mesh");
	}
	catch (const Base::Exception& e) {
		PyErr_SetString(PyExc_ImportError, e.what());
		PyMOD_Return(0);
	}

    PyObject* partModule = PartChipic::initModule();
    Base::Console().Log("Loading PartChipic module... done\n");

    
    PyMOD_Return(partModule);
}
