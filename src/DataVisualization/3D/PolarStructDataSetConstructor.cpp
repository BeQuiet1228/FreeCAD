#include"PolarStructDataSetConstructor.h"
#include"cassert"
#include"array"
#include"vtkUnstructuredGrid.h"
#include"vtkCellType.h"
namespace DV3D {
	PolarStructDaraSetConstruct::PolarStructDaraSetConstruct() :rSize(0),thetaSize(0),zSize(0){
	
	}
	PolarStructDaraSetConstruct::~PolarStructDaraSetConstruct() {
	
	}
	vtkSmartPointer<vtkDataSet> PolarStructDaraSetConstruct::creatDataset() {
		auto dataType=getThetaDatas();
		switch (dataType)
		{
		case DV3D::PolarStructDaraSetConstruct::Plane:
			return creatDatasetPlane();
		case DV3D::PolarStructDaraSetConstruct::PlaneHalf:
			return creatDatasetPlaneHalf();
		case DV3D::PolarStructDaraSetConstruct::nomal:
			return creatDatasetnormal();
		}
		
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
		//MIL_C
		switch (h5d.coordinateSystem)
		{
		case Hdf5Data::CoordinateSystem::CYLINDER:
		{
			//z-r-theta
		}
			break;
		case Hdf5Data::CoordinateSystem::POLAR:
		{
			//r-theta-z
			grid[2].swap(grid[0]);
			grid[1].swap(grid[2]);
		}
			break;
		}
		return grid;
	}
	PolarIndes PolarStructDaraSetConstruct::getPolarIndex()
	{
		auto h5d = getHdf5Data();
		std::vector<float> value;
		Hdf5IO::getValue(h5d.listDataSet.at(3), value);
		PolarIndes valueIndex;
		valueIndex.reserve(value.size()/4);
		int rIndex, zIndex, thetaIndex, properIndex;
		switch (h5d.coordinateSystem)
		{
		case Hdf5Data::CoordinateSystem::POLAR:
		{
			rIndex = 0;
			thetaIndex = 1;
			zIndex = 2;
			properIndex = 3;
		}
		break;
		case Hdf5Data::CoordinateSystem::CYLINDER:
		{
			zIndex = 0;
			rIndex = 1;
			thetaIndex = 2;
			properIndex = 3;
		}
		break;
		}
		const int itemSize = 4;
		for (auto iter=value.begin();iter!=value.end();)
		{
			std::vector<__int64> properDatas;
			for (auto i = 0; i < itemSize; i++,iter++) 
				properDatas.push_back(*iter);
			std::vector<__int64> valueItem;
			valueItem.reserve(4);
			//r-theta-z
			valueItem.push_back(properDatas[zIndex]);
			valueItem.push_back(properDatas[rIndex]);
			valueItem.push_back(properDatas[thetaIndex]);
			valueItem.push_back(properDatas[properIndex]);
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
	PolarStructDaraSetConstruct::DataType PolarStructDaraSetConstruct::getThetaDatas()
	{
		auto h5d = getHdf5Data();
		std::vector<float> thetaS;
		int thetaIndex = -1;
		switch (h5d.coordinateSystem)
		{
		case Hdf5Data::CoordinateSystem::CYLINDER:
			thetaIndex=2;
		break;
		case Hdf5Data::CoordinateSystem::POLAR:
			thetaIndex=1;
		break;
		}
		assert(thetaIndex!=-1);
		Hdf5IO::getValue(h5d.listDataSet.at(thetaIndex),thetaS);
		if (thetaS.size() > 3)
			return DataType::nomal;
		else if (thetaS.size() == 3)
			return DataType::Plane;
		else
			return DataType::PlaneHalf;
	}
	vtkSmartPointer<vtkDataSet> PolarStructDaraSetConstruct::creatDatasetnormal()
	{
		initPoints();
		auto value = getPolarIndex();
		//特殊情况
		//0~360
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
	vtkSmartPointer<vtkDataSet> PolarStructDaraSetConstruct::creatDatasetPlaneHalf()
	{
		//0~360
		auto grid = getPolarDatas();
		__int64 zs = grid[0].size();
		__int64 rs = grid[1].size();
		__int64 thetas = 1;
		initGridsize(rs,thetas,zs);
		//构建Points
		points = vtkSmartPointer<vtkPoints>::New();
		points->Allocate(rs*zs*thetas);
		//获取所有顶点
		__int64 pointId = 0;
		for (auto &z:grid[0])
		{
			for (auto& r : grid[1])
			{
				std::array<double, 3> p = {r*cos(grid[2][0]),r*sin(grid[2][0]),z};
				points->InsertPoint(pointId,p.data());
				pointId++;
			}
		}
	}
	vtkSmartPointer<vtkDataSet> PolarStructDaraSetConstruct::creatDatasetPlane()
	{
		//0-180-360
		auto grid = getPolarDatas();
		__int64 zs = grid[0].size();
		__int64 rs = grid[0].size();
		__int64 thetas = 2;
		initGridsize(rs,thetas,zs);
		//构建Points
	}
}
