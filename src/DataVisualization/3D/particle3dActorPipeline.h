#pragma once
#include "CartesianStructActorPipeline.h"
namespace DV3D {
	class Particle3dActorPipeline :public CartesianStructActorPipeline {
	public:
		Particle3dActorPipeline() = default;
		~Particle3dActorPipeline() = default;
	public:
		void connect() override;
	};
}