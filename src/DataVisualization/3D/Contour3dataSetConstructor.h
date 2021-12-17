#pragma once
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
			const vtkIdType& xs, 
			const vtkIdType& ys, 
			const vtkIdType& zs);
		vtkIdType getpointId(
			const vtkIdType& xi,
			const vtkIdType& yi,
			const vtkIdType& zi);
	private:
		vtkSmartPointer<vtkPoints> points;
		vtkSmartPointer<vtkFloatArray> scalars;
		vtkIdType xGridSize, yGridSize, zGridSize;
	};
}
