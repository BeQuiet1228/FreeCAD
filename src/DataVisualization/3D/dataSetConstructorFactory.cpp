#include "dataSetConstructorFactory.h"
#include "CartesianStructDataSetConstructor.h"
#include "PolarStructDataSetConstructor.h"
#include "PolarPlanConstruct.h"
#include "CylinderStructDataSetConstructor.h"
#include "CylinderPlanConstruct.h"
#include <cassert>

std::shared_ptr<DV3D::DataSetConstructor> DV3D::DataSetConstructorFactory::CreatConstructor(Hdf5Data& h5data)
{
	std::shared_ptr<DataSetConstructor> constructor;

	creatStrucConstructor(&constructor, h5data);


	assert(constructor && "constructor is nullptr!");
	return constructor;
}

bool DV3D::DataSetConstructorFactory::creatStrucConstructor(std::shared_ptr<DataSetConstructor>* constructor, Hdf5Data& h5data)
{
	if (h5data.name != "struct")
		return false;
	DataSetConstructorH5* ctr = nullptr;
	if (Hdf5Data::CoordinateSystem::CARTESIAN == h5data.coordinateSystem)
	{
		ctr = new CartesianStructDataSetConstructor();
		
	}else if (Hdf5Data::CoordinateSystem::POLAR == h5data.coordinateSystem)
	{
		if (findStringAttribute(h5data.headList.at(1)) > 20)
			ctr = new PolarStructDaraSetConstruct();
		else
			ctr = new PolarPlanConstruct();
	}else if (Hdf5Data::CoordinateSystem::CYLINDER == h5data.coordinateSystem)
	{
		if (findStringAttribute(h5data.headList.at(2)) > 20)
			ctr = new CylinderStructDataSetConstructor();
		else
			ctr = new CylinderPlanConstruct();
	}

	ctr->setHdf5Data(h5data);
	constructor->reset(ctr);
}

/**
* @brief DV3D::DataSetConstructorFactory::findStringAttribute 寻找结构图头属性中的长度信息
* @param const std::string & str
* @return int
*/
int DV3D::DataSetConstructorFactory::findStringAttribute(const std::string& str)
{
	bool ok = false;
	std::string temp;
	for (auto iter = str.begin(); iter != str.end(); iter++)
	{
		if (*iter == '=')
		{
			ok = true;
			continue;
		}
		if (ok)
			temp+= *iter;
	}

	return std::stoi(temp);
}


