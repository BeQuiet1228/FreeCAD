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
	
	//如果不是直角坐标系数据，那么转换数据
	if (h5d.coordinateSystem != Hdf5Data::CARTESIAN)
		disposThetaData(value);

	auto  cellArray = vtkSmartPointer<vtkCellArray>::New();
	auto polydata = vtkSmartPointer<vtkPolyData>::New();
	auto  points = vtkSmartPointer<vtkPoints>::New();
	float point[3];
	vtkIdType num;
	for (int i = 0; i < value.size(); i += 3)
	{
		point[0] = value.at(i);
		point[1] = value.at(i + 1);
		point[2] = value.at(i + 2);

		num = points->InsertNextPoint(point);
		cellArray->InsertNextCell(VTK_VERTEX, &num);

	}

	polydata->SetPoints(points);
	polydata->SetVerts(cellArray);
	
	return polydata;
}

/**
* @brief DV3D::Particle3dDataSetConstructor::disposThetaData 处理含theta方向的数据，转换为直角坐标系数据
* @param std::vector<float> & data
* @return void
*/
void DV3D::Particle3dDataSetConstructor::disposThetaData(std::vector<float>& data)
{
	float x = 0, y = 0, z = 0;

	for (int i = 0; i < data.size(); i += 3)
	{
		z = data.at(i + 2);
		x = data.at(i) * cos(data.at(i + 1));
		y = data.at(i) * sin(data.at(i + 1));

		data[i] = x;
		data[i + 1] = y;
		data[i + 2] = z;
	}
}

