#include"Contour3dataSetConstructor.h"
#include "vtkUnstructuredGrid.h"
#include <cassert>
#include"HDF5Reader/hdf5io.h"
#include "vtkCellType.h"
#include "vtkCellData.h"
DV3D::Contour3dDatasetConstructor::Contour3dDatasetConstructor()
: xGridSize(0),yGridSize(0),zGridSize(0)
{

}

DV3D::Contour3dDatasetConstructor::~Contour3dDatasetConstructor() {

}

vtkSmartPointer<vtkDataSet> DV3D::Contour3dDatasetConstructor::creatDataset() {
	initPoints();
	vtkSmartPointer<vtkUnstructuredGrid> ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	//创建网格
	for (auto z = 0; z < zGridSize - 1; ++z)
	{
		for (auto y = 0; y < yGridSize - 1; ++y)
		{
			for (auto x = 0; x < xGridSize - 1; ++x)
			{
				std::vector<vtkIdType> cell = {
					getpointId(x,y,z),
					getpointId(x,y + 1,z),
					getpointId(x + 1,y,z),
					getpointId(x + 1,y + 1,z),
					getpointId(x,y,z + 1),
					getpointId(x,y + 1,z + 1),
					getpointId(x + 1,y,z + 1),
					getpointId(x + 1,y + 1,z + 1)
				};
				ugrid->InsertNextCell(VTK_VOXEL, 8, cell.data());
			}
		}
	}
	ugrid->SetPoints(points);
	ugrid->GetCellData()->SetScalars(scalars);
	return ugrid;
}
void DV3D::Contour3dDatasetConstructor::initPoints() {
	auto h5d = getHdf5Data();//获取H5数据
	assert(h5d.listDataSet.size() == 4 && "list DataSet size is not 4");

	std::vector<std::vector<float>> grid;
	grid.reserve(4);
	for (auto i = 0; i < h5d.listDataSet.size(); ++i)
	{
		std::vector<float> d;
		Hdf5IO::getValue(h5d.listDataSet.at(i), d);
		grid.push_back(d);
	}
	//x-y-z
	std::vector<float>& xList = grid[0];
	std::vector<float>& yList = grid[1];
	std::vector<float>& zList = grid[2];
	std::vector<float>& vaList = grid[3];
	initGrid(zList.size(), yList.size(), zList.size());

	points = vtkSmartPointer<vtkPoints>::New();
	//创建点云 
	for (auto zi = 0; zi < zGridSize; ++zi)
	{
		for (auto yi = 0; yi < yGridSize; ++yi)
		{
			for (auto xi = 0; xi < xGridSize; ++xi)
			{
				points->InsertNextPoint(xList[xi], yList[yi], zList[zi]);
			}
		}
	}
	//填入标量
	int vals = vaList.size();
	scalars = vtkSmartPointer<vtkFloatArray>::New();
	for (auto vali = 0; vali < vals; ++vali)
		scalars->InsertNextTuple1(vaList[vali]);
}

void DV3D::Contour3dDatasetConstructor::initGrid(unsigned long long xs, unsigned long long ys, unsigned long long zs)
{
	xGridSize = xs;
	yGridSize = ys;
	zGridSize = zs;
}

vtkIdType DV3D::Contour3dDatasetConstructor::getpointId(
	unsigned long long xi,
	unsigned long long yi,
	unsigned long long zi)
{
	return zi * yGridSize * xGridSize + yi * xGridSize + xi;
}
