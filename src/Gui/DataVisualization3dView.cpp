#include "DataVisualization3dView.h"
#include "ControlerItemListWidget.h"
#include "DataVisualization/3D/controler.h"
Gui::DataVisualizationView::DataVisualizationView(DocumentPic* doc)
	:MDIViewPIC(doc)
{
	initGui();
}

void Gui::DataVisualizationView::initGui()
{
	widget3d = new DV3D::Widget3D(this);
	setCentralWidget(widget3d);
}

/**
* @brief Gui::DataVisualizationView::removeStructControler 移除结构图控制器 结构图标签需要在创建controler时 将图标的名称作为objectName传入
* @return void
*/
void Gui::DataVisualizationView::removeStructControler()
{
	auto controlerMap = widget3d->getControlerActorMap();

	for (auto iter = controlerMap.begin(); iter != controlerMap.end(); iter++)
	{
		auto controler = iter->first;
		if (controler->getObjectName() == "Struct" || controler->getObjectName() == "Grid")
		{
			widget3d->unbing(controler);
			removeControlerItemWidget(controler);
		}
	}
}

/**
* @brief Gui::DataVisualizationView::removeOtherControler 同removeStrucControler
* @return void
*/
void Gui::DataVisualizationView::removeOtherControler()
{
	auto controlerMap = widget3d->getControlerActorMap();

	for (auto iter = controlerMap.begin(); iter != controlerMap.end(); iter++)
	{
		auto controler = iter->first;
		if (controler->getObjectName() == "Struct" || controler->getObjectName() == "Grid")
			continue;

		widget3d->unbing(controler);
		removeControlerItemWidget(controler);
	}
	widget3d->scalarBarOff();
}

void Gui::DataVisualizationView::removeControlerItemWidget(DV3D::Controler* controler)
{
	auto listWidget = getControlerListWidget();
	if (!listWidget)
		return;
	listWidget->removeControlerItemWithControler(controler);
}

void Gui::DataVisualizationView::closeEvent(QCloseEvent* e)
{
	MDIViewPIC::closeEvent(e);
	auto listWidget = getControlerListWidget();
	if (!listWidget)
		return;
	listWidget->clearWidget();
	hideControlerListWidget();
}

DV3D::Widget3D* Gui::DataVisualizationView::getWidget3D()
{
	return widget3d;
}

/**
* @brief Gui::DataVisualizationView::addControler 添加一个控制器 
* @param std::shared_ptr<DV3D::Controler> controler
* @return void
*/
void Gui::DataVisualizationView::addControler(std::shared_ptr<DV3D::Controler> controler)
{
	/*
		按目前的逻辑，只允许同时显示一个结构图和其他图。
		如 结构图只能显示 struct 或者grid,等位图、粒子图、矢量图 只能同时与结构图显示一张。
		所以在添加控制器时需要按需求移除其他的控制器。
	*/

	if (controler->getObjectName() == "Struct" || controler->getObjectName() == "Grid")
		removeStructControler();
	else
		removeOtherControler();

	widget3d->scalarBarOn(controler.get());
	widget3d->binding(controler.get());
}

bool Gui::DataVisualizationView::onMsg(const char* pMsg, const char** ppReturn)
{
	return getDocumengPic()->onHasMsg(pMsg);
}

bool Gui::DataVisualizationView::onHasMsg(const char* pMsg) const
{
	return getDocumengPic()->onHasMsg(pMsg);
}

