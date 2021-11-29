#include"CylinderStructDataSetConstructor.h"
#include"cassert"
DV3D::CylinderStructDataSetConstructor::CylinderStructDataSetConstructor():PolarStructDaraSetConstruct()
	{

	}
DV3D::CylinderStructDataSetConstructor::~CylinderStructDataSetConstructor()
	{

	}
DV3D::PolarDatas DV3D::CylinderStructDataSetConstructor::getPolarDatas()
	{
		auto h5d = getHdf5Data();
		assert((h5d.listDataSet.size() == 4) && "list DataSet size is not 4!");
		PolarDatas grid;
		grid.reserve(3);
		//r-theta-z
		for (int i = 0; i < 3; i++)
		{
			std::vector<float>  d;
			Hdf5IO::getValue(h5d.listDataSet.at(i), d);
			grid.push_back(d);
		}
		return grid;
	}
DV3D::PolarIndes DV3D::CylinderStructDataSetConstructor::getPolarIndex()
	{
		auto h5d = getHdf5Data();
		std::vector<float> value;
		Hdf5IO::getValue(h5d.listDataSet.at(3), value);
		PolarIndes valueIndex;
		valueIndex.reserve(value.size() / 4);
		const int itemSize = 4;
		for (auto iter = value.begin(); iter != value.end();)
		{
			std::vector<long long> properDatas;
			for (auto i = 0; i < itemSize; i++, iter++)
				properDatas.push_back(*iter);
			std::vector<long long> valueItem;
			valueItem.reserve(4);
			//r-theta-z
			valueIndex.push_back(properDatas);
		}
		return valueIndex;
	}