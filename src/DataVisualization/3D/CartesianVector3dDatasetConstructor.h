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
	class CartesianVector3dDatasetConstructor :public DataSetConstructorH5S
	{
	public:
		CartesianVector3dDatasetConstructor();
		~CartesianVector3dDatasetConstructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	protected:
		void initDatas();
		void loadStructPoint();
		void initGrid(vtkIdType x,vtkIdType y,vtkIdType z);
		std::vector<vtkPoint3d> generateVectorData(Hdf5Data& h5d);
		void mergeDatas(std::vector<std::vector<vtkPoint3d>>&);
		vtkIdType getPointId(vtkIdType zi,vtkIdType yi,vtkIdType xi);
		AxisDir getAxisDir(Hdf5Data& h5d);
	private:
		vtkSmartPointer<vtkPoints> structPoint;
		vtkSmartPointer<vtkPolyData> polyData;
		vtkIdType xGridSize, yGridSize, zGridSize;
		double scaleFactor;//Ëõ·ÅÒò×Ó
	};
}