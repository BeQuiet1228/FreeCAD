#include "PolarContour3dDataSetConstructor.h"
#include <cassert>
#include "vtkUnstructuredGrid.h"
#include "vtkCellType.h"
#include "vtkCellData.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
DV3D::PolarContour3dDatasetConstructor::PolarContour3dDatasetConstructor()
	: rGridSize(0),thetaGridSize(0),zGridSize(0)
{

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

void DV3D::PolarContour3dDatasetConstructor::initPoints()
{
	auto h5d = getHdf5Data();
	assert(h5d.listDataSet.size() == 4 && "list DataSet size is not 4");
	std::vector <std::vector <float>> datas;
	datas.reserve(4);
	for (auto i : h5d.listDataSet)
	{
		std::vector<float> d;
		Hdf5IO::getValue(i, d);
		datas.push_back(d);
	}
	//r-theta-z
	std::vector<float>& valList = datas[0];
	std::vector<float>& rList = datas[1];
	std::vector<float>& thetaList = datas[2];
	std::vector<float>& zList = datas[3];
	initGrid(rList.size(),thetaList.size(),zList.size());
	//获取点云
	points = vtkSmartPointer<vtkPoints>::New();
	for (auto zi=0;zi<zGridSize;++zi)
	{
		for (auto thetai = 0; thetai < thetaGridSize; ++thetai)
		{
			for (auto ri=0;ri<rGridSize;++ri)
			{
				double x = rList[ri] * cos(thetaList[thetai]);
				double y = rList[ri] * sin(thetaList[thetai]);
				double z = zList[zi];
				points->InsertNextPoint(x,y,z);
			}
		}
	}
	//填入标量
	scalars = vtkSmartPointer<vtkFloatArray>::New();
	for (auto vali = 0; vali < valList.size(); ++vali)
		scalars->InsertNextTuple1(valList[vali]);
}

void DV3D::PolarContour3dDatasetConstructor::initGrid(int rs, int thetas, int zs)
{
	rGridSize = rs;
	thetaGridSize = thetas;
	zGridSize = zs;
}

vtkIdType DV3D::PolarContour3dDatasetConstructor::getpointId(const vtkIdType& ri, const vtkIdType& thetai, const vtkIdType& zi)
{
	return (ri+thetai*rGridSize+zi*rGridSize*thetaGridSize);
}
