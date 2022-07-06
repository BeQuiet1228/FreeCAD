#pragma once
#include <QTreeView>
#include <QStandardItemModel>
#include <vector>
#include "Hdf5DataItem.h"
#include "hdf5DataItemFactory.h"

namespace OriginUI {
	class InputLineEdit;
}
namespace Gui {
	class DataVisualizationTree :public QWidget{
		Q_OBJECT
	public:
		DataVisualizationTree(QWidget* parent= 0);
		~DataVisualizationTree();

	public:
		HDF5DataItem* addHDF5DataItem(HDF5DataItem* item);
		void addHDF5DataItem(std::vector<HDF5DataItem*> items);
		//清理item
		void clear();

		//载入hdf数据
		void loadHdf5Datas(std::vector<Hdf5Data> datas);
		HDF5DataItem* addHdf5Data(Hdf5Data& data);
		void addHdf5DataToShow(Hdf5Data& data);
		void addHdf5Data(std::vector<Hdf5Data> datas);

	private:
		void initFactorys();
		void clearFactorys();
		std::vector<HDF5DataItem*> creatHdf5DataItem(Hdf5Data data);
	private:
		//item mod
		QStandardItemModel* model;
		//工厂
		std::vector<std::shared_ptr<HDF5DataItemFactory>> factorys;
		//树控件
		QTreeView* treeView;
		//搜索框
		OriginUI::InputLineEdit* searchLineEdit;
	public Q_SLOTS:
		void itemDoubleClicked(const QModelIndex& index);
		
	};
}