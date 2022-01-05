#pragma once
#include "vtkFiltersModelingModule.h" // For export macro
#include "vtkPolyDataAlgorithm.h"
class StructRotationFilter :public vtkPolyDataAlgorithm
{
public:
	vtkTypeMacro(StructRotationFilter, vtkPolyDataAlgorithm);
	void PrintSelf(ostream& os, vtkIndent indent);
	static StructRotationFilter* New();
	/*
		设置平滑度
	*/
	vtkSetClampMacro(Resolution, int, 1, VTK_INT_MAX);
	vtkGetMacro(Resolution, int);
	/*
		设置角度
	*/
	vtkSetMacro(Angle, double);
	vtkGetMacro(Angle, double);
protected:
	StructRotationFilter();
	~StructRotationFilter();
	int RequestData(vtkInformation*, vtkInformationVector**, vtkInformationVector*);
	double Angle;
	int Resolution;
private:
	StructRotationFilter(const StructRotationFilter&);
	void operator=(const StructRotationFilter&);
};