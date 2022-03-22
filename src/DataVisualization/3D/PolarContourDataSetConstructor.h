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
		void setResolution(int);
	protected:
		void initData();
		void generateMapList(std::map<double, std::map<double, double>>& maplist);
		void generatePoints(std::map<double, std::map<double, double>>& maplist);
		void initGrid(vtkIdType zGrid,vtkIdType thetaGrid,vtkIdType rGrid);
		vtkIdType getPointId(vtkIdType thetai,vtkIdType ri);
	protected:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer<vtkFloatArray> scalar;
		int rGridSize, thetaGridSize, zGridSize;
		double polarZ;
		int mResolution;
		std::vector<double> angles;
	};
}
#endif