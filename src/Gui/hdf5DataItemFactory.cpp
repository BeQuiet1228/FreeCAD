#include "hdf5DataItemFactory.h"
#include <transition/transition.h>
#include "HDF5DataItem2DFactory.h"
using namespace Gui;


void HDF5DataItemFactory::setEventHander(std::shared_ptr<HDF5DataItemEventHander> hander)
{
	this->eventHader = hander;
}

std::shared_ptr<Gui::HDF5DataItemEventHander> HDF5DataItemFactory::getEventHander()
{
	return eventHader;
}

void HDF5DataItemFactory::itemSetHander(HDF5DataItem* item)
{
	if (!eventHader)
		return;
	item->setDoubleClickEventHander(eventHader);
}

HDF5DataItem* HDF5DataItem3DFactory::CreatStructDataItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	if (parentItem == nullptr)
	{
		parentItem = new HDF5DataItem(gbkStdstringToQstring("3D结构图"));
	}
	//如果不是直角坐标系则创建两个项
	if (Hdf5Data::CoordinateSystem::CARTESIAN != data.coordinateSystem)
	{
		auto gridItem = new HDF5DataItem(data, "Struct");
		itemSetHander(gridItem);
		parentItem->addSubItem(gridItem);
	}
	auto structItem = new HDF5DataItem(data, "Grid");
	itemSetHander(structItem);

	parentItem->addSubItem(structItem);
	
	return parentItem;
}

Gui::HDF5DataItem* HDF5DataItem3DFactory::CreatParticle3DItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	if (parentItem == nullptr)
	{
		parentItem = new HDF5DataItem(gbkStdstringToQstring("3D粒子图"));
	}
	//获取迭代时间作为数据名称
	std::string  iterCount = H5DataHead::getAttributeForIndex(*data.headList.begin(), 3);

	auto particleItem = new HDF5DataItem(data, gbkStdstringToQstring(iterCount));
	itemSetHander(particleItem);
	parentItem->addSubItem(particleItem);

	return parentItem;
}

/**
* @brief Gui::HDFDataItem3DFactory::CreatParticle3DItem 创建3d粒子图item，如果传入的数据中没有粒子图数据，那么返回一个nullptr，被用于生成item的数据将会从datas中移除
* @param std::vector<Hdf5Data> & datas
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* HDF5DataItem3DFactory::CreatParticle3DItem(std::vector<Hdf5Data>& datas)
{
	HDF5DataItem* item = nullptr;

	for (auto iter = datas.begin(); iter != datas.end();)
	{
		if (iter->name != "PARTICLE3D")
		{
			iter++;
			continue;
		}
		auto h5data = *iter;
		iter = datas.erase(iter);

		item = CreatParticle3DItem(h5data,item);
	}

	return item;
}

/**
* @brief Gui::HDFDataItem3DFactory::CreatStructDataItem  同CreatParticle3DItem
* @param std::vector<Hdf5Data> & datas
* @return Gui::HDF5DataItem*
*/
HDF5DataItem* HDF5DataItem3DFactory::CreatStructDataItem(std::vector<Hdf5Data>& datas)
{
	HDF5DataItem* item = nullptr;

	for (auto iter = datas.begin(); iter != datas.end();)
	{
		if (iter->name != "struct")
		{
			iter++;
			continue;
		}
			
		auto h5data = *iter;
		iter = datas.erase(iter);
		item = CreatStructDataItem(h5data,item);
	}
	
	return item;
}

HDF5DataItemFactory::HDF5DataItems HDF5DataItem3DFactory::CreatHDF5Items(std::vector<Hdf5Data> datas)
{
	HDF5DataItemFactory::HDF5DataItems items;

	auto item = CreatParticle3DItem(datas);
	if (item)
		items.push_back(item);
	item = CreatStructDataItem(datas);
	if (item)
		items.push_back(item);
	item = CreatContour3DItem(datas);
	if (item)
		items.push_back(item);
	item = CreatContour2DItem(datas);
	if (item)
		items.push_back(item);

	return items;
}

Gui::HDF5DataItem* HDF5DataItem3DFactory::CreatHDF5Item(Hdf5Data& data)
{
	std::vector<Hdf5Data> datas;
	datas.push_back(data);
	auto its = CreatHDF5Items(datas);
	if (its.size() <= 0)
		return nullptr;
	return *its.begin();
}

Gui::HDF5DataItem* HDF5DataItem3DFactory::CreatContour3DItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	if (parentItem == nullptr)
	{
		parentItem = new HDF5DataItem(gbkStdstringToQstring("3D等位图"));
	}
	//获场值+迭代步数为名称
	std::string  name = H5DataHead::getAttributeForIndex(*data.headList.begin(), 3);
	name += H5DataHead::getAttributeForIndex(*data.headList.begin(), 4);

	auto contourItem = new HDF5DataItem(data, gbkStdstringToQstring(name));
	itemSetHander(contourItem);
	parentItem->addSubItem(contourItem);

	return parentItem;
}

Gui::HDF5DataItem* HDF5DataItem3DFactory::CreatContour3DItem(std::vector<Hdf5Data>& datas)
{
	HDF5DataItem* item = nullptr;

	for (auto iter = datas.begin(); iter != datas.end();)
	{
		if (iter->name != "CONTOUR3D")
		{
			iter++;
			continue;
		}

		auto h5data = *iter;
		iter = datas.erase(iter);
		item = CreatContour3DItem(h5data,item);
	}

	return item;
}

Gui::HDF5DataItem* HDF5DataItem3DFactory::CreatContour2DItem(std::vector<Hdf5Data>& datas)
{
	/*
	2022-1-4
	暂时不适用2d结构图的三维显示
	*/
	return nullptr;

	HDF5DataItem2DFactory factory2d;
	factory2d.setEventHander(getEventHander());
	auto item = factory2d.CreatContourDataItem(datas);
	if (!item)
		return item;
	item->setName(gbkStdstringToQstring("2D等位图3D显示"));
	return item;
}

Gui::HDF5DataItem* HDF5DataItem3DFactory::CreatContour2DItem(Hdf5Data& data, HDF5DataItem* parentItem /*= nullptr*/)
{
	/*
	2022-1-4
	暂时不适用2d结构图的三维显示
	*/
	return nullptr;

	HDF5DataItem2DFactory factory2d;
	factory2d.setEventHander(getEventHander());
	auto item = factory2d.CreatContourDataItem(data,parentItem);
	if (!item)
		return item;
	item->setName(gbkStdstringToQstring("2D等位图3D显示"));
	return item;
}

