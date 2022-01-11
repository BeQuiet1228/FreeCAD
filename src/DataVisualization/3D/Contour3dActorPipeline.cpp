#include "Contour3dActorPipeline.h"
#include "vtkDataSetMapper.h"
#include "vtkPointData.h"
#include "vtkCellData.h"
#include "cassert"
#include "../CustomConfig.h"
#include "QString"
DV3D::Contour3dActorPipline::Contour3dActorPipline() :contourSurfarCount(10), isInit(false)
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
	this->setActor(ac);
	this->setMapper(mp);
	rang.valMin = 0.0f;
	rang.valMax = 1.0f;
	file = vtkSmartPointer<vtkContourFilter>::New();
	normal = vtkSmartPointer<vtkPolyDataNormals>::New();
	loadConfig();
}

DV3D::Contour3dActorPipline::~Contour3dActorPipline()
{

}

void DV3D::Contour3dActorPipline::update()
{
	loadConfig();
	connect();
}

void DV3D::Contour3dActorPipline::connect()
{
	initFilter();
	normal->SetInputConnection(file->GetOutputPort());
	normal->ComputeCellNormalsOff();
	normal->ComputePointNormalsOn();
	normal->SetSplitting(0);
	normal->SetAutoOrientNormals(1);
	normal->SetFeatureAngle(30);
	normal->Update();
	connectClipperToMapper(normal->GetOutput());
	auto mp = getMapper();
	mp->SetScalarRange(rang.valMin,rang.valMax);
	mp->ScalarVisibilityOn();
	mp->Update();
	auto ac = getActor();
	ac->SetMapper(mp);
}

void DV3D::Contour3dActorPipline::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto contour3dGroup = Group.getGroup("contour3d");
	auto valueNumberGroup = contour3dGroup.getGroup("valueNumber");
	auto valueNumber = atoi(valueNumberGroup.getValue("value").c_str());
	values.clear(); values.reserve(valueNumber);
	colors.clear(); colors.reserve(valueNumber);
	for (auto index=0;index<valueNumber;++index)
	{
		values.push_back(atof(valueNumberGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("value").c_str()));
		colors.push_back(getColors(valueNumberGroup.getGroup(QString("level_%1").arg(index).toStdString()).getValue("color")));
	}
}
void DV3D::Contour3dActorPipline::setContourSurfarCount(const int& n)
{
	contourSurfarCount = n;
}



/**
* @time	2021/12/21
* @brief DV3D::Contour3dActorPipline::getContourValues 获取等值面信息
* @return std::vector<DV3D::ContourValue>
*/
std::vector<DV3D::ContourValue> DV3D::Contour3dActorPipline::getContourValues()
{
	//获取设置的等值面信息
	auto contourCount=file->GetNumberOfContours();
	auto valueFs=file->GetValues();
	std::vector<ContourValue> valuelist;
	valuelist.reserve(contourCount);
	for (auto i=0;i<contourCount;++i)
		valuelist.push_back(valueFs[i]);
	return valuelist;
}


/**
* @time	2021/12/21
* @brief DV3D::Contour3dActorPipline::setContourValues 设置等值面
* @param std::vector<ContourValue> & values
* @return void
*/
void DV3D::Contour3dActorPipline::setContourValues(std::vector<ContourValue>& values)
{
	file->SetNumberOfContours(values.size());
	for (auto index=0;index<values.size();index++)
		file->SetValue(index,values[index]);
	file->SetComputeNormals(0);
	file->SetComputeGradients(0);
	file->Update();
	isInit = true;
}


double* DV3D::Contour3dActorPipline::getScalarRang()
{
	auto dataset = getDataSet();
	return dataset->GetPointData()->GetScalars()->GetRange();
}

void DV3D::Contour3dActorPipline::initFilter()
{
	if (isInit)
		return;
	auto contourData = getDataSet();
	file->SetInputData(contourData);
	auto rangs = contourData->GetPointData()->GetScalars()->GetRange();
	rang.valMin = rangs[0];
	rang.valMax = rangs[1];
	file->GenerateValues(contourSurfarCount,rangs);
	file->SetComputeNormals(0);
	file->SetComputeGradients(0);
	file->Update();
	isInit = true;
}
