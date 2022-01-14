#include "CartesianStructActorPipeline.h"
#include <vtkDataSetMapper.h>
#include <vtkProperty.h>
#include"vtk-7.0/vtkMapper.h"
#include <vtkPolyDataNormals.h>
#include "../CustomConfig.h"
#include "XmlGroup3D.h"
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
	XmlData::Struct3dXml xmlInfo;
	XmlData::loadXmlInfo(xmlInfo);
	colorf = XmlData::getColors(xmlInfo.color);
	return;
}

