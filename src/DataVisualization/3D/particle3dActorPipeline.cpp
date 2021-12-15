#include "particle3dActorPipeline.h"
#include <vtkActor.h>
#include <vtkProperty.h>
void DV3D::Particle3dActorPipeline::connect()
{
	CartesianStructActorPipeline::connect();
	auto actor = getActor();
	actor->GetProperty()->SetColor(1, 0, 0);
}

