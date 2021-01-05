#include "PreCompiled.h"
#include "DocumentM2dMod.h"
#include <Base/Interpreter.h>
bool DocumentM2dMod::save()
{
	bool re = Document::save();

	Base::InterpreterSingleton python;
	python.runString("FreeCADGui.runCommand('M2d_Save')");

	return true;
}

bool DocumentM2dMod::undo()
{
	bool re = Document::undo();

	Base::InterpreterSingleton python;
	python.runString("FreeCADGui.runCommand('CreateM2D')");

	return true;
}

bool DocumentM2dMod::redo()
{
	bool re = Document::redo();

	Base::InterpreterSingleton python;
	python.runString("FreeCADGui.runCommand('CreateM2D')");

	return true;
}

