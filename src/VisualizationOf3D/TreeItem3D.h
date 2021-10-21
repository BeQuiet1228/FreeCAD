#pragma once
#ifndef TREEITEM3D_H_
#define TREEITEM3D_H_
#include "Utility.h"
class TreeItem3D :public TreeItem
{
public:
	TreeItem3D();
	TreeItem3D(const QString& text);
	TreeItem3D(const QIcon& icon, const QString& text);
	explicit TreeItem3D(int rows, int columns = 1);
	virtual ~TreeItem3D();
	void setParent(QWidget* parent=nullptr);
protected:
	QWidget* parentWidget;
};
#endif