#include "Contour3dActorPipeline.h"
#include "vtkDataSetMapper.h"
#include "vtkPointData.h"
#include "vtkCellData.h"
DV3D::Contour3dActorPipline::Contour3dActorPipline():
	scalarMin(0.0), scalarMax(1.0),contourSurfarCount(10)
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
	this->setActor(ac);
	this->setMapper(mp);
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
	auto dataset = getDataSet();
	//»ñÈ¡±ê³ß·¶Î§
	auto rang = dataset->GetPointData()->GetScalars()->GetRange();
	file->SetInputData(dataset);
	file->GenerateValues(contourSurfarCount,rang);
	file->Update();
	connectClipperToMapper(file->GetOutput());
	auto mp = getMapper();
	//mp->SetInputDataObject(file->GetOutput());
	mp->SetScalarRange(rang);
	mp->ScalarVisibilityOn();
	mp->Update();
	auto ac = getActor();
	ac->SetMapper(mp);
}

void DV3D::Contour3dActorPipline::setContourSurfarCount(const int& n)
{
	contourSurfarCount = n;
}

