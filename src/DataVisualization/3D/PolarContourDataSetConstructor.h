#pragma once
#ifndef POLARCONTOURDATASETCONSTRUCTOR_H_
#define POLARCONTOURDATASETCONSTRUCTOR_H_
#include "dataSetConstructor.h"
#include "vtkPoints.h"
#include "vtkFloatArray.h"
namespace DV3D
{
	class PolarContourDatasetConstructor :public DataSetConstructorH5
	{
	public:
		PolarContourDatasetConstructor();
		~PolarContourDatasetConstructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	protected:
		void initData();
	protected:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer<vtkFloatArray> scalar;
		int rGridSize, thetaGridSize, zGridSize;
		double polarZ;
	};
}
#endif