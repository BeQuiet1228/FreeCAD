#include "PolarContourFliter.h"
#include "vtkObjectFactory.h"
#include "vtkInformationVector.h"
#include "vtkInformation.h"
#include "vtkArcSource.h"
#include"vtkFloatArray.h"
#include "vtkPointData.h"
#include "vtkMath.h"
vtkStandardNewMacro(PolarContour2dFilter);

void PolarContour2dFilter::PrintSelf(ostream& os, vtkIndent indent)
{
	this->Superclass::PrintSelf(os, indent);
	Rotation = 20;
	rGridSize = 0;
	thetaGridSize = 0;
	zGridSize = 0;
}

void PolarContour2dFilter::SetDimensions(int r, int theta, int z)
{
	rGridSize = r;
	thetaGridSize = theta;
	zGridSize = z;
}

void PolarContour2dFilter::setCenter(double* c)
{
	mCenter[0] = c[0];
	mCenter[1] = c[1];
	mCenter[2] = c[2];
}

void PolarContour2dFilter::setCenter(double x, double y, double z)
{
	mCenter[0] = x;
	mCenter[1] = y;
	mCenter[2] = z;
}

double* PolarContour2dFilter::getCenter()
{
	return mCenter;
}

vtkSmartPointer<vtkStructuredGrid> PolarContour2dFilter::getStructuredGrid()
{
	return grid;
}

PolarContour2dFilter::PolarContour2dFilter()
{
	this->SetNumberOfInputPorts(1);
	this->SetNumberOfOutputPorts(1);
}
int PolarContour2dFilter::RequestData(
	vtkInformation* vtkNotUsed(request),
	vtkInformationVector** inputVector,
	vtkInformationVector* outputVector)
{
	polarPoints.clear();
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
				double s1 = scalars->GetTuple1(id1);
				double s2 = scalars->GetTuple1(id2);
				auto temp = getArcTextinfo(p1.data(), p2.data(), s1, s2);
				polarPoints[z][r].insert(polarPoints[z][r].end(), temp.begin(), temp.end());
			}
		}
	}
	//数据处理，添加起点，删除重复点
	cleanRedundantPoint();
	createGrid();
	//auto structGriddata = createGrid();
	//output->DeepCopy(structGriddata);
	return 1;
}
int PolarContour2dFilter::getPointId(vtkIdType ri, vtkIdType thetai, vtkIdType zi)
{
	return (ri + thetai * rGridSize + zi * rGridSize * thetaGridSize);
}


/**
* @time	2021/12/23
* @brief PolarContour2dFilter::getArcTextinfo 获取弧度纹理信息
* @param double * p1 端点1
* @param double * p2 端点2
* @param double s1 标量1
* @param double s2 标量2
* @return std::vector<DV3D::ArcCalc::ArcTextInfo>
*/
std::vector<DV3D::ArcCalc::ArcTextInfo> PolarContour2dFilter::getArcTextinfo(double* p1, double* p2, double s1, double s2)
{
	DV3D::ArcCalc arcCalc;
	arcCalc.setResolution(Rotation);
	arcCalc.setPoint1(p1);
	arcCalc.setPoint2(p2);
	arcCalc.setScalar1(s1);
	arcCalc.setScalar2(s2);
	arcCalc.setCenter(mCenter);
	arcCalc.Update();
	return arcCalc.getOutputArc();
}

/**
* @time	2021/12/22
* @brief PolarContour2dFilter::getPoint 获取点
* @param vtkSmartPointer<vtkPoints>
* @param vtkIdType id
* @return std::vector<double>
*/
std::vector<double> PolarContour2dFilter::getPoint(vtkSmartPointer<vtkPoints> points, vtkIdType id)
{
	std::vector<double> point;
	point.reserve(3);
	auto ptr = points->GetPoint(id);
	point.push_back(ptr[0]);
	point.push_back(ptr[1]);
	point.push_back(ptr[2]);
	return point;
}

vtkSmartPointer<vtkStructuredGrid> PolarContour2dFilter::createGrid()
{
	grid = vtkSmartPointer<vtkStructuredGrid>::New();
	//添加点
	vtkSmartPointer<vtkPoints> points = vtkSmartPointer<vtkPoints>::New();
	vtkSmartPointer<vtkFloatArray> scalars = vtkSmartPointer<vtkFloatArray>::New();
	points->Allocate(zGridSize * thetaGridSize * rGridSize);
	for (auto zi = 0; zi < zGridSize; ++zi)
	{
		for (auto thetai = 0; thetai < thetaGridSize; ++thetai)
		{
			for (auto ri = 0; ri < rGridSize; ++ri)
			{
				points->InsertNextPoint(polarPoints[zi][ri][thetai].point.x(),
					polarPoints[zi][ri][thetai].point.y(), 
					polarPoints[zi][ri][thetai].point.z());
				scalars->InsertNextTuple1(polarPoints[zi][ri][thetai].scalar);
			}
		}
	}
	grid->SetPoints(points);
	grid->GetPointData()->SetScalars(scalars);
	grid->SetDimensions(rGridSize,thetaGridSize,zGridSize);
	return grid;
}


/**
* @time	2021/12/23
* @brief PolarContour2dFilter::cleanRedundantPoint 去除多余点
* @return void
*/
void PolarContour2dFilter::cleanRedundantPoint()
{
	//当极坐标下有r==0的情况，会需要添加点，其余不用
	int maxThetaCount = 0;
	{
		auto iterz = polarPoints.begin();
		auto iterr = iterz->second.begin();
		while (iterr != iterz->second.end())
		{
			auto itertheta = iterr->second.begin();
			double p[3] = { itertheta->point.x(),itertheta->point.y(),itertheta->point.z() };
			double distance = vtkMath::Distance2BetweenPoints(p, mCenter);
			if (abs(distance) > 0.00001f)
			{
				maxThetaCount = iterr->second.size();
				break;
			}
			iterr++;
		}
	}
	//为了网格化，需要添加点
	for (auto iterz = polarPoints.begin(); iterz != polarPoints.end(); iterz++)
	{
		for (auto iterr = iterz->second.begin(); iterr != iterz->second.end(); iterr++)
		{
			if (iterr->second.size() == maxThetaCount)
				continue;
			
			DV3D::ArcCalc::ArcTextInfo newArcText= *(iterr->second.begin());
			auto curCount = iterr->second.size();
			for (auto i = 0; i < maxThetaCount - curCount; ++i)
				iterr->second.push_back(newArcText);
		}
	}
	thetaGridSize = maxThetaCount;
}
