#pragma once
#include "vtkFiltersModelingModule.h"
#include "vtkPolyDataAlgorithm.h"
#include"vtkSmartPointer.h"
#include"vtkArcSource.h"
class PolarContourFilter :public vtkPolyDataAlgorithm
{
public:
	vtkTypeMacro(PolarContourFilter, vtkPolyDataAlgorithm);
	void PrintSelf(ostream& os,vtkIndent indent);
	static PolarContourFilter* New();
	void SetDimensions(int r,int theta,int z);
	vtkSetMacro(Rotation,int);
protected:
	PolarContourFilter();
	~PolarContourFilter() {}
	int RequestData(vtkInformation*, vtkInformationVector**, vtkInformationVector*);
	int getPointId(vtkIdType& ri, vtkIdType& thetai, vtkIdType& zi);
private:
	PolarContourFilter(const PolarContourFilter&);
	void operator =(const PolarContourFilter&);
	int Rotation;
	int rGridSize, thetaGridSize, zGridSize;
	vtkSmartPointer<vtkArcSource> arcTools;
	
};