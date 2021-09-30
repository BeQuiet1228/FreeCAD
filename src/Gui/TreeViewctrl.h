#pragma once
#ifndef TREEVIEWCTRL_H_
#define TREEVIEWCTRL_H_
#include "DataVisualization/ListTreeWidget.h"
namespace Gui{
	class GuiExport TreeViewCtrl :public ListTreeWidget
	{
	public:
		 explicit TreeViewCtrl(QWidget* parent = nullptr);
		~TreeViewCtrl();
		void upClear();
	public:
		virtual void double_clicked_event(const QModelIndex &index);
		virtual void fromWidget(std::shared_ptr<QWidget>);
	};
};

#endif