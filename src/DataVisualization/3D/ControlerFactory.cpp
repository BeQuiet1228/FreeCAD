#include "ControlerFactory.h"
#include <HDF5Reader/hdf5io.h>
#include "controler.h"
#include "CartesianStructDataSetConstructor.h"
#include "PolarStructDataSetConstructor.h"
#include "PolarPlanConstruct.h"
#include "CylinderStructDataSetConstructor.h"
#include "CylinderPlanConstruct.h"
#include "CartesianStructActorPipeline.h"
#include "PolarStructActorPipeline.h"
#include "actorPipeline.h"
#include <cassert>

std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatControler(Hdf5Data& h5data)
{
	std::shared_ptr<Controler> controler;
	if (h5data.name == "struct")
		controler = CreatStrucControler(h5data);

	assert(controler && "controler is nullptr!");
	return controler;
}

std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatStrucControler(Hdf5Data& h5data)
{

	std::shared_ptr<Controler> controler;

	if (Hdf5Data::CoordinateSystem::CARTESIAN == h5data.coordinateSystem)
	{
		CartesianStructDataSetConstructor constructor;
		constructor.setHdf5Data(h5data);
		std::shared_ptr<ActorPipemline> pipeline(new CartesianStructActorPipeline);
		pipeline->setDataSet(constructor.creatDataset());
		pipeline->connect();
		controler.reset(new Controler());
		controler->setActorPipeline(pipeline);
	}
	else if (Hdf5Data::CoordinateSystem::POLAR == h5data.coordinateSystem)
	{
		std::shared_ptr<DataSetConstructorH5> constructor;
		if (findStringAttribute(h5data.headList.at(1)) > 20)
			constructor.reset(new PolarStructDaraSetConstruct());
		else
			constructor.reset(new PolarPlanConstruct());
		constructor->setHdf5Data(h5data);
		std::shared_ptr<ActorPipemline> pipeline(new PolarStructActorPipeline());
		pipeline->setDataSet(constructor->creatDataset());
		pipeline->connect();
		controler.reset(new Controler());
		controler->setActorPipeline(pipeline);
	}
	else if (Hdf5Data::CoordinateSystem::CYLINDER == h5data.coordinateSystem)
	{
		std::shared_ptr<DataSetConstructorH5> constructor;
		if (findStringAttribute(h5data.headList.at(2)) > 20)
			constructor.reset(new CylinderStructDataSetConstructor());
		else
			constructor.reset( new CylinderPlanConstruct());
		constructor->setHdf5Data(h5data);
		std::shared_ptr<ActorPipemline> pipeline(new PolarStructActorPipeline());
		pipeline->setDataSet(constructor->creatDataset());
		pipeline->connect();
		controler.reset(new Controler());
		controler->setActorPipeline(pipeline);
	}
	
	
	return controler;
}

/**
* @brief DV3D::ControlerFactory::findStringAttribute 寻找头信息中的长度属性信息
* @param const std::string & str
* @return int
*/
int DV3D::ControlerFactory::findStringAttribute(const std::string& str)
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
			temp += *iter;
	}

	return std::stoi(temp);
}

