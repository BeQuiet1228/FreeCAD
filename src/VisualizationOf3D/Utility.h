#pragma once
#ifndef UTILITY_H_
#define UTILITY_H_
#include "exPortConfig.hpp"
#include <vector>
//#include <QObject>
//class QWidget;
#include <QWidget>
#include "QStandardItem"
class VISUALZATION3D_EXPORT TreeItem :public QStandardItem
{
public:
	TreeItem();
	TreeItem(const QString& text);
	TreeItem(const QIcon& icon, const QString& text);
	explicit TreeItem(int rows, int columns = 1);
	virtual ~TreeItem();
	virtual void initUI();
public:
	int pID;
};
class VISUALZATION3D_EXPORT BaseWidget:public QWidget
{
	Q_OBJECT
public:
	explicit BaseWidget(QWidget* parent=nullptr);
	virtual ~BaseWidget();
public:
	std::vector<TreeItem*>& GetTreeItems();
public Q_SLOTS:
	virtual void slotitemStateChange(QStandardItem*);
protected:
	std::vector<TreeItem*> items;
};
#endif // !1