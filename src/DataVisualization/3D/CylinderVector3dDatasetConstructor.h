#pragma once
#include "dataSetConstructor.h"
#include "vtkPoints.h"
#include "vtkPolyData.h"
#include "CartesianVector3dDatasetConstructor.h"
namespace DV3D
{
	class CylinderVector3dDatasetContructor :public DataSetConstructorH5
	{
	public:
		CylinderVector3dDatasetContructor();
		CylinderVector3dDatasetContructor(vtkIdType zunit, vtkIdType thetaunit, vtkIdType runit);
		~CylinderVector3dDatasetContructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
		void setGridMergeUnit(vtkIdType zunit, vtkIdType thetaunit, vtkIdType runit);
	protected:
		vtkIdType getPointId(vtkIdType zi,vtkIdType thetai,vtkIdType ri);
		void initData();
		void initGridSize(vtkIdType zgrid,vtkIdType thetagrid,vtkIdType rgrid);
		void generateVectorData(std::vector<vtkPoint3d>& datas, std::vector<float>& varList);
		void generatePolyData(
			std::vector<vtkPoint3d>& datas, 
			std::vector<float>& rList, 
			std::vector<float>& thetaList, 
			std::vector<float>& zList);
		vtkPoint3d getMergeVector(
			std::vector<vtkPoint3d>& datas, 
			std::vector<float>& zlist, 
			std::vector<float>& thetaList, 
			std::vector<float>& rList,
			vtkIdType zi, 
			vtkIdType thetai, 
			vtkIdType ri);
	private:
		vtkIdType rGridSize, thetaGridSize, zGridSize;//网格标尺数
		vtkIdType rUnit, thetaUnit, zUnit;//合并方阵
		double scaleFactor;//缩放因子
		vtkSmartPointer<vtkPolyData> polyData;
	};
};