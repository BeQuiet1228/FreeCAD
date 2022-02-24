#include "ControlerAction.h"
#include "controler.h"
#include <QFileDialog>
#include <QIcon>

DV3D::ControlerVisible::ControlerVisible()
{
	QIcon on(":/action/show.png");
	QIcon off(":/action/hide.png");
	setOnIcon(on);
	setOffIcon(off);
}

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

DV3D::ControlerEdgeVisible::ControlerEdgeVisible()
{
	QIcon on(":/action/grid_on.png");
	QIcon off(":/action/grid_off.png");
	setOnIcon(on);
	setOffIcon(off);
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

DV3D::ControlerClipEnable::ControlerClipEnable()
{
	QIcon on(":/action/cliper_on.png");
	QIcon off(":/action/cliper_off.png");
	setOnIcon(on);
	setOffIcon(off);
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

DV3D::ControlerClipPlan::ControlerClipPlan()
{
	QIcon on(":/action/cliper_face_setting.png");
	setOnIcon(on);
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

DV3D::ControlerSave::ControlerSave()
{
	QIcon on(":/action/save-as.png");
	setOnIcon(on);
}

void DV3D::ControlerSave::active(std::shared_ptr<Controler> controler)
{
	auto fileName = QFileDialog::getSaveFileName(0,
		"Save HDF5 Data", getPath(), "HDF5 Files (*.H5)");
	if (fileName.isEmpty())
		return;
	hdf5data.save(fileName.toStdString());
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

void DV3D::ControlerSave::setPath(const QString& pt)
{
	this->path = pt;
}

QString DV3D::ControlerSave::getPath()
{
	return path;
}
