#include "actorPipeline.h"
#include <iostream>
#include <cassert>
#include "clipper.h"
DV3D::ActorPipemline::ActorPipemline()
	:actor(nullptr),mapper(nullptr),dataSet(nullptr),clipperEnable(false)
{
	setObjectName("ActorPipeline");

	clipper.reset(new Clipper());
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

bool DV3D::ActorPipemline::getClipperEnable()
{
	return clipperEnable;
}

void DV3D::ActorPipemline::setClipperEnable(const bool& b)
{
	clipperEnable = b;
}

void DV3D::ActorPipemline::setClipper(std::shared_ptr<Clipper> clipper)
{
	this->clipper = clipper;
}


void DV3D::ActorPipemline::getClipPlane(vtkSmartPointer<vtkPlane>& palne)
{
	clipper->getClipPlane(palne);
}

void DV3D::ActorPipemline::setClipPlane(vtkSmartPointer<vtkPlane> plane)
{
	clipper->setClipPlane(plane);
}
/**
* @brief DV3D::ActorPipemline::connectClipperToMapper 将数据连接到剪切器，然后将剪切器的输出连接到映射器中。
*  如果剪切器的状态为不可用，那么会直接把输入数据连接到映射器
* @param vtkAlgorithmOutput * input 需要剪切的数据
* @return void
*/
void DV3D::ActorPipemline::connectClipperToMapper(vtkAlgorithmOutput* input)
{
	if (!getClipperEnable())
	{
		auto mapper = getMapper();
		mapper->SetInputConnection(input);
		return;
	}
	clipper->setInputConnection(input);
	auto mapper = getMapper();
	mapper->SetInputConnection(clipper->getOutpuPort());
}

/**
* @brief DV3D::ActorPipemline::connectClipperToMapper  将数据连接到剪切器，然后将剪切器的输出连接到映射器中。
* @param vtkDataObject * data
* @return void
*/
void DV3D::ActorPipemline::connectClipperToMapper(vtkDataObject* data)
{
	if (!getClipperEnable())
	{
		auto mapper = getMapper();
		mapper->SetInputDataObject(data);
		return;
	}
	
	clipper->setInputData(data);
	auto mapper = getMapper();
	mapper->SetInputConnection(clipper->getOutpuPort());
}
