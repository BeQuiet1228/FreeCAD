#pragma once
#ifndef POLAR_STRUCT_DATASET_CONSTRUCTOE_H_
#define POLAR_STRUCT_DATASET_CONSTRUCTOE_H_
#include "dataSetConstructor.h"
#include <vtkPoints.h>
namespace DV3D {
	using PolarDatas = std::vector<std::vector<float>>;
	using PolarIndes = std::vector<std::vector<__int64>>;
	//角向结构体的数据类
	class PolarStructDaraSetConstruct :public DataSetConstructorH5
	{
	public:
		PolarStructDaraSetConstruct();
		~PolarStructDaraSetConstruct();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	public:
		__int64 getPointId(const long long& thetai, const long long& ri, const long long& zi);
		//初始化网格的所有点
		void initPoints();
		//初始化网格大小
	protected:
		virtual PolarDatas getPolarDatas();
		virtual PolarIndes getPolarIndex();
		void initGridsize(unsigned long long rSize, unsigned long long thetaSize, unsigned long long zSize);
	protected:
		vtkSmartPointer<vtkPoints> points;
		//网格大小
		unsigned long long rSize, thetaSize, zSize;
	};

};
#endif
