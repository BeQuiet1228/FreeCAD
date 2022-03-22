#pragma once
#include"actorPipeline.h"
namespace DV3D
{
	class ContourActorPipeline :public ActorPipemline
	{
	public:
		ContourActorPipeline();
		~ContourActorPipeline();
	public:
		void update() override;
		void connect() override;
	private:
	};
}