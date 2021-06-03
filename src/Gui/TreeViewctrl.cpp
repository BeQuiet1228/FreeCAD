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
#include "MainWindow.h"
namespace Gui{
	/**
	* @brief  Gui::TreeViewCtrl::TreeViewCtrl
	* @param  QWidget * parent  
	* @return   
	*/
	TreeViewCtrl::TreeViewCtrl(QWidget* parent):ListTreeWidget(parent){

	}
	/**
	* @brief  Gui::TreeViewCtrl::~TreeViewCtrl
	* @return   
	*/
	TreeViewCtrl::~TreeViewCtrl()
	{

	}
	/**
	* @brief  Gui::TreeViewCtrl::double_clicked_event 双击事件
	* @param  const QModelIndex & index  
	* @return void  
	*/
	void TreeViewCtrl::double_clicked_event(const QModelIndex &index)
	{
		App::Document *doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (!docM)
			return;
		//获取plot
		QStandardItem* currenitem = goodsModel->itemFromIndex(index);
		//寻找对应的hdf数据
		auto iter = datainfor.find(currenitem);
		//查找plot
		auto guidoc = Gui::Application::Instance->activeDocument();
		std::list<Gui::MDIView*> list = guidoc->getMDIViews();
		Gui::PlotMDIView* ptr = nullptr;
		for each (Gui::MDIView* var in list)
		{
			ptr = dynamic_cast<Gui::PlotMDIView*>(var);
			if (ptr) break;
		}
		if (ptr == nullptr)
		{
			Gui::PlotMDIView* plot = new Gui::PlotMDIView(*guidoc);
			Gui::MainWindow::getInstance()->addWindow(plot);
			(DocumentManager*)(docM)->bindTreeContrue(nullptr, (Plot*)plot->GetViewPtr());
			
		}
		else
		{
			(DocumentManager*)(docM)->bindTreeContrue(nullptr, (Plot*)ptr->GetViewPtr());
		}
		if (iter != datainfor.end())
		{
			//传入hdf5数据
			std::string name = (index.data().toString()).toStdString();
			docM->_ToRenderer(name, iter->second);
		}
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
};