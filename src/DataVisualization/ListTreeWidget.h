#pragma once
#ifndef LIST_TREE_WIDGET_H_
#define LIST_TREE_WIDGET_H_
//Ê÷×´ÁÐ±í¿Ø¼þ
#include<QWidget>
#include<QTreeView>
#include <vector>
#include <HDF5Reader/hdf5io.h>
#include <QStandardItemModel>
class ListTreeWidget:public QWidget
{
	Q_OBJECT
public:
	explicit ListTreeWidget(QWidget* parent=nullptr);
	~ListTreeWidget();
	
protected:
	virtual void resizeEvent(QResizeEvent * event) override;
signals:
	void _transfromRenderer(std::string name,Hdf5Data data);
public slots:
	void loadHdflist(std::vector<Hdf5Data> Hdf5Datalist);
	void on_doubleclick(const QModelIndex &index);
private:
	QTreeView* m_TreeView;
	QStandardItemModel *goodsModel;
	std::map <QStandardItem*,Hdf5Data> datainfor;
};
#endif