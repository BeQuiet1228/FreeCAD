#include "StructRotationFilter.h"
#include "vtkObjectFactory.h"
#include "vtkInformation.h"
#include "vtkInformationVector.h"
#include "vtkMath.h"
#include "vtkPointData.h"
#include "vtkCellData.h"
#include "vtkUnstructuredGrid.h"
#include "vtkSmartPointer.h"
#include "vtkRotationalExtrusionFilter.h"
double getTheta(double* x);
void StructRotationFilter::SetInputPolyData(vtkSmartPointer<vtkPolyData> data)
{
	polydata->DeepCopy(data);
}



StructRotationFilter::StructRotationFilter()
{
	Angle = 360.0;
	Resolution = 12;
	ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	polydata = vtkSmartPointer<vtkPolyData>::New();
	isSuccess = false;
}

StructRotationFilter::~StructRotationFilter()
{

}

void StructRotationFilter::SetResolution(int val)
{
	Resolution = val;
}

int StructRotationFilter::GetResolution()
{
	return Resolution;
}

void StructRotationFilter::SetAngle(double val)
{
	Angle = val;
}

double StructRotationFilter::GetAngle()
{
	return Angle;
}

void StructRotationFilter::Updata()
{
	/*
	*	计算点位
	*/
	auto numPts = polydata->GetNumberOfPoints();
	auto numCell = polydata->GetNumberOfCells();
	if (numPts < 1 || numPts < 1)
		return;
	/*
		按z-axis旋转生成新的点
	*/
	auto angInvertal = vtkMath::RadiansFromDegrees(Angle) / Resolution;
	auto newNumPts = numPts * (Resolution + 1);
	vtkPoints* newPts = vtkPoints::New();
	newPts->Allocate(newNumPts);
	auto inpts = polydata->GetPoints();
	double x[3], newX[3];
	for (auto i = 0; i < numPts; ++i)
		newPts->InsertPoint(i,inpts->GetPoint(i));
	for (auto i = 1; i <= this->Resolution; ++i)
	{
		for (auto ptId = 0; ptId < numPts; ++ptId)
		{
			inpts->GetPoint(ptId, x);
			//点位旋转
			auto radio = sqrt(x[0] * x[0] + x[1] * x[1]);
			if (radio > 0.0)
			{
				auto theta = getTheta(x);
				newX[0] = radio * cos(i * angInvertal + theta);
				newX[1] = radio * sin(i * angInvertal + theta);
				newX[2] = x[2];
			}
			else
			{
				newX[0] = x[0];
				newX[1] = x[1];
				newX[2] = x[2];

			}
			newPts->InsertPoint(ptId + i * numPts, newX);
		}
	}
	
	//vtkSmartPointer<vtkRotationalExtrusionFilter> filter = vtkSmartPointer<vtkRotationalExtrusionFilter>::New();
	//filter->SetInputData(polydata);
	//filter->SetResolution(Resolution);
	//filter->SetAngle(Angle);
	//filter->Update();
	/*
		构建多面体
	*/
	vtkPolyData* mesh;
	mesh = vtkPolyData::New();
	mesh->SetPoints(polydata->GetPoints());
	mesh->SetVerts(polydata->GetVerts());
	mesh->SetLines(polydata->GetLines());
	mesh->SetPolys(polydata->GetPolys());
	mesh->SetStrips(polydata->GetStrips());
	vtkPolyData* outMesh = vtkPolyData::New();
	if (polydata->GetPolys() || polydata->GetStrips())
		mesh->BuildLinks();
	//ugrid->SetPoints(filter->GetOutput()->GetPoints());
	ugrid->SetPoints(newPts);
	for (auto i=1;i<=this->Resolution;++i)
	{
		for (auto ptId = 0; ptId < numCell/2; ++ptId)
		{
			vtkIdType pNum, * cell;
			mesh->GetCellPoints(ptId,pNum,cell);
			if (pNum < 4)
				return;
			std::vector<vtkIdType> celldataUp;
			std::vector<vtkIdType> celldataDown;
			for (auto ci = 0; ci < pNum; ++ci)
			{
				celldataUp.push_back(cell[ci]+(i-1)*numPts);
				celldataDown.push_back(cell[ci]+i*numPts);
			}
			celldataUp.insert(celldataUp.end(), celldataDown.begin(), celldataDown.end());
			ugrid->InsertNextCell(VTK_VOXEL,celldataUp.size(),celldataUp.data());
		}
	}
	isSuccess = true;
}

vtkSmartPointer<vtkUnstructuredGrid> StructRotationFilter::getOuput()
{
	if (!isSuccess)
		return nullptr;
	return ugrid;
}

double getTheta(double* x)
{
	double theta = 0.0f;
	auto radio = sqrt(x[0] * x[0] + x[1] * x[1]);
	if (radio > 0.0)
	{
		auto tempd = x[0] / radio;
		tempd = (tempd > 1.0 ? 1.0 : (tempd < -1.0 ? -1.0 : tempd));
		theta = acos(tempd);
		tempd = x[1] / radio;
		tempd = (tempd > 1.0 ? 1.0 : (tempd < -1.0 ? -1.0 : tempd));
		auto psi = asin(tempd);
		if (psi < (vtkMath::Pi() / 2.0))
			theta = (theta < (vtkMath::Pi() / 2.0) ? (2.0 * vtkMath::Pi() + psi) : (vtkMath::Pi() - psi));
	}
	return theta;
}