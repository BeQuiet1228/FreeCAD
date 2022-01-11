#pragma once
#include "actorPipeline.h"
#include "vtkArrowSource.h"
#include "UnifyXmlConfig3D.h"
namespace DV3D
{
	class Vector3dActorPipeline:public ActorPipemline,public UnifyXmlConfig3D
	{
	public:
		Vector3dActorPipeline();
		~Vector3dActorPipeline();
	public:
		void update() override;
		void connect() override;
		void loadConfig();
	private:
		std::vector<float> values;
		std::vector<ColorF> colorfs;
	};
}