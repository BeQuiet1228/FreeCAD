#include "PolarContour3dDataSetConstructor.h"
#include <cassert>
#include "vtkUnstructuredGrid.h"
#include "vtkCellType.h"
#include "vtkCellData.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
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
	mResolution = resolution;
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
	/*
		创建表格索引表，按z-theta-r的顺序分类存放，可以自动完成排序功能。
	*/
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
	/*
		maplist主要时用来分类存放增加的插入值，当新增一个插入值的时候，在完全计算完毕时，并不确定这个值的序号id，
		所以按照z-theta-r的索引存放，之后创建点位时，自动完成排序。
	*/
	//val-r-theta-z
	std::vector<float>& vaList = grid[0];
	std::vector<float>& rList = grid[1];
	std::vector<float>& thetaList = grid[2];
	std::vector<float>& zList = grid[3];
	//获取最大角度,和最小角度
	{
		auto minTheta = *thetaList.begin();
		auto maxTheta = *(thetaList.end() - 1);
		double angInterval = (maxTheta - minTheta) / mResolution;
		angles.clear(); angles.reserve(mResolution);
		for (auto i = 0; i < mResolution; ++i)
			angles.push_back(minTheta + angInterval * i);
	}
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
				double zVal = zList[zi];
				//将从原生数据中取出的按照z->theta-R的顺序分类存入
				maplist[zVal][thetVal][rVal] = scalVal;
				if (thetai == thetaGridSize - 1)
					continue;
				/*
					需要判断相邻的两个tehta之间是否需要进行插值，
					需要先获得相邻的两个theta和标量值
				*/
				double thetValNext = thetaList[(thetai + 1)];
				double scalValNext = vaList[getpointId(ri, thetai + 1, zi)];
				auto iter = angles.begin();
				//遍历插入的值角度列表
				while (iter != angles.end() && thetValNext > *iter)
				{
					if (*iter <= thetVal)
					{
						/*
						 当前角度没在两个相邻角度之间，且小于左侧,不进行插值计算，判断下个角度
						*/
						iter++;
						continue;
					}
					//计算插值的标量值
					double curScalar = (scalValNext - scalVal) * ((*iter) - thetVal)
						/ (thetValNext - thetVal) + scalVal;
					//将生成的插值数据按z->theta->r的顺序分类存入
					maplist[zVal][*iter][rVal] = curScalar;
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
	/*
		使用已经生成好的maplist，按照z->theta->r的访问顺序生成点位，以及装入标量值
	*/
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
