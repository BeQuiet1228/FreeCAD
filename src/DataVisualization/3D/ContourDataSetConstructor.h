#pragma once
#ifndef CONTOURDATASETCONSTRUCTOR_H_
#define CONTOURDATASETCONSTRUCTOR_H_
#include "dataSetConstructor.h"
#include "vtkPoints.h"
#include "vtkFloatArray.h"
#include "DataVisualization/ContourData.h"
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
		void createPointsXy(std::vector<DV::ContourData::Grid>& data, float z);
		void createPointsXz(std::vector<DV::ContourData::Grid>& data, float y);
		void createPointsYz(std::vector<DV::ContourData::Grid>& data, float x);
		void createPointsRz(std::vector<DV::ContourData::Grid>& data, float theta);
		void setGridSize(int xGrid,int yGrid,int zGrid);
	protected:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer < vtkFloatArray >scaler;
		int xGridSize, yGridSize, zGridSize;
		bool isNeg;
	};
};
#endif // !CONTOURDATASETCONSTRUCTOR_H_
