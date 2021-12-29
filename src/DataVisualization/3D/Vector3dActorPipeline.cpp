#include "Vector3dActorPipeline.h"
#include "vtkPointData.h"
#include "vtkPolyDataMapper.h"
DV3D::Vector3dActorPipeline::Vector3dActorPipeline()
{
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkPolyDataMapper>::New();
	this->setActor(ac);
	this->setMapper(mp);
	arrowSource = vtkSmartPointer<vtkArrowSource>::New();
	glyph = vtkSmartPointer<vtkGlyph3D>::New();
}

DV3D::Vector3dActorPipeline::~Vector3dActorPipeline()
{

}

void DV3D::Vector3dActorPipeline::update()
{
	connect();
}

void DV3D::Vector3dActorPipeline::connect()
{
	auto dataSet = getDataSet();
	//glyph->SetInputData(dataSet);
	//glyph->SetScaleFactor(0.1);//设置缩放因子
	//glyph->SetSourceConnection(arrowSource->GetOutputPort());
	//glyph->SetScaleModeToDataScalingOff(); //关闭随大小改变

	auto mp = getMapper();
	auto range = dataSet->GetPointData()->GetScalars()->GetRange();
	mp->SetScalarRange(range);
	//mp->SetInputConnection(glyph->GetOutputPort());
	mp->SetInputDataObject(dataSet);
	//mp->Update();

	//
	auto ac = getActor();
	ac->SetMapper(mp);
}