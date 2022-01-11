#include "Vector3dActorPipeline.h"
#include "vtkPointData.h"
#include "vtkPolyDataMapper.h"
#include "../CustomConfig.h"
#include "QString"
DV3D::Vector3dActorPipeline::Vector3dActorPipeline()
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkPolyDataMapper>::New();
	this->setActor(ac);
	this->setMapper(mp);
	loadConfig();
}

DV3D::Vector3dActorPipeline::~Vector3dActorPipeline()
{
	values.clear();
	colorfs.clear();
}

void DV3D::Vector3dActorPipeline::update()
{
	loadConfig();
	connect();
}

void DV3D::Vector3dActorPipeline::connect()
{
	auto dataSet = getDataSet();

	auto mp = getMapper();
	auto range = dataSet->GetPointData()->GetScalars()->GetRange();
	mp->SetScalarRange(range);
	mp->SetInputDataObject(dataSet);

	//
	auto ac = getActor();
	ac->SetMapper(mp);
}

void DV3D::Vector3dActorPipeline::loadConfig()
{
	values.clear();
	colorfs.clear();
	DV::Config::GetInstance()->loadConfig();
	auto group = DV::Config::GetInstance()->getRootGroup();
	auto valueNumberGroup = group.getGroup("vector3d").getGroup("valueNumber");
	int valueNumber =atoi(valueNumberGroup.getValue("value").c_str());
	values.reserve(valueNumber); colorfs.reserve(valueNumber);
	for (auto index = 0; index < valueNumber; ++index)
	{
		values.push_back(atof(valueNumberGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str()));
		colorfs.push_back(getColors(valueNumberGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("color")));
	}
}
