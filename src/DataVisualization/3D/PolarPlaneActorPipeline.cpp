#include "PolarPlaneActorPipeline.h"
#include "vtkDataSetMapper.h"
namespace DV3D
{
	PolarPlaneActorPipeline::PolarPlaneActorPipeline(){
		auto ac = vtkSmartPointer<vtkActor>::New();
		auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
		this->setActor(ac);
		this->setMapper(mp);
	}
	PolarPlaneActorPipeline::~PolarPlaneActorPipeline()	{

	}
	void PolarPlaneActorPipeline::update() {
	
	}
	void PolarPlaneActorPipeline::connect() {
	
	}
};