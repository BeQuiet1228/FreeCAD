#include "hdf5DataItemFactory.h"
#include <transition/transition.h>
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
	//创建两个结构图对象
	auto gridItem = new HDF5DataItem(data, "Grid");
	itemSetHander(gridItem);
	auto structItem = new HDF5DataItem(data, "Struct");
	itemSetHander(structItem);

	parentItem->addSubItem(gridItem);
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
	HDF5DataItem* item = new HDF5DataItem(gbkStdstringToQstring("3D粒子图"));;

	for (auto iter = datas.begin(); iter != datas.end();)
	{
		if (iter->name != "PARTICLE3D")
		{
			iter++;
			continue;
		}
		auto h5data = *iter;
		iter = datas.erase(iter);

		CreatParticle3DItem(h5data,item);
	}

	if (item->rowCount() != 0)
		return item;

	delete item;
	return nullptr;
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
		item = CreatStructDataItem(h5data);
		break;
	}
	
	return item;
}

HDF5DataItemFactory::HDF5DataItems HDF5DataItem3DFactory::CreatHDF5Items(std::vector<Hdf5Data>& datas)
{
	HDF5DataItemFactory::HDF5DataItems items;

	auto item = CreatParticle3DItem(datas);
	if (item)
		items.push_back(item);
	item = CreatStructDataItem(datas);
	if (item)
		items.push_back(item);

	return items;
}

