#include "PolarContourDataSetConstructor.h"
#include "DataVisualization/ContourDataPolar.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
#include "vtkPolyData.h"
#include "PolarContourFliter.h"
#include "vtkMath.h"
DV3D::PolarContourDatasetConstructor::PolarContourDatasetConstructor() :rGridSize(1), thetaGridSize(1), zGridSize(1)
{
	setResolution(40);
}
DV3D::PolarContourDatasetConstructor::~PolarContourDatasetConstructor()
{

}
vtkSmartPointer<vtkDataSet> DV3D::PolarContourDatasetConstructor::creatDataset()
{
	initData();
	vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
	polyData->SetPoints(points);
	polyData->GetPointData()->SetScalars(scalar);
	vtkSmartPointer<vtkStructuredGrid> structuredGrid = vtkSmartPointer<vtkStructuredGrid>::New();
	structuredGrid->SetDimensions(rGridSize, thetaGridSize, zGridSize);
	structuredGrid->SetPoints(points);
	structuredGrid->GetPointData()->SetScalars(scalar);
	return structuredGrid;
}


/**
* @time	2021/12/24
* @brief DV3D::PolarContourDatasetConstructor::setResolution 设置分辨率
* @param int
* @return void
*/
void DV3D::PolarContourDatasetConstructor::setResolution(int resolution)
{
	if (resolution < 1)
		return;
	angles.clear();
	angles.reserve(resolution);
	mResolution = resolution;
	double angInterval = vtkMath::RadiansFromDegrees(360.0) / mResolution;
	for (auto i = 0; i < mResolution; ++i)
		angles.push_back(angInterval * i);
}

void DV3D::PolarContourDatasetConstructor::initData()
{
	auto h5d = getHdf5Data();
	std::map<double, std::map<double, double>> maplist;
	generateMapList(maplist);
	generatePoints(maplist);
}

/**
* @time	2021/12/24
* @brief DV3D::PolarContourDatasetConstructor::generateMapList 生成分类表
* @param std::map<double
* @param std::map<double
* @param double>> & maplist
* @return void
*/
void DV3D::PolarContourDatasetConstructor::generateMapList(std::map<double, std::map<double, double>>& maplist)
{
	auto h5d = getHdf5Data();
	std::shared_ptr<DV::ContourDataPolar> data =
		std::shared_ptr<DV::ContourDataPolar>(DV::CreateContourDataPolar(h5d));
	data->loadPoint();
	auto datas = data->getGrids();
	auto face = data->getStructFace();
	(h5d.coordinateSystem == Hdf5Data::CoordinateSystem::CYLINDER) ?
		polarZ = face[0] :
		polarZ = face[2];
	//开始进行插值
	rGridSize = data->getWidth();
	thetaGridSize = data->getHeight();
	zGridSize = 1;
	for (int thetai = 0; thetai < thetaGridSize; ++thetai)
	{
		for (int ri = 0; ri < rGridSize; ++ri)
		{
			double rVal = datas[ri + thetai * rGridSize].x;
			double thetVal = datas[ri + thetai * rGridSize].y;
			double scalVal = datas[ri + thetai * rGridSize].value;
			maplist[thetVal][rVal] = scalVal;
			if (thetai == thetaGridSize - 1)
				continue;
			double thetValNext = datas[ri + (thetai + 1) * rGridSize].y;
			double scalValNext = datas[ri + (thetai + 1) * rGridSize].value;
			auto iter = angles.begin();
			while (iter != angles.end() && thetValNext > *iter)
			{
				if (*iter <= thetVal)
				{
					iter++;
					continue;
				}
				//插值的标量值计算
				double curScalar = (scalValNext - scalVal) * ((*iter) - thetVal) / (thetValNext - thetVal) + scalVal;
				maplist[*iter][rVal] = curScalar;
				iter++;
			}
		}
	}
}


/**
* @time	2021/12/24
* @brief DV3D::PolarContourDatasetConstructor::generatePoints 生成点云
* @param std::map<double
* @param std::map<double
* @param double>> & maplist
* @return void
*/
void DV3D::PolarContourDatasetConstructor::generatePoints(std::map<double, std::map<double, double>>& maplist)
{

	points = vtkSmartPointer<vtkPoints>::New();
	scalar = vtkSmartPointer<vtkFloatArray>::New();
	thetaGridSize = maplist.size();
	for (auto iterTheta = maplist.begin(); iterTheta != maplist.end(); iterTheta++)
	{
		for (auto iterR = iterTheta->second.begin(); iterR != iterTheta->second.end(); iterR++)
		{
			double x = iterR->first * cos(iterTheta->first);
			double y = iterR->first * sin(iterTheta->first);
			double z = polarZ;
			points->InsertNextPoint(x, y, z);
			scalar->InsertNextTuple1(iterR->second);
		}
	}
}
