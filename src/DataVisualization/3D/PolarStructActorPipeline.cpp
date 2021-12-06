#include"PolarStructActorPipeline.h"
#include"vtkDataSetMapper.h"
#include"vtkProperty.h"
#include"vtk-7.0/vtkMapper.h"
#include"vtkPolyDataNormals.h"
DV3D::PolarStructActorPipeline::PolarStructActorPipeline() {
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
	filter = vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();

	this->setActor(ac);
	this->setMapper(mp);
}
DV3D::PolarStructActorPipeline::~PolarStructActorPipeline()
{

}
void DV3D::PolarStructActorPipeline::update() {

}
void DV3D::PolarStructActorPipeline::connect() {

	vtkSmartPointer<vtkPolyDataNormals> normfilter = vtkSmartPointer<vtkPolyDataNormals>::New();
	auto data = getDataSet();

	filter->SetInputData(data);
	filter->MergingOn();
	filter->Update();

	auto mp = getMapper();
	mp->SetInputConnection(filter->GetOutputPort());
	mp->ScalarVisibilityOff();
	mp->Update();

	auto ac = getActor();
	ac->SetMapper(mp);
	ac->GetProperty()->EdgeVisibilityOn();
}
