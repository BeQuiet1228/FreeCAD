#include"PolarPlanConstruct.h"
#include"vtkDataSet.h"
#include"vtkSmartPointer.h"
#include"vtkUnstructuredGrid.h"
#include"vtkCellType.h"
#include"vtkPolyData.h"
#include"vtkRotationalExtrusionFilter.h"
#include"array"
#include"vtk-7.0/vtkTriangleFilter.h"
DV3D::PolarPlanConstruct::PolarPlanConstruct() :PolarStructDaraSetConstruct() {}
DV3D::PolarPlanConstruct::~PolarPlanConstruct() {}
vtkSmartPointer<vtkDataSet> DV3D::PolarPlanConstruct::creatDataset()
{
	initPoints();
	auto value = getPolarIndex();
	vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
	vtkSmartPointer<vtkCellArray> cellData = vtkSmartPointer<vtkCellArray>::New();

	//插入面的id
	vtkIdType pointNum = 4;
	for (auto& i : value)
	{
		long long zIndex = i[0];
		long long rIndex = i[1];
		long long thetaIndex = i[2];
		long long type = i[3];
		if ((type & 0x03) != 0x03)
			continue;
		if (zIndex == zSize || rIndex == rSize || thetaIndex == thetaSize)
			continue;
		std::array<long long, 4> cell = {
			getPointId(thetaIndex - 1,	rIndex - 1,		zIndex - 1),
			getPointId(thetaIndex - 1,	rIndex,			zIndex - 1),
			getPointId(thetaIndex - 1,	rIndex,			zIndex),
			getPointId(thetaIndex - 1,	rIndex - 1,		zIndex)
		};
		cellData->InsertNextCell(pointNum, cell.data());
	}
	polyData->SetPoints(points);
	polyData->SetPolys(cellData);
	vtkSmartPointer<vtkTriangleFilter> triangle = vtkSmartPointer<vtkTriangleFilter>::New();
	triangle->SetInputData(polyData);
	triangle->Update();
	////进行旋转
	vtkSmartPointer<vtkRotationalExtrusionFilter> filter = vtkSmartPointer<vtkRotationalExtrusionFilter>::New();
	filter->SetInputData(triangle->GetOutput());
	filter->SetResolution(72);
	filter->SetAngle(360 / (thetaSize - 1));
	filter->Update();
	auto ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	ugrid->DeepCopy(filter->GetOutput());
	return ugrid;
}
