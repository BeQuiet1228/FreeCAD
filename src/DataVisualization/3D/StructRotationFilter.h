#pragma once
#include "vtkFiltersModelingModule.h" // For export macro
#include "vtkPolyDataAlgorithm.h"
#include "vtkUnstructuredGridAlgorithm.h"
#include "vtkPolydata.h"
#include "vtkSmartPointer.h"
class StructRotationFilter
{
public:
	StructRotationFilter();
	~StructRotationFilter();
	/*
		设置平滑度
	*/
	void SetResolution(int);
	int GetResolution();
	/*
		设置角度
	*/
	
	void SetAngle(double);
	double GetAngle();
	/*
		传入面数据
	*/
	void SetInputPolyData(vtkSmartPointer<vtkPolyData> data);
	void Updata();
	vtkSmartPointer<vtkUnstructuredGrid> getOuput();
protected:
	
	//int RequestData(vtkInformation*, vtkInformationVector**, vtkInformationVector*);
	double Angle;
	int Resolution;
	vtkSmartPointer<vtkPolyData> polydata;
	vtkSmartPointer<vtkUnstructuredGrid> ugrid;
	bool isSuccess;
private:
	StructRotationFilter(const StructRotationFilter&);
	void operator=(const StructRotationFilter&);
	
};