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
	lookupTable = vtkSmartPointer<vtkLookupTable>::New();
}

DV3D::Vector3dActorPipeline::~Vector3dActorPipeline()
{
	colorfs.clear();
}

void DV3D::Vector3dActorPipeline::update()
{
	loadConfig();
	connect();
}

void DV3D::Vector3dActorPipeline::connect()
{
	updataLookupTable();
	auto dataSet = getDataSet();
	auto mp = getMapper();
	auto range = dataSet->GetPointData()->GetScalars()->GetRange();
	mp->SetScalarRange(range);
	mp->SetInputDataObject(dataSet);
	mp->SetLookupTable(lookupTable);
	mp->Update();
	//
	auto ac = getActor();
	ac->SetMapper(mp);
}

void DV3D::Vector3dActorPipeline::loadConfig()
{

	std::vector <float> values;
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
	colorfs = getColors(values,colorfs);
}

void DV3D::Vector3dActorPipeline::updataLookupTable()
{
	auto dataSet = getDataSet();
	auto rang = dataSet->GetPointData()->GetScalars()->GetRange();
	//使用颜色过度
	lookupTable->SetTableRange(rang);
	//colors=getColors(values,colors);
	lookupTable->SetNumberOfTableValues(colorfs.size());
	for (auto i = 0; i < colorfs.size(); ++i)
		lookupTable->SetTableValue(i, colorfs[i].r, colorfs[i].g, colorfs[i].b, colorfs[i].a);
	lookupTable->Build();
}
