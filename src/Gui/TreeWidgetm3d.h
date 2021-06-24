#pragma once
#ifndef TREEWIDGETM3D_H_
#define TREEWIDGETM3D_H_
#if 1
#include "Tree.h"
class TreeWidgetm3d :public Gui::TreeWidget
{
	Q_OBJECT
public:
	TreeWidgetm3d(QWidget* parent=0);
	~TreeWidgetm3d();
protected:
	void addSubItem(const Gui::Document&, const std::string&);
	void addSubItem2(const Gui::Document&, const std::string& GroupName,
		const std::string& KeyName, const int cusline);
	void clearsubItem(const Gui::Document&);
	void mouseDoubleClickEvent(QMouseEvent * event);
private:
	std::map <QTreeWidgetItem*, int> itemToLine;
	std::map<std::string, QTreeWidgetItem*> groupItems;
};
#else
#include <QWidget>
namespace Gui
{
	class TreeWidget;
	class Document;
};

class TreeWidgetm3d :public QWidget
{
	Q_OBJECT
public:
	TreeWidgetm3d(QWidget* parent = 0);
	~TreeWidgetm3d();
	void setRootIsDecorated(bool);
	Gui::TreeWidget* GetTreesite();
protected:
	void addSubItem(const Gui::Document&, const std::string&);
	void addSubItem2(const Gui::Document&, const std::string& GroupName,
		const std::string& KeyName, const int cusline);
	void clearsubItem(const Gui::Document&);
	void mouseDoubleClickEvent(QMouseEvent * event);
private:
	std::map <QTreeWidgetItem*, int> itemToLine;
	std::map<std::string, QTreeWidgetItem*> groupItems;
	Gui::TreeWidget* treewidget;
};
#endif
#endif