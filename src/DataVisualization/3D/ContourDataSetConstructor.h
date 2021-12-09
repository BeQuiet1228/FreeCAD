#pragma once
#ifndef CONTOURDATASETCONSTRUCTOR_H_
#define CONTOURDATASETCONSTRUCTOR_H_
#include "dataSetConstructor.h"
#include "vtkPoints.h"
#include "vtkFloatArray.h"
namespace DV
{
	class DirData;
}
namespace DV3D
{
	class ContourDatasetConstructor :public DataSetConstructorH5
	{
	public:
		ContourDatasetConstructor();
		~ContourDatasetConstructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	protected:
		void initData();
		void createPointsXy();
		void createPointsXz();
		void createPointsYz();
	protected:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer < vtkFloatArray >scaler;
		int xGridSize, yGridSize, zGridSize;
	};
};
#endif // !CONTOURDATASETCONSTRUCTOR_H_
