#include "CartesianStructDataSetConstructor.h"
#include <cassert>
#include <HDF5Reader/hdf5io.h>
//test
#include <QFileDialog>

#include <vtkPoints.h>
#include <vtkUnstructuredGrid.h>
#include <vtkCellType.h>

DV3D::CartesianStructDataSetConstructor::CartesianStructDataSetConstructor()
	:xSize(0), ySize(0), zSize(0)
{

}

DV3D::CartesianStructDataSetConstructor::~CartesianStructDataSetConstructor()
{

}


vtkSmartPointer<vtkDataSet> DV3D::CartesianStructDataSetConstructor::creatDataset()
{
	initPoints();

	auto h5d = getHdf5Data();
	VectorF value;
	Hdf5IO::getValue(h5d.listDataSet.at(3), value);

	auto ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	ugrid->SetPoints(points);
	//ugrid->Allocate(value.size());
	//添加六面体网格
	for (auto iter = value.begin(); iter != value.end(); iter++)
	{
		int xIndex = *iter;
		iter++;
		int yIndex = *iter;
		iter++;
		int zIndex = *iter;
		iter++;
		int type = *iter;
		if ((type & 0x03) != 0x03 && (type & 0x08) != 0x08)
			continue;
		vtkIdType cell[8] = {
			getPointID(xIndex - 1,yIndex - 1,zIndex - 1),
			getPointID(xIndex,yIndex - 1,zIndex - 1),
			getPointID(xIndex - 1,yIndex ,zIndex - 1),
			getPointID(xIndex,yIndex,zIndex - 1),
			getPointID(xIndex - 1,yIndex - 1,zIndex),
			getPointID(xIndex,yIndex - 1,zIndex),
			getPointID(xIndex - 1,yIndex ,zIndex),
			getPointID(xIndex,yIndex,zIndex),
		};
		ugrid->InsertNextCell(VTK_VOXEL, 8, cell);

	}
	return ugrid;
}

/**
* @brief DV3D::CartesianStructDataSetConstructor::getPointID 根据数据的列方式，获取到点数据在数据中的索引
* @param const vtkIdType & xi x方向上的网格索引
* @param const vtkIdType & yi y方向上的网格索引
* @param const vtkIdType & zi z方向上的网格索引
* @return vtkIdType 索引对应的点在数据中存在的位置
*/
vtkIdType DV3D::CartesianStructDataSetConstructor::getPointID(const vtkIdType& xi, const vtkIdType& yi, const vtkIdType& zi)
{
	return	zi * xSize * ySize + yi * xSize + xi;
}

void DV3D::CartesianStructDataSetConstructor::initPoints()
{
	auto h5d = getHdf5Data();
	assert((h5d.listDataSet.size() == 4) && "list DataSet size is not 4!");

	std::vector<std::vector<float>> grid;
	grid.reserve(3);
	for (int i = 0; i < 3; i++)
	{
		std::vector<float> d;
		Hdf5IO::getValue(h5d.listDataSet.at(i), d);
		grid.push_back(d);
	}

	//初始化网格大小
	int xs = grid[0].size();
	int ys = grid[1].size();
	int zs = grid[2].size();
	initGridsize(xs, ys, zs);

	//获取所有顶点 循环顺序为z -> y -> x
	//这里的顺序会影响到getPointID中获取点索引的方式
	points = vtkSmartPointer<vtkPoints>::New();
	//points->Allocate(xs * ys * zs);
	int pointId = 0;
	double temp[3] = {0,0,0};
	for (auto z = grid[2].begin(); z != grid[2].end(); z++)
	{
		for (auto y = grid[1].begin(); y != grid[1].end(); y++)
		{
			for (auto x = grid[0].begin(); x != grid[0].end(); x++)
			{
				temp[0] = *x;
				temp[1] = *y;
				temp[2] = *z;
				points->InsertPoint(pointId, temp);
				pointId++;
			}
		}
	}

}

/**
* @brief DV3D::CartesianStructDataSetConstructor::initGridsize 初始化网格大小，用于获取网格点的id
* @param unsigned int xSize
* @param unsigned ySize
* @param unsigned int zSize
* @return void
*/
void DV3D::CartesianStructDataSetConstructor::initGridsize(unsigned int xSize, unsigned ySize, unsigned int zSize)
{
	this->xSize = xSize;
	this->ySize = ySize;
	this->zSize = zSize;
}
