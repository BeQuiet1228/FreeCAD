#include "PolarContourDataSetConstructor.h"
#include "DataVisualization/ContourDataPolar.h"

namespace DV3D
{
	PolarContourDatasetConstructor::PolarContourDatasetConstructor()
	{

	}
	PolarContourDatasetConstructor::~PolarContourDatasetConstructor()
	{

	}
	vtkSmartPointer<vtkDataSet> PolarContourDatasetConstructor::creatDataset()
	{
		initData();
		vtkSmartPointer<vtkDataSet> dataset;
		return dataset;
	}
	void PolarContourDatasetConstructor::createPointsRtheta()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		return;
	}
	void PolarContourDatasetConstructor::createPointsRz()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		data->loadPoint();
		auto datas = data->getGrids();
		auto face = data->getStructFace();
		
		return;
	}
	void PolarContourDatasetConstructor::initData()
	{
		auto h5d = getHdf5Data();
		std::shared_ptr<DV::ContourData> data = std::shared_ptr<DV::ContourData>(new DV::ContourData(h5d));
		switch (data->getDirectionType())
		{
		case DV::DirectionType::R_THETA:
			createPointsRtheta();
			break;
		case DV::DirectionType::R_Z:
			createPointsRz();
			break;
		}
		return;
		
	}
}