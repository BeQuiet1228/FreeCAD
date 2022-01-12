#include "PreCompiled.h"
#include "DocumentH5.h"

App::DocumentH5::DocumentH5()
{
	classID = 5;
}

App::DocumentH5::~DocumentH5()
{

}

void App::DocumentH5::Save(Base::Writer& writer) const
{

}

bool App::DocumentH5::save()
{
	return true;
}

bool App::DocumentH5::undo()
{
	return true;
}

bool App::DocumentH5::redo()
{
	return true;
}

void App::DocumentH5::loadHdf5File(const std::string& path)
{
	hdff5IO.reset(new Hdf5IO(path));
	hdff5IO->initHdf5Data();
}

std::shared_ptr<Hdf5IO> App::DocumentH5::getHdf5IO()
{
	return hdff5IO;
}

