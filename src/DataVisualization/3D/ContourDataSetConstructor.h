#pragma once
#ifndef CONTOURDATASETCONSTRUCTOR_H_
#define CONTOURDATASETCONSTRUCTOR_H_
#include "dataSetConstructor.h"
#include "vtkPoints.h"

namespace DV3D
{
	class ContourDatasetConstructor :public DataSetConstructorH5
	{
	public:
		ContourDatasetConstructor();
		~ContourDatasetConstructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
		void initData();
	protected:
		vtkSmartPointer<vtkPoints> points;
	};
};
#endif // !CONTOURDATASETCONSTRUCTOR_H_
