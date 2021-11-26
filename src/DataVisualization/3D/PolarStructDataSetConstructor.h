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
		enum DataType
		{
			Plane=0,
			PlaneHalf=1,
			nomal
		};
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	public:
		__int64 getPointId(const __int64& thetai, const __int64& ri, const __int64& zi);
		//初始化网格的所有点
		void initPoints();
		//初始化网格大小
	protected:
		virtual PolarDatas getPolarDatas();
		virtual PolarIndes getPolarIndex();
		void initGridsize(unsigned __int64 rSize,unsigned __int64 thetaSize,unsigned __int64 zSize);
		DataType getThetaDatas();
		vtkSmartPointer<vtkDataSet> creatDatasetnormal();
		vtkSmartPointer<vtkDataSet> creatDatasetPlaneHalf();
		//vtkSmartPointer<vtkDataSet> creatDatasetPlane();
	protected:
		vtkSmartPointer<vtkPoints> points;
		//网格大小
		//unsigned __int64 xSize, ySize, zSize;
		unsigned __int64 rSize, thetaSize,zSize;
	};

};
#endif
