#ifndef CONTOURDATASETCONSTRUCTOR_H_
#define CONTOURDATASETCONSTRUCTOR_H_
#include"dataSetConstructor.h"
#include"vtkPoints.h"
#include "vtkFloatArray.h"
#include"vtkType.h"
namespace DV3D
{
	class Contour3dDatasetConstructor :public DataSetConstructorH5
	{
	public :
		Contour3dDatasetConstructor();
		~Contour3dDatasetConstructor();
	public:
		vtkSmartPointer<vtkDataSet> creatDataset();
	protected:
		void initPoints();
		void initGrid(
			unsigned long long xs, 
			unsigned long long ys, 
			unsigned long long zs);
		vtkIdType getpointId(
			unsigned long long xi,
			unsigned long long yi, 
			unsigned long long zi);
	private:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer<vtkFloatArray> scalars;
		unsigned long long xGridSize, yGridSize, zGridSize;
	};
}
#endif 
