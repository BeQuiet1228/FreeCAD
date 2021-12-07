#include "PreCompiled.h"
#include"TreeViewctrl.h"
#include "App/Document.h"
#include "App/DocumentDataManager.h"
#include <HDF5Reader/hdf5io.h>
#include "Contorl/ContorlInterface.h"
//
#include "Gui/Document.h"
#include "Application.h"
#include "PlotMDIView.h"
#include"PLaneMDIView.h"
#include "MainWindow.h"
#include"iostream"
#include"VisualizationOf3D/Widget3D.h"
#include "QDebug"
#include"DataVisualization/RendererFactory.h"

namespace Gui{
	TreeViewCtrl::TreeViewCtrl(QWidget* parent):ListTreeWidget(parent){
		structIndex = -1;
	}
	TreeViewCtrl::~TreeViewCtrl()
	{
	}
	void TreeViewCtrl::upClear()
	{
		structIndex = -1;
		clear();
		//获取当前活跃的Document;
		App::Document *doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (docM)
			docM->dataclear();
	}
	/**
	* @brief Gui::TreeViewCtrl::on_doubleclick 双击事件
	* @param const QModelIndex & index
	* @return void
	*/
	void TreeViewCtrl::on_doubleclick(const QModelIndex& index)
	{
		//寻找对应的hdf数据
		//获取到QStandardItem*
		QStandardItem* currentItem = goodsModel->itemFromIndex(index);
		auto dataItem=datainfor.find(currentItem);
		if (dataItem == datainfor.end())
			return;

		App::Document* doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (!docM)
		{
			std::cerr << "DocumentManager is null from FreeCadGui void TreeViewCtrl::double_clicked_event(const QModelIndex &index)" << std::endl;
			return;
		}
		std::string name = (index.data().toString()).toStdString();
		auto h5d = docM->gethdf5dataList()[dataItem->second.index];
		auto itemfunc = adapterFunc.find(currentItem);
		if (itemfunc != adapterFunc.end())
		{
			itemfunc->second->doubleEvent(h5d, name);
		}
	}
	void TreeViewCtrl::displayItem(QStandardItem* item,Hdf5Data& data)
	{
		auto dataItem = datainfor.find(item);
		if (dataItem == datainfor.end())
			return;
		std::string name = item->text().toStdString();
		auto itemfunc = adapterFunc.find(item);
		if (itemfunc != adapterFunc.end())
		{
			itemfunc->second->doubleEvent(data, name);
		}
	}
	/**
	* @brief Gui::TreeViewCtrl::loadHdflist 读取hdf5数据组，批量生成Item
	* @param std::vector<Hdf5Data> & Hdf5Datalist
	* @return void
	*/
	
	void TreeViewCtrl::loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist)
	{
		auto index=DV::RendererFactory::findStructDataIndex(Hdf5Datalist);
		if (-1 != index)
		{
			structIndex = index;
		}
		//增加清理流程
		clear();
		for (auto index=0;index<Hdf5Datalist.size();index++)
		{
			createIteminfo(Hdf5Datalist[index],index);
		}
	}
	/**
	* @brief Gui::TreeViewCtrl::createIteminfo 根据传入的数据和id生成item，并保存到内部字典
	* @param Hdf5Data & data
	* @param int index
	* @return void
	*/
	
	void TreeViewCtrl::createIteminfo(Hdf5Data& data, int index)
	{
		if (data.name.find("struct") != std::string::npos)
		{
			toStructh5df(data, index);
		}
		else if (data.name.find("PLANE") != std::string::npos)
		{
			//正投影面暂时不用
		}
		else//其他图
		{
			fromdataManageNewData(data, index);
		}
	}
	std::vector<QStandardItem*> TreeViewCtrl::toStructh5df(Hdf5Data& data, int index) {
		auto itemList=ListTreeWidget::toStructh5df(data,index);
		for (auto item:itemList)
		{
			//创建
			std::shared_ptr<PlotAdapterBase> plotadapter = std::shared_ptr<PlotAdapterBase>(new PlotAdapter2D(data));
			adapterFunc[item]=plotadapter;
		}
		structIndex = index;
		return itemList;
	}
	
	/**
	* @brief Gui::TreeViewCtrl::fromdataManageNewData 将非结构图的2维数据生成对应的item，并保存字典
	* @param Hdf5Data & data
	* @param int index
	* @return QT_NAMESPACE::QStandardItem*
	*/
	QStandardItem* TreeViewCtrl::fromdataManageNewData(Hdf5Data& data, int index) {
		auto item=ListTreeWidget::fromdataManageNewData(data,index);
		std::shared_ptr<PlotAdapterBase> funcPtr;
		if (-1 != structIndex)
		{
			App::Document* doc = App::GetApplication().getActiveDocument();
			DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
			if (nullptr != docM)
			{
				auto h5dStruct = docM->gethdf5dataList()[structIndex];
				funcPtr = std::shared_ptr<PlotAdapterBase>(new PlotAdapter2D(h5dStruct));
				adapterFunc[item] = funcPtr;
				return item;
			}
		}
		funcPtr = std::shared_ptr<PlotAdapterBase>(new PlotAdapter2D());
		adapterFunc[item] = funcPtr;
		return item;
	}
	/**
	* @brief Gui::TreeViewCtrl::showPlotfromData 用于直接传入hdf5data数据和类型时显示
	* @param Hdf5Data data
	* @param int _type
	* @return void
	* @time	2021/12/02
	*/
	void TreeViewCtrl::showPlotfromData(Hdf5Data data, int index)
	{
		auto item=fromdataManageNewData(data,index);
		displayItem(item, data);
	}
};

#include"moc_TreeViewctrl.cpp"