#pragma once
#ifndef TREEVIEWCTRL_H_
#define TREEVIEWCTRL_H_
#include "DataVisualization/ListTreeWidget.h"
#include "vector"
#include "PlotAdapterBase.h"
#include "TreeNode.h"
class QStandardItem;
namespace Gui{
	class GuiExport TreeViewCtrl :public DV::ListTreeWidget
	{
	public:
		 explicit TreeViewCtrl(QWidget* parent = nullptr);
		~TreeViewCtrl();
		void upClear();
	public:
		void on_doubleclick(const QModelIndex& index);
		void loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist);
		void createIteminfo(Hdf5Data& data, int index);
		void showPlotfromData(Hdf5Data data, int index);
		
	private:
		void displayItem(QStandardItem* ,Hdf5Data&);
		void  creatItem(TreeNode&,int type=2);
		void addItem(QStandardItem*,TreeNode& ,int type);
		int judgeNewNode(QStandardItem* item, TreeNode& node, int type);
		QStandardItem* creatNewNode(TreeNode& node);
		void addMap(QStandardItem* item, TreeNode& node, int type);
		void sortNode(QStandardItem* item, QStandardItem* subitem);
	private:
		std::map<std::string, QStandardItem*> parentNodes;
		std::map<QStandardItem*, int >hdf5Indexs;
		std::map<QStandardItem*, std::shared_ptr<PlotAdapterBase>> adapterFunc;
		int structIndex;
	};
};

#endif