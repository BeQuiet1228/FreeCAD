#include "Hdf5DataItem.h"
#include <QIcon>
#include <transition/transition.h>
#include <cassert>
#include "Hdf5DataItemEventHandler.h"
#include <QList>
#include <iostream>

const QString Gui::HDF5DataItem::IconPath[2] = {":/Tree/TreeFile2.png" , ":/Tree/TreeFile1.png"};

Gui::HDF5DataItem::HDF5DataItem(const Hdf5Data& h5data, const QString& name, const ItemType& type /*= FILE*/)
	:QStandardItem(QIcon(IconPath[type]),name)
{
	this->hdf5data = h5data;
	this->name = name;
	this->itemType = type;
	setEditable(false);
}

Gui::HDF5DataItem::HDF5DataItem(const HDF5DataItem& item)
	:QStandardItem(item)
{
	this->name = item.name;
	this->itemType = item.itemType;
	this->hdf5data = item.hdf5data;
	this->doubleClickEventHander = item.doubleClickEventHander;
	
	auto subItems = getSubItems();
	for (auto iter = subItems.begin(); iter != subItems.end(); iter++)
	{
		  HDF5DataItem* newItem = new HDF5DataItem(**iter);
		  addSubItem(newItem);
	}
}

Gui::HDF5DataItem::HDF5DataItem(const QString& name, const ItemType& type /*= FOLDER*/)
	:QStandardItem(QIcon(IconPath[type]), name)
{
	this->name = name;
	this->itemType = type;
	setEditable(false);
}

Gui::HDF5DataItem::~HDF5DataItem()
{

}

int Gui::HDF5DataItem::type() const
{
	return itemType;
}

void Gui::HDF5DataItem::setDoubleClickEventHander(std::shared_ptr<HDF5DataItemEventHander> hander)
{
	doubleClickEventHander = hander;
}

std::shared_ptr<Gui::HDF5DataItemEventHander> Gui::HDF5DataItem::getDoubleClickEventHander()
{
	assert(doubleClickEventHander && "doubleClickEventHander is null");
	return doubleClickEventHander;
}

void Gui::HDF5DataItem::setHdf5Data(const Hdf5Data& data)
{
	this->hdf5data = data;
}

Hdf5Data Gui::HDF5DataItem::getHdf5Data()
{
	return hdf5data;
}

void Gui::HDF5DataItem::setName(const QString& name)
{
	this->name = name;
	setText(name);
}

QString Gui::HDF5DataItem::getNmae()
{
	return this->name;
}

void Gui::HDF5DataItem::triggerDoubleClickEvent()
{
	if (doubleClickEventHander)
		doubleClickEventHander->trigger(this);
}

/**
* @brief Gui::HDF5DataItem::addSubItem 添加一个子节点，并使用name为节点排序
* @param HDF5DataItem * subItem
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem*  Gui::HDF5DataItem::addSubItem(HDF5DataItem* subItem)
{
	int subItemCount = this->rowCount();
	//尝试合并item
	for (int row = 0; row < subItemCount; row++)
	{
		auto item = this->child(row);
		if (mergeItem(item, subItem))
			return dynamic_cast<HDF5DataItem*>(item);
	}

	/*
		未合并成功则需要将subitem插入，插入顺序按照name排序。
		默认顺序为name最小，排在最前。
	*/
	int row = 0;
	for (; row < subItemCount; row++)
	{
		auto item = subItem->child(row);
		auto h5Item = dynamic_cast<HDF5DataItem*>(item);
		if(!h5Item)
			continue;
		if(subItem->name < h5Item->name)
			break;
	}
	this->insertRow(row, subItem);

	return subItem;
}


/**
* @brief Gui::HDF5DataItem::getSubItem 获取所有子节点的指针
* @return std::vector<Gui::HDF5DataItem*>
*/
std::vector<Gui::HDF5DataItem*> Gui::HDF5DataItem::getSubItems()
{
	std::vector<HDF5DataItem*> items;
	int rowCount = this->rowCount();
	for (int i = 0; i < rowCount; i++)
	{
		QStandardItem* stItem = child(i);
		auto item = dynamic_cast<HDF5DataItem*>(stItem);
		if (!item)
			continue;
		items.push_back(item);
	}

	return items;
}

/**
* @brief Gui::HDF5DataItem::mergeItem 合并两个相同的item，并释放掉item的内存
* @param HDF5DataItem * itemsub
* @return bool 不相同则返回false
*/
bool Gui::HDF5DataItem::mergeItem(HDF5DataItem* item)
{
	if ((*this) != (*item))
		return false;
	//将所有的子节点添加到当前节点下
	while (item->rowCount())
	{
		QList<QStandardItem*> listItem = item->takeRow(0);
		auto item = getHDF5DataItemFromQListItem(listItem);
		addSubItem(item);
	}

	delete item;
	return true;
}



/**
* @brief Gui::HDF5DataItem::mergeItem 如果item 与h5item相等，那么将h5item合并入item中
* @param QStandardItem * item
* @param HDF5DataItem * h5item
* @return bool 是否合并成功
*/
bool Gui::HDF5DataItem::mergeItem(QStandardItem* item, HDF5DataItem* h5item)
{
	auto temp = dynamic_cast<HDF5DataItem*>(item);
	if (!temp)
		return false;

	return temp->mergeItem(h5item);
}

/**
* @brief Gui::HDF5DataItem::deleteQlistQStandardItem 释放掉所有item的内存
* @param QList<QStandardItem * > listItem
* @return void
*/
void Gui::HDF5DataItem::deleteQlistQStandardItem(QList<QStandardItem*> listItem)
{
	for (auto iter = listItem.begin(); iter != listItem.end();)
	{
		auto item = *iter;
		iter = listItem.erase(iter);
		delete item;
	}
}


/**
* @brief Gui::HDF5DataItem::getHDF5DataItemFromQListItem 这个函数用于从row 中获取第一列并做类型转换，在拿走的同时会释放掉其他的item
* @param QList<QStandardItem * > listItem
* @return Gui::HDF5DataItem*
*/
Gui::HDF5DataItem* Gui::HDF5DataItem::getHDF5DataItemFromQListItem(QList<QStandardItem*> listItem)
{
	//这里因为应用场景的原因，一般只会构造一列，多余的暂时不处理。
	assert(listItem.size() && "list item size is 0!");

	auto iter = listItem.begin();
	auto h5Item = dynamic_cast<HDF5DataItem*>(*iter);

	assert(h5Item && "item class type is not HDF5DataItem!");
	if (h5Item)
	{
		listItem.erase(iter);
	}
	//释放掉多余的item
	deleteQlistQStandardItem(listItem);

	return h5Item;
}

/**
* @brief Gui::HDF5DataItem::operator== 如果类型跟名称都相等，那么判定两个item相等
* @param const HDF5DataItem & item
* @return bool
*/
bool Gui::HDF5DataItem::operator==(const HDF5DataItem& item)
{
	return (name == item.name) && (itemType == item.itemType);
}

bool Gui::HDF5DataItem::operator!=(const HDF5DataItem& item)
{
	return !((*this) == item);
}