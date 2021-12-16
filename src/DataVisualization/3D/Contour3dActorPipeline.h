#pragma once
#include "actorPipeline.h"
#include <vtkUnstructuredGridGeometryFilter.h>
#include "vtkSmartPointer.h"
#include "vtkPolyDataNormals.h"
namespace DV3D
{
	class  Contour3dActorPipline :public ActorPipemline {
	public:
		Contour3dActorPipline();
		~Contour3dActorPipline();
	public:
		void update() override;
		void connect() override;
	};
};