#include "PolarContourFliter.h"
#include "vtkObjectFactory.h"
#include "vtkInformationVector.h"
#include "vtkInformation.h"
#include "vtkArcSource.h"
#include"vtkFloatArray.h"

vtkStandardNewMacro(PolarContourFilter);

void PolarContourFilter::PrintSelf(ostream& os, vtkIndent indent)
{
	this->Superclass::PrintSelf(os, indent);
	Rotation = 20;
	rGridSize = 0;
	thetaGridSize = 0; 
	zGridSize = 0;
	arcTools = vtkSmartPointer<vtkArcSource>::New();
}
PolarContourFilter::PolarContourFilter()
{

}
int PolarContourFilter::RequestData(
	vtkInformation* vtkNotUsed(request), 
	vtkInformationVector** inputVector, 
	vtkInformationVector* outputVector)
{
	vtkInformation* inInfo = inputVector[0]->GetInformationObject(0);
	vtkInformation* outInfo = outputVector->GetInformationObject(0);
	//��ȡ���������
	vtkPolyData* input = vtkPolyData::SafeDownCast(inInfo->Get(vtkDataObject::DATA_OBJECT()));
	vtkPolyData* output = vtkPolyData::SafeDownCast(outInfo->Get(vtkDataObject::DATA_OBJECT()));
	vtkIdType numPts, numCells;
	numPts = input->GetNumberOfPoints();
	numCells = input->GetNumberOfCells();
	//����Բ
	auto points = input->GetPoints();
	//
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkFloatArray> scalars = vtkSmartPointer<vtkFloatArray>::New();
	for (auto z = 0; z < zGridSize; ++z)
	{
		for (auto thetai = 0; thetai < thetaGridSize-1; ++thetai)
		{
			for (auto r = 0; r < rGridSize; r++)
			{
				auto point1 = points->GetPoint(getPointId(r,thetai,z));
				auto point2=points->GetPoint(getPointId(r,thetai+1,z));
				arcTools->setCenter(0.0,0.0,0.0);
				arcTools->SetPoint1(point1);
				arcTools->setPoint2(point2);
				arcTools->SetRotation();
			}
		}
	}
	
	return 0;
}
int PolarContourFilter::getPointId(vtkIdType& ri, vtkIdType& thetai, vtkIdType& zi)
{
	return (ri + thetai * rGridSize + zi * rGridSize * thetaGridSize);
}