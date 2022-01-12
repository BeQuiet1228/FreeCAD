#include "PreCompiled.h"
#include "Hdf5DataItemEventHandler.h"
#include "Hdf5DataItem.h"
#include "DockWindowManager.h"
#include "ControlerItemListWidget.h"
#include "DataVisualization/3D/controler.h"
#include "DataVisualization/3D/ControlerFactory.h"
#include "DataVisualization/3D/controlerItemFactor.h"
#include "DataVisualization/3D/ControlerItem.h"
#include "Application.h"
#include "DocumentPic.h"
#include "DataVisualization3dView.h"
#include "MainWindow.h"
#include "FileDialog.h"
#include <mutex>
#include <cassert>
#include <QDockWidget>
#include <QWidget>
#include <cassert>


void Gui::HDF5DataItem3DDoubleClickEventHander::trigger(HDF5DataItem* item)
{
	assert(item && "item is nullptr!");

	//单独处理特殊情况下的结构图
	auto controler = creatStructControler(item);

	if(!controler)
		controler = DV3D::ControlerFactory::CreatControler(item->getHdf5Data());

	controler->setObjectName(item->getNmae().toStdString());
	auto controlerItem = DV3D::ControlerItemFactor::CreatContour3dControlerItem();

	//添加一个save按钮 ，并且传入工程路径作为路径选择的文件浏览器起始路径
	auto workPath = Gui::FileDialog::getWorkingDirectory();
	DV3D::ControlerItemFactor::AddSaveAction(controlerItem, item->getHdf5Data(), workPath);

	controlerItem->setControler(controler);
	controlerItem->setName(item->getNmae());

	showView3D(controlerItem);
}


std::shared_ptr<DV3D::Controler> Gui::HDF5DataItem3DDoubleClickEventHander::creatStructControler(HDF5DataItem* item)
{
	auto hdf5Data = item->getHdf5Data();
	if (hdf5Data.name != "struct")
		return nullptr;
	if (item->getNmae() != QString::fromLocal8Bit("Struct"))
		return nullptr;

	auto controler = DV3D::ControlerFactory::CreatStrucRotateControler(item->getHdf5Data());
	return controler;
}

void Gui::HDF5DataItem3DDoubleClickEventHander::showView3D(DV3D::ControlerItem* controlerItem)
{
	auto doc = Gui::Application::Instance->activeDocument();
	auto picDoc = dynamic_cast<DocumentPic*> (doc);

	assert(picDoc && "picDoc is nullptr!");

	auto mdiViews = picDoc->getMDIViews();
	auto iter = mdiViews.begin();
	Gui::DataVisualizationView* view3d = nullptr;
	for (; iter != mdiViews.end(); iter++)
	{
		view3d = dynamic_cast<Gui::DataVisualizationView*>(*iter);
		if (view3d)
			break;
	}

	auto mw = Gui::MainWindow::getInstance();
	if (view3d == nullptr)
	{
		view3d = new Gui::DataVisualizationView(picDoc);
		mw->addWindow(view3d);
		view3d->setWindowTitle(QString::fromLocal8Bit("3D_Plot"));
	}
	mw->setActiveWindow(view3d);


	view3d->addControler(controlerItem->getControler());

	auto listWidget = getControlerListWidget();
	if (!listWidget)
		listWidget = CreatControlerListWidget();
	listWidget->addWidget(controlerItem);
	showControlerListWidget();
}

/**
* @brief Gui::getControlerListWidget  获取一个listItemWidget 获取失败返回nullptr
* @return Gui::ControlerItemListWidget*
*/
Gui::ControlerItemListWidget* Gui::getControlerListWidget()
{
	auto widget = DockWindowManager::instance()->getDockWindow("3dControler");
	if (!widget)
		return nullptr;

	auto listWidget = dynamic_cast<ControlerItemListWidget*>(widget);

	return listWidget;
}

