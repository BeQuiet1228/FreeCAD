#include "Contour3dActorPipeline.h"
#include "vtkDataSetMapper.h"
DV3D::Contour3dActorPipline::Contour3dActorPipline()
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
	this->setActor(ac);
	this->setMapper(mp);
}

DV3D::Contour3dActorPipline::~Contour3dActorPipline()
{

}

void DV3D::Contour3dActorPipline::update()
{
	connect();
}

void DV3D::Contour3dActorPipline::connect()
{
	connectClipperToMapper(getDataSet());
	auto mp = getMapper();
	mp->SetScalarModeToUseCellData();
	mp->Update();

	auto ac = getActor();
	ac->SetMapper(mp);
}

