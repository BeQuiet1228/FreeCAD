#include "ContourDataSetConstructor.h"
#include "DataVisualization/ContourData.h"
#include "DataVisualization/ContourDataPolar.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
namespace DV3D
{
	ContourDatasetConstructor::ContourDatasetConstructor() :xGridSize(1), yGridSize(1), zGridSize(1)
	{

	}
	ContourDatasetConstructor::~ContourDatasetConstructor()
	{

	}
	vtkSmartPointer<vtkDataSet> ContourDatasetConstructor::creatDataset()
	{
		initData();
		vtkSmartPointer<vtkStructuredGrid> structuredGrid = vtkSmartPointer<vtkStructuredGrid>::New();
		structuredGrid->SetDimensions(xGridSize, yGridSize, zGridSize);
		structuredGrid->SetPoints(points);
		structuredGrid->GetPointData()->SetScalars(scaler);

		return structuredGrid;
	}
	void ContourDatasetConstructor::createPointsXy(std::vector<DV::ContourData::Grid>& datas, float z) {
		for (auto i = 0; i < datas.size(); ++i)
		{
			points->InsertNextPoint(datas[i].x, datas[i].y, z);
			scaler->InsertNextTuple1(datas[i].value);
		}
	}
	void ContourDatasetConstructor::createPointsXz(std::vector<DV::ContourData::Grid>& datas,float y) {
		for (auto i = 0; i < datas.size(); ++i)
		{
			points->InsertNextPoint(datas[i].x, y, datas[i].y);
			scaler->InsertNextTuple1(datas[i].value);
		}
	}
	void ContourDatasetConstructor::createPointsYz(std::vector<DV::ContourData::Grid>& datas,float x) {
		for (auto i = 0; i < datas.size(); ++i)
		{
			points->InsertNextPoint(x, datas[i].x, datas[i].y);
			scaler->InsertNextTuple1(datas[i].value);
		}
	}
	void ContourDatasetConstructor::createPointsRz(std::vector<DV::ContourData::Grid>& datas,float theta)
	{
		for (auto i = 0; i < datas.size(); ++i)
		{
			float x = datas[i].x * cos(theta);
			float y = datas[i].x * sin(theta);
			float z = datas[i].y;
			points->InsertNextPoint(x, y, z);
			scaler->InsertNextTuple1(datas[i].value);
		}
	}
	void ContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		//添加坐标点
		points = vtkSmartPointer<vtkPoints>::New();
		scaler = vtkSmartPointer<vtkFloatArray>::New();
		int x = 0, y = 1, z = 2;
		//角向时根据坐标系判断theta
		int theta = ((h5d.coordinateSystem == Hdf5Data::CoordinateSystem::CYLINDER) ?
			2 : 1);
		switch (data->getDirectionType())
		{
		case DV::DirectionType::X_Z:
		{
			createPointsXz(datas, face[y]);
			xGridSize = data->getWidth();
			zGridSize = data->getWidth();
		}
			break;
		case DV::DirectionType::X_Y:
		{
			createPointsXy(datas, face[z]);
			xGridSize = data->getWidth();
			yGridSize = data->getHeight();
		}
			break;
		case DV::DirectionType::Y_Z:
		{
			createPointsYz(datas, face[x]);
			yGridSize = data->getWidth();
			zGridSize = data->getHeight();
		}
			break;
		case DV::DirectionType::R_Z:
		{
			createPointsRz(datas, face[theta]);
			xGridSize = data->getWidth();
			zGridSize = data->getHeight();
		}
			break;
		}
		return;
	}
};