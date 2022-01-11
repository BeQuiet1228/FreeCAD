#include "CartesianStructActorPipeline.h"
#include <vtkDataSetMapper.h>
#include <vtkProperty.h>
#include"vtk-7.0/vtkMapper.h"
#include <vtkPolyDataNormals.h>
#include "../CustomConfig.h"
DV3D::CartesianStructActorPipeline::CartesianStructActorPipeline()
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();

	this->setActor(ac);
	this->setMapper(mp);
	loadConfig();
}

DV3D::CartesianStructActorPipeline::~CartesianStructActorPipeline()
{

}

void DV3D::CartesianStructActorPipeline::update()
{
	loadConfig();
	connect();
}

void DV3D::CartesianStructActorPipeline::connect()
{
	connectClipperToMapper(getDataSet());

	auto mp = getMapper();
	mp->ScalarVisibilityOff();
	mp->Update();

	auto ac = getActor();
	ac->SetMapper(mp);
	ac->GetProperty()->SetColor(colorf.r, colorf.g, colorf.b);
}

void DV3D::CartesianStructActorPipeline::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto structGroup = Group.getGroup("struct3d");
	auto colorStr = structGroup.getGroup("color").getValue("value");
	colorf = getColors(colorStr);
	return;
}

