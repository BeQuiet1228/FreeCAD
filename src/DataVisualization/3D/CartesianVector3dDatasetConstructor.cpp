#include "CartesianVector3dDatasetConstructor.h"
#include <cassert>
#include "vtkMath.h"
#include "vtkFloatArray.h"
#include "vtkPointData.h"
#include "vtkArrowSource.h"
#include "vtkGlyph3D.h"
#include "QMessageBox.h"
#include "../C_encoding.h"

DV3D::CartesianVector3dDatasetConstructor::CartesianVector3dDatasetConstructor() :
	xGridSize(0), yGridSize(0), zGridSize(0), scaleFactor(0.0f), xUnit(5), yUnit(2), zUnit(2), isNull(true)
{
	polyData = nullptr;
}
DV3D::CartesianVector3dDatasetConstructor::CartesianVector3dDatasetConstructor(vtkIdType zunit, vtkIdType yunit, vtkIdType xunit)
	: xGridSize(0), yGridSize(0), zGridSize(0), scaleFactor(0.0f), xUnit(xunit), yUnit(yunit), zUnit(zunit), isNull(true)
{
	//if (polyData != nullptr)
	//{
	//	polyData->Delete();
	//	polyData = nullptr;
	//}
}
DV3D::CartesianVector3dDatasetConstructor::~CartesianVector3dDatasetConstructor()
{
}
vtkSmartPointer<vtkDataSet> DV3D::CartesianVector3dDatasetConstructor::creatDataset()
{
	initDatas();
	if (isNull)
	{
		/*
		弹出窗口
		*/
		QMessageBox box;
		QString message = DV::GetEncodingstr("绘制失败,所有的场值均为零.", ENCODING_GB2312);
		box.setText(message);
		box.exec();
		return nullptr;
	}
	vtkSmartPointer<vtkArrowSource> arrowSource = vtkSmartPointer<vtkArrowSource>::New();
	vtkSmartPointer<vtkGlyph3D> glyph = vtkSmartPointer<vtkGlyph3D>::New();
	glyph->SetInputData(polyData);
	glyph->SetScaleFactor(scaleFactor);//设置缩放因子
	glyph->SetSourceConnection(arrowSource->GetOutputPort());
	//glyph->SetScaleModeToDataScalingOff();//关闭缩放
	glyph->Update();
	return glyph->GetOutput();
}
/**
* @time	2022/01/04
* @brief DV3D::CartesianVector3dDatasetConstructor::setGridMergeUnit 设置网格合并的单位方阵
* @param vtkIdType zunit
* @param vtkIdType yunit
* @param vtkIdType xunit
* @return void
*/
void DV3D::CartesianVector3dDatasetConstructor::setGridMergeUnit(vtkIdType zunit, vtkIdType yunit, vtkIdType xunit)
{
	zUnit = zunit;
	yUnit = yunit;
	xUnit = xunit;
}
void DV3D::CartesianVector3dDatasetConstructor::initDatas()
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
	std::vector<float>& xList = grid[1];
	std::vector<float>& yList = grid[2];
	std::vector<float>& zList = grid[3];
	initGrid(xList.size(), yList.size(), zList.size());
	/*
		获取方向数据
	*/
	std::vector<vtkPoint3d> datas;
	generateVectorData(datas, varList);
	/*
		构建数据
	*/
	generatePolyData(datas, xList, yList, zList);
}
void DV3D::CartesianVector3dDatasetConstructor::initGrid(vtkIdType x, vtkIdType y, vtkIdType z)
{
	xGridSize = x;
	yGridSize = y;
	zGridSize = z;
}

/**
* @time	2022/01/04
* @brief DV3D::CartesianVector3dDatasetConstructor::generatePolyData 构建三维矢量数据
* @param std::vector<vtkPoint3d> & datas 方向数据
* @param std::vector<float> & xList  x-方向标尺
* @param std::vector<float> & yList  y-方向标尺
* @param std::vector<float> & zList  z-方向标尺
* @return void
*/
void DV3D::CartesianVector3dDatasetConstructor::generatePolyData(std::vector<vtkPoint3d>& datas, std::vector<float>& xList, std::vector<float>& yList, std::vector<float>& zList)
{
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkFloatArray> normal = vtkSmartPointer<vtkFloatArray>::New();//法向
	vtkSmartPointer<vtkFloatArray> vector = vtkSmartPointer<vtkFloatArray>::New();//方向
	vtkSmartPointer<vtkFloatArray> scalars = vtkSmartPointer<vtkFloatArray>::New();//大小
	normal->SetNumberOfComponents(3); //normal->SetName("Normals");
	vector->SetNumberOfComponents(3); //vector->SetName("Vector");
	double scalarMax = 0.0f;
	auto zSize = (zGridSize % zUnit > 0) ? (zGridSize / zUnit + 1) : (zGridSize / zUnit);
	auto ySize = (yGridSize % yUnit > 0) ? (yGridSize / yUnit + 1) : (yGridSize / yUnit);
	auto xSize = (xGridSize % xUnit > 0) ? (xGridSize / xUnit + 1) : (xGridSize / xUnit);
	for (auto zi = 0; zi < zSize; ++zi)
	{
		for (auto yi = 0; yi < ySize; ++yi)
		{
			for (auto xi = 0; xi < xSize; ++xi)
			{
				auto vectorPoint = getMergeVector(datas, zi, yi, xi);
				auto scalar = getScalar(vectorPoint);
				if (0.0f == scalar)
					continue;
				isNull = false;
				if (scalarMax < scalar)
					scalarMax = scalar;
				scalars->InsertNextTuple1(scalar);
				vectorPoint = vectorPoint.normalized();
				vector->InsertNextTuple3(vectorPoint.x(), vectorPoint.y(), vectorPoint.z());
				points->InsertNextPoint(xList[xi * xUnit], yList[yi * yUnit], zList[zi * zUnit]);
				normal->InsertNextTuple3(1.0, 1.0, 1.0);
			}
		}
	}
	/*
		场值为空，直接返回
	*/
	if (isNull)
		return;
	polyData = vtkSmartPointer<vtkPolyData>::New();
	polyData->SetPoints(points);
	polyData->GetPointData()->SetScalars(scalars);
	polyData->GetPointData()->SetVectors(vector);
	polyData->GetPointData()->SetNormals(normal);
	//计算缩放因子
	double scaleFactorX = (xList[xGridSize - 1] - xList[0]) / (xGridSize / xUnit);
	double scaleFactorY = (yList[yGridSize - 1] - yList[0]) / (yGridSize / yUnit);
	double scaleFactorZ = (zList[zGridSize - 1] - zList[0]) / (zGridSize / zUnit);
	scaleFactor = sqrt(scaleFactorX * scaleFactorX +
		scaleFactorY * scaleFactorY +
		scaleFactorZ * scaleFactorZ);
	scaleFactor /= scalarMax;
}

/**
* @time	2022/01/04
* @brief DV3D::CartesianVector3dDatasetConstructor::generateVectorData 获取方向数据
* @param std::vector<vtkPoint3d> & datas
* @param std::vector<float> & varList
* @return void
*/
void DV3D::CartesianVector3dDatasetConstructor::generateVectorData(std::vector<vtkPoint3d>& datas, std::vector<float>& varList)
{
	datas.clear();
	datas.reserve(xGridSize * yGridSize * zGridSize);
	auto iter = varList.begin();
	while (iter != varList.end())
	{
		auto normalX = *iter; iter++;
		auto normalY = *iter; iter++;
		auto normalZ = *iter; iter++;
		datas.push_back(vtkPoint3d(normalX, normalY, normalZ));
	}
}
vtkIdType DV3D::CartesianVector3dDatasetConstructor::getPointId(vtkIdType zi, vtkIdType yi, vtkIdType xi)
{
	return (zi * xGridSize * yGridSize + yi * xGridSize + xi);
}
/**
* @time	2021/12/31
* @brief DV3D::CartesianVector3dDatasetConstructor::getMergeVector 更具单位进行合并矢量
* @param std::vector<std::vector<vtkPoint3d>> & datas
* @param vtkIdType zi
* @param vtkIdType yi
* @param vtkIdType xi
* @return DV3D::vtkPoint3d
*/
DV3D::vtkPoint3d DV3D::CartesianVector3dDatasetConstructor::getMergeVector(
	std::vector<vtkPoint3d>& datas,
	vtkIdType zIndex,
	vtkIdType yIndex,
	vtkIdType xIndex)
{
	/*
		获取出矢量数据，并按照zUnit*yUnit*xUnit为一个单位网格的方式进行合并
	*/
	vtkPoint3d vectorPoint(0.0, 0.0, 0.0);
	//获取大小
	for (auto zUniti = 0; zUniti < zUnit; zUniti++)
		for (auto yUniti = 0; yUniti < yUnit; yUniti++)
			for (auto xUniti = 0; xUniti < xUnit; xUniti++)
			{
				auto pointId = getPointId(zIndex * zUnit + zUniti, yIndex * yUnit + yUniti, xIndex * xUnit + xUniti);
				if (pointId >= (xGridSize * yGridSize * zGridSize))
					continue;
				vectorPoint += datas[pointId];
			}
	return vectorPoint;
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