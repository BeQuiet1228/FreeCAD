#include "PolarContourDataSetConstructor.h"
#include "DataVisualization/ContourDataPolar.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
namespace DV3D
{
	PolarContourDatasetConstructor::PolarContourDatasetConstructor()
	{

	}
	PolarContourDatasetConstructor::~PolarContourDatasetConstructor()
	{

	}
	vtkSmartPointer<vtkDataSet> PolarContourDatasetConstructor::creatDataset()
	{
		initData();
		vtkSmartPointer<vtkStructuredGrid> structuredGrid = vtkSmartPointer<vtkStructuredGrid>::New();
		structuredGrid->SetDimensions(rGridSize, thetaGridSize, zGridSize);
		structuredGrid->SetPoints(points);
		structuredGrid->GetPointData()->SetScalars(scalar);
		return structuredGrid;
	}
	void PolarContourDatasetConstructor::createPointsRtheta()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		std::map<float, float> rGridMap;
		std::map<float, float> thetaGirdMap;
		std::map<float, float> zGridMap;
		points = vtkSmartPointer<vtkPoints>::New();
		scalar = vtkSmartPointer<vtkFloatArray>::New();
		for (auto i = 0; i < datas.size(); ++i)
		{
			float x = datas[i].x * cos(datas[i].y);
			float y = datas[i].x * sin(datas[i].y);
			float z = face[2];
			points->InsertNextPoint(x, y, z);
			scalar->InsertNextTuple1(datas[i].value);
			rGridMap[datas[i].x] = 1;
			thetaGirdMap[datas[i].y] = 1;
			zGridMap[z] = 1;
		}
		rGridSize = rGridMap.size();
		thetaGridSize = thetaGirdMap.size();
		zGridSize = zGridMap.size();
		return;
	}
	void PolarContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		createPointsRtheta();
		return;

	}
}