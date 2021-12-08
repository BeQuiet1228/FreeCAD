#include "ContourDataSetConstructor.h"
namespace DV3D
{
	ContourDatasetConstructor::ContourDatasetConstructor()
	{

	}
	ContourDatasetConstructor::~ContourDatasetConstructor()
	{

	}
	vtkSmartPointer<vtkDataSet> ContourDatasetConstructor::creatDataset()
	{
		initData();
	}
	void ContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();

	}
};