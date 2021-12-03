#include "CartesianStructActorPipeline.h"
#include <vtkDataSetMapper.h>
#include <vtkProperty.h>
#include"vtk-7.0/vtkMapper.h"
DV3D::CartesianStructActorPipeline::CartesianStructActorPipeline()
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();

	this->setActor(ac);
	this->setMapper(mp);
}

DV3D::CartesianStructActorPipeline::~CartesianStructActorPipeline()
{

}

void DV3D::CartesianStructActorPipeline::update()
{
	connect();
}

void DV3D::CartesianStructActorPipeline::connect()
{
	connectClipperToMapper(getDataSet());
	auto mp = getMapper();
	mp->ScalarVisibilityOff();
	mp->Update();

	auto ac = getActor();
	ac->SetMapper(mp);
}

