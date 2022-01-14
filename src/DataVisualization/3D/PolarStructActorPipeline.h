#pragma once
#ifndef POLAR_STRUCT_ACTOR_PIPELINE_H_
#define POLAR_STRUCT_ACTOR_PIPELINE_H_
#include"actorPipeline.h"
#include"vtkUnstructuredGridGeometryFilter.h"
#include "XmlGroup3D.h"
namespace DV3D
{
	class PolarStructActorPipeline:public ActorPipemline
	{
	public:
		PolarStructActorPipeline();
		~PolarStructActorPipeline();
	public:
		void update() override;
		void connect() override;
	protected:
		void loadConfig();
	private:
		vtkSmartPointer<vtkUnstructuredGridGeometryFilter> filter;
		//XmlData::ColorF colorf;
		DV::XmlData::XmlColor colorf;
	};
}

#endif