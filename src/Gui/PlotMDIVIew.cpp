#include "PreCompiled.h"
#include "PlotMDIView.h"
#include "DataVisualization/Plot.h"
TYPESYSTEM_SOURCE_ABSTRACT(Gui::PlotMDIView, Gui::MDIView);
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
		contourStateGetter = new ContourRenderStateGetter(plot);
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

	bool PlotMDIView::onMsg(const char* pMsg, const char** ppReturn)
	{
		if (strcmp("Undo", pMsg) == 0)
		{
			plot->undo();
			return true;
		}else if (strcmp("Redo", pMsg) == 0)
		{
			plot->redo();
			return true;
		}else if (strcmp("ContourImageMod", pMsg) == 0)
		{
			ContourRenderStateGetter::DisplayMod mod = contourStateGetter->getDisplayMod();
			mod = ContourRenderStateGetter::DisplayMod(mod ^ ContourRenderStateGetter::IMAGE);
			contourStateGetter->setDisplayMode(mod);
			mod = contourStateGetter->getDisplayMod();
			if ((mod & ContourRenderStateGetter::IMAGE) == ContourRenderStateGetter::IMAGE)
			{
				*ppReturn = "on";
			}else {
				*ppReturn = "off";
			}
			plot->reRender();
		}else if (strcmp("ContourLineMod", pMsg) == 0) {
			ContourRenderStateGetter::DisplayMod mod = contourStateGetter->getDisplayMod();
			mod = ContourRenderStateGetter::DisplayMod(mod ^ ContourRenderStateGetter::CONTOUR);
			contourStateGetter->setDisplayMode(mod);
			mod = contourStateGetter->getDisplayMod();
			if ((mod & ContourRenderStateGetter::CONTOUR) == ContourRenderStateGetter::CONTOUR)
			{
				*ppReturn = "on";
			}
			else {
				*ppReturn = "off";
			}
			plot->reRender();
		}else if (strcmp("PlotDisplayMod", pMsg) == 0) {
			plot->setGridLineEnabled(!plot->getGridLineEnabled());
			if (plot->getGridLineEnabled())
			{
				*ppReturn = "on";
			}
			else {
				*ppReturn = "off";
			}
		}
		else if (strcmp("AutoMax", pMsg) == 0) {
			plot->autoMaxRender();
		}
		return false;
	}

	bool PlotMDIView::onHasMsg(const char* pMsg) const
	{
		if (strcmp("Undo", pMsg) == 0)
		{
			return true;
		}
		else if (strcmp("Redo", pMsg) == 0)
		{
			return true;
		}
		else if (strcmp("ContourImageMod", pMsg) == 0)
		{
			if (contourStateGetter->enabled())
				return true;
		}
		else if (strcmp("ContourLineMod", pMsg) == 0)
		{
			if (contourStateGetter->enabled())
				return true;
		}
		else if (strcmp("PlotDisplayMod", pMsg) == 0) {
			return true;
		}
		else if (strcmp("AutoMax", pMsg) == 0) {
			return true;
		}
		return false;
	}

}
#include "moc_PlotMDIView.cpp"