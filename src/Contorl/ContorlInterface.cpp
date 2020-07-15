#include "ContorlInterface.h"
#include "Contorl.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include <QString>
std::shared_ptr<ContorlInterface> ContorlInterface::_instance;
ContorlInterface::ContorlInterface()
{
	contorl = new Contorl;
}

ContorlInterface::~ContorlInterface()
{
	delete contorl;
}

ContorlButtonBar * ContorlInterface::getContorlButtonBar()
{
	return &(contorl->contorlButtonBar);
}

ContorlDataBar * ContorlInterface::getContorlDataBar()
{
	return &(contorl->contorlDataBar);
}

void ContorlInterface::setM3dPath(const std::string& path)
{
	auto temp = QString::fromStdString(path);

	temp.replace("FCStd", "m3d");

	contorl->m3dPath = temp.toStdString();
}

