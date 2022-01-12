#pragma once
#include "actorPipeline.h"
#include <vtkUnstructuredGridGeometryFilter.h>
#include <vtkSmartPointer.h>
#include <vtkPolyDataNormals.h>
#include "XmlGroup3D.h"
namespace DV3D {
	class CartesianStructActorPipeline :public ActorPipemline{
	public:
		CartesianStructActorPipeline();
		~CartesianStructActorPipeline();
	public:
		void update() override;
		void connect() override;
		virtual void loadConfig();
	protected:
		XmlData::ColorF colorf;
	};
}