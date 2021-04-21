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
class DATA_VISUALIZATION_EXPORT ListTreeWidget:public QWidget
{
	Q_OBJECT
public:
	explicit ListTreeWidget(QWidget* parent=nullptr);
	~ListTreeWidget();
protected:
	virtual void resizeEvent(QResizeEvent * event) override;
	std::string GetType(std::string name);
	Q_SIGNALS:
	void _transfromRenderer(std::string name,int index);
public Q_SLOTS:
	void loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist);
	void on_doubleclick(const QModelIndex &index);
private:
	QTreeView* m_TreeView;
	QStandardItemModel *goodsModel;
	std::map <QStandardItem*, int> datainfor;
};
#endif