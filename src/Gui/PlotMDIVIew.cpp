#include "PlotMDIView.h"
#include "DataVisualization/Plot.h"
namespace Gui{
	PlotMDIView::PlotMDIView(App::Document &_doc, QWidget* parent) :MDIView(0, parent, 0)
	{
		plot = new Plot(this);
		//plot->resize(400, 300);
		//plot->resize(this->size().height(), this->size().height());
		plot->resize(this->size());
		//plot->show();
	}
	PlotMDIView::~PlotMDIView(){

	}
	void* PlotMDIView::GetViewPtr()
	{
		return (void*)plot;
	}
	void PlotMDIView::resizeEvent(QResizeEvent* _event)
	{
		//plot->resize(QSize(this->size().height(), this->size().height()));
		plot->resize(this->size());
	}
}
#include "moc_PlotMDIView.cpp"