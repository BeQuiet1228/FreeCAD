#include "PolarContourDataSetConstructor.h"
#include "DataVisualization/ContourDataPolar.h"
#include "vtkStructuredGrid.h"
#include "vtkPointData.h"
#include "vtkPolyData.h"
#include "PolarContourFliter.h"
namespace DV3D
{
	PolarContourDatasetConstructor::PolarContourDatasetConstructor():rGridSize(1),thetaGridSize(1),zGridSize(1)
	{

	}
	PolarContourDatasetConstructor::~PolarContourDatasetConstructor()
	{

	}
	vtkSmartPointer<vtkDataSet> PolarContourDatasetConstructor::creatDataset()
	{
		initData();
		vtkSmartPointer<vtkPolyData> polyData = vtkSmartPointer<vtkPolyData>::New();
		polyData->SetPoints(points);
		polyData->GetPointData()->SetScalars(scalar);
		vtkSmartPointer<vtkStructuredGrid> structuredGrid = vtkSmartPointer<vtkStructuredGrid>::New();
		structuredGrid->SetDimensions(rGridSize, thetaGridSize, zGridSize);
		structuredGrid->SetPoints(points);
		structuredGrid->GetPointData()->SetScalars(scalar);
		return structuredGrid;
	}
	void PolarContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();
		//对数据进行插值
		PolarContourFilter polarContourFilter;
		polarContourFilter.loadPoint(h5d,40);
		points = vtkSmartPointer<vtkPoints>::New();
		scalar = vtkSmartPointer<vtkFloatArray>::New();
		auto rDatas = polarContourFilter.getRGridData();
		auto thetaDatas = polarContourFilter.getThetaGridData();
		auto zDatas = polarContourFilter.getZGridData();
		auto valDatas = polarContourFilter.getVallist();
		rGridSize = rDatas.size();
		thetaGridSize = thetaDatas.size();
		zGridSize = zDatas.size();
		for(int zi=0;zi<zGridSize;++zi)
			for (int thetai=0;thetai<thetaGridSize;++thetai)
				for (int ri=0;ri<rGridSize;++ri)
				{
					float x = rDatas[ri] * cos(thetaDatas[thetai]);
					float y= rDatas[ri] * sin(thetaDatas[thetai]);
					float z = zDatas[zi];
					points->InsertNextPoint(x, y, z);
					scalar->InsertNextTuple1(
						valDatas[ri+thetai*rGridSize+zi*rGridSize*thetaGridSize]);
				}
		return;
	}
}