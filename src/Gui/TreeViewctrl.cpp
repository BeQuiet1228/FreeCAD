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
	TreeViewCtrl::TreeViewCtrl(QWidget* parent):ListTreeWidget(parent){

	}
	TreeViewCtrl::~TreeViewCtrl()
	{

	}
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
			Gui::PlotMDIView* plot = new Gui::PlotMDIView(*guidoc->getDocument());
			Gui::MainWindow::getInstance()->addWindow(plot);
			(DocumentManager*)(docM)->bindTreeContrue(nullptr, (Plot*)plot->GetViewPtr());
			guidoc->attachView(plot, false);
		}
		if (iter != datainfor.end())
		{
			//传入hdf5数据
			std::string name = (index.data().toString()).toStdString();
			docM->_ToRenderer(name, iter->second);
		}
	}
};
//#include "moc_TreeViewctrl.cpp"