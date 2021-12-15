#pragma once
#ifndef POLARPLANEACTORPIPELINE_H_
#define  POLARPLANEACTORPIPELINE_H_
#include"actorPipeline.h"
namespace DV3D
{
	class PolarPlaneActorPipeline:public ActorPipemline
	{
	public:
		PolarPlaneActorPipeline();
		~PolarPlaneActorPipeline();
	public :
		void update() override;
		void connect() override;
	};
};
#endif 
