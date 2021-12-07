#include "PreCompiled.h"
#include "Item3DDoubleClickEvent.h"
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
void Gui::Item3DDoubleClickEvent::doubleEvent(Hdf5Data h5d, std::string name)
{
	static std::once_flag flag;
	std::call_once(flag,[&] {
		auto listItem = new ControlerItemListWidget;
		DockWindowManager::instance()->addDockWindow("3dControler", listItem);
		});

	
	auto controler = DV3D::ControlerFactory::CreatStrucControler(h5d);
	auto controlerItem = DV3D::ControlerItemFactor::CreatControlerItem();
	controlerItem->setControler(controler);

	auto doc = Gui::Application::Instance->activeDocument();
	auto picDoc = dynamic_cast<DocumentPic*> (doc);

	assert(picDoc && "picDoc is nullptr!");

	auto mdiViews = picDoc->getMDIViews();
	auto iter = mdiViews.begin();
	Gui::DataVisualizationView * view3d = nullptr;
	for (;iter != mdiViews.end(); iter++)
	{
		view3d = dynamic_cast<Gui::DataVisualizationView*>(*iter);
		if(view3d)
			break;
	}

	if (view3d == nullptr)
	{
		auto mw = Gui::MainWindow::getInstance();
		view3d = new Gui::DataVisualizationView(picDoc);
		mw->addWindow(view3d);
	}

	view3d->getWidget3D()->binding(controler.get());

	auto dockWindow = Gui::DockWindowManager::instance()->getDockWindow("3dControler");
	dockWindow->show();
}
