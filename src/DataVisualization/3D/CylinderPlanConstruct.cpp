#include"CylinderPlanConstruct.h"
#include"vtkPolyData.h"
#include"vtkTriangleFilter.h"
#include"vtkRotationalExtrusionFilter.h"
#include"vtkUnstructuredGrid.h"
#include"array"
#include"vtkPolyDataNormals.h"
DV3D::CylinderPlanConstruct::CylinderPlanConstruct() :CylinderStructDataSetConstructor() {

}
DV3D::CylinderPlanConstruct::~CylinderPlanConstruct()
{

}
vtkSmartPointer<vtkDataSet> DV3D::CylinderPlanConstruct::creatDataset()
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
		std::array<__int64, 4> cell = {
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

	vtkSmartPointer<vtkPolyDataNormals> normalfile = vtkSmartPointer<vtkPolyDataNormals>::New();
	normalfile->SetInputConnection(filter->GetOutputPort());
	normalfile->SetComputePointNormals(1);
	normalfile->SetComputeCellNormals(0);
	normalfile->SetAutoOrientNormals(1);
	normalfile->SetSplitting(0);
	normalfile->Update();
	auto ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
	ugrid->DeepCopy(normalfile->GetOutput());
	return ugrid;
}