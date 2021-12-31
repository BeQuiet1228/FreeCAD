#include "CartesianVector3dDatasetConstructor.h"
#include <cassert>
#include "vtkMath.h"
#include "vtkFloatArray.h"
#include "vtkPointData.h"
#include "vtkArrowSource.h"
#include "vtkGlyph3D.h"
namespace DV3D
{
	double getScalar(vtkPoint3d);
	std::vector<std::string> vStringSplit(const  std::string& s, const std::string& delim);
	struct AxisInfo
	{
		std::string str;
		AxisDir axisDir;
	};
	const AxisInfo axisInfos[] = {
		{"E1",X},{"E2",Y},{"E3",Z}
	};
}
DV3D::CartesianVector3dDatasetConstructor::CartesianVector3dDatasetConstructor() :
	xGridSize(0), yGridSize(0), zGridSize(0), scaleFactor(0.0f), xUnit(5), yUnit(5), zUnit(2)
{

}

DV3D::CartesianVector3dDatasetConstructor::~CartesianVector3dDatasetConstructor()
{

}

vtkSmartPointer<vtkDataSet> DV3D::CartesianVector3dDatasetConstructor::creatDataset()
{
	initDatas();
	vtkSmartPointer<vtkArrowSource> arrowSource = vtkSmartPointer<vtkArrowSource>::New();
	vtkSmartPointer<vtkGlyph3D> glyph = vtkSmartPointer<vtkGlyph3D>::New();
	glyph->SetInputData(polyData);
	glyph->SetScaleFactor(scaleFactor);//设置缩放因子
	glyph->SetSourceConnection(arrowSource->GetOutputPort());
	//glyph->SetScaleModeToDataScalingOff();//关闭缩放
	glyph->Update();
	return glyph->GetOutput();
}

void DV3D::CartesianVector3dDatasetConstructor::initDatas()
{
	//将结构数据处理成点位,z-y-x
	loadStructPoint();
	//生成矢量数据
	std::vector<vtkPoint3d> vectorDatas;
	vectorDatas.reserve(xGridSize * yGridSize * zGridSize);
	vectorDatas = generateVectorData();
	//合并
	mergeDatas(vectorDatas);
}

void DV3D::CartesianVector3dDatasetConstructor::loadStructPoint()
{
	//获取数据
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
	std::vector<float>& xList = grid[1];
	std::vector<float>& yList = grid[2];
	std::vector<float>& zList = grid[3];
	initGrid(xList.size(), yList.size(), zList.size());
	structPoint = vtkSmartPointer<vtkPoints>::New();
	for (auto zi = 0; zi < zGridSize; ++zi)
	{
		for (auto yi = 0; yi < yGridSize; ++yi)
		{
			for (auto xi = 0; xi < xGridSize; ++xi)
			{
				structPoint->InsertNextPoint(xList[xi], yList[yi], zList[zi]);
			}
		}
	}
	//计算缩放因子
	double scaleFactorX = (xList[xGridSize - 1] - xList[0]) / (xGridSize / xUnit);
	double scaleFactorY = (yList[yGridSize - 1] - yList[0]) / (yGridSize / yUnit);
	double scaleFactorZ = (zList[zGridSize - 1] - zList[0]) / (zGridSize / zUnit);
	scaleFactor = sqrt(scaleFactorX * scaleFactorX +
		scaleFactorY * scaleFactorY +
		scaleFactorZ * scaleFactorZ);
}
void DV3D::CartesianVector3dDatasetConstructor::initGrid(vtkIdType x, vtkIdType y, vtkIdType z)
{
	xGridSize = x;
	yGridSize = y;
	zGridSize = z;
}


/**
* @time	2021/12/28
* @brief DV3D::CartesianVector3dDatasetConstructor::generateVectorData 生成矢量数据
* @param Hdf5Data & h5d
* @return std::vector<DV3D::VectorData>
*/
std::vector<DV3D::vtkPoint3d> DV3D::CartesianVector3dDatasetConstructor::generateVectorData()
{
	auto h5d = getHdf5Data();
	std::vector<float> vaList;
	Hdf5IO::getValue(h5d.listDataSet.at(0), vaList);
	std::vector<vtkPoint3d> datas;
	long long index = 0;
	datas.reserve(xGridSize * yGridSize * zGridSize);
	for (auto zi = 0; zi < zGridSize; ++zi)
	{
		for (auto yi = 0; yi < yGridSize; ++yi)
		{
			for (auto xi = 0; xi < xGridSize; ++xi)
			{
				auto scalarX = vaList[index]; index++;//x
				auto scalarY = vaList[index]; index++;//y
				auto scalarZ = vaList[index]; index++;
				vtkPoint3d p2(scalarX, scalarY, scalarZ);
				datas.push_back(p2);
			}
		}
	}
	return datas;
}


/**
* @time	2021/12/28
* @brief DV3D::CartesianVector3dDatasetConstructor::mergeDatas 将三轴的数据进行合并
* @param std::vector<std::vector<VectorData>> &
* @return void
*/
void DV3D::CartesianVector3dDatasetConstructor::mergeDatas(std::vector<vtkPoint3d>& datas)
{
	/*
		对数据进行合并并生成polydata数据
	*/
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkFloatArray> normal = vtkSmartPointer<vtkFloatArray>::New();//法向
	vtkSmartPointer<vtkFloatArray> vector = vtkSmartPointer<vtkFloatArray>::New();//方向
	vtkSmartPointer<vtkFloatArray> scalars = vtkSmartPointer<vtkFloatArray>::New();//大小
	normal->SetNumberOfComponents(3); //normal->SetName("Normals");
	vector->SetNumberOfComponents(3); //vector->SetName("Vector");
		//记录下最大的标量
	double scalarMax = 0.0;
	long long index = 0;
#if 1
	for (auto zi = 0; zi < zGridSize; ++zi)
	{
		for (auto yi = 0; yi < yGridSize; ++yi)
		{
			for (auto xi = 0; xi < xGridSize; ++xi)
			{
				vtkPoint3d vectorPoint=datas[getPointId(zi, yi, xi)];
				//获取大小
				auto saclar = getScalar(vectorPoint);
				if (0.0f == saclar)
					continue;
				if (scalarMax < saclar)
					scalarMax = saclar;
				index++;
				scalars->InsertNextTuple1(saclar);
				vectorPoint = vectorPoint.normalized();
				vector->InsertNextTuple3(vectorPoint.x(), vectorPoint.y(), vectorPoint.z());
				auto p1 = structPoint->GetPoint(getPointId(zi, yi, xi));
				points->InsertNextPoint(p1[0], p1[1], p1[2]);
				normal->InsertNextTuple3(1.0, 1.0, 1.0);
			}
		}
	}
#else
#pragma region 矢量数据合并

	auto zSize = (zGridSize % zUnit > 0) ? (zGridSize / zUnit + 1) : (zGridSize / zUnit);
	auto ySize = (yGridSize % yUnit > 0) ? (yGridSize / yUnit + 1) : (yGridSize / yUnit);
	auto xSize = (xGridSize % xUnit > 0) ? (xGridSize / xUnit + 1) : (xGridSize / xUnit);
	for (auto zi = 0; zi < zSize; ++zi)
	{
		for (auto yi = 0; yi < ySize; ++yi)
		{
			for (auto xi = 0; xi < xSize; ++xi)
			{
				auto vectorPoint =
					getMergeVector(datas, zi * zUnit, yi * yUnit, xi * xUnit, zUnit, yUnit, xUnit);
				//获取大小
				auto saclar = getScalar(vectorPoint);
				if (0.0f == saclar)
					continue;
				if (scalarMax < saclar)
					scalarMax = saclar;
				index++;
				scalars->InsertNextTuple1(saclar);
				vectorPoint = vectorPoint.normalized();
				vector->InsertNextTuple3(vectorPoint.x(), vectorPoint.y(), vectorPoint.z());
				auto p1 = structPoint->GetPoint(getPointId(zi * zUnit, yi * yUnit, xi * xUnit));
				points->InsertNextPoint(p1[0], p1[1], p1[2]);
				normal->InsertNextTuple3(1.0, 1.0, 1.0);
			}
		}
	}
#pragma endregion
#endif
	polyData = vtkSmartPointer<vtkPolyData>::New();
	polyData->SetPoints(points);
	polyData->GetPointData()->SetScalars(scalars);
	polyData->GetPointData()->SetVectors(vector);
	polyData->GetPointData()->SetNormals(normal);
	scaleFactor /= scalarMax;
}

vtkIdType DV3D::CartesianVector3dDatasetConstructor::getPointId(vtkIdType zi, vtkIdType yi, vtkIdType xi)
{
	return (zi * xGridSize * yGridSize + yi * xGridSize + xi);
}



/**
* @time	2021/12/29
* @brief DV3D::CartesianVector3dDatasetConstructor::getAxisDir 获取轴向
* @param Hdf5Data & h5d
* @return DV3D::AxisDir
*/
DV3D::AxisDir DV3D::CartesianVector3dDatasetConstructor::getAxisDir(Hdf5Data& h5d)
{
	std::string headstr = h5d.headList.at(0);
	headstr.erase(0, headstr.find("=") + 1);
	int off = 0;
	auto elems = vStringSplit(headstr, "$");
	auto axisInfo = elems.at(2);
	AxisDir mAxisDir;
	bool isbreak = false;
	for (auto& i : axisInfos)
	{
		if (i.str == axisInfo)
		{
			mAxisDir = i.axisDir;
			isbreak = true; break;
		}
	}
	if (!isbreak) mAxisDir = Axis_NUll;
	return mAxisDir;
}



/**
* @time	2021/12/31
* @brief DV3D::CartesianVector3dDatasetConstructor::getMergeVector 更具单位进行合并矢量
* @param std::vector<std::vector<vtkPoint3d>> & datas
* @param vtkIdType zi
* @param vtkIdType yi
* @param vtkIdType xi
* @param vtkIdType zUnit
* @param vtkIdType yUnit
* @param vtkIdType xUnit
* @return DV3D::vtkPoint3d
*/
DV3D::vtkPoint3d DV3D::CartesianVector3dDatasetConstructor::getMergeVector(
	std::vector<vtkPoint3d>& datas,
	vtkIdType zIndex, vtkIdType yIndex, vtkIdType xIndex,
	vtkIdType zUnit, vtkIdType yUnit, vtkIdType xUnit)
{
	/*
		获取出矢量数据，并按照zUnit*yUnit*xUnit为一个单位网格的方式进行合并
	*/
	auto pointNumber = xGridSize * yGridSize * zGridSize;
	vtkPoint3d vecPoint(0.0, 0.0, 0.0);
	for (auto zi = 0; zi < zUnit; ++zi)
	{
		for (auto yi = 0; yi < yUnit; ++yi)
		{
			for (auto xi = 0; xi < xUnit; ++xi)
			{
				auto pointId = getPointId(zi + zIndex, yi + yIndex, xi + zIndex);
				if (pointId > pointNumber)
					continue;
				vecPoint += datas[pointId];
			}
		}
	}
	return vecPoint;
}
double DV3D::getScalar(vtkPoint3d p)
{
	return sqrt(p.x() * p.x() + p.y() * p.y() + p.z() * p.z());
}
std::vector<std::string> DV3D::vStringSplit(const  std::string& s, const std::string& delim)
{
	std::vector<std::string> elems;
	size_t pos = 0;
	size_t len = s.length();
	size_t delim_len = delim.length();
	if (delim_len == 0) return elems;
	while (pos < len)
	{
		int find_pos = s.find(delim, pos);
		if (find_pos < 0)
		{
			elems.push_back(s.substr(pos, len - pos));
			break;
		}
		elems.push_back(s.substr(pos, find_pos - pos));
		pos = find_pos + delim_len;
	}
	for (auto iter = elems.begin(); iter != elems.end();)
	{
		if (*iter != "")
		{
			iter++;
			continue;
		}
		iter = elems.erase(iter);
	}
	return elems;
}