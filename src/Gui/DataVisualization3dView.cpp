#include "DataVisualization3dView.h"
#include "ControlerItemListWidget.h"

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

