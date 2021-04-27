#include "PlotMDIView.h"
#include "DataVisualization/Plot.h"
namespace Gui{
	/**
	* @brief PlotMDIView::PlotMDIView 构造函数
	* @param App::Document &_doc
	* @param QWidget* parent
	*/
	PlotMDIView::PlotMDIView(Gui::Document &_doc, QWidget* parent) :MDIView(&_doc, parent, 0)
	{
		plot = new Plot(this);
		plot->resize(this->size());
		//bIsPassive = false;
	}
	PlotMDIView::~PlotMDIView(){
		printf("析构\n");
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
	/**
	* @brief PlotMDIView::canClose
	* @return bool
	*/
	bool PlotMDIView::canClose()
	{
		return true;
	}
}
#include "moc_PlotMDIView.cpp"