#include "PolarContourFliter.h"
#include "vtkObjectFactory.h"
#include "vtkInformationVector.h"
#include "vtkInformation.h"
#include "vtkArcSource.h"
#include"vtkFloatArray.h"
#include "vtkPointData.h"

vtkStandardNewMacro(PolarContourFilter);

void PolarContourFilter::PrintSelf(ostream& os, vtkIndent indent)
{
	this->Superclass::PrintSelf(os, indent);
	Rotation = 20;
	rGridSize = 0;
	thetaGridSize = 0;
	zGridSize = 0;
}

void PolarContourFilter::SetDimensions(int r, int theta, int z)
{
	rGridSize = r;
	thetaGridSize = theta;
	zGridSize = z;
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
	//获取多边形数据
	vtkPolyData* input = vtkPolyData::SafeDownCast(inInfo->Get(vtkDataObject::DATA_OBJECT()));
	vtkPolyData* output = vtkPolyData::SafeDownCast(outInfo->Get(vtkDataObject::DATA_OBJECT()));
	vtkIdType numPts, numCells;
	numPts = input->GetNumberOfPoints();
	//获取点云
	auto points = input->GetPoints();
	auto scalars = input->GetPointData()->GetScalars();
	for (auto z = 0; z < zGridSize; ++z)
	{
		for (auto thetai = 0; thetai < thetaGridSize - 1; ++thetai)
		{
			for (auto r = 0; r < rGridSize; r++)
			{
				vtkIdType id1 = getPointId(r, thetai, z);
				vtkIdType id2 = getPointId(r, thetai + 1, z);
				auto p1 = getPoint(points, id1);
				auto p2 = getPoint(points, id2);
			}
		}
	}
	return 0;
}
int PolarContourFilter::getPointId(vtkIdType ri, vtkIdType thetai, vtkIdType zi)
{
	return (ri + thetai * rGridSize + zi * rGridSize * thetaGridSize);
}
/**
* @time	2021/12/22
* @brief PolarContourFilter::getPoint 获取点
* @param vtkSmartPointer<vtkPoints>
* @param vtkIdType id
* @return std::vector<double>
*/
std::vector<double> PolarContourFilter::getPoint(vtkSmartPointer<vtkPoints> points, vtkIdType id)
{
	std::vector<double> point;
	point.reserve(3);
	auto ptr = points->GetPoint(id);
	point.push_back(ptr[0]);
	point.push_back(ptr[1]);
	point.push_back(ptr[2]);
	return point;
}
