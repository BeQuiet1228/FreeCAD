#include "ContourDataSetConstructor.h"
#include "DataVisualization/ContourData.h"
#include "DataVisualization/ContourDataPolar.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
DV3D::ContourDatasetConstructor::ContourDatasetConstructor() :xGridSize(1), yGridSize(1), zGridSize(1),isNeg(false)
{

}
DV3D::ContourDatasetConstructor::~ContourDatasetConstructor()
{

}
vtkSmartPointer<vtkDataSet> DV3D::ContourDatasetConstructor::creatDataset()
{
	initData();
	vtkSmartPointer<vtkStructuredGrid> structuredGrid = vtkSmartPointer<vtkStructuredGrid>::New();
	structuredGrid->SetDimensions(xGridSize, yGridSize, zGridSize);
	structuredGrid->SetPoints(points);
	structuredGrid->GetPointData()->SetScalars(scaler);

	return structuredGrid;
}
void DV3D::ContourDatasetConstructor::createPointsXy(std::vector<DV::ContourData::Grid>& datas, float z) {
	for (auto i = 0; i < datas.size(); ++i)
	{
		points->InsertNextPoint(datas[i].x, datas[i].y, z);
		scaler->InsertNextTuple1(datas[i].value);
	}
}
void DV3D::ContourDatasetConstructor::createPointsXz(std::vector<DV::ContourData::Grid>& datas, float y) {
	for (auto i = 0; i < datas.size(); ++i)
	{
		points->InsertNextPoint(datas[i].x, y, datas[i].y);
		scaler->InsertNextTuple1(datas[i].value);
	}
}
void DV3D::ContourDatasetConstructor::createPointsYz(std::vector<DV::ContourData::Grid>& datas, float x) {
	for (auto i = 0; i < datas.size(); ++i)
	{
		points->InsertNextPoint(x, datas[i].x, datas[i].y);
		scaler->InsertNextTuple1(datas[i].value);
	}
}
void DV3D::ContourDatasetConstructor::createPointsRz(std::vector<DV::ContourData::Grid>& datas, float theta)
{
	//grid和网格长宽做过处理，不需要做颠倒。
	for (auto i = 0; i < datas.size(); ++i)
	{
		float x = datas[i].y * cos(theta);
		float y =datas[i].y * sin(theta);
		float z = datas[i].x;
		points->InsertNextPoint(x, y, z);
		scaler->InsertNextTuple1(datas[i].value);
	}
}
bool isNegation(std::shared_ptr<DV::ContourData>& data)
{
	switch (data->getDirectionType())
	{
	case DV::DirectionType::X_Z:
	{
		if (data->getYTag() != "X")
			return true;
	}
	case DV::DirectionType::X_Y:
	{
		if (data->getYTag() != "Y")
			return true;
	}
	case DV::DirectionType::Y_Z:
	{
		if (data->getYTag() != "Z")
			return true;
	}
	case DV::DirectionType::R_Z:
		if (data->getXTag() != "R")
			return true;
	}
	return false;
}
void DV3D::ContourDatasetConstructor::setGridSize(int xGrid, int yGrid, int zGrid)
{
	xGridSize = xGrid;
	yGridSize = yGrid;
	zGridSize = zGrid;
}
void DV3D::ContourDatasetConstructor::initData()
{
	auto h5d = getHdf5Data();
	std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
	data->loadPoint();
	auto datas = data->getGrids();
	auto face = data->getStructFace();
	//判断坐标系是否颠倒
	//isNeg=isNegation(data);
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
		setGridSize(data->getHeight(), 1, data->getWidth());
	}
	break;
	case DV::DirectionType::X_Y:
	{
		createPointsXy(datas, face[z]);
		setGridSize(data->getHeight(), data->getWidth(), 1);
	}
	break;
	case DV::DirectionType::Y_Z:
	{
		createPointsYz(datas, face[x]);
		setGridSize(1, data->getHeight(), data->getWidth());
	}
	break;
	case DV::DirectionType::R_Z:
	{
		createPointsRz(datas, face[theta]);
		setGridSize(data->getWidth(), 1, data->getHeight());
	}
	break;
	}
	return;
}
