#include "PreCompiled.h"
#include "DocumentM3dMod.h"
#include <Base/Interpreter.h>
DocumentM3dMod::DocumentM3dMod()
{
	classID = 2;
}

DocumentM3dMod::~DocumentM3dMod()
{

}

bool DocumentM3dMod::save()
{
	bool re = Document::save();

	Base::InterpreterSingleton python;
	python.runString("FreeCADGui.runCommand('M3d_Save')");

	return true;
}

bool DocumentM3dMod::undo()
{
	bool re = Document::undo();
	/*lzg*/
	//Base::InterpreterSingleton python;
	this->recompute();
	this->flagNeedUpdateBoolean.setValue(0);
	//python.runString("DocumentTools.updateBoolean()");
	return re;
}

bool DocumentM3dMod::redo()
{
	bool re = Document::redo();
	/*lzg*/
	//Base::InterpreterSingleton python;
	this->recompute();
	this->flagNeedUpdateBoolean.setValue(0);
	//python.runString("DocumentTools.updateBoolean()");
	return re;
	
}

