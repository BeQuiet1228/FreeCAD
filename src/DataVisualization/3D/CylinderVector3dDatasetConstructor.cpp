#include "CylinderVector3dDatasetConstructor.h"
//#include "CartesianVector3dDatasetConstructor.h"
#include "vtkFloatArray.h"
#include "vtkPointData.h"
#include "vtkArrowSource.h"
#include "vtkGlyph3D.h"
#define _USE_MATH_DEFINES
#include "math.h"
DV3D::CylinderVector3dDatasetContructor::CylinderVector3dDatasetContructor()
	:CartesianVector3dDatasetConstructor()
{
	setGridMergeUnit(1, 1, 1);
}

DV3D::CylinderVector3dDatasetContructor::CylinderVector3dDatasetContructor(vtkIdType zunit, vtkIdType thetaunit, vtkIdType runit)
	: CartesianVector3dDatasetConstructor(zunit, thetaunit, runit)
{

}

DV3D::CylinderVector3dDatasetContructor::~CylinderVector3dDatasetContructor()
{

}
/**
* @time	2022/01/04
* @brief DV3D::CylinderVector3dDatasetContructor::generatePolyData 生成三维矢量数据集
* @param std::vector<vtkPoint3d> & datas
* @param std::vector<float> & rList
* @param std::vector<float> & thetaList
* @param std::vector<float> & zList
* @return void
*/
void DV3D::CylinderVector3dDatasetContructor::generatePolyData(
	std::vector<vtkPoint3d>& datas,
	std::vector<float>& rList,
	std::vector<float>& thetaList,
	std::vector<float>& zList)
{
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkFloatArray> normal = vtkSmartPointer<vtkFloatArray>::New();//法向
	vtkSmartPointer<vtkFloatArray> vector = vtkSmartPointer<vtkFloatArray>::New();//方向
	vtkSmartPointer<vtkFloatArray> scalars = vtkSmartPointer<vtkFloatArray>::New();//大小
	normal->SetNumberOfComponents(3); //normal->SetName("Normals");
	vector->SetNumberOfComponents(3); //vector->SetName("Vector");
	double scalarMax = 0.0f;
	/*
		按合并计算每个方向的间隔
	*/
	//单位转换
	auto thetaGridSize = yGridSize, rGridSize = xGridSize, thetaUnit = yUnit, rUnit = xUnit;

	auto zSize = (zGridSize % zUnit > 0) ? (zGridSize / zUnit + 1) : (zGridSize / zUnit);
	auto thetaSize = (thetaGridSize % thetaUnit > 0) ? (thetaGridSize / thetaUnit + 1) : (thetaGridSize / thetaUnit);
	auto rSize = (rGridSize % rUnit > 0) ? (rGridSize / rUnit + 1) : (rGridSize / rUnit);
	/*
		构建数据
	*/
	for (auto zi = 0; zi < zSize; ++zi)
		for (auto thetai = 0; thetai < thetaSize; ++thetai)
			for (auto ri = 0; ri < rSize; ++ri)
			{
				vtkPoint3d vectorPoint = getMergeVector(datas, zList, thetaList, rList, zi, thetai, ri);
				auto scalar = getScalar(vectorPoint);
				if (0.0f == scalar)
					continue;
				if (scalarMax < scalar)
					scalarMax = scalar;
				scalars->InsertNextTuple1(scalar);
				vectorPoint = vectorPoint.normalized();
				vector->InsertNextTuple3(vectorPoint.x(), vectorPoint.y(), vectorPoint.z());
				{
					auto x = rList[ri * rUnit] * cos(thetaList[thetai * thetaUnit]);
					auto y = rList[ri * rUnit] * sin(thetaList[thetai * thetaUnit]);
					auto z = zList[zi * zUnit];
					points->InsertNextPoint(x, y, z);
					normal->InsertNextTuple3(1.0, 1.0, 1.0);
				}
			}
	polyData = vtkSmartPointer<vtkPolyData>::New();
	polyData->SetPoints(points);
	polyData->GetPointData()->SetScalars(scalars);
	polyData->GetPointData()->SetVectors(vector);
	polyData->GetPointData()->SetNormals(normal);
	//计算缩放因子
	double scaleFactorX = (rList[rGridSize - 1] - rList[0]) / (rGridSize / rUnit);
	double scaleFactorY = scaleFactorX;
	double scaleFactorZ = (zList[zGridSize - 1] - zList[0]) / (zGridSize / zUnit);
	scaleFactor = sqrt(scaleFactorX * scaleFactorX + scaleFactorY * scaleFactorY + scaleFactorZ * scaleFactorZ);
	scaleFactor /= scalarMax;
}


/**
* @time	2022/01/04
* @brief DV3D::CylinderVector3dDatasetContructor::getMergeVector 方向合并
* @param std::vector<vtkPoint3d> & datas
* @param std::vector<float> & zlist
* @param std::vector<float> & thetaList
* @param std::vector<float> & rList
* @param vtkIdType zi
* @param vtkIdType thetai
* @param vtkIdType ri
* @return DV3D::vtkPoint3d
*/
DV3D::vtkPoint3d DV3D::CylinderVector3dDatasetContructor::getMergeVector(
	std::vector<vtkPoint3d>& datas,
	std::vector<float>& zlist,
	std::vector<float>& thetaList,
	std::vector<float>& rList,
	vtkIdType zi,
	vtkIdType thetai,
	vtkIdType ri)
{
	auto thetaUnit = yUnit, rUnit = xUnit;
	vtkPoint3d vectorPoint(0.0, 0.0, 0.0);
	for (auto zUniti = 0; zUniti < zUnit; ++zUniti)
		for (auto thetaUniti = 0; thetaUniti < thetaUnit; ++thetaUniti)
			for (auto rUniti = 0; rUniti < rUnit; ++rUniti)
			{
				auto rIndex = ri * rUnit + rUniti;
				auto tIndex = thetai * thetaUnit + thetaUniti;
				auto zIndex = zi * zUnit + zUniti;
				if (rIndex >= rList.size() || tIndex >= thetaList.size() || zIndex >= zlist.size())
					continue;
				auto r = rList[rIndex];
				auto theta = thetaList[tIndex];
				auto z = zlist[zIndex];
				/*
					计算出三个方向的矢量数据
				*/
				vtkPoint3d direct_R(r * cos(theta), r * sin(theta), 0.0);
				vtkPoint3d direct_T(r * cos(theta + M_PI / 2), r * sin(theta + M_PI / 2), 0.0);
				vtkPoint3d direct_Z(0.0, 0.0, z);
				direct_R = direct_R.normalized() * datas[getPointId(zIndex, tIndex, rIndex)].x();
				direct_T = direct_T.normalized() * datas[getPointId(zIndex, tIndex, rIndex)].y();
				direct_Z = direct_Z.normalized() * datas[getPointId(zIndex, tIndex, rIndex)].z();
				auto curPoint = direct_R + direct_T + direct_Z;
				vectorPoint += curPoint;
			}
	return vectorPoint;
}
