#include "DataVisualization3dView.h"

Gui::DataVisualizationView::DataVisualizationView(DocumentPic* doc)
	:MDIEditView(doc)
{
	initGui();
}

void Gui::DataVisualizationView::initGui()
{
	widget3d = new DV3D::Widget3D(this);
	setCentralWidget(widget3d);
}

DV3D::Widget3D* Gui::DataVisualizationView::getWidget3D()
{
	return widget3d;
}

