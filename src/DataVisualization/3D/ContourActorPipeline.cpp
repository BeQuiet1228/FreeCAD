#include"ContourActorPipeline.h"
#include "vtkDataSetMapper.h"
#include "vtkActor.h"
#include "vtkPointData.h"
#include "vtkDataArray.h"
#include "vtkLookupTable.h"
#include"vtkProperty.h"
namespace DV3D
{
	ContourActorPipeline::ContourActorPipeline()
	{
		auto ac = vtkSmartPointer<vtkActor>::New();
		auto mp = vtkSmartPointer<vtkDataSetMapper>::New();
		this->setActor(ac);
		this->setMapper(mp);
	}
	ContourActorPipeline::~ContourActorPipeline()
	{

	}
	void ContourActorPipeline::update() {
		connect();
	}
	void ContourActorPipeline::connect() {
		auto dataset = getDataSet();
		auto mp = getMapper();
		/*********************************************/
		mp->SetInputDataObject(dataset);
		mp->SetScalarRange(dataset->GetPointData()->GetScalars()->GetRange());
		mp->Update();
		auto ac = getActor();
		ac->SetMapper(mp);
		//ac->GetProperty()->SetEdgeVisibility(1);
	}

	DV3D::XmlData::ControlerXml ContourActorPipeline::getControlerData()
	{
		XmlData::ControlerXml data;
		data.centerPoint=QVector3D(0,0,0);
		data.normalPoint = QVector3D(0.0, 0.0, 0.0);
		data.alpha = 1.0;
		data.clipEnable = 0;
		data.gridEnable = 0;
		return data;
	}

}
