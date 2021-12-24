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
		void setResolution(int);
	protected:
		void initPoints();
		void initGrid(int rs,int thetas,int zs);
		vtkIdType getpointId(const vtkIdType& ri,const vtkIdType& thetai,const vtkIdType& zi );
		void generateMapList(
			std::map<double, std::map<double, std::map<double, double>>>& maplist,
			std::vector<std::vector<float>>& grid);
		void generatePoints(std::map<double, std::map<double, std::map<double, double>>>& maplist);
	private:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer<vtkFloatArray> scalars;
		vtkIdType rGridSize, thetaGridSize, zGridSize;
		int mResolution;
		std::vector<double> angles;
	};
}
#endif