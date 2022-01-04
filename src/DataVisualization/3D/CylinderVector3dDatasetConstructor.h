#pragma once
#include "dataSetConstructor.h"
#include "vtkPoints.h"
#include "vtkPolyData.h"
#include "CartesianVector3dDatasetConstructor.h"
namespace DV3D
{
	class CylinderVector3dDatasetContructor :public CartesianVector3dDatasetConstructor
	{
	public:
		CylinderVector3dDatasetContructor();
		CylinderVector3dDatasetContructor(vtkIdType zunit, vtkIdType thetaunit, vtkIdType runit);
		~CylinderVector3dDatasetContructor();
	protected:
		virtual void generatePolyData(
			std::vector<vtkPoint3d>& datas, 
			std::vector<float>& rList, 
			std::vector<float>& thetaList, 
			std::vector<float>& zList) override;
		vtkPoint3d getMergeVector(
			std::vector<vtkPoint3d>& datas, 
			std::vector<float>& zlist, 
			std::vector<float>& thetaList, 
			std::vector<float>& rList,
			vtkIdType zi, 
			vtkIdType thetai, 
			vtkIdType ri);
	};
};