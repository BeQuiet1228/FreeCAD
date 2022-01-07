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

void DV3D::ControlerVisible::initState(std::shared_ptr<Controler> controler)
{
	if (controler->getVisible())
		on();
	else
		off();
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

void DV3D::ControlerEdgeVisible::initState(std::shared_ptr<Controler> controler)
{
	if (controler->getEdgeVisible())
		on();
	else
		off();
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

void DV3D::ControlerClipEnable::initState(std::shared_ptr<Controler> controler)
{
	if (controler->getClipEnable())
		on();
	else
		off();
}

void DV3D::ControlerClipPlan::active(std::shared_ptr<Controler> controler)
{
	showWidget(controler);
}

void DV3D::ControlerClipPlan::showWidget(std::shared_ptr<Controler> controler)
{
	ClipPlaneWidget* clipPlaneWidget = new ClipPlaneWidget();
	clipPlaneWidget->setModal(true);
	clipPlaneWidget->setControler(controler);
	clipPlaneWidget->show();
}
void DV3D::ControlerClipPlan::initState(std::shared_ptr<Controler> controler)
{
	on();
}

void DV3D::ControlerSave::active(std::shared_ptr<Controler> controler)
{

}

void DV3D::ControlerSave::initState(std::shared_ptr<Controler> controler)
{
	on();
}

void DV3D::ControlerSave::setHdf5Data(const Hdf5Data& data)
{
	this->hdf5data = data;
}

Hdf5Data DV3D::ControlerSave::getHdf5Data()
{
	return hdf5data;
}
