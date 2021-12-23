#pragma once
#include "vtkFiltersModelingModule.h"
#include "vtkPolyDataAlgorithm.h"
#include"vtkSmartPointer.h"
#include "vtkStructuredGrid.h"
#include "ArcCalc.h"
#include "map"
class PolarContour2dFilter :public vtkPolyDataAlgorithm
{
public:
	using PolarPoints = std::map<int, std::map<int, std::vector<DV3D::ArcCalc::ArcTextInfo>>>;
	vtkTypeMacro(PolarContour2dFilter, vtkPolyDataAlgorithm);
	void PrintSelf(ostream& os,vtkIndent indent);
	static PolarContour2dFilter* New();
	void SetDimensions(int r,int theta,int z);
	vtkSetMacro(Rotation,int);
	//Center
	void setCenter(double x, double y, double z);
	void setCenter(double* c);
	double* getCenter();
	vtkSmartPointer<vtkStructuredGrid> getStructuredGrid();
protected:
	PolarContour2dFilter();
	~PolarContour2dFilter() {}
	int RequestData(vtkInformation*, vtkInformationVector**, vtkInformationVector*);
	int getPointId(vtkIdType ri, vtkIdType thetai, vtkIdType zi);
	std::vector<DV3D::ArcCalc::ArcTextInfo> getArcTextinfo(double* p1,double* p2,double s1,double s2);
	std::vector<double> getPoint(vtkSmartPointer<vtkPoints>,vtkIdType id);
	vtkSmartPointer<vtkStructuredGrid> createGrid();
	void cleanRedundantPoint();
private:
	PolarContour2dFilter(const PolarContour2dFilter&);
	void operator =(const PolarContour2dFilter&);
	double mCenter[3];
	int Rotation;
	int rGridSize, thetaGridSize, zGridSize;
	//z-r-theta
	PolarPoints polarPoints;
	vtkSmartPointer<vtkStructuredGrid> grid;
};