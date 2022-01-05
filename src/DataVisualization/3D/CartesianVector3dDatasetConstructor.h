#pragma once
#include "dataSetConstructor.h"
#include "QVector3D"
#include "vtkPoints.h"
#include "vtkPolyData.h"
namespace DV3D
{
	using vtkPoint3d = QVector3D;
	class CartesianVector3dDatasetConstructor :public DataSetConstructorH5
	{
	public:
		CartesianVector3dDatasetConstructor();
		CartesianVector3dDatasetConstructor(vtkIdType zunit,vtkIdType yunit,vtkIdType xunit);
		~CartesianVector3dDatasetConstructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
		void setGridMergeUnit(vtkIdType zunit, vtkIdType yunit, vtkIdType xunit);
	protected:
		void initDatas();
		void initGrid(vtkIdType x,vtkIdType y,vtkIdType z);
		virtual void generatePolyData(std::vector<vtkPoint3d>& datas,
			std::vector<float>& xList,
			std::vector<float>& yList,
			std::vector<float>& zList);
		void generateVectorData(std::vector<vtkPoint3d>& datas,std::vector<float>& varList);
		vtkIdType getPointId(vtkIdType zi,vtkIdType yi,vtkIdType xi);
		vtkPoint3d getMergeVector(std::vector<vtkPoint3d>& datas,vtkIdType zi,vtkIdType yi,vtkIdType xi);
	protected:
		vtkSmartPointer<vtkPolyData> polyData;
		vtkIdType xGridSize, yGridSize, zGridSize;
		vtkIdType xUnit, yUnit, zUnit;//矢量网格的合并方阵
		double scaleFactor;//缩放因子
	};


	double getScalar(vtkPoint3d);
	std::vector<std::string> vStringSplit(const  std::string& s, const std::string& delim);
}

