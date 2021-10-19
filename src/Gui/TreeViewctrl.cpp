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
		QStandardItem* currenitem = goodsModel->itemFromIndex(index);
		auto iter = datainfor.find(currenitem);
		if (iter == datainfor.end())
			return;
		App::Document* doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (!docM)
		{
			std::cerr << "DocumentManager is null from FreeCadGui void TreeViewCtrl::double_clicked_event(const QModelIndex &index)" << std::endl;
			return;
		}
		//获取plot
		//查找plot
		auto guidoc = dynamic_cast<DocumentPic*>(Gui::Application::Instance->activeDocument());
		std::list<Gui::MDIView*> list = guidoc->getMDIViews();
		Gui::PlotMDIView* ptr = nullptr;
		for each (Gui::MDIView * var in list)
		{
			ptr = dynamic_cast<Gui::PlotMDIView*>(var);
			if (ptr) break;
		}
		if (ptr == nullptr)
		{
			ptr = new Gui::PlotMDIView(guidoc);
			//Gui::PlotMDIView* plot = new Gui::PlotMDIView(*guidoc);
			Gui::MainWindow::getInstance()->addWindow(ptr);
			docM->bindTreeContrue(nullptr, ptr->GetViewPtr());
		}
		else
		{
			docM->bindTreeContrue(nullptr, ptr->GetViewPtr());
		}
		//确保当前页面为活动页
		MainWindow::getInstance()->setActiveWindow(ptr);
		if (iter != datainfor.end())
		{
			//传入hdf5数据
			std::string name = (index.data().toString()).toStdString();
			docM->_ToRenderer(name, iter->second.index);
		}
	}
	/**
	* @brief Gui::TreeViewCtrl::soltFromWidget 获取窗口指针
	* @param QWidget * wid3D
	* @return void
	*/
	
	void TreeViewCtrl::soltFromWidget(QWidget* wid3D)
	{
		App::Document* doc = App::GetApplication().getActiveDocument();
		DocumentManager* docM = dynamic_cast<DocumentManager*>(doc);
		if (!docM)
		{
			std::cerr << "DocumentManager is null from FreeCadGui void TreeViewCtrl::double_clicked_event(const QModelIndex &index)" << std::endl;
			return;
		}
		
		//获取
		auto guidoc = dynamic_cast<DocumentPic*>(Gui::Application::Instance->activeDocument());
		std::list<Gui::MDIView*> list = guidoc->getMDIViews();
		Gui::PlanMDIView* ptr = nullptr;
		for each (Gui::MDIView * var in list)
		{
			ptr = dynamic_cast<Gui::PlanMDIView*>(var);
			if (ptr) break;
		}
		if (nullptr == wid3D)
		{
			if (nullptr == ptr)
			{
				return;
			}
			else
			{
				MainWindow::getInstance()->setActiveWindow(ptr);
			}
			return;
		}
		if (nullptr == ptr)
		{
			ptr = new Gui::PlanMDIView(guidoc);
			ptr->setWidget(wid3D);
			Gui::MainWindow::getInstance()->addWindow(ptr);
		}
		else
			ptr->setWidget(wid3D);
		BaseWidget* baseWidget = dynamic_cast<BaseWidget*>(wid3D);
		auto items = baseWidget->GetTreeItems();
		QStandardItem* currenitem = goodsModel->itemFromIndex(m_TreeView->currentIndex());
		if (currenitem->hasChildren() > 0)
		{
			currenitem->removeRows(0, currenitem->rowCount());
		}
		for (auto iter = items.begin(); iter != items.end(); iter++)
		{
			int subrow = currenitem->rowCount();
			currenitem->setChild(subrow, *iter);
		}
		connect(goodsModel, SIGNAL(itemChanged(QStandardItem*)), baseWidget, SLOT(slotitemStateChange(QStandardItem*)));
		MainWindow::getInstance()->setActiveWindow(ptr);
	}
};
#include"moc_TreeViewctrl.cpp"