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
#include <mutex>
#include <cassert>
#include <QDockWidget>
#include <QWidget>
#include <cassert>


void Gui::HDF5DataItem3DDoubleClickEventHander::trigger(HDF5DataItem* item)
{
	assert(item && "item is nullptr!");

	//单独处理特殊情况下的结构图
	if (disposStructItem(item))
		return;

	auto controler = DV3D::ControlerFactory::CreatControler(item->getHdf5Data());
	auto controlerItem = DV3D::ControlerItemFactor::CreatContour3dControlerItem();
	controlerItem->setControler(controler);

	showView3D(controlerItem);
}

/**
* @brief Gui::HDF5DataItem3DDoubleClickEventHander::disposStructItem 处理需要旋转得到的结构图
* @param HDF5DataItem * item
* @return bool
*/
bool Gui::HDF5DataItem3DDoubleClickEventHander::disposStructItem(HDF5DataItem* item)
{
	auto hdf5Data = item->getHdf5Data();
	if (hdf5Data.name != "struct")
		return false;
	if (item->getNmae() !=  QString::fromLocal8Bit("Struct"))
		return false;

	auto controler = DV3D::ControlerFactory::CreatStrucRotateControler(item->getHdf5Data());
	auto controlerItem = DV3D::ControlerItemFactor::CreatContour3dControlerItem();
	controlerItem->setControler(controler);

	showView3D(controlerItem);
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

	if (view3d == nullptr)
	{
		auto mw = Gui::MainWindow::getInstance();
		view3d = new Gui::DataVisualizationView(picDoc);
		mw->addWindow(view3d);
		view3d->setWindowTitle(QString::fromLocal8Bit("3D_Plot"));
	}

	view3d->getWidget3D()->binding(controlerItem->getControler().get());

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

