#include"PolarStructDataSetConstructor.h"
#include"cassert"
#include"array"
#include"vtkUnstructuredGrid.h"
#include"vtkCellType.h"
#include"vtkPolyData.h"
#include"vtkCellArray.h"
#include"vtkRotationalExtrusionFilter.h"
#include"vtkFloatArray.h"
namespace DV3D {
	PolarStructDaraSetConstruct::PolarStructDaraSetConstruct() :rSize(0),thetaSize(0),zSize(0){
	
	}
	PolarStructDaraSetConstruct::~PolarStructDaraSetConstruct() {
	
	}
	vtkSmartPointer<vtkDataSet> PolarStructDaraSetConstruct::creatDataset() {
		initPoints();
		auto value = getPolarIndex();
		auto ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
		ugrid->Allocate(value.size() * 4);
		//添加六面体
		for (auto& iter : value)
		{
			__int64 zIndex = iter[0];
			__int64 rIndex = iter[1];
			__int64 thetaIndex = iter[2];
			__int64 type = iter[3];
			if (((iter)[3] & 0x03) != 0x03)
				continue;
			if (zIndex == zSize || rIndex == rSize || thetaIndex == thetaSize)
				continue;
			vtkIdType cell[8] = {
				getPointId(thetaIndex - 1,	rIndex - 1,		zIndex - 1),
				getPointId(thetaIndex,		rIndex - 1,		zIndex - 1),
				getPointId(thetaIndex - 1,	rIndex,			zIndex - 1),
				getPointId(thetaIndex,		rIndex,			zIndex - 1),
				getPointId(thetaIndex - 1,	rIndex - 1,		zIndex),
				getPointId(thetaIndex,		rIndex - 1,		zIndex),
				getPointId(thetaIndex - 1,	rIndex,			zIndex),
				getPointId(thetaIndex,		rIndex,			zIndex),
			};
			ugrid->InsertNextCell(VTK_VOXEL, 8, cell);
		}
		ugrid->SetPoints(points);
		return ugrid;
	}
	void PolarStructDaraSetConstruct::initPoints(){
		auto grid = getPolarDatas();
		__int64 zs = grid[0].size();
		__int64 rs = grid[1].size();
		__int64 thetas = grid[2].size();
		initGridsize(rs,thetas,zs);
		//构建points
		points = vtkSmartPointer<vtkPoints>::New();
		points->Allocate(rs*thetas*zs);
		//获取所有顶点
		__int64 pointId = 0;
		for (auto &z:grid[0])
		{
			for (auto& r : grid[1])
			{
				for (auto& theta : grid[2])
				{
					double* p = new double[3];
					p[0] = r * cos(theta);
					p[1] = r * sin(theta);
					p[2] = z;
					points->InsertPoint(pointId,p);
					pointId++;
				}
			}
		}
	}
	PolarDatas PolarStructDaraSetConstruct::getPolarDatas()
	{
		auto h5d = getHdf5Data();
		assert((h5d.listDataSet.size() == 4) && "list DataSet size is not 4!");
		PolarDatas grid;
		grid.reserve(3);
		for (int i=0;i<3;i++)
		{
			std::vector<float>  d;
			Hdf5IO::getValue(h5d.listDataSet.at(i), d);
			grid.push_back(d);
		}
		//r-theta-z,调换下坐标顺序
		grid[2].swap(grid[0]);
		grid[1].swap(grid[2]);
		return grid;
	}
	PolarIndes PolarStructDaraSetConstruct::getPolarIndex()
	{
		auto h5d = getHdf5Data();
		std::vector<float> value;
		Hdf5IO::getValue(h5d.listDataSet.at(3), value);
		PolarIndes valueIndex;
		valueIndex.reserve(value.size()/4);
		const int itemSize = 4;
		for (auto iter=value.begin();iter!=value.end();)
		{
			std::vector<__int64> properDatas;
			for (auto i = 0; i < itemSize; i++,iter++) 
				properDatas.push_back(*iter);
			std::vector<__int64> valueItem;
			valueItem.reserve(4);
			//r-theta-z
			valueItem.push_back(properDatas[2]);
			valueItem.push_back(properDatas[0]);
			valueItem.push_back(properDatas[1]);
			valueItem.push_back(properDatas[3]);
			valueIndex.push_back(valueItem);
		}
		return valueIndex;
	}
	void PolarStructDaraSetConstruct::initGridsize(unsigned __int64 rs, unsigned __int64 thetas, unsigned __int64 zs)
	{
		rSize = rs;
		thetaSize = thetas;
		zSize = zs;
	}
	__int64 PolarStructDaraSetConstruct::getPointId(const __int64& thetai, const __int64& ri, const __int64& zi)
	{
		return zi * thetaSize * rSize + ri * thetaSize + thetai;
	}
}
