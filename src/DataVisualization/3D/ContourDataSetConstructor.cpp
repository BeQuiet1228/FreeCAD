#include "ContourDataSetConstructor.h"
#include "DataVisualization/ContourData.h"
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
		vtkSmartPointer<vtkDataSet> dataset = nullptr;
		return dataset;
	}
	void ContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		//Ìí¼Ó×ø±êµã

	}
};