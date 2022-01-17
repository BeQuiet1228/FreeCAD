#include "particle3dActorPipeline.h"
#include <vtkActor.h>
#include <vtkProperty.h>
#include "vtkPolyData.h"
#include "../CustomConfig.h"

DV3D::Particle3dActorPipeline::Particle3dActorPipeline()
	:CartesianStructActorPipeline(), particleSize(1.0)
{
	loadConfig();
}

void DV3D::Particle3dActorPipeline::connect()
{
	CartesianStructActorPipeline::connect();
	auto actor = getActor();
	//actor->GetProperty()->SetColor(1, 0, 0);
	actor->GetProperty()->SetColor(colorf.redF(), colorf.greenF(), colorf.blueF());
	actor->GetProperty()->SetPointSize(particleSize);
}

void DV3D::Particle3dActorPipeline::loadConfig()
{
	XmlData::Particle3dXml xmlInfo;
	xmlInfo.loadXml();
	colorf = xmlInfo.particleColor.value;
	particleSize = xmlInfo.particleSize.value;
	if (particleSize < 0.000001f)
		particleSize = 1.0f;
	return;
}
