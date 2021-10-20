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
public:
	//之后继承该类的ID号，继承类之间的ID号不能相同
	//如果写了通用的处理方法，可一通过判断ID号,执行对应的操作。
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