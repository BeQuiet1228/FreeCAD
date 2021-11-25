#include "actorPipeline.h"
#include <iostream>
#include <cassert>
DV3D::ActorPipemline::ActorPipemline()
	:actor(nullptr),mapper(nullptr),dataSet(nullptr)
{
	setObjectName("ActorPipeline");
}

DV3D::ActorPipemline::~ActorPipemline()
{

}

vtkSmartPointer<vtkActor> DV3D::ActorPipemline::getActor()
{
	assert(actor && "actor is nullptr!");
	return actor;
}

void DV3D::ActorPipemline::setActor(vtkSmartPointer<vtkActor> ac)
{
	this->actor = ac;
}

vtkSmartPointer<vtkMapper> DV3D::ActorPipemline::getMapper()
{
	assert(mapper && "mapper is nullptr!");
	return mapper;
}

void DV3D::ActorPipemline::setMapper(vtkSmartPointer<vtkMapper> mp)
{
	this->mapper = mp;
}

vtkSmartPointer<vtkDataSet> DV3D::ActorPipemline::getDataSet()
{
	assert(dataSet && "dataSet is nullptr");
	return dataSet;
}

void DV3D::ActorPipemline::setDataSet(vtkSmartPointer<vtkDataSet> dataset)
{
	this->dataSet = dataset;
}
