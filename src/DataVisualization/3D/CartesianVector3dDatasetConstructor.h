#pragma once
#include "dataSetConstructor.h"
#include "QVector3D"
#include "vtkPoints.h"
#include "vtkPolyData.h"
namespace DV3D
{
	using vtkPoint3d = QVector3D;
	enum AxisDir {
		X=0,
		Y,
		Z,
		R,
		Theta,
		Axis_NUll
	};
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
		void loadStructPoint();
		void initGrid(vtkIdType x,vtkIdType y,vtkIdType z);
		std::vector<vtkPoint3d> generateVectorData();
		void mergeDatas(std::vector<vtkPoint3d>&);
		vtkIdType getPointId(vtkIdType zi,vtkIdType yi,vtkIdType xi);
		AxisDir getAxisDir(Hdf5Data& h5d);
		//测试
		vtkPoint3d getMergeVector(
			std::vector<vtkPoint3d>& datas,
			vtkIdType zi,vtkIdType yi,vtkIdType xi);
	private:
		vtkSmartPointer<vtkPoints> structPoint;
		vtkSmartPointer<vtkPolyData> polyData;
		vtkIdType xGridSize, yGridSize, zGridSize;
		vtkIdType xUnit, yUnit, zUnit;//矢量网格的合并方阵
		double scaleFactor;//缩放因子
	};
}