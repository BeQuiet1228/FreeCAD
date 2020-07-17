#include "ContorlInterface.h"
#include "Contorl.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
#include <QString>
#include "MessageTransition.h"
#include "Chipic.h"
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
	return (contorl->contorlButtonBar);
}

ContorlDataBar * ContorlInterface::getContorlDataBar()
{
	return (contorl->contorlDataBar);
}

void ContorlInterface::setM3dPath(const std::string& path)
{
	contorl->m3dPath = path;
}

void ContorlInterface::senWinMessage(const int& type, const int& wParam, const int& lParam)
{
	if (contorl->chipicManager.CurrentChipic)
	{
		contorl->chipicManager.CurrentChipic->sendMessage(type, wParam, lParam);
	}
}

