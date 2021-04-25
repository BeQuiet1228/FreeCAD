#include "PlotMDIView.h"
#include "DataVisualization/Plot.h"
namespace Gui{
	/**
	* @brief PlotMDIView::PlotMDIView 构造函数
	* @param App::Document &_doc
	* @param QWidget* parent
	*/
	PlotMDIView::PlotMDIView(App::Document &_doc, QWidget* parent) :MDIView(0, parent, 0)
	{
		plot = new Plot(this);
		plot->resize(this->size());
	}
	PlotMDIView::~PlotMDIView(){

	}
	/**
	* @brief PlotMDIView::GetViewPtr 获取plot控件的指针
	* @return void 
	*/
	void* PlotMDIView::GetViewPtr()
	{
		return (void*)plot;
	}
	/**
	* @brief PlotMDIView::resizeEvent 自适应大小
	* @param QResizeEvent* _event
	* @return void
	*/
	void PlotMDIView::resizeEvent(QResizeEvent* _event)
	{
		plot->resize(this->size());
	}
}
#include "moc_PlotMDIView.cpp"