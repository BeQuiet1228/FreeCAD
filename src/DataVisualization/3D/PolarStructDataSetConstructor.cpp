#include"PolarStructDataSetConstructor.h"
#include"cassert"
#include"array"
#include"vtkUnstructuredGrid.h"
#include"vtkCellType.h"
#include"vtkPolyData.h"
#include"vtkCellArray.h"
#include"vtkRotationalExtrusionFilter.h"
#include"vtkFloatArray.h"
#define _USE_MATH_DEFINES
#include"math.h"
const float preciSion = 0.00001f;//精度

DV3D::PolarStructDaraSetConstruct::PolarStructDaraSetConstruct() :rSize(0), thetaSize(0), zSize(0), isCir(false) {

}
DV3D::PolarStructDaraSetConstruct::~PolarStructDaraSetConstruct() {

}
/**
* @brief DV3D::PolarStructDaraSetConstruct::isComCir 判断是否为闭关的圆
* @param std::vector<float> & thetas
* @return bool
* @time	2021/12/15
*/
bool DV3D::PolarStructDaraSetConstruct::isComCir(std::vector<float>& thetas)
{
	//判断角度是否为一个封闭的圆
	auto maxTheta = thetas.end() - 1;
	auto minTheta = thetas.begin();
	if (2 * M_PI - (*maxTheta) > -preciSion && 2 * M_PI - (*maxTheta) < preciSion &&
		(*minTheta)>-preciSion && (*minTheta)< preciSion)
		return true;
	return false;
}
vtkSmartPointer<vtkDataSet> DV3D::PolarStructDaraSetConstruct::creatDataset() {
	initPoints();
	auto value = getPolarIndex();

	auto ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	ugrid->Allocate(value.size() * 4);
	//添加六面体
	for (auto& iter : value)
	{
		long long zIndex = iter[0];
		long long rIndex = iter[1];
		long long thetaIndex = iter[2];
		long long type = iter[3];
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
void DV3D::PolarStructDaraSetConstruct::initPoints() {
	auto grid = getPolarDatas();
	long long zs = grid[0].size();
	long long rs = grid[1].size();
	long long thetas = grid[2].size();
	isCir = isComCir(grid[2]);
	initGridsize(rs, thetas, zs);
	//构建points
	points = vtkSmartPointer<vtkPoints>::New();
	points->Allocate(rs * thetas * zs);
	//获取所有顶点
	long long pointId = 0;
	for (auto& z : grid[0])
	{
		for (auto& r : grid[1])
		{
			for (auto& theta : grid[2])
			{
				double p[3] = { r * cos(theta) ,r * sin(theta) ,z };
				points->InsertPoint(pointId, p);
				pointId++;
			}
		}
	}
	return;
}
/**
* @brief DV3D::PolarStructDaraSetConstruct::getPolarDatas 从H5数据中获取点云
* @return DV3D::PolarDatas
* @time	2021/12/15
*/
DV3D::PolarDatas DV3D::PolarStructDaraSetConstruct::getPolarDatas()
{
	auto h5d = getHdf5Data();
	assert((h5d.listDataSet.size() == 4) && "list DataSet size is not 4!");
	PolarDatas grid;
	grid.reserve(3);
	for (int i = 0; i < 3; i++)
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
/**
* @brief DV3D::PolarStructDaraSetConstruct::getPolarIndex 获取k矩阵网格数据
* @return DV3D::PolarIndes
* @time	2021/12/15
*/
DV3D::PolarIndes DV3D::PolarStructDaraSetConstruct::getPolarIndex()
{
	auto h5d = getHdf5Data();
	std::vector<float> value;
	Hdf5IO::getValue(h5d.listDataSet.at(3), value);
	PolarIndes valueIndex;
	valueIndex.reserve(value.size() / 4);
	const int itemSize = 4;
	for (auto iter = value.begin(); iter != value.end();)
	{
		std::vector<long long> properDatas;
		for (auto i = 0; i < itemSize; i++, iter++)
			properDatas.push_back(*iter);
		std::vector<long long> valueItem;
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
void DV3D::PolarStructDaraSetConstruct::initGridsize(unsigned long long rs, unsigned long long thetas, unsigned long long zs)
{
	rSize = rs;
	thetaSize = thetas;
	zSize = zs;
}
long long DV3D::PolarStructDaraSetConstruct::getPointId(const long long& thetai, const long long& ri, const long long& zi)
{
	//考虑0.0rad和6.28..rad的S曲线的取值会有浮动,
	//当theta取到6.28的时候修改pointid到0.0时
	if (isCir && (thetai == thetaSize - 1))
		return (zi * thetaSize * rSize + ri * thetaSize);
	return (zi * thetaSize * rSize + ri * thetaSize + thetai);
}
