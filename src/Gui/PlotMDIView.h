#pragma once
#ifndef _PLOTMDIVIEW_H_
#define _PLOTMDIVIEW_H_
#include "PreCompiled.h"
#include "MDIEditView.h"
#include <boost/shared_ptr.hpp>
#include <boost/signals.hpp>
#include <boost/signals2.hpp>
namespace DV
{
	class Plot;
};
namespace Gui{
	
	class MDIView;
	class GuiExport PlotMDIView :public MDIViewPIC
	{
		Q_OBJECT
			TYPESYSTEM_HEADER();
	public:
		PlotMDIView(DocumentPic *_doc, QWidget* parent = 0);
		~PlotMDIView();
		DV::Plot* GetViewPtr();
		virtual bool onMsg(const char* pMsg, const char** ppReturn) override;
		virtual bool onHasMsg(const char* pMsg) const override;

		//ªÒ»°plot÷∏’Î
		DV::Plot* getPlot() {
			return plot;
		}
	protected:
		void resizeEvent(QResizeEvent*);
	private:
		DV::Plot* plot;
	};
}
#endif