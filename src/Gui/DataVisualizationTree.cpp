#include "DataVisualizationTree.h"
#include <cassert>
#include "HDF5DataItem2DFactory.h"
#include "Hdf5DataItemEventHandler.h"
#include "HDF5DataItem2DDoubleClickEventHander.h"
Gui::DataVisualizationTree::DataVisualizationTree(QWidget* parent/*= 0*/)
	:QTreeView(parent),model(new QStandardItemModel)
{
	connect(this, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(itemDoubleClicked(QModelIndex)));
	setModel(model);

	initfactorys();
}

Gui::DataVisualizationTree::~DataVisualizationTree()
{
	for (auto iter = factorys.begin(); iter != factorys.end(); iter++)
	{
		delete *iter;
		iter = factorys.erase(iter);
	}
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
	model->clear();
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
* @return void
*/
void Gui::DataVisualizationTree::addHdf5Data(Hdf5Data& data)
{
	for (auto iter = factorys.begin(); iter != factorys.end(); iter++)
	{
		auto item = (*iter)->CreatHDF5Item(data);
		addHDF5DataItem(item);
	}
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
void Gui::DataVisualizationTree::initfactorys()
{
	HDF5DataItemFactory* factory = new HDF5DataItem3DFactory();
	std::shared_ptr<HDF5DataItemEventHander> hander(new HDF5DataItem3DDoubleClickEventHander());
	factory->setEventHander(hander);
	factorys.push_back(factory);

	factory = new HDF5DataItem2DFactory();
	hander.reset(new HDF5DataItem2DDoubleClickEventHander());
	factory->setEventHander(hander);
	factorys.push_back(factory);
}


void Gui::DataVisualizationTree::itemDoubleClicked(const QModelIndex& index)
{
	auto item = dynamic_cast<HDF5DataItem*>(model->itemFromIndex(index));
	assert(item);

	item->triggerDoubleClickEvent();
}

