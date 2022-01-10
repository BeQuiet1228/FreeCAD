#include "Vector3dActorPipeline.h"
#include "vtkPointData.h"
#include "vtkPolyDataMapper.h"
DV3D::Vector3dActorPipeline::Vector3dActorPipeline()
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkPolyDataMapper>::New();
	this->setActor(ac);
	this->setMapper(mp);
}

DV3D::Vector3dActorPipeline::~Vector3dActorPipeline()
{

}

void DV3D::Vector3dActorPipeline::update()
{
	connect();
}

void DV3D::Vector3dActorPipeline::connect()
{
	auto dataSet = getDataSet();
	auto mp = getMapper();
	auto range = dataSet->GetPointData()->GetScalars()->GetRange();
	mp->SetScalarRange(range);
	mp->SetInputDataObject(dataSet);

	//
	auto ac = getActor();
	ac->SetMapper(mp);
}