#pragma once
#ifndef TREEVIEWCTRL_H_
#define TREEVIEWCTRL_H_
#include "DataVisualization/ListTreeWidget.h"
#include "vector"
class QStandardItem;
namespace Gui{
	class GuiExport TreeViewCtrl :public ListTreeWidget
	{
	public:
		 explicit TreeViewCtrl(QWidget* parent = nullptr);
		~TreeViewCtrl();
		void upClear();
	public:
		void on_doubleclick(const QModelIndex& index);
		void soltFromWidget(QWidget*);
	};
};

#endif