#include "ContorlInterface.h"
#include "Contorl.h"
#include "ContorlDataBar.h"
#include "ContorlButtonBar.h"
ContorlInterface::ContorlInterface()
{
	contorl = new Contorl;
}

ContorlInterface::~ContorlInterface()
{
	delete contorl;
}

void * ContorlInterface::getContorlButtonBar()
{
	return &(contorl->contorlButtonBar);
}

void * ContorlInterface::getContorlDataBar()
{
	return &(contorl->contorlDataBar);
}

