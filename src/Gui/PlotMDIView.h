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
	public:
		PlotMDIView(App::Document &_doc, QWidget* parent = 0);
		~PlotMDIView();
		void* GetViewPtr();
	protected:
		void resizeEvent(QResizeEvent*);
	private:
		Plot* plot;
	};
}
#endif