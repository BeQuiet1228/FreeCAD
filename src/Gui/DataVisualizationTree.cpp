#include "DataVisualizationTree.h"
#include <cassert>
#include "QDebug"
Gui::DataVisualizationTree::DataVisualizationTree(QWidget* parent/*= 0*/)
	:QTreeView(parent),model(new QStandardItemModel)
{
	connect(this, SIGNAL(doubleClicked(QModelIndex)), this, SLOT(itemDoubleClicked(QModelIndex)));
	setModel(model);
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

void Gui::DataVisualizationTree::itemDoubleClicked(const QModelIndex& index)
{
	auto item = dynamic_cast<HDF5DataItem*>(model->itemFromIndex(index));
	assert(item);

	item->triggerDoubleClickEvent();
}

