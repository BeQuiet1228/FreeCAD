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
#include "particle3dActorPipeline.h"
#include "particle3dDataSetConstructor.h"
#include "ContourDataSetConstructor.h"
#include "PolarContourDataSetConstructor.h"
#include "ContourActorPipeline.h"
#include "DataVisualization/ContourData.h"
#include "Contour3dataSetConstructor.h"
#include "PolarContour3dDataSetConstructor.h"
#include "Contour3dActorPipeline.h"
#include "CartesianVector3dDatasetConstructor.h"
#include "CylinderVector3dDatasetConstructor.h"
#include "Vector3dActorPipeline.h"
#include"Contour3dControler.h"
#include <cassert>
/*
	配置窗口
*/
#include "Struct3dConfigWidget.h"
#include "Contour3dConfigWidget.h"
#include "Particle3dConfigWidget.h"
#include "Vector3dConfigWidget.h"
std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatControler(Hdf5Data& h5data)
{
	std::shared_ptr<Controler> controler;
	if (h5data.name == "struct")
		controler = CreatStrucControler(h5data);
	if (h5data.name == "CONTOUR")
		controler = CreatContourControler(h5data);
	if (h5data.name == "PARTICLE3D")
		controler = CreatParticle3dControler(h5data);
	if (h5data.name == "CONTOUR3D")
		controler = CreatContour3dControler(h5data);
	assert(controler && "controler is nullptr!");
	return controler;
}
std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatContourControler(Hdf5Data& h5data)
{
	std::shared_ptr<Controler> controler;
	std::shared_ptr<DataSetConstructorH5> constructor;
	std::shared_ptr<ActorPipemline> pipeline;
	DV::ContourData data(h5data);
	if (data.getDirectionType() != DV::R_THETA)
		constructor.reset(new ContourDatasetConstructor);
	else
		constructor.reset(new PolarContourDatasetConstructor);
	constructor->setHdf5Data(h5data);
	pipeline.reset(new  ContourActorPipeline);
	pipeline->setDataSet(constructor->creatDataset());
	pipeline->connect();
	controler.reset(new Controler());
	controler->setActorPipeline(pipeline);
	return controler;
}

std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatContour3dControler(Hdf5Data& h5data)
{
	std::shared_ptr<Controler> controler;
	std::shared_ptr<DataSetConstructorH5> constructor;
	std::shared_ptr<ActorPipemline> pipeline;
	if (Hdf5Data::CoordinateSystem::CARTESIAN == h5data.coordinateSystem)
		constructor.reset(new Contour3dDatasetConstructor());
	else
		constructor.reset(new PolarContour3dDatasetConstructor());
	constructor->setHdf5Data(h5data);
	pipeline.reset(new  Contour3dActorPipline());
	pipeline->setDataSet(constructor->creatDataset());
	pipeline->connect();
	controler.reset(new Contour3dControler());
	controler->setActorPipeline(pipeline);
	return controler;
}


/**
* @time	2021/12/29
* @brief DV3D::ControlerFactory::CreatVector3dControler
* @param std::vector<Hdf5Data> & h5datas
* @return std::shared_ptr<DV3D::Controler>
*/
std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatVector3dControler(Hdf5Data& h5data)
{
	std::shared_ptr<Controler> controler;
	std::shared_ptr<DataSetConstructorH5> constructor;
	std::shared_ptr<ActorPipemline> pipeline;
	if (Hdf5Data::CoordinateSystem::CARTESIAN == h5data.coordinateSystem)
		constructor.reset(new CartesianVector3dDatasetConstructor());
	else
		constructor.reset(new CylinderVector3dDatasetContructor());
	constructor->setHdf5Data(h5data);
	pipeline.reset(new Vector3dActorPipeline());
	pipeline->setDataSet(constructor->creatDataset());
	pipeline->connect();
	controler.reset(new Controler());
	controler->setActorPipeline(pipeline);
	return controler;
}

std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatStrucControler(Hdf5Data& h5data)
{

	std::shared_ptr<Controler> controler;
	std::shared_ptr<DataSetConstructorH5> constructor;
	std::shared_ptr<ActorPipemline> pipeline;

	if (Hdf5Data::CoordinateSystem::CARTESIAN == h5data.coordinateSystem)
	{
		constructor.reset(new CartesianStructDataSetConstructor());
		pipeline.reset(new CartesianStructActorPipeline);
	}
	else if (Hdf5Data::CoordinateSystem::POLAR == h5data.coordinateSystem)
	{

		if (findStringAttribute(h5data.headList.at(1)) > 20)
		{
			constructor.reset(new PolarStructDaraSetConstruct());
			pipeline.reset(new CartesianStructActorPipeline());
		}
		else {
			constructor.reset(new PolarPlanConstruct());
			pipeline.reset(new PolarStructActorPipeline);
		}
	}
	else if (Hdf5Data::CoordinateSystem::CYLINDER == h5data.coordinateSystem)
	{
		if (findStringAttribute(h5data.headList.at(2)) > 20)
		{
			constructor.reset(new CylinderStructDataSetConstructor());
			pipeline.reset(new CartesianStructActorPipeline());
		}
		else {
			constructor.reset(new CylinderPlanConstruct());
			pipeline.reset(new PolarStructActorPipeline());
		}
	}
	else {
		assert(true && "unknown coordinate system!");
	}
	constructor->setHdf5Data(h5data);
	pipeline->setDataSet(constructor->creatDataset());
	pipeline->connect();
	controler.reset(new Controler());
	controler->setActorPipeline(pipeline);

	return controler;
}

std::shared_ptr<DV3D::Controler> DV3D::ControlerFactory::CreatParticle3dControler(Hdf5Data& h5data)
{
	std::shared_ptr<Controler> controler;

	//测试3d粒子图
	std::shared_ptr<DataSetConstructorH5> constructor(new Particle3dDataSetConstructor);
	std::shared_ptr<ActorPipemline> pipeline(new Particle3dActorPipeline);

	constructor->setHdf5Data(h5data);
	pipeline->setDataSet(constructor->creatDataset());
	pipeline->connect();
	controler.reset(new Controler());
	controler->setActorPipeline(pipeline);


	assert(controler && "controler is nullptr!");
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

/**
* @brief DV3D::ControlerFactory::CreateConfigWidget 创建配置窗口
* @return std::vector<QWidget*>
* @time	2022/01/10
*/
std::vector<QWidget*> DV3D::ControlerFactory::CreateConfigWidget()
{
	std::vector<QWidget*> widgets;
	//Struct3dConfigWidget* struct3dConfigWidget = new Struct3dConfigWidget(); 
	//Contour3dConfigWidget* contour3dConfigWidget = new Contour3dConfigWidget();
	//Particle3dConfigWidget* particle3dConfigWidget = new Particle3dConfigWidget();
	//Vector3dConfigWidget* vector3dConfigWidget = new Vector3dConfigWidget();
	widgets.push_back(new Struct3dConfigWidget());
	widgets.push_back(new Contour3dConfigWidget());
	widgets.push_back(new Particle3dConfigWidget());
	widgets.push_back(new Vector3dConfigWidget());
	return widgets;
}

