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
	actor->GetProperty()->SetColor(colorf.r, colorf.g, colorf.b);
	actor->GetProperty()->SetPointSize(particleSize);
}

void DV3D::Particle3dActorPipeline::loadConfig()
{
	XmlData::Particle3dXml xmlInfo;
	XmlData::loadXmlInfo(xmlInfo);
	colorf = XmlData::getColors(xmlInfo.particleColor);
	particleSize = xmlInfo.particleSize;
	if (particleSize < 0.000001f)
		particleSize = 1.0f;
	return;
}
