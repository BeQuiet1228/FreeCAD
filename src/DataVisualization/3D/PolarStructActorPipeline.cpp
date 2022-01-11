#include"PolarStructActorPipeline.h"
#include"vtkDataSetMapper.h"
#include"vtkProperty.h"
#include"vtk-7.0/vtkMapper.h"
#include"vtkPolyDataNormals.h"
#include "../CustomConfig.h"
DV3D::PolarStructActorPipeline::PolarStructActorPipeline() {
	auto ac = vtkSmartPointer<vtkActor>::New();
	auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
	filter = vtkSmartPointer<vtkUnstructuredGridGeometryFilter>::New();

	this->setActor(ac);
	this->setMapper(mp);
	loadConfig();
}
DV3D::PolarStructActorPipeline::~PolarStructActorPipeline()
{

}
void DV3D::PolarStructActorPipeline::update() {
	loadConfig();
	connect();
}
void DV3D::PolarStructActorPipeline::connect() {

	vtkSmartPointer<vtkPolyDataNormals> normfilter = vtkSmartPointer<vtkPolyDataNormals>::New();
	auto data = getDataSet();

	filter->SetInputData(data);
	filter->MergingOn();
	filter->Update();

	connectClipperToMapper(filter->GetOutputPort());
	auto mp = getMapper();
	mp->ScalarVisibilityOff();
	mp->Update();

	auto ac = getActor();
	ac->SetMapper(mp);
}

void DV3D::PolarStructActorPipeline::loadConfig()
{
	DV::Config::GetInstance()->loadConfig();
	auto Group = DV::Config::GetInstance()->getRootGroup();
	auto structGroup = Group.getGroup("struct3d");
	auto colorStr = structGroup.getGroup("color").getValue("value");
	auto colorf = getColors(colorStr);
	return;
}

