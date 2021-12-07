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
	protected:
		virtual void resizeEvent(QResizeEvent* event) override;
	public Q_SLOTS:
		virtual void on_doubleclick(const QModelIndex& index);
	public:
		void clear();
	protected:
		QTreeView* m_TreeView;
		QStandardItemModel* goodsModel;
	};
};
#endif