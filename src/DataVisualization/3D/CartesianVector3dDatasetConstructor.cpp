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
	xGridSize(0), yGridSize(0), zGridSize(0), scaleFactor(0.0f)
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
	glyph->SetScaleFactor(scaleFactor*0.5);//设置缩放因子
	glyph->SetSourceConnection(arrowSource->GetOutputPort());
	glyph->SetScaleModeToDataScalingOff();//关闭缩放
	glyph->Update();
	return glyph->GetOutput();
}

void DV3D::CartesianVector3dDatasetConstructor::initDatas()
{
	//获取矢量数据
	auto h5ds = getHdf5Datas();
	//将结构数据处理成点位,z-y-x
	loadStructPoint();
	//生成矢量数据
	std::vector<std::vector<vtkPoint3d>> vectorDatas;
	vectorDatas.reserve(3);
	for (auto iter = h5ds.begin(); iter != h5ds.end(); iter++)
		vectorDatas.push_back(generateVectorData(*iter));
	//合并
	mergeDatas(vectorDatas);
}

void DV3D::CartesianVector3dDatasetConstructor::loadStructPoint()
{
	//获取结构数据
	auto structData = getStructData();
	assert(structData.listDataSet.size() == 4 && "list DataSet size is not 4");
	std::vector<std::vector<float>> grid;
	grid.reserve(4);
	for (auto i = 0; i < structData.listDataSet.size(); ++i)
	{
		std::vector<float> d;
		Hdf5IO::getValue(structData.listDataSet.at(i), d);
		grid.push_back(d);
	}
	std::vector<float>& xList = grid[0];
	std::vector<float>& yList = grid[1];
	std::vector<float>& zList = grid[2];
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
	double scaleFactorX = (xList[xGridSize - 1] - xList[0]) / xGridSize;
	double scaleFactorY = (yList[yGridSize - 1] - yList[0]) / yGridSize;
	double scaleFactorZ = (zList[zGridSize - 1] - zList[0]) / zGridSize;
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
std::vector<DV3D::vtkPoint3d> DV3D::CartesianVector3dDatasetConstructor::generateVectorData(Hdf5Data& h5d)
{
	//获取数据的方向
	vtkPoint3d vectorP(0.0, 0.0, 0.0);
	switch (getAxisDir(h5d))
	{
	case AxisDir::X:
		vectorP.setX(1.0);	break;
	case AxisDir::Y:
		vectorP.setY(1.0);	break;
	case AxisDir::Z:
		vectorP.setZ(1.0);	break;
	}
	std::vector<float> vaList;
	Hdf5IO::getValue(h5d.listDataSet.at(0), vaList);
	std::vector<vtkPoint3d> datas;
	datas.reserve(xGridSize * yGridSize * zGridSize);
	for (auto zi = 0; zi < zGridSize; ++zi)
	{
		for (auto yi = 0; yi < yGridSize; ++yi)
		{
			for (auto xi = 0; xi < xGridSize; ++xi)
			{
				auto scalar = vaList[getPointId(zi, yi, xi)];
				vtkPoint3d p2 = vectorP * scalar;
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
void DV3D::CartesianVector3dDatasetConstructor::mergeDatas(std::vector<std::vector<vtkPoint3d>>& datas)
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
	int index = 0;
	for (auto zi = 0; zi < zGridSize; ++zi)
	{
		for (auto yi = 0; yi < yGridSize; ++yi)
		{
			for (auto xi = 0; xi < xGridSize; ++xi)
			{
				vtkPoint3d vectorPoint(0.0, 0.0, 0.0);
				auto iter = datas.begin();
				while (iter != datas.end())
				{
					vectorPoint += (*iter)[getPointId(zi, yi, xi)];
					iter++;
				}
				//获取大小
				auto saclar = getScalar(vectorPoint);
				if (0.0f == saclar)
					continue;
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
	polyData = vtkSmartPointer<vtkPolyData>::New();
	polyData->SetPoints(points);
	polyData->GetPointData()->SetScalars(scalars);
	polyData->GetPointData()->SetVectors(vector);
	polyData->GetPointData()->SetNormals(normal);
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