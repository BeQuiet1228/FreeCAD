#include "Contour3dActorPipeline.h"
#include "vtkDataSetMapper.h"
#include "vtkPointData.h"
#include "vtkCellData.h"
#include "cassert"
DV3D::Contour3dActorPipline::Contour3dActorPipline() :contourSurfarCount(10), ishavescalar(false)
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
	this->setActor(ac);
	this->setMapper(mp);
	rang.valMin = 0.0f;
	rang.valMax = 1.0f;
	file = vtkSmartPointer<vtkContourFilter>::New();
}

DV3D::Contour3dActorPipline::~Contour3dActorPipline()
{

}

void DV3D::Contour3dActorPipline::update()
{
	connect();
}

void DV3D::Contour3dActorPipline::connect()
{
	updateFilter();
	connectClipperToMapper(file->GetOutput());
	auto mp = getMapper();
	mp->SetScalarRange(rang.valMin,rang.valMax);
	mp->ScalarVisibilityOn();
	mp->Update();
	auto ac = getActor();
	ac->SetMapper(mp);
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
	auto contour3dData = getDataSet();
	assert(contour3dData && "contour3dData is nullptr");
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
	file->RemoveAllInputs();
	file->SetInputData(getDataSet());
	//
	for (auto index=0;index<values.size();index++)
		file->SetValue(index,values[index]);
	file->Update();
	ishavescalar = true;
}


void DV3D::Contour3dActorPipline::updateFilter()
{
	if (ishavescalar)
		return;
	auto contourData = getDataSet();
	file->SetInputData(contourData);
	auto rangs = contourData->GetPointData()->GetScalars()->GetRange();
	rang.valMin = rangs[0];
	rang.valMax = rangs[1];
	file->GenerateValues(contourSurfarCount,rangs);
	file->Update();
	ishavescalar = true;
}
