#pragma once
#include <QTreeView>
#include <QStandardItemModel>
#include "Hdf5DataItem.h"
namespace Gui {
	class DataVisualizationTree :public QTreeView{
		Q_OBJECT
	public:
		DataVisualizationTree(QWidget* parent= 0);
		~DataVisualizationTree();

	public:
		void addHDF5DataItem(HDF5DataItem* item);
		void addHDF5DataItem(std::vector<HDF5DataItem*> items);
	private:
		QStandardItemModel* model;

	public Q_SLOTS:
		void itemDoubleClicked(const QModelIndex& index);
		
	};
}