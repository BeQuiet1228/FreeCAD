#include "CylinderVector3dDatasetConstructor.h"
//#include "CartesianVector3dDatasetConstructor.h"
#include "vtkFloatArray.h"
#include "vtkPointData.h"
#include "vtkArrowSource.h"
#include "vtkGlyph3D.h"
DV3D::CylinderVector3dDatasetContructor::CylinderVector3dDatasetContructor()
	:rGridSize(0), thetaGridSize(0), zGridSize(0), rUnit(1), thetaUnit(1), zUnit(1)
{

}
DV3D::CylinderVector3dDatasetContructor::~CylinderVector3dDatasetContructor()
{

}

vtkSmartPointer<vtkDataSet> DV3D::CylinderVector3dDatasetContructor::creatDataset()
{
	initData();
	vtkSmartPointer<vtkArrowSource> arrowSource = vtkSmartPointer<vtkArrowSource>::New();
	vtkSmartPointer<vtkGlyph3D> glyph = vtkSmartPointer<vtkGlyph3D>::New();
	glyph->SetInputData(polyData);
	glyph->SetScaleFactor(scaleFactor);//设置缩放因子
	glyph->SetSourceConnection(arrowSource->GetOutputPort());
	glyph->SetScaleModeToDataScalingOff();//关闭缩放
	glyph->Update();
	return glyph->GetOutput();
}


/**
* @time	2022/01/04
* @brief DV3D::CylinderVector3dDatasetContructor::initData 初始化数据
* @return void
*/
void DV3D::CylinderVector3dDatasetContructor::initData()
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
	std::vector<float>& varList = grid[0];
	std::vector<float>& rList = grid[1];
	std::vector<float>& thetaList = grid[2];
	std::vector<float>& zList = grid[3];
	initGridSize(zList.size(), thetaList.size(), rList.size());
	/*
		获取矢量数据
	*/
	std::vector<vtkPoint3d> datas;
	generateVectorData(datas, varList);
	/*
		构建数据
	*/
	generatePolyData(datas, rList, thetaList, zList);
}

void DV3D::CylinderVector3dDatasetContructor::initGridSize(vtkIdType zgrid, vtkIdType thetagrid, vtkIdType rgrid)
{
	zGridSize = zgrid;
	thetaGridSize = thetagrid;
	rGridSize = rgrid;
}

void DV3D::CylinderVector3dDatasetContructor::generateVectorData(std::vector<vtkPoint3d>& datas, std::vector<float>& varList)
{
	datas.reserve(zGridSize * thetaGridSize * rGridSize);
	auto iter = varList.begin();
	while (iter != varList.end())
	{
		auto normalX = *iter; iter++;
		auto normalY = *iter; iter++;
		auto normalZ = *iter; iter++;
		datas.push_back(vtkPoint3d(normalX, normalY, normalZ));
	}
}

void DV3D::CylinderVector3dDatasetContructor::generatePolyData(std::vector<vtkPoint3d>& datas, std::vector<float>& rList, std::vector<float>& thetaList, std::vector<float>& zList)
{
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkFloatArray> normal = vtkSmartPointer<vtkFloatArray>::New();//法向
	vtkSmartPointer<vtkFloatArray> vector = vtkSmartPointer<vtkFloatArray>::New();//方向
	vtkSmartPointer<vtkFloatArray> scalars = vtkSmartPointer<vtkFloatArray>::New();//大小
	normal->SetNumberOfComponents(3); //normal->SetName("Normals");
	vector->SetNumberOfComponents(3); //vector->SetName("Vector");
	double scalarMax = 0.0f;
	for (auto zi = 0; zi < zGridSize; ++zi)
		for (auto thetai = 0; thetai < thetaGridSize; ++thetai)
			for (auto ri = 0; ri < rGridSize; ++ri)
			{
				auto pointId = getPointId(zi, thetai, ri);
				auto polarVectorPoint = datas[pointId];
				vtkPoint3d vectorPoint;
				vectorPoint.setX(polarVectorPoint.x()*cos(polarVectorPoint.y()));
				vectorPoint.setY(polarVectorPoint.x() * cos(polarVectorPoint.y()));
				vectorPoint.setZ(polarVectorPoint.z());
				auto scalar = getScalar(vectorPoint);
				if (0.0f == scalar)
					continue;
				if (scalarMax < scalar)
					scalarMax = scalar;
				scalars->InsertNextTuple1(scalar);
				vectorPoint = vectorPoint.normalized();
				vector->InsertNextTuple3(vectorPoint.x(), vectorPoint.y(), vectorPoint.z());
				{
					auto x = rList[ri] * cos(thetaList[thetai]);
					auto y = rList[ri] * sin(thetaList[thetai]);
					auto z = zList[zi];
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
	double scaleFactorX = (rList[rGridSize - 1] - rList[0]) / (rGridSize);
	double scaleFactorY = scaleFactorX;
	double scaleFactorZ = (zList[zGridSize - 1] - zList[0]) / (zGridSize);
	scaleFactor = sqrt(scaleFactorX * scaleFactorX + scaleFactorY * scaleFactorY + scaleFactorZ * scaleFactorZ);
	//scaleFactor /= scalarMax;
}

vtkIdType DV3D::CylinderVector3dDatasetContructor::getPointId(vtkIdType zi, vtkIdType thetai, vtkIdType ri)
{
	return (ri + thetai * rGridSize + zi * rGridSize * thetaGridSize);
}

