#include "ContourDataSetConstructor.h"
#include "DataVisualization/ContourData.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
namespace DV3D
{
	ContourDatasetConstructor::ContourDatasetConstructor():xGridSize(0), yGridSize(0), zGridSize(0)
	{

	}
	ContourDatasetConstructor::~ContourDatasetConstructor()
	{

	}
	vtkSmartPointer<vtkDataSet> ContourDatasetConstructor::creatDataset()
	{
		initData();
		vtkSmartPointer<vtkStructuredGrid> structuredGrid= vtkSmartPointer<vtkStructuredGrid>::New();
		structuredGrid->SetDimensions(xGridSize,yGridSize,zGridSize);
		structuredGrid->SetPoints(points);
		structuredGrid->GetPointData()->SetScalars(scaler);

		return structuredGrid;
	}
	bool isReisreversal(std::shared_ptr<DV::ContourData>& data)
	{
		bool isreversal = false;
		switch (data->getDirectionType())
		{
		case DV::DirectionType::X_Z:
		{
			if (data->getXTag() != "X")
				isreversal = true;
		}
		break;
		case DV::DirectionType::X_Y:
		{
			if (data->getXTag() != "X")
				isreversal = true;
		}
		break;
		case DV::DirectionType::Y_Z:
		{
			if (data->getXTag() != "Y")
				isreversal = true;
		}
		break;
		}
		return isreversal;
	}
	int judgeface(std::vector<float>& data)
	{
		for (auto i = 0; i < data.size() / 2; ++i)
		{
			if (data[i] == data[i + 3])
				return i;
		}
		return -1;
	}
	void ContourDatasetConstructor::createPointsXy() {
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		//添加坐标点
		bool ok = isReisreversal(data);
		points = vtkSmartPointer<vtkPoints>::New();
		scaler = vtkSmartPointer<vtkFloatArray>::New();
		std::map<float, float> xGridMap;
		std::map<float, float> yGridMap;
		if (ok)
		{
			for (auto i = 0; i < datas.size(); ++i)
			{
				points->InsertNextPoint(datas[i].x,datas[i].y, face[2]);
				scaler->InsertNextTuple1(datas[i].value);
				xGridMap[datas[i].x] = 1;
				yGridMap[datas[i].y] = 1;
			}
		}
		else
		{
			for (auto i = 0; i < datas.size(); ++i)
			{
				points->InsertNextPoint(datas[i].y,datas[i].x,face[2]);
				scaler->InsertNextTuple1(datas[i].value);
				xGridMap[datas[i].y] = 1;
				yGridMap[datas[i].x] = 1;
			}
		}
		xGridSize = xGridMap.size();
		yGridSize = yGridMap.size();
		zGridSize = 1;
	}
	void ContourDatasetConstructor::createPointsXz() {
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		//添加坐标点
		bool ok = isReisreversal(data);
		int x = 0, z = 0;
		ok ? (x = 1, z = 0) : (x = 0, z = 1);
		points = vtkSmartPointer<vtkPoints>::New();
		scaler = vtkSmartPointer<vtkFloatArray>::New();
		std::map<float, float> xGridMap;
		std::map<float, float> zGridMap;
		if (ok)
		{
			for (auto i = 0; i < datas.size(); ++i)
			{
				points->InsertNextPoint(datas[i].x, face[1], datas[i].y);
				scaler->InsertNextTuple1(datas[i].value);
				xGridMap[datas[i].x] = 1;
				zGridMap[datas[i].y] = 1;
			}
		}
		else
		{
			for (auto i = 0; i < datas.size(); ++i)
			{
				points->InsertNextPoint(datas[i].y, face[1], datas[i].x);
				scaler->InsertNextTuple1(datas[i].value);
				xGridMap[datas[i].y] = 1;
				zGridMap[datas[i].x] = 1;
			}
		}
		xGridSize = xGridMap.size();
		yGridSize = 1;
		zGridSize = zGridMap.size();
	}
	void ContourDatasetConstructor::createPointsYz() {
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		//添加坐标点
		bool ok = isReisreversal(data);
		points = vtkSmartPointer<vtkPoints>::New();
		scaler = vtkSmartPointer<vtkFloatArray>::New();
		std::map<float, float> yGridMap;
		std::map<float, float> zGridMap;
		if (ok)
		{
			for (auto i = 0; i < datas.size(); ++i)
			{
				points->InsertNextPoint(face[0],datas[i].x, datas[i].y);
				scaler->InsertNextTuple1(datas[i].value);
				yGridMap[datas[i].x] = 1;
				zGridMap[datas[i].y] = 1;
			}
		}
		else
		{
			for (auto i = 0; i < datas.size(); ++i)
			{
				points->InsertNextPoint(face[0],datas[i].y, datas[i].x);
				scaler->InsertNextTuple1(datas[i].value);
				yGridMap[datas[i].y] = 1;
				zGridMap[datas[i].x] = 1;
			}
		}
		xGridSize = 0;
		yGridSize = yGridMap.size();
		zGridSize = zGridMap.size();
	}
	void ContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		switch (data->getDirectionType())
		{
		case DV::DirectionType::X_Z:
			createPointsXz();
		break;
		case DV::DirectionType::X_Y:
			createPointsXy();
		break;
		case DV::DirectionType::Y_Z:
			createPointsYz();
		break;
		}
		return;
	}
};