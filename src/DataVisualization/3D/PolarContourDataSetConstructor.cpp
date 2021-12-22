#include "PolarContourDataSetConstructor.h"
#include "DataVisualization/ContourDataPolar.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
#include "vtkPolyData.h"
#include "PolarContourFliter.h"
namespace DV3D
{
	PolarContourDatasetConstructor::PolarContourDatasetConstructor():rGridSize(1),thetaGridSize(1),zGridSize(1)
	{

	}
	PolarContourDatasetConstructor::~PolarContourDatasetConstructor()
	{

	}
	vtkSmartPointer<vtkDataSet> PolarContourDatasetConstructor::creatDataset()
	{
		initData();
		vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
		polyData->SetPoints(points);
		polyData->GetPointData()->SetScalars(scalar);
		vtkSmartPointer<PolarContourFilter> polarContourFliter = vtkSmartPointer<PolarContourFilter>::New();
		polarContourFliter->SetInputData(polyData);
		polarContourFliter->SetDimensions(rGridSize, thetaGridSize, zGridSize);
		polarContourFliter->SetRotation(30);
		polarContourFliter->Update();
		vtkSmartPointer<vtkStructuredGrid> structuredGrid = vtkSmartPointer<vtkStructuredGrid>::New();
		structuredGrid->SetDimensions(rGridSize, thetaGridSize, zGridSize);
		structuredGrid->SetPoints(points);
		structuredGrid->GetPointData()->SetScalars(scalar);
		return structuredGrid;
		//return polarContourFliter->GetOutput();
	}
	void PolarContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourDataPolar> data = std::shared_ptr<DV::ContourDataPolar>(DV::CreateContourDataPolar(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		points = vtkSmartPointer<vtkPoints>::New();
		scalar = vtkSmartPointer<vtkFloatArray>::New();
		float z;
		//根据坐标系判断
		(h5d.coordinateSystem == Hdf5Data::CoordinateSystem::CYLINDER) ?
			z = face[0] :
			z = face[2];
		for (auto i = 0; i < datas.size(); ++i)
		{
			float x = datas[i].x * cos(datas[i].y);
			float y = datas[i].x * sin(datas[i].y);
			points->InsertNextPoint(x, y, z);
			scalar->InsertNextTuple1(datas[i].value);
		}
		rGridSize = data->getWidth();
		thetaGridSize = data->getHeight();
		return;

	}
}