#include "Vector3dActorPipeline.h"
#include "vtkPointData.h"
#include "vtkPolyDataMapper.h"
#include "../CustomConfig.h"
#include "QString"
#include "XmlGroup3D.h"
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
	colorfs.clear();
	XmlData::Vector3dXml xmlInfo;
	xmlInfo.loadXml();
	colorfs=XmlData::getColors(xmlInfo.colorBar.values.toVector()
	,xmlInfo.colorBar.colors.toVector());
	//colorfs = XmlData::getColors(xmlInfo.colorBar., xmlInfo.colorBar.colors);
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
		lookupTable->SetTableValue(i
			, colorfs[i].redF()
			, colorfs[i].greenF()
			, colorfs[i].blueF()
			, colorfs[i].alphaF());
	lookupTable->Build();
}
