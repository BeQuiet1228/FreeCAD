#pragma once
#ifndef LIST_TREE_WIDGET_H_
#define LIST_TREE_WIDGET_H_
//Ê÷×´ÁÐ±í¿Ø¼þ
#include<QTreeView>
#include <vector>
#include <HDF5Reader/hdf5io.h>
#include <QStandardItemModel>
#include <string>
#include "exportConfig.hpp"
namespace DV {
	class DATA_VISUALIZATION_EXPORT ListTreeWidget :public QWidget
	{
		Q_OBJECT
	public:
		explicit ListTreeWidget(QWidget* parent = nullptr);
		virtual ~ListTreeWidget();
		struct  itemInfo
		{
			itemInfo() :index(-1), time(-1.0f) {}
			int index;
			double time;
		};
	protected:
		virtual void resizeEvent(QResizeEvent* event) override;
		std::string GetType(std::string name);
	Q_SIGNALS:
		void _transfromRenderer(std::string name, int index);
	public Q_SLOTS:
		virtual void on_doubleclick(const QModelIndex& index);
	public:
		void clear();
		virtual void loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist);
		virtual std::vector<QStandardItem*> toStructh5df(Hdf5Data& data, int index);
		virtual QStandardItem* fromdataManageNewData(Hdf5Data& data, int index);
		void toPlaneh5df(Hdf5Data& data, int index);
	protected:
		QTreeView* m_TreeView;
		QStandardItemModel* goodsModel;
		std::map <QStandardItem*, itemInfo> datainfor;
		std::map<std::string, QStandardItem*> parentnode;
	};
};
#endif