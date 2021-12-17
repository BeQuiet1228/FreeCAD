#include"Contour3dataSetConstructor.h"
#include "vtkUnstructuredGrid.h"
#include <cassert>
#include"HDF5Reader/hdf5io.h"
#include "vtkCellType.h"
#include "vtkCellData.h"
#include "vtkPointData.h"
#include "vtkStructuredGrid.h"
#include <vtkContourFilter.h>
#include <vector>
#include <array>
#include <vtkPolyDataNormals.h>
DV3D::Contour3dDatasetConstructor::Contour3dDatasetConstructor()
: xGridSize(0),yGridSize(0),zGridSize(0)
{

}

DV3D::Contour3dDatasetConstructor::~Contour3dDatasetConstructor() {

}

vtkSmartPointer<vtkDataSet> DV3D::Contour3dDatasetConstructor::creatDataset() {
	initPoints();
	vtkSmartPointer<vtkStructuredGrid> grid = vtkSmartPointer<vtkStructuredGrid>::New();
	grid->SetDimensions(xGridSize, yGridSize, zGridSize);
	grid->SetPoints(points);
	grid->GetPointData()->SetScalars(scalars);
	return grid;
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
	std::vector<float>& vaList = grid[0];
	std::vector<float>& xList = grid[1];
	std::vector<float>& yList = grid[2];
	std::vector<float>& zList = grid[3];
	initGrid(xList.size(), yList.size(), zList.size());

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
	{
		scalars->InsertNextTuple1(vaList[vali]);
	}
}

void DV3D::Contour3dDatasetConstructor::initGrid(const vtkIdType& xs, const vtkIdType& ys, const vtkIdType& zs)
{
	xGridSize = xs;
	yGridSize = ys;
	zGridSize = zs;
}


vtkIdType DV3D::Contour3dDatasetConstructor::getpointId(const vtkIdType& xi, const vtkIdType& yi, const vtkIdType& zi)
{
	return zi * yGridSize * xGridSize + yi * xGridSize + xi;
}

