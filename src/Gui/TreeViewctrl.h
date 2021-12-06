#pragma once
#ifndef TREEVIEWCTRL_H_
#define TREEVIEWCTRL_H_
#include "DataVisualization/ListTreeWidget.h"
#include "vector"
#include "PlotAdapterBase.h"
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
		//∂¿¡¢œ‘ æ
		//void Application::DisplatPlot(Hdf5Data data, int _type /*= 0*/)
		void showPlotfromData(Hdf5Data data, int _type=0);
	private:
		std::vector<QStandardItem*> toStructh5df(Hdf5Data& data, int index);
		QStandardItem* fromdataManageNewData(Hdf5Data& data, int index);
	private:
		std::map<QStandardItem*, std::shared_ptr<PlotAdapterBase>> adapterFunc;
		int structIndex;
	};
};

#endif