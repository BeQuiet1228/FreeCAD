#include "particle3dActorPipeline.h"
#include <vtkActor.h>
#include <vtkProperty.h>
#include "vtkPolyData.h"
#include "../CustomConfig.h"
void DV3D::Particle3dActorPipeline::connect()
{
	CartesianStructActorPipeline::connect();
	auto actor = getActor();
	//actor->GetProperty()->SetColor(1, 0, 0);
	actor->GetProperty()->SetColor(colorf.r,colorf.g,colorf.b);
	actor->GetProperty()->SetPointSize(particleSize);
}

void DV3D::Particle3dActorPipeline::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto particleGroup = Group.getGroup("particle3d");
	auto colorStr = particleGroup.getGroup("particleColor").getValue("value");
	colorf=getColors(colorStr);
	auto particleSizeStr= particleGroup.getGroup("particleSize").getValue("value");
	particleSize = atof(particleSizeStr.c_str());
}
