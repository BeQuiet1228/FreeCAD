#include "PreCompiled.h"
#include "PlotMDIView.h"
#include "DataVisualization/Plot.h"
#include "View3dMDI.h"
#include "DataVisualization/C_encoding.h"
#include "QMessageBox"
TYPESYSTEM_SOURCE_ABSTRACT(Gui::PlotMDIView, Gui::MDIView);
namespace Gui{
	/**
	* @brief PlotMDIView::PlotMDIView 构造函数
	* @param App::Document &_doc
	* @param QWidget* parent
	*/
	PlotMDIView::PlotMDIView(DocumentPic *_doc, QWidget* parent) :MDIViewPIC(_doc, parent)
	{
		plot = new Plot(this);
		plot->resize(this->size());
		//bIsPassive = false;
		setWindowTitle(QString::fromStdString("chart"));
	}
	PlotMDIView::~PlotMDIView(){    
 	}
	/**
	* @brief PlotMDIView::GetViewPtr 获取plot控件的指针
	* @return void 
	*/
	Plot* PlotMDIView::GetViewPtr()
	{
		return plot;
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
		if (!bIsPassive && getGuiDocument() && getGuiDocument()->isLastView()) {
			this->setFocus(); // raises the view to front
			//需要关闭工程
			auto result = QMessageBox::information(
				nullptr,
				GetEncodingstr("chart",ENCODING_GB2312),
				GetEncodingstr("关闭当前页面会关闭该工程,是否关闭?",ENCODING_GB2312),
				QMessageBox::Yes|QMessageBox::No);
			switch (result)
			{
			case QMessageBox::Yes:
			{
				return (getGuiDocument()->canClose());
			}
			case QMessageBox::No:
			{
				return false;
			}
				break;
			default:
				break;
			}
			
		}
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

		return getDocumengPic()->onMsg(pMsg, ppReturn);
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
		else if (strcmp("PlotDisplayMod", pMsg) == 0) {
			return true;
		}
		else if (strcmp("AutoMax", pMsg) == 0) {
			return true;
		}else if (strcmp("PlotDataExport", pMsg) == 0) {
			return true;
		}else if (strcmp("PlotEqualProportion", pMsg) == 0) {
			return true;
		}else if (strcmp("RunChipic", pMsg) == 0) {
			auto doc = getAppDocument();
			if (doc->classID == 5)
				return false;
			return true;
		}

		return getDocumengPic()->onHasMsg(pMsg);
	}

}
#include "moc_PlotMDIView.cpp"