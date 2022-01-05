#include "StructRotationFilter.h"
#include "vtkObjectFactory.h"
#include "vtkInformation.h"
#include "vtkInformationVector.h"
#include "vtkMath.h"
#include "vtkPointData.h"
#include "vtkCellData.h"
vtkStandardNewMacro(StructRotationFilter);
double getTheta(double* x);
void StructRotationFilter::PrintSelf(ostream& os, vtkIndent indent)
{
	this->Superclass::PrintSelf(os, indent);
	os << indent << "Resolution: " << this->Resolution << "\n";
	os << indent << "Angle: " << this->Angle << "\n";
}

StructRotationFilter::StructRotationFilter()
{
	Angle = 360.0;
	Resolution = 12;
}

StructRotationFilter::~StructRotationFilter()
{

}

int StructRotationFilter::RequestData(
	vtkInformation* vtkNotUsed(request),
	vtkInformationVector** inputVector,
	vtkInformationVector* outputVector)
{
	//获取对象信息
	vtkInformation* inInfo = inputVector[0]->GetInformationObject(0);
	vtkInformation* outInfo = outputVector->GetInformationObject(0);

	vtkPolyData* input = vtkPolyData::SafeDownCast(
		inInfo->Get(vtkDataObject::DATA_OBJECT()));
	vtkPolyData* output = vtkPolyData::SafeDownCast(
		outInfo->Get(vtkDataObject::DATA_OBJECT()));

	vtkIdType numPts, numCell;
	vtkPointData* pd = input->GetPointData();
	vtkCellData* cd = input->GetCellData();
	vtkPolyData* mesh;
	vtkPoints* inPts=input->GetPoints();
	vtkCellArray* polys=input->GetPolys();
	/*
		计算点位
	*/
	numPts = input->GetNumberOfPoints();
	numCell = input->GetNumberOfCells();
	if (numPts < 1 || numCell < 1)
	{
		vtkErrorMacro(<< "no data to extrude");
		return 1;
	}
	/*
		按z-axis旋转生成新的点
	*/
	vtkIdType newNumPts = numPts * (Resolution + 1);
	vtkPoints* newPts = vtkPoints::New();
	newPts->Allocate(newNumPts);
	double x[3], newX[3];
	auto angInvertal = vtkMath::RadiansFromDegrees(Angle) / Resolution;
	for (auto i = 1; i <= this->Resolution; ++i)
	{
		for (auto ptId = 0; ptId < numPts; ++ptId)
		{
			inPts->GetPoint(ptId, x);
			//点位旋转 z-axis
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
	/*
		构建多面体
	*/
	output->SetPoints(newPts);
	for (auto i = 1; i <= this->Resolution; ++i)
	{
		for (auto ptId = 0; ptId < numCell; ++ptId)
		{
			vtkIdType pNum, * cell;
			input->GetCellPoints(ptId, pNum, cell);///
			if (pNum < 4)
			{
				vtkErrorMacro(<< "初始多边形少于4个点");
				return 0;
			}
			std::vector<vtkIdType> celldataUp;
			std::vector<vtkIdType> celldataDown;
			for (auto ci=0;ci<pNum;++ci)
			{
				celldataUp.push_back(cell[ci]+(i - 1)*Resolution);
				celldataDown.push_back(cell[ci]+i*Resolution);
			}
			celldataUp.insert(celldataUp.end(), celldataDown.begin(), celldataDown.end());
			output->InsertNextCell(VTK_VOXEL,8,celldataUp.data());
		}
	}
	return 1;
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