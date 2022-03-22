#pragma once
#include "CartesianStructActorPipeline.h"
namespace DV3D {
	class Particle3dActorPipeline :public CartesianStructActorPipeline{
	public:
		Particle3dActorPipeline();
		~Particle3dActorPipeline() = default;
	public:
		void connect() override;
	protected:
		virtual void loadConfig();
	private:
		double particleSize;
	};
}