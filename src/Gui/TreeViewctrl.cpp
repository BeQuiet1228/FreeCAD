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
namespace Gui{
	/**
	* @brief  Gui::TreeViewCtrl::TreeViewCtrl 构造
	* @param  QWidget * parent  
	* @return   
	*/
	TreeViewCtrl::TreeViewCtrl(QWidget* parent):ListTreeWidget(parent){

	}
	/**
	* @brief  Gui::TreeViewCtrl::~TreeViewCtrl 析构
	* @return   
	*/
	TreeViewCtrl::~TreeViewCtrl()
	{
	}
	/**
	* @brief  Gui::TreeViewCtrl::upClear 数据清除
	* @return void  
	*/
	void TreeViewCtrl::upClear()
	{
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
	}
	void TreeViewCtrl::loadHdflist(std::vector<Hdf5Data>& Hdf5Datalist)
	{
		//增加清理流程
		clear();
		for (auto index=0;index<Hdf5Datalist.size();index++)
		{
			createIteminfo(Hdf5Datalist[index],index);
		}
	}
	void TreeViewCtrl::createIteminfo(Hdf5Data& data, int index)
	{
		if (data.name.find("struct") != std::string::npos)
		{
			toStructh5df(data, index);
		}
		else if (data.name.find("PLANE") != std::string::npos)
		{

		}
		else//其他图
		{
			fromdataManageNewData(data, index);
		}
	}
	std::vector<QStandardItem*> TreeViewCtrl::toStructh5df(Hdf5Data& data, int index) {
		return ListTreeWidget::toStructh5df(data,index);
	}
	QStandardItem* TreeViewCtrl::fromdataManageNewData(Hdf5Data& data, int index) {
		return ListTreeWidget::fromdataManageNewData(data,index);
	}
};

#include"moc_TreeViewctrl.cpp"