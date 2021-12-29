#pragma once
#include "actorPipeline.h"
#include "vtkArrowSource.h"
#include "vtkGlyph3D.h"
namespace DV3D
{
	class Vector3dActorPipeline:public ActorPipemline
	{
	public:
		Vector3dActorPipeline();
		~Vector3dActorPipeline();
	public:
		void update() override;
		void connect() override;
	private:
		vtkSmartPointer<vtkArrowSource> arrowSource;
		vtkSmartPointer<vtkGlyph3D> glyph;
	};
}