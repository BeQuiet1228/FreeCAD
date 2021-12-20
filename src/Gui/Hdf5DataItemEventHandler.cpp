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

	auto controler = DV3D::ControlerFactory::CreatControler(item->getHdf5Data());
	auto controlerItem = DV3D::ControlerItemFactor::CreatControlerItem();
	controlerItem->setControler(controler);

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
	}

	view3d->getWidget3D()->binding(controler.get());

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

/**
* @brief Gui::CreatControlerListWidget 创建一个listitemWidget 并添加到悬浮窗口中
* @return Gui::ControlerItemListWidget*
*/
Gui::ControlerItemListWidget* Gui::CreatControlerListWidget()
{
	auto listItem = new ControlerItemListWidget;
	listItem->setObjectName(QString::fromLocal8Bit("ControlerItemListWidget"));
	DockWindowManager::instance()->addDockWindow("3dControler", listItem, Qt::DockWidgetArea::RightDockWidgetArea)->show();

	return listItem;
}

void Gui::hideControlerListWidget()
{
	auto widget = DockWindowManager::instance()->getDockWindow("3dControler");
	if (!widget)
		return;
	auto docWidget = dynamic_cast<QDockWidget*>(widget->parent());
	docWidget->hide();
}

void Gui::showControlerListWidget()
{
	auto widget = DockWindowManager::instance()->getDockWindow("3dControler");
	if (!widget)
		return;
	auto docWidget = dynamic_cast<QDockWidget*>(widget->parent());
	docWidget->show();
}
