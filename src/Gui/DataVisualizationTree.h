#pragma once
#include <QTreeView>
#include <QStandardItemModel>
#include <vector>
#include "Hdf5DataItem.h"
#include "hdf5DataItemFactory.h"
namespace Gui {
	class DataVisualizationTree :public QTreeView{
		Q_OBJECT
	public:
		DataVisualizationTree(QWidget* parent= 0);
		~DataVisualizationTree();

	public:
		void addHDF5DataItem(HDF5DataItem* item);
		void addHDF5DataItem(std::vector<HDF5DataItem*> items);
		//清理item
		void clear();

		//载入hdf数据
		void loadHdf5Datas(std::vector<Hdf5Data> datas);
		void addHdf5Data(Hdf5Data& data);
		void addHdf5Data(std::vector<Hdf5Data> datas);

	private:
		void initfactorys();
	private:
		//item mod
		QStandardItemModel* model;
		//工厂
		std::vector<HDF5DataItemFactory*> factorys;
	public Q_SLOTS:
		void itemDoubleClicked(const QModelIndex& index);
		
	};
}