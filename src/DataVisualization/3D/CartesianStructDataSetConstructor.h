#pragma  once
#include "dataSetConstructor.h"
#include <vtkDataSet.h>
#include <vtkSmartPointer.h>
#include <vtkPoints.h>
namespace DV3D {
	class CartesianStructDataSetConstructor :public DataSetConstructorH5 {
	public:
		CartesianStructDataSetConstructor();
		~CartesianStructDataSetConstructor();


	public:
		vtkSmartPointer<vtkDataSet> creatDataset() override;

	private:
		//更加三维大小获取点的索引
		int getPointID(const int& xi, const int& yi, const int& zi);
		//初始化网格的所有点
		void initPoints();
		//初始化网格大小
		void initGridsize(unsigned int xSize, unsigned ySize, unsigned int zSize);
	private:
		//数据的所有点
		vtkSmartPointer<vtkPoints> points;
		//网格大小
		unsigned int xSize, ySize, zSize;
	};
}