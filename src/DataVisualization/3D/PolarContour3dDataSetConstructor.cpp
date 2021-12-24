#include "PolarContour3dDataSetConstructor.h"
#include <cassert>
#include "vtkUnstructuredGrid.h"
#include "vtkCellType.h"
#include "vtkCellData.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
#include "PolarContourFliter.h"
#include "vtkMath.h"
DV3D::PolarContour3dDatasetConstructor::PolarContour3dDatasetConstructor()
	: rGridSize(0), thetaGridSize(0), zGridSize(0)
{
	setResolution(40);
}
DV3D::PolarContour3dDatasetConstructor::~PolarContour3dDatasetConstructor()
{

}
vtkSmartPointer<vtkDataSet> DV3D::PolarContour3dDatasetConstructor::creatDataset()
{
	initPoints();
	vtkSmartPointer<vtkStructuredGrid> grid = vtkSmartPointer<vtkStructuredGrid>::New();
	grid->SetDimensions(rGridSize, thetaGridSize, zGridSize);
	grid->SetPoints(points);
	grid->GetPointData()->SetScalars(scalars);
	return grid;
}


/**
* @time	2021/12/24
* @brief DV3D::PolarContour3dDatasetConstructor::setResolution 设置插入点的分辨率
* @param int
* @return void
*/
void DV3D::PolarContour3dDatasetConstructor::setResolution(int resolution)
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

void DV3D::PolarContour3dDatasetConstructor::initPoints()
{
	auto h5d = getHdf5Data();
	assert(h5d.listDataSet.size() == 4 && "list DataSet size is not 4");
	std::vector<std::vector<float>> grid;
	grid.reserve(4);
	for (auto i = 0; i < h5d.listDataSet.size(); ++i)
	{
		std::vector<float> d;
		Hdf5IO::getValue(h5d.listDataSet.at(i), d);
		grid.push_back(d);
	}
	std::map<double, std::map<double, std::map<double, double>>> maplist;
	//
	generateMapList(maplist, grid);
	//存放数据
	generatePoints(maplist);
}

void DV3D::PolarContour3dDatasetConstructor::initGrid(int rs, int thetas, int zs)
{
	rGridSize = rs;
	thetaGridSize = thetas;
	zGridSize = zs;
}

vtkIdType DV3D::PolarContour3dDatasetConstructor::getpointId(const vtkIdType& ri, const vtkIdType& thetai, const vtkIdType& zi)
{
	return (ri + thetai * rGridSize + zi * rGridSize * thetaGridSize);
}

/**
* @time	2021/12/24
* @brief DV3D::PolarContour3dDatasetConstructor::generateMapList 根据分辨率进行插值,并生成表，按z-theta-r-value进行分类
* @param std::map<double, std::map<double, std::map<double, double>>>& maplist
* @param std::vector<std::vector<float>> & grid
* @return void
*/
void DV3D::PolarContour3dDatasetConstructor::generateMapList(
	std::map<double, std::map<double, std::map<double, double>>>& maplist,
	std::vector<std::vector<float>>& grid)
{
	//val-r-theta-z
	std::vector<float>& vaList = grid[0];
	std::vector<float>& rList = grid[1];
	std::vector<float>& thetaList = grid[2];
	std::vector<float>& zList = grid[3];
	//先初始化网格标尺
	initGrid(rList.size(), thetaList.size(), zList.size());
	for (int zi = 0; zi < zGridSize; ++zi)
	{
		for (int thetai = 0; thetai < thetaGridSize; ++thetai)
		{
			for (int ri = 0; ri < rGridSize; ++ri)
			{
				double rVal = rList[ri];
				double thetVal = thetaList[thetai];
				double scalVal = vaList[getpointId(ri, thetai, zi)];
				maplist[zList[zi]][thetVal][rVal] = scalVal;
				if (thetai == thetaGridSize - 1)
					continue;
				double thetValNext = thetaList[(thetai + 1)];
				double scalValNext = vaList[getpointId(ri, thetai + 1, zi)];
				auto iter = angles.begin();
				while (iter != angles.end() && thetValNext > *iter)
				{
					if (*iter <= thetVal)
					{
						iter++;
						continue;
					}
					//计算插值的标量值
					double curScalar = (scalValNext - scalVal) * ((*iter) - thetVal)
						/ (thetValNext - thetVal) + scalVal;
					maplist[zList[zi]][*iter][rVal] = curScalar;
					iter++;
				}
			}
		}

	}
}


/**
* @time	2021/12/24
* @brief DV3D::PolarContour3dDatasetConstructor::generatePoints 生成点云数据
* @param std::map<double,std::map<double,std::map<doubledouble>>> & maplist
* @return void
*/
void DV3D::PolarContour3dDatasetConstructor::generatePoints(
	std::map<double, std::map<double, std::map<double, double>>>& maplist)
{
	points = vtkSmartPointer<vtkPoints>::New();
	scalars = vtkSmartPointer<vtkFloatArray>::New();
	//重新设置theta方向的网格
	thetaGridSize = maplist.begin()->second.size();
	for (auto iterZ = maplist.begin(); iterZ != maplist.end(); iterZ++)
	{
		for (auto iterTheta = iterZ->second.begin(); iterTheta != iterZ->second.end(); iterTheta++)
		{
			for (auto iterR = iterTheta->second.begin(); iterR != iterTheta->second.end(); iterR++)
			{
				double x = iterR->first * cos(iterTheta->first);
				double y = iterR->first * sin(iterTheta->first);
				double z = iterZ->first;
				points->InsertNextPoint(x, y, z);
				scalars->InsertNextTuple1(iterR->second);
			}
		}
	}
}
