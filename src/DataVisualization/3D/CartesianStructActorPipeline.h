#pragma once
#include "actorPipeline.h"
#include <vtkUnstructuredGridGeometryFilter.h>
namespace DV3D {
	class CartesianStructActorPipeline :public ActorPipemline {
	public:
		CartesianStructActorPipeline();
		~CartesianStructActorPipeline();

	public:
		void update() override;
		void connect() override;
	};
}