#pragma once
#ifndef TREEVIEWCTRL_H_
#define TREEVIEWCTRL_H_
#include "DataVisualization/ListTreeWidget.h"
class TreeViewCtrl:public ListTreeWidget
{
public:
	TreeViewCtrl(QWidget* parent=nullptr);
	~TreeViewCtrl();
	
};
#endif