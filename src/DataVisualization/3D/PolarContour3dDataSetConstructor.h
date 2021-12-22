#pragma once
#ifndef  POLARCONTOUR3DDATASETCONSTRUCTOR_H_
#define POLARCONTOUR3DDATASETCONSTRUCTOR_H_
#include "dataSetConstructor.h"
#include "vtkPoints.h"
#include "vtkFloatArray.h"
namespace DV3D
{
	class PolarContour3dDatasetConstructor :public DataSetConstructorH5
	{
	public:
		PolarContour3dDatasetConstructor();
		~PolarContour3dDatasetConstructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	protected:
		void initPoints();
		void initGrid(int rs,int thetas,int zs);
		vtkIdType getpointId(const vtkIdType& ri,const vtkIdType& thetai,const vtkIdType& zi );
	private:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer<vtkFloatArray> scalars;
		vtkIdType rGridSize, thetaGridSize, zGridSize;
	};
}
#endif