#pragma once
#include "actorPipeline.h"
#include <vtkUnstructuredGridGeometryFilter.h>
#include <vtkSmartPointer.h>
#include <vtkPolyDataNormals.h>
#include "UnifyXmlConfig3D.h"
namespace DV3D {
	class CartesianStructActorPipeline :public ActorPipemline, public UnifyXmlConfig3D {
	public:
		CartesianStructActorPipeline();
		~CartesianStructActorPipeline();
	public:
		void update() override;
		void connect() override;
		virtual void loadConfig();
	protected:
		ColorF colorf;
	};
}