#pragma once
#ifndef _PLOTMDIVIEW_H_
#define _PLOTMDIVIEW_H_
#include "PreCompiled.h"
#include "MDIView.h"
#include <boost/shared_ptr.hpp>
#include <boost/signals.hpp>
#include <boost/signals2.hpp>
class Plot;
namespace Gui{
	
	class MDIView;
	class GuiExport PlotMDIView :public MDIView
	{
		Q_OBJECT
			TYPESYSTEM_HEADER();
	public:
		PlotMDIView(Gui::Document &_doc, QWidget* parent = 0);
		~PlotMDIView();
		Plot* GetViewPtr();
		bool canClose() override;

		virtual bool onMsg(const char* pMsg, const char** ppReturn) override;
		virtual bool onHasMsg(const char* pMsg) const override;

		//ªÒ»°plot÷∏’Î
		Plot* getPlot() {
			return plot;
		}
	protected:
		void resizeEvent(QResizeEvent*);
	private:
		Plot* plot;
	};
}
#endif