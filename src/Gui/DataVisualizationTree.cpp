#include "DataVisualizationTree.h"
#include <cassert>
#include "HDF5DataItem2DFactory.h"
#include "Hdf5DataItemEventHandler.h"
#include "HDF5DataItem2DDoubleClickEventHander.h"
#include "Hdf5DataItem.h"
#include <QStandardItem>
Gui::DataVisualizationTree::DataVisualizationTree(QWidget* parent/*= 0*/)
	:QTreeView(parent),model(new QStandardItemModel)
{
	connect(this, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(itemDoubleClicked(QModelIndex)));
	setModel(model);

	initFactorys();
}

Gui::DataVisualizationTree::~DataVisualizationTree()
{

}

void Gui::DataVisualizationTree::addHDF5DataItem(HDF5DataItem* item)
{
	/*
		首先尝试合并，如果无法合并再添加。
		这样可以去掉一些重复的item。
	*/
	int rowCount = model->rowCount();
	for (int row = 0; row < rowCount; row++)
	{
		HDF5DataItem* hdf5Item = dynamic_cast<HDF5DataItem*>(model->item(row));
		if (hdf5Item->mergeItem(item))
			return;
	}

	model->appendRow(item);
}

void Gui::DataVisualizationTree::addHDF5DataItem(std::vector<HDF5DataItem*> items)
{
	for (auto item = items.begin(); item != items.end(); item++)
	{
		addHDF5DataItem(*item);
	}
}

void Gui::DataVisualizationTree::clear()
{
// 	while (model->columnCount())
// 	{
// 		auto items = model->takeColumn(0);
// 		for each (auto item in items)
// 		{
// 			delete item;
// 		}
// 	}
	model->clear();
	clearFactorys();
	initFactorys();
}

/**
* @brief Gui::DataVisualizationTree::loadHdf5Datas 会覆盖之前所有的数据，然后重新添加新的数据
* @param std::vector<Hdf5Data> datas
* @return void
*/
void Gui::DataVisualizationTree::loadHdf5Datas(std::vector<Hdf5Data> datas)
{
	this->clear();
	for (auto iter = factorys.begin(); iter != factorys.end(); iter++)
	{
		auto items = (*iter)->CreatHDF5Items(datas);
		addHDF5DataItem(items);
	}
}

/**
* @brief Gui::DataVisualizationTree::addHdf5Data 使用数据添加item
* @param Hdf5Data & data
* @return HDF5DataItem* 添加失败返回nullptr
*/
Gui::HDF5DataItem* Gui::DataVisualizationTree::addHdf5Data(Hdf5Data& data)
{
	//临时存储添加成功的item
	HDF5DataItem *temp = nullptr;
	for (auto iter = factorys.begin(); iter != factorys.end(); iter++)
	{
		auto item = (*iter)->CreatHDF5Item(data);
		if (item)
		{
			temp = item;
			addHDF5DataItem(item);
		}
	}
	
	return temp;
}

void Gui::DataVisualizationTree::addHdf5DataToShow(Hdf5Data& data)
{
	auto item = addHdf5Data(data);

	if (!item)
		return;
	/*
		创建item时会返回父节点的item，所以这里要先找到子节点的item才能触发显示。
		不存在一个hdf5会生成多个父节点然后对应多个子节点的item。
	*/
	while (item->type() == HDF5DataItem::FOLDER)
	{
		auto items = item->getSubItems();
		if(items.size() <= 0)
			break;
		item = *items.begin();
	}
	item->triggerDoubleClickEvent();
}

void Gui::DataVisualizationTree::addHdf5Data(std::vector<Hdf5Data> datas)
{
	for (auto iter = factorys.begin(); iter != factorys.end(); iter++)
	{
		auto items = (*iter)->CreatHDF5Items(datas);
		addHDF5DataItem(items);
	}
}

/**
* @brief Gui::DataVisualizationTree::initfactorys 初始化所有的工程对象
* @return void
*/
void Gui::DataVisualizationTree::initFactorys()
{
	std::shared_ptr<HDF5DataItemFactory> factory(new HDF5DataItem3DFactory());
	std::shared_ptr<HDF5DataItemEventHander> hander(new HDF5DataItem3DDoubleClickEventHander());
	factory->setEventHander(hander);
	factorys.push_back(factory);

	factory.reset(new HDF5DataItem2DFactory());
	hander.reset(new HDF5DataItem2DDoubleClickEventHander());
	factory->setEventHander(hander);
	factorys.push_back(factory);
}

/**
* @brief Gui::DataVisualizationTree::clearFactorys 清理工厂类
* @return void
*/
void Gui::DataVisualizationTree::clearFactorys()
{
	factorys.clear();
}


void Gui::DataVisualizationTree::itemDoubleClicked(const QModelIndex& index)
{
	auto item = dynamic_cast<HDF5DataItem*>(model->itemFromIndex(index));
	assert(item);

	item->triggerDoubleClickEvent();
}

