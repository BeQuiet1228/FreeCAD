#include"CylinderPlanConstruct.h"
#include"vtkPolyData.h"
#include"vtkTriangleFilter.h"
#include"vtkRotationalExtrusionFilter.h"
#include"vtkUnstructuredGrid.h"
#include"array"
namespace DV3D
{
	CylinderPlanConstruct::CylinderPlanConstruct() :CylinderStructDataSetConstructor(){

	}
	CylinderPlanConstruct::~CylinderPlanConstruct()
	{

	}
	vtkSmartPointer<vtkDataSet> CylinderPlanConstruct::creatDataset()
	{
		initPoints();
		auto value = getPolarIndex();
		vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
		vtkSmartPointer<vtkCellArray> cellData = vtkSmartPointer<vtkCellArray>::New();

		//插入面的id
		vtkIdType pointNum = 4;
		for (auto& i : value)
		{
			__int64 zIndex = i[0];
			__int64 rIndex = i[1];
			__int64 thetaIndex = i[2];
			__int64 type = i[3];
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
		filter->SetResolution(32);
		if (2 == thetaSize)
		{
			filter->SetAngle(360);
		}
		else if (3 == thetaSize)
		{
			filter->SetAngle(180);
		}
		filter->Update();
		auto ugrid = vtkSmartPointer<vtkUnstructuredGrid>::New();
		ugrid->DeepCopy(filter->GetOutput());
		return ugrid;
	}
};
