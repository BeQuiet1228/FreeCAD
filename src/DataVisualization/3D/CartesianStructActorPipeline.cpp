#include "CartesianStructActorPipeline.h"
#include <vtkDataSetMapper.h>
#include <vtkProperty.h>
#include"vtk-7.0/vtkMapper.h"
DV3D::CartesianStructActorPipeline::CartesianStructActorPipeline()
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
	filter = vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();

	this->setActor(ac);
	this->setMapper(mp);
}

DV3D::CartesianStructActorPipeline::~CartesianStructActorPipeline()
{

}

void DV3D::CartesianStructActorPipeline::update()
{

}

void DV3D::CartesianStructActorPipeline::connect()
{
	auto data = getDataSet();
	filter->SetInputData(data);
	filter->MergingOn();
	filter->Update();

	auto mp = getMapper();
	mp->SetInputConnection(filter->GetOutputPort());
	mp->ScalarVisibilityOff();
	mp->Update();

	auto ac = getActor();
	ac->SetMapper(mp);
	ac->GetProperty()->EdgeVisibilityOn();
}

