#include "ControlerAction.h"
#include "controler.h"
void DV3D::ControlerVisible::active(std::shared_ptr<Controler> controler)
{
	if (getState() == ON)
	{
		off();
		controler->setVisible(false);
	}else {
		on();
		controler->setVisible(true);
	}
}

void DV3D::ControlerEdgeVisible::active(std::shared_ptr<Controler> controler)
{
	if (getState() == ON)
	{
		off();
		controler->setEdgeVisible(false);
	}
	else {
		on();
		controler->setEdgeVisible(true);
	}
}

void DV3D::ControlerClipEnable::active(std::shared_ptr<Controler> controler)
{
	if (getState() == ON)
	{
		off();
		controler->setClipEnable(false);
	}
	else {
		on();
		controler->setClipEnable(true);
	}
}

void DV3D::ControlerClipPlan::active(std::shared_ptr<Controler> controler)
{
	if (getState() == ON)
	{
		off();
	}
	else
	{
		on();
	}
}
