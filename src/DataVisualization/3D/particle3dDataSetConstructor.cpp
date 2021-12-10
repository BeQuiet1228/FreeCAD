#include "particle3dDataSetConstructor.h"
#include <HDF5Reader/hdf5io.h>
#include <math.h>
#include <vtkCellArray.h>
#include <vtkPolyData.h>
#include <vtkPoints.h>
#include <vtkCellType.h>
vtkSmartPointer<vtkDataSet> DV3D::Particle3dDataSetConstructor::creatDataset()
{
	auto h5d = getHdf5Data();
	VectorF value;
	Hdf5IO::getValue(h5d.listDataSet.at(0), value);
	

	auto  cellArray = vtkSmartPointer<vtkCellArray>::New();
	auto polydata = vtkSmartPointer<vtkPolyData>::New();
	auto  points = vtkSmartPointer<vtkPoints>::New();
	float x = 0, y = 0, z= 0;
	float point[3];
	vtkIdType num;
	for (int i = 0; i < value.size(); i += 3)
	{
		z = value.at(i + 2);
		x = value.at(i) * cos(value.at(i + 1));
		y = value.at(i) * sin(value.at(i + 1));

		point[0] = x;
		point[1] = y;
		point[2] = z;

		num = points->InsertNextPoint(point);
		cellArray->InsertNextCell(VTK_VERTEX, &num);

	}

	polydata->SetPoints(points);
	polydata->SetVerts(cellArray);
	
	return polydata;
}

